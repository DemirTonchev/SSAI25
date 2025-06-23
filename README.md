# Summer School 25 Agents Environment Setup

This project provides two ways to set up the development environment: using Conda or Pixi. Choose the method that works best for your workflow.

## Prerequisites

Before starting, ensure you have one of the following package managers installed:

- **Pixi**: [Installation guide](https://pixi.sh/latest/#installation)
- **Miniconda/Mamba**: [Download here](https://conda-forge.org/download/)

If you already have one of the above, there is no need to install the other!

- **API key to LLM provider** - best for this exercise - get gemini api key.

## Option 1: Setup with Pixi

Pixi automatically manages both conda and PyPI dependencies in a single workflow.

### Install and run

```bash
# Install dependencies (creates virtual environment automatically)
pixi install

# Activate the environment
pixi shell

```

### Quick guide - managing the Pixi environment
Do not execute the commands, use for reference.

```bash
# Add new conda dependency
pixi add package-name

# Add new PyPI dependency
pixi add --pypi package-name

# Remove dependency
pixi remove package-name

# Update all dependencies
pixi update

# Clean environment
pixi clean
```


## Option 2: Setup with Conda

### Install from environment file

```bash
# Create and activate the environment
conda env create -f environment.yml
conda activate agents-ss25
```

### Quick guide - managing the Conda environment
Do not execute the commands, use for reference.

```bash
# Activate environment
conda activate agents-ss25

# In activated environment

conda install package-name
# or 
pip install package-name

# Remove environment (if needed)
conda env remove -n agents-ss25

# Update environment from file
conda env update -f environment.yml
```

## Troubleshooting

- **Conda**: If you encounter package conflicts, try creating a fresh environment
- **Pixi**: Run `pixi clean` followed by `pixi install` to reset the environment
- **General**: Ensure your package manager is up to date before installation