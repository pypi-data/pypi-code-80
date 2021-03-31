import serial		#아두이노와 시리얼 통신하기위해 Serial이라는 라이브러리(코드뭉치)를 불러온다
import time		#시간을 지연시키는 명령어(time.sleep())를 사용하기 위해 time 라이브러리(코드뭉치)를 불러온다
connection = 0		#아두이노와 통신 상태(끊겼는지, 연결되었는지)를 저장하는 변수(현재는 끊겨있으니 0)
portnum = 1		#아두이노와의 통신 경로(포트)를 저장하는 변수(아두이노 연결을 1번포트부터 시도하라)
sv = [90,90,90,90]
sv2 = ["","","",""]
while(connection == 0):					#만약 아두이노와 연결이 없다면
    try:							#시도하라
        arduino = serial.Serial("com%d"%portnum,115200)		#아두이노와 시리얼 연결을 시작하라(1번포트부터 100까지)
        print("아두이노 연결 성공")				#만약 앞줄에서 에러가 안나고 성공하면, 통신 성공을 화면에 띄운다
        connection = 1					#통신 상태를 1로 바꾼다(연결이 되었다고 내려준다)
    except:							#만약 에러가 나면(아두이노와 연결 시도하는 코드에서 에러가 있다면)
        portnum = portnum + 1				#다른 포트를 시도해보아라(1에서 2번포트로, 45번에서 46번으로 등등)
    if(portnum > 100):					#만약 100번포트까지 다 시도해보았다면
        connection = 2					#통신 상태를 2로 바꾼다(에러)
        print("아두이노 연결 실패")				#아두이노와 통신에 실패했다는 것을 화면에 띄운다

def move(number,gap):
    global sv
    sv[number-8] = gap
    arduino.write(b"s")
    for i in range(4):
        if(sv[i] < 10):
            sv2[i] = "00" + str(sv[i])
        elif(sv[i] < 100):
            sv2[i] = "0" + str(sv[i])
        else:
            sv2[i] = "" + str(sv[i])
        sv2[i] = sv2[i].encode('utf-8')
        arduino.write(sv2[i])


    

    
    
