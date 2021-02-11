import sys

# Variables
import os

USR=os.environ['USR']
PWD=os.environ['PWD']

# watchdog
delete_after_work=True

# Logging
import logging

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

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)


