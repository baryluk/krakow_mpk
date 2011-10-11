#!/usr/bin/python
# -- encoding: UTF-8 --

"""
==== Globalne (linie, ulice i przystanki) ====

Linie:
linie.html

Wszystkie Ulice: (numeracja UID jest alfabetyczna)
aktualne/ulice.html

Przystanki przy danej ulicy:
aktualne/u/uUID.html
(ostatni link prowadzi do ulice.html)

Wszystkie Przystanki:
aktualne/przystan.html

Linie wyjezdzajace z danego przystanku:
aktualne/p/pPID.html
(linki prowadzą do ramek tam/spowrotem LID/LIDrw01.html lub LID/LIDrw02.html; ostatni link prowadzi do przystan.html)

==== Informacja o konkretnej linii ====

Pusty plik (do prawej ramki w LIDrw0?.html):
aktualne/LID/0.html

Przystanki na linii tam (do lewej ramki w LIDr???.html oraz LIDrw01.html):
aktualne/LID/LIDw001.html
(linki prowadzą do ramek LIDr001-0024.html, które wskazują na L=LIDw001.html#NUM, R=LIDtNUM.html,
są też linki do linii wyjeżdzających z przystanku ../p/pPID.html, oraz link do ramki spowrotem LIDrw02.html)

Przystanki na linii spowrotem (do lewej ramki w LIDr???.html oraz LIDrw02.html):
aktualne/LID/LIDw002.html

Tabele linii na przystanku (tam i spowrotem, do prawych ramek LIDr???.html):
aktualne/LID/LIDt001.html
...
aktualne/LID/LIDt047.html

Ramki tam (L=0194w001.htm#024 R=0194t024.htm):
aktualne/LID/LIDr001.html
...
aktualne/LID/LIDr024.html

Ramki spowrotem (L=0194w002.htm#047 R=0194t047.htm):
aktualne/LID/LIDr025.html
...
aktualne/LID/LIDr047.html

Ramka tam (L=LIDw001.html R=0.html):
aktualne/LID/LIDrw01.html

Ramka spowrotem (L=LIDw002.html R=0.html):
aktualne/LID/LIDrw02.html

==== Parsowanie ====
Ramki zupełnie nas nie obchodzą.

==== Tabele ====
"""

# UID -> Nazwa ulicy
# (wszystkie nazwy ulic)
ulice = {}

# UID -> [PID]
# (przystanki przy ulicy)
przystanki_przy_ulicy = {}

# PID -> Nazwa przystanku
# (wszystkie nazwy przystankow)
przystanki = {}

# PID -> [LID] (wlaczajac kierunek)
# (linie na przystanku danej nazwy)
linie_przy_przystanku = {}

# LID -> [PID]
# (przystanki na lini, tam/spowrotem)
linie = {}

# (czasy odjazdow w dzien, sobote, niedziele)
tabela = {}


wpisow = 0


from xml.dom import minidom

def parsuj_listeulic(FILE):
	t = minidom.parse(FILE)
	
	ret = []
	
	# html/body/table/tr/td/table/
	wiersze = t.childNodes[1].childNodes[1].childNodes[1].childNodes
	i = 0
	for wiersz in wiersze:
		if i == 0:
		    0
		if i > 0:
			if wiersz.getAttribute("bgcolor") != "#87CEFA":
				for subwiersze in wiersz.childNodes[0].childNodes[0].childNodes:
					ret.append((int(subwiersze.childNodes[0].getAttribute("href")[3 : -4]), subwiersze.childNodes[0].childNodes[0].data))
		i += 1
	
	return ret


print "Lista ulic (parsing)..."
ulice0 = parsuj_listeulic("ulice.htm")

ulice = {}
ulice.update(ulice0)

ulice_rev = {}
ulice_rev.update(map(lambda (uid, nazwa_ulicy): (nazwa_ulicy, uid), ulice0))
print "done."

#for uid, nazwa_ulicy in ulice:
#	parsuj_ulice("u/u%s.htm", toID4(uid))

def toID4(ID):
    return "%04d" % (ID)

def toID3(ID):
    return "%03d" % (ID)

