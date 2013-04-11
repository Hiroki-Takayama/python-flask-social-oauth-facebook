.PHONY: help install server

help:
	@echo "make install"
	@echo "make server"

install:
	virtualenv --no-site-package venv
	. venv/bin/activate
	pip install -r requirements.txt

server:
	@. venv/bin/activate; python manager.py runserver
    