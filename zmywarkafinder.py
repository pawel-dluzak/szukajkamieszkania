# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import os

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def SlowoFinder(slowo):
    for plik in ["gumtreeprzemielone.txt","olxprzemielone.txt"]:
        print("Handlinguje "+str(plik))
        with open(plik,'r') as file:
            linki = file.readlines()
        for id, oferta in enumerate(linki):
            print("Oferta nr "+str(id+1))
            string = ""
            url = oferta
            request = urllib.request.Request(url, data=None, headers=headers)
            f = urllib.request.urlopen(request)
            dane = f.read().decode('utf-8')
            if plik == "gumtreeprzemielone.txt":
                szukamy = 'style="font-family: inherit; white-space: pre-wrap;"'
                lower = 59
                upper = 1500
            elif plik == "olxprzemielone.txt":
                szukamy = '<p class="pding10 lheight20 large"'
                lower = 34
                upper = 1000
            numerlinii = dane.find(szukamy)
            for x in range(numerlinii+lower, numerlinii+upper):
                string = string +dane[x]
            if plik == "gumtreeprzemielone.txt":
                kupsko = string.split("</span>")
            elif plik == "olxprzemielone.txt":
                kupsko = string.split("</p>")
            if slowo in kupsko[0]:
                print(" {}\n".format(linki[id]))
                with open("ofertyzezmywarka.txt",'a') as kurwafile:
                    kurwafile.write(linki[id]+'\n')

def main():
    szukane = 'zmywarka'
    SlowoFinder(szukane)
    os.remove("gumtreeprzemielone.txt")
    os.remove("olxprzemielone.txt")
    os.system(r"copy ofertyzezmywarka.txt C:\Users\Paweł\Desktop")
    os.remove("ofertyzezmywarka.txt")

main()