"""Tests for class-based CLI functionality."""
import enum
from pathlib import Path

import pytest

from auto_cli.cli import CLI, TargetMode


class SampleEnum(enum.Enum):
  """Sample enum for class-based CLI testing."""
  OPTION_A = "a"
  OPTION_B = "b"


class SampleClass:
  """Sample class for testing CLI generation."""

  def __init__(self):
    """Initialize sample class."""
    self.state = "initialized"

  def simple_method(self, name: str = "world"):
    """Simple method with default parameter.

    :param name: Name to use in greeting
    """
    return f"Hello {name} from method!"

  def method_with_types(self, text: str, number: int = 42,
                        active: bool = False, choice: SampleEnum = SampleEnum.OPTION_A,
                        file_path: Path = None):
    """Method with various type annotations.

    :param text: Required text parameter
    :param number: Optional number parameter
    :param active: Boolean flag parameter
    :param choice: Enum choice parameter
    :param file_path: Optional file path parameter
    """
    return {
      'text': text,
      'number': number,
      'active': active,
      'choice': choice,
      'file_path': file_path,
      'state': self.state
    }

  def hierarchical__nested__command(self, value: str):
    """Nested hierarchical method.

    :param value: Value to process
    """
    return f"Hierarchical: {value} (state: {self.state})"

  def method_without_docstring(self, param: str):
    """Method without parameter docstrings for testing."""
    return f"No docstring method: {param}"


class SampleClassWithComplexInit:
  """Class that requires constructor parameters (should fail)."""

  def __init__(self, required_param: str):
    """Initialize with required parameter."""
    self.required_param = required_param

  def some_method(self):
    """Some method that won't be accessible via CLI."""
    return "This shouldn't work"


class TestClassBasedCLI:
  """Test class-based CLI functionality."""

  def test_from_class_creation(self):
    """Test CLI creation from class."""
    cli = CLI(SampleClass)

    assert cli.target_mode == TargetMode.CLASS
    assert cli.target_class == SampleClass
    assert cli.title == "Sample class for testing CLI generation."  # From docstring
    assert 'simple_method' in cli.functions
    assert 'method_with_types' in cli.functions
    assert cli.target_module is None
    assert cli.method_filter is not None
    assert cli.function_filter is None

  def test_from_class_with_custom_title(self):
    """Test CLI creation with custom title."""
    cli = CLI(SampleClass, title="Custom Title")
    assert cli.title == "Custom Title"

  def test_from_class_without_docstring(self):
    """Test CLI creation from class without docstring."""

    class NoDocClass:
      def __init__(self):
        pass

      def method(self):
        return "test"

    cli = CLI(NoDocClass)
    assert cli.title == "NoDocClass"  # Falls back to class name

  def test_method_discovery(self):
    """Test automatic method discovery."""
    cli = CLI(SampleClass)

    # Should include public methods
    assert 'simple_method' in cli.functions
    assert 'method_with_types' in cli.functions
    assert 'hierarchical__nested__command' in cli.functions  # Dunder name kept as-is in functions dict
    assert 'method_without_docstring' in cli.functions

    # Should not include private methods or special methods
    method_names = list(cli.functions.keys())
    assert not any(name.startswith('_') for name in method_names)
    assert '__init__' not in cli.functions
    assert '__str__' not in cli.functions

    # Check that methods are functions (unbound, will be bound at execution time)
    for method in cli.functions.values():
      assert callable(method)  # Methods should be callable

  def test_method_execution(self):
    """Test method execution through CLI."""
    cli = CLI(SampleClass)

    result = cli.run(['simple-method', '--name', 'Alice'])
    assert result == "Hello Alice from method!"

  def test_method_execution_with_defaults(self):
    """Test method execution with default parameters."""
    cli = CLI(SampleClass)

    result = cli.run(['simple-method'])
    assert result == "Hello world from method!"

  def test_method_with_types_execution(self):
    """Test method execution with type annotations."""
    cli = CLI(SampleClass)

    result = cli.run(['method-with-types', '--text', 'test'])
    assert result['text'] == 'test'
    assert result['number'] == 42  # default
    assert result['active'] is False  # default
    assert result['choice'] == SampleEnum.OPTION_A  # default
    assert result['state'] == 'initialized'  # From class instance

  def test_method_with_all_parameters(self):
    """Test method execution with all parameters specified."""
    cli = CLI(SampleClass)

    result = cli.run([
      'method-with-types',
      '--text', 'hello',
      '--number', '123',
      '--active',
      '--choice', 'OPTION_B',
      '--file-path', '/tmp/test.txt'
    ])

    assert result['text'] == 'hello'
    assert result['number'] == 123
    assert result['active'] is True
    assert result['choice'] == SampleEnum.OPTION_B
    assert isinstance(result['file_path'], Path)
    assert str(result['file_path']) == '/tmp/test.txt'

  def test_hierarchical_methods(self):
    """Test that dunder notation is converted to flat command for class methods."""
    cli = CLI(SampleClass)

    # Dunder notation should now create a flat command with underscores converted to dashes
    result = cli.run(['hierarchical--nested--command', '--value', 'test'])
    assert "Hierarchical: test" in result
    assert "(state: initialized)" in result

  def test_parser_creation_from_class(self):
    """Test parser creation from class methods."""
    cli = CLI(SampleClass)
    parser = cli.create_parser()

    help_text = parser.format_help()
    assert "Sample class for testing CLI generation." in help_text
    assert "simple-method" in help_text
    assert "method-with-types" in help_text

  def test_class_instantiation_error(self):
    """Test error handling for classes that can't be instantiated."""
    with pytest.raises(ValueError, match="parameters without default values"):
      CLI(SampleClassWithComplexInit)

  def test_custom_method_filter(self):
    """Test custom method filter functionality."""

    def only_simple_method(name, obj):
      return name == 'simple_method'

    cli = CLI(SampleClass, method_filter=only_simple_method)
    assert list(cli.functions.keys()) == ['simple_method']

  def test_theme_tuner_integration(self):
    """Test that theme tuner is now provided by System class."""
    # Theme tuner functionality is now in System class, not injected into CLI
    from auto_cli.system import System
    cli = CLI(System)

    # System class uses inner class pattern, so should have hierarchical commands
    assert 'tune-theme' in cli.commands
    assert cli.commands['tune-theme']['type'] == 'group'
    assert 'increase-adjustment' in cli.commands['tune-theme']['commands']

  def test_completion_integration(self):
    """Test that completion works with class-based CLI."""
    cli = CLI(SampleClass, enable_completion=True)

    assert cli.enable_completion is True

  def test_method_without_docstring_parameters(self):
    """Test method without parameter docstrings."""
    cli = CLI(SampleClass)

    result = cli.run(['method-without-docstring', '--param', 'test'])
    assert result == "No docstring method: test"


