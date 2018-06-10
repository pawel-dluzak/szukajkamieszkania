# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import time
import codecs
import os

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def WyciagnijWszystkieStrony():
    url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_price%3Afrom%5D=1400&search%5Bfilter_float_price%3Ato%5D=2400&search%5Bfilter_enum_builttype%5D%5B0%5D=blok&search%5Bfilter_enum_builttype%5D%5B1%5D=wolnostojacy&search%5Bfilter_enum_builttype%5D%5B2%5D=szeregowiec&search%5Bfilter_enum_rooms%5D%5B0%5D=three&search%5Bprivate_business%5D=private"
    request = urllib.request.Request(url,data=None,headers=headers)
    f = urllib.request.urlopen(request)
    dane = f.read().decode('utf-8')
    strHTMLkod = dane.splitlines()
    strony = []
    for line in strHTMLkod:
        if '<a class="block br3 brc8 large tdnone lheight24" href="' in line:
            strony.append(line)
    strony.append("Jeszcze jedna pusta")
    print("Tyle stron {}".format(len(strony)))
    listastron = []
    for id,strona in enumerate(strony):
        if id == 0:
            url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_price%3Afrom%5D=1400&search%5Bfilter_float_price%3Ato%5D=2400&search%5Bfilter_enum_builttype%5D%5B0%5D=blok&search%5Bfilter_enum_builttype%5D%5B1%5D=wolnostojacy&search%5Bfilter_enum_builttype%5D%5B2%5D=szeregowiec&search%5Bfilter_enum_rooms%5D%5B0%5D=three&search%5Bprivate_business%5D=private"
            request = urllib.request.Request(url, data=None, headers=headers)
            f = urllib.request.urlopen(request)
            listastron.append(f.read().decode('utf-8'))
        else:
            url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_price%3Afrom%5D=1400&search%5Bfilter_float_price%3Ato%5D=2400&search%5Bfilter_enum_builttype%5D%5B0%5D=blok&search%5Bfilter_enum_builttype%5D%5B1%5D=wolnostojacy&search%5Bfilter_enum_builttype%5D%5B2%5D=szeregowiec&search%5Bfilter_enum_rooms%5D%5B0%5D=three&search%5Bprivate_business%5D=private&page="+str(id+1)+""
            request = urllib.request.Request(url, data=None, headers=headers)
            f = urllib.request.urlopen(request)
            listastron.append(f.read().decode('utf-8'))
    print("Wyciagnieto")
    return listastron

def WyciagnijOfertyZeStron(listastron):
    klucz = 'class="marginright5 link linkWithHash detailsLink"'
    print("Wyciagam oferty ze stron...")
    oferty = []
    krotkiopis = []
    poteznyiterator = False
    for id, item in enumerate(listastron):
        podzielonaLista = iter(listastron[id].splitlines())
        for id, line in enumerate(podzielonaLista):
            if klucz in line:
                oferty.append(line)
                poteznyiterator = True
                continue
            if poteznyiterator:
                krotkiopis.append(line)
                poteznyiterator = False
    return oferty, krotkiopis

def CiecieWszystkichOfert(opisy,oferty):
    words = [word.replace('\t', '') for word in oferty]
    words2 = [word.replace('<a href="',"") for word in words]
    words3 = [word.replace('" class="marginright5 link linkWithHash detailsLink" >',"") for word in words2]
    words4 = [word.replace('?utm_source=refferals&utm_medium=traffic_exchange&utm_campaign=OLX_nieruchomosci_ad#xtor=SEC-18" class="marginright5 link linkWithHash detailsLink" target="_blank">',"") for word in words3]
    opisowo = [word.replace('\t', '') for word in opisy]
    opisowo2 = [word.replace('<strong>', '') for word in opisowo]
    opisowo3 = [word.replace('</strong>', '') for word in opisowo2]
    return opisowo3,words4

def Cichutko(opisy):
    print("Zmniejszam literki...")
    krzyczkontent = []
    for line in opisy:
        krzyczkontent.append(str.lower(line))
    return krzyczkontent

