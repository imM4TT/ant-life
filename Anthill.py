from Graph import Graph
from FileManager import get_data


# Classe Room qui contient toutes les rooms existantes ansi que les différents chemins possibles et le nombre de fourmis
class Room:
    rooms = []
    last_room_index = 0

    def __init__(self, index, is_last_room=False, nb_full=1, nb_current=0, is_dead_end=False,
                 is_full=False):
        self.dest_rooms = []
        self.index = index
        self.is_last_room = is_last_room
        self.nb_full = nb_full
        self.nb_current = nb_current
        self.is_full = is_full
        self.is_dead_end = is_dead_end
        self.distances = {}

    def append_destination(self, dest):
        self.dest_rooms.append(dest)

    def append_ant(self):
        self.nb_current += 1

    def remove_ant(self):
        self.nb_current -= 1

    def check_for_full(self):
        self.is_full = (self.nb_current == self.nb_full)

    # Calcul des distances entre l'arrivé et un noeud
    # On part de la derniere salle: on ajoute dans un dictionnaire au fur et a mesure la distance de la salle suivante
    # On évite les distances dupliquées et on fait en sorte que ce soit la/les disances les plus courte
    @staticmethod
    def set_distance():
        rooms = [Room.rooms[-1]]
        while len(rooms):
            current_room = rooms.pop()
            for i, next_room in enumerate(current_room.dest_rooms):
                if current_room.is_last_room:
                    current_distance = next_distance = 0
                    is_empty = True
                else:
                    current_distance = min(current_room.distances.values())[0]
                    next_distance = min(next_room.distances.values())[0] if len(next_room.distances) > 0 else 0
                    is_empty = next_room.distances == {}
                if next_room.is_last_room or (next_distance < current_distance + 1 and not is_empty):
                    # la distance qui est déjà dans le tableau est plus petite que cette distance:
                    # cette distance correspond à un chemin plus long donc on passe
                    continue
                if current_room.index in next_room.distances:
                    if 1 + current_distance < next_room.distances[current_room.index][0]:
                        # on remplace la distance par une autre distance plus courte qui correspondra à la distance
                        # d'un meilleur chemin
                        next_room.distances[current_room.index] = [1 + current_distance]
                else:
                    next_room.distances[current_room.index] = [1 + current_distance]
                rooms.append(next_room)

    # region Debug
    def __str__(self):
        return "\nRoom n°" + str(self.index) + \
               "\n Distance de l'arrivé -> " + str(self.distances) + \
               "\n  Destinations -> " + str(list(map(lambda room: room.index, self.dest_rooms))) + \
               "\n   Nb. max de fourmis -> " + str(self.nb_full) + \
               "\n    Nb. de fourmis -> " + str(self.nb_current) + \
               "\n     Is Full ? -> " + str(self.is_full) + \
               "\n      Is Dead End ? -> " + str(self.is_dead_end)

    @staticmethod
    def print_all_rooms():
        for room in Room.rooms:
            print(room)
    # endregion


# Classe Ant qui contient toutes les fourmies avec leurs positions et autres attributs
class Ant:
    ants = []
    nb_ants = 0

    def __init__(self, id):
        self.id = id
        self.index = 0
        self.has_reach_dest = False
        self.known_index = [0]

    def set_position(self, new_pos):
        self.index = new_pos

    def move(self):
        current_room = Room.rooms[self.index]
        dest_rooms = Room.rooms[self.index].dest_rooms
        for i, dest_room in enumerate(sorted(dest_rooms, key=lambda x: x.index, reverse=True)):
            if dest_room.index in self.known_index or dest_room.is_dead_end:
                continue
            if not dest_room.is_full:
                # region Add/Remove ant from room and set known index
                current_room.remove_ant()
                dest_room.append_ant()
                current_room.check_for_full()
                dest_room.check_for_full()
                self.known_index.append(self.index)
                # endregion
                self.index = dest_room.index
                # region Check end for this ant
                if dest_room.is_last_room:
                    self.has_reach_dest = True
                # endregion

                # return for Logs
                return [current_room.index, dest_room.index]

        return None

    # region Debug
    def __str__(self):
        return "\nFourmi n°" + str(self.id) + ":\n Position -> " + str(self.index) + \
               ":\n Arrivée ? -> " + str(self.has_reach_dest)

    @staticmethod
    def print_all_ants():
        for ant in Ant.ants:
            print(ant)
    # endregion


# Class mère qui gère l'avancement du programme
class AnthillManager:

    def __init__(self):
        self.run = True
        self.create_anthill()
        self.clean_anthill()
        self.graph = Graph(Room.rooms)
        self.main()

    def check_for_end(self):
        if all(ant.has_reach_dest for ant in Ant.ants):
            self.run = False

    def create_anthill(self):
        get_data(Room, Ant)
        Room.set_distance()
        self.create_ants()

    def main(self):
        nb_etape = 0
        self.graph.draw_next(Ant.ants)
        while self.run:
            turn = self.new_turn()
            self.debug_new_turn(nb_etape, turn)
            self.check_for_end()
            nb_etape += 1
            self.graph.draw_next(Ant.ants)

    @staticmethod
    def new_turn():
        moves = []
        for i, ant in enumerate(Ant.ants):
            if not ant.has_reach_dest:
                new_move = ant.move()
                if new_move is not None:
                    moves.append([i + 1, new_move[0], new_move[1]])
        return moves

    @staticmethod
    def create_ants():
        ants = []
        for i in range(Ant.nb_ants):
            ants.append(Ant(i + 1))
        Ant.ants = ants

    @staticmethod
    def clean_anthill():
        rooms = Room.rooms
        index_impasse = []
        # region Get dead_end index
        for i, room in enumerate(rooms):
            if len(room.dest_rooms) == 1 and room.index != 0 and not room.is_last_room:
                index_impasse.append(i)
                next_room = rooms[i].dest_rooms[0]
                while next_room is not None:
                    if len(next_room.dest_rooms) >= 3:
                        next_room = None
                    else:
                        index_impasse.append(next_room.index)
                        next_room = next_room.dest_rooms[0]
        # endregion
        # region Set dead_end room
        for index in index_impasse:
            rooms[index].is_dead_end = True
        # end region

    @staticmethod
    def debug_new_turn(nb_etape, turn):
        print("\n    --- E" + str(nb_etape) + " ---")
        for move in turn:
            move = list(map(str, move))
            print("Fourmi n°" + move[0] + ": " + move[1] + " --> " + move[2])


AnthillManager()
