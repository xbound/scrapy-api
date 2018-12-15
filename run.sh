#!/bin/bash

gunicorn --log-level=debug \
        --workers 4 --name scrapy_api \
        -b 0.0.0.0:8000 \
        --reload scrapy_api.wsgi:app \
        -t 100000