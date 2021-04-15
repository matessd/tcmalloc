# README
Tensorflow tests come from https://github.com/whybfq/tensorflow2.git and https://github.com/YunYang1994/TensorFlow2.0-Examples

Tests have been modified a little.

## Plateform
Linux System(supports restartable_sequence and huge page)

Python3

Tensorflow_gpu2(for tensorflow test, seems this test needless)

GCC version that supports C++17

bazel

## How to build and test somes tests

1. Directory structure like this:

   ---workspace

   ​           |-------- tcmalloc(in my github, only this part)

   ​                              |-----------test(main directory for running tests)

   ​           |-------- redis(src code of redis)

   ​           |-------- mozilla
   
   ​           |-------- other src_directory that too large 

2. How to build and run redis test:

   1. get source code from github.

   2. in worksapce/redis/src/Makefile, find the word "FINAL_LDFLAGS", then add two lines there:

      1. ```
         FINAL_LDFLAGS+= -L../../tcmalloc/bazel-bin/tcmalloc
         FINAL_LIBS+= -ltcmalloc
         ```

      2. Then come back to tcmalloc/test, use run.sh to build and run.

3. How to build and run firefox test:

   1. using hg to pull source code of firefox, rename as mozilla.

   2. Then create file "mozconfig", add three lines:

      1. ```
         ac_add_options --with-ccache=sccache
         ac_add_options --disable-jemalloc
         ac_add_options --disable-sandbox
         ```

      2. sccache for accelerating build.

      3. disable jemalloc for replacing tcmalloc, otherwise tcmalloc can't work.

      4. disable sanbox, otherwise have no access to create output file.

   3. The first time that run firefox, create "profile" directory in /tcmalloc/test/firefox/ 

   4. In **about:config** page, set **browser.tabs.remote.autostart = false** to decrease processes amount. (multi-process mode can't be off in newest version, "export MOZ_FORCE_DISABLE_E10S" also can't work). When running for a while, there should be only an extra socket process.

4. ./run.sh test_dirctory

## Some stats files
1. overall stats of local_hugepages 
   1. In **local_huge_page.data**, each line is a record, which consists of two number. The former one is bytes of local unique hugepages(MiB), and the next one is bytes in cpu cache(MiB).
   2. **local_huge_page.png** is the picture of data above.
2. stats of local rate in cpu cache
   1. In **local_rate.data**, four lines a record, each record contains cpu id, and allocate and deallocate times in this cpu.
   2. **local_rate.png** is the picture of data above. Value of y is allocate/deallocate, y=0 means allocate or deallocate times equals 0.
3. **outputxxx.txt** contains detail stats of hugepages in cpu cache.

## Something important

1. about sort central freelist:
