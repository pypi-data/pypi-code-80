from collections.abc import Mapping
from io import BytesIO
from warnings import warn, catch_warnings, simplefilter

try:
    import psutil
except ImportError:
    psutil = None

from fsspec.core import open as open_file, open_files
import numpy as np
import pandas as pd
from pandas.api.types import (
    is_integer_dtype,
    is_float_dtype,
    is_object_dtype,
    is_datetime64_any_dtype,
    CategoricalDtype,
)

from ...base import tokenize
from ...bytes import read_bytes
from ..core import new_dd_object
from ...core import flatten
from ...delayed import delayed
from ...utils import asciitable, parse_bytes
from ..utils import clear_known_categories

import fsspec.implementations.local
from fsspec.compression import compr
from fsspec.core import get_fs_token_paths
from fsspec.utils import infer_compression


class CSVSubgraph(Mapping):
    """
    Subgraph for reading CSV files.
    """

    def __init__(
        self,
        name,
        reader,
        blocks,
        is_first,
        head,
        header,
        kwargs,
        dtypes,
        columns,
        enforce,
        path,
    ):
        self.name = name
        self.reader = reader
        self.blocks = blocks
        self.is_first = is_first
        self.head = head  # example pandas DF for metadata
        self.header = header  # prepend to all blocks
        self.kwargs = kwargs
        self.dtypes = dtypes
        self.columns = columns
        self.enforce = enforce
        self.colname, self.paths = path or (None, None)

    def __getitem__(self, key):
        try:
            name, i = key
        except ValueError:
            # too many / few values to unpack
            raise KeyError(key) from None

        if name != self.name:
            raise KeyError(key)

        if i < 0 or i >= len(self.blocks):
            raise KeyError(key)

        block = self.blocks[i]
        if self.paths is not None:
            path_info = (
                self.colname,
                self.paths[i],
                sorted(list(self.head[self.colname].cat.categories)),
            )
        else:
            path_info = None

        write_header = False
        rest_kwargs = self.kwargs.copy()
        if not self.is_first[i]:
            write_header = True
            rest_kwargs.pop("skiprows", None)

        return (
            pandas_read_text,
            self.reader,
            block,
            self.header,
            rest_kwargs,
            self.dtypes,
            self.columns,
            write_header,
            self.enforce,
            path_info,
        )

    def __len__(self):
        return len(self.blocks)

    def __iter__(self):
        for i in range(len(self)):
            yield (self.name, i)


def pandas_read_text(
    reader,
    b,
    header,
    kwargs,
    dtypes=None,
    columns=None,
    write_header=True,
    enforce=False,
    path=None,
):
    """Convert a block of bytes to a Pandas DataFrame

    Parameters
    ----------
    reader : callable
        ``pd.read_csv`` or ``pd.read_table``.
    b : bytestring
        The content to be parsed with ``reader``
    header : bytestring
        An optional header to prepend to ``b``
    kwargs : dict
        A dictionary of keyword arguments to be passed to ``reader``
    dtypes : dict
        DTypes to assign to columns
    path : tuple
        A tuple containing path column name, path to file, and an ordered list of paths.

    See Also
    --------
    dask.dataframe.csv.read_pandas_from_bytes
    """
    bio = BytesIO()
    if write_header and not b.startswith(header.rstrip()):
        bio.write(header)
    bio.write(b)
    bio.seek(0)
    df = reader(bio, **kwargs)
    if dtypes:
        coerce_dtypes(df, dtypes)

    if enforce and columns and (list(df.columns) != list(columns)):
        raise ValueError("Columns do not match", df.columns, columns)
    elif columns:
        df.columns = columns
    if path:
        colname, path, paths = path
        code = paths.index(path)
        df = df.assign(
            **{colname: pd.Categorical.from_codes(np.full(len(df), code), paths)}
        )
    return df


