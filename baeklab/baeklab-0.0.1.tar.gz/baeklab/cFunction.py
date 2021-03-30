from isoweek import Week

def weekFunction(yearweek,preweek):
    
    #들어온 값을 인덱스 처리하기 위해 문자열로 형변환
    #diff라는 변수에 주차끼리 뺀 값을 넣어준다
    
    year = str(yearweek)[0:4]
    week = str(yearweek)[4:]
    diff = int(week) - int(preweek)
    
    #diff가 양수일경우 같은 년도 내에서 주차끼리만 단순 뺄셈 
    
    if (diff > 0) :
        result = int(yearweek) - int(preweek)
        result = str(result)
        return result
    
    #diff가 0일때 전년도로 마지막 주차로 넘어가기 위한 과정
    
    elif (diff == 0):
        year = int(year) - 1   #년도는 전년도로 넘어간다
        week = Week.last_week_of_year(year).week #주차는 넘어간 년도의 마지막 주차가 된다
        result = str(year) + str(week)  #두 값을 붙여주기 위해 문자열로 형변환
        return result
    
    #diff가 음수일때 계속해서 전년도로 넘어간다
    
    else:
        while(diff <0):
            year = int(year) - 1  #년도는 전년도로 넘어간다
            diff = diff + Week.last_week_of_year(year).week #주차는 넘어간 년도의 마지막 주차에서 diff만큼 빠진다
    
            if(diff<0):
                continue  #diff가 여전히 음수일 경우 위에 과정을 반복해준다 
                
            if(diff==0):   #diff가 다시 0이 되는 경우 전년도 마지막 주차로 넘어간다
                year = int(year) - 1
                week = Week.last_week_of_year(year).week
                result = str(year) + str(week)
                return result
            
            if(diff>0):   #diff가 다시 양수가 되면 단순계산 해준다
                if(diff<10):
                    result = str(year) +"0"+ str(diff)   #주차가 한자리로 나오지 않게 0을 붙여준다
                    return result
                result = str(year) + str(diff)   
                return result