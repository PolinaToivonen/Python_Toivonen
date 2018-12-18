import igraph
import time
from api import get_friends
from igraph import Graph, plot
from config import VK_CONFIG


def get_network(users_ids, as_edgelist=True) -> list:
    graph = []
    matrix = [[0 for i in range(len(users_ids))] for j in range(len(users_ids))]

    for user1 in range(len(users_ids)):
        response = get_friends(users_ids[user1])
        friends_list = response
        for user2 in range(user1 + 1, len(users_ids)):
            if users_ids[user2] in friends_list:
                if as_edgelist:
                    graph.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.4)
        print("loading...")

    if as_edgelist:
        return graph
    else:
        return matrix


def plot_graph(graph):
    friends = get_friends(57902269)
    vertices = [i for i in range(len(friends))]  # количество вершин
    edges = graph  # ребра графа

    # Создание графа
    g = Graph(vertex_attrs={"label": vertices, "shape": "circle", "size": 10},
              edges=edges, directed=False)

    # Задаем стиль отображения графа
    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=1000,
            area=n ** 3,
            repulserad=n ** 3)
    }

    # Удаляем петли и повторяющиеся ребра
    g.simplify(multiple=True, loops=True)

    # Разделяем вершины на группы по взаимосвязям
    clusters = g.community_multilevel()
    print(clusters)

    # Раскрашиваем разные группы вершин в разные цвета
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # Отрисовываем граф
    plot(g, **visual_style)


if __name__ == '__main__':
    user_id = VK_CONFIG['user_id']
    response = get_friends(user_id)
    graph = get_network(response, as_edgelist=True)
    plot_graph(graph)
    
