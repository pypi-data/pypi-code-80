from eazynlp.base.transcript import Transcript


class Analysis:
    """
    Superclass that defines the basic properties and methods
    supported by child classes that implement specific analyses.
    """
    analysis_result = None

    def __init__(self, transcript: Transcript = None):
        """
        :param transcript: Trancript object
        """
        self.transcript = transcript

    def generate_analysis_result(self):
        """
        Shell method for generating analysis result in child class
        """
        pass

    def save_analysis_result(self, target_filepath):
        """
        Shell method for saving analysis result in child class
        to a file
        :param target_filepath: Target filepath to save analysis result
        """
        pass


if __name__ == "__main__":
    print("All good!")
