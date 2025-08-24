import re


class StrUtils:
  """String utility functions."""

  @classmethod
  def kebab_case(cls, text: str) -> str:
    """
    Convert camelCase or PascalCase string to kebab-case.

    Args:
        text: The input string (e.g., "FooBarBaz", "fooBarBaz")

    Returns:
        Lowercase dash-separated string (e.g., "foo-bar-baz")

    Examples:
        StrUtils.kebab_case("FooBarBaz") # "foo-bar-baz"
        StrUtils.kebab_case("fooBarBaz") # "foo-bar-baz"
        StrUtils.kebab_case("XMLHttpRequest") # "xml-http-request"
        StrUtils.kebab_case("simple") # "simple"
    """
    if not text:
      return text

    # Insert dash before uppercase letters that follow lowercase letters or digits
    # This handles cases like "fooBar" -> "foo-Bar"
    result = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', text)

    # Insert dash before uppercase letters that are followed by lowercase letters
    # This handles cases like "XMLHttpRequest" -> "XML-Http-Request"
    result = re.sub(r'([A-Z])([A-Z][a-z])', r'\1-\2', result)

    return result.lower()
