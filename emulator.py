class CPU:
    def __init__(self,pc=0):
        self.reset(pc)
    def reset(self,pc=0):
        PC=0xFFFC
        SP=0x00FF
        C=Z=I=D=B=V=N=0
        A=X=Y=0
           