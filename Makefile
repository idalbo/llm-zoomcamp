.PHONY: help up venv install all

help:
	@echo "Available commands:"
	@echo "  up      - Start Elasticsearch with docker-compose"
	@echo "  venv    - Create Python virtual environment"
	@echo "  install - Install Python requirements into venv"
	@echo "  all     - Set up venv, install requirements, and start Elasticsearch"

up:
	docker-compose -f docker-compose.elasticsearch.yaml up -d 

venv:
	python3 -m venv venv

install: venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

all: install up
	@echo "Environment ready: venv, requirements installed, and Elasticsearch running."

down:
	docker-compose -f docker-compose.elasticsearch.yaml down

clean:
	rm -rf venv
	docker-compose -f docker-compose.elasticsearch.yaml down --volumes --remove-orphans