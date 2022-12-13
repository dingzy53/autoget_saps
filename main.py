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
mata_pelajaran = ["BAHASA MELAYU [MA]",
                  "BAHASA INGGERIS [MA]",
                  "MATEMATIK [MA]",
                  "MATEMATIK TAMBAHAN",
                  "KIMIA",
                  "FIZIK",
                  "SEJARAH [MA]",
                  "PRINSIP AKAUN",
                  "PENDIDIKAN MORAL [MA]",
                  "BIOLOGI",
                  "GRAFIK KOMUNIKASI TEKNIKAL",
                  "PENDIDIKAN ISLAM [MA]",
                  "TASAWWUR ISLAM",
                  "BAHASA CINA [MA]"]

def get_html ():
    # using curl to get slipma page
    curl = ('curl -4 -k https://sapsnkra.moe.gov.my/ibubapa2/slipma.php --data "nokp='+str(no_ic)+'&kodsek=xxxx&ting=T5&cboPep=SPMC" > '+str(no_ic)+'.html')
    os.system (curl)

def html_parser ():
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
    print ("[2] - html parser")
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
        while True :
            print ("==========================================================================")
            for mp in range (len(mata_pelajaran)):
                print ("[" + str(mp) + "] - " + str(mata_pelajaran[mp]))
            print ("[q] - quit this function")

            confirm = input ("enter 0~"+ str(int(len(mata_pelajaran))-1) + " / q : ")
            if str (confirm) == "q" :
                break
            elif (int(confirm)>=0) and (int(confirm)<len(mata_pelajaran)) :
                no_mata_pelajaran = int(confirm)
                for i in range (len(ic)) :
                    current_ic = ic[i]
                    no_ic = str(str(current_ic).strip("[']"))
                    html_parser()
            else :
                pass

    else :
        print ("input no valid ! ")
        pass
