import sys
sys.path.append('../passgenpy/')
from generate_password import gen_pass

passwrd_len = int(input("Enter the length of the password that will be generated:\n"))
passwrd = ""
passwrd = gen_pass(passwrd_len, passwrd) #, special="only_letters")
print(passwrd)
