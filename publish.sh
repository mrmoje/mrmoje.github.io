#!/usr/bin/env bash
#
rm output/* -rf
make publish
ghp-import -p -b master -m "$1" output
