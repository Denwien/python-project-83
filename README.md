# Hexlet Page Analyzer

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Denwien/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Denwien/python-project-83/actions/workflows/hexlet-check.yml)
[![Linter Status](https://github.com/Denwien/python-project-83/actions/workflows/my_workflow.yml/badge.svg)](https://github.com/Denwien/python-project-83/actions/workflows/my_workflow.yml)

### SonarQube Quality Gate:
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=Denwien_python-project-83&metric=alert_status)](https://sonarcloud.io/dashboard?id=Denwien_python-project-83)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Denwien_python-project-83&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=Denwien_python-project-83)

## About

Hexlet Page Analyzer is a web application for checking and analyzing web pages. It lets you add any URL, run HTTP checks against it, and extract key SEO metadata — all stored with a full history of past checks.

**Built with:** Python, Flask, PostgreSQL, BeautifulSoup, Gunicorn.

## Features

- Add URLs for analysis
- Check page availability (HTTP status code)
- Extract SEO data: `h1`, `title`, `description`
- Browse the full history of checks per URL

## Requirements

- Python 3.10+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

```bash
git clone https://github.com/Denwien/python-project-83.git
cd python-project-83
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/page_analyzer
SECRET_KEY=your-secret-key
```

Initialize the database (run once):

```bash
psql -a -d "$DATABASE_URL" -f database.sql
```

Install dependencies:

```bash
make install
```

## Usage

**Development server:**

```bash
make dev
```

**Production server:**

```bash
make start
```

The app will be available at `http://localhost:8000`.

## Makefile commands

| Command        | Description                        |
|----------------|------------------------------------|
| `make install` | Install dependencies via uv        |
| `make dev`     | Run Flask dev server with debugger |
| `make start`   | Run Gunicorn production server     |
| `make lint`    | Run ruff linter                    |
| `make build`   | Install uv and initialize the DB   |
