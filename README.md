# llm-zoomcamp

This repository contains the code for the LLM Zoomcamp course and the solutions to the exercises.

## Get LLM platform API key

Depending on the LLM platform you want to use, you need to create an account and get the API key. Here, I use [Groq](https://groq.com/), but you can use any other plaform of your choice. Just make sure to do the following once you have the API key:

* create a file called `.env` in the root of the repository and add the following line to it:
```
GROQ_API_KEY=<your_api_key>
```
* replace `<your_api_key>` with your actual API key.
* adapt the code to use the LLM platform of your choice. The code is written in a way that it can be easily adapted to any LLM platform. Just replace the `groq` module with the module of the LLM platform you want to use and change the API calls accordingly.

## How to run

If you don't want to use Github Codespaces, you can run the code locally using the template in the root of this repository. This template includes a `Makefile` that automates the setup process. You will need to have Docker and Python 3 installed on your machine.

The following commands are available::

* `make all`: this will create a python virtual environment, install the dependencies, and start all the containers. **Run this command before interacting with the code.**
* `make down`: this will stop the containers
* `make install`: this will install the dependencies in the virtual environment.
* `make venv`: this will create a python virtual environment.
* `make up`: this will start all the containers.
* `make clean`: this will remove the python virtual environment and all the containers.

**Note**: `make all` already runs `make venv`, `make install`, and `make up`, so you don't need to run them separately.

Current list of services spun up: elasticsearch, qdrant