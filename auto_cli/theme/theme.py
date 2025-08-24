"""Complete color theme configuration with adjustment capabilities."""
from __future__ import annotations

from typing import Optional

from auto_cli.theme.enums import Back, Fore, ForeUniversal
from auto_cli.theme.rgb import AdjustStrategy, RGB
from auto_cli.theme.theme_style import ThemeStyle, CommandStyleSection


class Theme:
  """
  Complete color theme configuration for CLI output with dynamic adjustment capabilities.
  Defines styling for all major UI elements in the help output with optional color adjustment.
  
  Uses hierarchical CommandStyleSection structure internally, with backward compatibility properties
  for existing flat attribute access patterns.
  """

  def __init__(self, 
               # Hierarchical sections (new structure)
               topLevelCommandSection: Optional[CommandStyleSection] = None,
               commandGroupSection: Optional[CommandStyleSection] = None, 
               groupedCommandSection: Optional[CommandStyleSection] = None,
               # Non-sectioned attributes
               title: Optional[ThemeStyle] = None,
               subtitle: Optional[ThemeStyle] = None,
               required_asterisk: Optional[ThemeStyle] = None,
               # Backward compatibility: flat attributes (legacy constructor support)
               command_name: Optional[ThemeStyle] = None, 
               command_description: Optional[ThemeStyle] = None,
               command_group_name: Optional[ThemeStyle] = None, 
               command_group_description: Optional[ThemeStyle] = None,
               grouped_command_name: Optional[ThemeStyle] = None, 
               grouped_command_description: Optional[ThemeStyle] = None,
               option_name: Optional[ThemeStyle] = None, 
               option_description: Optional[ThemeStyle] = None,
               command_group_option_name: Optional[ThemeStyle] = None, 
               command_group_option_description: Optional[ThemeStyle] = None,
               grouped_command_option_name: Optional[ThemeStyle] = None, 
               grouped_command_option_description: Optional[ThemeStyle] = None,
               # Adjustment settings
               adjust_strategy: AdjustStrategy = AdjustStrategy.LINEAR, 
               adjust_percent: float = 0.0):
    """Initialize theme with hierarchical sections or backward compatible flat attributes."""
    if adjust_percent < -5.0 or adjust_percent > 5.0:
      raise ValueError(f"adjust_percent must be between -5.0 and 5.0, got {adjust_percent}")
      
    self.adjust_strategy = adjust_strategy
    self.adjust_percent = adjust_percent
    
    # Handle both hierarchical and flat initialization patterns
    if topLevelCommandSection is not None or commandGroupSection is not None or groupedCommandSection is not None:
      # New hierarchical initialization
      self.topLevelCommandSection = topLevelCommandSection or CommandStyleSection(
        command_name=ThemeStyle(), command_description=ThemeStyle(),
        option_name=ThemeStyle(), option_description=ThemeStyle()
      )
      self.commandGroupSection = commandGroupSection or CommandStyleSection(
        command_name=ThemeStyle(), command_description=ThemeStyle(),
        option_name=ThemeStyle(), option_description=ThemeStyle()
      )
      self.groupedCommandSection = groupedCommandSection or CommandStyleSection(
        command_name=ThemeStyle(), command_description=ThemeStyle(),
        option_name=ThemeStyle(), option_description=ThemeStyle()
      )
    else:
      # Legacy flat initialization - construct sections from flat attributes
      self.topLevelCommandSection = CommandStyleSection(
        command_name=command_name or ThemeStyle(),
        command_description=command_description or ThemeStyle(),
        option_name=option_name or ThemeStyle(),
        option_description=option_description or ThemeStyle()
      )
      self.commandGroupSection = CommandStyleSection(
        command_name=command_group_name or ThemeStyle(),
        command_description=command_group_description or ThemeStyle(),
        option_name=command_group_option_name or ThemeStyle(),
        option_description=command_group_option_description or ThemeStyle()
      )
      self.groupedCommandSection = CommandStyleSection(
        command_name=grouped_command_name or ThemeStyle(),
        command_description=grouped_command_description or ThemeStyle(),
        option_name=grouped_command_option_name or ThemeStyle(),
        option_description=grouped_command_option_description or ThemeStyle()
      )
    
    # Non-sectioned attributes
    self.title = title or ThemeStyle()
    self.subtitle = subtitle or ThemeStyle()
    self.required_asterisk = required_asterisk or ThemeStyle()

  # Backward compatibility properties for flat attribute access
  
  # Top-level command properties
  @property
  def command_name(self) -> ThemeStyle:
    """Top-level command name style (backward compatibility)."""
    return self.topLevelCommandSection.command_name
  
  @command_name.setter
  def command_name(self, value: ThemeStyle):
    self.topLevelCommandSection.command_name = value
  
  @property
  def command_description(self) -> ThemeStyle:
    """Top-level command description style (backward compatibility)."""
    return self.topLevelCommandSection.command_description
  
  @command_description.setter
  def command_description(self, value: ThemeStyle):
    self.topLevelCommandSection.command_description = value
  
  @property
  def option_name(self) -> ThemeStyle:
    """Top-level option name style (backward compatibility)."""
    return self.topLevelCommandSection.option_name
  
  @option_name.setter
  def option_name(self, value: ThemeStyle):
    self.topLevelCommandSection.option_name = value
  
  @property
  def option_description(self) -> ThemeStyle:
    """Top-level option description style (backward compatibility)."""
    return self.topLevelCommandSection.option_description
  
  @option_description.setter
  def option_description(self, value: ThemeStyle):
    self.topLevelCommandSection.option_description = value
  
  # Command group properties
  @property
  def command_group_name(self) -> ThemeStyle:
    """Command group name style (backward compatibility)."""
    return self.commandGroupSection.command_name
  
  @command_group_name.setter
  def command_group_name(self, value: ThemeStyle):
    self.commandGroupSection.command_name = value
  
  @property
  def command_group_description(self) -> ThemeStyle:
    """Command group description style (backward compatibility)."""
    return self.commandGroupSection.command_description
  
  @command_group_description.setter
  def command_group_description(self, value: ThemeStyle):
    self.commandGroupSection.command_description = value
  
  @property
  def command_group_option_name(self) -> ThemeStyle:
    """Command group option name style (backward compatibility)."""
    return self.commandGroupSection.option_name
  
  @command_group_option_name.setter
  def command_group_option_name(self, value: ThemeStyle):
    self.commandGroupSection.option_name = value
  
  @property
  def command_group_option_description(self) -> ThemeStyle:
    """Command group option description style (backward compatibility)."""
    return self.commandGroupSection.option_description
  
  @command_group_option_description.setter
  def command_group_option_description(self, value: ThemeStyle):
    self.commandGroupSection.option_description = value
  
  # Grouped command properties
  @property
  def grouped_command_name(self) -> ThemeStyle:
    """Grouped command name style (backward compatibility)."""
    return self.groupedCommandSection.command_name
  
  @grouped_command_name.setter
  def grouped_command_name(self, value: ThemeStyle):
    self.groupedCommandSection.command_name = value
  
  @property
  def grouped_command_description(self) -> ThemeStyle:
    """Grouped command description style (backward compatibility)."""
    return self.groupedCommandSection.command_description
  
  @grouped_command_description.setter
  def grouped_command_description(self, value: ThemeStyle):
    self.groupedCommandSection.command_description = value
  
  @property
  def grouped_command_option_name(self) -> ThemeStyle:
    """Grouped command option name style (backward compatibility)."""
    return self.groupedCommandSection.option_name
  
  @grouped_command_option_name.setter
  def grouped_command_option_name(self, value: ThemeStyle):
    self.groupedCommandSection.option_name = value
  
  @property
  def grouped_command_option_description(self) -> ThemeStyle:
    """Grouped command option description style (backward compatibility)."""
    return self.groupedCommandSection.option_description
  
  @grouped_command_option_description.setter
  def grouped_command_option_description(self, value: ThemeStyle):
    self.groupedCommandSection.option_description = value

  def create_adjusted_copy(self, adjust_percent: float, adjust_strategy: Optional[AdjustStrategy] = None) -> 'Theme':
    """Create a new theme with adjusted colors.

    :param adjust_percent: Adjustment percentage (-5.0 to 5.0)
    :param adjust_strategy: Optional strategy override
    :return: New Theme instance with adjusted colors
    """
    if adjust_percent < -5.0 or adjust_percent > 5.0:
      raise ValueError(f"adjust_percent must be between -5.0 and 5.0, got {adjust_percent}")

    strategy = adjust_strategy or self.adjust_strategy

    # Temporarily set adjustment parameters for the adjustment process
    old_adjust_percent = self.adjust_percent
    old_adjust_strategy = self.adjust_strategy
    self.adjust_percent = adjust_percent
    self.adjust_strategy = strategy

    try:
      # Create adjusted CommandStyleSection instances
      adjusted_top_level = CommandStyleSection(
        command_name=self.get_adjusted_style(self.topLevelCommandSection.command_name),
        command_description=self.get_adjusted_style(self.topLevelCommandSection.command_description),
        option_name=self.get_adjusted_style(self.topLevelCommandSection.option_name),
        option_description=self.get_adjusted_style(self.topLevelCommandSection.option_description)
      )
      
      adjusted_command_group = CommandStyleSection(
        command_name=self.get_adjusted_style(self.commandGroupSection.command_name),
        command_description=self.get_adjusted_style(self.commandGroupSection.command_description),
        option_name=self.get_adjusted_style(self.commandGroupSection.option_name),
        option_description=self.get_adjusted_style(self.commandGroupSection.option_description)
      )
      
      adjusted_grouped_command = CommandStyleSection(
        command_name=self.get_adjusted_style(self.groupedCommandSection.command_name),
        command_description=self.get_adjusted_style(self.groupedCommandSection.command_description),
        option_name=self.get_adjusted_style(self.groupedCommandSection.option_name),
        option_description=self.get_adjusted_style(self.groupedCommandSection.option_description)
      )

      # Create new theme using hierarchical constructor
      new_theme = Theme(
        topLevelCommandSection=adjusted_top_level,
        commandGroupSection=adjusted_command_group,
        groupedCommandSection=adjusted_grouped_command,
        title=self.get_adjusted_style(self.title),
        subtitle=self.get_adjusted_style(self.subtitle),
        required_asterisk=self.get_adjusted_style(self.required_asterisk),
        adjust_strategy=strategy,
        adjust_percent=adjust_percent
      )
    finally:
      # Restore original adjustment parameters
      self.adjust_percent = old_adjust_percent
      self.adjust_strategy = old_adjust_strategy

    return new_theme

  def get_adjusted_style(self, original: ThemeStyle) -> ThemeStyle:
    """Create a ThemeStyle with adjusted colors.

    :param original: Original ThemeStyle
    :return: ThemeStyle with adjusted colors
    """
    adjusted_fg = None
    if original.fg:
      # Use RGB adjustment method directly
      adjusted_fg = original.fg.adjust(brightness=self.adjust_percent, strategy=self.adjust_strategy)

    # Background adjustment disabled for now (as in original)
    adjusted_bg = original.bg

    return ThemeStyle(
      fg=adjusted_fg, bg=adjusted_bg, bold=original.bold, italic=original.italic, dim=original.dim,
      underline=original.underline
    )


