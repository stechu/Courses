#!/usr/bin/env python

'''
    Generate tree search dot file
'''
import copy

# Colors supported by graphviz, in some pleasing order
colors = {
    "fillA": "cyan",
    "fillB": "cyan",
    "emptyA": "blue",
    "emptyB": "blue",
    "pourA": "orange",
    "pourB": "orange"
}


def export_dot():
    print """digraph searchTree {
  size = "6,6";
  node [ shape=oval, style=filled, fillcolor=lightblue2 ] ;
"""
    (nodes, edges) = getGraph()
    for n in nodes:
        print "{} [label=\"{}\", color=black, penwidth=2];".format(
            n["id"], n["state"])
    for (x, y, action) in edges:
        print "{} -> {} [color={}]".format(
            x, y, colors[action])
    print "}"


def getGraph():
    tree = bfs()
    nodes = [v for k, v in tree.items()]
    edges = [(n["parent"], n["id"], n["action"]) for n in nodes
             if n["parent"] != -1]
    return (nodes, edges)


def bfs():
    initState = {
        "state": (0, 0),
        "cost": 0,
        "id": 0,
        "parent": -1,
        "action": "Nothing",
        "visited": set()
    }
    goal = 2
    queue = []
    queue.append(initState)
    capA = 7
    capB = 4
    curId = 1
    tree = dict()

    while queue:
        state = queue.pop(0)
        rstate = state["state"]
        #check if visited
        if (rstate == (0, 0) and curId != 1) or rstate == (capA, capB):
            continue
        if rstate in state["visited"]:
            #tree[state["id"]] = state
            continue

        if rstate[0] == goal or rstate[1] == goal:
            tree[state["id"]] = state
            break
        else:
            tree[state["id"]] = state
            state["visited"].add(rstate)
            # fill A
            fillA = {
                "state": (capA, rstate[1]),
                "cost": state["cost"] + capA - rstate[0],
                "id": curId,
                "parent": state["id"],
                "action": "fillA",
                "visited": copy.deepcopy(state["visited"])
            }
            curId += 1
            if rstate[0] != capA:
                queue.append(fillA)
            # fill B
            fillB = {
                "state": (rstate[0], capB),
                "cost": state["cost"] + capB - rstate[1],
                "id": curId,
                "parent": state["id"],
                "action": "fillB",
                "visited": copy.deepcopy(state["visited"])
            }
            curId += 1
            if rstate[1] != capB:
                queue.append(fillB)
            # empty A
            emptyA = {
                "state": (0, rstate[1]),
                "cost": state["cost"],
                "id": curId,
                "parent": state["id"],
                "action": "emptyA",
                "visited": copy.deepcopy(state["visited"])
            }
            curId += 1
            if rstate[0] > 0:
                queue.append(emptyA)
            # empty B
            emptyB = {
                "state": (rstate[0], 0),
                "cost": state["cost"],
                "id": curId,
                "parent": state["id"],
                "action": "emptyB",
                "visited": copy.deepcopy(state["visited"])
            }
            curId += 1
            if rstate[1] > 0:
                queue.append(emptyB)
            # pour A to B
            pourA = {
                "state": (lambda x, y: (x + y - capB, capB)
                          if x + y > capB else (0, x + y))
                         (rstate[0], rstate[1]),
                "cost": state["cost"],
                "id": curId,
                "parent": state["id"],
                "action": "pourA",
                "visited": copy.deepcopy(state["visited"])
            }
            curId += 1
            if rstate[0] > 0 and rstate[1] != capB:
                queue.append(pourA)
            # pour B to A
            pourB = {
                "state": (lambda x, y: (capA, x + y - capA)
                          if x + y > capA else (x + y, 0))
                         (rstate[0], rstate[1]),
                "cost": state["cost"],
                "id": curId,
                "parent": state["id"],
                "action": "pourB",
                "visited": copy.deepcopy(state["visited"])
            }
            curId += 1
            if rstate[1] > 0 and rstate[0] != capA:
                queue.append(pourB)

    return tree


def main():
    export_dot()

if __name__ == '__main__':
    main()
