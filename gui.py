# Can not handle Chinese
import Tkinter, tkFileDialog

global BibFilePathStr
BibFilePathStr = "../Bib/all.bib"

def getPdfFile_by_askopen():
	global PDFFilePathStr
	PDFFilePathStr = tkFileDialog.askopenfilename()

def getBibFile_by_askopen():
	BibFilePathStr = tkFileDialog.askopenfilename()

def addBibContent_by_DOI():
	import getBib
	DOIStr = DOIInstance.get()
	getBib.addBibContent_by_DOI(DOIStr, BibFilePathStr)
	print "Successfully add Bib content to File!"

def renamePaper_by_Entry():
	import renamePaper
	EntryStr = BibEntryInstance.get()
	FileNewPathStr = renamePaper.movePDF(PDFFilePathStr)
	renamePaper.renamePaper_by_Entry(FileNewPathStr, BibFilePathStr, EntryStr)

def renamePaper_by_DOI():
	import renamePaper
	DOIStr = DOIInstance.get()
	FileNewPathStr = renamePaper.movePDF(PDFFilePathStr)
	renamePaper.renamePaper_by_DOI(FileNewPathStr, DOIStr, BibFilePathStr)

# Main GUI
root = Tkinter.Tk()
Frame_Functions_Row = [0, 1, 2]
Frame_Functions_Col = [0, 1]
Frame_Functions = Tkinter.Frame(root).grid( \
	row=Frame_Functions_Row[0], column=Frame_Functions_Col[0], \
	rowspan=Frame_Functions_Row[-1]+1, columnspan=Frame_Functions_Col[-1]+1)
Button_AddBibContent_by_DOI = Tkinter.Button( \
	Frame_Functions, text="Add Bib Content by DOI", \
	command=addBibContent_by_DOI \
	).grid(row=Frame_Functions_Row[0])
Button_RenamePaper_by_Entry = Tkinter.Button( \
	Frame_Functions, text="Rename Paper by Bib Entry", \
 	command=renamePaper_by_Entry \
 	).grid(row=Frame_Functions_Row[1])
Button_RenamePaper_by_DOI = Tkinter.Button( \
	Frame_Functions, text="Rename Paper by DOI", \
 	command=renamePaper_by_DOI \
 	).grid(row=Frame_Functions_Row[2])

Frame_Input_Row = [0, 1, 2]
Frame_Input_ColBase = Frame_Functions_Col[-1]+1
Frame_Input_Col = [Frame_Input_ColBase, Frame_Input_ColBase+1]
Frame_Input = Tkinter.Frame(root).grid( \
	row=Frame_Input_Row[0], column=Frame_Input_Col[0], \
	rowspan=Frame_Input_Row[-1]+1, columnspan=Frame_Input_Col[-1]+1)
LabelDOI = Tkinter.Label( \
	Frame_Input, text="DOI" \
	).grid(row=Frame_Input_Row[0], column=Frame_Input_Col[0])
DOIInstance = Tkinter.StringVar()
EntryDOI = Tkinter.Entry(Frame_Input, textvariable=DOIInstance \
	).grid(row=Frame_Input_Row[0], column=Frame_Input_Col[1])
LabelBibEntry = Tkinter.Label( \
	Frame_Input, text="Bib Entry" \
	).grid(row=Frame_Input_Row[1], column=Frame_Input_Col[0])
BibEntryInstance = Tkinter.StringVar()
EntryBibEntry = Tkinter.Entry(Frame_Input, textvariable=BibEntryInstance \
	).grid(row=Frame_Input_Row[1], column=Frame_Input_Col[1])
Button_SelectPdfFile = Tkinter.Button( \
	Frame_Input, text="Select PDF File", \
 	command=getPdfFile_by_askopen \
 	).grid(row=Frame_Input_Row[2], column=Frame_Input_Col[0])
Button_SelectBibFile = Tkinter.Button( \
	Frame_Input, text="Select Bib File", \
 	command=getBibFile_by_askopen \
 	).grid(row=Frame_Input_Row[2], column=Frame_Input_Col[1])





# Show main GUI
root.mainloop()