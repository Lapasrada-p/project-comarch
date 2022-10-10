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
    print(x)
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

reg = [0,0,0,0,0,0,0,0] #set all reg to 0 in first


    

#printing
#output
for i in range(len(fromAssem)): #loop showing what's inside mem
    print(f"memory[{i}]={fromAssem[i]}")

i = 0
count = 0
while( i < len(fromAssem)):
    # print('i',i)
    print()
    print("@@@")
    print("state:")
    print(f"\tpc {i}")
    print("\tmemory: ")
    for j in range(len(fromAssem)):
        print(f"\t\tmem[ {j} ] {fromAssem[j]}")
    print("\tregisters:")
    for k in range(len(reg)):
        print(f"\t\treg[ {k} ] {reg[k]}")
    print("end state")
    print()

    # print(i)
    opcode = machine_c[i][0:3] 
    # print(opcode)
    #add
    if opcode == '000' :
        # print("add")
        rs = int(machine_c[i][3:6],2)
        rt = int(machine_c[i][6:9],2)
        rd = int(machine_c[i][22:25],2)
        reg[rd] = reg[rs] + reg[rt]

    #nand
    elif opcode == '001' :
        print("nand")
        rs = int(machine_c[i][3:6],2)
        rt = int(machine_c[i][6:9],2)
        rd = int(machine_c[i][22:25],2)

        n1 = bin(reg[rs])
        n2 = bin(reg[rt])
        nand = not(n1 and n2)
        print(nand)
        reg[rd] = nand

    #lw
    elif opcode == '010':
        # print("lw")
        rs = int(machine_c[i][3:6],2)
        rt = int(machine_c[i][6:9],2)
        offset = int(machine_c[i][9:25],2)
        
        addr = int(offset) + reg[rs]
        # print('offset',offset)
        reg[rt] = int(fromAssem[addr]) #store reg of rt to pc that give from value in [offset+rs]
       

    #sw
    elif opcode == '011':
        print("sw")

    #beq    
    elif opcode == '100':
        # print("beq")
        rs = int(machine_c[i][3:6],2)
        rt = int(machine_c[i][6:9],2)
        if(machine_c[i][9] == '1'):
            m = machine_c[i][9:25] 
            
            o = (int(m,2)^0b1111111111111111) +1
            m = o*(-1)
            
            # print(o)  
            offset = m
        else:
            offset = int(machine_c[i][9:25],2)

        # print('offset',offset)
        if reg[rs] == reg[rt]:
            # print('yes')
            # print(i)
            i = i + offset
            # print(i)

    #jalr
    elif opcode == '101':
        print("jalr")
    #halt
    elif opcode == '110':
        print("halt")
        break
    #noop
    elif opcode == '111':
        #Do nothing
        print("noop")

    i+=1
    count += 1

print('machine halted')
print(f'total of {count+1} instructions executed')
print('final state of machine:')
print()
print("@@@")
print("state:")
print(f"\tpc {i+1}")
print("\tmemory: ")
for j in range(len(fromAssem)):
    print(f"\t\tmem[ {j} ] {fromAssem[j]}")
print("\tregisters:")
for k in range(len(reg)):
    print(f"\t\treg[ {k} ] {reg[k]}")
print("end state")

sys.exit(0) #end program

