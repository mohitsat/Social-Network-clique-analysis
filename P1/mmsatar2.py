import networkx as nx
from collections import defaultdict
import sys
import matplotlib.pyplot as plt

class socialNetwork(object):
  """docstring for socialNetwork"""
  def __init__(self):
    super(socialNetwork, self).__init__()

  featuresMap = {}

  def build_graphList(self, egonet):
    newgraph = nx.Graph()
    newgraph.add_node(0)
    for line in open(egonet):
      a, b = line.split(':')
      newgraph.add_edge(0,int(a))
      b = b.split()
      for e in b:
        if e == a: continue
        newgraph.add_edge(int(a),int(e))
    return newgraph


  def splitvalues(self, line, value):
     if value in line:
        attribute = line.split(value)
        if len(attribute) > 0:
          return attribute[1].split(" ")[0]
     else:
       return None


  def makedata(self, filename, egonet):
      for line in open(filename):
        split = line.split(" ")
        requiredvalue = {}
        requiredvalue["id"] = split[0]
        requiredvalue["school_id"] = self.splitvalues(line, "education;school;id;")
        requiredvalue["work_id"] = self.splitvalues(line, "work;employer;id;")
        requiredvalue["language"] = self.splitvalues(line, "languages;name;")
        self.featuresMap[split[0]] = requiredvalue 
      


  def hypothesis1(self, egonet):
    schoolMap = {}
    workMap = {}
    count = 0
    nodegraph = self.build_graphList(egonet)
    egoNode = egonet.split("/")[1].split(".")[0]
    for node in nodegraph.nodes:
      strinnpde = str(node)
      if strinnpde in self.featuresMap:
        nodedet = self.featuresMap[strinnpde]
        key = nodedet["school_id"]
        if key in schoolMap:
          temp = schoolMap[key]
          temp.append(node)
        else:
          temp = [node]
        schoolMap[key] = temp

        key = nodedet["work_id"]
        if key in workMap:
          temp = workMap[key]
          temp.append(node)
        else:
          temp = [node]
        workMap[key] = temp
    
    if str(egoNode) in self.featuresMap:
      schoolList = schoolMap[self.featuresMap[str(egoNode)]["school_id"]]
      workList = workMap[self.featuresMap[str(egoNode)]["work_id"]]
      schoolList = schoolList + workList
      finalSet = set(schoolList)
      print("Total number of nodes in egonet " + egoNode +": " + str(len(nodegraph.nodes)))
      print("Total number of nodes with same school_id or workId as same as egonet " + egoNode + " : " + str(len(finalSet)))
      Percentage = float(len(finalSet))/float(len(nodegraph.nodes))
      print("Percentage of nodes in same social network: " + str(Percentage * 100))
   

  def languageSocial(self):
    languageMap = {}
    nodegraph = self.build_graphList('egonets/0.egonet')
    for node in nodegraph.nodes:
      key = str(node)
      language = self.featuresMap[key]["language"]
      if language in languageMap:
        temp = languageMap[self.featuresMap[key]["language"]]
        temp.append(key)
      else:
          temp = [key]
      languageMap[key] = temp
      newgraph = nx.Graph()
    for key in languageMap:
      a = languageMap[key][0]
      b = languageMap[key]
      for e in b:
        if e == a: continue
        newgraph.add_edge(int(a),int(e))
    pos= nx.spring_layout(newgraph)
    nx.draw(newgraph, pos, with_labels=True)
    plt.show()





social = socialNetwork()
social.makedata('features.txt', 'egonets/0.egonet')
newgraph = social.build_graphList('egonets/0.egonet')
print ("Number of nodes: " + str(nx.number_of_nodes(newgraph)))
print ("Number of edges: " + str(nx.number_of_edges(newgraph)))

print ("Betweenness Centrality: " + str(nx.betweenness_centrality(newgraph)))
print ("Clustering value: " + str(nx.average_clustering(newgraph)))  

print(" \n**** ------ Hypothesis 1 observation ------- ****")

social.hypothesis1('egonets/0.egonet')
print("\n")
social.hypothesis1('egonets/850.egonet')
print("\n")
social.hypothesis1('egonets/2255.egonet')

social.languageSocial()