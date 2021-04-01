from logging import getLogger
import os
try:
    from lingua_franca.parse import normalize
except:
    def normalize(text, *args, **kwargs):
        return text

LOG = getLogger("intentBox")

flatten = lambda l: [item for sublist in l for item in sublist]


def resolve_resource_file(res_name):
    """Convert a resource into an absolute filename.

    Resource names are in the form: 'filename.ext'
    or 'path/filename.ext'

    The system wil look for ~/.mycroft/res_name first, and
    if not found will look at /opt/mycroft/res_name,
    then finally it will look for res_name in the 'mycroft/res'
    folder of the source code package.

    Example:
    With mycroft running as the user 'bob', if you called
        resolve_resource_file('snd/beep.wav')
    it would return either '/home/bob/.mycroft/snd/beep.wav' or
    '/opt/mycroft/snd/beep.wav' or '.../mycroft/res/snd/beep.wav',
    where the '...' is replaced by the path where the package has
    been installed.

    Args:
        res_name (str): a resource path/name
    Returns:
        str: path to resource or None if no resource found
    """
    # First look for fully qualified file (e.g. a user setting)
    if os.path.isfile(res_name):
        return res_name

    # Now look for ~/.chatterbox/res_name (in user folder)
    filename = os.path.expanduser("~/.chatterbox/" + res_name)
    if os.path.isfile(filename):
        return filename

    # Resource cannot be resolved
    raise FileNotFoundError(res_name)
