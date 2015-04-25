# Web-crawler-to-detect-malicious-websites
Implementation of a webcrawler, with a limited functionality detection for malicious websites

There are two python scripts in this repo. 

crawl.py - usage: python3 crawl.py [website]
example : python3 crawl.py http://www.vogellascoding.site90.net/cnsproj/main.html
This script basically crawls from website to website, finding links on each website and downloading it sequentially.
All the html files goes to the 'html' folder while all the HTTP header files goes to the 'header' folder.
Note : Please make sure both the folders are created before running the script.

yara_demo.py - usage: python3 yara_demo.py
example : python3 yara_demo.py [/path/to/rule/file]
This script looks for files in the html folder, and if found, starts analysing the content file by file and displaying it on stdout. 

There is one more file named myrules, which is a YARA rules file. This file has all the regular expressions for matching the malicious signatures.

Feel free to submit a pull request for any extra signatures that you find out there on a webpage.


Extra files:

phish.py - usage: python3 phish.py [website]
example : python3 phish.py http://vogellascoding.site90.net
This script performs URL heuristics on the website name, as well as considers page rank on alexa and generates a score(out of 1). I have checked the score to be more than 0.5 for it to be a phishing site.
