#!/bin/bash
gunicorn main:app --workers 1 --bind 0.0.0.0:$PORT
