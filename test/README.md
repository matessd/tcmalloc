# README
Tensorflow tests come from https://github.com/whybfq/tensorflow2.git and https://github.com/YunYang1994/TensorFlow2.0-Examples

C++ tests comes from  https://github.com/khanhtn1/malloc-benchmarks.

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
run as follows, will auto compile using bazel and generate stats.
### tensorflow test
./runpy.sh tensorflow_test_directory (dir name like ClassificationMLP)

ClassificationMLP, RegressionMLP, Neural_Network_Architecture are tensorflow test

### C/C++ test
./runcxx.sh cxx_test_dirctory (dir name like alloc_test)

alloc_test, larson, rptest are C++ test