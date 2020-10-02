import itertools as itr
import heapq as hq
from heapq import heappush, heappop
from itertools import count
import networkx as nx


def extraer_pesos(G, weight):
    if callable(weight):
        return weight

    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)




def para_un_vertice(G, inicio, final=None, limite=None, atributo="weight"):
    return varios_vertices(
        G, {inicio}, limite=limite, final=final, peso=atributo
    )


def varios_vertices(G, iniciales, final=None, limite=None, peso="weight"):
    if not iniciales:
        raise ValueError("El grafo esta vacio")

    if final in iniciales:
        return (0, [final])
    peso = extraer_pesos(G, peso)
    camino = {inicio: [inicio] for inicio in iniciales}
    distancia = _dijkstra_multisource(
        G, iniciales, peso, caminos=camino, limite=limite, final=final
    )
    if final is None:
        return (distancia, camino)
    try:
        return (distancia[final], camino[final])
    except KeyError as e:
        raise nx.NetworkXNoPath(f"No path to {final}.") from e


def _dijkstra_multisource(
        G, iniciales, pesos, pred=None, caminos=None, limite=None, final=None
):
    G_succ = G._succ if G.is_directed() else G._adj

    push = heappush
    pop = heappop
    distancia = {}
    visitado = {}



    #Sirve para evitar comparciones dobles entre dos vertices, a causa de un vertice ya visitado
    c = count()
    # Tripleta con valores (distancia, c, vertice)
    valores_x_vertice = []
    for vertice_inicial in iniciales:
        if vertice_inicial not in G:
            raise nx.NodeNotFound(f"El vertice origen {vertice_inicial}no es parte del grafo")
        visitado[vertice_inicial] = 0
        push(valores_x_vertice, (0, next(c), vertice_inicial))
    while valores_x_vertice:
        (dist, contador, verti) = pop(valores_x_vertice)
        if verti in distancia:
            continue
        distancia[verti] = dist
        if verti == final:
            break
        for u, e in G_succ[verti].items():
            cost = pesos(verti, u, e)
            if cost is None:
                continue
            vu_dist = distancia[verti] + cost
            if limite is not None:
                if vu_dist > limite:
                    continue
            if u in distancia:
                u_dist = distancia[u]
                if vu_dist < u_dist:
                    raise ValueError("Camino incorrecto:", "pesos negativos invalidos")
                elif pred is not None and vu_dist == u_dist:
                    pred[u].append(verti)
            elif u not in visitado or vu_dist < visitado[u]:
                visitado[u] = vu_dist
                push(valores_x_vertice, (vu_dist, next(c), u))
                if caminos is not None:
                    caminos[u] = caminos[verti] + [u]
                if pred is not None:
                    pred[u] = [verti]
            elif vu_dist == visitado[u]:
                if pred is not None:
                    pred[u].append(verti)

    return distancia

def a_start(G, nodo_inicial, nodo_final):
    if nodo_inicial not in G or nodo_final not in G:
        msg = f"El nodo inicial {nodo_inicial} o el nodo final {nodo_final} no se encuentran en G"

    peso = 1
    push = hq.heappush
    pop = hq.heappop
    contar = itr.count()
    cola = [(0, next(contar), nodo_inicial, 0, None)]
    en_cola = {}
    explorados = {}
    while cola:
        _, __, actual, dist, padre = pop(cola)

        if actual == nodo_final:
            camino = [actual]
            nodo = padre
            while nodo is not None:
                camino.append(nodo)
                nodo = explorados[nodo]
            camino.reverse()
            return camino

        if actual in explorados:
            if explorados[actual] is None:
                continue
            qcosto, h = en_cola[actual]
            if qcosto < dist:
                continue

        explorados[actual] = padre

        for vecino, w in G[actual].items():
            ncosto = dist + 1
            if vecino in en_cola:
                qcosto, h = en_cola[vecino]
                if qcosto <= ncosto:
                    continue
            else:
                h = 0
            en_cola[vecino] = ncosto, h
            push(cola, (ncosto + h, next(contar), vecino, ncosto, actual))

    print("No existe camino entre el nodo inicial y el nodo final")


# El atributo de las aristas sera por defecto weight
def dijkstra(G, inicio, final, atributo="weight"):
    def func(u, v, d):
        node_u_wt = G.nodes[u].get("node_weight", 1)
        node_v_wt = G.nodes[v].get("node_weight", 1)
        edge_wt = d.get("weight", 1)
        return node_u_wt / 2 + node_v_wt / 2 + edge_wt

    (distancia_total, camino) = para_un_vertice(G, inicio, final=final, atributo=atributo)
    return camino


