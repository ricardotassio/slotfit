PYTHON := uv run --python 3.12 python

.PHONY: test api-test review-test api-smoke web-build web-test screenshots verify docker-build docker-run docker-test demo multi-slot-demo generated-demo longitudinal-demo development-report alternative-diagnostic exposure-frontier

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

api-test:
	PYTHONPATH=src $(PYTHON) -m unittest tests.test_api_contract -v

review-test:
	PYTHONPATH=src $(PYTHON) -m unittest tests.test_review_persistence tests.test_review_api -v

api-smoke:
	PYTHONPATH=src $(PYTHON) -c 'from fastapi.testclient import TestClient; from slotfit.composition import app; client = TestClient(app); assert client.get("/health").status_code == 200; assert client.get("/api/v1/demos/global-conflict").status_code == 200; assert client.get("/api/v1/research/development-decision").json()["candidate_accepted"] is False'

web-build:
	npm --prefix web run build

web-test:
	npm --prefix web run test:e2e

screenshots:
	npm --prefix web run screenshots

verify: test api-smoke web-build web-test

demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.demo --seed 1400

multi-slot-demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.demo --mode multi-slot --seed 1500

generated-demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.demo --mode generated --seed 1101

longitudinal-demo:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.demo --mode generated --seed 1101 --rounds 3

development-report:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.report --split development

alternative-diagnostic:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.diagnostic

exposure-frontier:
	PYTHONPATH=src $(PYTHON) -m slotfit.adapters.cli.frontier

docker-build:
	docker build -t slotfit:local .

docker-run:
	docker compose up --build

docker-test:
	docker run --rm slotfit:local python -m unittest discover -s tests
	docker run --rm slotfit:local python -c 'from fastapi.testclient import TestClient; from slotfit.composition import app; client = TestClient(app); assert client.get("/health").status_code == 200; assert client.get("/").status_code == 200; assert client.get("/api/v1/demos/clinic-day").status_code == 200'
