#!/usr/bin/python3
class Node:
	def __init__(self, prev = None, next = None, data = None):
		self.data = data
		self.prev = prev
		self.next = next

class ListIteratorForward:
	def __init__(self, node):
		self.current = node

	def __iter__(self):
		while self.current is not None:
			yield self.current.data
			self.current = self.current.next

class ListIteratorBackward:
	def __init__(self, node):
		self.current = node

	def __iter__(self):
		while self.current is not None:
			yield self.current.data
			self.current = self.current.prev


class Linked:
	def __init__(self, first = None, last = None):
		self.first = first
		self.last = last
		self.size = 0

	def insert(self, data, index = 0):
		if index > self.size:
			print("insert: Index out of range")
			return

		if index == 0 and self.size == 0:
			node = Node(None, None, data)
			self.first = node
			self.last = node
			self.size += 1
			return

		elif index == 0 and self.size > 0:
			print("insert: List is not empty")
			return

		node = self.first
		i = 1
		while i < index:
			node = node.next
			i += 1
		if node.prev is not None and node.next is not None or node == self.last and self.size > 1:
			new_node = Node(node.prev, node, data)
			node.prev.next = new_node
			node.prev = new_node
			self.size += 1
		elif node == self.first:
			new_node = Node(None, node, data)
			node.prev = new_node
			self.first = new_node
			self.size += 1

	def delete(self, index=1):
		if self.first is None:
			print("delete: List is empty")
			return

		if index > self.size:
			print("delete: Out of range")
			return

		node = self.first
		i = 1

		while i < index:
			node = node.next
			i += 1

		if node.prev is not None and node.next is not None:
			node.prev.next = node.next
			node.next.prev = node.prev
			#node = None
			self.size -= 1
		elif node.prev is None and node.next is not None:
			self.first.next.prev = None
			self.first = self.first.next
			#node = None
			self.size -= 1
		elif node.prev is not None and node.next is None:
			self.last.prev.next = None
			self.last = self.last.prev
			#node = None
			self.size -= 1
		else:
			self.first = None
			self.last = None
			self.size = 0

			

	def pushback(self, data):
		if self.first is None:
			node = Node(None, None, data)
			self.first = node
			self.last = node
			self.size += 1
		else:
			node = Node(self.last, None, data)
			self.last.next = node
			self.last = node
			self.size += 1

	def popback(self):
		if self.first is None:
			print("popback: List is empty")
			return

		if self.last.prev is not None:
			self.last.prev.next = None
			self.last = self.last.prev
			self.size -= 1
		else:
			self.last = None
			self.first = None
			self.size = 0 

	def pushfront(self, data):
		if self.first is None:
			node = Node(None, None, data)
			self.first = node
			self.last = node
			self.size += 1
		else:
			node = Node(None, self.first, data)
			self.first.prev = node
			self.first = node
			self.size += 1

	def popfront(self):
		if self.first is None:
			print("popfront: List is empty")
			return

		if self.first.next is not None:
			self.first.next.prev = None
			self.first = self.first.next
			self.size -= 1

		else:
			self.first = None
			self.last = None
			self.size = 0

	def get(self, index=1):
		i = 1
		for data in ListIteratorForward(self.first):
			if i == index:
				return data
			i += 1

	def find(self, data):
		index = 1

		for d in ListIteratorForward(self.first):
			if d == data:
				return index
			index += 1
		
		return 0

	def dlprintf(self):
		if self.first is None:
			print("dlprintf: List is empty")
			return
		else:
			for data in ListIteratorForward(self.first):
				print(data)

	def dlprintb(self):
		if self.first is None:
			print("dlprintb: List is empty")
			return
		else:
			for data in ListIteratorBackward(self.last):
				print(data)

	def dlprint(self, data):
		print(data)
