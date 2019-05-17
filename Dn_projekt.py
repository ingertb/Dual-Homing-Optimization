#!/usr/bin/env python
# coding: utf-8

# In[1]:


#create a random network

import  networkx as nx

n_nodes=40  #number of nodes
ba = nx.barabasi_albert_graph(n_nodes, 1)


# In[2]:


#Assing funtion of nodes

#counters
cont_endponint=0
cont_server=0
cont_router=0

# Iterate over end nodes:
for v in nx.degree(ba):
    #if node connects only to one neighbour
    if v[1] == 1:
        
        #mark as endpoint and add numer:
        cont_endponint+=1
        ba.nodes[v[0]]['type'] = 'Ep'+str(cont_endponint)
        
        #if node has more connection choose whether is Server or router
    else:  
        if v[0] % 2 == 0:
            cont_router+=1
            ba.nodes[v[0]]['type'] = 'R'+str(cont_router)  
        else:
            cont_server+=1
            ba.nodes[v[0]]['type'] = 'S'+str(cont_server)               
                
print ('-Numer of endpoints:', cont_endponint,', -Numer of routers:',cont_router,', -Numer of servers:',cont_server)


# In[3]:


#create a dataframe to organize and analyze the information of the network 
#and add parameters of the each link
import pandas as pd

#capacity of links
SRV_LINK_CAP = 150
RUT_LINK_CAP = 200
EP_LINK_CAPu = 8
EP_LINK_CAPd = 16

#cost of using the links
SRV_LINK_UCOST = 10
RUT_LINK_UCOST = 15
EP_LINK_UCOST = 5

#cost of open the links
SRV_LINK_OCOST = 20
RUT_LINK_OCOST = 25
EP_LINK_OCOST = 10
        
data = pd.DataFrame([], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost', 'O_cost'])
for v in nx.degree(ba): 
    adj = list(nx.neighbors(ba, v[0]))
    for neig in adj:
        if ba.nodes[v[0]]['type'][0:1] == 'R' and ba.nodes[neig]['type'][0:1] == 'R': 
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],RUT_LINK_CAP,RUT_LINK_UCOST,RUT_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)
            
        elif ba.nodes[v[0]]['type'][0:1] == 'R' and ba.nodes[neig]['type'][0:1] == 'S':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],SRV_LINK_CAP,SRV_LINK_UCOST,SRV_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)
        
        elif ba.nodes[v[0]]['type'][0:1] == 'R' and ba.nodes[neig]['type'][0:1] == 'E':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],EP_LINK_CAPd,EP_LINK_UCOST,EP_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)
        
        elif ba.nodes[v[0]]['type'][0:1] == 'S' and ba.nodes[neig]['type'][0:1] == 'S':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],SRV_LINK_CAP,SRV_LINK_UCOST,SRV_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)
        
        elif ba.nodes[v[0]]['type'][0:1] == 'S' and ba.nodes[neig]['type'][0:1] == 'R':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],SRV_LINK_CAP,SRV_LINK_UCOST,SRV_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)

        elif ba.nodes[v[0]]['type'][0:1] == 'S' and ba.nodes[neig]['type'][0:1] == 'E':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],EP_LINK_CAPd,EP_LINK_UCOST,EP_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)
        
        elif ba.nodes[v[0]]['type'][0:1] == 'E' and ba.nodes[neig]['type'][0:1] == 'S':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],EP_LINK_CAPu,EP_LINK_UCOST,EP_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)

        elif ba.nodes[v[0]]['type'][0:1] == 'E' and ba.nodes[neig]['type'][0:1] == 'R':   
            data = data.append(pd.DataFrame([['',v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],EP_LINK_CAPu,EP_LINK_UCOST,EP_LINK_OCOST]], columns=['Edge_id','From_id','To_id','From_type','To_type','Capacity','U_cost','O_cost']), ignore_index = True)

