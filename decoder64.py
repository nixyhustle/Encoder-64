#!/usr/bin/env python3
import sys

def decode_base64(encoded: str) -> bytes:
    # Base64 alphabet and reverse mapping dictionary
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    char_to_value = {ch: idx for idx, ch in enumerate(alphabet)}
    result = bytearray()
    
    # Remove any extraneous whitespace/newlines
    encoded = encoded.strip()
    
    # Process the encoded string in groups of 4 characters
    for i in range(0, len(encoded), 4):
        chunk = encoded[i:i+4]
        pad = chunk.count('=')  # Count how many '=' padding characters are in the group
        
        # Convert each character to its 6-bit integer value;
        # for padding characters, use 0.
        values = []
        for ch in chunk:
            if ch == '=':
                values.append(0)
            else:
                values.append(char_to_value[ch])
        # Ensure the chunk is 4 elements long (should be by spec)
        if len(values) < 4:
            values += [0] * (4 - len(values))
        
        # Combine the four 6-bit values into one 24-bit integer
        n = (values[0] << 18) | (values[1] << 12) | (values[2] << 6) | values[3]
        
        # Extract the three bytes from the 24-bit number
        b1 = (n >> 16) & 0xFF
        b2 = (n >> 8) & 0xFF
        b3 = n & 0xFF
        
        # Append the appropriate number of bytes depending on the padding
        if pad == 0:
            result.extend([b1, b2, b3])
        elif pad == 1:
            result.extend([b1, b2])
        elif pad == 2:
            result.extend([b1])
    return bytes(result)

def main():
    if len(sys.argv) != 3:
        print("Usage: python decode_manual.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read the Base64 encoded file as text
    with open(input_file, "r") as f:
        encoded = f.read()
    
    # Decode the Base64 text into binary data
    decoded = decode_base64(encoded)
    
    # Write the binary data to the output file
    with open(output_file, "wb") as f:
        f.write(decoded)

if __name__ == "__main__":
    main()

