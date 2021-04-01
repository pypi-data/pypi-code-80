import os
import sys
import random

is_all_test_success = True
print("\033[94mChecking the installation of the package ...\033[0m")
try:
    from pypi_learn.youtube_srt_mp3 import YoutubeSrtMp3
    print("\033[0;32;49mThe module is imported SUCCESSFULLY\033[0m")
except ImportError as module_not_installed:
    print('\033[91m' + module_not_installed.name + "\033[0m module is not found")
    is_all_test_success = False
NUM_SUBTITLES = 193  # total number of the subtitles
TEST_SRT_FILE_PATH = "test/test_srt_file/Ot0vYkRT1Mg.srt"
DOWNLOAD_PATH = "test/test_downloads_cropped"
PATH_CROPPED_FILE = DOWNLOAD_PATH + "/Ot0vYkRT1Mg"
URLS_FILE_PATH = "test/urls.txt"


def read_test_srt_file():
    """
    to compare random subtitles
    """
    all_lines_in_srt = open(TEST_SRT_FILE_PATH, 'r').readlines()

    # To test random subtitle
    def _test_compare_random_subs():
        # generate random number to check 
        num_rand = random.randint(0, NUM_SUBTITLES)
        # get subtitle from the cropped file
        sub_from_the_random_txt_file = open(PATH_CROPPED_FILE + "/Ot0vYkRT1Mg_crop_"
                                            + str(num_rand) + ".txt").readlines()[0]

        # calculate the index of the random generated sub

        real_index = num_rand * 4 - 2
        if num_rand == 0:
            real_index = 2

        # get random sub text from the real srt file
        real_random_sub = all_lines_in_srt[real_index][:-1]
        assert sub_from_the_random_txt_file == real_random_sub

    return _test_compare_random_subs()


def _download_crop_files():
    """
    it's  downloading and cropping files
    """
    return YoutubeSrtMp3(urls_file_path=URLS_FILE_PATH, save_dir=DOWNLOAD_PATH).convert()


def test_total_number_of_cropped_files():
    """
    to test number rof files
    """
    total_num_mp3 = 0
    total_num_srt = 0
    for file in os.listdir(DOWNLOAD_PATH + "/Ot0vYkRT1Mg"):
        if file.endswith('.mp3'):
            total_num_mp3 += 1
        elif file.endswith('.txt'):
            total_num_srt += 1

    return total_num_srt + total_num_mp3 == NUM_SUBTITLES * 2 + 1


def main(is_all_test_success=None):
    success_count=0
    if is_all_test_success is  False:
        print("\033[91m Please check the module name to pass other test!\033[0m")
    else:
        success_count+=1
        print("##########################################################################\n")
        # test download and cropped files
        print("\033[94mChecking to crop and download files...\033[0m")
        if _download_crop_files() is False:
            print("\033[91mSomething went wrong while downloading or cropping files. \033[0m")
        else:
            success_count+=1
            print("\033[0;32;49mDownloading and cropping are SUCCESSFULLY done!"
                  "SUCCESSFULLY PASSED\033[0m")
        print("##########################################################################\n")

        print("\033[94mChecking the total number of downloaded and cropped files...\033[0m")
        if test_total_number_of_cropped_files() is False:
            print("\033[91mThe total number of files does not equal to real total files number. \033[0m")
        else:
            success_count+=1
            print("\033[0;32;49mThe total number of files is EQUAL. SUCCESSFULLY PASSED!\033[0m")
        # test the random subtitle between real sub and downloaded file
        print("##########################################################################\n")

        print("\033[94mComparing the random text which is downloaded "
              "in the previous test with the real subtitle...\033[0m")
        if read_test_srt_file() is False:
            print("\033[91m.FAILED! Two compared subtitles aren't equal.\033[0m")
        else:
            success_count+=1
            print("\033[0;32;49m Two compared subtitles are EQUAL. SUCCESSFULLY PASSED\033[0m")
        print("##########################################################################\n")
    
    if success_count<4:
        raise Exception("FAILED! Not PASSED " +str(4-success_count)+" tests.")


if __name__ == '__main__':
    main(is_all_test_success)
