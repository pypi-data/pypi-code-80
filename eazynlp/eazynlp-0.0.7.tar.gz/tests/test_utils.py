"""
Helper function module for running tests
"""

import os
import pandas as pd

current_dir = os.path.dirname(os.getcwd()) + "\\tests"


def get_sample_data_filepath(datatype="interview"):
    """
    :param datatype: Can be "interview" or "video"
    :return: Sample filepath as string
    """
    if datatype == "interview":
        return current_dir+"\\test_interview_transcript.csv"
    else:
        return current_dir+"\\test_video_transcript.csv"


def get_sample_metadata_filepath(datatype="interview"):
    """
        :param datatype: Can be "interview" or "video"
        :return: Sample filepath as string
        """
    if datatype == "interview":
        return current_dir + "\\test_interview_metadata.csv"
    else:
        return current_dir + "\\test_video_metadata.csv"


def load_sample_csv(filetype="interview"):
    """
    :param filetype: Can be "interview" or "video"
    :return: Test sample csv as dataframe
    """
    # transcript = ""
    if filetype == "interview":
        transcript = "test_interview_transcript.csv"
    else:
        transcript = "test_video_transcript.csv"
    return pd.read_csv(transcript)


if __name__ == "__main__":
    print("All good!")
