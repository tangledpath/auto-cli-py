#!/usr/bin/env python
"""Class-based CLI example demonstrating inner class hierarchical command organization."""

import enum
import sys
from pathlib import Path

from auto_cli.cli import CLI


class ProcessingMode(enum.Enum):
  """Processing modes for data operations."""
  FAST = "fast"
  THOROUGH = "thorough"
  BALANCED = "balanced"


class OutputFormat(enum.Enum):
  """Supported output formats."""
  JSON = "json"
  CSV = "csv"
  XML = "xml"


class DataProcessor:
  """Enhanced data processing utility with hierarchical organization.

  This class demonstrates the inner class pattern where each inner class
  provides command organization. Methods within inner classes become
  hierarchical commands (e.g., file-operations process-single) with
  proper command groups and subcommands.
  """

  def __init__(self, config_file: str = "config.json", verbose: bool = False):
    """Initialize the data processor with global settings.

    :param config_file: Configuration file path for global settings
    :param verbose: Enable verbose output across all operations
    """
    self.config_file = config_file
    self.verbose = verbose
    self.processed_count = 0

    if self.verbose:
      print(f"📁 DataProcessor initialized with config: {self.config_file}")

  def foo(self, text: str):
    print(text)

  class FileOperations:
    """File processing operations with batch capabilities."""

    def __init__(self, main_instance, work_dir: str = "./data", backup: bool = True):
      """Initialize file operations with working directory settings.

      :param main_instance: Main DataProcessor instance with global configuration
      :param work_dir: Working directory for file operations
      :param backup: Create backup copies before processing
      """
      self.main_instance = main_instance
      self.work_dir = work_dir
      self.backup = backup

    def process_single(self, input_file: Path,
                       mode: ProcessingMode = ProcessingMode.BALANCED,
                       dry_run: bool = False):
      """Process a single file with specified parameters.

      :param input_file: Path to the input file to process
      :param mode: Processing mode affecting speed vs quality
      :param dry_run: Show what would be processed without actual processing
      """
      action = "Would process" if dry_run else "Processing"
      print(f"{action} file: {input_file}")
      print(f"Global config: {self.main_instance.config_file}")
      print(f"Working directory: {self.work_dir}")
      print(f"Mode: {mode.value}")
      print(f"Backup enabled: {self.backup}")
      
      if self.main_instance.verbose:
        print(f"📝 Verbose: Using global settings from {self.main_instance.config_file}")
        print(f"📝 Verbose: Main instance processed count: {self.main_instance.processed_count}")

      if not dry_run:
        print(f"✓ File processed successfully")

      return {"file": str(input_file), "mode": mode.value, "dry_run": dry_run}

    def batch_process(self, pattern: str, max_files: int = 100,
                      parallel: bool = False):
      """Process multiple files matching a pattern.

      :param pattern: File pattern to match (e.g., '*.txt')
      :param max_files: Maximum number of files to process
      :param parallel: Enable parallel processing for better performance
      """
      processing_mode = "parallel" if parallel else "sequential"
      print(f"Batch processing {max_files} files matching '{pattern}'")
      print(f"Global config: {self.main_instance.config_file}")
      print(f"Working directory: {self.work_dir}")
      print(f"Processing mode: {processing_mode}")
      print(f"Backup enabled: {self.backup}")
      
      if self.main_instance.verbose:
        print(f"📝 Verbose: Batch processing using global config from {self.main_instance.config_file}")

      # Simulate processing
      for i in range(min(3, max_files)):  # Demo with just 3 files
        print(f"  Processing file {i + 1}: example_{i + 1}.txt")

      print(f"✓ Processed {min(3, max_files)} files")
      return {"pattern": pattern, "files_processed": min(3, max_files), "parallel": parallel}

  class ExportOperations:
    """Data export operations with format conversion."""

    def __init__(self, main_instance, output_dir: str = "./exports"):
      """Initialize export operations.

      :param main_instance: Main DataProcessor instance with global configuration
      :param output_dir: Output directory for exported files
      """
      self.main_instance = main_instance
      self.output_dir = output_dir

    def export_results(self, format: OutputFormat = OutputFormat.JSON,
                       compress: bool = True, include_metadata: bool = False):
      """Export processing results in specified format.

      :param format: Output format for export
      :param compress: Compress the output file
      :param include_metadata: Include processing metadata in export
      """
      compression_status = "compressed" if compress else "uncompressed"
      metadata_status = "with metadata" if include_metadata else "without metadata"

      print(f"Exporting results to {compression_status} {format.value} {metadata_status}")
      print(f"Output directory: {self.output_dir}")
      print(f"✓ Export completed: results.{format.value}{'.gz' if compress else ''}")

      return {
        "format": format.value,
        "compressed": compress,
        "metadata": include_metadata,
        "output_dir": self.output_dir
      }

    def convert_format(self, input_file: Path, target_format: OutputFormat,
                       preserve_original: bool = True):
      """Convert existing file to different format.

      :param input_file: Path to file to convert
      :param target_format: Target format for conversion
      :param preserve_original: Keep original file after conversion
      """
      preservation = "preserving" if preserve_original else "replacing"
      print(f"Converting {input_file} to {target_format.value} format")
      print(f"Output directory: {self.output_dir}")
      print(f"Original file: {preservation}")
      print(f"✓ Conversion completed")

      return {
        "input": str(input_file),
        "target_format": target_format.value,
        "preserved": preserve_original
      }

  class ConfigManagement:
    """Configuration management operations."""

    def __init__(self, main_instance):
      """Initialize configuration management.
      
      :param main_instance: Main DataProcessor instance with global configuration
      """
      self.main_instance = main_instance

    def set_default_mode(self, mode: ProcessingMode):
      """Set the default processing mode for future operations.

      :param mode: Default processing mode to use
      """
      print(f"🔧 Setting default processing mode to: {mode.value}")
      print("✓ Configuration updated")
      return {"default_mode": mode.value}

    def show_settings(self, detailed: bool = False):
      """Display current configuration settings.

      :param detailed: Show detailed configuration breakdown
      """
      print("📋 Current Configuration:")
      print(f"  Default mode: balanced")  # Would be dynamic in real implementation

      if detailed:
        print("  Detailed settings:")
        print("    - Processing threads: 4")
        print("    - Memory limit: 1GB")
        print("    - Timeout: 30s")

      print("✓ Settings displayed")
      return {"detailed": detailed}

  class Statistics:
    """Processing statistics and reporting."""

    def __init__(self, main_instance, include_history: bool = False):
      """Initialize statistics reporting.

      :param main_instance: Main DataProcessor instance with global configuration
      :param include_history: Include historical statistics in reports
      """
      self.main_instance = main_instance
      self.include_history = include_history

    def summary(self, detailed: bool = False):
      """Show processing statistics summary.

      :param detailed: Include detailed statistics breakdown
      """
      print(f"📊 Processing Statistics:")
      print(f"  Total files processed: 42")  # Would be dynamic
      print(f"  History included: {self.include_history}")

      if detailed:
        print("  Detailed breakdown:")
        print("    - Successful: 100%")
        print("    - Average time: 0.5s per file")
        print("    - Memory usage: 45MB peak")

      return {"detailed": detailed, "include_history": self.include_history}

    def export_report(self, format: OutputFormat = OutputFormat.JSON):
      """Export detailed statistics report.

      :param format: Format for exported report
      """
      print(f"📈 Exporting statistics report in {format.value} format")
      print(f"History included: {self.include_history}")
      print("✓ Report exported successfully")

      return {"format": format.value, "include_history": self.include_history}


if __name__ == '__main__':
  # Import theme functionality
  from auto_cli.theme import create_default_theme

  # Create CLI from class with colored theme
  theme = create_default_theme()
  cli = CLI(
    DataProcessor,
    theme=theme,
    enable_completion=True
  )

  # Run the CLI and exit with appropriate code
  result = cli.run()
  sys.exit(result if isinstance(result, int) else 0)
