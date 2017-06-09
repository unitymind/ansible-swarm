#!/bin/bash -uxe

VERSION=2.7.13.2715
PACKAGE=ActivePython-${VERSION}-linux-x86_64-glibc-2.12-402695

# make directory
mkdir -p /opt/bin
cd /opt

# tar -xzf ${PACKAGE}.tar.gz > /dev/null

mv ${PACKAGE} apy && cd apy && ./install.sh -I /opt/python/

ln -sf /opt/python/bin/easy_install /opt/bin/easy_install
ln -sf /opt/python/bin/pip /opt/bin/pip
ln -sf /opt/python/bin/python /opt/bin/python
ln -sf /opt/python/bin/python /opt/bin/python2
ln -sf /opt/python/bin/virtualenv /opt/bin/virtualenv
