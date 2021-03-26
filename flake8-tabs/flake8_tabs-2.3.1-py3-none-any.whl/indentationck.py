import itertools
import tokenize
import typing as ty

from . import categorizer
from . import config
from . import misc


__all__: ty.Final[ty.Tuple[str, ...]] = ("Checker",)


CATEGORY_NAMES: ty.Final[ty.Dict[categorizer.CategoryType, str]] = {
	categorizer.CategoryType.CALL: "call",
	categorizer.CategoryType.DEFN: "definition",
	categorizer.CategoryType.EXPR: "expression",
	categorizer.CategoryType.STMT: "statement",
}


def categorize_and_group_tokens_by_physical_line(
		tokens: ty.Iterable[tokenize.TokenInfo]
) -> ty.Generator[ty.Tuple[ty.List[categorizer.Token], ty.Optional[str]], ty.Any, None]:
	line_tokens = []
	
	ctokens = categorizer.Categorizer.process_all(tokens)
	for token, next_token in misc.pairwise_fill(ctokens):
		line_tokens.append(token)
		if token.type in (categorizer.TokenType.END_PLINE,
		                  categorizer.TokenType.END_LLINE):
			yield (line_tokens[:], next_token.line if next_token is not None else None)
			line_tokens.clear()
	
	assert len(line_tokens) == 0