def coerce_dtypes(df, dtypes):
    """Coerce dataframe to dtypes safely

    Operates in place

    Parameters
    ----------
    df: Pandas DataFrame
    dtypes: dict like {'x': float}
    """
    bad_dtypes = []
    bad_dates = []
    errors = []
    for c in df.columns:
        if c in dtypes and df.dtypes[c] != dtypes[c]:
            actual = df.dtypes[c]
            desired = dtypes[c]
            if is_float_dtype(actual) and is_integer_dtype(desired):
                bad_dtypes.append((c, actual, desired))
            elif is_object_dtype(actual) and is_datetime64_any_dtype(desired):
                # This can only occur when parse_dates is specified, but an
                # invalid date is encountered. Pandas then silently falls back
                # to object dtype. Since `object_array.astype(datetime)` will
                # silently overflow, error here and report.
                bad_dates.append(c)
            else:
                try:
                    df[c] = df[c].astype(dtypes[c])
                except Exception as e:
                    bad_dtypes.append((c, actual, desired))
                    errors.append((c, e))

    if bad_dtypes:
        if errors:
            ex = "\n".join(
                "- %s\n  %r" % (c, e)
                for c, e in sorted(errors, key=lambda x: str(x[0]))
            )
            exceptions = (
                "The following columns also raised exceptions on "
                "conversion:\n\n%s\n\n"
            ) % ex
            extra = ""
        else:
            exceptions = ""
            # All mismatches are int->float, also suggest `assume_missing=True`
            extra = (
                "\n\nAlternatively, provide `assume_missing=True` "
                "to interpret\n"
                "all unspecified integer columns as floats."
            )

        bad_dtypes = sorted(bad_dtypes, key=lambda x: str(x[0]))
        table = asciitable(["Column", "Found", "Expected"], bad_dtypes)
        dtype_kw = "dtype={%s}" % ",\n       ".join(
            "%r: '%s'" % (k, v) for (k, v, _) in bad_dtypes
        )

        dtype_msg = (
            "{table}\n\n"
            "{exceptions}"
            "Usually this is due to dask's dtype inference failing, and\n"
            "*may* be fixed by specifying dtypes manually by adding:\n\n"
            "{dtype_kw}\n\n"
            "to the call to `read_csv`/`read_table`."
            "{extra}"
        ).format(table=table, exceptions=exceptions, dtype_kw=dtype_kw, extra=extra)
    else:
        dtype_msg = None

    if bad_dates:
        also = " also " if bad_dtypes else " "
        cols = "\n".join("- %s" % c for c in bad_dates)
        date_msg = (
            "The following columns{also}failed to properly parse as dates:\n\n"
            "{cols}\n\n"
            "This is usually due to an invalid value in that column. To\n"
            "diagnose and fix it's recommended to drop these columns from the\n"
            "`parse_dates` keyword, and manually convert them to dates later\n"
            "using `dd.to_datetime`."
        ).format(also=also, cols=cols)
    else:
        date_msg = None

    if bad_dtypes or bad_dates:
        rule = "\n\n%s\n\n" % ("-" * 61)
        msg = "Mismatched dtypes found in `pd.read_csv`/`pd.read_table`.\n\n%s" % (
            rule.join(filter(None, [dtype_msg, date_msg]))
        )
        raise ValueError(msg)


