export LD_LIBRARY_PATH=../../bazel-bin/tcmalloc
g++ main.c -o a.out
LD_PRELOAD=../../bazel-bin/tcmalloc/libtcmalloc.so ./a.out
