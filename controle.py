#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from random import randint
from tree import *
from enumError import enumError


class Jogo():

	def __init__(self, *args, **kwargs):

		#Dicionário e funcoes de checagem
		self.dicionario=Tree()
		#Montagem do dicionário em forma de uma árvore
		self.dicionario.montaTree('dicionario.txt')

		#Lista de listas que representa a matriz do jogo atual
		self.matriz=[]
		#Montagem do tabuleiro do jogo
		self.montaTabuleiro()

		#Lista que contem as letras disponiveis
		self.lettersPack = []
		#Monta o saquinho das letras 
		self.montaSaquinho()

		#Listas que contém as letras de cada jogador
		self.packletters = [[],[]]

		#Distribui as 7 primeiras letras aos jogadores
		for i in range(0,7):
			self.packletters[0].append(self.lettersPack.pop())
			self.packletters[1].append(self.lettersPack.pop())

		#Inteiros que contém a pontuação de cada jogador
		self.points1 = 0
		self.points2 = 0

		#Variavel que controlará os turnos
		self.turno = randint(0,1)

		#Variavel que controlará o player atual que está jogando
		self.playerAtual = self.turno
		
		#Variavel que dirá se o jogo está no inicio que consequentemente a palavra tem que passar no meio do mapa
		self.inicio = True


	def __str__(self):
		string = ''
		string += 'Letras jogador 1: '
		for i in self.packletters[0]:
			string += i +' '
		string += '\n'
		
		string += 'Letras jogador 2: '
		for i in self.packletters[1]:
			string += i +' '
		string += '\n'

		string += 'Tabuleiro: \n'
		for linha in self.matriz:

			string += '|'
			for elem in linha:
				
				if len(elem)==0:
					string+='  |'
				elif len(elem)==1:
					string += ' ' + elem + '|'
				else:
					string += elem + '|'

			string += '\n'

		return string


	#Função que monta o tabuleiro do jogo
	def montaTabuleiro(self):

		#Manipulação para modificar a matriz colocando os modificadores de pontuação
		for i in range(0,15):
			self.matriz.append([])
			for j in range(0,15):
				self.matriz[i].append('')

		self.matriz[7][7]='*'
		
		for i in range(0,15,7):
			for j in range(0,15,7):
				if(not(i==7==j)):
					self.matriz[i][j]='TP'

		for i in range(1,5):
			self.matriz[i][i]='DP'
			self.matriz[14-i][14-i]='DP'
			self.matriz[i][14-i]='DP'
			self.matriz[14-i][i]='DP'

		for i in range(0,15,14):
			self.matriz[3][i]='DL'
			self.matriz[i][3]='DL'
			self.matriz[11][i]='DL'
			self.matriz[i][11]='DL'

		for i in range(1,15,12):
			self.matriz[5][i]='TL'
			self.matriz[i][5]='TL'
			self.matriz[9][i]='TL'
			self.matriz[i][9]='TL'

		for i in range(2,15,10):
			self.matriz[6][i]='DL'
			self.matriz[i][6]='DL'
			self.matriz[8][i]='DL'
			self.matriz[i][8]='DL'

		for i in range(3,15,8):
			self.matriz[7][i]='DL'
			self.matriz[i][7]='DL'

		for i in range(5,11,4):
			self.matriz[5][i]='TL'
			self.matriz[9][i]='TL'

		for i in range(6,10,2):
			self.matriz[6][i]='DL'
			self.matriz[8][i]='DL'


	#Função que monta o saquinho de letras disponiveis
	def montaSaquinho(self):
		self.lettersPack =  ['a']*14 + ['e']*11 + ['i']*10 + ['o']*10 + ['s']*8 + ['u']*7 + ['m']*6 
		self.lettersPack += ['r']*6 + ['t']*5 + ['d']*5 + ['l']*5 + ['c']*4 + ['p']*4 + ['n']*4 
		self.lettersPack += ['b']*3 + ['ç']*2 + ['f']*2 + ['g']*2 + ['h']*2 + ['v']*2 + ['j']*2
		self.lettersPack += ['q']*1 + ['x']*1 + ['z']*1 + ['_']*3
		#Embaralha o pacote que contém todas as letras
		random.shuffle(self.lettersPack)


	#Função que faz a checagem para ver se a palavra pode ser adicionada no tabuleiro
	def checkWord(self,line,col,word,direcao):

		#Checa a ultrapassagem do mapa em colunas (OK)
		if(direcao == 'H'):
			if(col+len(word)-1 > 15):
				return enumError.er_inWordLine


		#Checa a ultrapassagem do mapa em linhas (OK)
		else:
			if(line+len(word)-1 > 15):
				return enumError.er_inWordCol


		#Checa se a palavra passada existe no dicionário (OK)
		if(not self.dicionario.checkWordExistence(word)):
			return enumError.er_inWordInexist
		

		#Checagem do turno inicial se a palavra inserida passa no meio do mapa (OK)
		if(self.inicio):
			bu = True
			if( (direcao=='H') and ( line!=8 or (col > 8) or ( col+len(word) < 8)) ):
				bu = False
			elif((direcao=='V') and ( col!=8 or ((line > 8) or ( line+len(word) < 8))) ):
				bu = False

			if(not bu):
				return enumError.er_inWordInitFail
			else:
				self.inicio = False


		#Checagem se a palavra inserida utiliza ao menos uma das letras do tabuleiro (OK)
		else:	
			utiliza = False
			for i in range(0,len(word)):
				if(direcao=='V'):
					#Caso o tamanho seja 1 nesta posição da matriz significa que há alguma letra la
					#Pois no tabuleiro padrao o tamanho das string é 0 quando não há nada ou 2 quando há um multiplicador lá
					if(len(self.matriz[line+i-1][col-1])==1):
						utiliza=True
						break
				else:
					if(len(self.matriz[line-1][col+i-1])==1):
						utiliza=True
						break

			if not utiliza:
				return enumError.er_inWordNotTableUsed

		
		#Checagem se é possível de se encaixar esta palavra na matriz
		#E para verificação se foi utilizada ao menos uma letra do saquinho
		temp = []
		player = self.playerAtual
		utiliza = False
		for i in range(0,len(word)):
			if(direcao=='V'):
				#Caso de já possuir uma letra na matriz
				if(len(self.matriz[line+i-1][col-1])==1):
					#Caso a letra já está na matriz na posição esperada ou ser um asterisco
					if(self.matriz[line+i-1][col-1]==word[i] or self.matriz[line+i-1][col-1]=='*'):
						pass
					#Caso contrário da um erro pq a letra da palavra é diferente da que está na matriz
					else:
						self.packletters[player].extend(temp)
						return enumError.er_inWordNotPossibleIn
				else:

					#Caso a letra não esteja no pacote de letras do player 
					if(word[i] not in self.packletters[player]):
						#Caso o player não tenha a letra atual e não possua o coringa
						if('_' not in self.packletters[player]):
							self.packletters[player].extend(temp)
							return enumError.er_inWordNotPossibleIn
						#Caso ele tenha o coringa retira o coringa do saquinho
						else:
							temp += self.packletters[player].pop(self.packletters[player].index('_'))
					else:
						#Retira a letra da palavra temporariamente do conjunto de letras do player
						temp += self.packletters[player].pop(self.packletters[player].index(word[i]))

			else:
				#Caso de já possuir uma letra na matriz
				if(len(self.matriz[line-1][col+i-1])==1):
					#Caso a letra já está na matriz na posição esperada ou ser um asterisco
					if(self.matriz[line-1][col+i-1]==word[i] or self.matriz[line+i-1][col-1]=='*'):
						pass
					#Caso contrário da um erro pq a letra da palavra é diferente da que está na matriz
					else:
						self.packletters[player].extend(temp)
						return enumError.er_inWordNotPossibleIn

				else:
					#Caso a letra não esteja no pacote de letras do player retorna-se um erro
					if(word[i] not in self.packletters[player]):
						#Caso o player não tenha a letra atual e não possua o coringa
						if('_' not in self.packletters[player]):
							self.packletters[player].extend(temp)
							return enumError.er_inWordNotPossibleIn
						#Caso ele tenha o coringa retira o coringa do saquinho
						else:
							temp += self.packletters[player].pop(self.packletters[player].index('_'))
					else:
						#Retira a letra da palavra temporariamente do conjunto de letras do player
						temp += self.packletters[player].pop(self.packletters[player].index(word[i]))

		#Une-se as listas novamente
		self.packletters[player].extend(temp)
		


		#Checagem para verificar se a nova palavra adicionada na matriz não atrapalhou nenhuma outra palavra ja existente
		if(direcao=='V'):

			for i in range(0,len(word)):

				#A palavra esta colada no canto esquerdo
				if(col==1):
					#Caso haja incidencia de estar encostando em uma outra palavra a direita
					if(len(self.matriz[line+i-1][col])==1):
						palavra = ''
						palavra+=word[i]
						#Percorre a palavra adjacente a direita para a verificação de existencia 
						j=0
						while j+col!=15 and len(self.matriz[line+i-1][col+j])==1:
							palavra+=self.matriz[line+i-1][col+j]
							j+=1

						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 1')
							return enumError.er_inWordConflict

				#A palavra esta colada no canto direito
				elif(col==15):
					#Caso haja incidencia de estar encostando em uma outra palavra a esquerda
					if(len(self.matriz[line+i-1][col-2])==1):
						palavra = ''
						palavra+=word[i]
						#Percorre a palavra adjacente a esquerda para a verificação de existencia 
						j=0
						while col-j!=-1 and len(self.matriz[line+i-1][col-2-j])==1:
							palavra+=self.matriz[line+i-1][col-2-j]
							j+=1

						#Faz a palavra ficar ao contrário já que a mesma foi concatenada ao contrario
						palavra=palavra[::-1]
						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 2')
							return enumError.er_inWordConflict

				#A palavra esta em qualquer coluna do tabuleiro
				else:
					#Caso haja incidencia de estar encostando em uma outra palavra a esquerda
					if(len(self.matriz[line+i-1][col-2])==1):
						palavra = ''
						palavra+=word[i]
						#Percorre a palavra adjacente a esquerda para a concatenacao 
						j=0
						while col-j!=-1 and len(self.matriz[line+i-1][col-2-j])==1:
							palavra+=self.matriz[line+i-1][col-2-j]
							j+=1

						#Faz a palavra ficar ao contrário já que a mesma foi concatenada ao contrario
						palavra = palavra[::-1]

						#Verifica agora se há algo a frente da palavra
						if(len(self.matriz[line+i-1][col])==1):
							j=0
							while j+col!=15 and len(self.matriz[line+i-1][col+j])==1:
								palavra+=self.matriz[line+i-1][col+j]
								j+=1

						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 3')
							return enumError.er_inWordConflict

					#Caso haja incidencia de estar encostando em uma outra palavra a direita
					elif(len(self.matriz[line+i-1][col])==1):
						palavra = ''
						palavra+=word[i]

						j=0
						while j+col!=15 and len(self.matriz[line+i-1][col+j])==1:
							palavra+=self.matriz[line+i-1][col+j]
							j+=1

						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 4')
							return enumError.er_inWordConflict

			#Caso a palavra esteja encostada na parte superior do tabuleiro
			if(line==1):

				fim = len(word)
				palavra = word
				if(fim<15 and len(self.matriz[fim][col-1])==1):
					
					j=0
					#Percorre-se o que está abaixo da palavra para ver se há letras 'soltas' 
					while j+fim!=15 and len(self.matriz[fim+j][col-1])==1:
						palavra+=self.matriz[fim+j][col-1]
						j+=1

				if not self.dicionario.checkWordExistence(palavra):
					print('Deu erro aqui 5')
					return enumError.er_inWordConflict

			#Caso esteja em qualquer outra parte das linhas do tabuleiro
			else:

				fim = len(word)+line
				palavra = ''
				if fim<15 and len(self.matriz[line-2][col-1])==1:
					j=0
					while line-2-j!=-1 and len(self.matriz[line-2-j][col-1])==1:
						palavra+=self.matriz[line-2-j][col-1]
						j+=1

				palavra=palavra[::-1]
				palavra+=word

				if(fim<15 and len(self.matriz[fim][col-1])==1):

					j=0
					#Percorre-se o que está abaixo da palavra para ver se há letras 'soltas' 
					while j+fim!=15 and len(self.matriz[fim+j][col-1])==1:
						palavra+=self.matriz[fim+j][col-1]
						j+=1

				if not self.dicionario.checkWordExistence(palavra):
					print('Deu erro aqui 6')
					return enumError.er_inWordConflict


		#Caso seja na horizontal
		else:
	
			for i in range(0,len(word)):

				#A palavra esta colada no canto superior
				if(line==1):
					#Caso haja incidencia de estar encostando em uma outra palavra a direita
					if(len(self.matriz[line][col+i-1])==1):
						palavra = ''
						palavra+=word[i]
						#Percorre a palavra adjacente a direita para a verificação de existencia 
						j=0
						while j+line!=15 and len(self.matriz[line+j][col+i-1])==1:
							palavra+=self.matriz[line+j][col+i-1]
							j+=1

						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 1')
							return enumError.er_inWordConflict

				#A palavra esta colada no canto inferior
				elif(line==15):
					#Caso haja incidencia de estar encostando em uma outra palavra a esquerda
					if(len(self.matriz[line-2][col+i-1])==1):
						palavra = ''
						palavra+=word[i]
						#Percorre a palavra adjacente a esquerda para a verificação de existencia 
						j=0
						while line-j!=-1 and len(self.matriz[line-2-j][col+i-1])==1:
							palavra+=self.matriz[line-2-j][col+i-1]
							j+=1

						#Faz a palavra ficar ao contrário já que a mesma foi concatenada ao contrario
						palavra=palavra[::-1]
						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 2')
							return enumError.er_inWordConflict

				#A palavra esta em qualquer linha do tabuleiro
				else:
					#Caso haja incidencia de estar encostando em uma outra palavra acima da mesma
					if(len(self.matriz[line-2][col+i-1])==1):
						palavra = ''
						palavra+=word[i]
						#Percorre a palavra adjacente a esquerda para a concatenacao 
						j=0
						while line-j!=-1 and len(self.matriz[line-2-j][col+i-1])==1:
							palavra+=self.matriz[line-2-j][col+i-1]
							j+=1

						#Faz a palavra ficar ao contrário já que a mesma foi concatenada ao contrario
						palavra=palavra[::-1]

						#Verifica agora se há algo a frente da palavra
						if(len(self.matriz[line][col+i-1])==1):
							j=0
							while j+line!=15 and len(self.matriz[line+j][col+i-1])==1:
								palavra+=self.matriz[line+j][col+i-1]
								j+=1

						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 3')
							return enumError.er_inWordConflict

					#Caso haja incidencia de estar encostando em uma outra palavra abaixo da mesma
					elif(len(self.matriz[line][col+i-1])==1):
						palavra = ''
						palavra+=word[i]

						j=0
						while j+line!=15 and len(self.matriz[line+j][col+i-1])==1:
							palavra+=self.matriz[line+j][col+i-1]
							j+=1

						#Significa q a palavra encontrada a direita esta no dicionário
						if not self.dicionario.checkWordExistence(palavra):
							print('Deu erro aqui 4')
							return enumError.er_inWordConflict

			#Caso a palavra esteja encostada na parte a esquerda do tabuleiro
			if(col==1):

				fim = len(word)
				palavra = word
				if(fim<15 and len(self.matriz[line-1][fim])==1):
					
					j=0
					#Percorre-se o que está abaixo da palavra para ver se há letras 'soltas' 
					while j+fim!=15 and len(self.matriz[line-1][fim+j])==1:
						palavra+=self.matriz[line-1][fim+j]
						j+=1

				if not self.dicionario.checkWordExistence(palavra):
					print('Deu erro aqui 5')
					return enumError.er_inWordConflict

			#Caso esteja em qualquer outra parte das colunas do tabuleiro
			else:

				fim = len(word)+col
				palavra = ''
				if fim<15 and len(self.matriz[line-1][col-2])==1:
					j=0
					while col-2-j!=-1 and len(self.matriz[line-1][col-2-j])==1:
						palavra+=self.matriz[line-1][col-2-j]
						j+=1

				palavra=palavra[::-1]
				palavra+=word

				if(fim<15 and len(self.matriz[col-1][fim])==1):

					j=0
					#Percorre-se o que está abaixo da palavra para ver se há letras 'soltas' 
					while j+fim!=15 and len(self.matriz[col-1][fim+j])==1:
						palavra+=self.matriz[col-1][fim+j]
						j+=1

				if not self.dicionario.checkWordExistence(palavra):
					print('Deu erro aqui 6')
					return enumError.er_inWordConflict



		return 1


	#Função para calcular o ponto de uma letra na matriz
	def calculaPtsAtual(self,letra):

		if(letra in ['a','e','i','o','s','u','m','r','t']):
			return 1
		elif(letra in ['d','l','c','p']):
			return 2
		elif(letra in ['n','b','ç']):
			return 3
		elif(letra in ['f','g','h','v']):
			return 4
		elif(letra in ['j']):
			return 5
		elif(letra in ['q']):
			return 6
		elif(letra in ['x','z']):
			return 8
		else:
			return 0


	#Função que fará o adicionamento da palavra no tabuleiro além de calcular os pontos
	def inputWord(self,line,col,word,direcao):

		player = self.playerAtual
		pontos = 0
		palavraFinal = ''

		#Adicionar de uma palavra na matriz
		for i in range(0,len(word)):
			if(direcao=='V'):
				#self.matriz[line+i-1][col-1] = word[i]

				#Caso da letra a ser adicionada ja esta na matriz				
				if self.matriz[line+i-1][col-1]==word[i]:
					pass
				#Caso contrario vai ter que gastar do saquinho do player
				else:
					#Caso de gastar a letra normal
					if(word[i] in self.packletters[player]):
						self.packletters[player].pop(self.packletters[player].index(word[i]))
					#Caso de gastar um coringa
					else:
						self.packletters[player].pop(self.packletters[player].index('_'))
						pontos += self.calculaPtsAtual('_')
						self.matriz[line+i-1][col-1] = word[i]
						palavraFinal += word[i].upper()						
						continue
			
				self.matriz[line+i-1][col-1] = word[i]

			else:
				#self.matriz[line-1][col+i-1] = word[i]
				#Caso a letra a ser adicionada ja esta na matriz
				if self.matriz[line-1][col+i-1]==word[i]:
					pass
				#Caso contrario vai ter que gastar do saquinho do player
				else:					
					#Caso de gastar a letra normal
					if(word[i] in self.packletters[player]):
						self.packletters[player].pop(self.packletters[player].index(word[i]))
					#Caso de gastar um coringa
					else:
						self.packletters[player].pop(self.packletters[player].index('_'))
						pontos += self.calculaPtsAtual('_')
						self.matriz[line-1][col-1+i] = word[i]
						palavraFinal += word[i].upper()	
						continue
			
				self.matriz[line-1][col-1+i] = word[i]
			
			#Calcula a quantidade de pontos a ser adicionada
			palavraFinal += word[i]
			pontos += self.calculaPtsAtual(word[i])	

		self.atualizaSaquinho()

		return pontos,palavraFinal


	#Função que completa as 7 letras do saquinho após colocar uma palavra no tabuleiro
	def atualizaSaquinho(self):

		qtd = 7-len(self.packletters[self.playerAtual])

		for i in range(0,qtd):
			self.packletters[self.playerAtual].append(self.lettersPack.pop())


	#Função que fará a troca das letras dos jogadores
	def exchangeLetters(self,letters):

		player = self.playerAtual

		if(len(letters)>7):
			return enumError.er_exchBigger7

		#Caso da quantidade de letras a serem trocadas ser maior que a quantidade de letras disponíveis no saquinho
		if(len(letters) > len(self.lettersPack)):
			return enumError.er_exchBiggerPack
		
		#Tratamento do player 1
		if(player == 0):

			#Faz a interseção do pacote de letras do player referente, com as letras que o player deseja trocar
			intercesao = list(set([i for i in self.packletters[0] if i in letters]))

			#Caso da interseção acima de um tamanho menor que o conjunto passado significa que tem alguma letra que o player não possui e deseja trocar
			if(len(letters)>len(intercesao)):
				return enumError.er_exchLetterNotFound

			#Retira os elementos da pacote do jogador 1
			lTemp = []
			for el in letters:
				lTemp = self.packletters[0].pop(self.packletters[0].index(el))

			for i in range(0,len(letters)):
				self.packletters[0].append(self.lettersPack.pop())

			self.lettersPack.extend(lTemp)
			random.shuffle(self.lettersPack)

			return self.packletters[0]

		#Tratamento do player 2
		else:

			#Faz a interseção do pacote de letras do player referente, com as letras que o player deseja trocar
			intercesao = list(set([i for i in self.packletters[1] if i in letters]))

			#Caso da interseção acima de um tamanho menor que o conjunto passado significa que tem alguma letra que o player não possui e deseja trocar
			if(len(letters)>len(intercesao)):
				return enumError.er_exchLetterNotFound

			#Retira os elementos da pacote do jogador 2
			lTemp = []
			for el in letters:
				lTemp = self.packletters[1].pop(self.packletters[1].index(el))

			for i in range(0,len(letters)):
				self.packletters[1].append(self.lettersPack.pop())

			self.lettersPack.extend(lTemp)
			random.shuffle(self.lettersPack)

			return self.packletters[1]


	#Função que incrementará a quantidade de pontos de um determinado player
	def addPoints(self,qtd):

		if self.playerAtual==0:
			self.points1 += qtd
		else:
			self.points2 += qtd


	#Função feita para passa a vez de um participante
	def passaVez(self):

		self.turno += 1

		if(self.playerAtual==0):
			self.playerAtual = 1
		else:
			self.playerAtual = 0