def text_blocks_to_pandas(
    reader,
    block_lists,
    header,
    head,
    kwargs,
    enforce=False,
    specified_dtypes=None,
    path=None,
    blocksize=None,
):
    """Convert blocks of bytes to a dask.dataframe

    This accepts a list of lists of values of bytes where each list corresponds
    to one file, and the value of bytes concatenate to comprise the entire
    file, in order.

    Parameters
    ----------
    reader : callable
        ``pd.read_csv`` or ``pd.read_table``.
    block_lists : list of lists of delayed values of bytes
        The lists of bytestrings where each list corresponds to one logical file
    header : bytestring
        The header, found at the front of the first file, to be prepended to
        all blocks
    head : pd.DataFrame
        An example Pandas DataFrame to be used for metadata.
    kwargs : dict
        Keyword arguments to pass down to ``reader``
    path : tuple, optional
        A tuple containing column name for path and the path_converter if provided

    Returns
    -------
    A dask.dataframe
    """
    dtypes = head.dtypes.to_dict()
    # dtypes contains only instances of CategoricalDtype, which causes issues
    # in coerce_dtypes for non-uniform categories across partitions.
    # We will modify `dtype` (which is inferred) to
    # 1. contain instances of CategoricalDtypes for user-provided types
    # 2. contain 'category' for data inferred types
    categoricals = head.select_dtypes(include=["category"]).columns

    if isinstance(specified_dtypes, Mapping):
        known_categoricals = [
            k
            for k in categoricals
            if isinstance(specified_dtypes.get(k), CategoricalDtype)
            and specified_dtypes.get(k).categories is not None
        ]
        unknown_categoricals = categoricals.difference(known_categoricals)
    else:
        unknown_categoricals = categoricals

    # Fixup the dtypes
    for k in unknown_categoricals:
        dtypes[k] = "category"

    columns = list(head.columns)

    blocks = tuple(flatten(block_lists))
    # Create mask of first blocks from nested block_lists
    is_first = tuple(block_mask(block_lists))

    name = "read-csv-" + tokenize(reader, columns, enforce, head, blocksize)

    if path:
        colname, path_converter = path
        paths = [b[1].path for b in blocks]
        if path_converter:
            paths = [path_converter(p) for p in paths]
        head = head.assign(
            **{
                colname: pd.Categorical.from_codes(
                    np.zeros(len(head), dtype=int), set(paths)
                )
            }
        )
        path = (colname, paths)

    if len(unknown_categoricals):
        head = clear_known_categories(head, cols=unknown_categoricals)

    subgraph = CSVSubgraph(
        name,
        reader,
        blocks,
        is_first,
        head,
        header,
        kwargs,
        dtypes,
        columns,
        enforce,
        path,
    )

    return new_dd_object(subgraph, name, head, (None,) * (len(blocks) + 1))


def block_mask(block_lists):
    """
    Yields a flat iterable of booleans to mark the zeroth elements of the
    nested input ``block_lists`` in a flattened output.

    >>> list(block_mask([[1, 2], [3, 4], [5]]))
    [True, False, True, False, True]
    """
    for block in block_lists:
        if not block:
            continue
        yield True
        yield from (False for _ in block[1:])


