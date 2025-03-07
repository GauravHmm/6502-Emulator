class CPU:
    def __init__(self):
        self.reset()
    def reset(self):
        self.PC=0xFFFC
        self.SP=0xFF
        self.C=self.Z=self.I=self.D=self.B=self.V=self.N=0
        self.A=self.X=self.Y=0
        self.cycles=0
    def fetch(self,memory):
        ins=memory.read(self.PC)
        self.PC+=1
        self.cycles-=1
        return ins
    def execute(self,memory,cycles=2):
        self.cycles=cycles
        while(cycles>0):
            opcode=self.fetch(memory)
            cycles-=1
            if opcode==0xA9: #LDA
                self.A=self.fetch(memory)
                cycles-=1
            elif opcode == 0xAA: # TAX
                self.X = self.A
                self.cycles -= 1
            elif opcode==0x00:
                print("Execution Halted")
                break
            else:
                print(f"Unknown opcode: {hex(opcode)}")
class Memory:
    def __init__(self):
        self.mem = [0]*64*1024
    def read(self,address):
        address = address & 0xFFFF
        return self.mem[address]
    def write(self,address,value):
        address = address & 0xFFFF
        value = value & 0xFF
        self.mem[address]=value   
    def loadbin(self, filename, start_address=0x0000):
        try:
            with open(filename, 'rb') as f:
                binary_data = f.read()
                for i, byte in enumerate(binary_data):
                    self.mem[start_address + i] = byte
            print(f"Loaded {filename} at {start_address}")
            return True
        except Exception as e:
            print(f"Error loading binary file: {e}")
            return False
if __name__=="__main__":
    memory=Memory()
    cpu=CPU()
    memory.loadbin("instructions.bin")
    cpu.execute(memory)            