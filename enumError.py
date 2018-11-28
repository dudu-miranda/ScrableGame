#!/usr/bin/python
# -*- coding: utf-8 -*-

class enumError(object):

	#Erro onde a lista passada de letras a serem trocadas tem tamanho maior que 7
	er_exchBigger7 = 11
	#Erro onde a lista passada de letras a serem trocadas tem tamanho maior que a lista de letras disponiveis
	er_exchBiggerPack = 2
	#Erro da interseção acima de um tamanho menor que o conjunto passado significa que tem alguma letra que o player não possui e deseja trocar
	er_exchLetterNotFound = 3
	#Erro onde a palavra a ser adicionada ultrapassa o mapa horizontalmente
	er_inWordLine = 4
	#Erro onde a palavra a ser adicionada ultrapassa o mapa verticalmente
	er_inWordCol = 5
	#Erro onde a palavra a ser adicionada não existe no dicionário
	er_inWordInexist = 6
	#Erro onde a palavra a ser adicionada não passa no centro do mapa como deveria ser na primeira jogada
	er_inWordInitFail = 7
	#Erro onde a palavra a ser adicionada não utiliza nenhuma letra ja presente no tabuleiro
	er_inWordNotTableUsed = 8
	#Erro onde a palavra a ser adicionada não pode ser montada no tabuleiro
	er_inWordNotPossibleIn = 9
	#Erro onde a palavra a ser adicionada da conflito com  as outras palavras já presentes no tabuleiro
	er_inWordConflict = 10

	