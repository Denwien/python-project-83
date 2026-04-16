#!/bin/bash

pip install poetry
poetry install && psql -a -d "$DATABASE_URL" -f database.sql
