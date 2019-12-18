from bs4 import BeautifulSoup
import requests
import xlwt

def check_content(URL):

    field_title = [
        "Learning Outcome",
        "Assessment",
        "Assessor",
        "Target Year of Achievement",
        "Related Learning Outcomes",
        "Overview",
        "Resources",
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    html_table = soup.find("div", attrs={"class": "pure-u-1 pure-u-md-1 pure-u-lg-18-24"})
    table = soup.find("table", attrs={"class": "lotable"})

    # <th> contains the lo title
    title = []
    for row in table.find_all("th")[1:]:
        title.append(row.get_text())

    # <td> contains field names and content - tecnically this is not needed.
    content = []
    for row in table.find_all("td")[1:]:
        if row.get_text().strip() == None:
            content.append("NONE")
        else:
            content.append(row.get_text())

    # The <strong> contains the field names, the LO is in <strong> as well so we need to remove that from the list.
    headings = []
    for row in table.find_all("strong"):
        headings.append(row.get_text())

    # cleaning content from headings
    for item in field_title:
        content.remove(item)

    # cleaning up content
    clear_content = [item.strip() for item in content]

    # cleaning heading from content
    headings.remove(content[0])

    class url_content(object):
        def __init__(
            self,
            obj_clear_content=clear_content,
            obj_headings=headings,
            obj_title=title,
            obj_table=html_table,
        ):
            self.content = obj_clear_content
            self.headings = obj_headings
            self.title = obj_title
            self.table = obj_table

    obj_content = url_content()
    if len(clear_content) == 8:
        return obj_content
    else:
        return print(
            f"Attention! There was an error while parsing the content of url:{URL}: \nThe table {title} has lengh diferent than 8."
        )


def url_generator(input_file,output_file,exceptions):
    f = open(input_file, "r")
    lo_id = []
    lo_index = []

    for line in f:
        lo_id.append(line.split(" ")[0])
        lo_index.append(int(line.split(" ")[1].strip()))
    f.close()

    # For each lo_id creates append lo_url n = lo_index times with
    lo_url = []
    for id, index in zip(lo_id, lo_index):
        i = 0
        while i != index:
            lo_url.append(f"https://www.rcophth.ac.uk/learningoutcomes/{id}{i + 1}")
            i = i + 1

    exceptions_lo = [item[0] for item in exceptions]
    exceptions_url = [item[1] for item in exceptions]

    print(f"Found the following exceptions: {exceptions_lo}.\nReplacing the url's for {exceptions_url}")

    url_array_index = [item.split("https://www.rcophth.ac.uk/learningoutcomes/")[1] for item in lo_url]
    exception_indices = [key for key, val in enumerate(url_array_index) if val in set(exceptions_lo)]

    for indices, url in zip(exception_indices, exceptions_url):
         lo_url[indices] = url

    new_file = open(output_file, "w+")
    for item in lo_url:
        new_file.write(f"{item}\n")
    new_file.close()
    return lo_url


def create_xls_table(content, headings, title, number):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    book.save(lo_test)

    return True

# def create_htmltable(html_file_name,content,path):
#     pwd = f"{path}/{html_file_name}"
#     new_file = open(pwd, w+")
#     for line in content.table:
#         new_file.write(f"{line}")
#     new_file.close()
