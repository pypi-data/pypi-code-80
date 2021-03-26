from base.transcript import Transcript
from text_cleaner.cleaner import Cleaner
from nltk.tokenize import RegexpTokenizer


class PunctuationCleaner(Cleaner):
    """
    A subclass of Cleaner superclass that removes punctuation from transcript
    """

    def execute(self, option_dict=None):
        """
        :param option_dict: An empty dictionary (no options for this cleaner subclass)
        :return:
        """
        if self.transcript.df_transcript is not None:
            tokenizer = RegexpTokenizer(r'\w+')
            self.transcript.df_transcript["Transcript"] = self.transcript.df_transcript["Transcript"].apply(
                lambda x: " ".join(str(item) for item in tokenizer.tokenize(x)))


if __name__ == "__main__":
    print("All is good!")
