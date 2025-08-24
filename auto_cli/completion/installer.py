"""Completion installation and management."""

import os
import sys
from pathlib import Path
from typing import Optional

from .base import CompletionHandler


class CompletionInstaller:
  """Handles installation of shell completion scripts."""

  def __init__(self, handler: CompletionHandler, prog_name: str):
    """Initialize installer with handler and program name.

    :param handler: Completion handler for specific shell
    :param prog_name: Name of the program to install completion for
    """
    self.handler = handler
    self.prog_name = prog_name
    self.shell = handler.detect_shell()

  def install(self, shell: Optional[str] = None, force: bool = False) -> bool:
    """Install completion for specified or detected shell.

    :param shell: Target shell (auto-detect if None)
    :param force: Force overwrite existing completion
    :return: True if installation successful
    """
    target_shell = shell or self.shell

    if not target_shell:
      print("Could not detect shell. Please specify shell manually.", file=sys.stderr)
      return False

    if target_shell == 'bash':
      return self._install_bash_completion(force)
    elif target_shell == 'zsh':
      return self._install_zsh_completion(force)
    elif target_shell == 'fish':
      return self._install_fish_completion(force)
    elif target_shell == 'powershell':
      return self._install_powershell_completion(force)
    else:
      print(f"Unsupported shell: {target_shell}", file=sys.stderr)
      return False

  def _install_bash_completion(self, force: bool) -> bool:
    """Install bash completion."""
    # Try user completion directory first
    completion_dir = Path.home() / '.bash_completion.d'
    if not completion_dir.exists():
      completion_dir.mkdir(parents=True, exist_ok=True)

    completion_file = completion_dir / f'{self.prog_name}_completion'

    # Check if already exists
    if completion_file.exists() and not force:
      print(f"Completion already exists at {completion_file}. Use --force to overwrite.")
      return False

    # Generate and write completion script
    script = self.handler.generate_script(self.prog_name)
    completion_file.write_text(script)

    # Add sourcing to .bashrc if not already present
    bashrc = Path.home() / '.bashrc'
    source_line = f'source "{completion_file}"'

    if bashrc.exists():
      bashrc_content = bashrc.read_text()
      if source_line not in bashrc_content:
        with open(bashrc, 'a') as f:
          f.write(f'\n# Auto-CLI completion for {self.prog_name}\n')
          f.write(f'{source_line}\n')
        print(f"Added completion sourcing to {bashrc}")

    print(f"Bash completion installed to {completion_file}")
    print("Restart your shell or run: source ~/.bashrc")
    return True

  def _install_zsh_completion(self, force: bool) -> bool:
    """Install zsh completion."""
    # Try user completion directory
    completion_dirs = [
      Path.home() / '.zsh' / 'completions',
      Path.home() / '.oh-my-zsh' / 'completions',
      Path('/usr/local/share/zsh/site-functions')
    ]

    # Find first writable directory
    completion_dir = None
    for dir_path in completion_dirs:
      if dir_path.exists() or dir_path.parent.exists():
        completion_dir = dir_path
        break

    if not completion_dir:
      completion_dir = completion_dirs[0]  # Default to first option

    completion_dir.mkdir(parents=True, exist_ok=True)
    completion_file = completion_dir / f'_{self.prog_name}'

    # Check if already exists
    if completion_file.exists() and not force:
      print(f"Completion already exists at {completion_file}. Use --force to overwrite.")
      return False

    # Generate and write completion script
    script = self.handler.generate_script(self.prog_name)
    completion_file.write_text(script)

    print(f"Zsh completion installed to {completion_file}")
    print("Restart your shell for changes to take effect")
    return True

  def _install_fish_completion(self, force: bool) -> bool:
    """Install fish completion."""
    completion_dir = Path.home() / '.config' / 'fish' / 'completions'
    completion_dir.mkdir(parents=True, exist_ok=True)

    completion_file = completion_dir / f'{self.prog_name}.fish'

    # Check if already exists
    if completion_file.exists() and not force:
      print(f"Completion already exists at {completion_file}. Use --force to overwrite.")
      return False

    # Generate and write completion script
    script = self.handler.generate_script(self.prog_name)
    completion_file.write_text(script)

    print(f"Fish completion installed to {completion_file}")
    print("Restart your shell for changes to take effect")
    return True

  def _install_powershell_completion(self, force: bool) -> bool:
    """Install PowerShell completion."""
    # PowerShell profile path
    if os.name == 'nt':
      # Windows PowerShell
      profile_dir = Path(os.environ.get('USERPROFILE', '')) / 'Documents' / 'WindowsPowerShell'
    else:
      # PowerShell Core on Unix
      profile_dir = Path.home() / '.config' / 'powershell'

    profile_dir.mkdir(parents=True, exist_ok=True)
    profile_file = profile_dir / 'Microsoft.PowerShell_profile.ps1'

    # Generate completion script
    script = self.handler.generate_script(self.prog_name)

    # Check if profile exists and has our completion
    completion_marker = f'# Auto-CLI completion for {self.prog_name}'

    if profile_file.exists():
      profile_content = profile_file.read_text()
      if completion_marker in profile_content and not force:
        print(f"Completion already installed in {profile_file}. Use --force to overwrite.")
        return False

      # Remove old completion if forcing
      if force and completion_marker in profile_content:
        lines = profile_content.split('\n')
        new_lines = []
        skip_next = False

        for line in lines:
          if completion_marker in line:
            skip_next = True
            continue
          if skip_next and line.strip().startswith('Register-ArgumentCompleter'):
            skip_next = False
            continue
          new_lines.append(line)

        profile_content = '\n'.join(new_lines)
    else:
      profile_content = ''

    # Add completion to profile
    with open(profile_file, 'w') as f:
      f.write(profile_content)
      f.write(f'\n{completion_marker}\n')
      f.write(script)

    print(f"PowerShell completion installed to {profile_file}")
    print("Restart PowerShell for changes to take effect")
    return True

  def uninstall(self, shell: Optional[str] = None) -> bool:
    """Remove installed completion.

    :param shell: Target shell (auto-detect if None)
    :return: True if uninstallation successful
    """
    target_shell = shell or self.shell

    if not target_shell:
      print("Could not detect shell. Please specify shell manually.", file=sys.stderr)
      return False

    success = False

    if target_shell == 'bash':
      completion_file = Path.home() / '.bash_completion.d' / f'{self.prog_name}_completion'
      if completion_file.exists():
        completion_file.unlink()
        success = True

    elif target_shell == 'zsh':
      completion_dirs = [
        Path.home() / '.zsh' / 'completions',
        Path.home() / '.oh-my-zsh' / 'completions',
        Path('/usr/local/share/zsh/site-functions')
      ]

      for dir_path in completion_dirs:
        completion_file = dir_path / f'_{self.prog_name}'
        if completion_file.exists():
          completion_file.unlink()
          success = True

    elif target_shell == 'fish':
      completion_file = Path.home() / '.config' / 'fish' / 'completions' / f'{self.prog_name}.fish'
      if completion_file.exists():
        completion_file.unlink()
        success = True

    elif target_shell == 'powershell':
      # For PowerShell, we would need to edit the profile file
      print("PowerShell completion uninstall requires manual removal from profile.")
      return False

    if success:
      print(f"Completion uninstalled for {target_shell}")
    else:
      print(f"No completion found to uninstall for {target_shell}")

    return success
