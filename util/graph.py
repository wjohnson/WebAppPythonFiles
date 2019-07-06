import re

def isBadTerm(term):
    isBad = False
    if term in ["stop","words","example"]:
        isBad = True
    if re.match("page *of",term):
        isBad = True
    return isBad

def node_edge_creation(list_of_lists, query):
    container = dict() # keyphrase: [links to other nodes]
    for block in list_of_lists:
        clean_block = [term.lower() for term in block if not isBadTerm(term)]
        for unit in clean_block:
            unit = unit.lower()
            if isBadTerm(unit):
                continue
            unit = unit
            _temp_dict = container.get(unit,[])
            _temp_dict.extend(clean_block)
            container[unit] = _temp_dict

    unit_count = dict()        
    for key in container:
        unit_count[key] = len([x for x in container[key] if x == key])

    sorted_list = sorted([(k,v) for k,v in unit_count.items()], key=(lambda x: x[1]), reverse = True)

    for k,_ in sorted_list[0:2]:
        container[k]

    top_two_edges = []
    from collections import Counter
    for unit, _ in sorted_list[0:2]:
        counted = Counter(container[unit])
        sorted_connections = [k for _,k in sorted(zip(list(counted.values()), list(counted.keys())))]
        sorted_connections.remove(unit)
        top_two_edges.append(sorted_connections[0:10])


    top_10 = [k for k,v in sorted_list][0:10]

    nodes = list(set(top_10 + top_two_edges[0]+ top_two_edges[1]))
    nodes.insert(0,query)
    nodes_dict = {val:i for i, val in enumerate(nodes)}

    nodes_output = [(idx, label) for label, idx in nodes_dict.items()]

    edges = [(query,n) for n in top_10]
    edges.extend([(top_10[0], n) for n in top_two_edges[0]])
    edges.extend([(top_10[1], n) for n in top_two_edges[1]])

    edges_output = [(nodes_dict[n], nodes_dict[e]) for n,e in edges]

    return nodes_output, edges_output