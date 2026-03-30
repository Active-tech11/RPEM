import networkx as nx
import pandas as pd


def RA(G , ebunch) :
    RA_dic = dict ()
    for each in ebunch :
        a = sum ( 1.0 / len ( set ( G.neighbors ( w ) ) ) for w in
                  set ( G.neighbors ( each[0] ) ) & set ( G.neighbors ( each[1] ) ) )
        RA_dic[each] = a
    return RA_dic



def calculate_RA(G) :
    ebunch = list ( nx.non_edges ( G ) )
    ra_values = RA ( G , ebunch )
    
    sorted_ra_values = sorted ( ra_values.items () , key = lambda item : item[1] , reverse = True )
    print ( "节点对及其RA相似度：" )
    for i in range ( min ( 20 , len ( sorted_ra_values ) ) ) :
        print ( f"{sorted_ra_values[i][0]}: {sorted_ra_values[i][1]}" )
    return sorted_ra_values



def Calculate_jaccard(G) :
   
    non_edges = list ( nx.non_edges ( G ) )

   
    jaccard_similarities = [(u , v , len ( set ( G[u] ) & set ( G[v] ) ) / len ( set ( G[u] ) | set ( G[v] ) )) for
                            u , v in non_edges]

    
    jaccard_similarities.sort ( key = lambda x : x[2] , reverse = True )

    return jaccard_similarities



# Precision（RA） & AUC指标
def cal_PrecisionRA_and_AUC(G , target_edges) :
    preds = calculate_RA(G)
    dic = dict ()
    for (s , t) , v in preds :
        dic[(s , t)] = v
    target_edges = [tuple(edge) for edge in target_edges]
    topk_preds = sorted ( dic.items () , key = lambda x : x[1] , reverse = True )
    raTest = [each[0] for each in topk_preds[:len ( target_edges )]]
    items = set ( raTest ) & set ( target_edges )
    precision = float ( len ( items ) ) / len ( target_edges )
   
    edgesNotexit = set(nx.non_edges (G))
    AUC = 0.0
    for k in target_edges :
        for l in edgesNotexit :
            if k in dic and l in dic :
                if dic[k] > dic[l] :
                    AUC += 1
                if dic[k] == dic[l] :
                    AUC += 0.5
    AUC /= len ( target_edges ) * len ( edgesNotexit )
    print(f"precision: {precision}")
    print(f"AUC: {AUC}")
    return precision , AUC



def cal_PrecisionJA_and_AUC(G, target_edges ) :
    preds =Calculate_jaccard(G)
    dic = dict ()
    for s , t , v in preds :
        dic[(s , t)] = v
    topk_preds = sorted ( dic.items () , key = lambda x : x[1] , reverse = True )
    raTest = [each[0] for each in topk_preds[:len ( target_edges )]]
    items = set ( raTest ) & set ( target_edges )
    precision = float ( len ( items ) ) / len ( target_edges )
   
    #edgesNotexit = set ( complete_edges ) - set ( perturb.edges ) - set ( test_edges )
    edgesNotexit = set(nx.non_edges (G))
    auc = 0.0
    for k in target_edges :
        for l in edgesNotexit :
            if k in dic and l in dic :
                if dic[k] > dic[l] :
                    auc += 1
                if dic[k] == dic[l] :
                    auc += 0.5
    auc /= len ( target_edges ) * len ( edgesNotexit )
    return precision , auc


