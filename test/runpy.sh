#!/bin/sh
# build first
bazel build //tcmalloc:libtcmalloc.so
if [ $? -eq 1 ]; then
  exit 1
fi
cd $1
LIB="../../bazel-bin/tcmalloc/libtcmalloc.so"
../clean.sh
pyFile=$(find . -name "main.py")
if [ -z "$pyFile" ]; then
  pyFile=$(find . -name "*.py")
fi
LD_PRELOAD=$LIB python3 $pyFile 2>&1 | tee process.log
python3 ../draw.py
