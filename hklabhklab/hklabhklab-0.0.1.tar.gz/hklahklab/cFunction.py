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