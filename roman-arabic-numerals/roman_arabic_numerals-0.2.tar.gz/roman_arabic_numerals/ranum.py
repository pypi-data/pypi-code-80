#from Roman to Arabic
def rom_arab(z, p):
	for i in range(0, len(p)):
		if p[i]=='I' or p[i]=='i':
			try:
				if p[i+1]=='V' or p[i+1]=='X' or p[i+1]=='v' or p[i+1]=='x': 
					z-=1
				else:
					z+=1
			except:
				z+=1
		elif p[i]=='V' or p[i]=='v':
			z+=5
		elif p[i]=='X' or p[i]=='x':
			try:
				if p[i+1]=='C' or p[i+1]=='L' or p[i+1]=='c' or p[i+1]=='l': 
					z-=10
				else:
					z+=10
			except:
				z+=10
		elif p[i]=='L' or p[i]=='l':
			z+=50
		elif p[i]=='C' or p[i]=='c':
			try:
				if p[i+1]=='M' or p[i+1]=='D' or p[i+1]=='m' or p[i+1]=='d': 
					z-=100
				else:
					z+=100
			except:
				z+=100
		elif p[i]=='D' or p[i]=='d':
			z+=500
		elif p[i]=='M' or p[i]=='m':
			z+=1000
	return z