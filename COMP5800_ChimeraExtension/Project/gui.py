import os
import Tkinter
Tk = Tkinter
import chimera
from chimera.baseDialog import ModelessDialog
import re
MAINCHAIN = re.compile("^(N|CA|C|O)$", re.I)

ui = None

def showUI(callback=None):
	global ui

	if not ui:
		ui = Project()
	ui.enter()
	if callback:
		ui.addCallback(callback)
def initMenu():
	chimera.dialogs.register(Project.name, Project)
	label = {'label':"Mustafa"}
	menu = Tk.Menu(None, type="menubar", tearoff=False)
	menu.add_command(label="Project1", underline=0,command=showUI)
	chimera.tkgui.addMenu(menu, **label)
	
class Project(ModelessDialog):

	name = "Project 1"
	title = 'Project 1'
	buttons = ("Close")
	
	def fetchit(self):
		fetchById(fetchtxtval.get(), "PDBID")
	def fillInUI(self, parent):	
		global q2txtval,q3txtval,q4txtval,q5txt1val,q5txt2val,q6txt1val,q6txt2val,q6txt3val,q6txt4val,outputval,fetchtxtval
	
		
		fetchtxtval = Tkinter.StringVar(parent)
		fetchlbl = Tkinter.Label(parent, text='Fetch By ID:').grid(column=0, row=0, sticky=Tkinter.W)
		fetchtxt = Tkinter.Entry(parent, width=15, textvariable=fetchtxtval)
		fetchtxt.grid(column=1, row=0, sticky=Tkinter.W, columnspan=4)
		fetchbtn = Tkinter.Button(parent,text="Fetch",command=self.fetchit)
		fetchbtn.grid(column=5, row=0)
		
		
		q2txtval = Tkinter.StringVar(parent)
		q2 = Tkinter.Label(parent, text='2. Number of atoms in aa:').grid(column=0, row=1, sticky=Tkinter.W)
		q2txt = Tkinter.Entry(parent, width=5, textvariable=q2txtval)
		q2txt.grid(column=1, row=1)
		q2btn = Tkinter.Button(parent,text="Do it!",command=self.q2).grid(column=5, row=1)
		
		q3txtval = Tkinter.StringVar(parent)
		q3 = Tkinter.Label(parent, text='3. Number of atoms in aa\' side chain:').grid(column=0, row=2, sticky=Tkinter.W)
		q3txt = Tkinter.Entry(parent, width=5, textvariable=q3txtval)
		q3txt.grid(column=1, row=2)
		q3btn = Tkinter.Button(parent,text="Do it!",command=self.q3).grid(column=5, row=2)
		
		q4txtval = Tkinter.StringVar(parent)
		q4 = Tkinter.Label(parent, text='4. Number of aa in the chain:').grid(column=0, row=3, sticky=Tkinter.W)
		q4txt = Tkinter.Entry(parent, width=5, textvariable=q4txtval)
		q4txt.grid(column=1, row=3)
		q4btn = Tkinter.Button(parent,text="Do it!",command=self.q4).grid(column=5, row=3)
		
		q5txt1val = Tkinter.StringVar(parent)
		q5 = Tkinter.Label(parent, text='5. Coordinates of atom aa and name of atom:').grid(column=0, row=4, sticky=Tkinter.W)
		q5txt1 = Tkinter.Entry(parent, width=5, textvariable=q5txt1val)
		q5txt1.grid(column=1, row=4)
		q5txt2val = Tkinter.StringVar(parent)
		q5txt2 = Tkinter.Entry(parent, width=5, textvariable=q5txt2val)
		q5txt2.grid(column=2, row=4)
		q5btn = Tkinter.Button(parent,text="Do it!",command=self.q5).grid(column=5, row=4)
		
		q6 = Tkinter.Label(parent, text='6. distance between two atoms:').grid(column=0, row=5, sticky=Tkinter.W)
		q6txt1val = Tkinter.StringVar(parent)
		q6txt1 = Tkinter.Entry(parent, width=5, textvariable=q6txt1val)
		q6txt1.grid(column=1, row=5)
		q6txt2val = Tkinter.StringVar(parent)
		q6txt2 = Tkinter.Entry(parent, width=5, textvariable=q6txt2val)
		q6txt2.grid(column=2, row=5)
		q6txt3val = Tkinter.StringVar(parent)
		q6txt3 = Tkinter.Entry(parent, width=5, textvariable=q6txt3val)
		q6txt3.grid(column=3, row=5)
		q6txt4val = Tkinter.StringVar(parent)
		q6txt4 = Tkinter.Entry(parent, width=5, textvariable=q6txt4val)
		q6txt4.grid(column=4, row=5)
		q6btn = Tkinter.Button(parent,text="Do it!",command=self.q6).grid(column=5, row=5)

		outputval = Tkinter.StringVar(parent)
		output = Tkinter.Label(parent, textvariable=outputval).grid(column=0, row=9, columnspan=5, sticky=Tkinter.W)
		

	def findAAbySeq(self,seqnum):
		for m in chimera.openModels.list(modelTypes=[chimera.Molecule]):
			for res in m.residues:
				if res.id.position == int(seqnum):
					return res
					
	def findNumAAinChain(self,chain):
		count = 0
		for m in chimera.openModels.list(modelTypes=[chimera.Molecule]):
			for res in m.residues:
				if res.id.chainId == chain and res.type != None and res.type != "HOH" and res.isHet != True and res.id.insertionCode.isspace():
					count = count + 1
		return str(count)
	def q2(self):
		residue = self.findAAbySeq(q2txtval.get())
		outputval.set("Number of atoms in "+ residue.type +": " + str(residue.numAtoms))
		print residue.id, residue.id.chainId
	def q3(self):
		residue = self.findAAbySeq(q3txtval.get())
		count = 0
		for a in residue.atoms:
			if MAINCHAIN.match(a.name) == None:
				count = count + 1
		outputval.set("Number of atoms in the side chain: " + str(count))
	def q4(self):
		chainid = q4txtval.get()
		outputval.set("Number of AA in chain "+ chainid+ " is " +self.findNumAAinChain(chainid))
	def q5(self):
		residue = self.findAAbySeq(q5txt1val.get())
		atom = residue.findAtom(q5txt2val.get())
		outputval.set(str(atom.coord()))
	def q6(self):
		residue1 = self.findAAbySeq(q6txt1val.get())
		a1 = residue1.findAtom(q6txt2val.get())
		residue2 = self.findAAbySeq(q6txt3val.get())
		a2 = residue2.findAtom(q6txt4val.get())
		dist = []
		d = a1.xformCoord().distance(a2.xformCoord())
		dist.append((d, a1, a2))
		d1, a1, a2 = min(dist)
		outputval.set('Minimum distances '+ str(d1) + ' between '+ str(a1.oslIdent())+ ' and '+ str(a2.oslIdent()))

def fetchById(IDcode, IDtype):
	chimera.tkgui.openPath(IDcode, IDtype)