import time
from crawler import get_content, url_generator, create_html_table, mkdir, create_xls_table , create_doc
from pathlib import Path
from progressbar import ProgressBar
import os
import pickle
import sys
from bs4 import BeautifulSoup
import requests

start = time.time()
sys.setrecursionlimit(10000)
# Open txt with number of lo and creates and output file with all the urls.
# This is important because some of the URL's need to be changed by hand.
file_lo_txt = "lo.txt"
output_url_file = "url_lo.txt"
# Need to generate an exception list in the form lo_id -> url
exceptions = [
    ("ca3", "https://www.rcophth.ac.uk/learningoutcomes/12658/"),
    ("ps24", "https://www.rcophth.ac.uk/learningoutcomes/ps24-2/")
]
url_array = url_generator(file_lo_txt, output_url_file, exceptions)

# Creating a path to html tables

pwd = Path(os.getcwd())
html_path = pwd / "html_tables"
xls_path = pwd / "xls"
mkdir(pwd, "html_tables")
mkdir(pwd, "xls")

lo_content =[]

print(f"Would you like to collect all {len(url_array)} learning outcomes?:[y/n]")
answer = input()

pick_content = []
pick_headings = []
pick_title = []
pick_synopsis = []

if answer == "y":
    # begin of loop to access all the learning outcomes.
    pbar = ProgressBar()
    print(f"This crawler will access {len(url_array)} learning outcomes url's. Good luck!")
    lo_content = []
    for url in pbar(url_array):
        lo_page = get_content(url)
        lo_content.append(lo_page)
        create_html_table(f"{lo_page.content[0]}.html", lo_page.extended_table, html_path)
        create_html_table(f"{lo_page.content[0]}.html", lo_page.extended_table, html_path)
        #create_doc_function()



    for lo in lo_content:
        pick_content.append(lo.content)
        pick_headings.append(lo.headings)
        pick_title.append(lo.title)
        pick_synopsis.append(lo.synopsis)

    # save lo_content
    with open("lo.1", "wb") as pickle_file:
        pickle.dump(pick_content, pickle_file)

    # save lo_headings
    with open("lo.headings", "wb") as pickle_file:
        pickle.dump(pick_headings, pickle_file)

    # save lo_headings
    with open("lo.title", "wb") as pickle_file:
        pickle.dump(pick_title, pickle_file)

    # save lo_headings
    with open("lo.synopsis", "wb") as pickle_file:
        pickle.dump(pick_synopsis, pickle_file)


elif answer == "n":
    print("ok then - not accessing the learning outcomes. Will read the content from previous saved picked file")
    try:
        with open('lo.content', 'rb') as lo_temp:
            pick_content = pickle.load(lo_temp)
        with open('lo.headings', 'rb') as lo_temp:
            pick_headings = pickle.load(lo_temp)
        with open('lo.synopsis', 'rb') as lo_temp:
            pick_synopsis = pickle.load(lo_temp)
        with open('lo.title', 'rb') as lo_temp:
            pick_title = pickle.load(lo_temp)
    except OSError:
        print(f"could not find saved pick.content, pick.headings, pick.synopsis or pick.title")
    else:
        print("pickles have been loaded! :-)")

else:
    print("That's not yes or no... :-P")

#create_xls_table(lo_content, xls_path)
#Create_one_doc(lo.title,lo.synopsis,lo.headings,lo.content)

print("Would you like to create a doc with all the lo? [y/n]")
answer = input()
if input=="y":
    create_doc(pick_title,pick_synopsis,pick_headings,pick_content)
    print("Done!")
else:
    print("ok, not creating doc.")

print("Would you like to create a doc with domains? [y/n]")
answer = input()
url_domain = "https://www.rcophth.ac.uk/curriculum/ost/learning-outcomes/"


#
# lo_group=[]
# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
#     }
# page = requests.get(url_domain, headers=headers)
# soup = BeautifulSoup(page.content, "html.parser")
# domains = [8,1,1,1,1]
# i = 1
# for number in domains:
#     for j in range(1,number+1):
#         lo_group = soup.find("div", attrs={"class": f"theme-domain-link d{i}m{j}"})
#         i = i+1


# if input=="y":
#     lo_group = get_domains(url_domain)
#     print("Done")
# else:
#     print("ok")

# THE END!
final_time = time.time() - start
print(f"This has taken {final_time/60} minutes of your life...")
