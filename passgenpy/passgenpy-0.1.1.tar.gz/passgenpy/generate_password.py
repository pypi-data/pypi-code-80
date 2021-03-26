import random
    
def gen_pass(length: int, password: str) -> str:
    """Generates pseudo random password from a set of characters"""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols = "!@#$%^&*~_-+"
    length //= 2
    for i in range(length):
        password += "".join(f"{random.choice(letters)}{random.choice(symbols)}")
    
    return password

if __name__ == "__main__":
    gen_pass(0, "")
