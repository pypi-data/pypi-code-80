from eazynlp.base.transcript import Transcript


class Pipeline:
    """
    Superclass that defines basic properties and methods of pipelines
    """
    def __init__(self, transcript: Transcript, steps=None):
        """
        :param transcript: Transcript of type Transcript object
        :param steps: Steps in pipeline (default set to None)
        """
        if steps is None:
            steps = []
        self.transcript = transcript
        self.steps = steps

    def set_steps(self, steps):
        """
        :param steps: Steps in pipeline
        :return: N/A
        """
        self.steps = steps

    def execute(self):
        """
        Shell method for executing pipeline
        Expects each step in step list to contain a tuple
        of the form (step, dictionary of options for that step)
        :return: N/A
        """
        # for step in self.steps:
        #    step(self.transcript).execute()
        for (step, option_dict) in self.steps:
            step(self.transcript).execute(option_dict)


if __name__ == "__main__":
    print("All good!")
