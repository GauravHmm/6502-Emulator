class CPU:
    def __init__(self):
        self.PC=0 #Program Counter
        self.SP=0xFF #Stack Pointer
        self.C=self.Z=self.I=self.D=self.B=self.V=self.N=0 #Flags
        self.A=self.X=self.Y=0 #Registers
        self.cycles=0 #Execution cycle count
    def reset(self,memory):
        low=memory.read(0xFFFC)
        high=memory.read(0xFFFD)
        self.PC=(high<<8)|low
        print(f"CPU Reset - Start PC=${self.PC:04X}")
    def fetch(self,memory):
        ins=memory.read(self.PC)
        self.PC+=1
        return ins
    def immediate(self,memory):
        value=self.fetch(memory)
        return value
    def absolute(self,memory):
        lo=self.fetch(memory)
        hi=self.fetch(memory)
        return (hi << 8) | lo
    def execute(self,memory,cycles=2):
        self.cycles=cycles
        while(cycles>0):
            opcode=self.fetch(memory)
            cycles-=1
            #Instructions
            if opcode==0xA9: #LDA Immediate
                self.A=self.fetch(memory)
                self.update_flags(self.A)
                print(f"LDA #{self.A:02X}")
                cycles-=1
            elif opcode==0xA2: #LDX
                self.X=self.fetch(memory)
                print(f"LDX #{self.X:02X}")
                cycles-=1
            elif opcode==0xA0: #LDY
                self.Y=self.fetch(memory)
                print(f"LDY #{self.Y:02X}")
            elif opcode==0xAA: # TAX
                self.X=self.A
                self.update_flags(self.X)
                self.cycles-=1
                print(f"TAX (X={self.X:02X})")
            elif opcode==0xA8: #TAY
                self.Y=self.A
                self.cycles-=1
                print(f"TAY (Y={self.Y:02X})")
            elif opcode==0x98: #TYA
                self.A=self.Y
                self.cycles-=1
                print(f"TYA (A={self.A:02X})")
            elif opcode==0x8A: #TXA
                self.A=self.X
                self.cycles-=1
                print(f"TXA (A={self.A:02X})")
            elif opcode==0x8D:  #STA 
                address=self.absolute(memory)
                memory.write(address,self.A)
                self.cycles-=3
                print(f"STA ${address:04X}")
            elif opcode==0x48:  #PHA 
                self.push_stack(memory,self.A)
                self.cycles -= 2
                print(f"PHA (Pushed A = {self.A:02X})")
            elif opcode==0x68:  #PLA 
                self.A=self.pop_stack(memory)
                self.update_flags(self.A)
                self.cycles-=3  
                print(f"PLA (Pulled A = {self.A:02X})")
            elif opcode==0x4C:  #JMP Absolute
                address=self.absolute(memory)
                self.PC=address  
                self.cycles-=2
                print(f"JMP ${address:04X}")
            elif opcode==0xca: #DEX
                self.X=(self.X-1) &0xFF
                self.Z=1 if self.X==0 else 0
                self.N=1 if (self.X&0x80) else 0
                print(f"DEX (X={self.X:02X})")
            elif opcode==0xD0:  #BNE
                offset=self.fetch(memory)
                if offset>127: #convert to signed
                    offset-=256
                if self.Z==0:  
                    new_pc=(self.PC+offset)&0xFFFF  
                    self.cycles-=1  
                    if (self.PC&0xFF00)!=(new_pc&0xFF00):  
                        self.cycles-=1  
                    self.PC=new_pc  
                    print(f"BNE{offset:+}->PC=${self.PC:04X}") 
            elif opcode==0x00:
                print("Execution Halted")
                break
            else:
                print(f"Unknown opcode: {hex(opcode)}")
        return cycles-self.cycles
    def push_stack(self,memory,value):
        memory.write(0x0100+self.SP,value)
        self.SP=(self.SP-1)&0xFF
    def pop_stack(self,memory):
        self.SP=(self.SP+1)&0xFF
        return memory.read(0x0100+self.SP)
    def update_flags(self,value):
        self.Z=1 if value==0 else 0
        self.N=1 if (value&0x80) else 0
class Memory:
    def __init__(self):
        self.mem=[0]*64*1024
    def read(self,address):
        address=address&0xFFFF
        return self.mem[address]
    def write(self,address,value):
        address=address&0xFFFF
        value=value&0xFF
        self.mem[address]=value
    def reset_vector(self,address):
        self.write(0xFFFC,address&0xFF)  
        self.write(0xFFFD,(address>>8)&0xFF)  
        print(f"Reset vector set to ${address:04X}")
    def loadbin(self,filename,start_address=0x0000):
        try:
            with open(filename,'rb') as f:
                binary_data=f.read()
                for i, byte in enumerate(binary_data):
                    self.mem[(start_address + i)&0xFFFF]=byte
            print(f"Loaded {filename} at {start_address}")
            return True
        except Exception as e:
            print(f"Error loading binary file: {e}")
            return False
if __name__=="__main__":
    memory=Memory()
    cpu=CPU()
    if memory.loadbin("instructions.bin",0x0600):
        memory.reset_vector(0x0600)
        cpu.reset(memory)
        cycles_used=cpu.execute(memory,50)
        print(f"Execution completed. Used {cycles_used} cycles.")
        print(f"Final CPU state - A: ${cpu.A:02X}, X: ${cpu.X:02X}, Y: ${cpu.Y:02X}, PC: ${cpu.PC:04X}")      