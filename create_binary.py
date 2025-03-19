def create_test_binary():
    program = [
    0xA9, 0x10,  # LDA #$10
    0x8D, 0x00, 0x02,  # STA $0200
    0xA2, 0x05,  # LDX #$05
    0xCA,  # DEX
    0xD0, 0xFD,  #  BNE -5 (Loop back to `DEX`)
    0x48,  # PHA
    0xA9, 0x00,  # LDA #$00
    0x68,  # PLA
    0x4C, 0x11, 0x06,  #  JMP $0611
    0xA9, 0x20,  #  LDA #$20
    0xAA,  # TAX
    0x00  # BRK
    ]
    with open("instructions.bin","wb") as f:
        f.write(bytes(program))
    print("Created test binary file: instructions.bin")
if __name__=="__main__":
    create_test_binary()