def create_default_theme() -> Theme:
  """Create a default color theme using universal colors for optimal cross-platform compatibility."""
  # Create hierarchical sections
  top_level_section = CommandStyleSection(
    command_name=ThemeStyle(bold=True),
    command_description=ThemeStyle(bold=True),
    option_name=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.TEAL.value)),
    option_description=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.BROWN.value), bold=True)
  )
  
  command_group_section = CommandStyleSection(
    command_name=ThemeStyle(bold=True),
    command_description=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.BROWN.value), bold=True),
    option_name=ThemeStyle(),
    option_description=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.BROWN.value), bold=True)
  )
  
  grouped_command_section = CommandStyleSection(
    command_name=ThemeStyle(),
    command_description=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.BROWN.value), bold=True, italic=True),
    option_name=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.TEAL.value)),
    option_description=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.BROWN.value), bold=True)
  )
  
  return Theme(
    topLevelCommandSection=top_level_section,
    commandGroupSection=command_group_section,
    groupedCommandSection=grouped_command_section,
    title=ThemeStyle(bg=RGB.from_rgb(ForeUniversal.MEDIUM_GREY.value), bold=True),
    subtitle=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.TEAL.value), bold=True, italic=True),
    required_asterisk=ThemeStyle(fg=RGB.from_rgb(ForeUniversal.GOLD.value)),
    adjust_percent=0.0
  )


