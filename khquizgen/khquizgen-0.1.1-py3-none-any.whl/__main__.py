"""
This is the package's main module.
It should define a main function to be executed, representing execution of the
whole package.
"""
# external imports
import os
# Import project variables (provided via __init__)
from khquizgen import INPUTS_PATH, OUTPUTS_PATH, logger

# Import project-specific modules
from khquizgen.src import parse_questions, gen_quiz, use_template


def main(input_path=None, output_path=None):
    logger.debug("Main function called.")
    inputs = input_path if input_path else INPUTS_PATH
    outputs = output_path if output_path else OUTPUTS_PATH
    data = parse_questions.run(inputs_path=inputs, outputs_path=outputs)
    quiz = gen_quiz.run(data, 100)
    verify = use_template.run(quiz=quiz, inputs_path=inputs, outputs_path=outputs)
    print(verify)


if __name__ == '__main__':
    assert len(__package__) > 0, """

    The '__main__' module does not seem to have been run in the context of a
    runnable package ... did you forget to add the '-m' flag?

    Usage: python3 -m <packagename>
    """
    main()
