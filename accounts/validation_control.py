import random, string

def generate_token():
    # Define length of token
    length = 50

    # Initialize empty string
    random_string = ""

    # Loop to generate token
    for _ in range(length):
        random_char = random.choice(string.ascii_letters + string.digits)
        random_string += random_char

    return(random_string)
