#redis-server is compiled with tcmalloc
#LIB=~/workspace/tcmalloc/bazel-bin/tcmalloc/libtcmalloc.so
SRC_DIR=../../../redis
cd $SRC_DIR
make
cd ~/workspace/tcmalloc/test/redis
cp $SRC_DIR/src/redis-server ./
export LD_LIBRARY_PATH=/home/sun/workspace/tcmalloc/bazel-bin/tcmalloc 
./redis-server
