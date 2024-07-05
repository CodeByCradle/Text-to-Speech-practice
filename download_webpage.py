import requests
from bs4 import BeautifulSoup as bs

# TODO: put this into a function, so we can reuse later
r = requests.get("https://pangloss.cnrs.fr/corpus/Japhug")
if r.status_code == 200:
    with open(f"Webpages/Japhung.html", "w") as html_file:
        html_file.write(r.text)
        #html_file.write(r.text)

with open("Webpages/Japhung.html", "r") as html_file: 
    content = html_file.read()
    soup = bs(content, "html.parser")
    # let's try to parse the table 
    table= soup.find("table")
    rows = table.findAll("tr")
    links = []
    for row in rows:
        the_link_text = row.get("onclick")
        if the_link_text:
            the_link = the_link_text.split("= ")[1]
            links.append(the_link.replace("'", ""))

#TODO: reuse the function.
for link in links:
    r = requests.get(link)
    if r.status_code==200:
    # find the xml link, wav link, download, and make a file in the format of "filename.wav, corresponding_filename.xml" 
        break 



       
    

