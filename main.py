import time
from crawler import check_content, url_generator
import os
from pathlib import Path

start = time.time()
# Open txt with number of lo and creates and output file with all the urls.
# This is important because some of the URL's need to be changed by hand.
file_lo_txt = "lo.txt"
output_url_file = "url_lo.txt"
# Need to generate an exception list in the form lo_id -> url
exceptions = [
    ("ca3", "https://www.rcophth.ac.uk/learningoutcomes/12658/"),
]
url_array = url_generator(file_lo_txt, output_url_file, exceptions)

# begin of loop to access all the learning outcomes.
print(f"This crawler will access {len(url_array)} learning outcomes url's. Good luck!")

# Todo need to loop this, still just an example.
URL = "https://www.rcophth.ac.uk/learningoutcomes/hpdp4/"

pwd = Path(os.getcwd())
htm_path = pwd/"html_tables"
print(f"current working directory is {pwd}")
print(f"html path directory shall be {htm_path}")
os.mkdir(htm_path)

content = check_content(URL)



final_time = time.time() - start
print(f"it has taken {final_time} seconds")

