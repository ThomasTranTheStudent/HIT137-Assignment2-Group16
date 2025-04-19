def shift_char(c, shift, direction):
    """
    Shift a character forward or backward in the alphabet.
    """
    if not c.isalpha():
        return c

    base = ord('a') if c.islower() else ord('A')
    shift_amount = shift if direction == 'forward' else -shift
    return chr((ord(c) - base + shift_amount) % 26 + base)


def encrypt_text(text, n, m):
    """
    Encrypt text using custom shifting rules based on character case and value.
    """
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


def decrypt_text(encrypted, n, m, original_text):
    """
    Decrypt text using original text as a guide to reverse the encryption.
    """
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


def check_correctness(original, decrypted):
    """
    Check if decrypted text matches the original.
    """
    return original == decrypted


def main():
    """
    Run the encryption/decryption process with file I/O.
    """
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))

    # Read raw text
    with open('raw_text.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Encrypt
    encrypted = encrypt_text(raw_text, n, m)
    with open('encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted)
    print("✅ Encryption done!")

    # Decrypt
    decrypted = decrypt_text(encrypted, n, m, raw_text)
    with open('decrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted)
    print("✅ Decryption done!")

    # Check correctness
    if check_correctness(raw_text, decrypted):
        print("✅ Original and decrypted text match!")
    else:
        print("❌ Decryption failed!")


if __name__ == '__main__':
    main()
