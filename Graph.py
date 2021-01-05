import networkx as nx
import matplotlib.pyplot as plt


# Classe utilisée pour créer des graphs en fonction des objets Room et Ant
class Graph:

    def __init__(self, rooms):
        self.g = None
        self.pos = {}
        self.labels = None
        self.setup_graph(rooms)

    def setup_graph(self, rooms):
        plt.axis("off")
        self.g = nx.Graph()
        # region Création: Nodes, Edges
        for i, room in enumerate(rooms):
            self.g.add_node(room.index)
            # region Déclaration des edges et de leurs valeurs respectives
            # Il peut arriver qu'un noeud ait différentes distances pour ses différentes destination
            # Le calcul de distance est effectué au préalable et il faut maintenant assigner les distances aux edges
            edges = list(map(lambda x: x.index, room.dest_rooms))
            for index_dest in edges:
                distance = min(room.distances[index_dest]) if index_dest in room.distances else 10 ** 5
                if i in rooms[index_dest].distances:
                    d = min(rooms[index_dest].distances[i])
                    if d < distance:
                        distance = d
                if self.g.has_edge(i, index_dest) and self.g.get_edge_data(i, index_dest)["weight"] > distance:
                    # on conserve la distance la plus faible
                    continue
                self.g.add_edge(room.index, index_dest, weight=distance)
            # endregion
        # endregion
        # region Assignations: Positions des noeuds et des labels
        pos_dict = nx.spring_layout(self.g, k=.5, seed=77)
        for key in sorted(pos_dict):
            self.pos[key] = pos_dict[key]

        self.labels = nx.get_edge_attributes(self.g, 'weight')
        # endregion

    def draw_next(self, ants):
        plt.axis("off")
        nx.draw_networkx(self.g, self.pos, node_size=650, style="dotted", font_size=10, font_color="orange",
                         node_color="black", font_weight="bold")
        nx.draw_networkx_edge_labels(self.g, self.pos, font_color="black", font_size=8, edge_labels=self.labels)
        index = [0 for _ in range(len(self.pos))]
        for i, ant in enumerate(ants):
            index[ant.index] += 1
        for i, pos in enumerate(self.pos.values()):
            plt.text(round(pos[0], 3) + .01, round(pos[1], 3) + .01, str(index[i]), color="red", fontsize=10,
                     fontweight="bold")

        plt.plot([], [], '', label="Numéro de salle", color="white")
        plt.plot([], [], '', label="Nombre de fourmis", color="white")
        plt.plot([], [], '', label="Distance de l'arrivée", color="white")

        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=1, mode="expand", borderaxespad=0.)
        legend = plt.legend()
        plt.setp(legend.get_texts()[0], color="orange")
        plt.setp(legend.get_texts()[1], color="red")
        plt.setp(legend.get_texts()[2], color="black")
        legend.get_frame().set_linewidth(0.0)
        plt.show()
