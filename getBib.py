# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:34:02 2016

@author: ShiJingchang

@require:
	python packages: sys, os, subprocess
	software: curl(curl for windows can be downloaded from http://curl.haxx.se/download.html)
@sample: python getBib.py 10.1016/j.physd.2003.03.001 tmp.bib
"""

###################
def addBibContent_by_DOI(DOIStr, BibFilePathStr):
	import subprocess

	CommandGetBib_ExecStr = "curl.exe"
	CommandGetBib_ParametersStr = "-LH"
	CommandGetBib_AcceptHeaderStr = "\"Accept: application/x-bibtex\""
	CommandGetBib_DOIStr = "http://dx.doi.org/" + DOIStr
	CommandGetBibStr = ' '.join([CommandGetBib_ExecStr, \
		CommandGetBib_ParametersStr, \
		CommandGetBib_AcceptHeaderStr, \
		CommandGetBib_DOIStr])

	BibContentStr = \
		subprocess.Popen(CommandGetBibStr, stdout=subprocess.PIPE).communicate()[0]
	
	BibFile = open(BibFilePathStr, "a")
	BibFile.write(BibContentStr)
	BibFile.write("\n")
	BibFile.close()

def getBibContent_by_DOI(DOIStr, BibFilePathStr):
	import sys

	BibFile = open(BibFilePathStr, "r")
	BibFileContentList = BibFile.readlines()
	BibFile.close()

	for StringInd in range(len(BibFileContentList)):
		BibFileContentList[StringInd] = \
			BibFileContentList[StringInd].lower()
	DOIStr = DOIStr.lower()
	
	UrlEntryStrMatchedIndexList = \
		[i for i, s in enumerate(BibFileContentList) if "url" not in s]
	BibFileContentNoUrlList = \
		[BibFileContentList[i] for i in UrlEntryStrMatchedIndexList]
	DoiEntryStrMatchedIndexList = \
		[i for i, s in enumerate(BibFileContentNoUrlList) if "doi" in s]
	BibFileContentNoUrlWithDoiList = \
		[BibFileContentNoUrlList[i] for i in DoiEntryStrMatchedIndexList]
	DOIStrMatchedIndexList = \
		[i for i, s in enumerate(BibFileContentNoUrlWithDoiList) if DOIStr in s]
	if len(DOIStrMatchedIndexList) != 1:
		print "Error! Duplicate Bib entries!"
		print DOIStrMatchedIndexList
		sys.exit()
	DoiLineMatchedStr = \
		BibFileContentNoUrlWithDoiList[DOIStrMatchedIndexList[0]]
	DoiLineMatchedIndexList = \
		[i for i, s in enumerate(BibFileContentList) if DoiLineMatchedStr in s]
	if len(DoiLineMatchedIndexList) != 1:
		print "Error! Duplicate Bib entries!"
		print DoiLineMatchedIndexList
		sys.exit()
	DoiLineMatchedIndex = DoiLineMatchedIndexList[0]
	# Find the beginning bracket
	BibContentSearchedList = BibFileContentList[0:DoiLineMatchedIndex]
	LineNMAX = len(BibContentSearchedList)
	for Ind in range(LineNMAX):
		LineInd = LineNMAX-1 - Ind
	 	CurrentLineStr = BibContentSearchedList[LineInd].strip()
	 	if any("{" in s for s in CurrentLineStr):
	 		print "The beginning bracket exists!"
	 		if any("}" in s for s in CurrentLineStr):
	 			print "The ending bracket exists!\nSo this line is not the beginning line!"
 			else:
 				print "This line is the beginning line!"
	 			BeginningLineInd = LineInd
	 			break
	# Find the ending bracket
	BibContentSearchedList = BibFileContentList[DoiLineMatchedIndex:]
	for LineInd in range(len(BibContentSearchedList)):
	 	CurrentLineStr = BibContentSearchedList[LineInd].strip()
	 	if CurrentLineStr[0] == "}":
	 		EndingLineInd = LineInd + DoiLineMatchedIndex + 1
	 		break
	BibContentMatchedList = BibFileContentList[BeginningLineInd:EndingLineInd]

	return BibContentMatchedList

def getBibContent_from_BibFile(BibFilePathStr, EntryStr):
	import sys

	BibFile = open(BibFilePathStr, "r")
	BibFileContentList = BibFile.readlines()
	BibFile.close()

	BibEntryMatchedIndexList = [i for i, s in enumerate(BibFileContentList) if EntryStr in s]
	if len(BibEntryMatchedIndexList) != 1:
		print "Error! Duplicate Bib entries!"
		print BibEntryMatchedIndexList
		sys.exit()
	BibEntryMatchedIndex = BibEntryMatchedIndexList[0]
	BibContentSearchedList = BibFileContentList[BibEntryMatchedIndex:]
	for LineInd in range(len(BibContentSearchedList)):
		CurrentLineStr = BibContentSearchedList[LineInd].strip()
		if CurrentLineStr[0] == "}":
			EndingLineInd = LineInd + BibEntryMatchedIndex + 1
			break
	BibContentMatchedList = BibFileContentList[BibEntryMatchedIndex:EndingLineInd]

	return BibContentMatchedList

###################
# Main
if __name__ == "__main__":
	import sys
	DOIStr = sys.argv[1]
	BibFilePathStr = sys.argv[2]
	print getBibContent_by_DOI(DOIStr, BibFilePathStr)
