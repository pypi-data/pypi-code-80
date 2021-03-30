from isoweek import Week
def preWeek(inputYW,gapWeek):

#     inputYW = 202010
#     gapWeek = 20

    inputYW = str(inputYW)
    currYear = inputYW[:4]      #월, 주 나누어 알아보기
    currWeek = inputYW[4:]
    gapWeek = int(gapWeek)

    resultWeek= int(currWeek) - gapWeek
    calcYear = int(currYear)

    while resultWeek <= 0:
        calcYear = calcYear-1
        preYearLastWeek = Week.last_week_of_year(calcYear).week
        resultWeek = preYearLastWeek + resultWeek

    weekLen = len(str(resultWeek))
    if(weekLen < 2):
        result = str(calcYear) + "0" +str(resultWeek)
    else:
        result = str(calcYear) + str(resultWeek)
    return result

def postWeek(yearWeek, postWeek):  #postWeek 이후 주차를 반환하는 함수
    from isoweek import Week
    yeardigit = 4  #만년 이후에는 자리수가 바뀔 수 있으니까...
    inputYear = int(str(yearWeek)[:yeardigit]) #년도만 잘라서 저장
    inputWeek = int(str(yearWeek)[yeardigit:]) #주차만 잘라서 저장
    resultWeek = inputWeek + postWeek           #현 주차 + 뒤로 갈 주차 계산결과
    calcWeek = Week.last_week_of_year(inputYear).week
    
    while(resultWeek>calcWeek):       # 주차가 넘어간다면
        inputYear = inputYear+1    # 년도가 하나 늘어납니다
        calcWeek = Week.last_week_of_year(inputYear).week  #늘어난 년도의 총 주차수
        resultWeek = resultWeek - calcWeek
        #resultWeek 에서 총 주차를 빼줍니다
        #결과가 아직도 총 주차보다 크다면 작아질때까지계속 반복
    
    if(resultWeek<10):
        resultWeek = "0"+str(resultWeek) #1자리수면 앞에 0을 붙여줌
        
    result = str(inputYear)+str(resultWeek) #년도와 주차를 문자열로 더해서 출력
    
    return result