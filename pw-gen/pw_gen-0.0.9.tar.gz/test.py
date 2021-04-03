from collections import Counter
from matplotlib import pyplot as plt
import pw_gen

def main():
    """
        main function

        Args: none

        Example Usage: none
    """

    pw_list = []

    pw_test_lengths = [5, 6]

    pin_list = []

    pin_test_lengths = list(range(19, 20))

    pw_separator = ''

    sample_count = 1000000

    print("Password test lengths: ", pw_test_lengths)

    print("Pin Test Lengths: ", pin_test_lengths)

    for pin_test in pin_test_lengths:
        pin_test_filename = "pin_test_" + str(pin_test) + ".txt"

        print("Test filename for pins of length ", str(pin_test), ": ", pin_test_filename)

    for pw_test in pw_test_lengths:
        pw_test_filename = "pw_test_simple_" + str(pw_test) + ".txt"

        print("Test filename for simple passwords of length ", str(pw_test), ": ", pw_test_filename)

        for _ in range(sample_count):
            new_password = pw_gen.Simple(pin_test)
            pw_generated_list = new_password.generate()
            pw_final = new_password.result()

            if _ == 1:
                print("Simple Password Generation: ", new_password)
                print("Simple Password yielded: ", pw_final)

            del new_password

            pw_list.append(pw_final)

        with open(pw_test_filename, 'w') as file_handle:
            file_handle.write(pw_separator.join(pw_list))

        with open(pw_test_filename, 'r') as file_handle:
            sample_string = file_handle.read()

        print("1,000,000 passwords at ", str(pw_test), \
                " characters each yields: ", len(sample_string))

        counter_object = Counter(sample_string)

        counter_list = counter_object.most_common()

        print(counter_list)

        image_filename = pw_final + ".png"

        plt.scatter(*zip(*counter_list))
        plt.savefig(image_filename)
        plt.show()

    return 0

if __name__ == "__main__":
    main()