def parsuj_listeprzystankow(FILE):
	t = minidom.parse(FILE)
	
	ret = []

	# html/body/table/tr/td/table/
	#wiersze = t.childNodes[1].childNodes[1].childNodes[1].childNodes
	wiersze = t.childNodes[1].childNodes[1].childNodes[3].childNodes
	i = 0
	for wiersz in wiersze:
		if i == 0:
		    0
		if i > 0:
			if wiersz.getAttribute("bgcolor") != "#87CEFA":
				for subwiersze in wiersz.childNodes[0].childNodes[0].childNodes:
					ret.append((int(subwiersze.childNodes[0].getAttribute("href")[3 : -4]), subwiersze.childNodes[0].childNodes[0].data))
		i += 1
	
	return ret

print "Lista przystankow (parsing)..."
przystanki0 = parsuj_listeprzystankow("przystan.htm")

przystanki = {}
przystanki.update(przystanki0)

przystanki_rev = {}
przystanki_rev.update(map(lambda (pid, nazwa_przystanku): (nazwa_przystanku, pid), przystanki0))
print "done."

def parsuj_liste(FILE):
    p = file(FILE)
    return map(lambda x: int(x), p.read().split())

def parsuj_linie(FILE, LID, DID):
	t = minidom.parse(FILE)
	
	ret = []
	
	# html/body/table/tr/td/table/tr/td/ul/
	wiersze = t.childNodes[1].childNodes[1].childNodes[0].childNodes[1].childNodes[0].childNodes[0].childNodes
	i = 0
	for wiersz in wiersze:
		try:
			if len(wiersz.childNodes) == 4:
				a = wiersz.childNodes[1]
				a2 = wiersz.childNodes[3]
				numer_przystanku_na_linii = int(a.getAttribute("href")[5 : -4])
				pid = int(a2.getAttribute("href")[6 : -4])
				if i == 0:
					ret.append((numer_przystanku_na_linii, a.childNodes[0].childNodes[0].data, pid, 'B'))
				else:
					ret.append((numer_przystanku_na_linii, a.childNodes[0].data, pid, ''))
			else:
				ID = -1
				ret.append((numer_przystanku_na_linii, wiersz.childNodes[0].childNodes[0].data, -1, 'L'))
		except:
			pass
		i += 1
	
	return ret

