import collections
import itertools
import typing as ty


__all__: ty.Final[ty.Tuple[str, ...]] = (
	"__version__",
	"format_violation",
	"format_warning",
	"map_next",
	"pairwise_fill",
	"parse_indent",
	"Indent",
)
__version__ = "2.3.1"


T = ty.TypeVar("T")
U = ty.TypeVar("U")


def format_violation(code: int, message: str):
	return f"ET{code} (flake8-tabs) {message}"


def format_warning(code: int, message: str):
	return f"WT{code} (flake8-tabs) {message}"


def map_next(pred: ty.Callable[[T], U], *iterable: ty.Iterable[T], default: U = ...) -> U:
	try:
		val = next(itertools.chain.from_iterable(iterable))
	except StopIteration:
		if default is not Ellipsis:
			return default
		
		raise
	else:
		return pred(val)


def pairwise_fill(it: ty.Iterator[T], *, fill: U = None) \
    -> ty.Iterator[ty.Tuple[T, ty.Union[T, U]]]:
	"s -> (s0,s1), (s1,s2), (s2, s3), ..., (s_n-1, s_n), (s_n, None)"
	# Based on `pairwise` example at:
	# https://docs.python.org/3.9/library/itertools.html#itertools-recipes
	a, b = itertools.tee(itertools.chain(it, (fill,)))
	next(b, None)
	return zip(a, b)




class Indent(collections.namedtuple("Indent", ("tabs", "spaces"))):
	"""
	Convience class representing the combined indentation of tabs and spaces with vector-style math
	"""
	def __bool__(self) -> bool:
		return self.tabs != 0 or self.spaces != 0
	
	@property
	def characters(self) -> int:
		return self.tabs + self.spaces
	
	def columns(self, indent_size: int) -> int:
		return self.tabs * indent_size + self.spaces
	
	def __pos__(self) -> "Indent":
		return self
	
	def __neg__(self) -> "Indent":
		return Indent(-self.tabs, -self.spaces)
	
	def __eq__(self, other):
		if other == 0:
			return self.tabs == 0 and self.spaces == 0
		
		return super().__eq__(other)
	
	def __add__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			if other == 0:
				return self
			
			return NotImplemented
		
		return Indent(self.tabs + other[0], self.spaces + other[1])
	
	def __radd__(self, other):
		if not isinstance(other, Indent):
			# Special case for adding to zero (makes `sum` work)
			if other == 0:
				return self
			
			return NotImplemented
		
		return other.__add__(self)
	
	def __sub__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			# Special case for adding to zero (makes `sum` work)
			if other == 0:
				return self.__pos__()
			
			return NotImplemented
		
		return Indent(self.tabs - other[0], self.spaces - other[1])
	
	def __rsub__(self, other):
		if not isinstance(other, Indent):
			if other == 0:
				return self.__neg__()
			
			return NotImplemented
		
		return other.__add__(self)
	
	def __mul__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			return NotImplemented
		
		return Indent(self.tabs * other[0], self.spaces * other[1])
	
	def __div__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			return NotImplemented
		
		return Indent(self.tabs / other[0], self.spaces / other[1])

Indent.null = Indent(0, 0)


def parse_indent(line: str, *, allow_both: bool = True) -> Indent:
	"""
	Count number of tabs at start of line followed by number of spaces at start of line
	"""
	tabs   = 0
	spaces = 0
	expect_tab = True
	for char in line:
		if expect_tab and char == '\t':
			tabs += 1
		elif expect_tab and char == ' ':
			if not allow_both and tabs > 0:
				raise ValueError("Mixed tabs and spaces in indentation")
			spaces += 1
			expect_tab = False
		elif not expect_tab and char == ' ':
			spaces += 1
		elif not expect_tab and char == '\t':
			raise ValueError("Mixed tabs and spaces in indentation")
		else:
			break
	return Indent(tabs, spaces)