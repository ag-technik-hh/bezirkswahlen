#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simples Skript für die Piratenpartei Deutschland Landesverband Hamburg
Bestimmt den Wahlkreis für die Bezirkswahlen 2014."""

from csv import reader, writer
from re import match
from os.path import join

def enum(**enums):
    return type('Enum', (), enums)

Bezirke = enum(UNDEFINED = 0, HamburgMitte = 1, Altona = 2, Eimsbuettel = 3, HamburgNord = 4, Wandsbek = 5, Bergedorf = 6, Harburg = 7)
Seite = enum(GERADE = 1, UNGREADE = 2)

class Addresse(object):
	"""Datenobjekt für eine Straße aus der Datendatei"""

	class strassenSeite(object):
		"""docstring for strassenSeite"""

		bezirk = Bezirke.UNDEFINED
		stadtteil = ''
		wahlkreisnummer = -1
		wahlkreisname = ''

		def __str__(self):
			return "Bezirk: " + self.bezirk + ", Wahlkreis: " + self.wahlkreisnummer + " " + self.wahlkreisname

	ungeradeSeite = strassenSeite()
	geradeSeite = strassenSeite()

	def setData(self, dataRow):
		"Parst die Zeile aus der CSV Datei und setzt die Felder der Klasse."
		seite = self.strassenSeite()
		seite.stadtteil = dataRow[2]
		seite.wahlkreisnummer = dataRow[5]
		seite.wahlkreisname = dataRow[6]
		bezirk = int(dataRow[3]) // 100
		if bezirk == 1:
			seite.bezirk = Bezirke.HamburgMitte
		elif bezirk == 2:
			seite.bezirk = Bezirke.Altona
		elif bezirk == 3:
			seite.bezirk = Bezirke.Eimsbuettel
		elif bezirk == 4:
			seite.bezirk = Bezirke.HamburgNord
		elif bezirk == 5:
			seite.bezirk = Bezirke.Wandsbek
		elif bezirk == 6:
			seite.bezirk = Bezirke.Bergedorf
		elif bezirk == 7:
			seite.bezirk = Bezirke.Harburg
		nummern = dataRow[1].split()
		if nummern[1] == '/':
			m = match('(\d+)(\D+)', nummern[0])
			if m:
				start = nummern[0][:-1]
			else:
				start = nummern[0]
			if (int(start) % 2) == 0:
				self.geradeSeite = seite
			else:
				self.ungeradeSeite = seite
		elif nummern[1] == '-':
			self.ungeradeSeite = seite
			self.geradeSeite = seite

	def __str__(self):
		return "Gerade: " + self.geradeSeite + ", Ungerade: " + self.ungeradeSeite

wahlkreisDaten = dict()


def readData(filename = join('data', 'Strassenverzeichnis_HH_insgesamt_BVWahl2014.csv')):
	"""Datendatei lesen"""
	with open(filename) as dataFile:
		dataReader = reader(dataFile, delimiter=';', quotechar='"')
		print("lese Datei:", filename)
		count = 0
		for row in dataReader:
			count += 1
			try:
				adresse = wahlkreisDaten[row[0]]
			except KeyError:
				adresse = Addresse()
				wahlkreisDaten[row[0]] = adresse
			adresse.setData(row)
		print(count, "Datensätze gelsen")

def processMembers(memberInputFile = 'memberInput.csv', memberOutputFile = 'memberOutput.csv', memberErrorFile = 'memberError.csv'):
	"""Mitgliederdaten lesen und verarbeiten"""
	memberInput = open(memberInputFile)
	memberReader = reader(memberInput, delimiter=';', quotechar='"')
	memberOutput = open(memberOutputFile, 'w')
	memberWriter = writer(memberOutput, delimiter=';', quotechar='"')
	memberError = open(memberErrorFile, 'w')
	memberErrorWriter = writer(memberError, delimiter=';', quotechar='"')
	print("verarbeite Mitglieder aus:", memberInputFile)
	count = 0
	for row in memberReader:
		count += 1
		adresse = row[FeldIndex.addr_address1]
		m = match('^(\D+) (\d+)(\D?)$', adresse)
		try:
			wahlkreisEintrag = wahlkreisDaten[m.group(1)]

			if int(m.group(2)) % 2 == 0:
				seite = wahlkreisEintrag.geradeSeite
			else:
				seite = wahlkreisEintrag.ungeradeSeite

			row[FeldIndex.comp_user_gemeinde] = seite.stadtteil
			row[FeldIndex.comp_user_lvfreitext1] = seite.wahlkreisname + ' (' + seite.wahlkreisnummer + ')'

			memberWriter.writerow(row)
		except KeyError:
			memberErrorWriter.writerow(row)
	print(count, "Mitglieder verarbeitet")

def main():
	readData()
	processMembers()

if __name__ == '__main__':
	main()