class TestBackwardCompatibilityWithClasses:
  """Test that existing functionality still works with classes."""

  def test_from_module_still_works(self):
    """Test that from_module class method works like old constructor."""
    import tests.conftest as sample_module

    cli = CLI(sample_module, "Test CLI")

    assert cli.target_mode == TargetMode.MODULE
    assert cli.target_module == sample_module
    assert cli.title == "Test CLI"
    assert 'sample_function' in cli.functions
    assert cli.target_class is None
    assert cli.function_filter is not None
    assert cli.method_filter is None

  def test_old_constructor_still_works(self):
    """Test that old constructor pattern still works."""
    import tests.conftest as sample_module

    cli = CLI(sample_module, "Test CLI")

    # Should work exactly the same as before
    assert cli.target_mode == TargetMode.MODULE
    assert cli.title == "Test CLI"
    result = cli.run(['sample-function'])
    assert "Hello world!" in result

  def test_constructor_vs_from_module_equivalence(self):
    """Test that constructor and from_module produce equivalent results."""
    import tests.conftest as sample_module

    cli1 = CLI(sample_module, "Test CLI")
    cli2 = CLI(sample_module, "Test CLI")

    # Should have same structure
    assert cli1.target_mode == cli2.target_mode
    assert cli1.title == cli2.title
    assert list(cli1.functions.keys()) == list(cli2.functions.keys())
    assert cli1.theme == cli2.theme
    # enable_theme_tuner property no longer exists - it's now handled by System class


class TestClassVsModuleComparison:
  """Test that class and module modes have feature parity."""

  def test_type_annotation_parity(self):
    """Test that type annotations work the same for classes and modules."""
    import tests.conftest as sample_module

    # Module-based CLI
    cli_module = CLI(sample_module, "Module CLI")

    # Class-based CLI
    cli_class = CLI(SampleClass, "Class CLI")

    # Both should handle types correctly
    module_result = cli_module.run(['function-with-types', '--text', 'test', '--number', '456'])
    class_result = cli_class.run(['method-with-types', '--text', 'test', '--number', '456'])

    assert module_result['text'] == class_result['text']
    assert module_result['number'] == class_result['number']

  def test_hierarchical_command_parity(self):
    """Test that dunder notation creates flat commands for both classes and modules."""
    # Dunder notation should create flat commands with double dashes
    cli = CLI(SampleClass)

    result = cli.run(['hierarchical--nested--command', '--value', 'test'])
    assert "Hierarchical: test" in result

  def test_help_generation_parity(self):
    """Test that help generation works similarly for classes and modules."""
    import tests.conftest as sample_module

    cli_module = CLI(sample_module, "Module CLI")
    cli_class = CLI(SampleClass, "Class CLI")

    module_help = cli_module.create_parser().format_help()
    class_help = cli_class.create_parser().format_help()

    # Both should contain their respective titles
    assert "Module CLI" in module_help
    assert "Class CLI" in class_help

    # Both should have similar structure
    assert "COMMANDS" in module_help
    assert "COMMANDS" in class_help


