LIB=~/workspace/tcmalloc/bazel-bin/tcmalloc/libtcmalloc.so
LD_PRELOAD=$LIB python3 main.py 2>&1 | tee process.log
