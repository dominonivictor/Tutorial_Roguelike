from random import randint
from constants import get_constants

const = get_constants()

class Rect:
	'''
	Class that makes any kind of Rectangle in game, makes random size rooms
	text boxes?, Area of effect spells?, random scenery?
	'''
	def __init__(self, typ):
		#random width and height depending on type
		w = randint(const[typ+'_min_size'], const[typ+'_max_size'])
		h = randint(const[typ+'_min_size'], const[typ+'_max_size'])
		#random position w/out going out of bounds, FOR ROOMS
		x = randint(0, const['map_width'] - w - 1)
		y = randint(0, const['map_height'] - h - 1)

		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		self.size = w * h
		self.typ = typ

	def center(self):
		center_x = int((self.x1 + self.x2)/2)
		center_y = int((self.y1 + self.y2)/2)
		return (center_x, center_y)

	def intersect(self, other):
		'''
		Given another room, returns True if they intersect
		'''
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)