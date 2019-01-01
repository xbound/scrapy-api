#!/bin/bash

gunicorn --log-level=debug \
        --workers 2 --name scrapy_api \
        -b 0.0.0.0:8000 \
        --reload scrapy_api.wsgi:app \
        --timeout 10000