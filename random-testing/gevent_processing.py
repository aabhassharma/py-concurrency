import time
from gevent.pool import Pool
from gevent import monkey
from websites import WEBSITE_LIST
from utils import check_website

NUM_WORKERS = 4

monkey.patch_socket()

START_TIME = time.time()

pool = Pool(NUM_WORKERS)
for address in WEBSITE_LIST:
    pool.spawn(check_website, address)
pool.join()

END_TIME = time.time()  

print "Time for Async Futures Check: %ssecs" % (END_TIME - START_TIME)
