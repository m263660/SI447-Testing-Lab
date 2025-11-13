To test the Unit Tests and Integration Test use the following commands:

source .venv/bin/activate

pip install -U pip

pip install requests pytest

pytest -m unit -v

pytest -m integration -v
