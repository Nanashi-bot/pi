from mpmath import mp
from multiprocessing import Process, Value, Lock
import ctypes

def compute_pi_block(start, block_size, dps):
    mp.dps = dps
    pi_str = str(mp.pi)[2:]  # remove '3.'
    return pi_str[start:start + block_size]

def search_in_block(start, block_size, target, result, lock, precision_margin=20):
    dps = start + block_size + precision_margin
    block = compute_pi_block(start, block_size + len(target) - 1, dps)
    idx = block.find(target)
    if idx != -1:
        with lock:
            print(f"Match found at absolute index {start + idx} in block {start}:{start + block_size + len(target) - 1}")
            if result.value == -1 or start + idx < result.value:
                result.value = start + idx
            else:
                print(f"No match in block {start}:{start + block_size + len(target) - 1}")


def multithreaded_pi_search(target, num_processes=4, block_size=100000):
    result = Value(ctypes.c_longlong, -1)
    lock = Lock()
    processes = []
    for i in range(num_processes):
        start = i * block_size
        p = Process(target=search_in_block, args=(start, block_size, target, result, lock))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    return result.value

print(multithreaded_pi_search("1245"))
