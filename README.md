# Pebble
An FastApi web server project that demonstrates and processes OSINT LIAR backend requests. This system
is intended to be a template and overtime collect additional features needed for individual developers or teams
that are interested in adding their tools into the OSINT LIAR ecosystem. To get a free trial license go to https://osintliar.com 

## How It Works
OSINT LIAR is built using event driven software design patterns. The Discovery Tools functionality in OSINT LIAR will
push your captured data upon Creation or Modification to services like Pebble. The original captured record is not altered
and a linked record with the outputs from Pebble is created. This preserves your evidence in its original state and
also enriches it simultaneously.

## Features

- OCR Text Extraction using Pytesseract
- Email Extraction
  - Regex Email Validator
- Phone Number Extraction
  - Regex Phone Number Validator
  - phonenumbers Python Library


## Discovery Plugins
The Discovery Plugins for passing data to Pebble already exist within OSINT LIAR. Search for 'pebble' in the 
Configuration Options -> Discovery Plugins section. Activate the plugins. Whenever you bring in new content into OSINT LIAR
it will be passed off to Pebble for enrichment. 


You will need to set up an Api Key in OSINT LIAR that points to the IP and port of the Pebble instance. 
Specifically, the `DevUrl` needs to be set to something like http://localhost:8000/


![alt text](assets/api_screenshot.png "Image of Api Key settings")

## Docker Setup

```shell
docker-compose build
docker-compose up
```

## Command line setup

```shell
pip install poetry
poetry shell
poetry install
poetry run uvicorn pebble.main:app --host 0.0.0.0 --port 8000 --reload
```


