from auto_cli.str_utils import StrUtils


class TestStrUtils:
  """Test cases for StrUtils class."""

  def test_kebab_case_pascal_case(self):
    """Test conversion of PascalCase strings."""
    assert StrUtils.kebab_case("FooBarBaz") == "foo-bar-baz"
    assert StrUtils.kebab_case("XMLHttpRequest") == "xml-http-request"
    assert StrUtils.kebab_case("HTMLParser") == "html-parser"

  def test_kebab_case_camel_case(self):
    """Test conversion of camelCase strings."""
    assert StrUtils.kebab_case("fooBarBaz") == "foo-bar-baz"
    assert StrUtils.kebab_case("getUserName") == "get-user-name"
    assert StrUtils.kebab_case("processDataFiles") == "process-data-files"

  def test_kebab_case_single_word(self):
    """Test single word inputs."""
    assert StrUtils.kebab_case("simple") == "simple"
    assert StrUtils.kebab_case("SIMPLE") == "simple"
    assert StrUtils.kebab_case("Simple") == "simple"

  def test_kebab_case_with_numbers(self):
    """Test strings containing numbers."""
    assert StrUtils.kebab_case("foo2Bar") == "foo2-bar"
    assert StrUtils.kebab_case("getV2APIResponse") == "get-v2-api-response"
    assert StrUtils.kebab_case("parseHTML5Document") == "parse-html5-document"

  def test_kebab_case_already_kebab_case(self):
    """Test strings that are already in kebab-case."""
    assert StrUtils.kebab_case("foo-bar-baz") == "foo-bar-baz"
    assert StrUtils.kebab_case("simple-case") == "simple-case"

  def test_kebab_case_edge_cases(self):
    """Test edge cases."""
    assert StrUtils.kebab_case("") == ""
    assert StrUtils.kebab_case("A") == "a"
    assert StrUtils.kebab_case("AB") == "ab"
    assert StrUtils.kebab_case("ABC") == "abc"

  def test_kebab_case_consecutive_capitals(self):
    """Test strings with consecutive capital letters."""
    assert StrUtils.kebab_case("JSONParser") == "json-parser"
    assert StrUtils.kebab_case("XMLHTTPRequest") == "xmlhttp-request"
    assert StrUtils.kebab_case("PDFDocument") == "pdf-document"

  def test_kebab_case_mixed_separators(self):
    """Test strings with existing separators."""
    assert StrUtils.kebab_case("foo_bar_baz") == "foo_bar_baz"
    assert StrUtils.kebab_case("FooBar_Baz") == "foo-bar_baz"
