import os
import shutil

import cv2

from versign import VerSign
from versign.utils.segment import extract_from_grid


class VerSignUsers:
    def __init__(self, data_path):
        # type: (str) -> None
        self.__root = os.path.join(data_path, "users/")
        if not os.path.exists(self.__root):
            os.makedirs(self.__root)

        self.__out_ext = ".mat"

    def all(self):
        return [os.path.splitext(i)[0] for i in os.listdir(self.__root) if i.endswith(self.__out_ext)]

    def clear(self):
        shutil.rmtree(self.__root)
        if not os.path.exists(self.__root):
            os.makedirs(self.__root)

    def exists(self, user_id):
        # type: (str) -> bool
        """
        Checks if a user exists in database.

        :param user_id: unique id of the user to check
        :return true if user with given id exists, else false
        """
        return os.path.exists(os.path.join(self.__root, user_id + self.__out_ext))

    def remove(self, user_id):
        # type: (str) -> bool
        """
        Deletes a user from the database.

        :param user_id: unique id of the user to delete
        :return true if removal successful, else false
        """
        if not self.exists(user_id):
            return False

        user_file = os.path.join(self.__root, user_id + self.__out_ext)
        os.remove(user_file)
        return True

    def root(self):
        return self.__root


class VerSignClient:
    def __init__(self, v, data_path, verbose=False):
        # type: (VerSign, str, bool) -> None
        """
        Creates a desktop client instance.

        :param v: a VerSign object
        :param data_path: database location
        :param verbose: logs are printed if flag is set
        """
        self.__v = v
        self.__data_path = data_path
        self.__users = VerSignUsers(data_path)
        self.__verbose = verbose

    def __register(self, user_id, images_dir):
        self.__v.fit(images_dir, user_id, self.__users.root())
        return self.__users.exists(user_id)

    def contains_user(self, user_id):
        return self.__users.exists(user_id)

    def register(self, user_id, signature_grid):
        if self.__users.exists(user_id):
            return False

        # Create required directories for new user
        images_dir = os.path.join(self.__users.root(), user_id)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        signatures = extract_from_grid(signature_grid)
        if self.__verbose:
            print("found %s signatures" % len(signatures))

        # todo: augment signatures to generate more samples

        # Save all signatures
        for i, signature in enumerate(signatures):
            outfile = os.path.join(images_dir, "R%03d.png" % i)
            cv2.imwrite(outfile, signature)
            i += 1

        return self.__register(user_id, images_dir)

    def test(self, user_id, image, is_check=False):
        # todo
        pass
