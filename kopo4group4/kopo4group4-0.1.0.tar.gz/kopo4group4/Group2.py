def pastWeek2(inputYearWeek,minusWeek):
    from isoweek import Week
    #형변환
    inputYear = int(str(inputYearWeek)[:4])
    inputWeek = int(str(inputYearWeek)[4:])       
    yearWeek = Week.last_week_of_year(inputYear).week   

    # 년도가 바뀌지 않을때!
    if inputWeek<=yearWeek:
        JudgeWeek = minusWeek-inputWeek
        
        # minusWeek에서 inputWeek뺀 값을 JudgeWeek변수에 정의
        if JudgeWeek < 0:    #빼야 할 주차에서 기준주차가 0보다 작다면
                print(str(inputYear)+str(inputWeek-minusWeek))    #입력한 년주차의 년도와 연산한 주차정보 출력
                
    # 년도가 바뀔때
        ## judgeWeek=0일 때 0주차 값 변환 
        elif inputWeek == minusWeek:     #빼고자 하는 주차의 값과 기준 주차의 값이 같을떄 
                print(str(inputYear-1)+str(Week.last_week_of_year(inputYear-1).week))             
    
        elif JudgeWeek > 0:
            for i in range (1, inputYear):
             ## 반복한 횟수만큼 기준년도 감소   
                calcYear = inputYear - i
             ## 감소한 년도의 총 주차 
                calcWeek = Week.last_week_of_year(inputYear-i).week
             ## 기준주차에서 빼고자하는 주차가 더 크다면
                if JudgeWeek > calcWeek:
                     JudgeWeek = JudgeWeek-calcWeek

             ## 기준주차가 더 클때
                elif JudgeWeek < calcWeek: 
                    print(str(calcYear)+str(calcWeek-JudgeWeek))
                    break;
                    
              ## 기준주차 - 빼고자할 주차가 같을때
                elif JudgeWeek == calcWeek:
                    print(str(inputYear-(i+1))+str(Week.last_week_of_year(inputYear-(i+1)).week))
                    break;