import json,os,requests,logging
from collections import namedtuple
from json import JSONEncoder

__version__ = "1.0.1"
__author__ = "Melvin Paul Miki"
__credits__ = "Mickie Studioz"

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s |  %(levelname)s |  %(message)s', level=logging.INFO)

class conduit():
    def __init__(mes,endpoint,username,password,device_id,client_id):
        try:
            logging.info("Initializing Instance...")
            mes.json_template = json.loads(open('template.json','r').read())
            mes.endpoint = endpoint
            mes.json_template['source']['client_id']=client_id
            mes.json_template['source']['workstation']['station']=device_id
            mes.json_template['source']['employee']= username
            mes.json_template['source']['password']= password
            logging.info("Instance Ready!")
            
        except Exception as e:
            logging.error("Instance Creation error!")
            logging.error(e)
            

    def mes_login(mes):
        try:
            mes.json_template['transactions'] = []
            mes.json_template['transactions'].append({"unit": {"unit_id":"ABCD1234" ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            posting = requests.post(mes.endpoint, json=mes.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                if "cannot log in" in reply["transaction_responses"][0]["scanned_unit"]["status"]["message"]:
                    logging.info("Login Failed!")
                    return False
                else:
                    logging.info("Login Success!")
                    return True
            else:
                return False
                logging.error("Conduit Communication Error")

        except Exception as e:
            logging.error(e)

    
    def mes_PassUnit(mes,unitSerial):
        try:
            mes.json_template['transactions'] = []
            mes.json_template['transactions'].append({"unit": {"unit_id":"ABCD1234" ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})

            posting = requests.post(mes.endpoint, json=mes.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                logging.info(unitSerial + " : " + reply["transaction_responses"][0]["scanned_unit"]["status"]["message"])
                return reply["transaction_responses"][0]["scanned_unit"]["status"]["code"] + " :: " + reply["transaction_responses"][0]["scanned_unit"]["status"]["message"]

            else:
                return False
                logging.error("Conduit Communication Error")

        except Exception as e:
            logging.error(e)

    def mes_ApplyMeo(mes,unitSerial,admeocode):
        try:
            transaction =  mes.json_template['transactions'] = []

            unit = {"unit":{"unit_id":unitSerial},"commands":[]}
            transaction.append(unit)

            admeo = {"command":{"name": "ApplyMeo","meo_number":admeocode}}
            transaction[0]['commands'].append(admeo)



            posting = requests.post(mes.endpoint, json=mes.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                logging.info(unitSerial + " : " + reply["transaction_responses"][0]["scanned_unit"]["status"]["message"])
                return reply["transaction_responses"][0]["scanned_unit"]["status"]["code"] + " :: " + reply["transaction_responses"][0]["scanned_unit"]["status"]["message"]
            else:
                return False
                logging.error("Conduit Communication Error")

        except Exception as e:
            logging.error(e)

    def mes_AddNonTrackedComponent(mes,unitSerial,component,value):
        try:
            transaction =  mes.json_template['transactions'] = []

            unit = {"unit":{"unit_id":unitSerial},"commands":[]}
            transaction.append(unit)

            admeo = {"command":{"name": "AddNontrackedComponent","ref_designator":component,"component_id":value}}
            transaction[0]['commands'].append(admeo)



            posting = requests.post(mes.endpoint, json=mes.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                logging.info(unitSerial + " : " + reply["transaction_responses"][0]["scanned_unit"]["status"]["message"])
                return reply["transaction_responses"][0]["scanned_unit"]["status"]["code"] + " :: " + reply["transaction_responses"][0]["scanned_unit"]["status"]["message"]
            else:
                return False
                logging.error("Conduit Communication Error")

        except Exception as e:
            logging.error(e)



def help():
    print(open("help.txt",'r').read())

#help()
#x = conduit("http://sanmmed-conduit.42-q.com:18003/conduit","1002440","R129","566","mp5678dc1a")
#print(x.mes_login())
#print(x.mes_PassUnit("1"))#AddNontrackedComponent
#print(x.mes_ApplyMeo("33849244CC","SCC Measurements"))
#x.mes_ApplyMeo("33849244CC","SCC Measurements")
#x.mes_AddNonTrackedComponent()