class TestErrorHandling:
  """Test error handling for class-based CLI."""

  def test_missing_required_parameter(self):
    """Test error handling for missing required parameters."""
    cli = CLI(SampleClass)

    # Should raise SystemExit for missing required parameter
    with pytest.raises(SystemExit):
      cli.run(['method-with-types'])  # Missing required --text

  def test_invalid_enum_value(self):
    """Test error handling for invalid enum values."""
    cli = CLI(SampleClass)

    with pytest.raises(SystemExit):
      cli.run(['method-with-types', '--text', 'test', '--choice', 'INVALID'])

  def test_invalid_type_conversion(self):
    """Test error handling for invalid type conversions."""
    cli = CLI(SampleClass)

    with pytest.raises(SystemExit):
      cli.run(['method-with-types', '--text', 'test', '--number', 'not_a_number'])


class TestEdgeCases:
  """Test edge cases for class-based CLI."""

  def test_empty_class(self):
    """Test CLI creation from class with no public methods."""

    class EmptyClass:
      def __init__(self):
        pass

    cli = CLI(EmptyClass)
    assert len(cli.functions.keys()) == 0

  def test_class_with_only_private_methods(self):
    """Test class with only private methods."""

    class PrivateMethodsClass:
      def __init__(self):
        pass

      def _private_method(self):
        return "private"

      def __special_method__(self):
        return "special"

    cli = CLI(PrivateMethodsClass)
    # Should have no public methods
    assert len(cli.functions.keys()) == 0

  def test_class_with_property(self):
    """Test that properties are not included as methods."""

    class ClassWithProperty:
      def __init__(self):
        self._value = 42

      @property
      def value(self):
        return self._value

      def method(self):
        return "method"

    cli = CLI(ClassWithProperty)
    assert 'method' in cli.functions
    assert 'value' not in cli.functions  # Property should not be included


class SampleClassWithDefaults:
  """Class with constructor parameters that have defaults (should work)."""

  def __init__(self, config_file: str = "config.json", debug: bool = False):
    """Initialize with parameters that have defaults."""
    self.config_file = config_file
    self.debug = debug

  def test_method(self, message: str = "hello"):
    """Test method."""
    return f"Config: {self.config_file}, Debug: {self.debug}, Message: {message}"


class SampleClassWithInnerClasses:
  """Class with inner classes for hierarchical commands."""

  def __init__(self, base_config: str = "base.json"):
    """Initialize with base configuration."""
    self.base_config = base_config

  class GoodInnerClass:
    """Inner class with parameters that have defaults (should work)."""

    def __init__(self, database_url: str = "sqlite:///test.db"):
      self.database_url = database_url

    def create_item(self, name: str):
      """Create an item."""
      return f"Creating {name} with DB: {self.database_url}"


class TestConstructorParameterValidation:
  """Test constructor parameter validation for both patterns."""

  def test_direct_method_class_with_defaults_succeeds(self):
    """Test that class with default constructor parameters works for direct method pattern."""
    # Should work because all parameters have defaults
    cli = CLI(SampleClassWithDefaults)
    assert cli.target_mode == TargetMode.CLASS
    assert not cli.use_inner_class_pattern  # Using direct methods
    assert 'test_method' in cli.functions

  def test_direct_method_class_without_defaults_fails(self):
    """Test that class with required constructor parameters fails for direct method pattern."""
    # Should fail because constructor has required parameter
    with pytest.raises(ValueError, match="parameters without default values"):
      CLI(SampleClassWithComplexInit)

  def test_inner_class_pattern_with_good_constructors_succeeds(self):
    """Test that inner class pattern works when all constructors have default parameters."""
    # Should work because both main class and inner class have defaults
    cli = CLI(SampleClassWithInnerClasses)
    assert cli.target_mode == TargetMode.CLASS
    assert cli.use_inner_class_pattern  # Using inner classes
    # Inner class methods become hierarchical commands with proper nesting
    assert 'good-inner-class' in cli.commands
    assert cli.commands['good-inner-class']['type'] == 'group'
    assert 'create-item' in cli.commands['good-inner-class']['commands']

  def test_inner_class_pattern_with_bad_inner_class_fails(self):
    """Test that inner class pattern fails when inner class has required parameters."""

    # Create a class with bad inner class
    class ClassWithBadInner:
      def __init__(self, config: str = "test.json"):
        pass

      class BadInner:
        def __init__(self, required: str):  # No default!
          pass

        def method(self):
          pass

    # Should fail because inner class constructor has required parameter
    with pytest.raises(ValueError, match="Constructor for inner class.*parameters without default values"):
      CLI(ClassWithBadInner)

  def test_inner_class_pattern_with_bad_main_class_fails(self):
    """Test that inner class pattern fails when main class has required parameters."""

    # Create a class with bad main constructor
    class ClassWithBadMain:
      def __init__(self, required: str):  # No default!
        pass

      class GoodInner:
        def __init__(self, config: str = "test.json"):
          pass

        def method(self):
          pass

    # Should fail because main class constructor has required parameter
    with pytest.raises(ValueError, match="Constructor for main class.*parameters without default values"):
      CLI(ClassWithBadMain)
