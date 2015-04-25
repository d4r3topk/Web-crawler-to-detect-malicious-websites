import sys,bs4,re
from urllib.request import urlopen
 
'''
Parameters taken in consideration
1.domain_length
2.unique characters
3.brand name presence
4.url length
5.website rank on alexa
'''

d={}
score = [0,0,0,0,0]

def check_phish(url):
	total_score=0
	final_score=0
	rev_ratio=0
	flag=0
	a=re.search(r'.+[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.*',url)
	if(a!=None):
		final_score=0.90
		print("Final score : ",final_score)
		sys.exit(0)

	only_dom  = re.match(r"^(https?:\/\/)?(www.)?([\da-z\.-]+)\.([a-z\.]{2,6})(.*)\/?$",url)
              sys.exit(0)

	if(only_dom!=None):
		print(only_dom.groups())
	else:
		print("No match")
	print("\nDomain Length");	
	print("--------------------")
	domain_length  = len(only_dom.group(3))
	print("domain length : ",domain_length)
	#-----calculating score------
	if(domain_length >= 1 and domain_length <= 4):
		score[0]=7
	elif(domain_length > 4 and domain_length<=7):
		score[0]=6
	elif(domain_length > 8 and domain_length<=10):
		score[0]=5
	elif(domain_length>10):
		score[0]=3

	print("\nURL length")
	print("--------------------")
	url_length = len(only_dom.group(3)) + len(only_dom.group(5))
	print("url length : ",url_length)
	#-----calculating score------
	if(url_length==domain_length):
		score[1]=2
	elif(url_length >= 100):
		score[1]=8
	elif(url_length > 40 and url_length <=100):
		score[1]=7
	elif(url_length >30 and url_length<=40):
		score[1]=6
	elif(url_length >20 and url_length<=30):
		score[1]=5
	elif(url_length >10 and url_length<=20):
		score[1]=4
	elif(url_length<=10):
		score[1]=3

	for i in set(only_dom.group(3)):
		d[i]=only_dom.group(3).count(i)
	print("\nUnique character ratio")
	print("--------------------")
	ratio=len(d)/len(only_dom.group(3))
	print(" Ratio : ",ratio)
	if(ratio>0 and ratio<=0.25):
		score[2]=8
	elif(ratio>0.25 and ratio<=0.40):
		score[2]=7
	elif(ratio>0.40 and ratio<=0.55):
		score[2]=6
	elif(ratio>0.55 and ratio<=0.70):
		score[2]=5
	elif(ratio>0.70 and ratio<=0.80):
		score[2]=4
	elif(ratio>0.80):
		score[2]=3


	print("\nBrand name presence")
	print("--------------------")

	brand_names = ["google","yahoo","g00gle","yah00","runescape","vogella","v0gella"]
	ignore_names = ["google-melange","google-styleguide","googlesciencefair","thinkwithgoogle","googleforentrepreneurs","withgoogle"]
	malicious_names = ["account","free","membs","membership","hacks","lottery","prize","money"]

	for i in brand_names:
		if(only_dom.group(3).find(i)!=-1):
			if(only_dom.group(3)==i):
				print("Not Phishing")
				sys.exit(0)
			regex1 = ".*\."+i+"\..*"
			regex3 = ".*\."+i
			if(re.match(regex1,only_dom.group(3)) or re.match(regex3,only_dom.group(3))):
				print("Not phishing")
				sys.exit(0)
			regex2 = ".*"+i+".*"
			if(re.match(regex2, only_dom.group(3))):
				flag=flag+1
				print("detected brand name")
		# FOR IGNORING NON-PHISHING SITES !!
			for j in ignore_names:
				regex2= ".*\."+j+"\..*"
				if(re.match(regex2,only_dom.group(3))):
					print("Not phishing")
					sys.exit(0)
			for k in malicious_names:
				if(only_dom.group(3).find(k)!=-1):
					flag=flag+1
					print("Suspected phishing")
	if(flag==1):
		score[3]=8
	elif(flag==2):
		score[3]=9
	elif(flag==3):
		score[3]=10
	elif(flag>3):
		score[3]=10	
	elif(flag==0):
		score[3]=3

	print("SCORE[3] : ",score[3])

					
	print("\nGlobal rank of website")
	print("---------------------------")

	try:
		str1 = bs4.BeautifulSoup(urlopen("http://www.alexa.com/siteinfo/"+ url).read(), "xml")		
	except urllib.URLError:
		print("URL error : ")	
	list_rank=re.findall(r"metrics-data align-vmiddle..([0-9,]*)<\/strong>",str(str1))
	if(len(list_rank)!=0):
		list_rank[0].strip('''metrics-data align-vmiddle">''')
		list_rank[0]=list_rank[0].replace(',','')       
		list_rank[0]=int(list_rank[0])
		print(list_rank[0])
		if(list_rank[0]>0 and list_rank[0]<50000):
			score[4]=1
		elif(list_rank[0]>=50000 and list_rank[0]<=100000):
			score[4]=2
		elif(list_rank[0]>100000):
			score[4]=8
		else:
			print("sorry invalid site name")
	else:
		print("No rank for this site")
		score[4]=10
#-------calculation of final score--------------

	for i in score:
		total_score=total_score+i
	final_score=total_score/50
	print("\nPercentage to be a phishing site : ",(final_score*100))

	if(final_score>=0.50):
		print("\n----------More than 50 percent---------")
		print("--> Checking for password fields")
		str2 = bs4.BeautifulSoup(urlopen(url).read(),"xml")
		str2=str(str2)
		if(str2.find('''type="password"''')!=-1):
			print("::: Password fields present")
			rev_ratio = (total_score+9)/60
			print("--> Revised final percent : ",rev_ratio*100)
			flag=1
		else:	
			flag=0
			print("::: No password fields")
	print("Conclusion")
	print("--------------------")
	
	if(final_score>=0.50):
		if(flag==1):
			print("Most probably a phishing site with ",rev_ratio*100,"%")
		elif(flag==0):
			print("Most probably a phishing site with ",final_score*100,"%")
	else:
		print("Not a phishing site")

if __name__=="__main__":
	url = str(sys.argv[1])
	check_phish(url)

