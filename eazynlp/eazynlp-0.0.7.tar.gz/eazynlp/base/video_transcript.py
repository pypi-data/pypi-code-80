from eazynlp.base.transcript import Transcript


class VideoTranscript(Transcript):
    """
    Child class of transcript for video transcript objects
    """

    def __init__(self, timestep_interval=None, transcript_filepath=None, metadata_filepath=None):
        super(VideoTranscript, self).__init__(transcript_filepath, metadata_filepath)
        self.timestep_interval = timestep_interval
        if timestep_interval:
            self.timestep_interval = self.get_timestep_interval()

    def get_timestep_interval(self):
        df_metadata = self.load_df_metadata()
        timestep_interval = df_metadata["Timestep Interval"]
        return timestep_interval[0]


if __name__ == "__main__":
    print("All good!")
