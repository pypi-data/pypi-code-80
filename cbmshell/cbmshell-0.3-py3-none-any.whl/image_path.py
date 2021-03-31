import string


class Drive(int):
    pass


class ImagePath:
    @staticmethod
    def is_image_path(path):
        return len(path) > 1 and path[0] in string.digits and path[1] == ':'

    @staticmethod
    def split(drive_name, encoding):
        parts = drive_name.split(':', 1)
        return int(parts[0]), parts[1].encode(encoding)

    def __repr__(self):
        return "ImagePath({}:{})".format(self.drive, self.encoded_name)
