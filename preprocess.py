import requests
from bs4 import BeautifulSoup as bs

def process_link(link):
    """find the wav link and xml link.

    Args:
        link (str): html link

    Returns:
        dict: a dictionary reports the wav and xml links
    """
    output_file = download_html(link, "Webpages/temp.html")
    with open(output_file, "r") as html_file:
        content = html_file.read()
        soup = bs(content, "html.parser") 
        resources = soup.find_all("a")
        output = {"wav":"", "xml":""}
        for resource in resources: 
            link = resource.get("href")
            if link and "wav" in link:
                output["wav"] = link
            elif link and "xml" in link:
                output["xml"] = link
    return output

def download_html(web_link: str, output_file: str):
    r = requests.get(web_link)
    if r.status_code == 200:
        with open(output_file, "w") as html_file:
            html_file.write(r.text)
    return output_file

if __name__ == "__main__":
    """execution area. we can for sure make it cleaner, but we can also do it later..."""

    output_file=download_html(
        "https://pangloss.cnrs.fr/corpus/Japhug", 
        "Webpages/Japhung.html"
        )

    with open(output_file, "r") as html_file: 
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

    with open("weblinks.txt", "a") as f:
        for link in links:
            audio_and_transcribe = process_link(link) 
            f.write(f"{audio_and_transcribe['wav']},{audio_and_transcribe['xml']}\n")
            print(f"wrote the links {audio_and_transcribe} to file")
    



       
    

