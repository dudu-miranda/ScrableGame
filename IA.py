#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import copy

from itertools  import permutations as permut
from tree       import *
from controle   import *

class IA(object):
    """docstring for IA"""
    def __init__(self, jogo):

        self.palavras = []
        self.jogo = jogo
        self.tree = jogo.dicionario

    def montaPalavra(self, string, direcao, limit, saquinho, noTree=None, bool=False, bool2=False):
        # direcao == (atraz == 0, frente == 1)
        # limit da profundidade da arvore e logo da recursão
        # noTree, posição da arvore na recursão
        # bool = primera recursão

        if limit == 0 or len(saquinho) == 0:
            return []

        saq     = copy.deepcopy(saquinho)
        limite  = copy.deepcopy(limit)

        #caso de primeira chamada absoluta
        if (noTree is None):
            # no = copy.deepcopy(self.tree.raiz)
            self.palavras = []
            no     = (self.tree.raiz)
            noTree = (self.tree.raiz)
            # caminha na arvore e deixa o no com a palavra de entrada na primeira recursão
            if direcao == 1:
                for i in string:
                    no = no.connections[i]
        else:
            no = (noTree)

        if direcao == 0:
            lista = self.montaPalavra("",1,limite,saq,bool=True,bool2=True)
            lista2 = []
            for i in lista:
                existPalavra = True
                lenI = len(i[0])
                str = copy.deepcopy(string)
                str = i[0]+str
                no = (noTree)
                for j in str:
                    if not no.checkConection(j):
                        existPalavra = False
                        break;
                    no = no.connections[j]
                if (no.final or bool2)and existPalavra:
                    lista2.append((str, lenI))

            return lista2

        limite -= 1
        str = copy.deepcopy(string)

        if direcao == 1:
            atual    = (no)
            contador = 0
            lenSaq   = len(saq)
            while(contador!=lenSaq):
                if saq[0] == '_':
                     lpop = saq.pop(0)
                     for i in atual.connections:
                         no   = no.connections[i]
                         str  = str+i.upper()
                         self.montaPalavra(str,direcao,limite,saq,no,False,bool2)
                         if (no.final or bool2) and str not in self.palavras:
                             self.palavras.append(str)
                         str  = str[:len(str)-1]
                         no   = (atual)
                     saq  = saq+[lpop]
                     contador += 1
                     continue

                if no.checkConection(saq[0]):
                    str  = str+saq[0]
                    no   = no.connections[saq[0]]
                    lpop = saq.pop(0)
                    self.montaPalavra(str,direcao,limite,saq,no,False,bool2)
                    saq  = saq+[lpop]
                    if (no.final or bool2) and str not in self.palavras:
                        self.palavras.append(str)
                    str  = str[:len(str)-1]
                    no   = (atual)
                else:
                    lpop = saq.pop(0)
                    saq  = saq+[lpop]
                contador += 1

            list = []
            if bool:
                for i in self.palavras:
                    list.append((i, 0))
            return list


    def permutation(self,saquinho):

        #os.system('clear')  # on linux / os x
        #print(self.jogo)
        tuplas = self.getreadwords(self.jogo.matriz)

        melhor = 0
        palavraFinal = None
        for tupla in tuplas:

            #c=[("str", "D" ,X ,Y ,ec ,bd )]
            lista = self.montaPalavra(tupla[0], 0, tupla[4], saquinho)
            lista.extend(self.montaPalavra(tupla[0], 1, tupla[5], saquinho, bool=True))

            for elemento in lista:
                if tupla[1]=='V':
                    #elemento[0]=str, tupla[2]=pos(x), tupla[3]=pos(y), elemento[1]=deslocamento, tupla[1]=direcao
                    pt = self.jogo.calculapontos(elemento[0], tupla[2]-elemento[1], tupla[3], tupla[1])
                    if melhor<pt:
                        melhor=pt
                        #row, col, word, direcao
                        palavraFinal = (tupla[2]-elemento[1]+1 ,tupla[3]+1 , elemento[0], tupla[1])

                else:
                    pt = self.jogo.calculapontos(elemento[0], tupla[2], tupla[3]-elemento[1], tupla[1])
                    if melhor<pt:
                        melhor=pt
                        #row,col,word,direcao
                        palavraFinal = (tupla[2]+1 ,tupla[3]-elemento[1]+1 , elemento[0], tupla[1])

        return palavraFinal

    #Função que gera uma tupla caso seja possivel com (Word,Dir,lin,col,espaço1,espaço2)
    def geraTupla(self,lin,col,word,direcao,tabul):

        l = []
        rec = 0
        rbd = 0
        #Caso da palavra estar na horizontal
        if direcao=='H':

            i=col+len(word)-1

            #Caso de estar colado na parede a direita
            if col==0:

                if len(tabul[lin][i+1])==1:
                        return []

                #Caso de estar colado na parede a direita e na parte superior
                if lin==0:

                    while i<13 and (len(tabul[0][i+1])!=1 and len(tabul[1][i+1])!=1 and
                                    len(tabul[0][i+2])!=1):
                        i += 1
                        rbd += 1

                    if i==13 and len(tabul[0][14])!=1:
                        rbd += 1

                #Caso de estar colado na parede a direita e na parte inferior
                elif lin ==14:

                    while i<13 and (len(tabul[14][i+1])!=1 and len(tabul[13][i+1])!=1 and
                                    len(tabul[14][i+2])!=1):
                        i += 1
                        rbd += 1

                    #A mais
                    if i==13 and len(tabul[14][14])!=1:
                        rbd+=1

                #Caso de estar colado na parede a direita e em qualquer outra parte do mapa das linhas
                else:

                    while i<13 and (len(tabul[lin][i+1])!=1 and len(tabul[lin+1][i+1])!=1 and len(tabul[lin-1][i+1])!=1 and
                                    len(tabul[lin][i+2])!=1):
                        i += 1
                        rbd += 1

                    if i==13 and len(tabul[lin][14])!=1:
                        rbd += 1

            #Caso de estar em qualquer parte do mapa em colunas
            else:

                if 14==i:
                    if len(tabul[lin][col-1])==1:
                        return []
                else:
                    if len(tabul[lin][col-1])==1 or len(tabul[lin][i+1])==1:
                        return []


                #Em qualquer coluna do mapa e na parte superior
                if lin==0:

                    while i<13 and (len(tabul[0][i+1])!=1 and len(tabul[1][i+1])!=1 and
                                    len(tabul[0][i+2])!=1):
                        i += 1
                        rbd += 1

                    if i==13 and len(tabul[0][14])!=1:
                        rbd+=1

                    i=col

                    while i!=1 and (len(tabul[0][i-1])!=1 and len(tabul[1][i-1])!=1 and
                                    len(tabul[0][i-2])!=1):
                        i -= 1
                        rec += 1

                    if i==1 and len(tabul[0][0])!=1:
                        rec +=1

                #Em qualquer coluna do mapa e na parte inferior
                elif lin ==14:

                    while i<13 and (len(tabul[14][i+1])!=1 and len(tabul[13][i+1])!=1 and
                                    len(tabul[14][i+2])!=1):
                        i += 1
                        rbd += 1

                    if i==13 and len(tabul[14][14])!=1:
                        rbd+=1

                    i = col

                    while i!=1 and (len(tabul[14][i-1])!=1 and len(tabul[13][i-1])!=1 and
                                    len(tabul[14][i-2])!=1):
                        i -= 1
                        rec += 1

                    if i==1 and len(tabul[14][0])!=1:
                        pass

                #Em qualquer coluna do mapa e em qualquer outra parte do mapa das linhas
                else:

                    while i<13 and (len(tabul[lin][i+1])!=1 and len(tabul[lin+1][i+1])!=1 and len(tabul[lin-1][i+1])!=1 and
                                    len(tabul[lin][i+2])!=1):
                        i += 1
                        rbd += 1

                    #a mais q precisa
                    if i==13 and len(tabul[lin][i+1])!=1:
                        rbd +=1

                    i = col

                    while i!=1 and (len(tabul[lin][i-1])!=1 and len(tabul[lin+1][i-1])!=1 and len(tabul[lin-1][i-1])!=1 and
                                    len(tabul[lin][i-2])!=1):
                        i -= 1
                        rec += 1

                    if i==1 and len(tabul[lin][0])!=1:
                        rec+=1


        #Caso a direção seja na vertical
        else:

            i=lin+len(word)-1
            #Caso esteja no topo do mapa
            if lin==0:

                if len(tabul[i+1][col])==1:
                    return []

                #Caso esteja no topo do mapa e no canto esquerdo do mesmo
                if col==0:
                    while i<13 and (len(tabul[i+1][0])!=1 and len(tabul[i+1][1])!=1 and
                                    len(tabul[i+2][0])!=1):
                        i+=1
                        rbd+=1

                    if i==13 and len(tabul[14][0])!=1:
                        rbd+=1

                #Caso esteja no topo do mapa e no canto direito do mesmo
                elif col==14:
                    while i<13 and (len(tabul[i+1][14])!=1 and len(tabul[i+1][13])!=1 and
                                    len(tabul[i+2][14])!=1):
                        i+=1
                        rbd+=1

                    if i==13 and len(tabul[14][14])!=1:
                        rbd+=1


                #Caso esteja no topo do mapa e em qualquer coluna do mapa
                else:
                    while i<13 and (len(tabul[i+1][col])!=1 and len(tabul[i+1][col-1])!=1 and len(tabul[i+1][col+1])!=1 and
                                    len(tabul[i+2][col])!=1 ):
                        i+=1
                        rbd+=1

                    if i==13 and len(tabul[14][col])!=1:
                        rbd+=1


            #Caso esteja em qualquer linha do mapa
            else:

                if i==14:
                    if len(tabul[lin-1][col])==1:
                        return []
                else:
                    if len(tabul[lin-1][col])==1 or len(tabul[i+1][col])==1:
                        return []

                #Caso esteja em qualquer linha do mapa e no canto esquerdo do mesmo
                if col==0:
                    while i<13 and (len(tabul[i+1][0])!=1 and len(tabul[i+1][1])!=1 and
                                    len(tabul[i+2][0])!=1):
                        i+=1
                        rbd+=1

                    if i==13 and len(tabul[14][0])!=1:
                        rbd+=1

                    i = lin
                    while i!=1 and (len(tabul[i-1][0])!=1 and len(tabul[i-1][1])!=1 and
                                    len(tabul[i-2][0])!=1):
                        i-=1
                        rec+=1

                    if i==1 and len(tabul[0][0])!=1:
                        rec+=1


                #Caso esteja em qualquer linha do mapa e no canto direito do mesmo
                elif col==14:
                    while i<13 and (len(tabul[i+1][14])!=1 and len(tabul[i+1][13])!=1 and
                                    len(tabul[i+2][14])!=1):
                        i+=1
                        rbd+=1

                    if i==13 and len(tabul[14][14])!=1:
                        rbd+=1

                    i = lin
                    while i!=1 and (len(tabul[i-1][13])!=1 and len(tabul[i-1][14])!=1 and
                                    len(tabul[i-2][14])!=1):
                        i-=1
                        rec+=1

                    if i==1 and len(tabul[0][14])!=1:
                        rec+=1

                #Caso esteja em qualquer linha do mapa e em qualquer coluna do mapa
                else:
                    while i<13 and (len(tabul[i+1][col])!=1 and len(tabul[i+1][col-1])!=1 and len(tabul[i+1][col+1])!=1 and
                                    len(tabul[i+2][col])!=1):
                        i+=1
                        rbd+=1

                    if i==13 and len(tabul[14][col])!=1:
                        rbd+=1

                    i=lin
                    while i!=1 and (len(tabul[i-1][col])!=1 and len(tabul[i-1][col-1])!=1 and len(tabul[i-1][col+1])!=1 and
                                    len(tabul[i-2][col])!=1):
                        i-=1
                        rec+=1

                    if i==1 and len(tabul[0][col])!=1:
                        rec+=1


        #Minimizador de permutações
        '''
        if len(word)==1 :
            if rec<=1 and rbd<=1:
                return []
            elif rec<=1:
                rec = 0
            elif rbd<=1:
                rbd = 0
        '''

        if rec==0 and rbd==0:
            pass
        else:
            if rec > 7:
                rec = 7
            if rbd >7:
                rbd = 7

            l.append((word,direcao,lin,col,rec,rbd))

        return l


    #Função que retorna as tuplas
    def getreadwords(self, tabul):

        if(self.jogo.inicio):
            return [('','H',7,7,7,7)]

        saida = []

        #c=[("str", "D" ,X ,Y ,ec ,bd )]
        #Itera todas as palavras do jogo
        #print(self.jogo.palavras)
        for lin, col, direcao  in  self.jogo.palavras:

            word = self.jogo.palavras[(lin, col, direcao)]
            saida.extend(self.geraTupla(lin,col,word,direcao,tabul))

            for i in range(len(word)):
                if(direcao=='H'):
                    saida.extend(self.geraTupla(lin,col+i,word[i],'V',tabul))
                else:
                    saida.extend(self.geraTupla(lin+i,col,word[i],'H',tabul))

        return saida


    #elemento[0]=str, tupla[2]=pos(x), tupla[3]=pos(y), elemento[1]=deslocamento, tupla[1]=direcao
    def calculapontos(self, word, lin, col, dir):
        pontos = 0
        for i in word:
            pontos += self.jogo.valores[i]

        return pontos

j = Jogo()
ia = IA(j)

#ia.jogo.matriz[7][7] = '*'
ia.jogo.inputWord2(5,4,'palavras','H')
ia.jogo.inputWord2(5,5,'azul','V')
ia.jogo.inputWord2(5,7,'ave','V')
ia.jogo.matriz[7][7]=' *'
ia.jogo.inicio=False

# j.packletters[0][0]='_'
# j.packletters[0][1]='e'
# j.packletters[0][2]='s'
j.packletters[0][3]='_'
# j.packletters[0][4]='_'
# j.packletters[0][5]='_'

print(ia.jogo)

#ia.jogo.inputWord2(9,4,'lassada','H')
#ia.jogo.inputWord2(5,13,'pedra','V')

#def calculapontos(self, word, lin, col, direcao):
#print(ia.jogo)
#print(ia.jogo.calculapontos('palavra',5,4,'H'))
print(ia.permutation(j.packletters[0]))
#print(ia.getreadwords(ia.jogo.matriz))

# l = ia.montaPalavra("s",1,7,['a','_','_','g','i','r','l'],bool=1)
# print(l)
# print()
# l = ia.montaPalavra("s",1,10,['a','_'],bool=1)
# print(l)
