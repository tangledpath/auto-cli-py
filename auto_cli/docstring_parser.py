"""Parse function docstrings to extract parameter descriptions."""
import re
from dataclasses import dataclass


@dataclass
class ParamDoc:
  """Holds parameter documentation extracted from docstring."""
  name: str
  description: str
  type_hint: str | None = None


def parse_docstring(docstring: str) -> tuple[str, dict[str, ParamDoc]]:
  """Extract main description and parameter docs from docstring.

  Parses docstrings in the format:
  Main description text.

  :param name: Description of parameter
  :param other_param: Description of other parameter

  :param docstring: The docstring text to parse
  :return: Tuple of (main_description, param_docs_dict)
  """
  if not docstring:
    return "", {}

  # Split into lines and clean up
  lines = [line.strip() for line in docstring.strip().split('\n')]
  main_lines = []
  param_docs = {}

  # Regex for :param name: description
  param_pattern = re.compile(r'^:param\s+(\w+):\s*(.+)$')

  for line in lines:
    if not line:
      continue

    match = param_pattern.match(line)
    if match:
      param_name, param_desc = match.groups()
      param_docs[param_name] = ParamDoc(param_name, param_desc.strip())
    elif not line.startswith(':'):
      # Only add non-param lines to main description
      main_lines.append(line)

  # Join main description lines, removing empty lines at start/end
  main_desc = ' '.join(main_lines).strip()

  return main_desc, param_docs


def extract_function_help(func) -> tuple[str, dict[str, str]]:
  """Extract help information from a function's docstring.

  :param func: Function to extract help from
  :return: Tuple of (main_description, param_help_dict)
  """
  import inspect

  docstring = inspect.getdoc(func) or ""
  main_desc, param_docs = parse_docstring(docstring)

  # Convert ParamDoc objects to simple string dict
  param_help = {param.name: param.description for param in param_docs.values()}

  return main_desc or f"Execute {func.__name__}", param_help
