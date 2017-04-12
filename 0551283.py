# encoding=utf-8

import configparser
import numpy as np
from tkinter import *

# 計算 矩陣
class CalMatrix:

	def __init__(self):
		pass

	def do(self, inifile):
		file=configparser.ConfigParser()
		file.read(inifile)
		matrixdatatitle = file.options('data')
		dim = int(file['data']['n'])
		matrix = []
		for title in matrixdatatitle:
			dataraw = file['data'][title]
			if title[0] == 'r':
				raw = dataraw.split(',')
				row = []
				for r in raw:
					row.append(int(r))
				matrix.append(row)
		print("A = ")
		#print(matrix)
		npmatrix = np.array(matrix)
		print(npmatrix)
		print('show A x A')
		print(np.dot(npmatrix,npmatrix))


class Point:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

class Shape:
	def __init__(self, p1, p2, outline, bg, name):
		self.p1 = p1
		self.p2 = p2
		self.shape = None
		self.outline = outline
		self.bg = bg
		self.name = name

	def draw(self, canvas):
		self.canvas = canvas
		print('shape')

class Line(Shape):
	def __init__(self, p1, p2, outline, bg, name):
		super().__init__(p1, p2, outline, bg, name)

	def draw(self, canvas):
		super().draw(canvas)
		self.shape = self.canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.outline)

class Oval(Shape):
	def __init__(self, p1, p2, outline, bg, name):
		super().__init__(p1, p2, outline, bg, name)

	def draw(self, canvas):
		super().draw(canvas)
		self.shape = self.canvas.create_oval(self.p1.x, self.p1.y, self.p1.x+self.p2.x, self.p1.y+self.p2.y, fill=self.bg)

class Face(Shape):
	def __init__(self,p1,p2, outline, bg, name):
		super().__init__(p1,p2, outline, bg, name)

	def draw(self, canvas):
		super().draw(canvas)

		centerx = (self.p1.x + self.p2.x) / 2
		centery = self.p2.y - 20

		self.canvas.create_oval(self.p1.x,self.p1.y, self.p2.x,self.p2.y, fill=self.bg,outline=self.outline)
		# l eye
		self.canvas.create_oval(self.p1.x + 15 + 10, self.p1.y+15 + 10,self.p1.x + 35 + 10, self.p1.y+35 + 10,fill=self.outline, outline= self.bg)
		# r eye
		self.canvas.create_oval(self.p1.x + 15 + 50, self.p1.y+15+10,self.p1.x + 35 + 50, self.p1.y+35 + 10,fill=self.outline, outline= self.bg)
		# m
		self.canvas.create_line(centerx,centery, centerx + 20, centery - 10)
		self.canvas.create_line(centerx,centery, centerx - 20, centery - 10)

class Text(Shape):
	def __init__(self,p1,fontsize,fontcolor ,name):
		super().__init__(p1,Point(fontsize,0), fontcolor,'black', name)

	def draw(self, canvas):
		super().draw(canvas)
		self.shape = self.canvas.create_text(self.p1.x, self.p1.y, text = self.name,fill=self.outline, font=('微軟正黑體',self.p2.x))

class Triangle(Shape):
	def __init__(self,p1,p2, outline, bg, name):
		super().__init__(p1,p2, outline, bg, name)
		self.points = []
		self.points.append(p1)
		self.points.append(Point(self.p1.x + self.p2.x, self.p1.y + self.p2.y))
		self.points.append(Point(self.p1.x - self.p2.x, self.p1.y + self.p2.y))

	def draw(self, canvas):
		super().draw(canvas)
		self.shapeShape = self.canvas.create_polygon(self.points[0].x,self.points[0].y,self.points[1].x,self.points[1].y,self.points[2].x,self.points[2].y,outline=self.outline,fill=self.bg)


class MyFrame:

	def __init__(self,configfile):
		self.shapes = []
		self.configfile = configfile
		file = configparser.ConfigParser()
		file.read(self.configfile)
		self.width = int(file['graph']['width'])
		self.height = int(file['graph']['height'])
		self.bg = file['graph']['bg']
		self.frametitle = file['graph']['title']
		print("----Canvas config----")
		print("W:%d\nH:%d\nBG:%s" %(self.width, self.height, self.bg))
		print("--------------------")
		self.listboxdata = ["Python", "C++", "Javascript","Objective-c"]
		self.shapeTitle = ["oval", "line", "face", "triangle", "text"]



	def draw(self):
		self.root = Tk()
		self.root.title(self.frametitle)
		#self.root.geometry("%dx%d" %(self.width,self.height))
		self.root.geometry("500x500")
		self.labelshows = Label(self.root)
		self.labelshows['text'] = "土木工程系"
		self.labelshows.grid(row=1, column = 1)

		self.listbox = Listbox(self.root,width=10,height=5)

		# insert data
		for i in range(0, len(self.listboxdata)):
			self.listbox.insert(i, self.listboxdata[i])
		self.listbox.grid(row = 2, column = 2)

		self.btn1 = Button(self.root)
		self.btn1['text'] = "快點來按我吧"
		self.btn1['command'] = self.e_button
		self.btn1.grid(row = 3, column = 3)

		self.shapeFactory("0551283_1.ini")
		self.shapeFactory("0551283_2.ini")
		self.root.mainloop()


	def shapeFactory(self, datafile):
		file = configparser.ConfigParser()
		file.read(datafile)
		for shapeT in self.shapeTitle:
			if not file.has_section(shapeT):
				continue

			options = file.options(shapeT)
			for st in options:
				name = st
				data = file[shapeT][st].split(',')
				print(data)
				if("line" in shapeT):
					self.shapes.append(Line(Point(data[0],data[1]),Point(data[2],data[3]),data[4],data[5],name))
				elif("oval" in shapeT):
					self.shapes.append(Oval(Point(data[0],data[1]),Point(data[2],data[3]),data[4],data[5],name))
				elif("face" in shapeT):
					self.shapes.append(Face(Point(data[0],data[1]),Point(data[2],data[3]),data[4],data[5],name))
				elif("triangle" in shapeT):
					self.shapes.append(Triangle(Point(data[0],data[1]),Point(data[2],data[3]),data[4],data[5],name))
				elif("text" in shapeT):
					self.shapes.append(Text(Point(data[0],data[1]),data[2],data[3],data[4]))

				

	def e_button(self):
		self.root.geometry("%dx%d" %(self.width,self.height))
		self.canvas = Canvas(self.root,bg=self.bg)
		self.canvas['width'] = self.width
		self.canvas['height'] = self.height
		self.canvas.grid(row=4,column=1, columnspan = 3)
		select = 0
		if(self.listbox.curselection()):
			select = self.listbox.curselection()[0]
		
		self.labelshows['text'] = self.listboxdata[select]

		for shape in self.shapes:
			shape.draw(self.canvas)


def main():
	cm = CalMatrix()
	cm.do("0551283_1.ini")

	mf = MyFrame("0551283_1.ini")
	mf.draw()







if __name__ == "__main__":
	main()






