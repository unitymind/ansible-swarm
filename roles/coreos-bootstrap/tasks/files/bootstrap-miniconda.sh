#!/bin/bash -uxe

cd /home/core

wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh -b
rm Miniconda2-latest-Linux-x86_64.sh
touch .bootstrapped
