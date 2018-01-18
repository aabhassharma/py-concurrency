import time
import logging
import requests
 
 
class WebsiteDownException(Exception):
    pass
 
 
def ping_website(address, timeout=20):
    try:
        response = requests.head(address, timeout=timeout)
        if response.status_code >= 400:
            logging.warning("Website %s returned status_code=%s" % (address, response.status_code))
            raise WebsiteDownException()
    except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()
         
 
def notify_owner(address):
    logging.info("Notifying the owner of %s website" % address)
    time.sleep(0.5)
     
 
def check_website(address):
    try:
        ping_website(address)
    except WebsiteDownException:
        notify_owner(address)