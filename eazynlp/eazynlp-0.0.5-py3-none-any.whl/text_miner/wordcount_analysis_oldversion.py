from base.transcript import Transcript
from tests.test_utils import get_sample_data_filepath
from tests.test_utils import get_sample_metadata_filepath
from text_miner.analysis import Analysis
from visualizer.visualizer import Visualization
from wordcloud import WordCloud  # , STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt


class WordCountAnalysis(Analysis, Visualization):
    """
    Analysis class that generates word count statistics
    for a transcript.
    """

    # def __init__(self, wordcloud=None):
    #    super().__init__()
    #    self.wordcloud = wordcloud

    def generate_analysis_result(self):
        """
        Shell method for generating analysis result in child class
        """
        transcript = self.transcript
        df_text = transcript.load_df_text()
        wordcount_result = df_text["Transcript"].str.split(expand=True).stack().value_counts()
        return wordcount_result

    def save_analysis_result(self, target_filepath):
        """
        Shell method for saving analysis result in child class
        to a file
        :param target_filepath: Target filepath to save analysis result
        """
        res.to_csv(
            path_or_buf=target_filepath,
            sep=",",
            header=False,
            index=True
        )

    def show_visualization(self, visual_type=None):
        """
        Shell method for showing visualization in child class
        :param visual_type: Type of visualization
        """
        transcript = self.transcript
        df_text = transcript.load_df_text()
        text = df_text["Transcript"].iloc[1:].to_string()
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(text)
        text = " ".join(str(item) for item in text)
        if visual_type == "wordcloud":
            if transcript.get_language()[0] == "DE":
                stopword_set = set(stopwords.words('german'))
            else:
                stopword_set = set(stopwords.words('english'))
            # self.wordcloud = WordCloud(
            wordcloud = WordCloud(
                width=1500,
                height=1000,
                background_color='black',
                stopwords=stopword_set
            ).generate(text)
            plt.figure(
                figsize=(40, 30),
                facecolor='k',
                edgecolor='k')
            # plt.imshow(self.wordcloud, interpolation='bilinear')
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.show()

    def save_visualization(self, visual_type, target_filepath=None):
        """
        Shell method for saving analysis result in child class
        to a file
        :param visual_type: Type of visualization
        :param target_filepath: Target filepath to save visualization
        """
        # if visual_type == "wordcloud": self.wordcloud.to_file(target_filepath)
        pass


if __name__ == "__main__":
    t = Transcript()

    t.set_metadata_filepath(get_sample_metadata_filepath())
    lang = t.get_language()
    # print(lang[0])

    t.set_transcript_filepath(get_sample_data_filepath())
    sample_interview = t.load_df_text()
    print(sample_interview.head())

    a = WordCountAnalysis(t)
    # print(a.transcript.transcript_filepath)
    res = a.generate_analysis_result()
    a.save_analysis_result("wordcount_analysis.csv")
    """res.to_csv(
        path_or_buf="wordcount_analysis.csv",
        sep=",",
        header=False,
        index=True
    )"""
    a.show_visualization(visual_type="wordcloud")