def create_default_theme_colorful() -> Theme:
  """Create a colorful theme with traditional terminal colors."""
  # Create hierarchical sections
  top_level_section = CommandStyleSection(
    command_name=ThemeStyle(fg=RGB.from_rgb(Fore.CYAN.value), bold=True),
    command_description=ThemeStyle(fg=RGB.from_rgb(Fore.LIGHTRED_EX.value)),
    option_name=ThemeStyle(fg=RGB.from_rgb(Fore.GREEN.value)),
    option_description=ThemeStyle(fg=RGB.from_rgb(Fore.YELLOW.value))
  )
  
  command_group_section = CommandStyleSection(
    command_name=ThemeStyle(fg=RGB.from_rgb(Fore.CYAN.value), bold=True),
    command_description=ThemeStyle(fg=RGB.from_rgb(Fore.LIGHTRED_EX.value)),
    option_name=ThemeStyle(fg=RGB.from_rgb(Fore.GREEN.value)),
    option_description=ThemeStyle(fg=RGB.from_rgb(Fore.YELLOW.value))
  )
  
  grouped_command_section = CommandStyleSection(
    command_name=ThemeStyle(fg=RGB.from_rgb(Fore.CYAN.value), italic=True, bold=True),
    command_description=ThemeStyle(fg=RGB.from_rgb(Fore.LIGHTRED_EX.value)),
    option_name=ThemeStyle(fg=RGB.from_rgb(Fore.GREEN.value)),
    option_description=ThemeStyle(fg=RGB.from_rgb(Fore.YELLOW.value))
  )
  
  return Theme(
    topLevelCommandSection=top_level_section,
    commandGroupSection=command_group_section,
    groupedCommandSection=grouped_command_section,
    title=ThemeStyle(fg=RGB.from_rgb(Fore.MAGENTA.value), bg=RGB.from_rgb(Back.LIGHTWHITE_EX.value), bold=True),
    subtitle=ThemeStyle(fg=RGB.from_rgb(Fore.YELLOW.value), italic=True),
    required_asterisk=ThemeStyle(fg=RGB.from_rgb(Fore.YELLOW.value))
  )


def create_no_color_theme() -> Theme:
  """Create a theme with no colors (fallback for non-color terminals)."""
  # Create hierarchical sections with no colors
  top_level_section = CommandStyleSection(
    command_name=ThemeStyle(),
    command_description=ThemeStyle(),
    option_name=ThemeStyle(),
    option_description=ThemeStyle()
  )
  
  command_group_section = CommandStyleSection(
    command_name=ThemeStyle(),
    command_description=ThemeStyle(),
    option_name=ThemeStyle(),
    option_description=ThemeStyle()
  )
  
  grouped_command_section = CommandStyleSection(
    command_name=ThemeStyle(),
    command_description=ThemeStyle(),
    option_name=ThemeStyle(),
    option_description=ThemeStyle()
  )
  
  return Theme(
    topLevelCommandSection=top_level_section,
    commandGroupSection=command_group_section,
    groupedCommandSection=grouped_command_section,
    title=ThemeStyle(),
    subtitle=ThemeStyle(),
    required_asterisk=ThemeStyle()
  )
