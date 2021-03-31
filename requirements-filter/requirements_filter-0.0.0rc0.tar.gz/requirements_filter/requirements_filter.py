import click

# The exit(1) is used to indicate error in pre-commit
NOT_OK = 1


@click.command()
@click.option("--filename1", default="requirements.txt")
@click.option("--filename2", default="requirements-private.txt")
def rqf(filename1, filename2):
    requirements = open_file(filename1)
    private_txt = open_file(filename2)

    at_sign_set = create_set(private_txt, "@")
    requirements_without_at_sign = remove_common_elements(
        requirements, at_sign_set
    )

    # the filename1 will be overwritten
    write_file(filename1, requirements_without_at_sign)


def remove_common_elements(package_list, remove_set):
    """
    Remove the common elements between package_list and remove_set.

    Note that this is *not* an XOR operation: packages that do not
    exist in remove_set (but exists in remove_set) are not included.

    Parameters
    ----------
    package_list : list
        List with string elements representing the packages from the
        requirements file. Assumes that the list has "==" to denote
        package versions.

    remove_set : set
        Set with the names of packages to be removed from requirements.

    Returns
    -------
    list
        List of packages not presented in remove_set.
    """
    package_not_in_remove_set = []
    for package in package_list:
        package_name = package.split("==")[0].strip()
        if package_name not in remove_set:
            package_not_in_remove_set.append(package)
    return package_not_in_remove_set


def open_file(filename):
    """
    Open txt file.

    Parameters
    ----------
    filename : str
        Name of the file to be opened.

    Returns
    -------
    list
        List of strings with the packages names and versions.
    """
    try:
        with open(filename) as file_object:
            requirements = file_object.readlines()
        return requirements
    except FileNotFoundError:
        print(f"{filename} not found.")
        exit(NOT_OK)


def create_set(package_list, delimiter):
    """
    Create a set of packages to be excluded.

    This function receives a list of strings, takes the packages' names
    and transforms them to a set.

    If the list contains packages with @ but the delimiter input is '==',
    then the package is ignored.

    Parameters
    ----------
    package_list : list
        List of strings with each element representing a package name
        and version.

    Returns
    -------
    set
        Set with the package names.
    """
    list_of_package_names = []
    for package in package_list:
        if delimiter in package:
            package_name = package.split(delimiter)
            list_of_package_names.append(package_name[0].strip())
    package_set = set(list_of_package_names)
    return package_set


def write_file(filename, information):
    """
    Write string information into a file.

    Parameters
    ----------
    file1 : str
        Name of the file where the information will be saved.
        It should have the filepath and the file extension (.txt).

    information : str
        Information to be saved.
    """
    with open(filename, "w") as file_save:
        for line in information:
            file_save.write(line)


if __name__ == "__main__":
    rqf(file1="requirements.txt", file2="requirements-private.txt")
