"""Formatting engine for CLI help text generation.

Consolidates all formatting logic for commands, options, groups, and descriptions.
Eliminates duplication across formatter methods while maintaining consistent alignment.
"""

from typing import List, Tuple, Optional, Dict, Any
import argparse
import textwrap


class FormattingEngine:
    """Centralized formatting engine for CLI help text generation."""

    def __init__(self, console_width: int = 80, theme=None, color_formatter=None):
        """Formatting engine needs display constraints and styling capabilities.""" 
        self.console_width = console_width
        self.theme = theme
        self.color_formatter = color_formatter

    def format_command_with_description(self, name: str, parser: argparse.ArgumentParser,
                                      base_indent: int, description_column: int,
                                      name_style: str, desc_style: str,
                                      add_colon: bool = True) -> List[str]:
        """Format command with description using unified alignment strategy."""
        lines = []
        
        # Get help text from parser
        help_text = parser.description or getattr(parser, 'help', '')
        
        if help_text:
            formatted_lines = self.format_inline_description(
                name=name,
                description=help_text,
                name_indent=base_indent,
                description_column=description_column,
                style_name=name_style,
                style_description=desc_style,
                add_colon=add_colon
            )
            lines.extend(formatted_lines)
        else:
            # No description - just format the name
            styled_name = self._apply_style(name, name_style)
            name_line = ' ' * base_indent + styled_name
            if add_colon:
                name_line += ':'
            lines.append(name_line)
        
        return lines

    def format_inline_description(self, name: str, description: str,
                                name_indent: int, description_column: int,
                                style_name: str, style_description: str,
                                add_colon: bool = True) -> List[str]:
        """Format name and description with consistent column alignment."""
        lines = []
        
        # Apply styling to name
        styled_name = self._apply_style(name, style_name)
        
        # Calculate name section with colon
        name_section = ' ' * name_indent + styled_name
        if add_colon:
            name_section += ':'
        
        # Calculate available width for description wrapping
        desc_start_col = max(description_column, len(name_section) + 2)
        available_width = max(20, self.console_width - desc_start_col)
        
        # Wrap description text
        wrapped_desc = textwrap.fill(
            description, 
            width=available_width,
            subsequent_indent=' ' * desc_start_col
        )
        desc_lines = wrapped_desc.split('\n')
        
        # Style description lines
        styled_desc_lines = [self._apply_style(line.strip(), desc_style) for line in desc_lines]
        
        # Check if description fits on first line
        first_desc_styled = styled_desc_lines[0] if styled_desc_lines else ''
        name_with_desc = name_section + ' ' * (desc_start_col - len(name_section)) + first_desc_styled
        
        if len(name_section) + 2 <= description_column and first_desc_styled:
            # Description fits on same line
            lines.append(name_with_desc)
            # Add remaining wrapped lines
            for desc_line in styled_desc_lines[1:]:
                if desc_line.strip():
                    lines.append(' ' * desc_start_col + desc_line)
        else:
            # Put description on next line
            lines.append(name_section)
            for desc_line in styled_desc_lines:
                if desc_line.strip():
                    lines.append(' ' * description_column + desc_line)
        
        return lines

    def format_argument_list(self, required_args: List[str], optional_args: List[str], 
                           base_indent: int, option_column: int) -> List[str]:
        """Format argument lists with consistent alignment and styling."""
        lines = []
        
        # Format required arguments
        if required_args:
            for arg in required_args:
                styled_arg = self._apply_style(arg, 'required_option_name')
                asterisk = self._apply_style(' *', 'required_asterisk')
                arg_line = ' ' * base_indent + styled_arg + asterisk
                
                # Add description if available
                desc = self._get_argument_description(arg)
                if desc:
                    formatted_desc_lines = self.format_inline_description(
                        name=arg,
                        description=desc,
                        name_indent=base_indent,
                        description_column=option_column,
                        style_name='required_option_name',
                        style_description='required_option_description',
                        add_colon=False
                    )
                    lines.extend(formatted_desc_lines)
                else:
                    lines.append(arg_line)
        
        # Format optional arguments
        if optional_args:
            for arg in optional_args:
                styled_arg = self._apply_style(arg, 'option_name')
                arg_line = ' ' * base_indent + styled_arg
                
                # Add description if available
                desc = self._get_argument_description(arg)
                if desc:
                    formatted_desc_lines = self.format_inline_description(
                        name=arg,
                        description=desc,
                        name_indent=base_indent,
                        description_column=option_column,
                        style_name='option_name',
                        style_description='option_description',
                        add_colon=False
                    )
                    lines.extend(formatted_desc_lines)
                else:
                    lines.append(arg_line)
        
        return lines

    def calculate_column_widths(self, items: List[Tuple[str, str]], 
                              base_indent: int, max_name_width: int = 30) -> Tuple[int, int]:
        """Calculate optimal column widths for name and description alignment."""
        max_name_len = 0
        
        for name, _ in items:
            name_len = len(name) + base_indent + 2  # +2 for colon and space
            if name_len <= max_name_width:
                max_name_len = max(max_name_len, name_len)
        
        # Ensure minimum spacing and reasonable description width
        desc_column = max(max_name_len + 2, base_indent + 20)
        desc_column = min(desc_column, self.console_width // 2)
        
        return max_name_len, desc_column

    def wrap_text(self, text: str, width: int, indent: int = 0, 
                  subsequent_indent: Optional[int] = None) -> List[str]:
        """Wrap text with proper indentation and width constraints."""
        if subsequent_indent is None:
            subsequent_indent = indent
        
        wrapped = textwrap.fill(
            text,
            width=width,
            initial_indent=' ' * indent,
            subsequent_indent=' ' * subsequent_indent
        )
        return wrapped.split('\n')

    def _apply_style(self, text: str, style_name: str) -> str:
        """Apply styling to text if theme and formatter are available."""
        if not self.theme or not self.color_formatter:
            return text
        
        style = getattr(self.theme, style_name, None)
        if style:
            return self.color_formatter.apply_style(text, style)
        
        return text

    def _get_argument_description(self, arg: str) -> Optional[str]:
        """Get description for argument from parser metadata."""
        # This would be populated by the formatter with actual argument metadata
        # For now, return None as this is handled by the existing formatter logic
        return None

    def format_section_header(self, title: str, base_indent: int = 0) -> List[str]:
        """Format section headers with consistent styling."""
        styled_title = self._apply_style(title, 'subtitle')
        return [' ' * base_indent + styled_title + ':']

    def format_usage_line(self, prog: str, usage_parts: List[str], 
                         max_width: int = None) -> List[str]:
        """Format usage line with proper wrapping."""
        if max_width is None:
            max_width = self.console_width
        
        usage_prefix = f"usage: {prog} "
        usage_text = usage_prefix + ' '.join(usage_parts)
        
        if len(usage_text) <= max_width:
            return [usage_text]
        
        # Wrap with proper indentation
        indent = len(usage_prefix)
        return self.wrap_text(
            ' '.join(usage_parts), 
            max_width - indent, 
            indent, 
            indent
        )

    def format_command_group_header(self, group_name: str, description: str, 
                                  base_indent: int = 0) -> List[str]:
        """Format command group headers with description."""
        lines = []
        
        # Group name with styling
        styled_name = self._apply_style(group_name.upper(), 'subtitle')
        lines.append(' ' * base_indent + styled_name + ':')
        
        # Group description if available
        if description:
            desc_lines = self.wrap_text(description, self.console_width - base_indent - 2, base_indent + 2)
            lines.extend(desc_lines)
        
        return lines