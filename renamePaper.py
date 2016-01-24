# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:34:02 2016

@author: ShiJingchang

@require:
	python packages: sys, os, subprocess
	software: curl(curl for windows can be downloaded from http://curl.haxx.se/download.html)
@sample: python renamePaper.py ../test.pdf ../Bib/Jet.bib Crow1971
"""

###################
# Rename PDF file by Bib file
def getStringBetweenSymbols(WholeStringStr, InitSymbolStr, EndSymbolStr):
	WholeStringStr = WholeStringStr.strip()
	WholeStringStr = WholeStringStr.lower()

	IndexInitSymbol = \
		[i for i, s in enumerate(WholeStringStr) if InitSymbolStr in s]
	if not IndexInitSymbol:
		return None
	IndexInitSymbol = IndexInitSymbol[0]
	IndexEndSymbol = \
		[i for i, s in enumerate(WholeStringStr) if EndSymbolStr in s]
	IndexEndSymbol = IndexEndSymbol[0]
	StringFoundStr = WholeStringStr[IndexInitSymbol+1:IndexEndSymbol]

	return StringFoundStr

def renamePaper_Core(PDFFilePathStr, BibFileContentList):
	import os

	for LineInd in range(len(BibFileContentList)):
		BibFileSingleLineStr = BibFileContentList[LineInd].strip()
		BibFileSingleLineStr = BibFileSingleLineStr.lower()
		if BibFileSingleLineStr[0:6] == "author":
			AuthorsStr = getStringBetweenSymbols( \
				BibFileSingleLineStr, "{", "}")
			if not AuthorsStr:
				AuthorsStr = getStringBetweenSymbols( \
					BibFileSingleLineStr, "\"", "\"")
				if not AuthorsStr:
					AuthorsStr = BibFileSingleLineStr[10:-2]
					if not AuthorsStr:
						print "I can not get the author information!"
						raw_input()
			AuthorsList = AuthorsStr.split()
			FirstAuthorLastNameStr = AuthorsList[-1].lower()
			FirstAuthorLastNameStr = \
				''.join(s for s in FirstAuthorLastNameStr if s.isalnum())
			for StrInd in range(len(AuthorsList)):
				if AuthorsList[StrInd] == "and":
					FirstAuthorLastNameStr = AuthorsList[StrInd-1].lower()
					FirstAuthorLastNameStr = \
						''.join(s for s in FirstAuthorLastNameStr if s.isalnum())
					break
		if BibFileSingleLineStr[0:4] == "year":
			YearStr = getStringBetweenSymbols( \
				BibFileSingleLineStr, "{", "}")
			if not YearStr:
				YearStr = getStringBetweenSymbols( \
					BibFileSingleLineStr, "\"", "\"")
				if not YearStr:
					YearStr = ''.join(e for e in BibFileSingleLineStr[7:-1] if e.isalnum())
					if not YearStr:
						print "I can not get the year information!"
						raw_input()
		if BibFileSingleLineStr[0:5] == "title":
			TitleStr = getStringBetweenSymbols( \
				BibFileSingleLineStr, "{", "}")
			if not TitleStr:
				TitleStr = getStringBetweenSymbols( \
					BibFileSingleLineStr, "\"", "\"")
				if not TitleStr:
					TitleStr = BibFileSingleLineStr[9:-2]
					if not TitleStr:
						print "I can not get the title information!"
						raw_input()
			TitleList = TitleStr.split()
			for StrInd in range(len(TitleList)):
				TitleList[StrInd] = \
					''.join(s for s in TitleList[StrInd] if s.isalnum())
			TitleStr = '_'.join(TitleList)
			TitleStr = TitleStr.lower()
	PDFFileNewNameStr = "-".join([FirstAuthorLastNameStr, YearStr, TitleStr])
	PDFFileNewNameStr = PDFFileNewNameStr + ".pdf"
	print PDFFileNewNameStr
	PDFFilePathDirStr = os.path.dirname(os.path.abspath(PDFFilePathStr))
	os.rename(PDFFilePathStr, os.path.join(PDFFilePathDirStr, PDFFileNewNameStr))

	print "Your paper file is renamed!"

def renamePaper_by_Entry(PDFFilePathStr, BibFilePathStr, EntryStr):
	import getBib

	BibFileContentList = getBib.getBibContent_from_BibFile(BibFilePathStr, EntryStr)
	renamePaper_Core(PDFFilePathStr, BibFileContentList)

def renamePaper_by_DOI(PDFFilePathStr, DOIStr, BibFilePathStr):
	import getBib

	getBib.addBibContent_by_DOI(DOIStr, BibFilePathStr)
	BibFileContentList = getBib.getBibContent_by_DOI(DOIStr, BibFilePathStr)
	renamePaper_Core(PDFFilePathStr, BibFileContentList)
	
def movePDF(FileOldPathStr):
	import os

	PapersDirStr = os.path.abspath("../Papers/")
	FileOldPathBasenameStr = os.path.basename(os.path.abspath(FileOldPathStr))
	FileNewPathStr = os.path.join(PapersDirStr, FileOldPathBasenameStr)
	os.rename(FileOldPathStr, FileNewPathStr)
	print "Your paper file is moved to the destination!"
	return FileNewPathStr

###################
# Main
if __name__ == "__main__":
	import sys

	# PDFFilePathStr = sys.argv[1]
	# BibFilePathStr = sys.argv[2]
	# EntryStr = sys.argv[3]
	# FileNewPathStr = movePDF(PDFFilePathStr)
	# renamePaper_by_Entry(FileNewPathStr, BibFilePathStr, EntryStr)
	WholeStringStr = "	author = {S. C. Crow and F. H. Champagne},"
	InitSymbolStr = "{"
	EndSymbolStr = "}"
	print getStringBetweenSymbols(WholeStringStr, InitSymbolStr, EndSymbolStr)