#!/bin/bash
cd "$(dirname "$0")/behave_tests" && PYTHONPATH=.. python -m behave "$@"
