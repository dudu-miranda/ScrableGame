#!/usr/bin/python
# -*- coding: utf-8 -*-

from node import Node


class Tree():

	def __init__(self):
		self.raiz = Node(False,' ')


	def montaTree(self,nomeArquivo):

		Arq = open(nomeArquivo, "r")

		#Itera as linhas do arquivo
		for palavra in Arq:

			#Reseta o no atual para a raiz da árvore
			noAtual = self.raiz
			#Itera as letras da palavra
			for i in range(0,len(palavra)-1):

				letra = palavra[i]
				#print(palavra + '  -  '+letra)
				#Itera as conexões do nó atual
				existe = False

				if letra in noAtual.connections.keys():
					noAtual = noAtual.connections[letra]
					existe = True

				#print(noAtual)
				#Caso a letra atual não tenha um nó só pra ela
				if(not existe):

					#Caso de ser a ultima letra da palavra
					#Palavra[-2] pois o ultimo caractere de uma palavra do dicionário é sempre um \n

					#self.__tabelasimbolo[bloco].update({chave: tipo})
					if(i==len(palavra)-2):
						no = Node(True,letra)
						noAtual.connections.update({letra: no})
						noAtual.connections.update({letra.upper(): no})
					else:
						no = Node(False,letra)
						noAtual.connections.update({letra: no})
						noAtual.connections.update({letra.upper(): no})
						noAtual = noAtual.connections[letra]


		Arq.close()


	def checkWordExistence(self,word):

		#Reseta o no atual para a raiz da árvore
		noAtual = self.raiz
		#Itera as letras da palavra
		for i in range(0,len(word)):
			letra=word[i]

			#Itera as conexões do nó atual
			existe = False

			if letra in noAtual.connections.keys():
				noAtual = noAtual.connections[letra]
				existe = True

			#Caso da palavra digitada não existir na árvore
			if(not existe):
				return False

			if(i==len(word)-1):
				return noAtual.final
