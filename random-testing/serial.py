import time
from websites import WEBSITE_LIST
from utils import check_website

start_time = time.time()

for address in WEBSITE_LIST:
    check_website(address)     
end_time = time.time()    

print("Time for Serial Checking: %ssecs" % (end_time - start_time))