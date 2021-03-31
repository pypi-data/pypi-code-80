from anndata import AnnData as _AnnData
import scipy as _sp
import numpy as _np
import scanpy as _sc
from scipy.sparse import issparse as _issparse, csr as _csr
from scanpy.neighbors import _compute_connectivities_umap


def ftt(data, reversed=False, copy=False, correction=-1):
    """
    Freeman-Tukey transform (FTT), y = √(x) + √(x + 1) + correction

    reversed this is x = (y - correction)^2 - 1

    correction is default -1 to preserve sparse data.
    """

    if isinstance(data, _AnnData):
        copy = True if data.is_view else copy
        if data.is_view:
            print('Data is view. Making a copy.')
        adata = data.copy() if copy else data

        ftt(adata.X, reversed=reversed, copy=False)
        return adata if copy else None

    X = data.copy() if copy else data

    if _issparse(X):
        X.data = _np.sqrt(X.data) + _np.sqrt(X.data + 1) + correction

    else:
        X = _np.sqrt(X) + _np.sqrt(X + 1) + correction

    if reversed:
        raise NotImplementedError
        # X[nnz] = _sp.square(X[nnz] - correction) - 1

    return X if copy else None


def convert_graph2DnC(graph, mask, nobs):

    I, D, N = get_indices_distances_from_sparse_matrix(graph, mask)
    # nobs = self._data.shape[0]
    DD, CC = _compute_connectivities_umap(I, D, nobs, N)

    return DD, CC


def get_indices_distances_from_sparse_matrix(D, con):
    n_neighbors = max([i.data.shape[0] for i in con]) + 1
    indices = _np.zeros((con.shape[0], n_neighbors), dtype=int) - 1
    distances = _np.zeros((D.shape[0], n_neighbors), dtype=D.dtype) - 1
    n_neighbors_m1 = n_neighbors - 1
    for i in range(indices.shape[0]):
        neighbors = con[i].nonzero()  # 'true' and 'spurious' zeros
        indices[i, 0] = i
        distances[i, 0] = 0
        # account for the fact that there might be more than n_neighbors
        # due to an approximate search
        # [the point itself was not detected as its own neighbor during the search]
        if len(neighbors[1]) > n_neighbors_m1:
            sorted_indices = _np.argsort(D[i][neighbors].A1)[:n_neighbors_m1]
            indices[i, 1:] = neighbors[1][sorted_indices]
            distances[i, 1:] = D[i][
                neighbors[0][sorted_indices], neighbors[1][sorted_indices]]
        else:
            indices[i, 1:(len(neighbors[1]) + 1)] = neighbors[1]
            distances[i, 1:(len(neighbors[1]) + 1)] = D[i][neighbors]

    return indices, distances, n_neighbors


def denoise_values(data, col_name, modest=None, copy=False):

    def _row_stochastic(C):
        cs = C.sum(1)
        cs[cs == 0] = 1
        if _issparse(C):
            C = C.multiply(1. / cs)
            C.eliminate_zeros()
            C = _csr.csr_matrix(C)
        else:
            # https://stackoverflow.com/questions/18522216/multiplying-across-in-a-numpy-array
            C = C * (1. / cs)[:, _sp.newaxis]

        return C

    if isinstance(data, _AnnData):
        adata = data.copy() if copy else data

    col = adata.obs[col_name].astype(float)

    C = adata.uns['dewakss']['Ms']['dewakss_connectivities'].copy()

    if modest is not None:
        modest_adjust(C, modest)

    isna = ~col.isna().values
    C = C[:, isna]
    if modest is not None:
        C = _row_stochastic(C)

    new_col = C @ col[isna].values

    adata.obs['dwks_' + col_name] = new_col

    return adata if copy else None


def modest_adjust(C, modest):

    if isinstance(modest, (int, float)):
        if _issparse(C):
            C.setdiag(modest)
        else:
            _np.fill_diagonal(C, modest)
    elif isinstance(modest, str):
        vecvals = []
        for row in C:
            method = getattr(_np, modest)
            vals = method(row.data)
            vecvals.append(vals)
        vecvals = _sp.sparse.spdiags(vecvals, 0, len(vecvals), len(vecvals))
        C = C + vecvals
    else:
        if modest:
            vecvals = C.astype(bool).sum(1).A1
            vecvals = _sp.sparse.spdiags(1 / vecvals, 0, len(vecvals), len(vecvals))
            C = C + vecvals


