#!/bin/bash
dropdb trivia_test
createdb trivia_test
psql trivia_test -f trivia.psql
clear
python -m unittest -v test_flaskr.py
dropdb trivia_test

