#!/bin/bash

cd src
gunicorn app.wsgi
