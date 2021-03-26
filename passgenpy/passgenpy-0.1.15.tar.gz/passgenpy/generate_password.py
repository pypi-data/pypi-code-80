import random

# special_cases = {
#     "only_letters": 0,
#     "only_symbols": 1,
#     "letters_and_symbols": 2,
# }

def gen_pass(length: int, password: str, **kwargs) -> str:
    """Generates pseudo random password from a set of characters"""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols = "!@#$%^&*~_-+"
    length //= 2
    # for key, value in kwargs.items():
    #     if len(kwargs.items()) == 0:
    #         print([key, value in special_cases] )
    for i in range(length):
        rand_choice = random.randint(0, 1)
        if rand_choice == 0:
            password += "".join(f"{random.choice(letters)}{random.choice(symbols)}")
        else:
            password += "".join(f"{random.choice(symbols)}{random.choice(letters)}")
    return password

if __name__ == "__main__":
    gen_pass(0, "")
