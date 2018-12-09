#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from itertools  import permutations as permut
from tree       import *
from controle   import *

class IA(object):
    """docstring for IA"""
    def __init__(self, jogo):
        
        self.jogo = jogo
        self.tr = jogo.dicionario
        self.valores={'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':4,'h':4,'i':1,'j':5,'l':2,
        'm':1,'n':3,'o':1,'p':2,'q':6,'r':1,'s':1,'t':1,'u':1,'v':4,'x':8,
        'z':8,'ç':3,'_':0}
        

    def permutation(self,tabul,saquinho):

        #os.system('clear')  # on linux / os x
        print(self.jogo)
        c = self.getreadwords(self.jogo.matriz)
        print(c)
        
        for i in saquinho:
            if i=='_':
                saquinho.remove('_')
        #c=[("str", "D" ,X ,Y ,ec ,bd )]
        # Caso de Start
        if len(c)==0:
            c.append((7,7,'H'))
            c.append('')


        # exit()

        per_palavras = []

        #Pega as letras e coloca como "palavras"
        for i in range(len(c)):
            if (i%2)!=0:
                cont = 0
                for j in c[i]:
                    if c[i-1][2]=='H':
                        c.append((c[i-1][0],c[i-1][1]+cont,'V'))
                        c.append(j)
                    else:
                        c.append((c[i-1][0]+cont,c[i-1][0],'H'))
                        c.append(j)
                    cont += 1

        print(c)
        print(saquinho)
        # exit()

        #pega somente as palavras
        for i in range(len(c)):
            if (i%2)!=0:
                per_palavras.append(c[i])

        melhorpontos = 0
        palavrafinal  = ()

        for i in per_palavras:
            aux = []
            aux.append(i)
            for k in range(len(saquinho)+1):
                for j in range(0,k):
                    aux.append(saquinho[j])
                for o in range(k,len(saquinho)):
                    aux.append(saquinho[o])
                    for j in permut(aux):
                        word = ''
                        for p in j:
                            if type(p)==tuple:
                                for t in range(len(p)):
                                    word += p[t]
                            else:
                                word += p
                        #verificar pontuação
                        #verificar se pode ser usada
                        pontos = self.calculapontos(word)
                        #verificar se é a melhor palavra
                        #e se pode entrar no tabuleiro
                        if (len(word)>2) and (pontos > melhorpontos) and self.jogo.checkWord(c[c.index(i)-1][0]+1,c[c.index(i)-1][1]+1,word,c[c.index(i)-1][2])==1:
                                palavrafinal  = (c[c.index(i)-1],word)
                                melhorpontos = pontos
                    aux.pop()
                for j in range(0,k):
                    aux.pop()

        #caso onde não existe possibilidade de palavra
        if len(palavrafinal)==0:
            print ('SEM PAlAVRAS VALIDAS')
            return (0,0,'','')

        desc = 0
        if (palavrafinal[0][0],palavrafinal[0][1],palavrafinal[0][2]) in c:
            desc = palavrafinal[1].index(c[c.index((palavrafinal[0][0],palavrafinal[0][1],palavrafinal[0][2])) +1])

        if desc != 0:
            if palavrafinal[0][2]=='V':
                return (palavrafinal[0][0]+1-desc,palavrafinal[0][1]+1,palavrafinal[1],palavrafinal[0][2])
            else:
                return (palavrafinal[0][0]+1,palavrafinal[0][1]+1-desc,palavrafinal[1],palavrafinal[0][2])

        return (palavrafinal[0][0]+1,palavrafinal[0][1]+1,palavrafinal[1],palavrafinal[0][2])



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

                #Caso de estar colado na parede a direita e na parte superior
                if lin==0:

                    while i<14 and len(tabul[0][i+1])!=1 and len(tabul[1][i+1])!=1:
                        i += 1
                        rbd += 1

                #Caso de estar colado na parede a direita e na parte inferior
                elif lin ==14:

                    while i<14 and len(tabul[14][i+1])!=1 and len(tabul[13][i+1])!=1:
                        i += 1
                        rbd += 1

                #Caso de estar colado na parede a direita e em qualquer outra parte do mapa das linhas
                else:

                    while i<14 and len(tabul[lin][i+1])!=1 and len(tabul[lin+1][i+1])!=1 and len(tabul[lin-1][i+1])!=1:
                        i += 1
                        rbd += 1

            #Caso de estar em qualquer parte do mapa em colunas
            else:

                #Em qualquer coluna do mapa e na parte superior
                if lin==0:
                    
                    while i<14 and len(tabul[0][i+1])!=1 and len(tabul[1][i+1])!=1:
                        i += 1
                        rbd += 1

                    i=col

                    while i!=0 and len(tabul[0][i-1])!=1 and len(tabul[1][i-1])!=1:
                        i -= 1
                        rec += 1

                #Em qualquer coluna do mapa e na parte inferior
                elif lin ==14:

                    while i<14 and len(tabul[14][i+1])!=1 and len(tabul[13][i+1])!=1:
                        i += 1
                        rbd += 1

                    i = col

                    while i!=0 and len(tabul[14][i-1])!=1 and len(tabul[13][i-1])!=1:
                        i -= 1
                        rec += 1

                #Em qualquer coluna do mapa e em qualquer outra parte do mapa das linhas
                else:

                    while i<14 and len(tabul[lin][i+1])!=1 and len(tabul[lin+1][i+1])!=1 and len(tabul[lin-1][i+1])!=1:
                        i += 1
                        rbd += 1

                    i = col

                    while i!=0 and len(tabul[lin][i-1])!=1 and len(tabul[lin+1][i-1])!=1 and len(tabul[lin-1][i-1])!=1:
                        i -= 1
                        rec += 1


        #Caso a direção seja na vertical
        else:

            i=lin+len(word)-1
            #Caso esteja no topo do mapa
            if lin==0:

                #Caso esteja no topo do mapa e no canto esquerdo do mesmo
                if col==0:
                    while i<14 and len(tabul[i+1][0])!=1 and len(tabul[i+1][1])!=1 :
                        i+=1
                        rbd+=1

                #Caso esteja no topo do mapa e no canto direito do mesmo
                elif col==14:
                    while i<14 and len(tabul[i+1][14])!=1 and len(tabul[i+1][13])!=1:
                        i+=1
                        rbd+=1


                #Caso esteja no topo do mapa e em qualquer coluna do mapa
                else:
                    while i<14 and len(tabul[i+1][col])!=1 and len(tabul[i+1][col-1])!=1 and len(tabul[i+1][col+1])!=1:
                        i+=1
                        rbd+=1


            #Caso esteja em qualquer linha do mapa
            else:

                #Caso esteja em qualquer linha do mapa e no canto esquerdo do mesmo
                if col==0:
                    while i<14 and len(tabul[i+1][0])!=1 and len(tabul[i+1][1])!=1:
                        i+=1
                        rbd+=1

                    i = lin
                    while i!=0 and len(tabul[i-1][0])!=1 and len(tabul[i-1][1])!=1:
                        i-=1
                        rec+=1


                #Caso esteja em qualquer linha do mapa e no canto direito do mesmo
                elif col==14:
                    while i<14 and len(tabul[i+1][13])!=1 and len(tabul[i+1][14])!=1:
                        i+=1
                        rbd+=1

                    i = lin
                    while i!=0 and len(tabul[i-1][13])!=1 and len(tabul[i-1][14])!=1:
                        i-=1
                        rec+=1

                #Caso esteja em qualquer linha do mapa e em qualquer coluna do mapa
                else:
                    while i<14 and len(tabul[i+1][col])!=1 and len(tabul[i+1][col-1])!=1 and len(tabul[i+1][col+1])!=1:
                        i+=1
                        rbd+=1

                    i=lin
                    while i!=0 and len(tabul[i-1][col])!=1 and len(tabul[i-1][col-1])!=1 and len(tabul[i-1][col+1])!=1:
                        i-=1
                        rec+=1


        if rec==0 and rbd==0:
            pass
        else:
            if rec > 7:
                rec = 7
            if rbd >7:
                rbd = 7

            l.append((word,direcao,lin,col,rec,rbd))

        return l


    def getreadwords(self, tabul):
        
        #if(self.jogo.inicio):
        #    return [('','H',7,7,7,7)]

        saida = []

        #c=[("str", "D" ,X ,Y ,ec ,bd )]
        #Itera todas as palavras do jogo
        print(self.jogo.palavras)
        for lin, col, direcao  in  self.jogo.palavras:
            
            word = self.jogo.palavras[(lin, col, direcao)]
            saida.extend(self.geraTupla(lin,col,word,direcao,tabul))

            for i in range(len(word)):
                if(direcao=='H'):
                    saida.extend(self.geraTupla(lin,col+i,word[i],'V',tabul))
                else:
                    saida.extend(self.geraTupla(lin+i,col,word[i],'H',tabul))            
        
        return saida


    def calculapontos(self,str):
        pontos = 0
        for i in str:
            pontos += self.valores[i]

        return pontos



ia = IA(Jogo())

ia.jogo.inputWord2(2,7,'zalavra','H')
ia.jogo.inputWord2(1,7,'azul','V')
ia.jogo.matriz[7][7] = '  '

print(ia.jogo)

print(ia.getreadwords(ia.jogo.matriz))
