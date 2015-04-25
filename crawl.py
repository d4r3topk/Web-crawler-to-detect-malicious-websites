from urllib.parse import urlparse,urljoin
import sys
import urllib.request
from bs4 import BeautifulSoup



def crawl():
	cnt=0
	while(len(urls) >0):
		print("--")
		templi=[]
		print("Current URL : ",urls[0])
		a = urllib.request.urlopen(urls[0])
		htmltext = a.read()
		headertext = str(a.info())
		soup = BeautifulSoup(htmltext)
		soup1 = BeautifulSoup(headertext)
		cnt=cnt+1
		f = open("html/"+str(cnt)+".html", "w+")
		f1 = open("header/"+str(cnt),"w+")
		f.write(soup.prettify())
		f1.write(soup1.prettify())
		f.close()
		f1.close()		

		li = soup.findAll('a',href=True)  #A result set
		currentUrl=urls.pop(0)	

		for tag in li:
			tag['href'] = urljoin(currentUrl,tag['href'])  #if https:// is not there in the a href tag it pre-appends url
			if tag['href'] not in visited:	
				templi.append(tag['href'])
				urls.append(tag['href'])
				visited.append(tag['href'])
		print(currentUrl," has ",str(len(templi))," links.")
		for j in templi:
			print(j)
	print(len(visited), " sites are visited\n")
	for i in visited:
		print(i,"\n")
if __name__=="__main__":
	url=str(sys.argv[1])
	urls = [url]
	visited = [url]
	templi=[]
	crawl()