data.index=data.index+1            
data['Edge_id'] = data.index #add index route
data.to_csv('network.csv') #create a .csv file with the information of the network


# In[10]:


#cost of using the nodes
SRV_NODE_COST = 10
RUT_NODE_COST = 15
EP_NODE_COST = 5

dat_node = pd.DataFrame([], columns=['id','type'])
dat_node['id'] = data['From_id']
dat_node['type'] = data['From_type']
dat_node = dat_node.drop_duplicates(subset='type', keep='first')
dat_node = dat_node.reset_index(drop=True)
dat_node['O_cost'] = ''

dat_node.index= dat_node.index+1

for i in range (1, len(dat_node)+1):
    if dat_node['type'][i][0:1] == 'R':
        dat_node['O_cost'][i] = RUT_NODE_COST
    elif dat_node['type'][i][0:1] == 'S':
        dat_node['O_cost'][i] = SRV_NODE_COST
    elif dat_node['type'][i][0:1] == 'E':
        dat_node['O_cost'][i] = EP_NODE_COST


# In[11]:


#create the network with the new indexes 
Network = nx.Graph()
Network.add_nodes_from([1, n_nodes])
for i in range(1, len(data)+1):
    Network.add_edge(data['From_id'][i], data['To_id'][i])


# In[12]:


#draw the network
import matplotlib.pyplot as plt

nx.draw(Network, with_labels=True, font_weight='bold', pos=nx.spring_layout(Network))
plt.savefig("path.png")
plt.show()
print ('-Numer of endpoints:', cont_endponint,', -Numer of routers:',cont_router,', -Numer of servers:',cont_server)


# In[13]:


data.head(len(data)) 


# In[14]:


dat_node.head(len(dat_node))



# In[8]:


Vn=n_nodes
En=0
for i in range(len(data)): 
    if En <= data['Edge_id'][i]:
        En = data['Edge_id'][i]


# In[9]:


#create de file data.dat with the information of the network for optimization
with open("data.dat", "w") as f:
    f.write("""
data;
#-----------------------------------------------------------------------
#liczba łuki, zapotrzebowań oraz ścieżek

param Vn := {Vn};
param En := {En};
param Dn := {Dn};
#-----------------------------------------------------------------------
#rozmiar zapotrzebowania d, węzeł żródłowy d, węzeł docelowy d

param : h  s  t :=
 1      {h} {s} {t}
 2      {h} {s} {t2} 
;
        """.format(Vn=Vn, En=En, Dn=2, h=8, s=21, t=33,t2=24))

#*************************************************************************

with open("data.dat", "a") as f:
    f.write("""
#-----------------------------------------------------------------------
#węzłe-łącze  Aev(e,v) 
param : A :=
""")

    for i in range(En):       
        f.write("""  {link_number}  {From_edge_number}    1
""".format(link_number=data['Edge_id'][i], From_edge_number=data['From_id'][i]))
    f.write(""";""")

#*************************************************************************    
    
with open("data.dat", "a") as f:
    f.write("""

#----------------------------------------------------------------------- 
#węzłe-łącze  Bev(e,v) 
param : B :=
""")
        
    for i in range(En):       
        f.write("""  {link_number}  {to_edge_number}    1
""".format(link_number=data['Edge_id'][i], to_edge_number=data['To_id'][i]))
    f.write(""";""")

#*************************************************************************    
    
with open("data.dat", "a") as f:
    f.write("""

#-----------------------------------------------------------------------       
#koszt jednostkowy użycia przepływności na łączach     
param : K :=
""")
    for i in range(En):       
        f.write("""  {link_number}  {cost}
""".format(link_number=data['Edge_id'][i], cost=data['Cost'][i]))
    f.write(""";""")
    
#*************************************************************************    
    
with open("data.dat", "a") as f:
    f.write("""

#-----------------------------------------------------------------------       
#koszt jednostkowy użycia przepływności na łączach     
param : C :=
""")
    for i in range(En):       
        f.write("""  {link_number}  {cap}
""".format(link_number=data['Edge_id'][i], cap=data['Capacity'][i]))
    f.write(""";""")
        
