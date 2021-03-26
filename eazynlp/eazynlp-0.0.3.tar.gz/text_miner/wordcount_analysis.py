from base.transcript import Transcript
from base.pipeline import Pipeline
from text_cleaner.punctuation_cleaner import PunctuationCleaner
from text_cleaner.stopword_cleaner import StopwordCleaner
from text_cleaner.wordcase_cleaner import WordCaseCleaner
from text_miner.analysis import Analysis
from visualizer.visualizer import Visualization
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class WordCountAnalysis(Analysis, Visualization):
    """
    Analysis class that generates word count statistics
    for a transcript.
    """

    def generate_analysis_result(self):
        """
        Shell method for generating analysis result in child class
        """
        transcript = self.transcript
        Pipeline(transcript,
                 [
                     (WordCaseCleaner, {"to_lower": True}),
                     (PunctuationCleaner, {}),
                     (StopwordCleaner, {"stopword_list": ["ja"]})
                 ]
                 ).execute()
        text = transcript.df_transcript["Transcript"]
        wordcount_result = text.str.split(expand=True).stack().value_counts()
        return wordcount_result

    def save_analysis_result(self, target_filepath):
        """
        Shell method for saving analysis result in child class
        to a file
        :param target_filepath: Target filepath to save analysis result
        """
        wordcount_result = self.generate_analysis_result()
        wordcount_result.to_csv(
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
        Pipeline(transcript,
                 [
                     (WordCaseCleaner, {"to_lower": True}),
                     (PunctuationCleaner, {}),
                     (StopwordCleaner, {"stopword_list": ["ja"]})
                 ]
                 ).execute()
        text = transcript.df_transcript["Transcript"].str.cat(sep=" ")
        if visual_type == "wordcloud":
            wordcloud = WordCloud(
                width=1500,
                height=1000,
                background_color='black'
            ).generate(text)
            plt.figure(
                figsize=(40, 30),
                facecolor='k',
                edgecolor='k')
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
        pass


if __name__ == "__main__":
    print("All good!")