def calc_metrics(T, P=None):
    """Calculate MSE and R2,

    Only seem to be faster than the sklearn if both matrices are sparse.
    Of course sklearn computes the wrong MSE if that is the case."""

    M, N = T.shape
    if P is None:
        P = _csr.csr_matrix((M, N))

    sstot_cells = _sp.array([((i.A - i.mean() if _issparse(i) else i - i.mean()).flatten()**2).sum() for i in T])
    sstot = _sp.sum(sstot_cells)

    if any([not _issparse(T), not _issparse(P)]):
        __ = _np.power(((T.A if _issparse(T) else T) - (P.A if _issparse(P) else P)), 2)
        ssres_cells = (__).sum(1)
        ssres = ssres_cells.sum()
    else:
        ssres_cells = _sp.sparse.csr_matrix.power((T - P), 2).sum(1).A1
        ssres = ssres_cells.sum()

    mse = ssres / _sp.prod([M, N])
    msec = ssres_cells / N

    r2 = 1 - ssres / sstot
    r2c = 1 - ssres_cells / sstot_cells

    return mse, r2, msec, r2c


def select_distances(dist, n_neighbors=None):
    D = dist.copy()
    n_counts = (D > 0).sum(1).A1 if _issparse(D) else (D > 0).sum(1)
    n_neighbors = (
        n_counts.min() if n_neighbors is None else min(n_counts.min(), n_neighbors)
    )
    rows = _np.where(n_counts > n_neighbors)[0]
    cumsum_neighs = _np.insert(n_counts.cumsum(), 0, 0)
    dat = D.data

    for row in rows:
        n0, n1 = cumsum_neighs[row], cumsum_neighs[row + 1]
        rm_idx = n0 + dat[n0:n1].argsort()[n_neighbors:]
        dat[rm_idx] = 0
    D.eliminate_zeros()
    return D


def select_connectivities(connectivities, n_neighbors=None):
    C = connectivities.copy()
    n_counts = (C > 0).sum(1).A1 if _issparse(C) else (C > 0).sum(1)
    n_neighbors = (
        n_counts.min() if n_neighbors is None else min(n_counts.min(), n_neighbors)
    )
    rows = _np.where(n_counts > n_neighbors)[0]
    cumsum_neighs = _np.insert(n_counts.cumsum(), 0, 0)
    dat = C.data

    for row in rows:
        n0, n1 = cumsum_neighs[row], cumsum_neighs[row + 1]
        rm_idx = n0 + dat[n0:n1].argsort()[::-1][n_neighbors:]
        dat[rm_idx] = 0
    C.eliminate_zeros()
    return C


def select_neighbors(dist, n_neighbors=None):
    D = dist.copy()
    n_counts = (D > 0).sum(1).A1 if _issparse(D) else (D > 0).sum(1)
    n_neighbors = (
        n_counts.min() if n_neighbors is None else min(n_counts.min(), n_neighbors)
    )
    rows = _np.where(n_counts > n_neighbors)[0]
    cumsum_neighs = _np.insert(n_counts.cumsum(), 0, 0)
    dat = D.data

    for row in rows:
        n0, n1 = cumsum_neighs[row], cumsum_neighs[row + 1]
        remove = len(dat[n0:n1]) - n_neighbors

        rm_idx = n0 + dat[n0:n1].argsort()[:remove]
        dat[rm_idx] = 0
    D.eliminate_zeros()
    return D


def impose_mask(graph, mask):

    graph = graph.multiply(mask)
    graph.eliminate_zeros()
    graph = _csr.csr_matrix(graph)

    return graph


