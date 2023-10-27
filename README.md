## Page analyzer
### [Visit the site](https://page-analyzer-zx8t.onrender.com/)
### Hexlet tests and linter status:
[![Actions Status](https://github.com/BezrezenTLNH/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/BezrezenTLNH/python-project-83/actions)
[![CI](https://github.com/BezrezenTLNH/python-project-83/actions/workflows/CI.yml/badge.svg)](https://github.com/BezrezenTLNH/python-project-83/actions/workflows/CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/c018d23b6d3aa96ea3a6/maintainability)](https://codeclimate.com/github/BezrezenTLNH/python-project-83/maintainability)

## Description

This is a web service for checking metadata from sites using databases.

## Requirements:
* python ^3.8.1
* poetry ^1.3.2
* PostgreSQL ^12.16
* gunicorn ^20.1.0
* Flask ^2.3.2
* validators ^0.20.0
* python-dotenv ^1.0.0
* psycopg2-binary ^2.9.7
* requests ^2.31.0
* BeautifulSoup4 ^4.12.2
* pytest ^7.4.2
* Flake8 ^6.1.0

## Installation and launch instructions
### Install:

1. Clone the project github using `git clone`
2. Install dependencies by running make build (Poetry is required)
After installing file ".env" should be created in the root directory of the project. This file must contain environment variables:

SECRET_KEY
DATABASE_URL (Format: {provider}://{user}:{password}@{host}:{port}/{db})
On a deployment these variables should be defined on your service for deploy.

### Dev mode with debug

`make dev`

### Launch web-service

`make start`
