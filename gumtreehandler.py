# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import time
import codecs
import os

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def PierwszaStrona():
    #pr - cena od do
    #fr - wlasciciel czy agencja
    #nr - liczba pokojów
    url= 'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/mieszkanie/v1c9008l3200114a1dwp1?fr=ownr&nr=3&pr=1200,2400'
    print("Strona testowa... ")
    request = urllib.request.Request(url,data=None,headers=headers)
    f = urllib.request.urlopen(request)
    dane = f.read().decode('utf-8')
    return dane

def IloscStron():
    #moze nie ilosc stron, ale lista ktorej ilosc elementow to liczba stron
    strKodHtmlPierwszejStrony = PierwszaStrona()
    strPodzielonyKodHtlm = iter(strKodHtmlPierwszejStrony.splitlines())
    strony = []
    for line in strPodzielonyKodHtlm:
        if '<a href="/s-mieszkania-i-domy-do-wynajecia/wroclaw/mieszkanie/page' in line:
            strony.append(line)
    strony.append("pusty szajz")
    return strony

def WszystkieStrony():
    kodPierwszejStrony = []
    kodPozostalychStron = []
    kodWszystkichStron = []
    for id,nazwa in enumerate(IloscStron()):
        if id == 0:
            url = 'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/mieszkanie/v1c9008l3200114a1dwp1?fr=ownr&nr=3&pr=1200,2400'
            print("Strona 1 ")
            request = urllib.request.Request(url, data=None, headers=headers)
            f = urllib.request.urlopen(request)
            kodPierwszejStrony.append(f.read().decode('utf-8'))
        else:
            url= 'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/mieszkanie/page-'+str(id+1)+'/v1c9008l3200114a1dwp'+str(id+1)+'?fr=ownr&nr=3&pr=1200,2400'
            data = None
            print("Strona "+str(id+1))
            time.sleep(1)
            request = urllib.request.Request(url,data=None,headers=headers)
            f = urllib.request.urlopen(request)
            kodPozostalychStron.append(f.read().decode('utf-8'))
    kodWszystkichStron.insert(0,kodPierwszejStrony[0])
    for index,item in enumerate(kodPozostalychStron):
        kodWszystkichStron.insert(index+1,kodPozostalychStron[index])
    return kodWszystkichStron

def WyciaganieOfert():
    listaWszystkichStronHtml = WszystkieStrony()
    print("Wyciagam oferty ze stron...")
    oferty = []
    for id,item in enumerate(listaWszystkichStronHtml):
        podzielonaLista = iter(listaWszystkichStronHtml[id].splitlines())
        for line in podzielonaLista:
            if '<a class="href-link" href=' in line:
                oferty.append(line)
    return oferty

def MachinacjeInformacjami():
    listaofert = WyciaganieOfert()
    print("Usuwam zbedny szit...")
    words = [word.replace('<a class="href-link" href="', 'https://www.gumtree.pl') for word in listaofert]
    words2 = [word.replace("    ", '') for word in words]
    words3 = [word.replace("\t", '') for word in words2]
    words4 = [word.replace("</a>", '') for word in words3]
    words5 = [word.replace("\n", '') for word in words4]
    return words5

def SzlifowanieDiamentu():
    listaokrojonazgowna = MachinacjeInformacjami()
    wyjebanalista = []
    listalinkow = []
    opispluspszczaukapluslink = []
    print("Szlifuję linki...")
    typie = [word.index('">') for word in listaokrojonazgowna]
    for id,element in enumerate(listaokrojonazgowna):
        elemencik = str(listaokrojonazgowna[id][typie[id]+2:])
        link = str(listaokrojonazgowna[id][:typie[id]])
        wyjebanalista.insert(id, elemencik)
        listalinkow.insert(id, link)
    nazwapluspszczauka = [nazwa + " ----> " for nazwa in wyjebanalista]
    for id, item in enumerate(wyjebanalista):
        opispluspszczaukapluslink.append(nazwapluspszczauka[id] + listalinkow[id])
    print("#Done, znaleziono {} ofert".format(len(opispluspszczaukapluslink)))
    return opispluspszczaukapluslink

