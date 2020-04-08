from lxml import html
import requests
import xlrd
import csv
import os
import pandas as pd
import time

#Function to remove not-interested format's file
def getFormat(link):
	if int(fileType) == 1: #If choice 1, let only .pdf files
		for item in link:
			if ".pdf" not in item:
				link.remove(item)

	if int(fileType) == 2: #If choice 2, let only .epub files
		for item in link:
			if ".epub" not in item:
				link.remove(item)

	return link

def book(root, nt, n0):

	#request book page and get all available files list
	page = requests.get(root[1])
	tree = html.fromstring(page.content)
	link = tree.xpath('//*[@class="cta-button-container__item"]//a/@href')
	link = list(dict.fromkeys(link))
	
	link = getFormat(link)

	banList = '.,- çÇ' # Removing some unwanted characters from Authors or Books name
	

	dirName = "SpringerBooks/"+str(root[0])+"_by_"+str(root[2])
	for i in banList:
		dirName = dirName.replace(i, '')

	try:
		os.mkdir(dirName)
	except:
		print("Already have this folder name")

	for item in link:
		# Requesting the document page ans saving as a new file
		a = requests.get("https://link.springer.com"+str(item))
		newFile = dirName+'/'+root[0]+"."+item.rsplit('.',1)[1]
		print("["+n0+"/"+nt+"] Downloading " + newFile + " ...")
		open(newFile, 'wb').write(a.content)

def origem(root, nt, n0):
	# Request the excel's book link. Will redirect to another page. Getting this one with .url
	page = requests.get(root[1])
	root[1] = page.url
	
	book(root, nt, n0)

def headerPrint():
	print("\n#####\n\nSpringer Books Downloader\n\nReview the README.txt file before use.\n\n#####\n")
	

def createRoot():
	try:
		os.mkdir("SpringerBooks")
	except:
		print("Already have root folder")

headerPrint()

fileType = input("1 - PDF\n2 - EPUB\n3 - ALL\n4 - EXIT\nOPTION: ")
try:
	if int(fileType) not in [1,2,3]:
		print("a")
		exit()
except:
	print("b")
	exit()

df = pd.read_excel('books.xlsx')


pp = []
for index, row in df.iterrows():
  pp.append([row["Book Title"],row["OpenURL"],row["Author"]])

createRoot()
num = 1

for item in pp:
	origem(item, str(len(pp)), str(num))
	num = num + 1


print("\nFinished. Have a nice day.")