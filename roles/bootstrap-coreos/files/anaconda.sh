#!/bin/bash -uxe

cd $HOME

wget https://repo.continuum.io/archive/Anaconda2-4.4.0-Linux-x86_64.sh
bash Anaconda2-4.4.0-Linux-x86_64.sh -b
rm Anaconda2-4.4.0-Linux-x86_64.sh
touch .bootstrapped
