class CPU:
    def __init__(self,pc=0):
        self.reset(pc)
    def reset(self,pc=0):
        PC=0xFFFC
        SP=0x00FF
        C=Z=I=D=B=V=N=0
        A=X=Y=0
    def Fetch(Cycles,mem):
        ins=mem[PC]
        PC+=1
        Cycles-=1
        return ins
    def Execute(mem,Cycles=2):
        while(Cycles>0):
            ins=Fetch(Cycles,mem)
class Memory:
    def __init__(self):
        self.mem = [0]*64*1024
              