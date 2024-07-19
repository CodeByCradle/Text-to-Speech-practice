import argparse
import requests
from pathlib import Path

from bs4 import BeautifulSoup as bs
from lxml import etree  
import pandas as pd
from helper import get_transcription_links

class WebCrawler:
    def __init__(self, web_link: list, filename_stem: list):
        """initiation.

        Args:
            web_link (str): A link that we want to download the pangloss file and extract the data.
            filename_stem (str): A filename and it is not including the stems (no .txt )
        """
        self.web_link: list = web_link
        self.filename_stem: list = filename_stem

    def get_material(self, data_dir: str):
        """Download material from a given web page link and save it

        Returns:
            str: a file path
        """
        r = requests.get(self.web_link)
        if r.status_code == 200:
            with open(f"{data_dir}/{self.filename_stem}", "w") as xml_file:
                xml_file.write(r.text)
            return f"{data_dir}/{self.filename_stem}"        
        return None

    def extract_data_by_tag(self, data_path: str, tag: str):
        """Extract the data according to a given tag from the given data path. I decide to move the language tag recognition to later.

        Returns:
            list: an array contains all the sentences.
        """
        try:
            with open(data_path) as f:
                bs_data = bs(f.read(), "xml")
                tag_data = bs_data.find_all("S")
                start_points, end_points, content = [],[],[]
                for each_tag in tag_data:
                    document= each_tag.find_all(tag, recursive=False)
                    if tag != "AUDIO":
                        content.extend([sentence.text for sentence in document])
                    else:
                        start_points.extend(sentence.get("start") for sentence in document)
                        end_points.extend([sentence.get("end") for sentence in document])
                if tag == "AUDIO":
                    for s, e in zip(start_points, end_points):
                        content.append([float(s), float(e)])
                return content
        except Exception as e:
            print(f"error is {e}")

    def write_data_to_file(self, data_dict:dict, output_filename: str):
        """Write the phonology, translation, and timestamps to a file

        Args:
            data_dict (dict): A dictionary with form, translation, and timestamps.
            output_filename (str): The output file name, the stem, not the .txt or something.
        """
        # Here, we need Pandas. 
        df = pd.DataFrame.from_dict(data_dict)
        # split the dataframe into two columns
        timestamps = pd.DataFrame(df['AUDIO'].to_list(), columns = ['START', 'END'])
        df.drop(columns=df.columns[-1],  axis=1,  inplace=True)
        df = pd.concat([timestamps, df], axis=1) 
        df.to_csv(output_filename, sep="\t")


if __name__ == "__main__":
    # TODO: find a better way to reduce this argument parser.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "links", help="Please give a file contains multiple web links of the transcriptions and audios"
    )
    parser.add_argument("data_dir", help="Please give a directory to store the data")
    args = parser.parse_args()
    pairs = get_transcription_links(args.links)
    Path(args.data_dir).mkdir(parents=True, exist_ok=True)
    data_dir = args.data_dir
    for filename, link in pairs.items():
        wc = WebCrawler(link, filename)
        xml_file_path = wc.get_material(data_dir)
        if xml_file_path:
            data_dict={}
            for tag in ["FORM", "TRANSL", "AUDIO"]:
                data_dict[tag] = wc.extract_data_by_tag(Path(xml_file_path).as_posix(), tag) 
            #TODO: find a better way to generate the file name.       
            wc.write_data_to_file(data_dict, f"audio_{filename}.tsv")
