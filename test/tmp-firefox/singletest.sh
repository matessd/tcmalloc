TC_LIB=~/workspace/tcmalloc/bazel-bin/tcmalloc/libtcmalloc.so
OBJ_DIR=/home/sun/workspace/mozilla/obj-x86_64-pc-linux-gnu/dist/bin
#export MOZ_DISABLE_CONTENT_SANDBOX=1
LD_PRELOAD=$TC_LIB $OBJ_DIR/firefox -no-remote -profile ./profile
