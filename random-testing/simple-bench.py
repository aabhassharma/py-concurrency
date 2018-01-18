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


def process_things():
    print ("PID: {}\nProcess Name: {}\nThread Name: {}".format(
        os.getpid(),
        multiprocessing.current_process().name,
        threading.current_thread().name
    ))
    x = 0
    while x < 1000000:
        x += 1


start_time = time.time()
for _ in range(NUM_WORKERS):
    lets_sleep()
end_time = time.time()
print "Total time for serial runs: {}\n".format(end_time - start_time)

start_time = time.time()
threads = [threading.Thread(target=lets_sleep) for _ in range(NUM_WORKERS)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]
end_time = time.time()
print "Total time for threaded runs: {}\n".format(end_time - start_time)

start_time = time.time()
processes = [multiprocessing.Process(target=lets_sleep) for _ in range(NUM_WORKERS)]
[process.start() for process in processes]
[process.join() for process in processes]
end_time = time.time()
print "Total time for multiprocessing runs: {}\n".format(end_time - start_time)

print "\nStarting process_things task\n"
start_time = time.time()
for _ in range(NUM_WORKERS):
    process_things()
end_time = time.time()
print "Total time for serial runs: {}\n".format(end_time - start_time)

start_time = time.time()
threads = [threading.Thread(target=process_things) for _ in range(NUM_WORKERS)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]
end_time = time.time()
print "Total time for threaded runs: {}\n".format(end_time - start_time)

start_time = time.time()
processes = [multiprocessing.Process(target=process_things) for _ in range(NUM_WORKERS)]
[process.start() for process in processes]
[process.join() for process in processes]
end_time = time.time()
print "Total time for multiprocessing runs: {}\n".format(end_time - start_time)
