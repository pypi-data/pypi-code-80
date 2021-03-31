from os import environ
from os.path import dirname, join

MAJOR_VERSION = 0
MINOR_VERSION = 1


def get_version(setup_dist=False):
    curr_directory = dirname(__file__)
    version_file = join(curr_directory, "version")

    if setup_dist:
        print(environ)
        build_id = int(environ['BUILD_ID'])
        f = open(version_file, "w")
        f.write("%s" % build_id)
        f.close()
    else:
        try:
            build_id = open(version_file).read()
        except FileNotFoundError:
            build_id = "404"

    return "%d.%d.%s" % (MAJOR_VERSION, MINOR_VERSION, build_id)
