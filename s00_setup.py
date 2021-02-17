#!/usr/bin/env python
import networkx as nx
import numpy as np
import seaborn as sns
import matplotlib as plt
import os
import time
import pickle
from s01_load import *
from s02_plot import *
from s03_functions import *
from s04_mesures import *

print('')
print('#####################################################################')
print('## PPGSI - EACH/USP 2020 ############################################')
print('## LCDS  - 5965830       ############################################')
print('## Similaridades v4      ############################################')
print('#####################################################################')

'****************************************************************************'
print('')
print('#####################################################################')
print('## Menu de ontologias    ############################################')
print('#####################################################################')
print('')

encontrar_arq()

print('---------------------------------------------------------------------')
print('* Ontologias disponíveis:')

dic=criar_menu_arq()

print('---------------------------------------------------------------------')
ontologia=input('Qual arquivo/ontologia você deseja utilizar?')
print(dic[int(ontologia)])

'****************************************************************************'
print('')
print('#####################################################################')
print('## Menu de medidas       ############################################')
print('#####################################################################')
print('')
print('---------------------------------------------------------------------')
print('* Medidas de similaridade disponíveis:')
print(' 1 - Sim_path   :  Path based - Caminho mínimo')
print(' 2 - Sim_wup    :  Path based - Wu e Palmer')
print(' 3 - Sim_lch    :  Path based - Leacock e Chodorow')
print(' 4 - Sim_lin    :  IC based - Lin')
print(' 5 - Sim_res    :  IC based - Resnik')
print(' 6 - Sim_jcn    :  IC based - Jiang e Conrath')
#print(' 7 - Sim_ilin   :  i-Lin')
#print(' 8 - Sim_ires   :  i-Res')
#print(' 9 - Sim_ijcn   :  i-JCN')
#print('10 - Rel_lesk   :  Lesk')
#print('11 - Rel_vector :  Vector')
print('---------------------------------------------------------------------')

medida = input('Escolha uma medida (utilize os números):')

medida_dic={
    '1':'Sim_path',
    '2':'Sim_wup',
    '3':'Sim_lch',
    '4':'Sim_lin',
    '5':'Sim_res',
    '6':'Sim_jcn',
    '7':'Sim_ilin',
    '8':'Sim_ires',
    '9':'Sim_ijcn',
    '10':'lesk',
    '11':'vector'
}
print(medida_dic[medida])
print('')
print('---------------------------------------------------------------------')
print('')
print('#####################################################################')
print('## Avaliação             ############################################')
print('#####################################################################')
print('')

avaliacao=input('Deseja utilizar uma base de avaliação? 1-Sim/2-Não')
#print(avaliacao)
print('')

if avaliacao == '1':
    encontrar_arq_avaliacao()
    print('* Avaliações disponíveis:')

    dic_avaliacao=criar_menu_arq_avaliacao()

    print('')
    avalia_input=input('Qual arquivo de avaliação você deseja utilizar?')
    avaliacao_nome=dic_avaliacao[int(avalia_input)]
    print(avaliacao_nome)

print('---------------------------------------------------------------------')
print('')
print('* Experimento selecionado:')

if avaliacao == '1':
    print(dic[int(ontologia)]+', '+ medida_dic[medida]+' e '+dic_avaliacao[int(avalia_input)])
    base=dic[int(ontologia)]
    df_avaliacao = carga_de_avaliacao(avaliacao_nome)
else:
    print(dic[int(ontologia)]+' e '+ medida_dic[medida])
    base=dic[int(ontologia)]
    df_avaliacao = ''
print('---------------------------------------------------------------------')

'****************************************************************************'
print('')
print('#####################################################################')
print('## Plot                  ############################################')
print('#####################################################################')
print('')

path = './data_in/' + base
data = pickle.load(open(path, "rb"))
H = data[0]
G = data[1]

grafo_imagem = input('Deseja representar a imagem do grafo? 1-Sim/2-Não')
print('* Escolha: '+str(grafo_imagem))
if grafo_imagem == '1':
    draw_grafo=draw_Digraph(nos,arestas,base)

path = './data_in/'
arr = os.listdir(path)
lista = [arq for arq in arr if
         (arq.endswith(".owl") or arq.endswith(".rdf"))]

#print(lista)
for i in lista:
    shutil.move(path+str(i), './owl_rdf/')
'****************************************************************************'
print('')
print('#####################################################################')
print('## Resultados            ############################################')
print('#####################################################################')
print('')

print("Medida selecionada: "+ str(medida_dic[medida]))

if medida_dic[medida] == 'Sim_path':
    ini = time.time()
    m=matriz_sim_path(H,base,avaliacao,df_avaliacao)
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_wup':
    ini = time.time()
    m=matriz_sim_wup(G,base,avaliacao,df_avaliacao)
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_lch':
    ini = time.time()
    m=matriz_sim_lch(G,base,avaliacao,df_avaliacao)
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_ires':
    ini = time.time()
    m=matriz_sim_ires(G, nos, base)
    fim = time.time()
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_ijcn':
    ini = time.time()
    m=matriz_sim_ijcn(G, nos, base)
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_ilin':
    ini = time.time()
    m=matriz_sim_ilin(G, nos, base)
    fim = time.time()
    print("Duração: " + str(fim - ini))



elif medida_dic[medida] == 'Sim_res':
    ini = time.time()
    m=matriz_sim_resnik(G, nos, base)
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_jcn':
    ini = time.time()
    m = matriz_sim_jcn(G, nos, base)
    fim = time.time()
    print("Duração: " + str(fim - ini))

elif medida_dic[medida] == 'Sim_lin':
    ini = time.time()
    m=matriz_sim_lin(G, nos, base)
    fim = time.time()
    print("Duração: " + str(fim - ini))
