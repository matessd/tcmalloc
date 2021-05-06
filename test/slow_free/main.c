#include<stdio.h>
#include<iostream>
#include <thread>
#include <chrono>
#include<stdlib.h>
#include<assert.h>
#include<cstring>

#define TEST_MAX_CLASS_NUM 20
#define TEST_CLASS_COUNT_LIMIT 5000
// each class has at most 100 MiB space
#define TEST_CLASS_MEM_LIMIT 100<<20
void *g_ptr[TEST_MAX_CLASS_NUM][TEST_CLASS_COUNT_LIMIT];
int g_size[TEST_MAX_CLASS_NUM];
int g_tot_mem;
#define class_to_mem(i) ( 2<<i )

int Class_Malloc(int class_num, int batch_cnt){
  int tot_mem = 0;
  assert(g_size[class_num]+batch_cnt<=TEST_CLASS_COUNT_LIMIT);
  for(int i=0; i<batch_cnt; i++){
    int mem = rand()%class_to_mem(class_num)+1;
    char *ptr = (char *)malloc(mem);
    memset(ptr, '\0', mem);
    g_ptr[class_num][g_size[class_num]++] = (void *)ptr;
    tot_mem += mem;
  }
  return tot_mem;
}

int Class_Free(int class_num, int batch_cnt){
  int i = class_num;
  while(g_size[i]>0 && batch_cnt>0){
    //int j = rand()%g_size[i];
    int j = 0;
    free(g_ptr[i][j]);
    g_ptr[i][j] = g_ptr[i][--g_size[i]];
    batch_cnt--;

    void *tmp = g_ptr[i][0];
    for(j=0; j<g_size[i]-1; j++){
        g_ptr[i][j] = g_ptr[i][j+1];
    }
    g_ptr[i][g_size[i]-1] = tmp;
  }
  return 0;
}

int main(){
  double MiB = 1<<20;
  // fill
  g_tot_mem = 0;
  int max_size[TEST_MAX_CLASS_NUM];
  srand(0);
  for(int i=0; i<TEST_MAX_CLASS_NUM; i++){
    g_size[i] = 0;
    int cnt = 0, mem = 0;
    while(cnt<TEST_CLASS_COUNT_LIMIT && mem<TEST_CLASS_MEM_LIMIT){
      mem += Class_Malloc(i, 1);
      cnt++;
    }
    g_tot_mem += mem;
    max_size[i] = g_size[i];
    printf("%d %lf\n", max_size[i], g_tot_mem/MiB);
  }
  bool malloc_flg[TEST_MAX_CLASS_NUM];
  for(int i = 0; i<TEST_MAX_CLASS_NUM; i++){
    malloc_flg[i] = false;
  }
  while(true){
    for(int i=0; i<TEST_MAX_CLASS_NUM; i++){
      // switch to free mode
      /*if(malloc_flg[i] == true && g_size[i]>max_size[i]/2){
        malloc_flg[i] = false;
      }*/
      // swtich to alloc mode
      if(malloc_flg[i] == false && g_size[i]<max_size[i]/2){
        malloc_flg[i] = true;
      }
      // alloc or free
      if(malloc_flg[i]){
        Class_Malloc(i, max_size[i]/10);
        malloc_flg[i] = false;
      }else{
        Class_Free(i, max_size[i]/20);
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
  }
  return 0;
}