def parsuj_tabele(FILE, LID, DID, KID):
	global wpisow
	
	t = minidom.parse(FILE)
	
	# html/body/table/tr/td/table/
	opisnode = t.childNodes[1].childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0]
	
	numer_linii = int(opisnode.childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].data)
	przystanek = opisnode.childNodes[0].childNodes[1].childNodes[0].childNodes[0].childNodes[0].data
	trasa = opisnode.childNodes[0].childNodes[1].childNodes[3].toxml()
	
	# html/body/table/tr/td/table
	wiersze = t.childNodes[1].childNodes[1].childNodes[0].childNodes[1].childNodes[0].childNodes[0].childNodes
	bylyflagi = False
	i = 0
	ret = []
	wierszy = len(wiersze)
	for wiersz in wiersze:
		if i == 0:
			for kolumna in wiersz.childNodes:
				# b/font/
				dzien = kolumna.childNodes[0].childNodes[0].childNodes[0].data
				# 300kB mniej (8%)
				m = {
					u"Pon.-Czw.": "14",
					u"Święta": "7",
					u"Dzień powszedni": "15",
					u"Soboty": "6",
					u'Pt./Sob.,Sob./\u015aw.': "56",
					u'Pt./Sob., Sob./\u015aw.': "56"
				}
				ret.append([m[dzien]])
		if i > 0:
			l = len(wiersz.childNodes)
			for j in range(l/2):
				# td/b/
				kolumna1 = wiersz.childNodes[2*j].childNodes[0].childNodes[0].data
				# td/
				kolumna2 = wiersz.childNodes[2*j+1].childNodes[0].data
				godzina = int(kolumna1)
				if (kolumna2 != " -"):
					for minuta in kolumna2.split():
						if not ('0' <= minuta[-1] <= '9'):
							flaga = minuta[-1:]
							minutar = minuta[0:-1]
						else:
							flaga = ""
							minutar = minuta
						
						czas = 60*godzina + int(minutar) # zmniejsza rozmiar pliku o 50% (4.5 MB)
						if (flaga != ""): # costam
							ret[j].append((czas, flaga))
							bylyflagi = True
						else:
							#ret[j].append((godzina, int(minuta), ""))
							# zmniejsza rozmiar pliku o 20% (300kB)
							ret[j].append(czas)
						wpisow += 1
			if l == 1: # legenda (ostatni wiersz)
				legenda_node = wiersz.childNodes[0]
			
		i += 1
	
	legenda = {}
	if bylyflagi:
		assert len(legenda_node.childNodes) > 8 and len(legenda_node.childNodes) % 2 == 0
		if len(legenda_node.childNodes) > 8:
			flag = (len(legenda_node.childNodes) - 8)/2
			for i in range(flag):
				text = legenda_node.childNodes[4+2*i].data
				flaga = text[0]
				flaga_opis = text[4:]
				legenda[flaga] = flaga_opis
				# typy:
				# Kurs do przystanku: X
				# Kurs przez: X
				# Kurs przez: X, X2, X3
				# kurs przez U
				# (linia 235, 238, 278) A - Nie kursuje przez: X, X2
				# (linia 230) T - kurs wykonuje autobus lini XXX
				# w okresie kwiecień - październik kurs z bagażnikiem dla rowerów
				# zatrzymuje sie na przystanku: Z
				# kurs realizowany z bagażnikiem dla rowerów
				# (linia 145) C - kurs wykonuje aut. linii 225 (nie zatrzymuje się na przystanku: Góra Borkowska) ; na przystanku: Swoszowice Sklep przesiadka na aut. linii 145 do Golkowic
				# (linia 158) s - w dni nauki szkolnej kursuje przez: Płaszów Szkoła
				# (linia 158) s - kurs realizowany w dni nauku szkolnej
				# (linia 166) A - Kurs do Sidziny przez Skotniki Szkołę (pętla l. 106).
				# (linia 166) A - Kurs przez Skotniki Szkołę (petla l. 106).
				# (linia 184) s - zatrzymuje się na przystanku: Malborska Szkoła (następny po przystanku Wola Duchacka).
				# (linia 222) p - Kurs przez: Pękowice
				# (linia 222) B - Kurs do przystanku: Giebułtów Morgi przez: Pękowice
				# (linia 222) p - p. Pękowice do przystanku: Giebułtów
				# (linia 225) a - Kurs od przystanku Świątniki Górne
				# (linia 225) C - na przystanku: "Swoszowice Sklep" przesiadka na linię 145 do Golkowic
				# (linia 238) B - Kurs do przystanku: Motel Krak. Nie kursuje przez: Rudawa Kościół
				# (linia 240) p - kurs wykonuje autobus linii 220
				# (linia 239) A - Kurs do przystanku: Jeziorzany przez: Jeziorzany, Grotowa
				# (linia 239) B - Kurs do przystanku: Jeziorzany przez: Jeziorzany, Powieszon, Wołowice
				# (linia 245) A - Kurs autobusu linii 275 do przystanku Włosań przez Buków, Chorowice
				# (linia 245) x - kurs z pominięciem Chorowic
				# (linia 247) A - Kurs do przystanku: Nowy Kleparz przez: Bibice Pętla
				# (linia 248) C - Kurs w dni nauki szkolnej do Zelkowa przez Zabierzów Gimnazjum, Bolechowice.
				# (linia 248) D - Kurs w dni nauki szkolnej.
				# (linia 248) F - Kurs w dni wolne od nauki szkolnej.
				# (linia 254) x - kurs z pominięciem Wróżenic.
				# (linia 254) W - kurs do Wróżenic
				# (linia 409) n - kursuje w dniach: 1.03, 15.03, 29.03, 19.04, 10.05, 24.05, 7.06.2009
				# (linia 409) s - kursuje w dniach: 28.02, 14.03, 28.03, 18.04, 9.05, 23.05, 6.06.2009
	
	return (numer_linii, przystanek, trasa, ret, legenda)

# dziwne linie, m.in.: 107 (s, 3 trasy), 110 (B, 5 tras), 111 (R, 4 trasy), 112 (C, 7 tras), 210(r), 230 (T), 239 (D)
# mniej dziwne: 100 (r)

# grep HREF ../linie.html | awk -F '<|>' '{print $3}' >> ../linie.txt
linie = parsuj_liste("../linie.txt")

rozklad_na_przystanku = {}

# pid - id przystanku
# lid - id linii (numer linii)
# kid - id przystanku na trasie
# did - id kierunku (1, 2)

