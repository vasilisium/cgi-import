import sys
import os
import logging

# Variables
USR=os.environ['USR']
PWD=os.environ['PWD']
url = 'https://test2.credithistory.com.ua/DataPump/Service.asmx'

# watchdog
delete_after_work=True

# Logging
logging.basicConfig(
  filename='import.log',
  level=logging.INFO,
  format='%(asctime)s - %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'
)

# logging.basicConfig(
#   filename='import.errors.log',
#   level=logging.ERROR,
#   format='%(asctime)s - %(message)s',
#   datefmt='%Y-%m-%d %H:%M:%S'
# )

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))


