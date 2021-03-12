#redis-server is compiled with tcmalloc
#LIB=~/workspace/tcmalloc/bazel-bin/tcmalloc/libtcmalloc.so
SRC_DIR=../../../redis
cd $SRC_DIR
make
cd ~/workspace/tcmalloc/test/redis
cp $SRC_DIR/src/redis-server ./
export LD_LIBRARY_PATH=/home/sun/workspace/tcmalloc/bazel-bin/tcmalloc 
./redis-server&
PID=$!
#echo -e "\033[31m$PID\033[0m"
sleep 0.01
./redis-benchmark -c 1000 -d 2000 -r 2000 -n 10000
./redis-benchmark -c 100 -n 20000
sleep 62
kill -9 $PID
rm dump.rdb
