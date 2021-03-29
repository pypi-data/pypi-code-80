#from Arabic to Roman
def arab_rom(s):
	v=""
	while s>0:
		if s>=1000:
			s-=1000
			v+="M"
		elif s>=900:
			s-=900
			v+="CM"
		elif s>=500:
			s-=500
			v+="D"
		elif s>=400:
			s-=400
			v+="CD"
		elif s>=100:
			s-=100
			v+="C"
		elif s>=90:
			s-=90
			v+="XC"
		elif s>=50:
			s-=50
			v+="L"
		elif s>=40:
			s-=40
			v+="XL"
		elif s>=10:
			s-=10
			v+="X"
		elif s>=9:
			s-=9
			v+="IX"
		elif s>=5:
			s-=5
			v+="V"
		elif s>=4:
			s-=4
			v+="IV"
		elif s>=1:
			s-=1
			v+="I"
	return v