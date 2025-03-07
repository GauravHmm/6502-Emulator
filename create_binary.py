def create_test_binary():
    program = [
        0xA9, 0x42,  # LDA #$42
        0xAA,        # TAX
        0x00         # BRK
    ]
    with open("instructions.bin", "wb") as f:
        f.write(bytes(program))
    print("Created test binary file: instructions.bin")
if __name__ == "__main__":
    create_test_binary()

