# Function to shift a character 
def shift_char(c, shift, direction):
    if not c.isalpha():  
        return c

    # Determine the base ASCII value (either 'a' or 'A')
    base = ord('a') if c.islower() else ord('A')
    
    # Calculate the shift amount based on the direction (forward or backward)
    shift_amount = shift if direction == 'forward' else -shift
    
    # Shift the character within the alphabet (preserving case - lowercase/uppercase)
    return chr((ord(c) - base + shift_amount) % 26 + base)

# Function to encrypt the given text
def encrypt_text(text, n, m):
    encrypted = []
    for c in text:
        if c.islower():  
            if c <= 'm':  
                encrypted.append(shift_char(c, n * m, 'forward'))
            else:  
                encrypted.append(shift_char(c, n + m, 'backward'))
        elif c.isupper():  
            if c <= 'M':  
                encrypted.append(shift_char(c, n, 'backward'))
            else:  
                encrypted.append(shift_char(c, m * m, 'forward'))
        else:
            encrypted.append(c)  
    return ''.join(encrypted)

# Function to decrypt the encrypted text using the original text to determine the encryption rules
def decrypt_text(encrypted, n, m, original_text):
    decrypted = []
    for i, c in enumerate(encrypted):
        if i >= len(original_text):  
            decrypted.append(c)
            continue

        original_char = original_text[i]
        if original_char.islower():  
            if original_char <= 'm':
                decrypted.append(shift_char(c, n * m, 'backward'))
            else:
                decrypted.append(shift_char(c, n + m, 'forward'))
        elif original_char.isupper():  
            if original_char <= 'M':
                decrypted.append(shift_char(c, n, 'forward'))
            else:
                decrypted.append(shift_char(c, m * m, 'backward'))
        else:
            decrypted.append(c)  
    return ''.join(decrypted)

# Function to check if the decrypted text matches the original text
def check_correctness(original, decrypted):
    return original == decrypted

# Main function
def main():
    # Get input values for n and m
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))

    # Read the original text from 'raw_text.txt'
    with open('raw_text.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Encrypt the original text
    encrypted = encrypt_text(raw_text, n, m)
    
    # Write the encrypted text to 'encrypted_text.txt'
    with open('encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted)
    print("✅ Encryption done!")

    # Decrypt the encrypted text
    decrypted = decrypt_text(encrypted, n, m, raw_text)
    
    # Write the decrypted text to 'decrypted_text.txt'
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
