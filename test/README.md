# README
Tensorflow tests come from https://github.com/whybfq/tensorflow2.git and https://github.com/YunYang1994/TensorFlow2.0-Examples

Tests have been modified a little.

## Plateform and PreCondition
Linux System(should support **restartable_sequence** and **huge page**)

Python3

Tensorflow2(for tensorflow test. Seems this test useless now, because its hugepage coverage is high)

GCC version that supports C++17

bazel

## How to build and test somes tests

1. Directory structure should look like this:

   ---workspace

   ​           |-------- tcmalloc(only this part in my github)

   ​                              |---------test(main directory for running tests)

   ​                                      |----------redis(directory that stores test output of redis with original tcmalloc)

   ​                                      |----------sort-redis(directory that stores test output of redis with modified tcmalloc)

   ​           |-------- redis(src code of redis)

   ​           |-------- mozilla(src code of firefox)

   ​           |-------- other src_directory

2. How to build and run redis test:

   1. Get source code from github.(https://github.com/redis/redis)

   2. ```
      cd workspace/redis/src
      make
      cp redis-benchmark workspace/tcmalloc/test/redis
      cp redis-benchmark workspace/tcmalloc/test/sort-redis
      ```

      These command will build original version of redis and copy original redis-benchmark to test directory.

   3. In worksapce/redis/src/Makefile, find where "FINAL_LDFLAGS" defines, then add two lines here:

      1. ```
         FINAL_LDFLAGS+= -L../../tcmalloc/bazel-bin/tcmalloc
         FINAL_LIBS+= -ltcmalloc
         ```

      2. Then come to tcmalloc/test, 

         ```
         ./run.sh redis
         (Or ./runSort.sh sort-redis)
         (it will build and test tcmalloc version redis-server)
         ```

3. How to build and run firefox test(https://firefox-source-docs.mozilla.org/contributing/coantribution_quickref.html):

   1. Use hg to pull source code of firefox, rename directory as mozilla.

   2. Then create file "mozconfig" in src code directory, add three lines:

      1. ```
         ac_add_options --with-ccache=sccache
         ac_add_options --disable-jemalloc
         ac_add_options --disable-sandbox
         ```

      2. sccache for accelerating build.

      3. disable jemalloc for replacing tcmalloc, otherwise tcmalloc can't work.

      4. disable sanbox, otherwise program will have no access to create output file.

   3. Then build firefox according to official doc.

   4. Create "profile" directory in tcmalloc/test/firefox/ and tcmalloc/test/sort-firefox/

   5. In tcmalloc/test/

      ```
      ./run.sh firefox
      (Or ./runSort.sh sort-firefox) 
      (tcmalloc will be replaced by LD_PRELOAD, command is in tcmalloc/test/firefox/singletest.sh)
   ```
   
   6. At the first time for running firefox:
   
      1. open **about:config** page
      2. search "autostart", set all to **false** 
      3. set "dom.ipc.processCount" to **0**
      4. It is because multi-process mode can't be off in newest firefox version ("export MOZ_FORCE_DISABLE_E10S" also can't work). These measures can decrease the number of processes.

## Description for some files and functions
1. **outputxxx.txt** contains detail stats of test.
   1. For redis, I can just use atexit() to only one output stats before program ends.
   2. But for firefox, It seems the root(parent) process will not call the function registered by atexit(), so need to output every second.
   3. So in redis test, comment the use of function DumpAllStats() in BackgroundTask(). In firefox, use it to output every second.
2. **run.sh** and **runSort.sh** will clean last output, rebuild tcmalloc, and run test.
3. **debug.sh** can build and tcmalloc with gdb information and run it.
4. **draw.py** was used to draw picture of local cpu stats, now I comment this part code.
5. The top level of modified tcmalloc is in tcmalloc.cc, and see the function "BackgroundTask". It keeps loop at background, and will record stats and do some measures per second.

## Other important
