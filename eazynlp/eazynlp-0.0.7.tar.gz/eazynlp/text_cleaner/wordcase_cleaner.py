from eazynlp.base.transcript import Transcript
from eazynlp.text_cleaner.cleaner import Cleaner


class WordCaseCleaner(Cleaner):
    """
    A subclass of Cleaner superclass that converts transcript to lower/uppercase
    """

    def execute(self, option_dict=None):
        """
        :param option_dict: A dictionary consisting of
        "to_lower": True (convert transcript to lowercase)
        or False (convert transcript to uppercase)
        :return: N/A
        """
        if (option_dict is not None) and ("to_lower" in option_dict):
            to_lower = option_dict["to_lower"]
        else:
            to_lower = True

        if self.transcript.df_transcript is not None:
            if to_lower:
                self.transcript.df_transcript["Transcript"] = self.transcript.df_transcript["Transcript"].str.lower()
            else:
                self.transcript.df_transcript["Transcript"] = self.transcript.df_transcript["Transcript"].str.upper()


if __name__ == "__main__":
    print("All is good!")
