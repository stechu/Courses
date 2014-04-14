#!/usr/bin/env python

'''
    Generate tree search dot file
'''
import copy

# Colors supported by graphviz, in some pleasing order
colors = {
    "fa": "brown",
    "fb": "brown1",
    "ea": "cadetblue",
    "eb": "cadetblue1",
    "pa": "orange",
    "pb": "orange4"
}

curId = 1
capAset = 4
capBset = 7
goal = 2


def export_dot():
    # helper functions
    def getColor(node):
        (a, b) = node["state"]
        if a == goal or b == goal:
            return "red"
        return "black"

    def getLabel(node):
        if node["leaf"]:
            return "{} \n cost:{}".format(node["state"], node["cost"])
        else:
            return node["state"]

    print """digraph searchTree {
  size = "8,8";
  node [ shape=oval, style=filled, fillcolor=lightblue2 ] ;
  edge [fontname="Helvetica"];
  splines=curved;
"""
    (nodes, edges) = getGraph()
    for n in nodes:
        print "{} [label=\"{}\", color={}, penwidth=2];".format(
            n["id"], getLabel(n), getColor(n))
    for (x, y, action) in edges:
        print "{} -> {} [xlabel=\"{}\",color={}]".format(
            x, y, action, colors[action])
    print "}"


def getGraph():
    tree = bfs(capAset, capBset, goal)
    nodes = [v for k, v in tree.items()]
    edges = [(n["parent"], n["id"], n["action"]) for n in nodes
             if n["parent"] != -1]
    hasChild = set()
    for node in nodes:
        hasChild.add(node["parent"])
    for node in nodes:
        if node["id"] in hasChild:
            node["leaf"] = False
        else:
            node["leaf"] = True
    return (nodes, edges)


def bfs(capA, capB, goal):
    #helper functions
    def fillA(state):
        (a, b) = state["state"]
        global curId
        curId += 1
        ans = {
            "state": (capA, b),
            "cost": state["cost"] + capA - a,
            "id": curId,
            "parent": state["id"],
            "action": "fa",
            "visited": copy.deepcopy(state["visited"])
        }
        return ans

    def fillB(state):
        (a, b) = state["state"]
        global curId
        curId += 1
        ans = {
            "state": (a, capB),
            "cost": state["cost"] + capB - b,
            "id": curId,
            "parent": state["id"],
            "action": "fb",
            "visited": copy.deepcopy(state["visited"])
        }
        return ans

    def emptyA(state):
        (a, b) = state["state"]
        global curId
        curId += 1
        ans = {
            "state": (0, b),
            "cost": state["cost"],
            "id": curId,
            "parent": state["id"],
            "action": "ea",
            "visited": copy.deepcopy(state["visited"])
        }
        return ans

    def emptyB(state):
        (a, b) = state["state"]
        global curId
        curId += 1
        ans = {
            "state": (a, 0),
            "cost": state["cost"],
            "id": curId,
            "parent": state["id"],
            "action": "eb",
            "visited": copy.deepcopy(state["visited"])
        }
        return ans

    def pourA(state):
        (a, b) = state["state"]
        global curId
        curId += 1
        ans = {
            "state": (lambda x, y: (x + y - capB, capB)
                      if x + y > capB else (0, x + y))
                     (a, b),
            "cost": state["cost"],
            "id": curId,
            "parent": state["id"],
            "action": "pa",
            "visited": copy.deepcopy(state["visited"])
        }
        return ans

    def pourB(state):
        (a, b) = state["state"]
        global curId
        curId += 1
        ans = {
            "state": (lambda x, y: (capA, x + y - capA)
                      if x + y > capA else (x + y, 0))
            (a, b),
            "cost": state["cost"],
            "id": curId,
            "parent": state["id"],
            "action": "pb",
            "visited": copy.deepcopy(state["visited"])
        }
        return ans

    initState = {
        "state": (0, 0),
        "cost": 0,
        "id": 0,
        "parent": -1,
        "action": "Nothing",
        "visited": set()
    }
    queue = []
    queue.append(initState)
    tree = dict()

    while queue:
        state = queue.pop(0)
        (a, b) = state["state"]
        #check if visited
        if ((a, b) == (0, 0) and curId != 1) or (a, b) == (capA, capB):
            continue
        if (a, b) in state["visited"]:
            #tree[state["id"]] = state
            continue

        if a == goal or b == goal:
            tree[state["id"]] = state
            break
        else:
            tree[state["id"]] = state
            state["visited"].add((a, b))
            # fill A
            if a != capA:
                queue.append(fillA(state))
            # fill B
            if b != capB:
                queue.append(fillB(state))
            # empty A
            if a > 0:
                queue.append(emptyA(state))
            # empty B
            if b > 0:
                queue.append(emptyB(state))
            # pour A to B
            if a > 0 and b != capB:
                queue.append(pourA(state))
            # pour B to A
            if b > 0 and a != capA:
                queue.append(pourB(state))

    return tree


def main():
    export_dot()

if __name__ == '__main__':
    main()