def SpisOfert(opis,link):
    eleganckalista = []
    for id,line in enumerate(opis):
        eleganckalista.append(opis[id]+"  ----->  "+link[id])
    print("Znaleziono {} ofert".format(len(eleganckalista)))
    return eleganckalista

def NiewygodneOferty(listaSlowZakazanych, listaofert):
    newlist = []
    for line in listaofert:
        if not any(zlerzeczy in line for zlerzeczy in listaSlowZakazanych):
            newlist.append(line)
    for id,line in enumerate(newlist):
        if 'https://www.otodom.pl/oferta/' in line:
            newlist.pop(id)
    print("Zostalo {}".format(len(newlist)))
    return newlist

def PojedynczaOfertaHandler(listaSlowZakazanych, listaofert):
    okazaleoferty = []
    opis = []
    szukamy = '<p class="pding10 lheight20 large"'
    typie = [word.index('---->') for word in listaofert]
    for id, element in enumerate(listaofert):
        link = str(listaofert[id][typie[id] + 7:])
        okazaleoferty.insert(id, link)
    for id, oferta in enumerate(okazaleoferty):
        try:
            if id % 4 == 0:
                time.sleep(2)
            elif id % 11 == 0:
                time.sleep(9)
            string = ""
            url = oferta
            request = urllib.request.Request(url, data=None, headers=headers)
            f = urllib.request.urlopen(request)
            dane = f.read().decode('utf-8')
            numerlinii = dane.find(szukamy)
            for x in range(numerlinii + 34, numerlinii + 1000):
                string = string + dane[x]
            dupa = string.split("</p>")
            opis.append(dupa[0])
            print("Miele oferte nr {}".format(id + 1))
        except:
            continue
    newfile = []
    for id, line in enumerate(opis):
        if not any(zlerzeczy in line for zlerzeczy in listaSlowZakazanych):
            newfile.append(okazaleoferty[id])
    print("Zostalo {}".format(len(newfile)))
    newnewfile = []
    for link in newfile:
        if link not in newnewfile:
            newnewfile.append(link)
    print("A teraz zostalo {}".format(len(newnewfile)))
    with codecs.open("olxprzemielone.txt", "a", "utf-8") as pliq:
        for id, line in enumerate(newnewfile):
            pliq.write(newnewfile[id]+"\n")
    print("#Zrzut do pliku...")

def main():
    listaSlowZakazanych = ['psie pole', 'kromera', 'marino', 'nadodrze', 'ołtaszyn',
                           'partynice', 'jaracza', 'sołtysowice', 'jagodno', 'śródmieście',
                           'księże', 'księża', 'kamieńskiego', 'aneks', 'maślic',
                           'rędzin', 'świniar', 'biskupin', 'bartoszowic', 'sępoln',
                           'tarnogaj', "broch", 'traugutta', 'kościuszk', 'wojszyc',
                           'leśnic', 'kleczk', 'różanka', 'różance', 'antresol',
                           'salon', 'psiego pola', 'curie sklodowskiej', 'huby', 'kamienn',
                           'piec kaflow', 'ogrzewanie gazow', 'piec elektrycz', 'kamieni',
                           'sky tower', 'przechodni', 'parter', 'agencja', 'estates',
                           'stabłowic']
    lista = WyciagnijWszystkieStrony()
    oferty,opisy = WyciagnijOfertyZeStron(lista)
    pocieteopisy,pocieteoferty = CiecieWszystkichOfert(opisy,oferty)
    cichutkiopis = Cichutko(pocieteopisy)
    listaopisilink = SpisOfert(cichutkiopis,pocieteoferty)
    znowulista = NiewygodneOferty(listaSlowZakazanych, listaopisilink)
    PojedynczaOfertaHandler(listaSlowZakazanych,znowulista)
    os.system(r"copy olxprzemielone.txt C:\Users\Paweł\Desktop")
    print("#Done")

main()
