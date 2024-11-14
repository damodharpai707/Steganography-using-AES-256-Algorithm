import argparse
import sys
from PIL import Image

def generate_key(password, length=32):
    """Generates a 256-bit (32-byte) key by repeating or truncating the password."""
    password = password.encode()  # Ensure password is in bytes
    return (password * (length // len(password) + 1))[:length]  # Repeat or truncate to 32 bytes

def xor_encrypt(data, key):
    """Encrypts data using XOR with a 256-bit key."""
    return bytearray(d ^ key[i % len(key)] for i, d in enumerate(data))

def pad_message(message, block_size=16):
    """Pad the message to a multiple of block_size bytes."""
    padding_length = block_size - (len(message) % block_size)
    padding = bytes([padding_length] * padding_length)
    return message + padding

def unpad_message(padded_message):
    """Remove the padding from the message."""
    padding_length = padded_message[-1]
    if padding_length > len(padded_message):
        raise ValueError("Invalid padding")
    if padded_message[-padding_length:] != bytes([padding_length] * padding_length):
        raise ValueError("Invalid padding")
    return padded_message[:-padding_length]

def embed_message_in_image(pixels, width, height, message_bytes):
    """Embeds byte-aligned message data into the LSBs of an image's RGB channels."""
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index >= len(message_bytes) * 8:  # Stop when message is fully embedded
                return
            r, g, b, a = pixels[x, y]
            if data_index < len(message_bytes) * 8:
                r = (r & 0xFE) | ((message_bytes[data_index // 8] >> (7 - (data_index % 8))) & 1)
                data_index += 1
            if data_index < len(message_bytes) * 8:
                g = (g & 0xFE) | ((message_bytes[data_index // 8] >> (7 - (data_index % 8))) & 1)
                data_index += 1
            if data_index < len(message_bytes) * 8:
                b = (b & 0xFE) | ((message_bytes[data_index // 8] >> (7 - (data_index % 8))) & 1)
                data_index += 1
            pixels[x, y] = (r, g, b, a)

def extract_message_from_image(pixels, width, height, num_bytes):
    """Extracts byte-aligned message data from the LSBs of an image's RGB channels."""
    bits = []
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index >= num_bytes * 8:
                break
            r, g, b, a = pixels[x, y]
            bits.append((r & 1))
            data_index += 1
            if data_index < num_bytes * 8:
                bits.append((g & 1))
                data_index += 1
            if data_index < num_bytes * 8:
                bits.append((b & 1))
                data_index += 1

    # Convert extracted bits to bytes
    message_bytes = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        message_bytes.append(byte)

    return message_bytes

def main():
    parser = argparse.ArgumentParser(description="Embed or retrieve a message in an image using LSB steganography.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for the "save" command
    save_parser = subparsers.add_parser("save", help="Embed a message in an image.")
    save_parser.add_argument("-i", "--input", required=True, help="Path to the cover image.")
    save_parser.add_argument("-m", "--message", required=True, help="Secret message to embed.")
    save_parser.add_argument("-o", "--output", required=True, help="Output path for the stego image.")

    # Sub-parser for the "retrieve" command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve a message from a stego image.")
    retrieve_parser.add_argument("-i", "--input", required=True, help="Path to the stego image.")

    args = parser.parse_args()

    TAG = "SECRET:"  # Known tag for verification

    if args.command == "save":
        # Embedding Process
        input_image_path = args.input
        message = TAG + args.message
        output_image_path = args.output

        # Open cover image
        try:
            cover_image = Image.open(input_image_path)
            cover_image = cover_image.convert("RGBA")
            pixels = cover_image.load()
        except IOError:
            print("Error: Could not open cover image.")
            sys.exit(1)

        # Prompt for password and confirm it
        password = input("Enter the key password: ")
        confirm_password = input("Confirm the key password: ")
        if password != confirm_password:
            print("Error: Passwords do not match.")
            sys.exit(1)

        # Generate a 256-bit key from the confirmed password
        key = generate_key(password)

        # Pad and encrypt the message
        padded_message = pad_message(message.encode())
        encrypted_message = xor_encrypt(padded_message, key)

        # Convert message length to a fixed 4-byte format and prepend to message
        message_length = len(encrypted_message)
        length_bytes = message_length.to_bytes(4, byteorder='big')
        message_bytes = length_bytes + encrypted_message

        # Embed the message in the image
        width, height = cover_image.size
        embed_message_in_image(pixels, width, height, message_bytes)

        # Save the stego image
        cover_image.save(output_image_path, "PNG")
        print(f"Output image '{output_image_path}' saved with success.")

    elif args.command == "retrieve":
        # Extraction Process
        input_image_path = args.input

        try:
            stego_image = Image.open(input_image_path)
            stego_image = stego_image.convert("RGBA")
            pixels = stego_image.load()
        except IOError:
            print("Error: Could not open stego image.")
            sys.exit(1)

        # Prompt for password
        password = input("Enter the key password: ")
        key = generate_key(password)

        # Extract message length (first 4 bytes)
        width, height = stego_image.size
        length_bytes = extract_message_from_image(pixels, width, height, 4)
        message_length = int.from_bytes(length_bytes, byteorder='big')

        # Extract the encrypted message based on the extracted length
        encrypted_message = extract_message_from_image(pixels, width, height, message_length + 4)[4:]  # Skip length bytes
        decrypted_bytes = xor_encrypt(encrypted_message, key)
        
        try:
            unpadded_message = unpad_message(decrypted_bytes)
            # Check for the tag before any further processing
            if unpadded_message.startswith(TAG.encode()):
                # Only decode if the tag is present
                decrypted_message = unpadded_message.decode('utf-8', errors='strict')
                actual_message = decrypted_message[len(TAG):]
                print("Decrypted message:", actual_message)
            else:
                print("Invalid password.")
                sys.exit(1)
        except Exception:
            print("Invalid password.")
            sys.exit(1)

if __name__ == "__main__":
    main()
