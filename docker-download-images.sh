#!/bin/sh

. ./configure.sh

bash scripts/download-images.sh -o images
bash scripts/load-images.sh -l images
