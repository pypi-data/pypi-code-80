#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8




HOST = ""
PORT = 0
ini = False
s = None
_pickle = None

def init(h,p,__pickle):

        global HOST
        global PORT
        global init
        ini = True
        global s
        global _pickle
        
        _pickle = __pickle
        HOST = h
        PORT = p

   
    
def start_server(host,port,debug = False):

            global s
            global _pickle
        
            if s == None:
                raise RuntimeError("Not initialised. Call remfunc.init(host,port) first.")
                
               
        
            if debug == True:
                print ("Server is Listening.....")
            HOST = host
            PORT = port
            
            s.bind((HOST, PORT))
            s.listen(1)

            while True:

                try:



                    conn, addr = s.accept()
                    if debug == True:
                        print ('Connected by', addr)

                    size = None
                    #conn.send(bytes("OK","utf-8"))
                    #data_variable = pickle.loads(data)

                    if debug == True:
                        print ("Waiting for data of size: " + str(int(size.decode("utf-8"))))
                        size = conn.recv(4096)

                    #conn.send(pickle.dumps(size))

                    data = conn.recv(int(size.decode("utf-8")))

                    code = _pickle.loads(data)
                    block = '\n'.join(code.splitlines()[:-1])

                    result = None
                    try:

                        result = exec(code)

                    except Exception as e:

                        result = e




                    resultsize = str(len(_pickle.dumps(result,-1)))

                    conn.send(_pickle.dumps(resultsize))

                    conn.send(result)

                    if debug == True:
                        print ('Data received from client')


                except:
                    if debug == True:
                        print("ERROR OR CLIENT DONE")
                    pass


   

    



                
       
            
def do(code):
            
           
            
            
            global HOST
            global PORT
            global ini
            global s
            global _pickle
                
            if ini == False:
                
                raise RuntimeError("Client not initialized, run remfunc.init(HOST,PORT) first. You only need to do this once.")
            
           
            
            try:
                
                s.connect((HOST,PORT))
                
            except:
                
                raise RuntimeError("Can not connect to server. Is it running? Is host " + HOST + " and port " + str(PORT) + " correct?")
                
                
            datatosend = code
            
            size = str(len(_pickle.dumbs(datatosend,-1)))
            
            rsize = None
            result = None
            
            try:
                
                s.send(bytes(size,"utf-8"))
                
                
            except:
                
                raise RuntimeError("Error sending code size")
                
            try:
                
                s.send(_pickle.dumps(datatosend))
                
            except:
                
                raise RuntimeError("Error sending code")
              
            
            while True:
                
                try:
                    
                    rsize = s.recv(4096)
                    
                except:
                    
                    raise RuntimeError("Error recieving result size")
                   
                
                try:
                    
                    result = _pickle.loads(conn.recv(int(rsize.decode("utf-8"))))
                    return result
                
                except:
                    
                    raise RuntimeError("Error recieving result")
                    
                
                    
                    





