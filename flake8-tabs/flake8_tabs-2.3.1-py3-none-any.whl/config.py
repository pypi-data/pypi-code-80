import typing as ty

from . import editorconfig
from . import misc


if ty.TYPE_CHECKING:
	import os


__all__: ty.Final[ty.Tuple[str, ...]] = ("Config",)


# Support for `__class_getitem__` was added in Python 3.7
class ClassGetItemPolyfill(type):
	def __getitem__(self, name: str) -> ty.Union[bool, int, str]:
		return self.__class_getitem__(name)


class Config(metaclass=ClassGetItemPolyfill):
	"""
	Registers the configuration options for the other checkers
	"""
	name: str    = "flake8-tabs"
	version: str = misc.__version__
	
	
	OPTIONS: ty.Final[
		ty.Dict[
			str,  # Field name
			ty.Tuple[
				ty.Union[bool, int, str],  # Default value
				ty.Optional[str],          # EditorConfig option name
			]
		]
	] = {
		# Master switch for the `IndentationChecker` module
		"use-flake8-tabs": (
			False,
			None,
		),
		
		"use-pycodestyle-indent": (
			True,  # + Special default code
			None,
		),
		
		"blank-lines-indent": (
			"keep",
			"trim_trailing_whitespace",  # + Special mapping code
		),
		
		"indent-style": (
			"keep",
			"indent_style",
		),
		
		# Indentation size: Used when requiring further indentation after we already have alignment
		"indent-size": (
			4,
			"indent_size",
		),
		
		# Indentation tabs: The number of tabs, when indenting, to require for the
		#                   first level of indentation of functions calls,
		#                   function/class definitions and other expressions/statements
		
		"indent-levels-call": (
			1,
			None,
		),
		
		"indent-levels-defn": (
			2,  # PEP-8 requires indentation to be distinguishable
			None,
		),
		
		"indent-levels-expr": (
			1,
			None,
		),
		
		# Continuation line style: Which indentation style to allow on continuation lines
		#  * “aligned” means that follow-up lines should be indented by the exact
		#    number of extra spaces required to align them if the previous line's
		#    final opening brace
		#  * “hanging” means that follow-up lines should be indented by a tab
		#  * “both” chooses the allowed indentation style based on whether the
		#    first lines contains any relevant values after the final opening brace
		"continuation-style": (
			"both",
			None,
		),
	}
	
	_option_values: ty.Dict[str, ty.Optional[ty.Union[bool, int, str]]] = {}
	
	
	@classmethod
	def add_options(cls, option_manager):
		# Patch support for indent-size and the use-pycodestyle-indent options into flake8
		from . import monkeypatch
		monkeypatch.patch_flake8()
		
		
		# Indentation style: Tabs or spaces?
		option_manager.add_option(
			"--indent-style", type="choice", metavar="STYLE", parse_from_config=True,
			choices=("tab", "space", "keep"),
			help=(f"The indentation style to enforce on newly opened blocks "
			      f"(Default: `{cls.OPTIONS['indent-style'][1]}` from .editorconfig "
			      f"or {cls.OPTIONS['indent-style'][0]!r})"),
		)
		
		
		# Indentation style options
		option_manager.add_option(
			"--blank-lines-indent", type="choice", metavar="MODE", parse_from_config=True,
			choices=("maybe", "always", "never"),
			help=(f"Whether there should be, properly aligned, indentation in blank lines; "
			      f"\"always\" forces this, \"never\" disallows this (Default: Depends on "
			      f"`{cls.OPTIONS['blank-lines-indent'][1]}` from .editorconfig or "
			      f"{cls.OPTIONS['blank-lines-indent'][0]!r})")
		)
		
		# Patcher options
		option_manager.add_option(
			"--use-flake8-tabs", action="store_true", parse_from_config=True, default=None,
			help=("Use flake8-tabs instead for indentation checking? "
			      "Enabling this will disable PyCodeStyle's indentation checks "
			      "unless you override that behaviour; by default only minimal "
			      "checking will be performed")
		)
		option_manager.add_option(
			"--use-pycodestyle-indent", action="store_true", parse_from_config=True, default=None,
			help=("Force the use of PyCodeStyle's indentation checks even if "
			      "flake8-tabs is enabled")
		)
		
		# First-indentation tab number options
		option_manager.add_option(
			"--indent-tabs-call", type="int", metavar="n", parse_from_config=True,
			dest="indent_levels_call",
			help=(f"Number of tabs to indent on the first level of indentation within a function/"
			      f"method call (Default: {cls.OPTIONS['indent-levels-call'][0]!r})")
		)
		option_manager.add_option(
			"--indent-tabs-def", type="int", metavar="n", parse_from_config=True,
			dest="indent_levels_defn",
			help=(f"Number of tabs to indent on the first level of indentation within a class/"
			      f"function definition (Default: {cls.OPTIONS['indent-levels-defn'][0]!r})")
		)
		option_manager.add_option(
			"--indent-tabs-expr", type="int", metavar="n", parse_from_config=True,
			dest="indent_levels_expr",
			help=(f"Number of tabs to indent on the first level of indentation within an "
			      f"expression (Default: {cls.OPTIONS['indent-levels-expr'][0]!r})")
		)
		
		
		# More rigid style enforcing options
		option_manager.add_option(
			"--continuation-style", type="choice", metavar="STYLE", parse_from_config=True,
			choices=("aligned", "hanging", "both"),
			help=(f"Restrict the allowed continuation line style to either "
			      f"\"hanging\" or \"aligned\"; see the documentation for what "
			      f"this means (Default: {cls.OPTIONS['continuation-style'][0]!r})")
		)
		
		# Prevent conflict with other plugins registering `--tab-width` as well
		for option in option_manager.options:
			if option.dest == "tab_width":
				return
		
		option_manager.add_option(
			"--tab-width", type="int", metavar="n", parse_from_config=True,
			dest="indent_size",
			help=(f"Number of spaces per tab character for line length checking "
			      f"(Default: `{cls.OPTIONS['indent-size'][1]}` from .editorconfig or "
			      f"{cls.OPTIONS['indent-size'][0]!r})"),
		)
	
	@classmethod
	def parse_options(cls, option_manager, options, extra_args) -> None:
		for option_name in cls.OPTIONS.keys():
			cls._option_values[option_name] = getattr(options, option_name.replace("-", "_"))
	
	@classmethod
	def _get_field(cls, field: str, filepath: ty.Union[bytes, str, "os.PathLike", None] = None) \
	    -> ty.Union[bool, int, str]:
		(default, ec_name) = cls.OPTIONS[field]
		
		value: ty.Union[str, int, bool, None] = cls._option_values.get(field)
		if value is not None:
			return value
		
		if ec_name is not None and filepath is not None:
			# While this branch may be run several times in this loop, the
			# result of `query_filepath` is LRU cached so we only read the
			# relevant configuration files at most once per filepath
			#
			# Using an LRU cache on the function has the benefit that it
			# also caches the results between different calls to this
			# function (like when the different checkers of this module
			# are called one after another).
			value = editorconfig.query_filepath(filepath).get(ec_name)
			
			if value is not None:
				# EditorConfig value of some fields requires mapping to obtain
				# the equivalent configuration value
				if field == "blank-lines-indent":
					# `value` here is actually “trim_trailing_whitespace”
					return "never" if value else "always"
				
				return value
		
		# Special default values
		if field == "use-pycodestyle-indent":
			return not cls._get_field("use-flake8-tabs", filepath)
		
		return default
	
	
	@classmethod
	def __class_getitem__(cls, field: str) -> ty.Union[bool, int, str]:
		return cls._get_field(field)
	
	
	@classmethod
	def with_filepath(cls, filepath: ty.Union[bytes, str, "os.PathLike"], *fields: str) \
	    -> ty.Dict[str, ty.Union[bool, int, str]]:
		result: ty.Dict[str, ty.Union[str, int, bool]] = {}
		for field in fields:
			result[field] = cls._get_field(field, filepath)
		return result
	
	def __init__(self, filename: str) -> None:
		pass