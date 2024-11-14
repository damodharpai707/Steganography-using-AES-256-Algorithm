"""-------------------------------------By: Damodhar Pai------------------------------------------------"""
import argparse
import sys
from PIL import Image

def generate_key(password, length=32):
    """Generates a 256-bit (32-byte) key by repeating or truncating the password."""
    password = password.encode()
    return (password * (length // len(password) + 1))[:length]

def xor_encrypt(data, key):
    """Encrypts data using XOR with a 256-bit key."""
    return bytearray(d ^ key[i % len(key)] for i, d in enumerate(data))

def image_to_bytes(image):
    """Convert image to bytes with dimensions."""
    width, height = image.size
    pixels = image.convert("RGBA").tobytes()
    dimension_bytes = width.to_bytes(2, 'big') + height.to_bytes(2, 'big')
    return dimension_bytes + pixels

def bytes_to_image(data):
    """Convert bytes back to image."""
    width = int.from_bytes(data[:2], 'big')
    height = int.from_bytes(data[2:4], 'big')
    pixel_data = data[4:]
    return Image.frombytes("RGBA", (width, height), pixel_data)

def embed_message_in_image(pixels, width, height, message_bytes):
    """Embeds byte-aligned message data into the LSBs of an image's RGB channels."""
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index >= len(message_bytes) * 8:
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

    message_bytes = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        message_bytes.append(byte)

    return message_bytes

def main():
    parser = argparse.ArgumentParser(description="Embed or retrieve an image within another image using LSB steganography.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Save command
    save_parser = subparsers.add_parser("save", help="Embed secret image into cover image.")
    save_parser.add_argument("-i", "--input", required=True, help="Path to the cover image.")
    save_parser.add_argument("-s", "--secret", required=True, help="Path to the secret image.")
    save_parser.add_argument("-o", "--output", required=True, help="Output path for the stego image.")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve an embedded image from a stego image.")
    retrieve_parser.add_argument("-i", "--input", required=True, help="Path to the stego image.")
    retrieve_parser.add_argument("-o", "--output", required=True, help="Output path for extracted image.")

    args = parser.parse_args()

    if args.command == "save":
        try:
            # Load images
            cover_image = Image.open(args.input).convert("RGBA")
            secret_image = Image.open(args.secret).convert("RGBA")
            pixels = cover_image.load()
            
            # Convert secret image to bytes
            secret_bytes = image_to_bytes(secret_image)
            
            # Get password
            password = input("Enter the key password: ")
            confirm_password = input("Confirm the key password: ")
            if password != confirm_password:
                print("Error: Passwords do not match.")
                sys.exit(1)

            # Generate key and encrypt
            key = generate_key(password)
            encrypted_secret = xor_encrypt(secret_bytes, key)

            # Check capacity
            width, height = cover_image.size
            available_bits = width * height * 3
            if len(encrypted_secret) * 8 > available_bits:
                print("Error: Secret image is too large to fit into the cover image.")
                sys.exit(1)

            # Embed encrypted secret in cover image
            embed_message_in_image(pixels, width, height, encrypted_secret)

            # Save stego image
            cover_image.save(args.output, "PNG")
            print(f"Output image '{args.output}' saved with success.")

        except Exception as e:
            print(f"Error during embedding: {str(e)}")
            sys.exit(1)

    elif args.command == "retrieve":
        try:
            # Load stego image
            stego_image = Image.open(args.input).convert("RGBA")
            pixels = stego_image.load()
            width, height = stego_image.size

            # Get password
            password = input("Enter the key password: ")
            key = generate_key(password)

            # Extract header (first 4 bytes) to get dimensions
            header_data = extract_message_from_image(pixels, width, height, 4)
            secret_width = int.from_bytes(header_data[:2], 'big')
            secret_height = int.from_bytes(header_data[2:4], 'big')

            # Calculate total size of secret image data
            total_bytes = 4 + (secret_width * secret_height * 4)  # header + RGBA pixels

            # Extract and decrypt the full message
            encrypted_data = extract_message_from_image(pixels, width, height, total_bytes)
            decrypted_data = xor_encrypt(encrypted_data, key)

            try:
                # Convert decrypted data back to image
                secret_image = bytes_to_image(decrypted_data)
                secret_image.save(args.output)
                print(f"Successfully extracted hidden image to {args.output}")
            except Exception as e:
                print("Error: Invalid password or corrupted data")
                sys.exit(1)

        except Exception as e:
            print(f"Error during extraction: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
