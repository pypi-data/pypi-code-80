"""
This defines a git repository for each known query_type.
"""

TEMPLATEMAP = {
    "api": {
        "url": "https://github.com/lsst-sqre/lsst-apiquerytemplate",
        "branch": "JL2",
        "subdir": None,
    },
    "squash": {
        "url": "https://github.com/lsst-sqre/squash-bokeh",
        "branch": "JL2",
        "subdir": "template_notebooks/check_astrometry",
    },
}
