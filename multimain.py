from mpmath import mp
from multiprocessing import Process, Value, Lock, Event
import ctypes

def compute_pi_block(start, block_size, dps):
    mp.dps = dps
    pi_str = str(mp.pi)[2:]  # remove '3.'
    return pi_str[start:start + block_size]

def search_in_block(start, block_size, target, result, lock, exit_event, precision_margin=20):
    if exit_event.is_set():
        return
    dps = start + block_size + precision_margin
    block = compute_pi_block(start, block_size + len(target) - 1, dps)
    if exit_event.is_set():
        return
    idx = block.find(target)
    if idx != -1:
        with lock:
            abs_index = start + idx
            print(f"Match found at index {abs_index} in block:")
            if result.value == -1 or abs_index < result.value:
                result.value = abs_index
                exit_event.set()

def multithreaded_pi_search(target, num_processes=4, block_size=100000):
    result = Value(ctypes.c_longlong, -1)
    lock = Lock()
    exit_event = Event()
    processes = []
    for i in range(num_processes):
        start = i * block_size
        p = Process(target=search_in_block, args=(start, block_size, target, result, lock, exit_event))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    return result.value

print(multithreaded_pi_search("12455"))
