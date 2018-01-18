import time
from Queue import Queue
from threading import Thread
from websites import WEBSITE_LIST
from utils import check_website
 
NUM_WORKERS = 4
task_queue = Queue()
 
def worker():
    while True:
        address = task_queue.get()
        check_website(address)
        task_queue.task_done()
 
start_time = time.time()
         
# Create the worker threads
threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
 
# Add the websites to the task queue
[task_queue.put(item) for item in WEBSITE_LIST]
 
# Start all the workers
[thread.start() for thread in threads]
 
# Wait for all the tasks in the queue to be processed
task_queue.join()
 
         
end_time = time.time()        
 
print("Time for Threaded Checks: %ssecs" % (end_time - start_time))