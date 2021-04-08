#redis-server is compiled with tcmalloc
SRC_DIR=../../../redis
REDIS_DIR=$(pwd)
cd $SRC_DIR
make
cd $REDIS_DIR
cp $SRC_DIR/src/redis-server ./
export LD_LIBRARY_PATH=/home/sun/workspace/tcmalloc/bazel-bin/tcmalloc 
./redis-server&
PID=$!
#echo -e "\033[31m$PID\033[0m"
sleep 0.1
./redis-benchmark -c 1000 -d 2000 -r 2000 -n 5000>/dev/null
./redis-benchmark -c 100 -n 50000
sleep 12
kill -9 $PID
rm dump.rdb
