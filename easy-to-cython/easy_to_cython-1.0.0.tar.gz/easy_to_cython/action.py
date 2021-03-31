import glob
import json
import os
import shutil


def release():
    for path in glob.glob('./build/lib.*'):
        dirs = os.listdir(path)
        for dir_name in dirs:
            shutil.rmtree('./%s' % dir_name)
            shutil.copytree(os.path.join(path, dir_name), './%s' % dir_name)


def package():
    pyinstall_spec = 'pyi-makespec ./main.py '

    config_entity = None
    if os.path.exists('./easy_to_cython.json'):
        with open('./easy_to_cython.json', 'r', encoding='utf-8') as file:
            config_entity = json.load(file)
    if config_entity is not None:
        if config_entity['with_scikit'] == 'true':
            pyinstall_spec += '--hiddenimport sklearn '
            pyinstall_spec += '--hiddenimport sklearn.ensemble '
            pyinstall_spec += '--hiddenimport sklearn.tree._utils '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.typedefs '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.ball_tree '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.dist_metrics '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.quad_tree '
            pyinstall_spec += '--hiddenimport sklearn.utils._cython_blas '
            pyinstall_spec += '--hiddenimport scipy._lib.messagestream '
        if config_entity['with_statics_model'] == 'true':
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._conventional '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._univariate '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._inversions '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._conventional '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._univariate '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._inversions '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._classical '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._alternative '
    os.system(pyinstall_spec)

    with open('./main.spec', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('import sys\nsys.setrecursionlimit(5000)\n' + content)
    os.system('pyinstaller --clean ./main.spec')
