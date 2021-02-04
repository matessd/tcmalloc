import matplotlib.pyplot as plt

def draw_local_hp():
  x=0; x_data = []
  y1_data = []#cpu cache memory
  y2_data = []#huge page memory(MiB, compute by number*2)
  with open('local_huge_page.data','r+') as f:
    lines = f.readlines()
    for line in lines:
      y1,y2 = line.strip().split()
      y1_data.append(float(y1))
      y2_data.append(int(y2))
      x_data.append(x)
      x=x+1
    #print(x_data,y1_data,y2_data)
    y_data = [y1/y2 for y1,y2 in zip(y1_data,y2_data)]
    plt.figure(figsize=(20, 10), dpi=80)
    plt.plot(x_data, y_data, label='upper: bytes in cpu cache bytes(MiB)\
      \nlower: bytes of unique hugepages(MiB)')
    plt.xlabel('number of record',size=20)
    plt.ylabel('hugepage coverage of cpu cache',size=20)
    plt.legend(fontsize=15,loc='best')
    for x,y,y1,y2 in zip(x_data,y_data,y1_data,y2_data):
        plt.text(x,y,str(round(y1,2))+'\n'+str(y2),ha='center',va='bottom',fontsize=15)
    plt.title('Partial coverage of huge pages in cpu cache',size=20)
    plt.savefig('local_huge_page.png')
    #plt.show()

def draw_local_rate():
  x=0; x_data = []
  y1_data = [[],[],[],[]]# allocate times
  y2_data = [[],[],[],[]]# deallocate times
  with open('local_rate.data','r+') as f:
    lines = f.readlines()
    for line in lines:
      line_str = line.strip().split()
      cpu_id = int(line_str[0])
      y1_data[cpu_id].append(line_str[1])
      y2_data[cpu_id].append(line_str[2])
      if cpu_id == 0:
        x_data.append(x)
      if cpu_id == 3:
        x=x+1
    #print(x_data,y1_data,y2_data)
    y_data = [[],[],[],[]]
    for cpu_id in range(0,4):
      for y1,y2 in zip(y1_data[cpu_id],y2_data[cpu_id]):
        if float(y2)==0:
          y_data[cpu_id].append(0)
          continue
        y_data[cpu_id].append(float(y1)/float(y2))
    plt.figure(figsize=(20, 10), dpi=80)
    for cpu_id in range(0,4):
      plt.plot(x_data, y_data[cpu_id], label='cpu'+str(cpu_id))
    plt.xlabel('number of record',size=20)
    plt.ylabel('rate of allocate/deallocate',size=20)
    plt.legend(fontsize=15,loc='best')
    plt.title('Local rate of allocate/deallocate during interval',size=20)
    plt.savefig('local_rate.png')
    #plt.show()

if __name__ == '__main__':
  draw_local_hp()
  draw_local_rate()