#!/bin/bash -uxe

cd $HOME

wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh -b -p /opt
rm Miniconda2-latest-Linux-x86_64.sh
touch .bootstrapped
