import typing as ty

import flake8.checker
import flake8.processor

from . import config


__all__: ty.Final[ty.Tuple[str, ...]] = ("expand_indent", "patch_flake8")


class FileChecker(flake8.checker.FileChecker):
	"""
	Blacklist some `pycodestyle` checks that our plugin will implement instead
	"""
	
	BLACKLIST: ty.Final[ty.FrozenSet[str]] = frozenset({
		# E101 indentation contains mixed spaces and tabs
		#  – Incorrectly reports cases of using tabs for indentation but spaces for alignment
		#    (We have our own checks for cases where the two are mixed, which is still an error.)
		"pycodestyle.tabs_or_spaces",
		
		# E121 continuation line under-indented for hanging indent
		# E122 continuation line missing indentation or outdented
		# E123 closing bracket does not match indentation of opening bracket’s line
		# E126 continuation line over-indented for hanging indent
		# E127 continuation line over-indented for visual indent
		# E128 continuation line under-indented for visual indent
		#  – We handle these ourselves: That's what this checker is about after all
		# E124 closing bracket does not match visual indentation
		# E125 continuation line with same indent as next logical line
		# E129 visually indented line with same indent as next logical line
		# E131 continuation line unaligned for hanging indent
		# E133 closing bracket is missing indentation
		#  – These aren't handled yet but cannot be disabled separately
		"pycodestyle.continued_indentation",
		
		# W191 indentation contains tabs
		#  – Not applicable since we love tabs 🙂️
		"pycodestyle.tabs_obsolete",
		
		# W291 trailing whitespace
		# W293 blank line contains whitespace
		#  – Implemented by `BlankLinesChecker` with more options and saner defaults
		"pycodestyle.trailing_whitespace",
	})
	
	def __init__(self, filename: str, checks: ty.Dict[str, ty.List[str]], options) -> None:
		if not config.Config["use-pycodestyle-indent"]:
			for checks_type in checks:
				checks[checks_type] = list(filter(
					lambda c: c["name"] not in self.BLACKLIST,
					checks[checks_type]
				))
		super().__init__(filename, checks, options)


def expand_indent(line: str) -> int:
	r"""Return the amount of indentation (patched function for `flake8`)
	
	Tabs are expanded to the next multiple of the current tab size.
	
	>>> expand_indent('    ')
	4
	>>> expand_indent('\t')
	4
	>>> expand_indent('   \t')
	4
	>>> expand_indent('    \t')
	8
	"""
	if "\t" not in line:
		return len(line) - len(line.lstrip())
	
	# XXX: Technically this should consider the per-file indent configuration as
	#      well, but its only for pretty-printing and we don't have the filepath
	cfg = {
		"indent-size": config.Config["indent-size"],
	}
	
	result = 0
	for char in line:
		if char == "\t":
			result  = result // cfg["indent-size"] * cfg["indent-size"]
			result += cfg["indent-size"]
		elif char == " ":
			result += 1
		else:
			break
	return result


def patch_flake8() -> None:
	flake8.checker.FileChecker = FileChecker
	flake8.processor.expand_indent = expand_indent