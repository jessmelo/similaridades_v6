import networkx as nx
import pandas as pd
import seaborn as sns
import matplotlib as plt
import math
import time

###################################################################
# Apresenta a menor distância entre os nós
def shortest_path_length(H,i,j):
    try:
        short_parth=nx.shortest_path_length(H,source=i,target=j)
    except:
        short_parth = 1.0
    return(short_parth)

###################################################################
# Medida de similaridade Spath
def sim_spath(H,i,j):

    try:
        res=1/shortest_path_length(H,i,j)
    except:
        res=1.0

    return(res)

def matriz_sim_path(H,base,avaliacao,df_avaliacao):
    #u=metrica
    #n = len(nos)

    m = []
    if avaliacao == '1':
        #print(df_avaliacao[['c1','c2']])
        for index, row in df_avaliacao.iterrows():
            res = sim_spath(H, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])
            #print(row['c1'], row['c2'],row['res_in'],res)

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    else:
        for i in list(H.nodes):
            for j in list(H.nodes):
                res = sim_spath(H, i, j)
                #print(i, j, round(res, 4))
                m.append([i, j, round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_calc']

    #m = m.pivot_table(2, 0, 1, fill_value=0)
    nome_arq = str(base).replace('.graph', '')
    m.to_csv('./data_out/' + nome_arq + '_sim_path.csv', index=False)
    print('Lista de resultados: ' + './data_out/' + nome_arq + '_sim_path.csv')
    return(m)

###################################################################
# Medida de similaridade Sim_wup

def sim_wup(G, i, j):
    # definindo o no raiz da arvore
    root = "id.138875005"

    # calculando o Least Common Subsumer (Ancestor)
    LCS = nx.lowest_common_ancestor(G, i, j)

    H = G.to_undirected()
    # calculando a profundidade dos nos =  menor caminho do no até a raiz
    depth_lcs   = shortest_path_length(H, root, LCS)
    depth_node1 = shortest_path_length(H, root, i)
    depth_node2 = shortest_path_length(H, root, j)

    try:
        sim_wup = (2 * depth_lcs) / (depth_node1 + depth_node2)
    except ZeroDivisionError:
        sim_wup = 0

    return(sim_wup)

def matriz_sim_wup(G, base ,avaliacao,df_avaliacao):

    #u=metrica
    #n = len(nos)

    m = []
    if avaliacao == '1':
        #print(df_avaliacao[['c1','c2']])
        for index, row in df_avaliacao.iterrows():
            res = sim_spath(G, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])
            #print(row['c1'], row['c2'],row['res_in'],res)

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    else:
        for i in list(G.nodes):
            for j in list(G.nodes):
                res = sim_spath(G, i, j)
                #print(i, j, round(res, 4))
                m.append([i, j, round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_calc']

    #m = m.pivot_table(2, 0, 1, fill_value=0)
    nome_arq = str(base).replace('.graph', '')
    m.to_csv('./data_out/' + nome_arq + '_sim_wup.csv', index=False)
    print('Lista de resultados: ' + './data_out/' + nome_arq + '_sim_wup.csv')
    return(m)

###################################################################
# Medida de similaridade Sim_lch

def sim_lch(G, i, j):
    # medindo o menor caminho do grafo nao direcionado
    G_undirected = G.to_undirected()
    shortest_path = shortest_path_length(G_undirected, i, j)

    #print('*********************************************')
    #print('i'+str(i))
    #print('j'+str(j))
    #print('shortest_path'+str(shortest_path))
    # calcula profundidade do grafo
    Depth_ontology = nx.dag_longest_path_length(G)
    #print('Depth_ontology'+str(Depth_ontology))
    # formula:
    lch = shortest_path / (2 * Depth_ontology)
    #print('lch'+str(lch))
    if(lch == 0):
        sim_lch = 1.0
    else:
        sim_lch = -math.log10(lch)

    #print('sim_lch'+str(sim_lch))

    return(sim_lch)

def matriz_sim_lch(G, nos, base,avaliacao,df_avaliacao):

#    m = []
#    for i in nos:
#        for j in nos:
#            res = sim_lch(G, i, j)

#            #print(i, j, round(res, 4))
#            m.append([i, j, round(res, 4)])



    m = []
    if avaliacao == '1':

        #print(df_avaliacao[['c1','c2']])
        for index, row in df_avaliacao.iterrows():
            print(row)
            res = sim_lch(G, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])
            #print(row['c1'], row['c2'],row['res_in'],res)


    else:
        for i in nos:
            for j in nos:
                res = sim_lch(G, i, j)
                #print(i, j, round(res, 4))
                m.append([i, j, round(res, 4)])



    m = pd.DataFrame(m)
    #m = m.pivot_table(2, 0, 1, fill_value=0)

    m.to_csv('./data_out/' +  str(base) + '_lista_sim_lch', index=True)
    #m.to_csv('./data_out/'+'matrix_sim_lch_'+str(base), index=True)
    print('Lista de resultados: '+'./data_out/' +  str(base) + '_lista_sim_lch')
    return(m)


###################################################################
# Medida de information_content by Sanchez

def information_content(G, node):
    # calcula information content de um nó

    #print('++++++++++++++++++++++++'+str(node))
    descendants = nx.descendants(G, node)

    descendants_leaves = []
    for x in descendants:
        if (G.in_degree(x) != 0 and G.out_degree(x) == 0):
            descendants_leaves.append(x)

    num_descendants_leaves = len(descendants_leaves)
    #print('num_descendants_leaves:'+str(num_descendants_leaves))

    if (G.in_degree(node) == 0 and G.out_degree(node) != 0):
        num_subsumers = 1
    else:
        subsumers = nx.ancestors(G, node)
        num_subsumers = len(subsumers)
    #print('num_subsumers:' + str(num_subsumers))

    leaf_nodes=[]
    for nodes in G.nodes():
        if G.in_degree(nodes) != 0 and G.out_degree(nodes) == 0:
            leaf_nodes.append(nodes)

    max_leaves = len(leaf_nodes)
    #print('max_leaves:' + str(max_leaves))

    calc = (num_descendants_leaves / num_subsumers + 1) / (max_leaves + 1)
    #print('calc:' +str(node)+'|'+ str(calc))

    ic = -1*math.log10(calc)
    #print('ic:' +str(node)+'|'+ str(ic))

    #print(' ')

    return ic

###################################################################
# Medida de similaridade de lin

def sim_lin(G, i, j , lcs):
    lcs = str(lcs)

    #print('i:'+str(type(i)))
    #print('j:'+str(type(j)))
    #print('lcs:'+str(type(lcs)))

    #print(str(i)+' | '+str(j)+' | '+str(lcs))

    ic_i = information_content(G, i)
    ic_j = information_content(G, j)
    ic_lcs = information_content(G, lcs)

    #time.sleep(1)
    #print('')
    #print('ic_i: ' + str(ic_i))
    #print('ic_j: ' + str(ic_j))
    #print('lcs : ' + str(ic_lcs))

    try:
        sim_lin = (2 * ic_lcs) / (ic_i + ic_j)
    except ZeroDivisionError:
        sim_lin = 1

    return sim_lin


#Matriz de similaridade Lin
def matriz_sim_lin(G, nos, base):
    m = []
    s = []

    lista=[]
    for x in nos:
        lista.append(x)

    #print(lista)

    w = 0
    for i in lista:
        u=0
        for j in lista:

            lcs = nx.lowest_common_ancestor(G, i, j)
            #print('*****************************************************')
            #print('node_i:'+str(i))
            #print('node_j:'+str(j))
            #print('node_lcs:' + str(lcs))
            #print(' ')

            res = sim_lin(G, i, j, lcs)

            #print('sim_lin<<<<<<<<<<<<<<<<<' + str(res))

            s.append([i, j, res])
            m.append([i, j, res])

            u = u + 1
            #print('#:' + str(w) + str('|') + '#:' + str(u))
            #print('')
        w=w+1
        #time.sleep(1)

    s = pd.DataFrame(s)
    s.append([i, j, res])

    #m = m.pivot_table(2, 0, 1, fill_value=0)

    m.to_csv('./data_out/' + str(base) + '_lista_sim_IC_lin', index=True)
    #m.to_csv('./data_out/'+'matrix_sim_IC_lin_'+str(base), index=True)

    print('*****************************************************')
    print('Lista de similaridades: '+'./data_out/' +  str(base) + '_lista_sim_IC_lin')

    return(s)


###################################################################
# Medida de similaridade de resnik

# Medida de Resnik
def sim_resnik(G, node1, node2):

    lcs = nx.lowest_common_ancestor(G, node1, node2)

    sim_res = information_content(G, lcs)

    return sim_res

#Matriz de similaridade Lin
def matriz_sim_resnik(G, nos, base):
    m = []
    s = []
    for i in nos:
        for j in nos:
            res = sim_resnik(G, i, j)

            #print(i, j, res)

            s.append([i, j, res])
            m.append([i, j, res])

    s = pd.DataFrame(s)
    s.append([i, j, res])

    m = pd.DataFrame(m)
    #m = m.pivot_table(2, 0, 1, fill_value=0)

    m.to_csv('./data_out/' + str(base) + '_lista_sim_IC_resnik', index=True)
    #m.to_csv('./data_out/'+'matrix_sim_IC_resnik_'+str(base), index=True)
    print('Lista de similaridades: '+'./data_out/' +  str(base) + '_Lista_sim_IC_resnik')

    return(s)


###################################################################
# Medida de similaridade de Jiang and Conrath

# Medida de JCN
def sim_jcn(G, i, j):

    lcs = nx.lowest_common_ancestor(G, i, j)

    #print('*****************************************************')
    #print('node_i:' + str(i))
    #print('node_j:' + str(j))
    #print('node_lcs:' + str(lcs))
    #print(' ')

    #print('**********')
    ic_i = information_content(G, i)
    #print(i)
    #print(ic_i)

    #print('**********')
    ic_j = information_content(G, j)
    #print(j)
    #print(ic_j)

    #print('**********')
    ic_lcs = information_content(G, lcs)
    #print(lcs)
    #print(ic_lcs)

    try:
        sim_jcn = 1 / (ic_i + ic_j-2 * ic_lcs)
    except ZeroDivisionError:
        sim_jcn = 1

    return sim_jcn


#Matriz de similaridade Lin
def matriz_sim_jcn(G, nos, base):
    m = []
    s = []
    for i in nos:
        for j in nos:

            res = sim_jcn(G, i, j)

            #print('*******************************')
            #print(i, j, res)
            #print('*******************************')

            s.append([i, j, res])
            m.append([i, j, res])

    s = pd.DataFrame(s)
    s.append([i, j, res])

    m = pd.DataFrame(m)
    #m = m.pivot_table(2, 0, 1, fill_value=0)

    m.to_csv('./data_out/' +  str(base) + '_lista_sim_IC_jcn', index=True)
    #m.to_csv('./data_out/'+'matrix_sim_IC_jcn_'+str(base), index=True)
    print('Lista de similaridades: '+'./data_out/' +  str(base) + '_lista_sim_IC_lin')

    return(s)
