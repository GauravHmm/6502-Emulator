class CPU:
    def __init__(self,PC=0):
        self.reset(PC)
    def reset(self,PC=0):
        self.PC=0xFFFC
        self.SP=0x00FF
        self.C=self.Z=self.I=self.D=self.B=self.V=self.N=0
        self.A=self.X=self.Y=0
    def Fetch(Cycles,mem):
        ins=mem[PC]
        PC+=1
        Cycles-=1
        return ins
    def Execute(self,mem,Cycles=2):
        while(Cycles>0):
            self.ins=self.Fetch(Cycles,mem)
class Memory:
    def __init__(self):
        self.mem = [0]*64*1024
              