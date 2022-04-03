def get_random_string(x):
    from string import ascii_lowercase, digits
    from random import choices

    letters_and_digits = ascii_lowercase + digits
    res = ''.join(choices(letters_and_digits, k=x))
    res += ''.join(choices(letters_and_digits, k=x))
    return res