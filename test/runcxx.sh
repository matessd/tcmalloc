#!/bin/sh
# build first
bazel build //tcmalloc:libtcmalloc.so
if [ $? -eq 1 ]; then
  exit 1
fi
cd $1
../clean.sh
needed=$(ls WORKSPACE)
if [ $? -ne 0 ]; then
  echo "error c++ test directory"
  exit 1
fi
dir=$1
output=${dir%/}
bazel build //example:$output
cp -f bazel-bin/example/$output a.out
./singletest.sh
python3 ../draw.py
