#!/bin/sh
# build first
bazel build //tcmalloc:libtcmalloc.so --copt -DTCMALLOC_TRANSFER_OFF --copt -DTCMALLOC_TRACK_SPAN_LIFE
# build fail
if [ $? -eq 1 ]; then
  exit 1
fi
cd $1
# clean
../clean.sh
# check directory
needed=$(ls singletest.sh)
if [ $? -ne 0 ]; then
  echo "wrong test directory"
  exit 1
fi
# run
./singletest.sh
# draw picture
# python3 ../draw.py
