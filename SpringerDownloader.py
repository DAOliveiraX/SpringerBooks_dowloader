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

	banList = '.,-çÇ?:/' # Removing some unwanted characters from Authors or Books name
	hierarchical = str(root[3])
	book_name = str(root[0])
	authors_name = str(root[2])

	for i in banList:
		hierarchical = hierarchical.replace(i, '')
		book_name = book_name.replace(i, '')
		authors_name = authors_name.replace(i, '')
	
	dirName = "SpringerBooks/"+hierarchical+"/"+book_name+"_by_"+authors_name

	try:
		os.mkdir(dirName)
	except:
		print("Already have this folder name")

	for item in link:
		# Requesting the document page ans saving as a new file
		a = requests.get("https://link.springer.com"+str(item))
		newFile = dirName+'/'+book_name+"."+item.rsplit('.',1)[1]
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
start_time = time.time()

try:
	if int(fileType) not in [1,2,3]:
		exit()
except:
	exit()

df = pd.read_excel('books.xlsx')

pp = []
for index, row in df.iterrows():
  pp.append([row["Book Title"],row["OpenURL"],row["Author"],row['English Package Name']])

createRoot()
num = 1

for item in pp:

	try:
		os.mkdir("SpringerBooks/"+item[3])
	except:
		print("Already have root folder")

	origem(item, str(len(pp)), str(num))
	num = num + 1

print("\n--- ", str(len(pp)) ," books downloaded in %s seconds ---" % round((time.time() - start_time), 2 ) )
print("\nFinished. Have a nice day.")
