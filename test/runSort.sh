#!/bin/sh
# build first
bazel build //tcmalloc:libtcmalloc.so --copt -DTCMALLOC_LOW_ADDRESS_FIRST --copt -DTCMALLOC_TRANSFER_OFF \
  --copt -DTCMALLOC_TRACK_SPAN_LIFE
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
