#!/bin/sh
# build first
bazel build //tcmalloc:libtcmalloc.so --strip=never --copt -g
if [ $? -eq 1 ]; then
  exit 1
fi
cd $1
../clean.sh
needed=$(ls singletest.sh)
if [ $? -ne 0 ]; then
  echo "wrong test directory"
  exit 1
fi
./singletest.sh
