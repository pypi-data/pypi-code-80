import functools
import logging
import os
import subprocess

log = logging.getLogger(__name__)


def report_open_fds(sockets_only):
    def wrap(func):
        # Report on open sockets
        def wrapper(*args, **kwargs):
            # Get number of open fds before function
            pid = os.getpid()
            p_args = ["lsof", "-a", "-p", str(pid)]
            if sockets_only:
                p_args.insert(1, "-i")
            ps = subprocess.Popen(p_args, stdout=subprocess.PIPE)
            before = (
                subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
                .decode("utf-8")
                .strip("\r\n")
            )
            func(*args, **kwargs)
            ps = subprocess.Popen(p_args, stdout=subprocess.PIPE)
            after = (
                subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
                .decode("utf-8")
                .strip("\r\n")
            )

            log.debug(
                f"Number of fds ({func.__name__}) before: {before}, after: {after}"
            )

        return wrapper

    return wrap
