"""
Cleaner module
Clean text from your data files into a format that allows for analysis
"""

from base.transcript import Transcript


class Cleaner:
    """
    Superclass that defines basic properties and methods of pipelines
    """

    def __init__(self, transcript: Transcript = None):
        """
        :param transcript: Trancript object
        """
        self.transcript = transcript

    def set_transcript(self, transcript: Transcript):
        """
        :param transcript: Trancript object
        :return: N/A
        """
        self.transcript = transcript

    def execute(self, option_dict=None):
        """
        Shell method for executing cleaning in child class
        :param option_dict: Dictionary of options that cleaners take
        :return: N/A
        """
        # if option_dict is None:
        #    option_dict = {}
        pass


if __name__ == "__main__":
    print("All is good!")
