class file:

    def __init__(self,filename,*separator):   # * symbol before separator makes it optional variable for user while creating the object (also it allows more than one sparator values)
        self.filename=filename
        self.separator=separator
        f=open(self.filename,"r+")
        lineno=0
        for lns in f.readlines():
            if not lns[0:1]=="#":
                lineno+=1
        self.lines=lineno #len(f.readlines())
       # print(len(self.lines))
        f.close()
        
    def read(self,colArgs,*operator):
        lineIndex=0
        f=open(self.filename,"r+")
        lines=f.readlines()
        if len(self.separator)!=0:
            sep=self.separator[0]
        else:
            sep=" "
        lineTot=len(lines)
        for ln in lines:
            if not ln[0:1]=="#":
                a=ln.split(sep)
                for i in range(len(a)):
                    try:
                        a[i]=float(a[i])
                    except:
                        pass
                colArgs.append(a)    
        f.close()
        if not len(operator)==0:
            if (operator[0]=="l/c") or (operator[0]=="line/col"):
                pass
            else:
                opCol=[]
                [opCol.append([]) for ax in range(len(colArgs[0]))] 
                if (operator[0]=="av") or (operator[0]=="average"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        opCol[i]=sum(opCol[i])/len(opCol[i])
                if (operator[0]=="sm") or (operator[0]=="sum"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        opCol[i]=sum(opCol[i])
                if (operator[0]=="sd") or (operator[0]=="sigma"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i]**2)
                        opCol[i]=(sum(opCol[i])/len(opCol[i]))**0.5
                if (operator[0]=="mx") or (operator[0]=="maximum"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        opCol[i]=max(opCol[i])
                if (operator[0]=="mn") or (operator[0]=="minumum"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):
                            if not type(colArgs[j][i])==str:
                                opCol[i].append(colArgs[j][i])
                        opCol[i]=min(opCol[i])
                if (operator[0]=="c/l") or (operator[0]=="col/line"):
                    for i in range(len(opCol)):
                        for j in range(len(colArgs)):                        
                            opCol[i].append(colArgs[j][i])
                
                colArgs.clear()
                for item in opCol:
                    colArgs.append(item)
        #print(colArgs)
        return colArgs
            
        
    """def lines:
        f=open(self.filename,"r+")
        lines=f.readlines()
        return"""  
    