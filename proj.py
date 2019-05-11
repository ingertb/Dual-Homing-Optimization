import  networkx as nx
import matplotlib.pyplot as plt

# G = nx.Graph()


# er = nx.erdos_renyi_graph(100, 0.15)
# ws = nx.watts_strogatz_graph(30, 3, 0.1)
ba = nx.barabasi_albert_graph(40, 1)
# red = nx.random_lobster(20, 0.5, 0.9)

plt.plot(1)

nx.draw(ba, with_labels=True, font_weight='bold')
# print(nx.average_degree_connectivity(ba))
# print(nx.number_of_edges(ba))
# print(nx.degree(ba))

SRV_CMP_PWR = 1000
SRV_LINK_CAP = 100
RUT_LINK_CAP = 200

# Iterate over end nodes:
for v in nx.degree(ba):

        #if node connects only to one neighbour
    if v[1] == 1:

        #mark as endpoint:
        ba.nodes[v[0]]['type'] = 'Endpoint'
        # print('node number: ', v[0])
        # print(ba.nodes[v[0]])

        #add maximum capacity of connection
        adj = list(nx.neighbors(ba, v[0]))
        # print(adj)
        ba[v[0]][adj[0]]['capacity'] = 100
        print(ba[v[0]][adj[0]])
    # elif 1<=v[1]<=4:
    #     print('aa')

        #if node has more connection choose whether is Server or router
    else:
        ba.nodes[v[0]]['type'] = 'Router' if v[0] % 2 == 0 else 'Server'
        # print('node number: ', v[0])
        # print(ba.nodes[v[0]])
        adj = list(nx.neighbors(ba, v[0]))
        for neig in adj:
            if ba.nodes[v[0]]['type'] == 'Router':
                ba[v[0]][neig]['capacity'] = RUT_LINK_CAP
                # print(node)
            if ba.nodes[v[0]]['type'] == 'Server':
                ba[v[0]][neig]['capacity'] = SRV_LINK_CAP
                # print(node)

    print('node number: ', v[0])
    # print(ba.nodes[v[0]])
    for neig in adj:
        print('for link:' ,v[0],' ',neig,'attributes:', ba[v[0]][neig])

plt.plot(2)
nx.draw(ba,pos=nx.spring_layout(ba), with_labels=True, font_weight='bold')
plt.show()

#TODO: dual homming
#TODO: uzwględnienie FPS i opóźnienia
#TODO: liczna oznacza np: MFLOPs


#TODO: algorytm herustyka
