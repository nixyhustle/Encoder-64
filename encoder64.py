#!/usr/bin/env python3

import sys

def encode_base64(data: bytes) -> str:
    # Base64 alphabet
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = []
    
    # Process input data in 3-byte chunks
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        pad = 3 - len(chunk)  # number of missing bytes in this chunk
        if pad:
            # Pad the chunk with zero bytes if it's less than 3 bytes
            chunk += b'\x00' * pad
        
        # Combine the three bytes into a 24-bit number
        n = (chunk[0] << 16) + (chunk[1] << 8) + chunk[2]
        
        # Split the 24 bits into four 6-bit values and map them to characters
        indices = [(n >> 18) & 0x3F, (n >> 12) & 0x3F, (n >> 6) & 0x3F, n & 0x3F]
        for j in range(4):
            # For each padded byte, output an '=' instead of a valid character.
            if j >= 4 - pad:
                result.append('=')
            else:
                result.append(alphabet[indices[j]])
    return ''.join(result)

def main():
    if len(sys.argv) != 3:
        print("Usage: python encode_manual.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read input file in binary mode
    with open(input_file, "rb") as f:
        data = f.read()

    # Encode data to Base64
    encoded = encode_base64(data)
    
    # Write the encoded text to the output file
    with open(output_file, "w") as f:
        f.write(encoded)

if __name__ == "__main__":
    main()

