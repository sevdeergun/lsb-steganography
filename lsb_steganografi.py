from PIL import Image

END_MARKER = "1111111111111110"

def encode(img_path, message, output_path):
    img = Image.open(img_path)
    pixels = list(img.getdata())

    # Convert message to binary + end marker
    binary_msg = ''.join(f"{ord(c):08b}" for c in message) + END_MARKER

    # Check capacity
    if len(binary_msg) > len(pixels):
        raise ValueError("Message is too long to be hidden in this image.")

    new_pixels = []
    i = 0

    for pixel in pixels:
        if i < len(binary_msg):
            r = (pixel[0] & ~1) | int(binary_msg[i])
            i += 1
        else:
            r = pixel[0]

        new_pixels.append((r, *pixel[1:]))

    img.putdata(new_pixels)
    img.save(output_path)

    print("Message successfully encoded into:", output_path)


def decode(img_path):
    img = Image.open(img_path)
    pixels = img.getdata()

    bits = ""

    for pixel in pixels:
        bits += str(pixel[0] & 1)

        if bits.endswith(END_MARKER):
            bits = bits[:-len(END_MARKER)]
            break

    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    message = ''.join(chars)

    return message



def main():
    print("LSB Steganography Tool")
    

    choice = input("Choose operation - Encode (e) / Decode (d): ").lower()

    if choice == "e":
        img = input("Enter image path (PNG recommended): ")
        msg = input("Enter the secret message: ")
        out = input("Enter output image path: ")

        try:
            encode(img, msg, out)
        except Exception as e:
            print("Error:", e)

    elif choice == "d":
        img = input("Enter image path: ")

        try:
            message = decode(img)
            print("Decoded message:", message)
        except Exception as e:
            print("Error:", e)

    else:
        print("Invalid choice. Please select 'e' or 'd'.")


if __name__ == "__main__":
    main()