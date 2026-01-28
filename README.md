# auto-cli-py
Python Library that builds a complete CLI given one or more functions.

Most options are set using introspection/signature and annotation functionality, so very little configuration has to be done.

## Setup
@@DEPRECATED; USE https://github.com/terracoil/freyja at https://pypi.org/project/freyja/ instead.

### TL;DR Install for usage
```bash
# Install from github
pip install auto-cli-py

# See example code and output
python examples.py

```

### In python code
## Development
* Standard python packaging - Follows methodologies from: https://python-packaging.readthedocs.io/en/latest/minimal
.html
* Uses pytest

### Pytest
https://docs.pytest.org/en/latest/

### Python (Anaconda) environment
*(assumes anaconda is properly installed)*
```bash
# First time. Create conda environment from environment.yml and activate it:
conda env create -f environment.yml -n auto-cli-py
conda activate auto-cli-py
```

```bash
# If environment changes:
conda activate auto-cli-py
conda env update -f=environment.yml
# -- OR remove and restart --
conda remove --name auto-cli-py --all
conda env create -f environment.yml
```

### Activate environment
```bash
conda activate auto-cli-py

# This symlinks the installed auto_cli package to the source:
pip install -e .
```

### Preparation
```bash
conda activate auto-cli-py
```

### Linting and Testing
*pytest behavior and output is controlled through `auto_cli/tests/pytest.ini`*

```bash
# Lint all code:
pylint auto_cli

# Run all tests
pytest

# See more options for pytest:
pytest --help

# This is handy:
pytest --fixtures-per-test

```

### Installation (other)

```bash
# AND/OR Install from a specific github branch
pip uninstall auto-cli-py
pip install git+https://github.com/tangledpath/auto-cli-py.git@features/blah
```

