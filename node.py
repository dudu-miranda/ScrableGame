#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node():


	def __init__(self,final,letra):
		

		self.final = final
		self.letra = letra
		self.connections = []


	def findIndex(self,letra):
		
		for i in range(0,len(self.connections)):
			if(letra == self.connections[i].letra):
				return i


	def __str__(self):
		conexoes=''
		for i in range(0,len(self.connections)):
			conexoes+=str(self.connections[i].letra)+' '
		return 'Final='+str(self.final)+' Letra='+self.letra+' Conexões='+conexoes

