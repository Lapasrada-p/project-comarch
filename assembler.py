import sys

fname = "multiply.txt"
assem = []      #collect assambly

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
opcode = []     #collect opcode
ins = ['add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'halt', 'noop']
rs = []     #collect rs
rt = []     #collect rt
rd = []     #collect rd or offset
f = []      #collect value in .fill

for i in range(len(assem)): #loop assembly code
    x = assem[i].split() 
    
    if x[0] in ins:     #In case code doesn't have label
        #checking R-type
        if x[0] =='add' or x[0] =='nand' :      
            if x[0] =='add':
                opcode.append('000')
            elif x[0] == 'nand':
                opcode.append('001')
            
            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])
            f.append(None)

        #checking I-type
        elif x[0] =='lw' or x[0] =='sw' or x[0] =='beq':        
            if x[0] == 'lw':
                opcode.append('010')
            elif x[0] == 'sw':
                opcode.append('011')
            elif x[0] == 'beq':
                opcode.append('100')

            rs.append(x[1])
            rt.append(x[2])
            rd.append(x[3])     #append offfset
            f.append(None)

        #checking J-type
        elif x[0] == 'jalr':        
            opcode.append('101')
            rs.append(x[1])
            rd.append(None)         #null bcuz j-type doesn't have rd or offset
            rt.append(x[2])
            f.append(None)
        
        #checking O-type
        elif x[0] == 'halt' or x[0]=='noop':        
            if x[0] =='halt':
                opcode.append('110')
            elif x[0] == 'noop':
                opcode.append('111')

            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)
        
        label.append(None) #Set label[i] is null

    elif len(x[0]) >6 or x[0][0].isdigit() or x[0] in label: #Check label more than 6 charactor, or starting char is number
        # print("Error: Label error")
        sys.exit(1)
    elif(len(x)) == 1 :     #checking pc has only label
        print("Error: Label undefine")
        sys.exit(1)
    else:       #In case present pc have label
        label.append(x[0])
        #R-type
        if x[1] =='add' or x[1] =='nand' :
            if x[1] =='add':
                opcode.append('000')
            elif x[1] == 'nand':
                opcode.append('001')
            
            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])
            f.append(None)

        #I-type
        elif x[1] =='lw' or x[1] =='sw' or x[1] =='beq':
            if x[1] == 'lw':
                opcode.append('010')
            elif x[1] == 'sw':
                opcode.append('011')
            elif x[1] == 'beq':
                opcode.append('100')

            rs.append(x[2])
            rt.append(x[3])
            rd.append(x[4])     #append offset
            f.append(None)
        
        #JALR
        elif x[1] == 'jalr':
            opcode.append('101')
            rs.append(x[2])
            rd.append(None)
            rt.append(x[3])
            f.append(None)

        #halt or noop O-type
        elif x[1] == 'halt' or x[1]=='noop':
            if x[1] =='halt':
                opcode.append('110')
            elif x[1] == 'noop':
                opcode.append('111')

            rs.append(None)
            rt.append(None)
            rd.append(None)
            f.append(None)

        #.fill
        elif x[1] == '.fill':
            if(len(x) < 3):
                print("Error")
                sys.exit(1)

            opcode.append(None)
            rs.append(None)
            rt.append(None)
            rd.append(None)
             
            if x[2] in label and not(x[0] in rd):     #if after .fill is in label and doesn't have in rd[]
                index = label.index(x[2])       #finding index of .fill's value in label list
                f.append(index)                 #add index of .fill's value in label to .fill list
        
            elif x[0] in rd and not(x[2] in label):      #if label have the same name in rd[] and .fill's value isn't in label
                for j in range(len(rd)):        #loop in rd list 
                    if rd[j] == x[0]:           #if offset in rd is same as label
                        rd[j] = i               #change offset from symbolic to present address
                f.append(x[2])
                
            elif x[0] in rd and x[2] in label:      #if rd/offset have value as same as label and .fill's value is in label
                l_index = label.index(x[2])         #find index of .fill's value that's in label list 

                f.append(l_index)
                for j in range(len(rd)):
                    if rd[j] == x[0]:
                        rd[j] = i
                        
            else:
                f.append(x[2])

        else:       #In case pc have other instruction
            print("Opcode Error: Do not have this instruction")
            sys.exit(1)


#checking beq if rd is symbolic
for i in range(len(rd)):        
    s = str(rd[i])
    if(rd[i] != None):
        if s[0].isalpha():      #if offsetField is symbolic
                    if rd[i] in label:      #if offset is in label
                        ind = label.index(rd[i])        #find index that offset has the same name as label[]
                        rd[i] = ind - i -1      #edit offset
                       
                    
w = open("input_simulator.txt","w")     #open file writing for simulator


for i in range(len(assem)): #loop for generate bin and dec
    
    isFill = False
    
    # R-type
    if(opcode[i] == '000' or opcode[i] == '001'):

        s = str(rd[i])
        if s[0].isalpha():      #checking rd is symbolic
            print("Cannot use symbolic in rd of R-type")
            sys.exit(1)

        #Changing decimal to 3 bit binary 
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)   
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)
        rd[i] =  bin(int(rd[i]))[2:].zfill(3)

        m = opcode[i]+rs[i]+rt[i]+'0000000000000'+rd[i]
        
    # I-Type
    elif (opcode[i] == '010' or opcode[i] == '011' or opcode[i] == '100') :
        #Changing decimal to 3 bit binary
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)

        if int(rd[i])>32767 or int(rd[i])<-32768:
            print(f"Error: In address {i}, offsetField is more than 16 bit")
            sys.exit(1)
        elif(int(rd[i])<0):     #If offset is negative number
            #Changing decimal to 16 bit binary
            rd[i] =  bin(int(rd[i])&0b1111111111111111)[2:].zfill(16)
        else:     #If offset is pos
            rd[i] =  bin(int(rd[i]))[2:].zfill(16)

        m = opcode[i]+rs[i]+rt[i]+rd[i]

        
    # J-Type
    elif (opcode[i] == '101') :
        #Changing decimal to 3 bit binary
        rs[i] =  bin(int(rs[i]))[2:].zfill(3)
        rt[i] =  bin(int(rt[i]))[2:].zfill(3)

        m = opcode[i]+rs[i]+rt[i]+'0000000000000000'
    
    # O-Type
    elif (opcode[i] == '110' or opcode[i] == '111'):
        m= opcode[i] + '0000000000000000000000'

    # .fill
    else:
        isFill = True
        m = f[i]


    machine_c.append((m)) 
    if(isFill == False):        #instruction is not .fill
        decimal = int(machine_c[i], 2)      #Convert bin to dec
    else:
        decimal = machine_c[i]
    dec.append(decimal)
    

#Printing
for i in range(len(assem)):
    # print(rs[i],rt[i],rd[i])   #easy for checking
    print(f"(address {i}): {dec[i]}" ) #print decimal of code line by line
    
    #write decimal in file for simulator
    w.write(str(dec[i]))
    if i != len(assem)-1:
        w.write('\n')

w.close()       #close writer
sys.exit(0) #end program