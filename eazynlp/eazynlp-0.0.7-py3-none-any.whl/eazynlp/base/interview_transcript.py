from eazynlp.base.transcript import Transcript


class InterviewTranscript(Transcript):
    """
    Child class of transcript for interview transcript objects
    """

    def __init__(self, transcript_filepath=None, metadata_filepath=None):
        super(InterviewTranscript, self).__init__(transcript_filepath, metadata_filepath)


if __name__ == "__main__":
    print("All good!")
