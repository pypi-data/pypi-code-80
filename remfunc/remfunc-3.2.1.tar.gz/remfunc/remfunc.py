#!/usr/bin/env python
# coding: utf-8

# In[2]:



HOST = ""
PORT = 0
ini = False


def init(_host,_port):

        global HOST
        global PORT
        global ini
        ini = True

        HOST = _host
        PORT = _port

   
    
def start_server(debug = False):

            import pickle, socket
            global HOST
            global PORT
            if ini == False:
                
                raise RuntimeError("Server not initialized, run remfunc.init(HOST,PORT) first. You only need to do this once.")
            
            if debug == True:
                print ("Server is Listening.....")
           
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

                    code = pickle.loads(data)
                    block = '\n'.join(code.splitlines()[:-1])

                    result = None
                    try:

                        result = exec(code)

                    except Exception as e:

                        result = e




                    resultsize = str(len(pickle.dumps(result,-1)))

                    conn.send(pickle.dumps(resultsize))

                    conn.send(result)

                    if debug == True:
                        print ('Data received from client')


                except Exception as g:
                    if debug == True:
                        print("ERROR OR CLIENT DONE")
                        print(g)
                        resultsize = str(len(pickle.dumps(g,-1)))

                        conn.send(pickle.dumps(resultsize))

                        conn.send(result)
                        pass


   

    



                
       
            
def do(code):
            
           
            
            import pickle, socket
            global HOST
            global PORT
            global ini
           
                
            if ini == False:
                
                raise RuntimeError("Client not initialized, run remfunc.init(HOST,PORT) first. You only need to do this once.")
            
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            
            try:
                
                s.connect((HOST,PORT))
                
            except:
                
                raise RuntimeError("Can not connect to server. Is it running? Is host " + HOST + " and port " + str(PORT) + " correct?")
                
                
            datatosend = code
            
            size = str(len(pickle.dumps(datatosend,-1)))
            
            rsize = None
            result = None
            
            try:
                
                s.send(bytes(size,"utf-8"))
                
                
            except:
                
                raise RuntimeError("Error sending code size")
                
            try:
                
                s.send(pickle.dumps(datatosend))
                
            except:
                
                raise RuntimeError("Error sending code")
              
            
            while True:
                
                try:
                    
                    rsize = s.recv(4096)
                    
                except:
                    
                    raise RuntimeError("Error recieving result size")
                   
                
                try:
                    
                    result = pickle.loads(conn.recv(int(rsize.decode("utf-8"))))
                    return result
                
                except:
                    
                    raise RuntimeError("Error recieving result")
                    
                


# In[ ]:





# In[ ]:




