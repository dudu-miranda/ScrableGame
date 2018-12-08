#!/usr/bin/python
# -*- coding: utf-8 -*-

from itertools  import permutations as permut
from tree       import *
from controle   import *

class IA(object):
    """docstring for IA"""
    def __init__(self, jogo):
        
        self.jogo = jogo
        self.tr = jogo.dicionario
        

    def permutation(self,tabul,saquinho):

        
        print(self.jogo)

        for i in saquinho:
            if i=='_':
                saquinho.remove('_')
        c = self.getreadwords(self.jogo.matriz)

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



    def getreadwords(self, tabul):
        letras = []
        palavras = []
        #pega todas as palavras do tabuleiro
        for l in range(len(tabul)):
            for c in range(len(tabul[l])):
                if len(tabul[l][c]) == 1:
                    letras.append((tabul[l][c],l,c))

        cont  = 0
        aux   = ''
        linha = letras[cont][1]
        letras.append(('',-1,-1))

        while((len(letras)-1)>cont):
            if linha != letras[cont][1]:
                linha = letras[cont][1]
                if len(aux)>1:
                    palavras.append(aux)
                    aux = ''

            if ((letras[cont][1] == letras[cont+1][1]) and (letras[cont][2] == letras[cont+1][2]-1)) or ((letras[cont][1] != letras[cont+1][1]) and (letras[cont][2] == letras[cont-1][2]+1)) :
                if (len(aux)==0):
                    palavras.append((letras[cont][1],letras[cont][2],'H'))
                aux += letras[cont][0]

            cont += 1
        if len(aux)>1:
            palavras.append(aux)

        letras = []
        for i in range(len(tabul)):
            for j in range(len(tabul[i])):
                if len(tabul[j][i])==1:
                    letras.append((tabul[j][i],j,i))

        letras.append(('',-1,-1))
        cont   = 0
        aux    = ''
        coluna = letras[cont][2]
        while((len(letras)-1)>cont):
            if coluna != letras[cont][2]:
                coluna = letras[cont][2]
                if len(aux)>1:
                    palavras.append(aux)
                    aux = ''

            if ((letras[cont][2] == letras[cont+1][2]) and (letras[cont][1] == letras[cont+1][1]-1)) or ((letras[cont][2] != letras[cont+1][2]) and (letras[cont][1] == letras[cont-1][1]+1)):
                if (len(aux)==0):
                    palavras.append((letras[cont][1],letras[cont][2],'V'))
                aux += letras[cont][0]

            cont += 1
        if len(aux)>1:
            palavras.append(aux)
        letras.pop()
        return(palavras)

    def calculapontos(self,str):
        valores={'a':1,'b':3,'c':2,'d':2,'e':1,'f':4,'g':4,'h':4,'i':1,'j':5,'l':2,
              'm':1,'n':3,'o':1,'p':2,'q':6,'r':1,'s':1,'t':1,'u':1,'v':4,'x':8,
              'z':8,'ç':3,'_':0}
        pontos = 0
        for i in str:
            pontos += valores[i]

        return pontos
