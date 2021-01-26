#!/bin/bash

cd src
gunicorn blog.wsgi
