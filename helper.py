
def create_filename_from_link(web_link: str):
    """Create a filename from a given web link. Ok.... the function sounds so stupid...

    Args:
        web_link (str): a given web link
    """
    filename = web_link.split("/")
    # usually web_link.split("/")[-1] should really work 
    return filename[-1] 


def get_transcription_links(filename: str): 
    pairs = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            transcribe = line.split(",")[1].strip("\n")
            if not transcribe:
                continue
            filename = create_filename_from_link(transcribe)
            pairs[filename] = transcribe
    return pairs