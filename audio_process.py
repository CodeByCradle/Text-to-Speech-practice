# Two goals with this test.py. First, being able to download mp3 file. Second, being able to crop the mp3 file. Third, massively crop mp3 files.
import argparse
from pathlib import Path
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import pandas as pd
import requests

import pydub
from pydub import AudioSegment

# This command works with virtual environment
pydub.AudioSegment.converter = (
    "/Users/codebycradle/Library/Application Support/ffmpeg-downloader/ffmpeg"
)


# TODO: A better file system, because it might be the problem that the data file cannot find the corresponding audio.


# First task.
def download_audio_from_link(link: str, data_dir: str, filename):
    r = requests.get(link)
    if r.status_code == 200:
        with open(f"{data_dir}/{filename}", "wb") as audio_file:
            audio_file.write(r.content)
        return f"{data_dir}/{filename}"
    else:
        return r.status_code
    
def read_audio_text_pairs(input_data: pd.DataFrame):
    # What will be a better variable name????
    the_list = []
    df= pd.read_csv(input_data, sep=",", header=0)
    for index, row in df.iterrows():
        the_list.append((f'Data/{row["audio_file"]}', f'Data/{row["text_file"]}'))
    return the_list


def clip_audio(audio_file: str, data_file: str):
    """Clip the audio according to the start and end timestamps, and also report the file name and phonoform

    Args:
        audio_file (str): audio file
        data_file (str): data file

    Returns:
        dict: key is audio filename, value is phonoform
    """
    df = pd.read_csv(data_file, header=0, sep="\t")
    audio_file = AudioSegment.from_file(audio_file)
    subfolder_path = Path(data_file).parent / Path(data_file).stem
    Path(subfolder_path).mkdir(parents=True, exist_ok=True)
    filename_stem = Path(data_file).stem
    output_dict = {"audio":[], "form":[]} 
    for idx, row in df.iterrows():
        start = row["START"]
        end = row["END"]
        seg = audio_file[start * 1000 : end * 1000]
        seg.export(f"{subfolder_path}/{filename_stem}_{idx}.wav", format="wav")
        output_dict["audio"].append(f"{filename_stem}_{idx}.wav")
        output_dict["form"].append(row["FORM"])
    return output_dict

# Third task.
# TODO: We have to create another dataframe to have the form of
# clip_file phonoform


if __name__ == "__main__":
    # Let's download audio :D
    # TODO: Refactor!!!! I need to make this entire workflow "make sense"
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "input_file", help="Please give a file contains multiple audio links."
    # )
    parser.add_argument("pair_data", help="Please give a file contains the audio file name and the phono form file name")
    args = parser.parse_args()
    # supress for now
    # There is a pipeline gap between these two chunks.
    # with open(args.input_file, "r") as data_file:
    #     links = data_file.readlines()
    #     for link in links:
    #         link.rstrip("\n")
    #         filename = download_audio_from_link(link.rstrip("\n"), "Data", link.rstrip("\n").split("/")[-1])
    # Preparation: read in dataframe and create an array with [(audio, text_file)]
    pairs = read_audio_text_pairs(args.pair_data)

    #TODO: Supress the warning.
    idx = 0
    for each in pairs:
        aud, dat = each[0], each[1]
        output_dict= clip_audio(aud, dat)
        pd_df = pd.DataFrame.from_dict(output_dict, orient='columns')
        pd_df.to_csv(f"output_file_{idx}.txt", sep="|", header = False, index=False)
        idx +=1
        