# tak samo tylko duzo litery ->
#   pid,kid,did -> "1" -> "001"
#   lid -> "194" -> "0194"

def parsuj_i_dodaj(numer_linii, LID, numer_przystanku_na_trasie, nazwa_przystanku, pid, flagi, DID):
	if (numer_przystanku_na_trasie > 0 and flagi != 'L'):
		KID = toID3(numer_przystanku_na_trasie)
		(numer_linii2, nazwa_przystanku2, trasa_linii, rozklad, legenda) = parsuj_tabele("%s/%st%s.htm" % (LID, LID, KID), LID, DID, KID)
		
		#print numer_linii, LID, numer_przystanku_na_trasie, nazwa_przystanku, flagi, DID
		#print numer_linii2, nazwa_przystanku2, trasa_linii
		#print rozklad
		trasa_linii = '' # wyrzucamy z oszczednosci miejsca, plik o 1.3MB mniejszy (30%)
		a = (numer_linii, LID, numer_przystanku_na_trasie, nazwa_przystanku, flagi, DID, KID, numer_linii2, nazwa_przystanku2, trasa_linii, rozklad, legenda)
		if pid not in rozklad_na_przystanku:
			rozklad_na_przystanku[pid] = ((nazwa_przystanku), [])
		rozklad_na_przystanku[pid][1].append(a)

import cPickle

try:
    print "Loading linie..."
    rozklad_na_przystanku = cPickle.load(file("rozklady.pickle"))
    print "done."
except:
	print "Linie (parsing)..."
	for numer_linii in linie:
		LID = toID4(numer_linii)
		print LID
	
		linia1 = parsuj_linie("%s/%sw001.htm" % (LID, LID), LID, "001")
		for (numer_przystanku_na_trasie, nazwa_przystanku, pid, flagi) in linia1:
			parsuj_i_dodaj(numer_linii, LID, numer_przystanku_na_trasie, nazwa_przystanku, pid, flagi, "001")
		
		if numer_linii != 405 and numer_linii != 424 and numer_linii != 425:
			linia2 = parsuj_linie("%s/%sw002.htm" % (LID, LID), LID, "002")
			for (numer_przystanku_na_trasie, nazwa_przystanku, pid, flagi) in linia2:
				parsuj_i_dodaj(numer_linii, LID, numer_przystanku_na_trasie, nazwa_przystanku, pid, flagi, "002")
	print "done."
	print "Dumping..."
	cPickle.dump(rozklad_na_przystanku, file("rozklady.pickle", 'w'), 2) # wersja 2, zmniejsza plik o 25%
	print "done."

#file("r2.repr", 'w').write(repr(rozklad_na_przystanku))

if 1:
	pid = przystanki_rev[u'Konopnickiej']
	v = rozklad_na_przystanku[pid]
	print v[0]
	print
	for v1 in v[1]:
		print v1
		print

# rekonstrukcja kursow
# zaczynamy od przystanku poczatkowe, i szukamy dla kazdego odjazdu, odjazdu niemniejszego na nazstepnym przystanku
# (flagi powinny byc takie same)
#
# problem jest z ostatnim przystankiem, poniewaz nie wiemy kiedy przyjezdza kurs na ostatni przystanek (w tabeli sa tylko czasy odjazdow,
# a na ostatnim przystanku nie ma odjazdow przeciez)
# mozemy albo poprostu dac czas przejazdu 1 minuta
# albo uzyc czasu prezjazdu w druga strone

# rekonstrukcja w niektorych przypadkach jest utrdniona. przyklad:
# linia 215, z rzesztotary panciawa, przystanek swiatniki gorne, godzina 7:42. on nie wyjezdza z rzesztotary, tylko dopiero z swiatnikow gornych
# musimy wiec nie tylko dopasowac godzine ale i flagi, przy czym byc moze niezbedne jest uwazanie na semantyke.
# np. flaga A oznaczajaca przejazd przez jakis przystanek X, byc moze nie jest pokazywana w rozkladzie juz za przystanek X
# (nie jest to informacja niezbedna do dalszej jazdy)
# niektora sa przekomibnowana. np. T, r na lini 230 / 210. (czesc linii wykonywana przez autobus z innym numerem)
# albo 124 na w kierunku Ruczaj, na 5 pierwszych przystankach (rozne trasy, potem sie lacza)
