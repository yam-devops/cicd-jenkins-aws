import logging
from datetime import datetime

current_time = datetime.now() 

logging.basicConfig(filename=f'web_logs/record-{current_time.strftime("%d-%m-%Y-%H-%M-%S")}.log',
							level=logging.DEBUG,
							format="%(asctime)s %(levelname)s %(message)s")
