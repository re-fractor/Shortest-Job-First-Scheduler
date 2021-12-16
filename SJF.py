"""Implementation of a CPU scheduling program using a Shortest Job First in Python3."""


from collections import defaultdict
from typing import DefaultDict, Dict, List, NamedTuple


class Proc(NamedTuple):
    proc_id: int
    arrival_time: int
    burst_time: int


class CompletedProc(NamedTuple):
    proc_id: int
    arrival_time: int
    completion_time: int
    execution_starts: List[int]
    execution_paused: List[int]


procs: List[Proc] = []
idx = 1
while True:
    command = input(
        "Enter 'q' or 'Q' to stop input of processes or 'a' or 'A' to add one : ").capitalize()
    if command == "Q":
        break
    elif command != "A":
        print("No Command Entered!")
        continue
    print("Adding Process...")
    arrival_time = input("Enter Arrival Time : ")
    burst_time = input("Enter Burst Time : ")
    if not (arrival_time.isdigit() and burst_time.isdigit()):
        print("Arrival Time or Burst time is not a digit!")
        continue
    print(
        f"Added Process {idx} to queue, with burst time = {burst_time} and arrival time {arrival_time}")
    procs.append(Proc(idx, int(arrival_time), int(burst_time)))
    idx += 1

print("Sorting Procs by Arrival Time and Secondarily by Burst time (Not Changing Their IDs, burst time, etc.,)")
procs.sort(key=lambda x: (x.arrival_time, x.burst_time))
procs_copy = procs.copy()
print('Currently Registered Processes : ')
for proc in procs:
    print('\t', proc)
completed_procs: List[CompletedProc] = []
last_end = procs[0].arrival_time
switch = True
mutable_queue = [
    proc for proc in procs.copy() if proc.arrival_time <= last_end]
# print("Current Queue[", last_end, "] : ", mutable_queue)
# pop the first element in a queue, reduce burst time by 1, put it back in the queue, sort the queue repeat until a process reaches burst_time == 0, then put it in completed procs
exec_starts: DefaultDict[int, List[int]] = defaultdict(list)
pauses: DefaultDict[int, List[int]] = defaultdict(list)
last_executing_proc = mutable_queue[0]
executing_for = 0
while switch:
    new_procs: List[Proc] = []
    currently_executing = mutable_queue.pop(0)
    if (
        exec_starts[last_executing_proc.proc_id]
        and last_executing_proc.proc_id != currently_executing.proc_id
        and last_executing_proc.burst_time != 1
    ):
        # print(f"PAUSING:[{last_end}]", last_executing_proc)
        pauses[last_executing_proc.proc_id].append(last_end)
    if (
        exec_starts[currently_executing.proc_id]
        and last_executing_proc.proc_id != currently_executing.proc_id
        or not exec_starts[currently_executing.proc_id]
    ):
        # print("STARTING:", currently_executing)
        exec_starts[currently_executing.proc_id].append(last_end)

        # print("Currently Executing", currently_executing)
    if currently_executing.burst_time == 1:
        to_remove = list(filter(lambda x: x.proc_id ==
                         currently_executing.proc_id, procs_copy))[0]
        procs_copy.remove(to_remove)
        completed_proc = CompletedProc(
            currently_executing.proc_id, currently_executing.arrival_time,
            last_end+1,
            exec_starts[currently_executing.proc_id],
            pauses[currently_executing.proc_id])
        completed_procs.append(completed_proc)
        # print("Completed Executing Process",
        #       completed_proc)
    if currently_executing.burst_time > 1:
        new_proc = Proc(currently_executing.proc_id,
                        currently_executing.arrival_time,
                        currently_executing.burst_time-1)
        new_procs.append(new_proc)
    new_procs += mutable_queue
    for proc in procs_copy:
        if proc.arrival_time <= last_end+1 and not list(
                filter(lambda x: x.proc_id == proc.proc_id, completed_procs)) and not list(filter(lambda x: x.proc_id == proc.proc_id, new_procs)):
            new_procs.append(proc)

    new_procs.sort(key=lambda x: x.burst_time)
    mutable_queue = new_procs
    # print("Current Queue[", last_end+1, "] : ", mutable_queue)
    if not new_procs:
        print("All Processes Completed Executing!")
        switch = False
        continue
    last_executing_proc = currently_executing
    last_end += 1
print(f"All Processes Completed in {last_end} seconds!")
# print(pauses)
print("Order of Completion :")
for proc in completed_procs:
    print("\t", proc)