#*************************************************************************        
        
with open("data.dat", "a") as f:
    f.write("""
    
#----------------------------------------------------------------------- 
#upper bound for the degree of transit node v     
param : G :=
""")
    for i in range(1,Vn+1):       
        f.write("""  {node_number}  {grade}
""".format(node_number=i, grade=Network.degree[i]))        
    f.write(""";""")

#*************************************************************************      
    
    
with open("data.dat", "a") as f:
     f.write("""
end;
""")


# In[10]:


#run the math-program with the data of the network created 
get_ipython().system('cbc projekt.mod%data.dat -solve -solu result.csv')


# In[47]:


#clean and organize the data optained in the 
with open("wynik.csv", "r") as f:
    fl =f.readlines()
    f.close()

data_r = pd.DataFrame([], columns=['Demand','Edge','flow'])        
#data = data.append(pd.DataFrame([[v[0]+1,neig+1,ba.nodes[v[0]]['type'],ba.nodes[neig]['type'],ba[v[0]][neig]['cost'],ba[v[0]][neig]['capacity']]], columns=['From_index','To_index','From_type','To_type','Cost','Capacity']), ignore_index = True)        
for j in range (len(fl)):
    flag =0
    temp1=''
    temp2=''
    temp3=''
    for i in range (len(fl[j])):
        if fl[j][i] == 'u' and flag == 0:
            flag =1                    
        elif fl[j][i] == '[' and flag == 1:
            flag =2
        elif fl[j][i] != ',' and flag == 2:        
            temp1 = temp1+fl[j][i]
        elif fl[j][i] == ',' and flag == 2:
            flag =3            
        elif fl[j][i] != ']' and flag == 3:
            temp2 = temp2+fl[j][i]            
        elif fl[j][i] == ']' and flag == 3:
            flag =4
        elif fl[j][i] != ' ' and flag == 4:
            flag =5
            temp3 = temp3+fl[j][i]
        elif fl[j][i] != ' ' and flag == 5:
            temp3 = temp3+fl[j][i]
        elif fl[j][i] == ' ' and flag == 5:
            break
    if temp1 != '':        
        data_r = data_r.append(pd.DataFrame([[temp2,temp1,temp3]], columns=['Demand','Edge','flow']), ignore_index = True)        


# In[48]:


Net_demand = nx.Graph()
data_r['From']=''
data_r['To']=''
for i in range(len(data_r)):
    Net_demand.add_node(data.iloc[(int(data_r.iloc[i]['Edge']))-1]['From_id'])
    Net_demand.add_node(data.iloc[(int(data_r.iloc[i]['Edge']))-1]['To_id'])
    data_r['From'][i]=str(data.iloc[(int(data_r.iloc[i]['Edge']))-1]['From_id'])+' - '+str(data.iloc[(int(data_r.iloc[i]['Edge']))-1]['From_type'])
    data_r['To'][i]=str(data.iloc[(int(data_r.iloc[i]['Edge']))-1]['To_id'])+' - '+str(data.iloc[(int(data_r.iloc[i]['Edge']))-1]['To_type'])

    #print (data_r.iloc[i]['Edge'], data.iloc[(int(data_r.iloc[i]['Edge']))-1]['From_index'], data.iloc[(int(data_r.iloc[i]['Edge']))-1]['To_index'])
for i in range(len(data_r)):    
    Net_demand.add_edge(data['From_id'][(int(data_r.iloc[i]['Edge']))-1], data['To_id'][(int(data_r.iloc[i]['Edge']))-1])
   


# In[49]:


data_r.head(len(data_r))    


# In[50]:


nx.draw(Net_demand, with_labels=True, font_weight='bold', pos=nx.spring_layout(Net_demand))
plt.savefig("demands.png")
plt.show() 


# In[ ]:




