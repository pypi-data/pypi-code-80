import pandas as pd


class Transcript:
    """
    Superclass that defines the basic properties and methods
    supported by child classes that implement specific transcript types.
    """
    def __init__(self, transcript_filepath=None, metadata_filepath=None):
        self.transcript_filepath = transcript_filepath
        self.metadata_filepath = metadata_filepath

        self.df_transcript = None
        self.df_metadata = None
        if transcript_filepath:
            self.df_transcript = pd.read_csv(transcript_filepath)
        if metadata_filepath:
            self.df_metadata = pd.read_csv(metadata_filepath)

    # Instance method
    def set_transcript_filepath(self, transcript_filepath):
        """
        Sets transcript property transcript_filepath
        :param transcript_filepath: Transcript filepath
        :return: None
        """
        self.transcript_filepath = transcript_filepath

    def set_metadata_filepath(self, metadata_filepath):
        """
        Sets transcript property metadata_filepath
        :param metadata_filepath: Metadata filepath
        :return: None
        """
        self.metadata_filepath = metadata_filepath

    def set_df_transcript(self):
        if self.transcript_filepath:
            self.df_transcript = pd.read_csv(self.transcript_filepath)

    def set_df_metadata(self):
        if self.metadata_filepath:
            self.df_metadata = pd.read_csv(self.metadata_filepath)

    def load_df_text(self):
        df_text = pd.read_csv(self.transcript_filepath)
        return df_text

    def load_df_metadata(self):
        df_metadata = pd.read_csv(self.metadata_filepath)
        return df_metadata

    def get_researcher(self):
        df_metadata = self.load_df_metadata()
        researcher = df_metadata["Researcher"]
        return researcher

    def get_participant(self):
        df_metadata = self.load_df_metadata()
        participant = df_metadata["Participant"]
        return participant

    def get_duration(self):
        df_metadata = self.load_df_metadata()
        duration = df_metadata["Duration"]
        return duration

    def get_language(self):
        df_metadata = self.load_df_metadata()
        language = df_metadata["Language"]
        return language

    def get_timestep_interval(self):
        pass


if __name__ == "__main__":
    print("All good!")
