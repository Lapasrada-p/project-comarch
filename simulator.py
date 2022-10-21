import sys

fromAssem = []
fname = "input_simulator.txt"

#Read file
try:
    f = open(fname, 'r')
except OSError:
    print ("Could not open/read file:", fname)
    sys.exit(1) #catch error: if it doesn't have a file, exit 1

with f:
    for x in f:
        y = x.rstrip()      #For deleting /n in line
        fromAssem.append(int(y))
    f.close()

## stateStruct ##
pc = 0
mem = []
reg = [0,0,0,0,0,0,0,0] #set all reg to 0 at first
numMemory = 0

## PrintState ##
def printState():
    w.write('\n')
    w.write("@@@\n")
    w.write("state:\n")
    w.write(f"\tpc {pc}\n")
    w.write("\tmemory: \n")
    for j in range(numMemory):
        w.write(f"\t\t\tmem[ {j} ] {mem[j]}\n")
    w.write("\tregisters:\n")
    for k in range(len(reg)):
        w.write(f"\t\t\treg[ {k} ] {reg[k]}\n")
    w.write("end state\n")    


machine_c = []      #For collecting machine code
for i in range(len(fromAssem)):
    b = bin(fromAssem[i]).replace("0b", "").zfill(25) #Convert decimal to binary
    machine_c.append(b)
   


for i in range(len(fromAssem)): #loop fromAssem[]
    mem.append(fromAssem[i])        #memory[i] = address[i]
    
w = open("output_simulator.txt","w")        #open file to write


numMemory = len(mem)
count = 0   #For counting executed instruction


#printing
#output
for i in range(numMemory): #loop for writing what's inside mem
    w.write(f"memory[{i}]={mem[i]}\n")
w.write("\n")


while( pc < numMemory):
   
    printState() 

    ## instruction executes ##
    opcode = machine_c[pc][0:3]         #Opcode = bits 22-24


    # Add
    if opcode == '000' :
        #Convert binary to decimal
        rs = int(machine_c[pc][3:6],2)      #bits 21-19
        rt = int(machine_c[pc][6:9],2)      #bits 18-16
        rd = int(machine_c[pc][22:25],2)    #bits 2-0
        reg[rd] = reg[rs] + reg[rt]         #value in rd = value in rs+rd
        pc+=1   #Next pc

    # Nand 
    elif opcode == '001' :
        # print("nand")
        s = ''      #String for answer of nand
        #Convert binary to decimal
        rs = int(machine_c[pc][3:6],2)      #bits 21-19
        rt = int(machine_c[pc][6:9],2)      #bits 18-16
        rd = int(machine_c[pc][22:25],2)    #bits 2-0
        
        #Changing decimal to 16 bit binary 
        if(int(reg[rs])<0):     #If value in reg[rs] is negative number
            n1 =  bin((reg[rs])&0b1111111111111111)[2:].zfill(16)
        else:     #positive
            n1 = bin(reg[rs])[2:].zfill(16)

        #Changing decimal to 16 bit binary      
        if(reg[rt]<0):     #If value in reg[rt] is negative number
            n2 =  bin((reg[rt])&0b1111111111111111)[2:].zfill(16)
        else:     #positive
            n2 = bin(reg[rt])[2:].zfill(16)
   
        for i in range(len(n1)):        #loop each character and nand each other
            if n1[i] == '1' and n2[i] == '1':       #If reg[rs][i] = 1 and reg[rt][i] = 1
                s = s+'0'       # ~(1&1)
            else:
                s = s+'1'

        reg[rd] = int(s,2)       #Convert binary to decimal then save to reg[rd]

        pc+=1

    # Lw 
    elif opcode == '010':
        # Convert binary to decimal
        rs = int(machine_c[pc][3:6],2)      #bits 21-19
        rt = int(machine_c[pc][6:9],2)      #bits 18-16
        offset = int(machine_c[pc][9:25],2) #bits 15-0
        
        addr = int(offset) + reg[rs]        #Finding address by offsetField + value in regA (reg[rs])

        reg[rt] = int(mem[addr])    #write pc that give from value in [offset+rs] in reg[rt]

        pc+=1
       

    # Sw 
    elif opcode == '011':
        #Convert binary to decimal
        rs = int(machine_c[pc][3:6],2)      #bits 21-19
        rt = int(machine_c[pc][6:9],2)      #bits 18-16
        offset = int(machine_c[pc][9:25],2) #bits 15-0
        
        addr = int(offset) + reg[rs]
        
        if(addr < numMemory):
            mem[addr] = reg[rt] #store reg of rt to pc that give from value in [offset+rs]
        else:
            for i in range(numMemory,addr+1):   #loop to add new memory
                if i == addr:
                    mem.append(reg[rt]) #add more memory to store reg[rt]
                else:
                    mem.append(0)
                numMemory+=1

        pc+=1

    # Beq     
    elif opcode == '100':
        # Convert decimal to binary
        rs = int(machine_c[pc][3:6],2)      #bits 21-19
        rt = int(machine_c[pc][6:9],2)      #bits 18-16

        # Convert 2's complement
        if(machine_c[pc][9] == '1'):        #negative
            m = machine_c[pc][9:25]         #bits 15-0
            o = (int(m,2)^0b1111111111111111) +1
            m = o*(-1)
            
            offset = m
        else:                           #positive
            offset = int(machine_c[pc][9:25],2) #bits 15-0

        if reg[rs] == reg[rt]:      #if value in reg[rs] and reg[rt] is the same
            pc = pc + 1 + offset    #Set new pc to jump
        else:
            pc+=1

    # Jalr
    elif opcode == '101':
        #Convert binary to decimal
        rs = int(machine_c[pc][3:6],2)      #bits 21-19
        rt = int(machine_c[pc][6:9],2)      #bits 18-16
        reg[rt] = pc+1      #reg[rt] = next line
        if(rs != rt):       #if regA != regB 
            pc = reg[rs]    #set new pc = value in reg[rs]
            
    # Halt
    elif opcode == '110':
        # print("halt")
        pc+=1
        break

    # Noop 
    elif opcode == '111':
        #Do nothing
        # print("noop")
        pc+=1   #Go to next pc

    count += 1  #counting instructions that was executed



w.write('machine halted\n')
w.write(f'total of {count+1} instructions executed\n')
w.write('final state of machine:\n')

#For printing final state of machine
printState()

sys.exit(0) #end program

