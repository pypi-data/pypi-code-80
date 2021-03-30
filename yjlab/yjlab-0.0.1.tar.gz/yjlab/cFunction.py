#!/usr/bin/env python
# coding: utf-8

# In[15]:


from isoweek import Week

def preWeek(yearWeek, inputWeeks):
    yearWeek = str(yearWeek)  
    inputWeeks = int(inputWeeks)  

    # 문자열 yearWeek를 split (year, week)
    year = int(yearWeek[:4])   
    week = int(yearWeek[4:])   

    # inputWeeks가 week보다 클때 전년도로 넘어가서 전년도 week수를 더함
    # (week가 inputWeeks보다 커질때까지 계속 while문 반복)
    if week <= inputWeeks:
        while (week <= inputWeeks):
            week = week +  Week.last_week_of_year(year - 1).week
            year = year - 1;
        week = week - inputWeeks
        
    else :
        week = week - inputWeeks;

    # week값이 10미만일 경우 앞에 문자"0"을 추가함    
    if (week < 10):
        week = str(week)
        week = "0" + week

    result = str(year) + str(week)
    return result

