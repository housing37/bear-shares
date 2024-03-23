hex_string = "0x4e487b710000000000000000000000000000000000000000000000000000000000000032"

# Remove the leading "0x" if present
if hex_string.startswith("0x"):
    hex_string = hex_string[2:]

# Convert hexadecimal string to bytes
hex_bytes = bytes.fromhex(hex_string)

# Decode bytes assuming UTF-8 encoding
decoded_text = hex_bytes.decode("utf-8")

print(decoded_text)
