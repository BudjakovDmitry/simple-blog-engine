#!/usr/bin/env bash

-set -Eeuo pipefail

PYTHON_VERSION=3.14.3
PYTHON_MAJOR_VERSION="${PYTHON_VERSION%.*}"
PYTHON_DIR=/opt/python/$PYTHON_VERSION


echo Update requirements
apt update

echo Upgrade requirements
apt -y upgrade

echo Install building tools
apt install -y build-essential gcc make

echo Install pre-requirements
apt install -y \
    wget \
    unzip \
    zlib1g-dev \
    gdb \
    lzma \
    lcov \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    libreadline-dev \
    libncurses5-dev \
    uuid-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    tk-dev \
    libzstd-dev \
    inetutils-inetd

echo Donload Python
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz
tar xvf Python-$PYTHON_VERSION.tar.xz
cd Python-$PYTHON_VERSION

echo Build Python
mkdir -p $PYTHON_DIR
./configure --enable-optimizations --prefix=$PYTHON_DIR
make -j$(nproc)
make altinstall
rm -r Python-$PYTHON_VERSION

echo Add symlink to Python executable
ln -s $PYTHON_DIR/bin/python$PYTHON_MAJOR_VERSION /usr/local/bin/python

echo Update pip
python -m pip install -U pip

echo Download source code
wget https://github.com/BudjakovDmitry/simple-blog/archive/refs/heads/main.zip
unzip main.zip /opt/dmitbud
rm main.zip
cd /opt/dmitbud/simple-blog-main

echo Instal project requirements
python -m pip install -r requirements.txt

export PGSERVICEFILE=$(pwd)/secrets/pg_service.conf

echo Appy migrations
python manage.py migrate
