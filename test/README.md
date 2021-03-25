# README
Tensorflow tests come from https://github.com/whybfq/tensorflow2.git and https://github.com/YunYang1994/TensorFlow2.0-Examples

Tests have been modified a little.

## Plateform
Linux System

Python3

Tensorflow_gpu2

need compiler that supports C++17

## Some files
1. overall stats of local_hugepages 
   1. In **local_huge_page.data**, each line is a record, which consists of two number. The former one is bytes of local unique hugepages(MiB), and the next one is bytes in cpu cache(MiB).
   2. **local_huge_page.png** is the picture of data above.
2. stats of local rate in cpu cache
   1. In **local_rate.data**, four lines a record, each record contains cpu id, and allocate and deallocate times in this cpu.
   2. **local_rate.png** is the picture of data above. Value of y is allocate/deallocate, y=0 means allocate or deallocate times equals 0.
3. **outputxxx.txt** contains detail stats of hugepages in cpu cache.

## To test tcmalloc
./run.sh test_dirctory

## Something important

1. firefox:
   1.  build with --disable-jemalloc(replace malloc) and --disable-sandbox(sandbox will prevent write file). 
   2. In **about:config** page, set browser.tabs.remote.autostart = false so that firefox run single-process mode. Otherwise in multi-process mode, multiple tcmalloc instances will be created.(and dom.ipc.processcount=0, but still a socket process)

2. about sort central freelist:
   1. cpu on, then 0.07-0.1 coverage at last(200 hps); cpu off, then transfer off, 0.27-0.3 coverage
