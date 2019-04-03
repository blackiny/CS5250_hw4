
# coding: utf-8

# In[1]:


from simulator import FCFS_scheduling,RR_scheduling,SJF_scheduling,SRTF_scheduling,read_input,write_output
import sys


# In[3]:


def AnaQforRR(process_list):
    maxtime = 0
    for process in process_list:
        maxtime = max(maxtime, process.burst_time)
    besti = 0
    best_sch = []
    best_ave = sys.maxsize
    for i in range(1,maxtime+1):
        sch, avetime = RR_scheduling(process_list,i)
        if avetime < best_ave :
            best_sch = sch
            besti = i
            best_ave = avetime
    print("Best quantum is %d" %(besti))
    print("Best average time is %.2f" %(best_ave))
    write_output("bestRR.txt",best_sch,best_ave)

def AnaAlphaforSJF(process_list):
    bestalpha = 0
    best_sch = []
    best_ave = sys.maxsize
    for i in range(0,101):
        alpha = float(i) / 100
        sch, avetime = SJF_scheduling(process_list,alpha)
        if avetime < best_ave :
            best_sch = sch
            bestalpha = alpha
            best_ave = avetime
    print("Best Alpha is %d" %(bestalpha))
    print("Best average time is %.2f" %(best_ave))
    write_output("bestSJF.txt",best_sch,best_ave)  


# In[4]:


def main(argv):
    input_file='input.txt'
    process_list = read_input(input_file)
    AnaQforRR(process_list)
    AnaAlphaforSJF(process_list)




if __name__ == '__main__':
    main(sys.argv[1:])

