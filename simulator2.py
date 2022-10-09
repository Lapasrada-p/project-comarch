import sys
from dataclasses import dataclass,field
# set var-----------------------------------------------
fromAssem = []
MEMORY = []
REG =[0]*8
fname = "input_simulator.txt"

@dataclass
class stateStruct:
    pc: int = field(default=0)
    mem: list[int] = field(default_factory=list)
    reg: list[int] = field(default_factory=list)
    numMemory: int = field(default=0)
   
state = stateStruct(0,MEMORY,REG)
# read file-------------------------------------------- 
try:
    f = open(fname, 'r')
except OSError:
    print ("Could not open/read file:", fname)
    sys.exit(1) #catch error: if it doesn't have a file, exit 1

with f:
    for x in f:
        fromAssem.append(x)
        state.mem.append(x)
        state.numMemory += 1
    f.close()

print(state)
    
# function of each instruction-----------------------------
def add(rs,rt,rd):
    ans = int(rs) + int(rt)                                   
    state.reg[rd] = int(ans)                                   
    return 'add'            

def nand(rs,rt,rD):                                     
    return 'nand'                                            

def lw(rs,regB,rd):                               
    return 'lw'                                          

def sw(rs,rt,rd):                           
    return 'sw'

def beq(rs,rt,rd):
    return 'beq'                                      

def jalr(rs,rd):
    return 'jalr'   
                                           
def halt():
    return 'halt'

def noop():
    return 'noop'
# compute------------------------------------------------------------
def compute(opcode,regA,regB,rD):
    if(opcode == '000'):    #add
        rs = state.reg[regA] 
        rt = state.reg[regB] 
        return add(rs,rt,rD)
    elif(opcode == '001'):  #nand
        rs = state.reg[regA] 
        rt = state.reg[regB] 
        return nand(rs,rt,rD)
    elif(opcode == '010'):  #lw
        rs = state.reg[regA] 
        return lw(rs,regB,rD)
    elif(opcode == '011'):  #sw
        rs = state.reg[regA] 
        rt = state.reg[regB] 
        return sw(rs,rt,rD) 
    elif(opcode == '100'):  #beq
        rs = state.reg[regA] 
        rt = state.reg[regB] 
        return beq(rs,rt,rD)
    elif(opcode == '101'):  #jalr
        rs = state.reg[regA] 
        rd = state.reg[regB] 
        return jalr(rs,regB)
    elif(opcode == '110'):  #halt
        return halt()
    elif(opcode == '111'):  #noop
        return noop()
# --------------------------------------------------------------
def printStruct(x):
    print('@@@\nstate:')
    print('\tpc ' + str(state.pc))
    print('\tmemory:')
    for i in range(len(MEMORY)): 
        print('\t\t\tmem[ {} ] {}'.format(i,int(MEMORY[i])))
    print('\tregisters:')
    for i in range(len(REG)):    
        print('\t\t\treg[ {} ] {}'.format(i,state.reg[i]))
    print('end state\n')
    return ''
# --------------------------------------------------------------
def Simulator():
    count_instruction = 0
    while(state.pc != state.numMemory):
        dec = int(state.mem[state.pc])
        i = bin(dec).replace("0b", "")
        if i[0:3] == '000' :
            # print("add")
            opcode = '000'
            regA = int(i[3:6],2)
            regB = int(i[6:9],2)
            regC = int(i[22:25],2)
        #nand
        elif i[0:3] == '001' :
            # print("nand")
            opcode = '001'
            regA = int(i[3:6],2)
            regB = int(i[6:9],2)
            regC = int(i[22:25],2)
        #lw
        elif i[0:3] == '010':
            # print("lw")
            opcode = '010'
            regA = int(i[3:6],2)
            regB = int(i[6:9],2)
            regC = int(i[9:25],2)  #offset
        #sw
        elif i[0:3] == '011':
            # print("sw")
            opcode = '011'
            regA = int(i[3:6],2)
            regB = int(i[6:9],2)
            regC = int(i[9:25],2) #offset
        #beq    
        elif i[0:3] == '100':
            # print("beq")
            opcode =  '100'
            regA = int(i[3:6],2)
            regB = int(i[6:9],2)
            regC = int(i[9:25],2)  #offset
        #jalr
        elif i[0:3] == '101':
            # print("jalr")
            opcode = '101'
            regA = int(i[0:3],2)
            regB = int(i[6:9],2)
            regC = 0
        #halt
        elif i[0:3] == '110':
            # print("halt")
            opcode = '110'
            regA = 0
            regB = 0
            regC = 0
            # break;
        #noop
        elif i[0:3] == '111':
            #Do nothing
            # print("noop")
            opcode = '111'
            regA = 0
            regB = 0
            regC = 0
            
        # printStruct(state.pc)
        result = compute(opcode,regA,regB,regC)
        count_instruction+=1
        if(result == 'jalr'):
            state.pc +=0
        elif(result == 'noop'):
            state.pc +=1
        elif(result == 'halt'):
            state.pc +=1
# Simulator()



