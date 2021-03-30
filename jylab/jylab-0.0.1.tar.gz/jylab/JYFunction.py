{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 라이브러리 불러오기\n",
    "\n",
    "# preWeek 함수로 정의 인덱스로 년도 및 주차 계산\n",
    "def preWeek(inputYearWeek, inputWeek): #inputYearWeek=201720,inputWeek=55\n",
    "    from isoweek import Week\n",
    "    yearWeek = str(inputYearWeek)\n",
    "    year = int(yearWeek[0:4]) #year=2017\n",
    "    week = int(yearWeek[4:]) #week=20\n",
    "    differWeek = week - inputWeek #20 - 56\n",
    "   \n",
    "    #totalWeek = Week.last_week_of_year(year).week\n",
    "    \n",
    "    # if 문으로 주차 계산\n",
    "    if ( week > inputWeek) :      # 예) 2020.20(week)>10(inputWeek) 그냥 빼기\n",
    "        answerWeek=str(int(inputYearWeek)-inputWeek)\n",
    "        \n",
    "    elif (week <= inputWeek): #20 <= 56\n",
    "       \n",
    "        # 조건반복문 differWeek > 0 로직 종료. \n",
    "        while (differWeek <= 0): #20-56 =-36  (week - inputWeek)\n",
    "            year = year - 1 #2018\n",
    "            totalWeek = Week.last_week_of_year(year).week #52\n",
    "            differWeek = differWeek + totalWeek # 53+(-36) =20\n",
    "        # differWeek 가 한자리 수 일경우 20203 이 찍히는걸 202003 변환 로직\n",
    "            if(differWeek < 10):\n",
    "                answerWeek = str(year) + \"0\" + str(differWeek)\n",
    "            else:\n",
    "                answerWeek = str(year) + str(differWeek) #'2016'+'20'\n",
    "    return answerWeek"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
