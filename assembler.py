
f = open("tester.txt", "r")
assem = []
if(f== None):
    print("error: can't open file", f)
else:
    for x in f:
        assem.append(x)
        # print(x)
    f.close


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
    n = 0
    print(i)

    if x[0] in ins: #In case code doesn't have label
        if x[0] =='add':
            opcode.append('000')
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)
        elif x[0] == 'nand':
            opcode.append('001')
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)
        elif x[0] == 'lw':
            opcode.append('010')
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)
        elif x[0] == 'sw':
            opcode.append('011')
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)
        elif x[0] == 'beq':
            opcode.append('100')
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)
            if rd[i].isalpha():
                if rd[i] in label:
                    ind = label.index(rd[i])
                    print(ind)
                    rd[i] = (-1)*ind-1
        elif x[0] == 'jarl':
            opcode.append('101')
            rs.append(x[1])
            rt.append(None)
            rd.append(x[2])
            f.append(None)
        elif x[0] == 'halt':
            opcode.append('110')
            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)
        elif x[0] == 'noop':
            opcode.append('111')
            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)
        
        label.append(None) #Set label[i] is null

    elif len(x[0]) >6 or x[0][0].isdigit() : #Check label
        print("error: Label error")
        break
    else:
        label.append(x[0])
        if x[1] =='add':
            opcode.append('000')
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)
        elif x[1] == 'nand':
            opcode.append('001')
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)
        elif x[1] == 'lw':
            opcode.append('010')
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)
        elif x[1] == 'sw':
            opcode.append('011')
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)
        elif x[1] == 'beq':
            opcode.append('100')
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            if rd[i].isalpha():
                if rd[i] in label:
                    ind = label.index(rd[i])
                    
                    rd[i] = (-1)*ind-1
            f.append(None)
        elif x[1] == 'jarl':
            opcode.append('101')
            rs.append(x[2])
            rt.append(None)
            rd.append(x[3])
            f.append(None)
        elif x[1] == 'halt':
            opcode.append('110')
            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)
        elif x[1] == 'noop':
            opcode.append('111')
            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)
        elif x[1] == '.fill':
            print(rd)
            print(label)
            opcode.append(None)
            rs.append(None)
            rt.append(None)
            rd.append(None)
            index = rd.index(label[i])
            rd[index] = x[2]
            f.append(x[2])
            
        n = 1


w = open("input_simulator.txt","w")     #open filewriting for simulator

for i in range(len(assem)):
    # print(i)
    isFill = False
    # R-type
    if(opcode[i] == '000' or opcode[i] == '001'):
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)
        rd[i] =  bin(int(rd[i]))[2:].zfill(3)

        # print(rs[i],rt[i],rd[i])
        m = opcode[i]+rs[i]+rt[i]+'0000000000000'+rd[i]
        # print(m)
        
    # I-Type
    elif (opcode[i] == '010' or opcode[i] == '011' or opcode[i] == '100') :
        # rs.append(bin(int(x[n+1]))[2:].zfill(3))
        # rt.append(bin(int(x[n+2]))[2:].zfill(3))
        # rd.append(bin(int(x[n+3]))[2:].zfill(16)) #still not 2's
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)
        if(int(rd[i])<0):
            rd[i] =  bin(int(rd[i])&0b1111111111111111)[2:].zfill(16)
        else:     
            rd[i] =  bin(int(rd[i]))[2:].zfill(16)

        # print(rs[i],rt[i],rd[i])
        m = opcode[i]+rs[i]+rt[i]+rd[i]
        # print(m)
        
    # J-Type
    elif (opcode[i] == '101') :
        # rs.append(bin(int(x[n+1]))[2:].zfill(3))
        # rd.append(bin(int(x[n+2]))[2:].zfill(3))
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rd[i] =  bin(int(rd[i]))[2:].zfill(3)

        # print(rs[i],rt[i],rd[i])
        m = opcode[i]+rs[i]+rd[i]+'0000000000000000'
        # print(m)
    #
    # O-Type
    elif (opcode[i] == '110' or opcode[i] == '111'):
        m=opcode[i] + '0000000000000000000000'

    else:
        # print(f)
        isFill = True
        m = f[i]

    # # R-type
    # if(opcode[i] == '000' or opcode[i] == '001'):
    #     rs.append(bin(int(x[n+1]))[2:].zfill(3))
    #     rt.append(bin(int(x[n+2]))[2:].zfill(3))
    #     rd.append(bin(int(x[n+3]))[2:].zfill(3)) 

    #     # print(rs[i],rt[i],rd[i])
    #     m = opcode[i]+rs[i]+rt[i]+'0000000000000'+rd[i]
    #     # print(m)
        
    # # I-Type
    # elif (opcode[i] == '010' or opcode[i] == '011' or opcode[i] == '100') :
    #     rs.append(bin(int(x[n+1]))[2:].zfill(3))
    #     rt.append(bin(int(x[n+2]))[2:].zfill(3))
    #     rd.append(bin(int(x[n+3]))[2:].zfill(16)) #still not 2's

    #     # print(rs[i],rt[i],rd[i])
    #     m = opcode[i]+rs[i]+rt[i]+rd[i]
    #     # print(m)
        
    # # J-Type
    # elif (opcode[i] == '101') :
    #     rs.append(bin(int(x[n+1]))[2:].zfill(3))
    #     rd.append(bin(int(x[n+2]))[2:].zfill(3))

    #     # print(rs[i],rt[i],rd[i])
    #     m = opcode[i]+rs[i]+rd[i]+'0000000000000000'
    #     # print(m)
    # #
    # # O-Type
    # elif (opcode[i] == '110' or opcode[i] == '111'):
    #     m=opcode[i] + '0000000000000000000000'

    print(rs[i],rt[i],rd[i])   

    machine_c.append((m)) 
    if(isFill == False):
        decimal = int(machine_c[i], 2)
    else:
        decimal = machine_c[i]
    dec.append(decimal)
    
    print(f"(address {i}): {dec[i]}" ) #print decimal of code line by line
    
    # print(dec[i])
    #write decimal in file for simulator
    w.write(str(dec[i]))
    if i != len(assem)-1:
        w.write('\n')
    
# print(label)
w.close()