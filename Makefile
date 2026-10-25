PYTHON := uv run --no-project --python 3.12 python

.PHONY: test demo

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.cli --seed 1400
