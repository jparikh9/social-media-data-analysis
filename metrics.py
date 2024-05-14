import networkx as nx
import os.path
import pandas as pd

if __name__ == '__main__':
    print("network measure calculations")
    #file_path = 'C:/Users/jinit/PycharmProjects/osna_project_1/edges.csv'

    if os.path.exists("edges.csv"):
        edges = pd.read_csv("edges.csv")
        G = nx.from_pandas_edgelist(edges, 'source', 'target', create_using=nx.DiGraph())
        #nx.draw(G)
        degree_centrality = nx.degree_centrality(G)
        print(degree_centrality)
        dc = pd.DataFrame(degree_centrality.items(),columns=["node", "measure"])
        dc.to_csv("degree_centrality_networkx.csv",index=False)
        closeness = nx.closeness_centrality(G)
        close = pd.DataFrame(closeness.items(), columns=["node", "measure"])
        close.to_csv("closeness_centrality_networkx.csv", index=False)
        betweenness = nx.betweenness_centrality(G)
        between = pd.DataFrame(betweenness.items(), columns=["node", "measure"])
        between.to_csv("betweenness_centrality_networkx.csv", index=False)
        pagerank = nx.pagerank(G)
        pr = pd.DataFrame(pagerank.items(), columns=["node", "measure"])
        pr.to_csv("pagerank_networkx.csv", index=False)
        clustering = nx.clustering(G)
        cluster = pd.DataFrame(clustering.items(), columns=["node", "measure"])
        cluster.to_csv("clustering_networkx.csv", index=False)
        hubs, authorities = nx.hits(G)
        #print(hubs)
        h = pd.DataFrame(hubs.items(), columns=["node", "measure"])
        h.to_csv("hubs(hits)_networkx.csv", index=False)
        a = pd.DataFrame(authorities.items(), columns=["node", "measure"])
        h.to_csv("authorities(hits)_networkx.csv", index=False)