class Checker:
	"""
	Checks indentation within braces with a “tabs for indentation, spaces
	for alignment” kind of mindset
	"""
	name: str    = "flake8-tabs"
	version: str = misc.__version__
	
	messages: ty.List[ty.Tuple[ty.Tuple[int, int], str]]
	
	
	def __init__(self, logical_line: str, line_number: int, noqa: bool, previous_indent_level: int,
	             tokens: ty.Iterable[tokenize.TokenInfo], filename: str) -> None:
		self.messages = []
		
		# We only care about non-empty non-noqa-marked lines
		if len(tokens) < 1 or noqa:
			return
		
		# Look up per-file attributes from EditorConfig
		config_fields = ("indent-style",)
		if config.Config["use-flake8-tabs"]:
			config_fields += (
				"continuation-style",
				"indent-levels-call",
				"indent-levels-defn",
				"indent-levels-expr",
				"indent-size",
			)
		
		cfg = config.Config.with_filepath(filename, *config_fields)
		
		# If we receive an INDENT token as first token here and the previous
		# line is reported to have had no indentation then we are seeing the
		# very first indentation of some code block here. This is a great place
		# to check if the block's entire indentation matches the expected
		# indentation style without producing an error for every single
		# mismatching logical line.
		if cfg["indent-style"] != "keep" and \
		   tokens[0].type == tokenize.INDENT and previous_indent_level == 0:
			block_indent = tokens[0].line[tokens[0].start[1]:tokens[0].end[1]]
			
			if cfg["indent-style"] == "tab" and not all(c == "\t" for c in block_indent):
				self.messages.append((tokens[0].start, misc.format_warning(
					191,
					"indentation contains spaces, but option indent-style=tab requires tabs"
				)))
			elif cfg["indent-style"] == "space" and not all(c == " " for c in block_indent):
				self.messages.append((tokens[0].start, misc.format_warning(
					191,
					"indentation contains tabs, but option indent-style=space requires spaces"
				)))
		
		# Don't run main part of checker unless enabled
		if not config.Config["use-flake8-tabs"]:
			return
		
		# Assume first line to be correctly indented
		try:
			first_indent = misc.parse_indent(tokens[0].line, allow_both=False)
		except ValueError:  # mixed tabs and spaces – report error and abort this logical line
			self.messages.append((tokens[0].start, misc.format_violation(
				101, "indentation contains mixed spaces and tabs"
			)))
			return
		
		# Indentation stack: Keeps track of the indentation `(tabs, spaces)`
		#                    caused by each brace
		# Item 0 represents the base indentation we got above, item 1 represents
		# indentation gained because of continuation lines
		indent_stack = [first_indent, misc.Indent.null]
		
		# Indentation gained by adding up the length of all initial keywords
		#
		# Needed to determine the expected indention of continuation lines if
		# there are no brackets open after the first line.
		keyword_indent: ty.Optional[misc.Indent] = None
		
		open_brackets: int = 0
		for ltokens, next_line in categorize_and_group_tokens_by_physical_line(tokens):
			# Convenience aliases for current physical line
			line_category = ltokens[0].category
			line_start    = ltokens[0].start
			line_text     = ltokens[0].line
			
			# Determine current physical line indentation
			try:
				line_indent = misc.parse_indent(line_text)
			except ValueError:  # mixed tabs and spaces – report error and abort this logical line
				self.messages.append((line_start, misc.format_violation(
					101, "indentation contains mixed spaces and tabs"
				)))
				return
			
			# Skip blank lines within expressions (no opinion on those)
			if len(line_text.strip()) < 1:
				continue
			
			# Determine number of characters in initial keywords on first line
			if keyword_indent is None:
				keyword_indent = misc.Indent.null
				for token, next_token in misc.pairwise_fill(ltokens):
					if token.type in (
						categorizer.TokenType.INDENT,
						categorizer.TokenType.DEDENT,
					):
						continue
					
					if token.type is not categorizer.TokenType.KEYWORD \
					   or token.string not in categorizer.KEYWORDS_STATEMENT:
						break
					
					# Add up length of token and any whitespace between this token
					# and the next one
					keyword_indent += misc.Indent(
						0,
						((next_token.start[1] - token.start[1])
						 if next_token is not None
						 else token.end[1] - token.start[1])
					)
				
				# Fallback for continuation lines without initial keywords such as
				# variable assignments
				#
				# Fixes GL/ntninja/flake8-tabs#5.
				if keyword_indent == misc.Indent.null:
					keyword_indent = misc.Indent(1, 0)
			
			# Calculate expected indentation for the current line
			#
			# While indentation is mostly determined by the contents of the
			# preceding line some adjustments for initial closing brackets
			# on the current line are applied before considering the value
			# final and comparing to the line's actual indentation.
			line_expected_indent: misc.Indent = sum(indent_stack)
			
			# Check if line ends with an opening bracket
			#
			# Depending on whether the lines ends with an opening bracket we'll
			# either expect the following line to be indented with spaces to align
			# with each opened bracket, or expect it to be indented with a single
			# tab for the outermost opened bracket.
			line_final_bracket_token: ty.Optional[categorizer.Token] = misc.map_next(
				lambda t: t if t.type is categorizer.TokenType.BRACKET_OPEN else None,
				itertools.dropwhile(
					# Skip end-of-line tokens
					lambda t: t.type in (
						categorizer.TokenType.COMMENT,
						categorizer.TokenType.END_LLINE,
						categorizer.TokenType.END_PLINE,
					),
					reversed(ltokens),
				),
				default=None
			)
			next_line_indent_hanging = (line_final_bracket_token is not None)
			
			# Issue warning if opened bracket implies non-allowed indentation
			# style on next line
			if next_line_indent_hanging and cfg["continuation-style"] == "aligned":
				self.messages.append((line_start, misc.format_violation(
					113,
					"use of hanging indentation, but option continuation-style=aligned "
					"does not permit this"
				)))
			
			if not next_line_indent_hanging and cfg["continuation-style"] == "hanging":
				self.messages.append((line_start, misc.format_violation(
					113,
					"use of alignment as indentation, but option continuation-style=hanging "
					"does not permit this"
				)))
			
			# Determine indentation closed by initial closing brackets
			#
			# Unlike other closed brackets, brackets closed at the start of line
			# also decrease the expected indentation on the current line and not
			# just subsequent lines.
			line_initial_closing_brackets: int = sum(1 for _ in itertools.takewhile(
				lambda t: t.type is categorizer.TokenType.BRACKET_CLOSE,
				ltokens,
			))
			line_initial_dedent: misc.Indent = \
				sum(indent_stack[(len(indent_stack) - line_initial_closing_brackets):])
			
			line_expected_indent -= line_initial_dedent
			
			# Calculate expected indentation for next line
			if next_line_indent_hanging:
				# Choose expected number of tabs for indentation on the following
				# lines based on the innermost active category
				indent_tabs = cfg["indent-levels-expr"]
				if ltokens[-1].category is categorizer.CategoryType.CALL:
					indent_tabs = cfg["indent-levels-call"]
				elif ltokens[-1].category is categorizer.CategoryType.DEFN:
					indent_tabs = cfg["indent-levels-defn"]
				
				# Parse indentation of the following line (if any), for cases where we
				# really and truly cannot predict which indentation it should have
				# and therefor need to peak at what is actually there
				next_indent = misc.Indent.null
				try:
					if next_line is not None:
						next_indent = misc.parse_indent(next_line)
				except ValueError:
					pass
				
				# Apply indentation as spaces or tabs depending on whether
				# the current indentation already contains any spaces
				#
				# This ensures that that we don't create any weird tab/
				# spaces hybrid structures that would look bad if
				# [editor tab width] != cfg["indent-size"].
				#
				# In order to also support spaces-indented documents we
				# also check whether the current line contains any
				# indentation at all and if that isn't the case we
				# fall back to analyzing the indentation of the next line
				# of the document instead: If it only starts with spaces,
				# we also expect spaces-based indentation, otherwise we
				# expect tabs.
				indent_with_tabs: bool = True
				if sum(indent_stack).characters > 0:
					indent_with_tabs = (sum(indent_stack).spaces < 1)
				elif next_indent.characters > 0:
					indent_with_tabs = (next_indent.tabs > 0)
				
				hanging_indent: misc.Indent =  \
					misc.Indent(indent_tabs, 0) \
					if indent_with_tabs         \
					else misc.Indent(0, indent_tabs * cfg["indent-size"])
				
				newly_opened_brackets: int = line_initial_closing_brackets
				for token in ltokens:
					if token.type is categorizer.TokenType.BRACKET_OPEN:
						newly_opened_brackets += 1
						
						if ltokens[-1].category is categorizer.CategoryType.CALL:
							# Record single added level of indentation on first opened
							# bracket on this line
							if newly_opened_brackets == 1:
								indent_stack.append(hanging_indent)
							else:
								indent_stack.append(misc.Indent.null)
						else:
							# Record single added level of indentation on last opened
							# bracket on this line
							if token is line_final_bracket_token:
								indent_stack.append(hanging_indent)
							else:
								indent_stack.append(misc.Indent.null)
					elif token.type is categorizer.TokenType.BRACKET_CLOSE:
						newly_opened_brackets -= 1
						
						# Pop the indentation added by a previous opening bracket
						#
						# If we have more closing brackets than opening brackets on
						# this line this may also pop brackets added on previous lines.
						indent_stack.pop()
				open_brackets += newly_opened_brackets
			else:
				for token in ltokens:
					if token.type is categorizer.TokenType.BRACKET_OPEN:
						open_brackets += 1
						
						# Record alignment indentation added by the opened bracket
						#
						# Brackets on the same line will be popped again from the stack
						# leaving only those that actually matter when computing the
						# amount of hanging indent added by each bracket. By using
						# `sum(indent_stack).characters` here these previously popped
						# brackets will not be considered when determining the number
						# of characters/spaces added by this opening bracket.
						indent_stack.append(
							misc.Indent(0, token.end[1] - sum(indent_stack).characters)
						)
					elif token.type is categorizer.TokenType.BRACKET_CLOSE:
						open_brackets -= 1
						
						# Pop the indentation added by a previous opening bracket
						#
						# If we have more closing brackets than opening brackets on
						# this line this may also pop brackets added on previous lines.
						indent_stack.pop()
			
			
			# +-----------------------------------------------+ #
			# | Compare found indentation with expected value | #
			# +-----------------------------------------------+ #
			
			# If there are no open braces after the end of the current line,
			# expect the next line to be indented by the size of any leading
			# keyword (useful for `assert`, `with`, …)
			if sum(indent_stack) == first_indent:
				indent_stack[1] = keyword_indent
			
			# Compare settings on current line
			if line_indent != line_expected_indent:
				# Find error code similar to `pycodestyle`
				code = 112
				if line_indent == first_indent:
					code = 122
				elif line_expected_indent.spaces == line_indent.spaces == 0:
					if line_indent.tabs < line_expected_indent.tabs:
						code = 121
					else:
						code = 126
				else:
					if line_indent.spaces > line_expected_indent.spaces:
						code = 127
					else:
						code = 128
				
				# Generate and store error message
				if line_expected_indent.spaces == line_indent.spaces:
					self.messages.append((line_start, misc.format_violation(
						code,
						f"unexpected number of tabs at start of "
						f"{CATEGORY_NAMES[line_category]} line (expected "
						f"{line_expected_indent.tabs}, got {line_indent.tabs})"
					)))
				elif line_expected_indent.tabs == line_indent.tabs:
					self.messages.append((line_start, misc.format_violation(
						code,
						f"unexpected number of spaces at start of "
						f"{CATEGORY_NAMES[line_category]} line (expected "
						f"{line_expected_indent.spaces}, got {line_indent.spaces})"
					)))
				else:
					self.messages.append((line_start, misc.format_violation(
						code,
						f"unexpected number of tabs and spaces at start of "
						f"{CATEGORY_NAMES[line_category]} line " +  # noqa: W504
						"(expected {0.tabs} tabs and {0.spaces} spaces, "
						"got {1.tabs} tabs and {1.spaces} spaces)".format(
							line_expected_indent, line_indent,
						)
					)))
	
	def __iter__(self) -> ty.Iterator[ty.Tuple[int, str]]:
		return iter(self.messages)