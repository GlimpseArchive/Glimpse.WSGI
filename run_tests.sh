#! /usr/bin/env bash

nosetests -m="^$" unit_tests/*tests.py integration_tests/*tests.py
