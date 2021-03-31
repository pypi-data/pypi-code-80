import os
SVN_PARENT_PATH = os.getenv("SVN_PARENT_PATH", '/opt/svn_parent_path')
SVN_PARENT_URL = os.getenv("SVN_PARENT_URL", "file:////opt/svn_parent_path")
# PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER", "/mnt/c/Users/Tanjiro/Projects/eru_test_dir/projects")
FILE_MAP = {
            'shading':'base',
            'concept':'none',
            'modeling':'base',
            'rigging':'base',
            'storyboard':'none',
            'layout':'layout',
            'previz':'layout',
            'animation':'anim',
            'lighting':'lighting',
            'fx':'fx',
            'rendering':'lighting',
            'compositing':'comp',
        }
LOGIN_NAME = os.getenv("LOGIN_NAME", "email")
TEMPLATE_FILES_DIR =os.path.join(os.path.dirname(__file__), 'template_files')