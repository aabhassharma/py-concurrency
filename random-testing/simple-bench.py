import os
import time
import threading
import multiprocessing

NUM_WORKERS = 5

def lets_sleep():
    print "PID: {}\nProcess Name: {}\nThread Name: {}".format(
        os.getpid(),
        multiprocessing.current_process().name,
        threading.current_thread().name
    )
    time.sleep(1)


def process():
    print ("PID: {}\nProcess Name: {}\nThread Name: {}".format(
        os.getpid(),
        multiprocessing.current_process().name,
        threading.current_thread().name
    ))
    x = 0
    while x < 10000:
        x += 1


start_time = time.time()
for _ in range(NUM_WORKERS):
    lets_sleep()
end_time = time.time()
print "Total time for serial runs: {}".format(end_time - start_time)

start_time = time.time()
threads = [threading.Thread(target=lets_sleep) for _ in range(NUM_WORKERS)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]
end_time = time.time()
print "Total time for threaded runs: {}".format(end_time - start_time)

start_time = time.time()
processes = [multiprocessing.Process(target=lets_sleep) for _ in range(NUM_WORKERS)]
[process.start() for process in processes]
[process.join() for process in processes]
end_time = time.time()
print "Total time for multiprocessing runs: {}".format(end_time - start_time)
