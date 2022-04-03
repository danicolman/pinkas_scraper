from tqdm import tqdm
import csv
from urllib.request import urlopen
fields = ["Name", "DOB", "DOD", "Residence"]
filename = "victims_test.csv"
with open(filename, "w", encoding = "utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    for page in tqdm(range(1,10)):
        url = "http://pinkas.jewishmuseum.cz/vyhledavani/detail?victim_id={}".format(page)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        victim_dict = {}

        name_index = html.find("<p class=\"detail-person__name\">")
        name_start_index = name_index + len("<p class=\"detail-person__name\">")
        name_end_index = html.find("</p>")
        name = html[name_start_index:name_end_index]
        victim_dict["Name"] = name

        dob_index = html.find("<p class=\"detail-person__date\">")
        dob_start_index = dob_index + len("<p class=\"detail-person__date\">")
        dob_end_index = html.find("-", dob_start_index)
        dob = html[dob_start_index:dob_end_index].strip()
        victim_dict["DOB"] = dob

        dod_start_index = html.find("-", dob_end_index) + 1
        dod_end_index = html.find("</p>", dod_start_index)
        dod = html[dod_start_index:dod_end_index].strip()
        victim_dict["DOD"] = dod

        residence_index = html.find("Last residence before deportation:")
        residence_start_index = residence_index + len("Last residence before deportation:")
        residence_end_index = html.find("</p>", dod_end_index + 1)
        residence = html[residence_start_index:residence_end_index]
        victim_dict["Residence"] = residence

        writer.writerow(victim_dict)
