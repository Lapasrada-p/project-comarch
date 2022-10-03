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