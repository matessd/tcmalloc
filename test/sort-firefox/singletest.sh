TC_LIB=../../bazel-bin/tcmalloc/libtcmalloc.so
OBJ_DIR=../../../mozilla/obj-x86_64-pc-linux-gnu/dist/bin
#OBJ_DIR=/home/sun/download/firefox
#export MOZ_FORCE_DISABLE_E10S=86
LD_PRELOAD=$TC_LIB $OBJ_DIR/firefox -no-remote -profile ./profile
#LD_PRELOAD=$TC_LIB $OBJ_DIR/firefox
