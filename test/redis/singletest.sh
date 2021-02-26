LIB=~/workspace/tcmalloc/bazel-bin/tcmalloc/libtcmalloc.so 
LD_PRELOAD=$LIB ./redis-benchmark -c 10000 -l
