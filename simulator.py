import sys

fromAssem = []
fname = "input_simulator.txt"

try:
    f = open(fname, 'r')
except OSError:
    print ("Could not open/read file:", fname)
    sys.exit(1) #catch error: if it doesn't have a file, exit 1

with f:
    for x in f:
        fromAssem.append(x)
    f.close()

dec = []
# #convert dec to bin
for i in range(len(fromAssem)):
    x = fromAssem[i].split()
    # print(x)
    dec.append(int(x[0]))

# print(dec)
# print(type(dec[0]))
# print(bin(dec[0]).replace("0b", ""))

machine_c = []
for i in range(len(dec)):
    b = bin(dec[i]).replace("0b", "").zfill(25) #แก้ให้เป็น 25 bit
    machine_c.append(b)
   
# print(dec) 
# print(machine_c)


mem = []
reg = [0,0,0,0,0,0,0,0] #set all reg to 0 in first

for i in range(len(fromAssem)): #loop showing what's inside mem
    mem.append(fromAssem[i])
    

#printing
#output
for i in range(len(mem)): #loop for showing what's inside mem
    print(f"memory[{i}]={mem[i]}")

pc = 0
numMemory = len(mem)
count = 0


w = open("output_simulator.txt","w")    #For writing output

while( pc < numMemory):
    # print()
    # print("@@@")
    # print("state:")
    # print(f"\tpc {pc}")
    # print("\tmemory: ")
    # for j in range(numMemory):
    #     print(f"\t\tmem[ {j} ] {mem[j]}")
    # print("\tregisters:")
    # for k in range(len(reg)):
    #     print(f"\t\treg[ {k} ] {reg[k]}")
    # print("end state")
    # print()

    # print('reg1',reg[1])

    #For writing output
    w.write('\n')
    w.write("@@@\n")
    w.write("state:\n")
    w.write(f"\tpc {pc}\n")
    w.write("\tmemory: \n")
    for j in range(numMemory):
        w.write(f"\t\tmem[ {j} ] {mem[j]}\n")
    w.write("\tregisters:\n")
    for k in range(len(reg)):
        w.write(f"\t\treg[ {k} ] {reg[k]}\n")
    w.write("end state\n")

    

    opcode = machine_c[pc][0:3] 


    #### Add ####
    if opcode == '000' :
        # print("add")
        rs = int(machine_c[pc][3:6],2)
        rt = int(machine_c[pc][6:9],2)
        rd = int(machine_c[pc][22:25],2)
        reg[rd] = reg[rs] + reg[rt]
        pc+=1

    #### Nand ####
    elif opcode == '001' :
        print("nand")
        s = ''
        rs = int(machine_c[pc][3:6],2)
        rt = int(machine_c[pc][6:9],2)
        rd = int(machine_c[pc][22:25],2)
        
        n1 = bin(reg[rs])[2:].zfill(16)
        # print(bin(reg[rt]))
   
        n2 = bin(reg[rt])[2:].zfill(16)
        # print(n1,n2)

        s = ''
        for i in range(len(n1)):        #loop each character, nand each other
            if n1[i] == '1' and n2[i] == '1':
                # nand.append('0')
                s = s+'0'
            else:
            # nand.append('1')
                s = s+'1'

        reg[rd]= int(s,2)       #bin to dec then save to reg[rd]
        # print('n1',n1)
        # print('n2',n2)
        # print('s ',s)

        pc+=1

    #### Lw ####
    elif opcode == '010':
        # print("lw")
        rs = int(machine_c[pc][3:6],2)
        rt = int(machine_c[pc][6:9],2)
        offset = int(machine_c[pc][9:25],2)
        
        addr = int(offset) + reg[rs]        #Finding address
        # print(addr)
        # print('offset',offset)
        reg[rt] = int(mem[addr])    #store reg of rt to pc that give from value in [offset+rs]
        pc+=1
       

    #### Sw ####
    elif opcode == '011':
        print("sw")
        rs = int(machine_c[pc][3:6],2)
        rt = int(machine_c[pc][6:9],2)
        offset = int(machine_c[pc][9:25],2)
        
        addr = int(offset) + reg[rs]
        # print('offset',offset)
        # w.write(str(offset))
        
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

    #### Beq ####    
    elif opcode == '100':
        # print("beq")
        rs = int(machine_c[pc][3:6],2)
        rt = int(machine_c[pc][6:9],2)
        #To convert 2s component
        if(machine_c[pc][9] == '1'):    #negative
            m = machine_c[pc][9:25] 
            o = (int(m,2)^0b1111111111111111) +1
            m = o*(-1)
            
            offset = m
        else:                           #positive
            offset = int(machine_c[pc][9:25],2)

        # print('offset',offset)
        if reg[rs] == reg[rt]:
            # print(i)
            pc = pc + 1 + offset    #Set new pc to jump
            # print(i)
        else:
            pc+=1

        # print('pc',pc) 

    #### Jalr ####
    elif opcode == '101':
        print("jalr")
        rs = int(machine_c[pc][3:6],2)
        rt = int(machine_c[pc][6:9],2)
        reg[rt] = pc+1
        if(rs != rt):
            pc = reg[rs]
            
    #### Halt ####
    elif opcode == '110':
        print("halt")
        break

    #### Noop ####
    elif opcode == '111':
        #Do nothing
        print("noop")
        pc+=1

    
    count += 1  #counting instructions executed

print('machine halted')
print(f'total of {count+1} instructions executed')
print('final state of machine:')
print()
print("@@@")
print("state:")
print(f"\tpc {pc+1}")
print("\tmemory: ")
for j in range(numMemory):
    print(f"\t\tmem[ {j} ] {mem[j]}")
print("\tregisters:")
for k in range(len(reg)):
    print(f"\t\treg[ {k} ] {reg[k]}")
print("end state")



w.write('machine halted\n')
w.write(f'total of {count+1} instructions executed\n')
w.write('final state of machine:\n')
w.write('\n')
w.write("@@@\n")
w.write("state:\n")
w.write(f"\tpc {pc+1}\n")
w.write("\tmemory: \n")
for j in range(numMemory):
    w.write(f"\t\tmem[ {j} ] {mem[j]}\n")
w.write("\tregisters:\n")
for k in range(len(reg)):
    w.write(f"\t\treg[ {k} ] {reg[k]}\n")
w.write("end state\n")

sys.exit(0) #end program

