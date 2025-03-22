# Sequence Extractor

Implemented as a simple UI application built with Python and [Tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter).

## Requirements

- Python 3.13 or later
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Installing uv

Before you can use this project, you need to install uv on your Mac:

```bash
# Using Homebrew (recommended)
brew install uv

# Or using pip
pip install uv
```

For more installation options, see the [uv installation guide](https://github.com/astral-sh/uv#installation).

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd sequence_extractor
   ```

2. Create a virtual environment using uv:
   ```bash
   uv venv
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   uv pip install -e .
   ```

## Running the Application

After installation, you can run the application:

```bash
uv run main.py
```

## Managing Dependencies

### Adding New Dependencies

To add a new dependency:

1. Add it to the `dependencies` list in `pyproject.toml`:
   ```toml
   dependencies = [
       "package-name>=1.0.0",
   ]
   ```

2. Install the updated dependencies:
   ```bash
   uv pip install -e .
   ```

### Adding Development Dependencies

For development-only dependencies:

1. Add a `[project.optional-dependencies]` section to `pyproject.toml`:
   ```toml
   [project.optional-dependencies]
   dev = [
       "pytest>=7.0.0",
       "black>=23.0.0",
   ]
   ```

2. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

## Running Tests

If you've added pytest as a development dependency:

```bash
uv run pytest
```
