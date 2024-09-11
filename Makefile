include .env

.PHONY: setup \
		run \
		help


.venv/bin/activate: ## Alias for virtual environment
	python -m venv .venv

setup: .venv/bin/activate ## Project setup
	. .venv/bin/activate; pip install pip==${PIP_VERSION} wheel setuptools
	. .venv/bin/activate; pip install -Ur requirements/requirements.txt
	. .venv/bin/activate; pre-commit install

run: .venv/bin/activate ## Run project
	. .venv/bin/activate; uvicorn api.fast:app --host $(HOST)--port $(PORT) --reload

build: # Build service image
	docker build -t $(IMAGE_NAME) .

up: build # Start service
	docker run -d --rm \
		--name $(CONTAINER_NAME) \
		-v $(shell pwd)/sources:/sources \
		-p $(PORT):$(PORT) \
		$(IMAGE_NAME)  

down: # Stop service
	docker rm -f $(CONTAINER_NAME)

logs: # See service logs
	docker logs --tail=100 -f $(CONTAINER_NAME)