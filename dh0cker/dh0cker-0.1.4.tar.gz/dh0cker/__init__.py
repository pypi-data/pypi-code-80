import os
import time
import getpass


def get_flag():
	name = getpass.getuser()
	print("\n\nHello " + name + ", I wan't to play a game.\n")
	time.sleep(1)
	answer = input("Let me ask you something. Do you want the flag? Answer Y or N")
	print("\nSorry, wrong answer.\n")
	for i in range(10):
		print(str(i*10) + "% completed...")
		time.sleep(0.5)
	print("\nOoooops! Your files have been encrypted!")
	time.sleep(1)
	print("\nWe will tell you soon about the payment method to decrypt your files")
	time.sleep(2)
	print("\nHa ha ha")
	print("\nBe more careful next time with what you download and execute")
	time.sleep(3)
	print("...")
	time.sleep(2)
	print("\nWell, that was the joke. Now, keep looking for the flag")
	time.sleep(2)
	print("\nYour hard drive is safe, nothing was encrypted")
	time.sleep(2)
	print("\nHopefully you always mistrust what you download from unknown sources ;)\n")
		
	#cuenta atras y decir al final que ha cifrado el disco