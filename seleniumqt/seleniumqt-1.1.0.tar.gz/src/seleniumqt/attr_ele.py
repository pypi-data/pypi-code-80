import traceback


def run(path, function_name, ele, p):
    imp = path + '.' + function_name + '.' + ele

    try:
        dd = __import__(imp, fromlist=True)
        if hasattr(dd, function_name):
            f = getattr(dd, function_name, None)
            t = f(p)
            return t
    except:
        traceback.print_exc()