def auto_blocksize(total_memory, cpu_count):
    memory_factor = 10
    blocksize = int(total_memory // cpu_count / memory_factor)
    return min(blocksize, int(64e6))


# guess blocksize if psutil is installed or use acceptable default one if not
if psutil is not None:
    with catch_warnings():
        simplefilter("ignore", RuntimeWarning)
        TOTAL_MEM = psutil.virtual_memory().total
        CPU_COUNT = psutil.cpu_count()
        AUTO_BLOCKSIZE = auto_blocksize(TOTAL_MEM, CPU_COUNT)
else:
    AUTO_BLOCKSIZE = 2 ** 25


def read_pandas(
    reader,
    urlpath,
    blocksize="default",
    lineterminator=None,
    compression="infer",
    sample=256000,
    enforce=False,
    assume_missing=False,
    storage_options=None,
    include_path_column=False,
    **kwargs,
):
    reader_name = reader.__name__
    if lineterminator is not None and len(lineterminator) == 1:
        kwargs["lineterminator"] = lineterminator
    else:
        lineterminator = "\n"
    if include_path_column and isinstance(include_path_column, bool):
        include_path_column = "path"
    if "index" in kwargs or "index_col" in kwargs:
        raise ValueError(
            "Keywords 'index' and 'index_col' not supported. "
            "Use dd.{0}(...).set_index('my-index') "
            "instead".format(reader_name)
        )
    for kw in ["iterator", "chunksize"]:
        if kw in kwargs:
            raise ValueError("{0} not supported for dd.{1}".format(kw, reader_name))
    if kwargs.get("nrows", None):
        raise ValueError(
            "The 'nrows' keyword is not supported by "
            "`dd.{0}`. To achieve the same behavior, it's "
            "recommended to use `dd.{0}(...)."
            "head(n=nrows)`".format(reader_name)
        )
    if isinstance(kwargs.get("skiprows"), int):
        skiprows = lastskiprow = firstrow = kwargs.get("skiprows")
    elif kwargs.get("skiprows") is None:
        skiprows = lastskiprow = firstrow = 0
    else:
        # When skiprows is a list, we expect more than max(skiprows) to
        # be included in the sample. This means that [0,2] will work well,
        # but [0, 440] might not work.
        skiprows = set(kwargs.get("skiprows"))
        lastskiprow = max(skiprows)
        # find the firstrow that is not skipped, for use as header
        firstrow = min(set(range(len(skiprows) + 1)) - set(skiprows))
    if isinstance(kwargs.get("header"), list):
        raise TypeError(
            "List of header rows not supported for dd.{0}".format(reader_name)
        )
    if isinstance(kwargs.get("converters"), dict) and include_path_column:
        path_converter = kwargs.get("converters").get(include_path_column, None)
    else:
        path_converter = None

    # If compression is "infer", inspect the (first) path suffix and
    # set the proper compression option if the suffix is recongnized.
    if compression == "infer":
        # Translate the input urlpath to a simple path list
        paths = get_fs_token_paths(urlpath, mode="rb", storage_options=storage_options)[
            2
        ]

        # Infer compression from first path
        compression = infer_compression(paths[0])

    if blocksize == "default":
        blocksize = AUTO_BLOCKSIZE
    if isinstance(blocksize, str):
        blocksize = parse_bytes(blocksize)
    if blocksize and compression:
        # NONE of the compressions should use chunking
        warn(
            "Warning %s compression does not support breaking apart files\n"
            "Please ensure that each individual file can fit in memory and\n"
            "use the keyword ``blocksize=None to remove this message``\n"
            "Setting ``blocksize=None``" % compression
        )
        blocksize = None
    if compression not in compr:
        raise NotImplementedError("Compression format %s not installed" % compression)
    if blocksize and sample and blocksize < sample and lastskiprow != 0:
        warn(
            "Unexpected behavior can result from passing skiprows when\n"
            "blocksize is smaller than sample size.\n"
            "Setting ``sample=blocksize``"
        )
        sample = blocksize
    b_lineterminator = lineterminator.encode()
    b_out = read_bytes(
        urlpath,
        delimiter=b_lineterminator,
        blocksize=blocksize,
        sample=sample,
        compression=compression,
        include_path=include_path_column,
        **(storage_options or {}),
    )

    if include_path_column:
        b_sample, values, paths = b_out
        path = (include_path_column, path_converter)
    else:
        b_sample, values = b_out
        path = None

    if not isinstance(values[0], (tuple, list)):
        values = [values]
    # If we have not sampled, then use the first row of the first values
    # as a representative sample.
    if b_sample is False and len(values[0]):
        b_sample = values[0][0].compute()

    # Get header row, and check that sample is long enough. If the file
    # contains a header row, we need at least 2 nonempty rows + the number of
    # rows to skip.
    names = kwargs.get("names", None)
    header = kwargs.get("header", "infer" if names is None else None)
    need = 1 if header is None else 2
    parts = b_sample.split(b_lineterminator, lastskiprow + need)
    # If the last partition is empty, don't count it
    nparts = 0 if not parts else len(parts) - int(not parts[-1])

    if sample is not False and nparts < lastskiprow + need and len(b_sample) >= sample:
        raise ValueError(
            "Sample is not large enough to include at least one "
            "row of data. Please increase the number of bytes "
            "in `sample` in the call to `read_csv`/`read_table`"
        )

    header = b"" if header is None else parts[firstrow] + b_lineterminator

    # Use sample to infer dtypes and check for presence of include_path_column
    head = reader(BytesIO(b_sample), **kwargs)
    if include_path_column and (include_path_column in head.columns):
        raise ValueError(
            "Files already contain the column name: %s, so the "
            "path column cannot use this name. Please set "
            "`include_path_column` to a unique name." % include_path_column
        )

    specified_dtypes = kwargs.get("dtype", {})
    if specified_dtypes is None:
        specified_dtypes = {}
    # If specified_dtypes is a single type, then all columns were specified
    if assume_missing and isinstance(specified_dtypes, dict):
        # Convert all non-specified integer columns to floats
        for c in head.columns:
            if is_integer_dtype(head[c].dtype) and c not in specified_dtypes:
                head[c] = head[c].astype(float)

    values = [[list(dsk.dask.values()) for dsk in block] for block in values]

    return text_blocks_to_pandas(
        reader,
        values,
        header,
        head,
        kwargs,
        enforce=enforce,
        specified_dtypes=specified_dtypes,
        path=path,
        blocksize=blocksize,
    )


READ_DOC_TEMPLATE = """
Read {file_type} files into a Dask.DataFrame

This parallelizes the :func:`pandas.{reader}` function in the following ways:

- It supports loading many files at once using globstrings:

    >>> df = dd.{reader}('myfiles.*.csv')  # doctest: +SKIP

- In some cases it can break up large files:

    >>> df = dd.{reader}('largefile.csv', blocksize=25e6)  # 25MB chunks  # doctest: +SKIP

- It can read CSV files from external resources (e.g. S3, HDFS) by
  providing a URL:

    >>> df = dd.{reader}('s3://bucket/myfiles.*.csv')  # doctest: +SKIP
    >>> df = dd.{reader}('hdfs:///myfiles.*.csv')  # doctest: +SKIP
    >>> df = dd.{reader}('hdfs://namenode.example.com/myfiles.*.csv')  # doctest: +SKIP

Internally ``dd.{reader}`` uses :func:`pandas.{reader}` and supports many of the
same keyword arguments with the same performance guarantees. See the docstring
for :func:`pandas.{reader}` for more information on available keyword arguments.

Parameters
----------
urlpath : string or list
    Absolute or relative filepath(s). Prefix with a protocol like ``s3://``
    to read from alternative filesystems. To read from multiple files you
    can pass a globstring or a list of paths, with the caveat that they
    must all have the same protocol.
blocksize : str, int or None, optional
    Number of bytes by which to cut up larger files. Default value is computed
    based on available physical memory and the number of cores, up to a maximum
    of 64MB. Can be a number like ``64000000` or a string like ``"64MB"``. If
    ``None``, a single block is used for each file.
sample : int, optional
    Number of bytes to use when determining dtypes
assume_missing : bool, optional
    If True, all integer columns that aren't specified in ``dtype`` are assumed
    to contain missing values, and are converted to floats. Default is False.
storage_options : dict, optional
    Extra options that make sense for a particular storage connection, e.g.
    host, port, username, password, etc.
include_path_column : bool or str, optional
    Whether or not to include the path to each particular file. If True a new
    column is added to the dataframe called ``path``. If str, sets new column
    name. Default is False.
**kwargs
    Extra keyword arguments to forward to :func:`pandas.{reader}`.

Notes
-----
Dask dataframe tries to infer the ``dtype`` of each column by reading a sample
from the start of the file (or of the first file if it's a glob). Usually this
works fine, but if the ``dtype`` is different later in the file (or in other
files) this can cause issues. For example, if all the rows in the sample had
integer dtypes, but later on there was a ``NaN``, then this would error at
compute time. To fix this, you have a few options:

- Provide explicit dtypes for the offending columns using the ``dtype``
  keyword. This is the recommended solution.

- Use the ``assume_missing`` keyword to assume that all columns inferred as
  integers contain missing values, and convert them to floats.

- Increase the size of the sample using the ``sample`` keyword.

It should also be noted that this function may fail if a {file_type} file
includes quoted strings that contain the line terminator. To get around this
you can specify ``blocksize=None`` to not split files into multiple partitions,
at the cost of reduced parallelism.
"""


def make_reader(reader, reader_name, file_type):
    def read(
        urlpath,
        blocksize="default",
        lineterminator=None,
        compression="infer",
        sample=256000,
        enforce=False,
        assume_missing=False,
        storage_options=None,
        include_path_column=False,
        **kwargs,
    ):
        return read_pandas(
            reader,
            urlpath,
            blocksize=blocksize,
            lineterminator=lineterminator,
            compression=compression,
            sample=sample,
            enforce=enforce,
            assume_missing=assume_missing,
            storage_options=storage_options,
            include_path_column=include_path_column,
            **kwargs,
        )

    read.__doc__ = READ_DOC_TEMPLATE.format(reader=reader_name, file_type=file_type)
    read.__name__ = reader_name
    return read


read_csv = make_reader(pd.read_csv, "read_csv", "CSV")
read_table = make_reader(pd.read_table, "read_table", "delimited")
read_fwf = make_reader(pd.read_fwf, "read_fwf", "fixed-width")


def _write_csv(df, fil, *, depend_on=None, **kwargs):
    with fil as f:
        df.to_csv(f, **kwargs)
    return None


def to_csv(
    df,
    filename,
    single_file=False,
    encoding="utf-8",
    mode="wt",
    name_function=None,
    compression=None,
    compute=True,
    scheduler=None,
    storage_options=None,
    header_first_partition_only=None,
    compute_kwargs=None,
    **kwargs,
):
    """
    Store Dask DataFrame to CSV files

    One filename per partition will be created. You can specify the
    filenames in a variety of ways.

    Use a globstring::

    >>> df.to_csv('/path/to/data/export-*.csv')  # doctest: +SKIP

    The * will be replaced by the increasing sequence 0, 1, 2, ...

    ::

        /path/to/data/export-0.csv
        /path/to/data/export-1.csv

    Use a globstring and a ``name_function=`` keyword argument.  The
    name_function function should expect an integer and produce a string.
    Strings produced by name_function must preserve the order of their
    respective partition indices.

    >>> from datetime import date, timedelta
    >>> def name(i):
    ...     return str(date(2015, 1, 1) + i * timedelta(days=1))

    >>> name(0)
    '2015-01-01'
    >>> name(15)
    '2015-01-16'

    >>> df.to_csv('/path/to/data/export-*.csv', name_function=name)  # doctest: +SKIP

    ::

        /path/to/data/export-2015-01-01.csv
        /path/to/data/export-2015-01-02.csv
        ...

    You can also provide an explicit list of paths::

    >>> paths = ['/path/to/data/alice.csv', '/path/to/data/bob.csv', ...]  # doctest: +SKIP
    >>> df.to_csv(paths) # doctest: +SKIP

    Parameters
    ----------
    df : dask.DataFrame
        Data to save
    filename : string
        Path glob indicating the naming scheme for the output files
    single_file : bool, default False
        Whether to save everything into a single CSV file. Under the
        single file mode, each partition is appended at the end of the
        specified CSV file. Note that not all filesystems support the
        append mode and thus the single file mode, especially on cloud
        storage systems such as S3 or GCS. A warning will be issued when
        writing to a file that is not backed by a local filesystem.
    encoding : string, optional
        A string representing the encoding to use in the output file,
        defaults to 'ascii' on Python 2 and 'utf-8' on Python 3.
    mode : str
        Python write mode, default 'w'
    name_function : callable, default None
        Function accepting an integer (partition index) and producing a
        string to replace the asterisk in the given filename globstring.
        Should preserve the lexicographic order of partitions. Not
        supported when `single_file` is `True`.
    compression : string, optional
        a string representing the compression to use in the output file,
        allowed values are 'gzip', 'bz2', 'xz',
        only used when the first argument is a filename
    compute : bool
        If true, immediately executes. If False, returns a set of delayed
        objects, which can be computed at a later time.
    storage_options : dict
        Parameters passed on to the backend filesystem class.
    header_first_partition_only : boolean, default None
        If set to `True`, only write the header row in the first output
        file. By default, headers are written to all partitions under
        the multiple file mode (`single_file` is `False`) and written
        only once under the single file mode (`single_file` is `True`).
        It must not be `False` under the single file mode.
    compute_kwargs : dict, optional
        Options to be passed in to the compute method
    kwargs : dict, optional
        Additional parameters to pass to `pd.DataFrame.to_csv()`

    Returns
    -------
    The names of the file written if they were computed right away
    If not, the delayed tasks associated to the writing of the files

    Raises
    ------
    ValueError
        If `header_first_partition_only` is set to `False` or
        `name_function` is specified when `single_file` is `True`.
    """
    if single_file and name_function is not None:
        raise ValueError("name_function is not supported under the single file mode")
    if header_first_partition_only is None:
        header_first_partition_only = single_file
    elif not header_first_partition_only and single_file:
        raise ValueError(
            "header_first_partition_only cannot be False in the single file mode."
        )
    file_options = dict(
        compression=compression,
        encoding=encoding,
        newline="",
        **(storage_options or {}),
    )
    to_csv_chunk = delayed(_write_csv, pure=False)
    dfs = df.to_delayed()
    if single_file:
        first_file = open_file(filename, mode=mode, **file_options)
        if not isinstance(first_file.fs, fsspec.implementations.local.LocalFileSystem):
            warn("Appending data to a network storage system may not work.")
        value = to_csv_chunk(dfs[0], first_file, **kwargs)
        append_mode = mode.replace("w", "") + "a"
        append_file = open_file(filename, mode=append_mode, **file_options)
        kwargs["header"] = False
        for d in dfs[1:]:
            value = to_csv_chunk(d, append_file, depend_on=value, **kwargs)
        values = [value]
        files = [first_file]
    else:
        files = open_files(
            filename,
            mode=mode,
            name_function=name_function,
            num=df.npartitions,
            **file_options,
        )
        values = [to_csv_chunk(dfs[0], files[0], **kwargs)]
        if header_first_partition_only:
            kwargs["header"] = False
        values.extend(
            [to_csv_chunk(d, f, **kwargs) for d, f in zip(dfs[1:], files[1:])]
        )
    if compute:
        if compute_kwargs is None:
            compute_kwargs = dict()

        if scheduler is not None:
            warn(
                "The 'scheduler' keyword argument for `to_csv()` is deprecated and"
                "will be removed in a future version. "
                "Please use the `compute_kwargs` argument instead. "
                f"For example, df.to_csv(..., compute_kwargs={{scheduler: {scheduler}}})",
                FutureWarning,
            )

        if (
            scheduler is not None
            and compute_kwargs.get("scheduler") is not None
            and compute_kwargs.get("scheduler") != scheduler
        ):
            raise ValueError(
                f"Differing values for 'scheduler' have been passed in.\n"
                f"scheduler argument: {scheduler}\n"
                f"via compute_kwargs: {compute_kwargs.get('scheduler')}"
            )

        if scheduler is not None and compute_kwargs.get("scheduler") is None:
            compute_kwargs["scheduler"] = scheduler

        delayed(values).compute(**compute_kwargs)
        return [f.path for f in files]
    else:
        return values


from ..core import _Frame

_Frame.to_csv.__doc__ = to_csv.__doc__