def mask_connections(data, prior_mask, graph_name=None, prior_name='mask', copy=False, var=True, mask_what='dewakss_key', random_state=0, hires=True):

    if isinstance(data, _AnnData):
        adata = data.copy() if copy else data

        if graph_name is None:
            raise Exception("graph_name needs to be set to a key in adata.uns.keys()")

        if graph_name not in adata.uns.keys():
            raise Exception("graph_name needs to be set to a key in adata.uns.keys()")

        dd = adata.uns[graph_name][mask_what]
        # cc = adata.uns[graph_name]['connectivities_key']

        adata.uns[f'{prior_name}_{graph_name}'] = adata.uns[graph_name].copy()
        data = adata.varp[dd] if var else adata.obsp[dd]

        masked_graph = mask_connections(data, prior_mask, graph_name=None, prior_name=prior_name)
        dd = adata.uns[graph_name]['distances_key']
        data = adata.varp[dd] if var else adata.obsp[dd]

        nobs = adata.shape[1] if var else adata.shape[0]
        DD, CC = convert_graph2DnC(data, masked_graph, nobs)

        __ = _sc.AnnData()

        if var:
            adata.varp[f'{prior_name}_{graph_name}_distances'] = DD
            adata.varp[f'{prior_name}_{graph_name}_connectivities'] = CC
            adata.varp[f'{prior_name}_{graph_name}_graph'] = masked_graph
            adata.var[f'{prior_name}_{graph_name}_n'] = DD.astype(bool).sum(1).A1
            # _sc.tl.leiden(adata.T, adjacency=CC, key_added=f'{prior_name}_{graph_name}_leiden')
            _sc.tl.leiden(__, adjacency=CC, random_state=random_state)
            adata.var[f'{prior_name}_{graph_name}_leiden'] = __.obs['leiden'].values
            adata.uns[f'{prior_name}_{graph_name}_leiden'] = __.uns['leiden']

            adata.var[f'{prior_name}_{graph_name}_leiden'] = adata.var[f'{prior_name}_{graph_name}_leiden'].astype(str)
            adata.var.loc[DD.astype(bool).sum(1).A1 == 0, f'{prior_name}_{graph_name}_leiden'] = '-1'

            if hires:

                _sc.tl.leiden(__, adjacency=CC, random_state=random_state, resolution=2)
                adata.var[f'{prior_name}_{graph_name}_hires_leiden'] = __.obs['leiden'].values
                adata.uns[f'{prior_name}_{graph_name}_hires_leiden'] = __.uns['leiden']

                adata.var[f'{prior_name}_{graph_name}_hires_leiden'] = adata.var[f'{prior_name}_{graph_name}_hires_leiden'].astype(str)
                adata.var.loc[DD.astype(bool).sum(1).A1 == 0, f'{prior_name}_{graph_name}_hires_leiden'] = '-1'

        else:
            adata.obsp[f'{prior_name}_{graph_name}_distances'] = DD
            adata.obsp[f'{prior_name}_{graph_name}_connectivities'] = CC
            adata.obsp[f'{prior_name}_{graph_name}_graph'] = masked_graph
            adata.obs[f'{prior_name}_{graph_name}_n'] = DD.astype(bool).sum(1).A1
            _sc.tl.leiden(__, adjacency=CC, random_state=random_state)
            adata.obs[f'{prior_name}_{graph_name}_leiden'] = __.obs['leiden'].values
            adata.uns[f'{prior_name}_{graph_name}_leiden'] = __.uns['leiden']

            adata.obs[f'{prior_name}_{graph_name}_leiden'] = adata.obs[f'{prior_name}_{graph_name}_leiden'].astype(str)
            adata.obs.loc[DD.astype(bool).sum(1).A1 == 0, f'{prior_name}_{graph_name}_leiden'] = '-1'

            if hires:

                _sc.tl.leiden(__, adjacency=CC, random_state=random_state, resolution=2)
                adata.obs[f'{prior_name}_{graph_name}_hires_leiden'] = __.obs['leiden'].values
                adata.uns[f'{prior_name}_{graph_name}_hires_leiden'] = __.uns['leiden']

                adata.obs[f'{prior_name}_{graph_name}_hires_leiden'] = adata.obs[f'{prior_name}_{graph_name}_hires_leiden'].astype(str)
                adata.obs.loc[DD.astype(bool).sum(1).A1 == 0, f'{prior_name}_{graph_name}_hires_leiden'] = '-1'

        adata.uns[f'{prior_name}_{graph_name}']['connectivities_key'] = f'{prior_name}_{graph_name}_connectivities'
        adata.uns[f'{prior_name}_{graph_name}']['distances_key'] = f'{prior_name}_{graph_name}_distances'
        adata.uns[f'{prior_name}_{graph_name}']['dewakss_key'] = f'{prior_name}_{graph_name}_graph'

        # data = adata.varp[cc] if var else adata.obsp[cc]
        # masked_graph = mask_connections(data, prior_mask, graph_name=None, prior_name=prior_name)

        adata._sanitize()

        return adata if copy else None

    masked_graph = impose_mask(data, prior_mask)
    return masked_graph
