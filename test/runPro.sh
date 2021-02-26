#!/bin/sh
# build first
bazel build //tcmalloc:libtcmalloc.so
if [ $? -eq 1 ]; then
  exit 1
fi
cd $1
../clean.sh
needed=$(ls a.out redis-benchmark)
if [ $? -ne 0 ]; then
  echo "error c++ test directory"
  exit 1
fi
./singletest.sh
python3 ../draw.py
