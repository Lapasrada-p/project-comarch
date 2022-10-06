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
        # print(x)
    f.close()


# print(fromAssem)
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
   
print(dec) 
print(machine_c)

reg = [0,0,0,0,0,0,0,0] #set all reg to 0 in first

stage = []
stage.append(1) #Just for testing printer


for i in machine_c:
    #add
    if i[0:3] == '000' :
        print("add")
    #nand
    elif i[0:3] == '001' :
        print("nand")
    #lw
    elif i[0:3] == '010':
        print("lw")
    #sw
    elif i[0:3] == '011':
        print("sw")
    #beq    
    elif i[0:3] == '100':
        print("beq")
    #jalr
    elif i[0:3] == '101':
        print("jalr")
    #halt
    elif i[0:3] == '110':
        print("halt")
        break;
    #noop
    elif i[0:3] == '111':
        #Do nothing
        print("noop")


    

#printing
#output
for i in range(len(fromAssem)): #loop showing what's inside mem
    print(f"memory[{i}]={fromAssem[i]}")


for i in range (len(stage)):
    print("@@@")
    print("state:")
    print(f"\tpc {i}")
    print("\tmemory: ")
    for i in range(len(fromAssem)):
        print(f"\t\tmem[ {i} ] {fromAssem[i]}")
    print("\tregisters:")
    for i in range(len(reg)):
        print(f"\t\treg[ {i} ] {reg[i]}")
print("end state")
print("")

sys.exit(0) #end program

