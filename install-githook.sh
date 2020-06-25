#!/usr/bin/env bash

pip install --upgrade docformatter
pip install --upgrade black
pip install --upgrade pre-commit

pre-commit install -f
