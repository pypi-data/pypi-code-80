from eazynlp.text_cleaner.punctuation_cleaner import PunctuationCleaner
from eazynlp.text_cleaner.stopword_cleaner import StopwordCleaner
from eazynlp.text_cleaner.wordcase_cleaner import WordCaseCleaner
from eazynlp.text_miner.analysis import Analysis
from eazynlp.visualizer.visualizer import Visualization
from eazynlp.base.pipeline import Pipeline


class TopicModelAnalysis(Analysis, Visualization):
    """
    Analysis class that generates topic model for a transcript.
    """

    def generate_analysis_result(self):
        transcript = self.transcript
        Pipeline(transcript,
                 [
                     (WordCaseCleaner, {"to_lower": True}),
                     (PunctuationCleaner, {}),
                     (StopwordCleaner, {"stopword_list": ["ja"]})
                 ]
                 ).execute()
        text = transcript.df_transcript["Transcript"].str.cat(sep=" ")
        return text

    def save_analysis_result(self, target_filepath):
        """
        Shell method for saving analysis result in child class
        to a file
        :param target_filepath: Target filepath to save analysis result

        topicmodel_result = self.generate_analysis_result()
        topicmodel_result.to_csv(
            path_or_buf=target_filepath,
            sep=",",
            header=False,
            index=True
        )"""

    def show_visualization(self, visual_type=None):
        """
        Shell method for showing visualization in child class
        :param visual_type: Type of visualization
        """
        pass

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
