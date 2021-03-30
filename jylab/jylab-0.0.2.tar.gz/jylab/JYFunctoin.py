# 라이브러리 불러오기

# preWeek 함수로 정의 인덱스로 년도 및 주차 계산
def preWeek(inputYearWeek, inputWeek): #inputYearWeek=201720,inputWeek=55
    from isoweek import Week
    yearWeek = str(inputYearWeek)
    year = int(yearWeek[0:4]) #year=2017
    week = int(yearWeek[4:]) #week=20
    differWeek = week - inputWeek #20 - 56
   
    #totalWeek = Week.last_week_of_year(year).week
    
    # if 문으로 주차 계산
    if ( week > inputWeek) :      # 예) 2020.20(week)>10(inputWeek) 그냥 빼기
        answerWeek=str(int(inputYearWeek)-inputWeek)
        
    elif (week <= inputWeek): #20 <= 56
       
        # 조건반복문 differWeek > 0 로직 종료. 
        while (differWeek <= 0): #20-56 =-36  (week - inputWeek)
            year = year - 1 #2018
            totalWeek = Week.last_week_of_year(year).week #52
            differWeek = differWeek + totalWeek # 53+(-36) =20
        # differWeek 가 한자리 수 일경우 20203 이 찍히는걸 202003 변환 로직
            if(differWeek < 10):
                answerWeek = str(year) + "0" + str(differWeek)
            else:
                answerWeek = str(year) + str(differWeek) #'2016'+'20'
    return answerWeek