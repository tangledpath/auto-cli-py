"""System-level CLI commands for auto-cli-py."""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Set

from auto_cli.ansi_string import AnsiString
from auto_cli.theme import (AdjustStrategy, ColorFormatter, create_default_theme,
                            create_default_theme_colorful, RGB)
from auto_cli.theme.theme_style import ThemeStyle


class System:
  """System-level utilities for CLI applications."""

  def __init__(self, config_dir: Path = Path.home() / '.auto-cli'):
    """Initialize system utilities.

    :param config_dir: Configuration directory for system settings
    """
    self.config_dir = config_dir

  class TuneTheme:
    """Interactive theme tuning utility."""

    # Adjustment increment constant for easy modification
    ADJUSTMENT_INCREMENT = 0.05

    def __init__(self, initial_theme: str = "universal"):
      """Initialize theme tuner.

      :param initial_theme: Starting theme (universal or colorful)
      """
      self.adjust_percent = 0.0
      self.adjust_strategy = AdjustStrategy.LINEAR
      self.use_colorful_theme = initial_theme.lower() == "colorful"
      self.formatter = ColorFormatter(enable_colors=True)

      # Individual color override tracking
      self.individual_color_overrides: Dict[str, RGB] = {}
      self.modified_components: Set[str] = set()

      # Theme component metadata for user interface
      self.theme_components = [
        ("title", "Title text"),
        ("subtitle", "Section headers (COMMANDS:, OPTIONS:)"),
        ("command_name", "Command names"),
        ("command_description", "Command descriptions"),
        # Command Group Level (inner class level)
        ("command_group_name", "Command group names (inner class names)"),
        ("command_group_description", "Command group descriptions (inner class descriptions)"),
        ("command_group_option_name", "Command group option flags"),
        ("command_group_option_description", "Command group option descriptions"),
        # Grouped Command Level (commands within the group)
        ("grouped_command_name", "Grouped command names (methods within groups)"),
        ("grouped_command_description", "Grouped command descriptions (method descriptions)"),
        ("grouped_command_option_name", "Grouped command option flags"),
        ("grouped_command_option_description", "Grouped command option descriptions"),
        ("option_name", "Regular option flags (--name)"),
        ("option_description", "Regular option descriptions"),
        ("required_asterisk", "Required field markers (*)")
      ]

      # Get terminal width
      try:
        self.console_width = os.get_terminal_size().columns
      except (OSError, ValueError):
        self.console_width = int(os.environ.get('COLUMNS', 80))

    def increase_adjustment(self) -> None:
      """Increase color adjustment by 0.05."""
      self.adjust_percent = min(5.0, self.adjust_percent + self.ADJUSTMENT_INCREMENT)
      print(f"Adjustment increased to {self.adjust_percent:.2f}")

    def decrease_adjustment(self) -> None:
      """Decrease color adjustment by 0.05."""
      self.adjust_percent = max(-5.0, self.adjust_percent - self.ADJUSTMENT_INCREMENT)
      print(f"Adjustment decreased to {self.adjust_percent:.2f}")

    def select_strategy(self, strategy: str = None) -> None:
      """Select color adjustment strategy.

      :param strategy: Strategy name or None for interactive selection
      """
      if strategy:
        # Convert string to enum if valid
        try:
          self.adjust_strategy = AdjustStrategy[strategy.upper()]
          print(f"Strategy set to: {self.adjust_strategy.name}")
        except KeyError:
          print(f"Invalid strategy: {strategy}")
      else:
        # Interactive selection
        self._select_adjustment_strategy()

    def toggle_theme(self) -> None:
      """Toggle between universal and colorful themes."""
      self.use_colorful_theme = not self.use_colorful_theme
      theme_name = "COLORFUL" if self.use_colorful_theme else "UNIVERSAL"
      print(f"Theme toggled to {theme_name}")

    def edit_colors(self) -> None:
      """Edit individual color values interactively."""
      self.edit_individual_color()

    def show_rgb(self) -> None:
      """Display RGB values for current theme colors."""
      self.display_rgb_values()
      input("\nPress Enter to continue...")

    def run_interactive(self) -> None:
      """Run the interactive theme tuner."""
      self.run_interactive_menu()

    def get_current_theme(self):
      """Get theme with global adjustments and individual overrides applied."""
      # 1. Start with base theme
      base_theme = create_default_theme_colorful() if self.use_colorful_theme else create_default_theme()

      # 2. Apply global adjustments if any
      if self.adjust_percent != 0.0:
        try:
          adjusted_theme = base_theme.create_adjusted_copy(
            adjust_percent=self.adjust_percent,
            adjust_strategy=self.adjust_strategy
          )
        except ValueError:
          adjusted_theme = base_theme
      else:
        adjusted_theme = base_theme

      # 3. Apply individual color overrides if any
      result = adjusted_theme
      if self.individual_color_overrides:
        result = self._apply_individual_overrides(adjusted_theme)

      return result

    def _apply_individual_overrides(self, theme):
      """Create new theme with individual color overrides applied."""
      from auto_cli.theme.theme import Theme

      # Get all current theme styles
      theme_styles = {}
      for component_name, _ in self.theme_components:
        original_style = getattr(theme, component_name)

        if component_name in self.individual_color_overrides:
          # Create new ThemeStyle with overridden color but preserve other attributes
          override_color = self.individual_color_overrides[component_name]
          theme_styles[component_name] = ThemeStyle(
            fg=override_color,
            bg=original_style.bg,
            bold=original_style.bold,
            italic=original_style.italic,
            dim=original_style.dim,
            underline=original_style.underline
          )
        else:
          # Use original style
          theme_styles[component_name] = original_style

      # Create new theme with overridden styles
      return Theme(
        adjust_percent=theme.adjust_percent,
        adjust_strategy=theme.adjust_strategy,
        **theme_styles
      )

    def display_theme_info(self):
      """Display current theme information and preview."""
      theme = self.get_current_theme()

      # Create a fresh formatter with the current adjusted theme
      current_formatter = ColorFormatter(enable_colors=True)

      # Simple header
      print("=" * min(self.console_width, 60))
      print("🎛️  THEME TUNER")
      print("=" * min(self.console_width, 60))

      # Current settings
      strategy_name = self.adjust_strategy.name
      theme_name = "COLORFUL" if self.use_colorful_theme else "UNIVERSAL"

      print(f"Theme: {theme_name}")
      print(f"Strategy: {strategy_name}")
      print(f"Adjust: {self.adjust_percent:.2f}")

      # Show modification status
      if self.individual_color_overrides:
        modified_count = len(self.individual_color_overrides)
        total_count = len(self.theme_components)
        modified_names = ', '.join(sorted(self.individual_color_overrides.keys()))
        print(f"Modified Components: {modified_count}/{total_count} ({modified_names})")
      else:
        print("Modified Components: None")
      print()

      # Simple preview with real-time color updates
      print("📋 CLI Preview:")
      print(
        f"  {current_formatter.apply_style('hello', theme.command_name)}: {current_formatter.apply_style('Greet the user', theme.command_description)}"
      )
      print(
        f"  {current_formatter.apply_style('--name NAME', theme.option_name)}: {current_formatter.apply_style('Specify name', theme.option_description)}"
      )
      print(
        f"  {current_formatter.apply_style('--email EMAIL', theme.option_name)} {current_formatter.apply_style('*', theme.required_asterisk)}: {current_formatter.apply_style('Required email', theme.option_description)}"
      )
      print()

    def display_rgb_values(self):
      """Display RGB values for theme incorporation with names colored in their RGB values on different backgrounds."""
      theme = self.get_current_theme()  # Get the current adjusted theme

      print("\n" + "=" * min(self.console_width, 60))
      print("🎨 RGB VALUES FOR THEME INCORPORATION")
      print("=" * min(self.console_width, 60))

      # Color mappings for the current adjusted theme - include ALL theme components
      color_map = [
        ("title", theme.title.fg, "Title color"),
        ("subtitle", theme.subtitle.fg, "Subtitle color"),
        ("command_name", theme.command_name.fg, "Command name"),
        ("command_description", theme.command_description.fg, "Command description"),
        # Command Group Level (inner class level)
        ("command_group_name", theme.command_group_name.fg, "Command group name"),
        ("command_group_description", theme.command_group_description.fg, "Command group description"),
        ("command_group_option_name", theme.command_group_option_name.fg, "Command group option name"),
        ("command_group_option_description", theme.command_group_option_description.fg, "Command group option description"),
        # Grouped Command Level (commands within the group)
        ("grouped_command_name", theme.grouped_command_name.fg, "Grouped command name"),
        ("grouped_command_description", theme.grouped_command_description.fg, "Grouped command description"),
        ("grouped_command_option_name", theme.grouped_command_option_name.fg, "Grouped command option name"),
        ("grouped_command_option_description", theme.grouped_command_option_description.fg, "Grouped command option description"),
        ("option_name", theme.option_name.fg, "Option name"),
        ("option_description", theme.option_description.fg, "Option description"),
        ("required_asterisk", theme.required_asterisk.fg, "Required asterisk"),
      ]

      # Create background colors for testing readability
      white_bg = RGB.from_rgb(0xFFFFFF)  # White background
      black_bg = RGB.from_rgb(0x000000)  # Black background

      # Collect theme code components
      theme_code_lines = []

      for name, color_code, description in color_map:
        if isinstance(color_code, RGB):
          # Check if this component has been modified
          is_modified = name in self.individual_color_overrides

          # RGB instance - show name in the actual color
          r, g, b = color_code.to_ints()
          hex_code = color_code.to_hex()
          hex_int = f"0x{hex_code[1:]}"  # Convert #FF80FF to 0xFF80FF

          # Get the complete theme style for this component (includes bold, italic, etc.)
          current_theme_style = getattr(theme, name)

          # Create styled versions using the complete theme style with different backgrounds
          # Only the white/black background versions should be styled
          white_bg_style = ThemeStyle(
            fg=color_code,
            bg=white_bg,
            bold=current_theme_style.bold,
            italic=current_theme_style.italic,
            dim=current_theme_style.dim,
            underline=current_theme_style.underline
          )
          black_bg_style = ThemeStyle(
            fg=color_code,
            bg=black_bg,
            bold=current_theme_style.bold,
            italic=current_theme_style.italic,
            dim=current_theme_style.dim,
            underline=current_theme_style.underline
          )

          # Apply styles (first name is unstyled, only white/black background versions are styled)
          colored_name_white = self.formatter.apply_style(name, white_bg_style)
          colored_name_black = self.formatter.apply_style(name, black_bg_style)

          # First name display is just plain text with standard padding
          padding = 20 - len(name)
          padded_name = name + ' ' * padding

          # Show modification indicator
          modifier_indicator = " [CUSTOM]" if is_modified else ""

          print(f"  {padded_name} = rgb({r:3}, {g:3}, {b:3})  # {hex_code}{modifier_indicator}")

          # Show original color if modified
          if is_modified:
            # Get the original color (before override)
            base_theme = create_default_theme_colorful() if self.use_colorful_theme else create_default_theme()
            adjusted_base = base_theme
            if self.adjust_percent != 0.0:
              try:
                adjusted_base = base_theme.create_adjusted_copy(
                  adjust_percent=self.adjust_percent,
                  adjust_strategy=self.adjust_strategy
                )
              except ValueError:
                adjusted_base = base_theme

            original_style = getattr(adjusted_base, name)
            if original_style.fg and isinstance(original_style.fg, RGB):
              orig_r, orig_g, orig_b = original_style.fg.to_ints()
              orig_hex = original_style.fg.to_hex()
              print(f"    Original: rgb({orig_r:3}, {orig_g:3}, {orig_b:3})  # {orig_hex}")

          # Calculate alignment width based on longest component name for clean f-string alignment
          max_component_name_length = max(len(comp_name) for comp_name, _ in self.theme_components)
          white_field_width = max_component_name_length + 2  # +2 for spacing buffer

          # Use AnsiString for proper f-string alignment with ANSI escape codes
          print(
            f"    On white: {AnsiString(colored_name_white):<{white_field_width}}On black: {AnsiString(colored_name_black)}")
          print()

          # Build theme code line for this color
          # Handle background colors and text styles
          additional_styles = []
          if hasattr(theme, name):
            style_obj = getattr(theme, name)
            if style_obj.bg:
              if isinstance(style_obj.bg, RGB):
                bg_r, bg_g, bg_b = style_obj.bg.to_ints()
                bg_hex = style_obj.bg.to_hex()
                bg_hex_int = f"0x{bg_hex[1:]}"
                additional_styles.append(f"bg=RGB.from_rgb({bg_hex_int})")
            if style_obj.bold:
              additional_styles.append("bold=True")
            if style_obj.italic:
              additional_styles.append("italic=True")
            if style_obj.dim:
              additional_styles.append("dim=True")
            if style_obj.underline:
              additional_styles.append("underline=True")

          # Create ThemeStyle constructor call
          style_params = [f"fg=RGB.from_rgb({hex_int})"]
          style_params.extend(additional_styles)
          style_call = f"ThemeStyle({', '.join(style_params)})"

          theme_code_lines.append(f"    {name}={style_call},")

        elif color_code and isinstance(color_code, str) and color_code.startswith('#'):
          # Hex string (fallback handling)
          try:
            hex_clean = color_code.strip().lstrip('#').upper()
            if len(hex_clean) == 3:
              hex_clean = ''.join(c * 2 for c in hex_clean)
            if len(hex_clean) == 6 and all(c in '0123456789ABCDEF' for c in hex_clean):
              hex_int = int(hex_clean, 16)
              rgb = RGB.from_rgb(hex_int)
              r, g, b = rgb.to_ints()

              padding = 20 - len(name)
              padded_name = name + ' ' * padding

              print(f"  {padded_name} = rgb({r:3}, {g:3}, {b:3})  # {color_code}")

              # Add to theme code
              hex_int_str = f"0x{hex_clean}"
              theme_code_lines.append(f"    {name}=ThemeStyle(fg=RGB.from_rgb({hex_int_str})),")
            else:
              print(f"  {name:20} = {color_code}")
          except ValueError:
            print(f"  {name:20} = {color_code}")
        elif color_code:
          print(f"  {name:20} = {color_code}")
        else:
          # No color defined
          print(f"  {name:20} = (no color)")

      # Display the complete theme creation code
      print("\n" + "=" * min(self.console_width, 60))
      print("📋 THEME CREATION CODE")
      print("=" * min(self.console_width, 60))
      print()
      print("from auto_cli.theme import RGB, ThemeStyle, Theme")
      print()
      print("def create_custom_theme() -> Theme:")
      print("  \"\"\"Create a custom theme with the current colors.\"\"\"")
      print("  return Theme(")

      for line in theme_code_lines:
        print(line)

      print("  )")
      print()
      print("# Usage in your CLI:")
      print("from auto_cli.cli import CLI")
      print("cli = CLI(your_module, theme=create_custom_theme())")
      print("cli.display()")

      print("=" * min(self.console_width, 60))

    def edit_individual_color(self):
      """Interactive color editing for individual theme components."""
      while True:
        print("\n" + "=" * min(self.console_width, 60))
        print("🎨 EDIT INDIVIDUAL COLOR")
        print("=" * min(self.console_width, 60))

        # Display components with modification indicators
        for i, (component_name, description) in enumerate(self.theme_components, 1):
          is_modified = component_name in self.individual_color_overrides
          status = " [MODIFIED]" if is_modified else ""
          print(f"  {i:2d}. {component_name:<25} {status}")
          print(f"      {description}")

          # Show current color
          current_theme = self.get_current_theme()
          current_style = getattr(current_theme, component_name)
          if current_style.fg and isinstance(current_style.fg, RGB):
            hex_color = current_style.fg.to_hex()
            r, g, b = current_style.fg.to_ints()
            colored_preview = self.formatter.apply_style("██", ThemeStyle(fg=current_style.fg))
            print(f"      Current: {colored_preview} rgb({r:3}, {g:3}, {b:3}) {hex_color}")
          print()

        print("Commands:")
        print("  Enter number (1-12) to edit component")
        print("  [x] Reset all individual colors")
        print("  [q] Return to main menu")

        try:
          choice = input("\nChoice: ").lower().strip()

          if choice == 'q':
            break
          elif choice == 'x':
            self._reset_all_individual_colors()
            print("All individual color overrides reset!")
            continue

          # Try to parse as component number
          try:
            component_index = int(choice) - 1
            if 0 <= component_index < len(self.theme_components):
              component_name, description = self.theme_components[component_index]
              self._edit_component_color(component_name, description)
            else:
              print(f"Invalid choice. Please enter 1-{len(self.theme_components)}")
          except ValueError:
            print("Invalid input. Please enter a number or command.")

        except (KeyboardInterrupt, EOFError):
          break

    def _edit_component_color(self, component_name: str, description: str):
      """Edit color for a specific component."""
      # Get current color
      current_theme = self.get_current_theme()
      current_style = getattr(current_theme, component_name)
      current_color = current_style.fg if current_style.fg else RGB.from_rgb(0x808080)

      is_modified = component_name in self.individual_color_overrides

      print(f"\n🎨 EDITING: {component_name}")
      print(f"Description: {description}")

      if isinstance(current_color, RGB):
        hex_color = current_color.to_hex()
        r, g, b = current_color.to_ints()
        colored_preview = self.formatter.apply_style("██████", ThemeStyle(fg=current_color))
        print(f"Current: {colored_preview} rgb({r:3}, {g:3}, {b:3}) {hex_color}")

      if is_modified:
        print("(This color has been customized)")

      print("\nInput Methods:")
      print("  [h] Hex color entry (e.g., FF8080)")
      print("  [r] Reset to original color")
      print("  [q] Cancel")

      try:
        method = input("\nChoose input method: ").lower().strip()

        if method == 'q':
          return
        elif method == 'r':
          self._reset_component_color(component_name)
          print(f"Reset {component_name} to original color!")
          return
        elif method == 'h':
          self._hex_color_input(component_name, current_color)
        else:
          print("Invalid choice.")

      except (KeyboardInterrupt, EOFError):
        return

    def _hex_color_input(self, component_name: str, current_color: RGB):
      """Handle hex color input for a component."""
      print(f"\nCurrent color: {current_color.to_hex()}")
      print("Enter new hex color (without #):")
      print("Examples: FF8080, ff8080, F80 (short form)")

      try:
        hex_input = input("Hex color: ").strip()

        if not hex_input:
          print("No input provided, canceling.")
          return

        # Normalize hex input
        hex_clean = hex_input.upper().lstrip('#')

        # Handle 3-character hex (e.g., F80 -> FF8800)
        if len(hex_clean) == 3:
          hex_clean = ''.join(c * 2 for c in hex_clean)

        # Validate hex
        if len(hex_clean) != 6 or not all(c in '0123456789ABCDEF' for c in hex_clean):
          print("Invalid hex color format. Please use 6 digits (e.g., FF8080)")
          return

        # Convert to RGB
        hex_int = int(hex_clean, 16)
        new_color = RGB.from_rgb(hex_int)

        # Preview the new color
        r, g, b = new_color.to_ints()
        colored_preview = self.formatter.apply_style("██████", ThemeStyle(fg=new_color))
        print(f"\nPreview: {colored_preview} rgb({r:3}, {g:3}, {b:3}) #{hex_clean}")

        # Confirm
        confirm = input("Apply this color? [y/N]: ").lower().strip()
        if confirm in ('y', 'yes'):
          self.individual_color_overrides[component_name] = new_color
          self.modified_components.add(component_name)
          print(f"✅ Applied new color to {component_name}!")
        else:
          print("Color change canceled.")

      except (KeyboardInterrupt, EOFError):
        print("\nColor editing canceled.")
      except ValueError as e:
        print(f"Error: {e}")

    def _reset_component_color(self, component_name: str):
      """Reset a component's color to original."""
      if component_name in self.individual_color_overrides:
        del self.individual_color_overrides[component_name]
        self.modified_components.discard(component_name)

    def _reset_all_individual_colors(self):
      """Reset all individual color overrides."""
      self.individual_color_overrides.clear()
      self.modified_components.clear()

    def _select_adjustment_strategy(self):
      """Allow user to select from all available adjustment strategies."""
      strategies = list(AdjustStrategy)

      print("\n🎯 SELECT ADJUSTMENT STRATEGY")
      print("=" * 40)

      # Display current strategy
      current_index = strategies.index(self.adjust_strategy)
      print(f"Current strategy: {self.adjust_strategy.name}")
      print()

      # Display all available strategies with numbers
      print("Available strategies:")
      strategy_descriptions = {
        AdjustStrategy.LINEAR: "Linear blend adjustment (legacy compatibility)",
        AdjustStrategy.COLOR_HSL: "HSL-based lightness adjustment",
        AdjustStrategy.MULTIPLICATIVE: "Simple RGB value scaling",
        AdjustStrategy.GAMMA: "Gamma correction for perceptual uniformity",
        AdjustStrategy.LUMINANCE: "ITU-R BT.709 perceived brightness adjustment",
        AdjustStrategy.OVERLAY: "Photoshop-style overlay blend mode",
        AdjustStrategy.ABSOLUTE: "Legacy absolute color adjustment"
      }

      for i, strategy in enumerate(strategies, 1):
        marker = "→" if strategy == self.adjust_strategy else " "
        description = strategy_descriptions.get(strategy, "Color adjustment strategy")
        print(f"{marker} [{i}] {strategy.name}: {description}")

      print()
      print("  [Enter] Keep current strategy")
      print("  [q] Cancel")

      try:
        choice = input("\nSelect strategy (1-7): ").strip().lower()

        if choice == '' or choice == 'q':
          return  # Keep current strategy

        try:
          strategy_index = int(choice) - 1
          if 0 <= strategy_index < len(strategies):
            old_strategy = self.adjust_strategy.name
            self.adjust_strategy = strategies[strategy_index]
            print(f"✅ Strategy changed from {old_strategy} to {self.adjust_strategy.name}")
          else:
            print("❌ Invalid strategy number. Strategy unchanged.")
        except ValueError:
          print("❌ Invalid input. Strategy unchanged.")

      except (EOFError, KeyboardInterrupt):
        print("\n❌ Selection cancelled.")

    def run_interactive_menu(self):
      """Run a simple menu-based theme tuner."""
      print("🎛️  THEME TUNER")
      print("=" * 40)
      print("Interactive controls are not available in this environment.")
      print("Using simple menu mode instead.")
      print()

      while True:
        self.display_theme_info()

        print("Available commands:")
        print(f"  [+] Increase adjustment by {self.ADJUSTMENT_INCREMENT}")
        print(f"  [-] Decrease adjustment by {self.ADJUSTMENT_INCREMENT}")
        print("  [s] Select adjustment strategy")
        print("  [t] Toggle theme (universal/colorful)")
        print("  [e] Edit individual colors")
        print("  [r] Show RGB values")
        print("  [q] Quit")

        try:
          choice = input("\nEnter command: ").lower().strip()

          if choice == 'q':
            break
          elif choice == '+':
            self.increase_adjustment()
          elif choice == '-':
            self.decrease_adjustment()
          elif choice == 's':
            self._select_adjustment_strategy()
          elif choice == 't':
            self.toggle_theme()
          elif choice == 'e':
            self.edit_colors()
          elif choice == 'r':
            self.show_rgb()
          else:
            print("Invalid command. Try again.")

          print()

        except (KeyboardInterrupt, EOFError):
          break

      print("\n🎨 Theme tuning session ended.")

  class Completion:
    """Shell completion management."""

    def __init__(self, shell: str = "bash", cli_instance=None):
      """Initialize completion manager.

      :param shell: Default shell type
      :param cli_instance: CLI instance for completion functionality (set by CLI class)
      """
      self.shell = shell
      self._cli_instance = cli_instance
      self._completion_handler = None

    def install(self, shell: Optional[str] = None, force: bool = False) -> bool:
      """Install shell completion for the current CLI.

      :param shell: Shell type (bash/zsh/fish) or auto-detect
      :param force: Force overwrite existing completion
      :return: True if installation successful
      """
      target_shell = shell or self.shell
      result = False

      if not self._cli_instance or not self._cli_instance.enable_completion:
        print("Completion is disabled for this CLI.", file=sys.stderr)
      elif not self._completion_handler:
        self.init_completion(target_shell)
        if not self._completion_handler:
          print("Completion handler not available.", file=sys.stderr)
      
      if self._completion_handler:
        try:
          from auto_cli.completion.installer import CompletionInstaller

          # Extract program name from sys.argv[0]
          prog_name = os.path.basename(sys.argv[0])
          if prog_name.endswith('.py'):
            prog_name = prog_name[:-3]

          installer = CompletionInstaller(self._completion_handler, prog_name)
          result = installer.install(target_shell, force)
        except ImportError:
          print("Completion installer not available.", file=sys.stderr)
      
      return result

    def show(self, shell: Optional[str] = None) -> None:
      """Show shell completion script.

      :param shell: Shell type (bash/zsh/fish)
      """
      target_shell = shell or self.shell

      if not self._cli_instance or not self._cli_instance.enable_completion:
        print("Completion is disabled for this CLI.", file=sys.stderr)
      else:
        # Initialize completion handler for specific shell
        self.init_completion(target_shell)

        if not self._completion_handler:
          print("Completion handler not available.", file=sys.stderr)
        else:
          # Extract program name from sys.argv[0]
          prog_name = os.path.basename(sys.argv[0])
          if prog_name.endswith('.py'):
            prog_name = prog_name[:-3]

          try:
            script = self._completion_handler.generate_script(prog_name)
            print(script)
          except Exception as e:
            print(f"Error generating completion script: {e}", file=sys.stderr)

    def handle_completion(self) -> None:
      """Handle completion request and exit."""
      exit_code = 0

      if not self._completion_handler:
        self.init_completion()

      if not self._completion_handler:
        exit_code = 1
      else:
        # Parse completion context from command line and environment
        try:
          from auto_cli.completion.base import CompletionContext

          # Get completion context
          words = sys.argv[:]
          current_word = ""
          cursor_pos = 0

          # Handle --_complete flag
          if '--_complete' in words:
            complete_idx = words.index('--_complete')
            words = words[:complete_idx]  # Remove --_complete and after
            if complete_idx < len(sys.argv) - 1:
              current_word = sys.argv[complete_idx + 1] if complete_idx + 1 < len(sys.argv) else ""

          # Extract command group path
          command_group_path = []
          if len(words) > 1:
            for word in words[1:]:
              if not word.startswith('-'):
                command_group_path.append(word)

          # Create parser for context
          parser = self._cli_instance.create_parser(no_color=True) if self._cli_instance else None

          # Create completion context
          context = CompletionContext(
            words=words,
            current_word=current_word,
            cursor_position=cursor_pos,
            command_group_path=command_group_path,
            parser=parser,
            cli=self._cli_instance
          )

          # Get completions and output them
          completions = self._completion_handler.get_completions(context)
          for completion in completions:
            print(completion)

        except ImportError:
          pass  # Completion module not available

      sys.exit(exit_code)

    def init_completion(self, shell: str = None):
      """Initialize completion handler if enabled.

      :param shell: Target shell (auto-detect if None)
      """
      if not self._cli_instance or not self._cli_instance.enable_completion:
        return

      try:
        from auto_cli.completion import get_completion_handler
        self._completion_handler = get_completion_handler(self._cli_instance, shell)
      except ImportError:
        # Completion module not available
        if self._cli_instance:
          self._cli_instance.enable_completion = False

    def is_completion_request(self) -> bool:
      """Check if this is a completion request."""
      return (
          '--_complete' in sys.argv or
          os.environ.get('_AUTO_CLI_COMPLETE') is not None
      )
