# Question Answering (QA) Component of Elas4RDF

This repository contains code for the Question Answering Component of Elas4RDF.

It is used to provide answers for the QA tab of Elas4RDF ([demo available here](https://demos.isl.ics.forth.gr/elas4rdf)), but it can be used as a REST API as well.

Endpoint: `/answer`, Parameter: `question`, Example: `/answer?question=who is the father of Obama?`

Requirements:
1.	python 3
2.	pip 3
3.	pip modules in requirements.txt (install with: `pip3 install -r requirements.txt`)
4.	model files ([download here](https://drive.google.com/drive/folders/1-oGWdh5Zbl9bF_BpyXd__beJRAiyg-Ug?usp=sharing) to /resources folder)

To start:
1. development server: `flask run --host=0.0.0.0`
2. production server: `gunicorn IP:PORT --workers 1 --limit-request-line 0 app:app --daemon --error-logfile gunicorn_error.log --timeout 120`
