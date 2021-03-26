from eazynlp.base.transcript import Transcript
from eazynlp.text_cleaner.cleaner import Cleaner
from nltk.corpus import stopwords


class StopwordCleaner(Cleaner):
    """
    A subclass of Cleaner superclass that removes stopwords from transcript
    """

    def execute(self, option_dict=None):
        """
        :param option_dict: A dictionary consisting of
        "stopword_list": [a list of additional stopwords]
        :return: N/A
        """
        if (option_dict is not None) and ("stopword_list" in option_dict):
            stopword_list = option_dict["stopword_list"]
        else:
            stopword_list = []

        if self.transcript.df_transcript is not None:
            # Check language to get the correct stopwords
            # Add upper and lowercase stopwords to work with WordCaseCleaner in Pipeline
            if self.transcript.get_language()[0] == "DE":
                stopword_list += stopwords.words('german') + [word.upper() for word in stopwords.words('german')]
            else:
                stopword_list += stopwords.words('english') + [word.upper() for word in stopwords.words('english')]
            self.transcript.df_transcript["Transcript"] = self.transcript.df_transcript["Transcript"].apply(
                lambda x: " ".join([item for item in x.split(" ") if item not in stopword_list]))


if __name__ == "__main__":
    print("All is good!")
