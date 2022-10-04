f = open("input_simulator.txt", "r")
fromAssem = []
if(f== None):
    print("error: can't open file", f)
else:
    for x in f:
        fromAssem.append(x)
        # print(x)
    f.close
  
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
    b = bin(dec[0]).replace("0b", "")
    machine_c.append(b)
   
print(dec) 
print(machine_c)

reg = [0,0,0,0,0,0,0,0] #set all reg to 0 in first


#printing
#output
for i in range(len(fromAssem)): #loop showing what's inside mem
    print(f"memory[{i}]={fromAssem[i]}")


stage = []
stage.append(1) #Just for testing printer

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