def KrzyczPliku(lista):
    print("Zmniejszam literki...")
    krzyczkontent = []
    for line in lista:
        krzyczkontent.append(str.lower(line))
    return krzyczkontent

def NiewygodneSlowa(listaSlowZakazanych,mieszkanka):
    newfile = []
    for line in mieszkanka:
        if not any(zlerzeczy in line for zlerzeczy in listaSlowZakazanych):
            newfile.append(line)
    print("Zostalo {}".format(len(newfile)))
    with codecs.open("swiezutkiemieszkania.txt", "a", "utf-8") as pliq:
        for id,line in enumerate(newfile):
            pliq.write(newfile[id] + '\n')
    print("#Zrzut do pliku...")

def PojedynczaOfertaHandler(listaSlowZakazanych):
    okazaleoferty = []
    opis = []
    print("Wyciagam linki z pliku...")
    with open("swiezutkiemieszkania.txt",'r') as plik:
        qualitykontent = plik.readlines()
        typie = [word.index('---->') for word in qualitykontent]
        for id, element in enumerate(qualitykontent):
            link = str(qualitykontent[id][typie[id]+6:])
            okazaleoferty.insert(id, link)
    for id,oferta in enumerate(okazaleoferty):
        try:
            if id % 4 == 0:
                time.sleep(3)
            elif id % 11 == 0:
                time.sleep(15)
            time.sleep(0.5)
            string = ""
            url = oferta
            request = urllib.request.Request(url, data=None, headers=headers)
            f = urllib.request.urlopen(request)
            dane = f.read().decode('utf-8')
            szukamy = 'style="font-family: inherit; white-space: pre-wrap;"'
            numerlinii = dane.find(szukamy)
            for x in range(numerlinii+59, numerlinii+1500):
                string = string +dane[x]
            kupsko = string.split("</span>")
            opis.append(kupsko[0])
            print("Miele oferte nr {}".format(id+1))
        except:
            continue
    newfile = []
    for id,line in enumerate(opis):
        if not any(zlerzeczy in line for zlerzeczy in listaSlowZakazanych):
            newfile.append(okazaleoferty[id])
    print("Zostalo {}".format(len(newfile)))
    newnewfile = []
    for link in newfile:
        if link not in newnewfile:
            newnewfile.append(link)
    print("A teraz zostalo {}".format(len(newnewfile)))
    with codecs.open("gumtreeprzemielone.txt", "a", "utf-8") as pliq:
        for id, line in enumerate(newnewfile):
            pliq.write(newnewfile[id])
    print("#Zrzut 2")

def main():
    listaSlowZakazanych = ['psie pole', 'kromera', 'marino', 'nadodrze', 'ołtaszyn',
                           'partynice', 'jaracza', 'sołtysowice', 'jagodno', 'śródmieście',
                           'księże', 'księża', 'kamieńskiego', 'aneks', 'maślic',
                           'rędzin', 'świniar', 'biskupin', 'bartoszowic', 'sępoln',
                           'tarnogaj', "broch", 'traugutta', 'kościuszk', 'wojszyc',
                           'leśnic', 'kleczk', 'różanka', 'różance','antresol',
                           'salon', 'psiego pola', 'curie sklodowskiej', 'huby','kamienn',
                           'piec kaflow', 'ogrzewanie gazow', 'piec elektrycz', 'kamieni',
                           'sky tower','przechodni','parter','agencja','estates',
                           'stabłowic']
    NiewygodneSlowa(listaSlowZakazanych, KrzyczPliku(SzlifowanieDiamentu()))
    PojedynczaOfertaHandler(listaSlowZakazanych)
    os.remove("swiezutkiemieszkania.txt")
    os.system(r"copy gumtreeprzemielone.txt C:\Users\Paweł\Desktop")
    print("#Done")

main()
