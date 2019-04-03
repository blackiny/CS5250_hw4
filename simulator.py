
import sys

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.remain_time = burst_time
        self.esti_time = 0.0
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))
    def reset_remain(self):
        self.remain_time = self.burst_time
        
def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    l = len(process_list)
    current_time = 0
    waiting_time = 0
    pos = 0
    ready_q = []
    process_q = []
    schedule = []
    finish_num = 0
    while finish_num < l :
        if not ready_q:
            ready_q.append(pos)
            pos = pos + 1
        process_q = ready_q.copy()
        ready_q = []
        for process_id in process_q:
            process = process_list[process_id]
            if current_time < process.arrive_time :
                current_time = process.arrive_time
            schedule.append((current_time, process.id))
            consume_time = min(process.remain_time,time_quantum)
            current_time = current_time + consume_time
            process.remain_time = process.remain_time - consume_time
            # put process arriving in this quantum in the ready_queue
            if pos < l :
                next_process = process_list[pos]
                while current_time >= next_process.arrive_time:
                    ready_q.append(pos)
                    pos = pos + 1
                    if pos >= l:
                        break
                    next_process = process_list[pos]
            # if finished, add 1 to finish_num; else put it into ready_queue
            if process.remain_time == 0:
                finish_num = finish_num + 1
                waiting_time = waiting_time + current_time - process.arrive_time - process.burst_time
            else :
                ready_q.append(process_id)
    # reset the remaining time for each process
    for process in process_list:
        process.reset_remain()
    average_waiting_time = waiting_time/float(l)
    
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    l = len(process_list)
    process_q = []
    current_time = 0
    waiting_time = 0
    finish_num = 0
    pos = 0
    schedule = []
    while finish_num < l:
        if not process_q:
            process_q.append(pos)
            pos = pos + 1
        # the process being executed
        curr_id = process_q.pop(0)
        process = process_list[curr_id]
        if current_time < process.arrive_time :
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        # end_time: the stop time if no process preempt in
        # stop_time: the real stop time
        end_time = current_time + process.remain_time
        stop_time = end_time
        if pos < l:
            next_process = process_list[pos]
            while (next_process.arrive_time <= end_time):
                process_q.append(pos)
                # means that a process can preempt in
                if next_process.remain_time < process.remain_time - next_process.arrive_time + current_time:
                    stop_time = next_process.arrive_time
                    break
                pos = pos + 1
                if pos >= l:
                    break
                next_process = process_list[pos]
        if stop_time != end_time :
            pos = pos + 1
        process.remain_time = process.remain_time - stop_time + current_time
        current_time = stop_time
        if process.remain_time == 0:
            waiting_time = waiting_time + current_time - process.arrive_time - process.burst_time
            finish_num += 1
        # if the process being preempted in, put it back into waiting queue
        else :
            process_q.append(curr_id)
        # sort the queue according to remaining time 
        process_q = sorted(process_q, key=lambda pid: process_list[pid].remain_time)
    # reset remaining time for each process
    for process in process_list :
        process.reset_remain()
    average_waiting_time = waiting_time/float(l)  
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    # assume that id is 0-n continuously!!!
    id_set = set()
    for process in process_list:
        id_set.add(process.id)
    id_list = list(id_set)
    id_list = sorted(id_list)
    id_num = len(id_list)
    # initial guess is 5 for all pids
    guess_time = [5] * id_num
    real_time = [-1] * id_num
    l = len(process_list)
    process_q = []
    current_time = 0
    waiting_time = 0
    finish_num = 0
    pos = 0
    schedule = []
    while finish_num < l:
        if not process_q:
            process_q.append(pos)
            toput_process = process_list[pos]
            if real_time[toput_process.id] != -1:
                toput_process.esti_time = alpha * real_time[toput_process.id] + (1-alpha) * guess_time[toput_process.id]
            else :
                toput_process.esti_time = guess_time[toput_process.id]
            pos += 1
        curr_id = process_q.pop(0)
        process = process_list[curr_id]
        if current_time < process.arrive_time:
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        end_time = current_time + process.burst_time
        if pos <l:
            next_process = process_list[pos]
            while next_process.arrive_time <= end_time:
                process_q.append(pos)
                pos += 1
                if real_time[next_process.id] != -1:
                    next_process.esti_time = alpha * real_time[next_process.id] + (1-alpha) * guess_time[next_process.id]
                else :
                    next_process.esti_time = guess_time[next_process.id]
                if pos >= l:
                    break
                next_process = process_list[pos]
        finish_num += 1
        waiting_time = waiting_time + end_time - process.arrive_time - process.burst_time
        current_time = end_time
        # we update the real_time and esti_time at entry x only when a task with pid as x finished. 
        guess_time[process.id] = process.esti_time
        real_time[process.id] = process.burst_time
        # sort by estimate time
        process_q = sorted(process_q, key=lambda pid: process_list[pid].esti_time)
    
    average_waiting_time = waiting_time/float(l)  
    return schedule, average_waiting_time

def read_input(input_file):
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    input_file = 'input.txt'
    process_list = read_input(input_file)
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    print("The average waiting time of FCFS is %.2f" %(FCFS_avg_waiting_time))
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print("The average waiting time of RR is %.2f" %(RR_avg_waiting_time))
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print("The average waiting time of SRTF is %.2f" %(SRTF_avg_waiting_time))
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )
    print("The average waiting time of SJF is %.2f" %(SJF_avg_waiting_time))

if __name__ == '__main__':
    main(sys.argv[1:])

