import yaml
from decorator import decorator


@decorator
def write_result(func, *args, **kw):
    """Write method result"""
    self = args[0]
    if isinstance(self.in_yaml, dict):
        result = func(*args, **kw)
        self.in_yaml != result
        self.build_file.write_text(yaml.safe_dump(result, sort_keys=False))
        return result
    else:
        raise PermissionError('%s does not have the permission to run %s!' %
                              (self.user, func.__name__))
