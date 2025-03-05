class CPU:
    def __init__(self):
        self.reset()
    def reset(self):
        self.PC=0xFFFC
        self.SP=0x00FF
        self.C=self.Z=self.I=self.D=self.B=self.V=self.N=0
        self.A=self.X=self.Y=0
    def fetch(self,memory):
        ins=memory.read(self.PC)
        self.PC+=1
        self.cycles-=1
        return ins
    def execute(self,memory,cycles=2):
        while(cycles>0):
            opcode=self.fetch(memory)
            cycles-=1
            if opcode==0xA9:
                self.A=self.fetch(memory)
                cycles-=1
            elif opcode==0x00:
                print("Execution Halted")
                break
            else:
                print(f"Unknown opcode: {hex(opcode)}")
class Memory:
    def __init__(self):
        self.mem = [0]*64*1024
    def read(self,address):
        return self.mem[address]
    def write(self,address,value):
        self.mem[address]=value & 0xFF   
    def loadbin(self,filename,start_address=):
        with open(filename,'rb') as f:
            binary_data=f.read()
            self.mem[start_address:start_address+len(binary_data)]=list(binary_data)
if __name__=="__main__":
    memory=Memory()
    cpu=CPU()
    cpu.execute(memory)            