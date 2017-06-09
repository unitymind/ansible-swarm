#!/bin/bash -uxe

cd /home/core

cp opt/Anaconda2-4.4.0-Linux-x86_64.sh ./Anaconda2-4.4.0-Linux-x86_64.sh
bash ./Anaconda2-4.4.0-Linux-x86_64.sh -b
touch .bootstrapped
