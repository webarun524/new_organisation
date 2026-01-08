#!/bin/bash
set -euxo pipefail

apt-get update && apt-get install -y curl
curl -sSL https://install.python-poetry.org | python3 - --version 2.2.1

export POETRY_HOME=/root/.local
export PATH="$POETRY_HOME/bin:$PATH"
$POETRY_HOME/bin/poetry --version
