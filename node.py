#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node():

	def __init__(self,final,letra):
		self.final = final
		self.letra = letra
		self.connections = {}


	def findIndex(self,letra):
		
		for i in range(0,len(self.connections)):
			if(letra == self.connections[i].letra):
				return i


	def __str__(self):
		conexoes=''
		for i in self.connections.keys():
			conexoes += str(i)+' '
		return 'Final='+str(self.final)+' Letra='+self.letra+' Conexões='+conexoes


	#Checa a existencia parcial a partir de um nó se ele tem ligação para o char passado
	def checkConection(self, char):

		if char in self.connections.keys():
			return 1

		return 0

