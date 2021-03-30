import shortuuid


def get_type_name(obj):
    type_name = obj.__class__.__module__ + "." + obj.__class__.__name__
    if type_name in ["builtins.module", "__builtin__.module"]:
        return obj.__name__
    else:
        return type_name


def generate_uuid():
    generated_uuid = shortuuid.ShortUUID(alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz"))
    return generated_uuid.random(8)
