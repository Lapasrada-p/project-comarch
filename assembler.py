import sys
#### Still don't have checking reg after instruct ####

fname = "tester.txt"
assem = []

try:
    f = open(fname, 'r')
except OSError:
    print ("Could not open/read file:", fname)
    sys.exit(1) #catch error: if it doesn't have a file, exit 1

with f:
    for x in f:
        assem.append(x)
        # print(x)
    f.close()

machine_c = []
dec = []
label = []
opcode = []
ins = ['add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'halt', 'noop']
rs = []
rt = []
rd = []
f = []

for i in range(len(assem)): #loop assemble code
    x = assem[i].split() 
    # print(x)
    
    if x[0] in ins: #In case code doesn't have label
        if x[0] =='add' or x[0] =='nand' :
            if x[0] =='add':
                opcode.append('000')
            elif x[0] == 'nand':
                opcode.append('001')
            
            
            #why use this got invalid syntax ;-;
            # match x[0]:
            #     case 'add':
            #         opcode.append('000')
            #     case 'nand':
            #         opcode.append('001')
            #     case 'lw':
            #         opcode.append('010')
            #     case 'sw':
            #         opcode.append('011')
            #     case 'beq':
            #         opcode.append('100')
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)

            # print(rd[i])
        elif x[0] =='lw' or x[0] =='sw' or x[0] =='beq':
            if x[0] == 'lw':
                opcode.append('010')
            elif x[0] == 'sw':
                opcode.append('011')
            elif x[0] == 'beq':
                opcode.append('100')

            # print('x3', x[3])

            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)

        elif x[0] == 'jalr':
            opcode.append('101')
            rs.append(x[1])
            rd.append(None)
            rt.append(x[2])
            f.append(None)
        elif x[0] == 'halt' or x[0]=='noop':
            if x[0] =='halt':
                opcode.append('110')
            elif x[0] == 'noop':
                opcode.append('111')

            # match x[0]:
            #     case 'halt':
            #         opcode.append('110')
            #     case 'noop':
            #         opcode.append('111')

            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)
        
        label.append(None) #Set label[i] is null

    elif len(x[0]) >6 or x[0][0].isdigit() or x[0] in label: #Check label
        print("Error: Label error")
        sys.exit(1)
    elif(len(x)) == 1 :
        print("Error: Label undefine")
        sys.exit(1)
    else:
        label.append(x[0])
        if x[1] =='add' or x[1] =='nand' :
            if x[1] =='add':
                opcode.append('000')
            elif x[1] == 'nand':
                opcode.append('001')
            
            
            # match x[1]:
            #     case 'add':
            #         opcode.append('000')
            #     case 'nand':
            #         opcode.append('001')
            #     case 'lw':
            #         opcode.append('010')
            #     case 'sw':
            #         opcode.append('011')
            #     case 'beq':
            #         opcode.append('100')
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)
        elif x[1] =='lw' or x[1] =='sw' or x[1] =='beq':
            if x[1] == 'lw':
                opcode.append('010')
            elif x[1] == 'sw':
                opcode.append('011')
            elif x[1] == 'beq':
                opcode.append('100')

            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)
        
        #JALR
        elif x[1] == 'jalr':
            opcode.append('101')
            rs.append(x[2])
            rd.append(None)
            rt.append(x[3])
            f.append(None)

        #halt or noop
        elif x[1] == 'halt' or x[1]=='noop':
            if x[1] =='halt':
                opcode.append('110')
            elif x[1] == 'noop':
                opcode.append('111')
            # match x[1]:
            #     case 'halt':
            #         opcode.append('110')
            #     case 'noop':
            #         opcode.append('111')
            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)

        #.fill
        elif x[1] == '.fill':
            # print(rd)
            # print(label)
            # print(len(x))
            if(len(x) < 3):
                print("Error")
                sys.exit(1)

            opcode.append(None)
            rs.append(None)
            rt.append(None)
            rd.append(None)
            # print('x[2]',x[2])
            # print(x[2] in label)

             
            if x[2] in label and not(x[0] in rd):     #if  after .fill is in label
                index = label.index(x[2])       #finding index of x[2] in label list
                f.append(index)
                for j in range(len(rd)):
                    if rd[j] == x[0]:
                        rd[j] = i
            elif x[0] in rd and not(x[2] in label):      #if label have the same name in rd
                for j in range(len(rd)):
                    if rd[j] == x[0]:
                        rd[j] = i
                f.append(x[2])
                # print(2)
            elif x[0] in rd and x[2] in label:      
                l_index = label.index(x[2])         
                # print("index", l_index)
                # r_index = rd.index(x[0])

                f.append(l_index)
                for j in range(len(rd)):
                    if rd[j] == x[0]:
                        rd[j] = i
                        # rd[j] = l_index
                # print(3)
            else:
                f.append(x[2])
                # print(4)
        else:
            print("Opcode Error: Do not have this instruction")
            sys.exit(1)



# print("rd",rd)
# print("f",f)

#checking beq if rd is symbolic
for i in range(len(rd)):
    print(f)
    s = str(rd[i])
    if(rd[i] != None):
        if s[0].isalpha():
                    if rd[i] in label:
                        ind = label.index(rd[i])
                        # print("ind",ind)
                        # print("i",i)
                        rd[i] = ind - i -1 
                       
                        # print("rd",rd[i])
                    


w = open("input_simulator.txt","w")     #open filewriting for simulator


for i in range(len(assem)): #loop for generate bin and dec
    
    # print(i)
    isFill = False
    
    # R-type
    if(opcode[i] == '000' or opcode[i] == '001'):
        # print(rd[i][0])
        s = str(rd[i])
        if s[0].isalpha():
            print("Cannot use symbolic in rd")
            sys.exit(1)

        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)
        rd[i] =  bin(int(rd[i]))[2:].zfill(3)

        # print(rs[i],rt[i],rd[i])
        m = opcode[i]+rs[i]+rt[i]+'0000000000000'+rd[i]
        # print(m)
        
    # I-Type
    elif (opcode[i] == '010' or opcode[i] == '011' or opcode[i] == '100') :
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)
        # print('i',i ,'rd',rd[i])
        if int(rd[i])>32767 or int(rd[i])<-32768:
            print(f"Error: In address {i}, offsetField is more than 16 bit")
            sys.exit(1)
        elif(int(rd[i])<0):
            rd[i] =  bin(int(rd[i])&0b1111111111111111)[2:].zfill(16)
        else:     
            rd[i] =  bin(int(rd[i]))[2:].zfill(16)

        m = opcode[i]+rs[i]+rt[i]+rd[i]
        # print(m)
        
    # J-Type
    elif (opcode[i] == '101') :
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)

        # print(rs[i],rt[i],rd[i])
        m = opcode[i]+rs[i]+rt[i]+'0000000000000000'
        # print(m)
    
    # O-Type
    elif (opcode[i] == '110' or opcode[i] == '111'):
        m= opcode[i] + '0000000000000000000000'

    else:
        # print(f)
        isFill = True
        m = f[i]


    machine_c.append((m)) 
    if(isFill == False):
        decimal = int(machine_c[i], 2)
    else:
        decimal = machine_c[i]
    dec.append(decimal)
    
    
    
# print(label)


#Printing
for i in range(len(assem)):
    print(rs[i],rt[i],rd[i])   #easy for checking
    print(f"(address {i}): {dec[i]}" ) #print decimal of code line by line
    

    #write decimal in file for simulator
    w.write(str(dec[i]))
    if i != len(assem)-1:
        w.write('\n')

w.close()
sys.exit(0) #end program