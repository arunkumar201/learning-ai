import random

digits_set = "0123456789"
special_chars_set = "!@#$%^&*()-_=+[{]};:,.<>/?"
lowercase_set = "abcdefghijklmnopqrstuvwxyz"
uppercase_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_random_password(minLen=8, maxLen=16, digits=True, specialChars=True, lowercase=True, uppercase=True):
    """Generate a random password."""

    if(minLen>maxLen):
        raise ValueError("Minimum length cannot be greater than maximum length.")
    if(not digits and not specialChars and not lowercase and not uppercase):
        raise ValueError("At least one criteria should be enabled for password generation.")
    
    length = random.randint(minLen, maxLen)
    password = []

    if digits:
        password.append(random.choice(digits_set))
    if specialChars:
        password.append(random.choice(special_chars_set))
    if lowercase:
        password.append(random.choice(lowercase_set))
    if uppercase:
        password.append(random.choice(uppercase_set))

    while len(password) < length:
        password.append(random.choice(digits_set + special_chars_set + lowercase_set + uppercase_set))

    # Shuffle the password to make it more secure
    random.shuffle(password)
    return ''.join(password)

def check_password_strength(password):
    """Check the strength of the given password."""
    length_criteria = len(password) >= 8
    digit_criteria = any(char in digits_set for char in password)
    special_char_criteria = any(char in special_chars_set for char in password)
    lowercase_criteria = any(char in lowercase_set for char in password)
    uppercase_criteria = any(char in uppercase_set for char in password)

    if all([length_criteria, digit_criteria, special_char_criteria, lowercase_criteria, uppercase_criteria]):
        return "Strong"
    elif length_criteria and (digit_criteria or special_char_criteria) and (lowercase_criteria or uppercase_criteria):
        return "Moderate"
    else:
        return "Weak"

# run inside the main
if __name__ == "__main__":
    # take the user inputs for password criteria
 try:
    minLen = int(input("Enter minimum length of password: "))
    maxLen = int(input("Enter maximum length of password: "))
    digits = input("Include digits in the password (y/n)? ").lower() == 'y'
    specialChars = input("Include special characters in the password (y/n)? ")
    specialChars = specialChars.lower() == 'n'if False else True
    lowercase = input("Include lowercase letters in the password (y/n)? ")
    lowercase = lowercase.lower() == 'n' if False else True
    uppercase = input("Include uppercase letters in the password (y/n)? ")
    uppercase = uppercase.lower() == 'n' if False else True
    # generate the password
    password = generate_random_password(minLen, maxLen, digits, specialChars, lowercase, uppercase)
    print("Generated password:", password, len(password))

    # check the password strength
    strength = check_password_strength(password)
    print("Password strength:", strength)
 except Exception as e:
    print("Error:", e)
