"""Legacy compatibility wrapper for ThemeTuner.

This module provides backward compatibility for direct ThemeTuner usage.
New code should use System.TuneTheme instead.
"""

import warnings


def ThemeTuner(*args, **kwargs):
  """Legacy ThemeTuner factory.

  Deprecated: Use System().TuneTheme() instead.
  """
  warnings.warn(
    "ThemeTuner is deprecated. Use System().TuneTheme() instead.",
    DeprecationWarning,
    stacklevel=2
  )
  from auto_cli.system import System
  return System().TuneTheme(*args, **kwargs)


def run_theme_tuner(base_theme: str = "universal") -> None:
  """Convenience function to run the theme tuner (legacy compatibility).

  :param base_theme: Base theme to start with (universal or colorful)
  """
  warnings.warn(
    "run_theme_tuner is deprecated. Use System().TuneTheme().run_interactive() instead.",
    DeprecationWarning,
    stacklevel=2
  )
  from auto_cli.system import System
  tuner = System().TuneTheme(base_theme)
  tuner.run_interactive()
