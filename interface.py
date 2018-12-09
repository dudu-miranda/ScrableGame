#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets  import QPushButton, QTableWidget, QWidget, QSpinBox, QVBoxLayout, QHBoxLayout, QApplication, QComboBox
from PyQt5.QtWidgets  import QTableView, QTextBrowser, QAbstractItemView, QTableWidgetItem, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore     import pyqtSlot

import threading
import sys
import time
import cProfile as profile
import pstats

from controle 		  import *
from enumError import enumError
from IA  import *



class MirandasWindow(QWidget):

	def __init__(self, *args, **kwargs):

		super().__init__()

		self.p = profile.Profile()
		self.p.enable()

		self.estilo = int(sys.argv[1])

		#Aqui basicamente se instancia e inicia todas as partes da interface
		self.iniciaComponentes()

		self.jogo = Jogo()

		self.playerAtual = self.jogo.turno

		self.alteraContexto()
		self.alteraContexto()

		self.condicao = True
		self.contador = 0

		self.ia1 = IA(self.jogo)
		self.ia2 = IA(self.jogo)
			
		#print(self.jogo.packletters[self.playerAtual])
		#self.labelLetras.setText(letrasIniciais)


	#Função que iniciará todos os componentes da tela
	def iniciaComponentes(self):

		self.setWindowTitle('Screble')

		#Configuração do botão que adiciona as palavras
		self.botaoAddWord = QPushButton('Add Word')
		self.botaoAddWord.setToolTip('Botão para adicionar uma palavra')
		self.botaoAddWord.clicked.connect(self.clickbotao_addWord)

		#Configuração dos labels do player 1
		self.label1 = QLabel('Player1:')
		self.label1Pts = QLabel('0')

		#Configuração dos labels do player 2
		self.label2 = QLabel('Player2:')
		self.label2Pts = QLabel('0')

		#Configuração do identificador textual da coluna para adicionamento da palavra
		self.editRow = QSpinBox()
		self.editRow.setMinimum(1)
		self.editRow.setMaximum(15)
		self.labelRow = QLabel('Linha:')

		#Configuração do identificador textual da coluna para adicionamento da palavra
		self.editCol = QSpinBox()
		self.editCol.setMinimum(1)
		self.editCol.setMaximum(15)
		self.labelCol = QLabel('Coluna:')

		#Configuração dos edits que conterão a palavra a ser adicionada e a direção da mesma
		self.comboDir  = QComboBox()
		self.comboDir.addItem("V")
		self.comboDir.addItem("H")
		self.labelDir = QLabel('Direção:')
		self.editWord = QLineEdit('Palavra')
		self.labelWord = QLabel('Palavra:')


		#Configuração da matriz que contem as letras e bonus das palavras colocadas
		self.tabela_matriz = QTableWidget()
		self.tabela_matriz.setColumnCount(15)
		self.tabela_matriz.setRowCount(15)
		self.tabela_matriz.setShowGrid(True)
		self.tabela_matriz.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.setaLetrasIniciais()
		self.tabela_matriz.resizeColumnsToContents()
		self.tabela_matriz.resizeRowsToContents()
		
		#Configuração do label das letras disponíveis
		self.labelDisponiveis = QLabel('Letras disponíveis:')
		self.labelLetras = QLabel('')

		#Configuração do edit que conterá as letras a serem trocadas
		self.editTroca = QLineEdit('')

		#Configuração do botão que troca as letras
		self.botaoTrocaLetras = QPushButton('Troca letras')
		self.botaoTrocaLetras.setToolTip('Botão para trocar suas letras')
		self.botaoTrocaLetras.clicked.connect(self.clickbotao_trocaLetra)

		#Configuração do botão de passar a vez
		self.botaoPassaVez = QPushButton('Passar vez')
		self.botaoPassaVez.setToolTip('Botão para passar sua rodada')
		#self.botaoPassaVez.clicked.connect(self.clickbotao_passaVez)

		#Configuração dos layouts
		main_layout = QVBoxLayout()		
		
		# Header
		layout = QHBoxLayout()
		layout.addWidget(self.label1)
		layout.addWidget(self.label1Pts)
		layout.addStretch()
		layout.addWidget(self.label2)
		layout.addWidget(self.label2Pts)
		
		main_layout.addLayout(layout)
		
		# Main Vision
		layout = QHBoxLayout()
		layout.addWidget(self.tabela_matriz)
		l = QVBoxLayout()
		l.addWidget(self.labelDisponiveis)
		l.addWidget(self.labelLetras)
		
		l1 = QHBoxLayout()
		l1.addWidget(self.editTroca)
		l1.addWidget(self.botaoTrocaLetras)
		l1.addWidget(self.botaoPassaVez)
		l.addLayout(l1)
		layout.addLayout(l)
		
		main_layout.addLayout(layout)
		
		# Footer
		layout = QVBoxLayout()
		l = QHBoxLayout()
		l.addWidget(self.labelRow)
		l.addWidget(self.editRow)
		l.addWidget(self.labelCol)
		l.addWidget(self.editCol)
		l.addWidget(self.labelDir)
		l.addWidget(self.comboDir)
		l.addWidget(self.labelWord)
		l.addWidget(self.editWord)
		layout.addLayout(l)
		layout.addWidget(self.botaoAddWord)
		
		main_layout.addLayout(layout)

		#Input do layout completo
		self.setLayout(main_layout)
		self.setGeometry(50, 50, 1220, 450)


	#Ação do botão que adicionará uma palavra na matriz
	@pyqtSlot()
	def clickbotao_addWord(self):
	
		if(self.contador > 9):
			self.p.disable()
			pstats.Stats(self.p).sort_stats('cumulative').print_stats(30)
			exit()

		row,col,word,direcao = 0,0,'',''
		#Caso do jogador

		#Caso de ser PVP
		if(self.estilo == 0):
			row=self.editRow.value()
			col=self.editCol.value()
			word=self.editWord.text().lower()
			direcao=self.comboDir.currentText()

		#Caso de ser PvsIA
		elif(self.estilo == 1):
			#Jogada do player
			if self.playerAtual==0:
				#Pega todos os dados digitados
				row=self.editRow.value()
				col=self.editCol.value()
				word=self.editWord.text().lower()
				direcao=self.comboDir.currentText()
			#Jogada da IA
			else:
				row,col,word,direcao = self.ia1.permutation(self.jogo.matriz,self.jogo.packletters[1])
				print ('saindo '+str(row)+' '+str(col)+' '+word+' '+direcao)
				#Chamar troca de letra

		#Caso de ser IAvsIA
		else:
			#Jogada da IA1
			if self.playerAtual==0:
				row,col,word,direcao = self.ia1.permutation(self.jogo.matriz,self.jogo.packletters[0])
				print ('saindo '+str(row)+' '+str(col)+' '+word+' '+direcao)
				#Chamar troca de letra
			#Jogada da IA2
			else:
				row,col,word,direcao = self.ia2.permutation(self.jogo.matriz,self.jogo.packletters[1])
				print ('saindo '+str(row)+' '+str(col)+' '+word+' '+direcao)
				#Chamar troca de letra

		#Caso a IA queira passar a vez ele mandará uma string vazia que também serve para o jogador
		if word=='':
			if(self.estilo == 2):
				self.clickbotao_trocaLetra(self.jogo.packletters[self.jogo.playerAtual])

			elif(self.estilo == 1 and self.playerAtual == 1):
				self.clickbotao_trocaLetra(self.jogo.packletters[1])

			else:
				self.passaVez()
			
			return 1

		#Faz a checagem de erros
		res = self.jogo.checkWord(row,col,word,direcao)

		if(res!=1):
			self.printError(res)
			self.passaVez()
			return -1

		#Chama a função para calcular os pontos e a palavra final que pode ser modificada caso use-se um coringa
		pontos,palavra = self.jogo.inputWord(row,col,word,direcao)
		#Chama a função para colocar a palavra na matriz
		self.inputWord(row,col,palavra,direcao)	
		#Chama a função de adicionar a pontuação
		self.addPonts(pontos)		
		#Chamará a troca de contexto na interface e no backend	
		self.passaVez()
		self.contador +=1

		#Caso de ser player VS IA para a IA jogar sozinha
		if(self.estilo==1):
			if(self.playerAtual==1):
				self.clickbotao_addWord()

	
	#Ação doo botão que trocara as letras do determinado player
	@pyqtSlot()
	def clickbotao_trocaLetra(self, letrasAntigas=[]):

		if( (self.estilo == 0) or (self.playerAtual==0 and self.estilo == 1) ):
			#Pega as letras do edit, da um split para que se transforme em uma lista
			letrasAntigas = self.editTroca.text().split(',')
		
		#Chama a função de trocar letras
		listaNovasLetras = self.jogo.exchangeLetters(letrasAntigas)

		#Casos de erros
		if(type(listaNovasLetras)==int):
			self.printError(listaNovasLetras)
			return -1

		novasLetras = self.listToStr(listaNovasLetras)

		self.labelLetras.setText(novasLetras)
		self.passaVez()


	#Ação do botão que adicionará uma palavra na matriz
	@pyqtSlot()
	def clickbotao_passaVez(self):

		#Chamará a troca de contexto na interface e no backend
		self.passaVez()


	#Chamará a troca de contexto na interface e também no backend do jogo
	def passaVez(self):
		self.alteraContexto()
		self.jogo.passaVez()


	#Função que fará a transição de jogadas entre o jogador 1 e 2
	def alteraContexto(self):
		
		if(self.playerAtual==0):
			self.label1.setStyleSheet("QLabel { background-color : lightgray; color : black; }")
			self.label2.setStyleSheet("QLabel { background-color : lightgreen; color : black; }")
			self.playerAtual = 1
		else:
			self.label2.setStyleSheet("QLabel { background-color : lightgray; color : black; }")
			self.label1.setStyleSheet("QLabel { background-color : lightgreen; color : black; }")
			self.playerAtual = 0
		self.labelLetras.setText(self.listToStr(self.jogo.packletters[self.playerAtual]))


	#Função que adiciona uma palavra na matriz
	def inputWord(self,row,col,word,direcao):

		for i in range(0,len(word)):
			if(direcao=='V'):
				self.tabela_matriz.setItem(row+i-1,col-1,QTableWidgetItem(word[i]))
			else:
				self.tabela_matriz.setItem(row-1,col+i-1,QTableWidgetItem(word[i]))


	#Função que adiciona pontos na pontuação de determinado jogador
	def addPonts(self,pontos):
		if(self.playerAtual==0):
			self.label1Pts.setNum(int(self.label1Pts.text())+pontos)
		else:
			self.label2Pts.setNum(int(self.label2Pts.text())+pontos)


	#Função que seta as letras iniciais para que o tabuleiro fique igual ao do scrabble
	def setaLetrasIniciais(self):

		self.tabela_matriz.setItem(7,7,QTableWidgetItem('*'))

		for i in range(0,15,7):
			for j in range(0,15,7):
				if(not(i==7==j)):
					self.tabela_matriz.setItem(i,j,QTableWidgetItem('TP'))

		for i in range(1,5):
			self.tabela_matriz.setItem(i,i,QTableWidgetItem('DP'))
			self.tabela_matriz.setItem(14-i,14-i,QTableWidgetItem('DP'))
			self.tabela_matriz.setItem(i,14-i,QTableWidgetItem('DP'))
			self.tabela_matriz.setItem(14-i,i,QTableWidgetItem('DP'))

		for i in range(0,15,14):
			self.tabela_matriz.setItem(3,i,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(i,3,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(11,i,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(i,11,QTableWidgetItem('DL'))

		for i in range(1,15,12):
			self.tabela_matriz.setItem(5,i,QTableWidgetItem('TL'))
			self.tabela_matriz.setItem(i,5,QTableWidgetItem('TL'))
			self.tabela_matriz.setItem(9,i,QTableWidgetItem('TL'))
			self.tabela_matriz.setItem(i,9,QTableWidgetItem('TL'))

		for i in range(2,15,10):
			self.tabela_matriz.setItem(6,i,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(i,6,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(8,i,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(i,8,QTableWidgetItem('DL'))

		for i in range(3,15,8):
			self.tabela_matriz.setItem(7,i,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(i,7,QTableWidgetItem('DL'))

		for i in range(5,11,4):
			self.tabela_matriz.setItem(5,i,QTableWidgetItem('TL'))
			self.tabela_matriz.setItem(9,i,QTableWidgetItem('TL'))

		for i in range(6,10,2):
			self.tabela_matriz.setItem(6,i,QTableWidgetItem('DL'))
			self.tabela_matriz.setItem(8,i,QTableWidgetItem('DL'))


	#Função que printa o erro correspondente
	def printError(self,erro):

		string = ''
		if(erro == enumError.er_exchBigger7):
			string = 'ERRO: Impossível trocar mais que 7 letras.'
		elif(erro == enumError.er_exchBiggerPack):
			string = 'ERRO: Impossível trocar esta quantidade pois não há esta mesma quantidade de letras disponíveis.'
		elif(erro == enumError.er_exchLetterNotFound):
			string = 'ERRO: Impossível trocar pois há letras a serem trocadas que você não possui.'
		elif(erro == enumError.er_inWordLine):
			string = 'ERRO: A palavra a ser adicionada ultrapassa o mapa horizontalmente.'
		elif(erro == enumError.er_inWordCol):
			string = 'ERRO: A palavra a ser adicionada ultrapassa o mapa verticalmente.'
		elif(erro == enumError.er_inWordInexist):
			string = 'ERRO: A palavra a ser adicionada não existe no dicionário.'
		elif(erro == enumError.er_inWordInitFail):
			string = 'ERRO: A palavra a ser adicionada não atravessou o centro do mapa.'
		elif(erro == enumError.er_inWordNotTableUsed):
			string = 'ERRO: A palavra a ser adicionada não utilizou nenhuma outra letra do mapa.'
		elif(erro == enumError.er_inWordNotPossibleIn):
			string = 'ERRO: A palavra a ser adicionada não pode ser montada no mapa com suas letras.'
		elif(erro == enumError.er_inWordConflict):
			string = 'ERRO: A palavra a ser adicionada conflitou com outras palavras já presentes no mapa'

		QMessageBox.about(self, "ERROR", string)


	#Função facilitadora pois é muito utilizada no módulo
	def listToStr(self,lista):

		string = ''
		for el in lista:
			string += el + ','

		return string[0:-1]


app = QApplication([])

w = MirandasWindow()
w.show()

app.exec_()
