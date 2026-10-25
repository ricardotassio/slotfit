PYTHON := uv run --no-project --python 3.12 python

.PHONY: test demo multi-slot-demo generated-demo longitudinal-demo

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.cli --seed 1400

multi-slot-demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.cli --mode multi-slot --seed 1500

generated-demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.cli --mode generated --seed 1101

longitudinal-demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.cli --mode generated --seed 1101 --rounds 3
