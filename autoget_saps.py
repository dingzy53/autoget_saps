#!/usr/bin/env python
# encoding: utf-8

import threading
import pandas as pd
import os
from bs4 import BeautifulSoup

# read ic from csv file *count from 0
df = pd.read_csv('ic.csv',usecols=[1],index_col=False,dtype=str)
# save ic number in to a list
ic = df.values.tolist()

# list of all subject (mata pelajaran)
# add your mata pelajaran if doesn't exist in list
mata_pelajaran = ["MATEMATIK [MA]","SEJARAH [MA]","BAHASA INGGERIS [MA]"]

def get_html ():
	# define a bash command to use curl
	# use your user agent as firefox and linux environment in my situation
	# modify kodsek, tingkatan, and kelas according your school
	curl = ("curl -k 'https://sapsnkra.moe.gov.my/ibubapa2/slipma.php' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://sapsnkra.moe.gov.my/ibubapa2/semak.php' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://sapsnkra.moe.gov.my' -H 'DNT: 1'  -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data-raw 'nokp="+str(no_ic)+"&kodsek=JEE4036&ting=T5&kelas=T1&cboPep=PPT' > "+str(no_ic)+".html")
	# require curl
	os.system (curl)

def html_filter ():
	file = no_ic + ".html"
	with open (file) as html :
		current_mata_pelajaran = mata_pelajaran[no_mata_pelajaran]
		# find the string of "mata pelajaran" in current html file
		if (current_mata_pelajaran in html.read()) :
			soup = BeautifulSoup(open(file),'lxml')
			# find next sibling of "mata pelajaran" (markah)
			result =  (soup.find("td", text=current_mata_pelajaran).find_next_sibling("td").text)
			print (result)
		else :
			print ("")
			pass


while True :
	print ("[1] - update saps html")
	print ("[2] - html filter")
	print ("[q] - quit this program")

	func = input ("enter 1~2 / q : ")

	if (str(func)) == "q" or (str(func)) == "quit" :
		quit()

	elif (int(func)) == 1 :
		for i in range (len(ic)):
			current_ic = ic[i]
			# remove [,],and ' symbol from ic number
			no_ic = str(str(current_ic).strip("[']"))
			# use multiprocessing
			trd = threading.Thread(target=get_html)
			trd.start()

	elif (int(func)) == 2:
		for mp in range (len(mata_pelajaran)):
			print ("[" + str(mp) + "] - " + str(mata_pelajaran[mp]))
		print ("[q] - quit this function")
		while True :
			confirm = input ("enter 1~"+ str(len(mata_pelajaran)) + " / q : ")
			if str (confirm) == "q" :
				break
			elif (int(confirm)>=0) and (int(confirm)<len(mata_pelajaran)) :
				no_mata_pelajaran = int(confirm)
				for i in range (len(ic)) :
					current_ic = ic[i]
					no_ic = str(str(current_ic).strip("[']"))
					html_filter()
			else :
				pass

	else :
		print ("input no valid ! ")
		pass
