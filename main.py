import numpy as np
import cv2
import base64

def encode_message(img, message):
    # Convert the image to dtype uint8 (0-255) if it's not already
    img = img.astype(np.uint8)

    # Ensure the message length is less than the maximum number of pixels in the image
    max_message_length = img.size // 8
    if len(message) > max_message_length:
        raise ValueError("Message is too long to encode in the image.")

    # Convert the message to binary format
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Initialize variables for keeping track of pixel index and binary message index
    pixel_index = 0
    binary_index = 0

    # Loop through the image pixels and embed the message bits using LSB strategy
    for row in img:
        for pixel in row:
            for channel in range(3):  # Loop through R, G, B channels
                if binary_index < len(binary_message):
                    pixel[channel] &= 0xFE  # Clear the LSB
                    pixel[channel] |= int(binary_message[binary_index])  # Set the LSB to the message bit
                    binary_index += 1
                else:
                    break  # Message embedded, exit loop
            pixel_index += 1
            if binary_index >= len(binary_message):
                break  # Message embedded, exit loop

    # Convert the modified image array to bytes and then to base64
    encoded_image = cv2.imencode('.png', img)[1].tobytes()
    encoded_base64 = base64.b64encode(encoded_image).decode('utf-8')

    return encoded_base64

# Example usage
if __name__ == "__main__":
    # Load an example image as a NumPy array
    img_path = 'example_image.png'
    img = cv2.imread(img_path)

    # Message to hide in the image
    message = "My message"

    # Encode the message in the image using LSB steganography
    encoded_image_base64 = encode_message(img, message)

    print("Encoded image in base64:", encoded_image_base64)
