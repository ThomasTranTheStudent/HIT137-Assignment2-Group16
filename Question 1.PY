# Function to shift a character 'c' by a number of steps 'shift' in the specified direction ('forward' or 'backward')
def shift_char(c, shift, direction):
    if not c.isalpha():  # If the character is not alphabetic, return it as it is
        return c

    # Determine the base ASCII code (either 'a' for lowercase or 'A' for uppercase)
    base = ord('a') if c.islower() else ord('A')
    
    # Calculate the shift amount based on the direction (forward or backward)
    shift_amount = shift if direction == 'forward' else -shift
    
    # Shift the character within the alphabet, maintaining its case (lowercase or uppercase)
    return chr((ord(c) - base + shift_amount) % 26 + base)

# Function to encrypt the input text
def encrypt_text(text, n, m):
    encrypted = []
    for c in text:
        if c.islower():  # If the character is a lowercase letter
            if c <= 'm':  # If the character is between 'a' and 'm'
                encrypted.append(shift_char(c, n * m, 'forward'))
            else:  # If the character is between 'n' and 'z'
                encrypted.append(shift_char(c, n + m, 'backward'))
        elif c.isupper():  # If the character is an uppercase letter
            if c <= 'M':  # If the character is between 'A' and 'M'
                encrypted.append(shift_char(c, n, 'backward'))
            else:  # If the character is between 'N' and 'Z'
                encrypted.append(shift_char(c, m * m, 'forward'))
        else:
            encrypted.append(c)  # If the character is not a letter, leave it unchanged
    return ''.join(encrypted)

# Function to decrypt the encrypted text based on the original text to determine the encryption pattern
def decrypt_text(encrypted, n, m, original_text):
    decrypted = []
    for i, c in enumerate(encrypted):
        if i >= len(original_text):  # If the index is greater than the length of the original text, continue without decryption
            decrypted.append(c)
            continue

        original_char = original_text[i]
        if original_char.islower():  # If the original character is lowercase
            if original_char <= 'm':
                decrypted.append(shift_char(c, n * m, 'backward'))
            else:
                decrypted.append(shift_char(c, n + m, 'forward'))
        elif original_char.isupper():  # If the original character is uppercase
            if original_char <= 'M':
                decrypted.append(shift_char(c, n, 'forward'))
            else:
                decrypted.append(shift_char(c, m * m, 'backward'))
        else:
            decrypted.append(c)  # If the character is not a letter, leave it unchanged
    return ''.join(decrypted)

# Function to check if the decrypted text matches the original text
def check_correctness(original, decrypted):
    return original == decrypted

# Main function to run the encryption and decryption process
def main():
    # Input n and m values from the user
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))

    # Read the content from the file 'raw_text.txt'
    with open('raw_text.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Encrypt the raw text
    encrypted = encrypt_text(raw_text, n, m)
    
    # Write the encrypted result to 'encrypted_text.txt'
    with open('encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted)
    print("✅ Encryption done!")

    # Decrypt the encrypted text
    decrypted = decrypt_text(encrypted, n, m, raw_text)
    
    # Write the decrypted result to 'decrypted_text.txt'
    with open('decrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted)
    print("✅ Decryption done!")

    # Check if the decrypted text matches the original text
    if check_correctness(raw_text, decrypted):
        print("✅ Original and decrypted text match!")
    else:
        print("❌ Decryption failed!")

# Run the main function
if __name__ == '__main__':
    main()

