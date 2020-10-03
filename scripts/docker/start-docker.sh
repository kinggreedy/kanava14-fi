#!/usr/bin/env bash

alembic -c development.ini upgrade head
pserve development.ini --reload
