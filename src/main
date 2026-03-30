if __name__ == '__main__' :
    edges = pd.read_csv ( 'DataSet\dolphins_perturb.csv' , header = None , sep = '\t' ).values
    G = nx.Graph ()
    G.add_edges_from ( edges )
    target_edges = pd.read_csv ( 'DataSet\\target_edges.csv' , header = None , sep = '\t').values

    cal_PrecisionRA_and_AUC ( G, target_edges)

    #cal_PrecisionJA_and_AUC( G , target_edges)
