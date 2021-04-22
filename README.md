# LookingGlassAPI

[![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

 An GraphQL API wrapper around a postgres database backend. The API is designed for use in gameplay tracking systems Looking Glass Desktop and Looking Glass Mobile.

## Installation

Note: it is recommended but not required to use a virtual environment when installing the requirements

```bash
git clone https://github.com/Morioki/LookingGlass.API.git

cd LookingGlass.API

pip install -r requirements.txt
```

## Usage

```bash
# Running
source devFlaskSetup.env
flask run --host 0.0.0.0

# Testing 
pytest # from within the root of the project

# Linting
pylint api # from within the root of the project

```

