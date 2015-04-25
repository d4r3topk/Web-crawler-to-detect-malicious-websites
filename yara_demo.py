import re
import yara
import sys
import os.path

#---------------------------------------------------------------------
#This is for rule matching from yara. Takes care of all the regex's
data=0
'''
def mycallback(data):
	print(data)
	a=bool(input("continue to next rule?"))
	if(a):
		yara.CALLBACK_CONTINUE
	else:
		yara.CALLBACK_ABORT
'''
def run_yara(filename):
	matched = rules.match(filename)	
	a=[]
	for key,value in matched.items():
		print(len(value))
		for i in range(len(value)):
			count = len(value[i]['strings'])
			rule_name = str(value[i]['rule'])
			print(rule_name+" "+str(count)+" times.")
			for j in range(0,count):
				rule_match =  str(value[i]['strings'][j]['data'])
				if(rule_name == "hidden_link"):
					a.append(rule_match)
				print("match ",str(i)," : ",rule_match)
	
#---------------------------------------------------------------
#Looking for hidden links and checking for equality of colors
		link1_color="black"
		body1_color="white"
		body2_color="white"
		for v in a:
			body1=re.search("background-color *: *(.*?);",v)
			if(body1!=None):
				body1_color=body1.group(1)
	
			body2=re.search("bgcolor *= *[\"\'](.*?)[\"\']",v)
			if(body2!=None):
				body2_color=body2.group(1)
	
			link1=re.search("[^-]color *: *(.*?);",v)
			if(link1):
				link1_color=link1.group(1)
		if(link1_color==body1_color or link1_color==body2_color):
			print("Hidden link found")
	print("done")
#---------------------------------------------------------------

if __name__=="__main__":
	i=1
	file_name = "./html/"+str(i)+".html"
	rules = yara.compile(sys.argv[1])
	li=[]
	while(True):
		if(os.path.isfile(file_name)):
			print("-------------------------------------")
			print("GOT "+file_name)
			run_yara(file_name)
			li.append(file_name)
		if(file_name in li):
			i=i+1
			file_name="./html/"+str(i)+".html"

