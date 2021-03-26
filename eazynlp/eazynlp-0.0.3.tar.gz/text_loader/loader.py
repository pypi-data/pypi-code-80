"""
Loader module
Load text from your data files into a format that allows for analysis
"""

import pandas as pd


def load_interview_transcript(transcript):
    """Reads interview transcript csv file as a dataframe.
    """
    transcript_df = pd.read_csv(transcript)
    return transcript_df


if __name__ == "__main__":
    print("All good!")
