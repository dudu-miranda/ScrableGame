#!/usr/bin/python
# -*- coding: utf-8 -*-

from node import Node


class Tree():


	def __init__(self):
		

		self.raiz = Node(False,' ')

		#self.montaTree(nomeArquivo)
		'''
		print(self.raiz)
		atual=self.raiz.connections[0]
		print(atual)
		atual=atual.connections[0]
		print(atual)
		atual=atual.connections[0]
		print(atual)
		atual=atual.connections[0]
		print(atual)
		atual=atual.connections[0]
		print(atual)
		atual=atual.connections[0]
		print(atual)
		atual=atual.connections[0]
		print(atual)
		l1=self.checkWordExistence('babaremos')
		l2=self.checkWordExistence('babadasso')
		l3=self.checkWordExistence('aburpat')
		print(str(l1)+str(l2)+str(l3))
		'''


	def montaTree(self,nomeArquivo):

		Arq = open(nomeArquivo, "r")

		#Itera as linhas do arquivo
		for palavra in Arq:

			#Reseta o no atual para a raiz da árvore
			noAtual = self.raiz
			#Itera as letras da palavra
			for i in range(0,len(palavra)-1):
				letra=palavra[i]
				#print(palavra + '  -  '+letra)
				#Itera as conexões do nó atual
				existe = False
				for conexao in noAtual.connections:		
					#Verifica a existência de um nó da árvore
					if(letra==conexao.letra):
						noAtual = noAtual.connections[noAtual.findIndex(letra)]
						existe = True
						break

				#print(noAtual)
				#Caso a letra atual não tenha um nó só pra ela
				if(not existe):

					#Caso de ser a ultima letra da palavra
					#Palavra[-2] pois o ultimo caractere de uma palavra do dicionário é sempre um \n
					if(i==len(palavra)-2):
						noAtual.connections.append(Node(True,letra))
					else:
						noAtual.connections.append(Node(False,letra))
						noAtual = noAtual.connections[noAtual.findIndex(letra)]
															

		Arq.close()


	def checkWordExistence(self,word):

		#Reseta o no atual para a raiz da árvore
		noAtual = self.raiz
		#Itera as letras da palavra
		for i in range(0,len(word)):
			letra=word[i]

			#Itera as conexões do nó atual
			existe = False
			for conexao in noAtual.connections:		
				#Verifica a existência de um nó da árvore
				if(letra==conexao.letra):
					noAtual = noAtual.connections[noAtual.findIndex(letra)]
					existe = True
					break

			#Caso da palavra digitada não existir na árvore
			if(not existe):
				return False
			
			if(i==len(word)-1):
				return noAtual.final
