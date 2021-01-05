import os


# Permet de parser le fichier d'entrer pour obtenir obtenir les infos du sujet
# Toutes les infos sont stockées dans la classe Room et Ant
def get_data(Room, Ant):
    # region Déclarations
    idx_file = input("Input for the index of the anthill (1, 2, 3 ..)")
    file = os.path.join("data", "anthill_" + idx_file + ".txt")
    data = open(file, "r").read().split("\n")
    last_room_index = sum(1 if "-" not in line else 0 for line in data)
    data = [word.lower().replace("sv", "s0").replace("sd", "s" + str(last_room_index)) for word in data]
    data = list(map(str.lower, data))
    nb_ant = int(data[0].split("=")[1])
    rooms = [Room(0, False, nb_ant, nb_ant), Room(last_room_index, is_last_room=True, nb_full=nb_ant)]
    # endregion

    # region Création des rooms et de leurs attributs nb_full
    for i, line_content in enumerate(data[1:last_room_index]):
        # region new Room
        index_room = int(''.join(c for c in line_content.split(" ")[0] if c.isdigit()))
        if "{" not in line_content:
            rooms.insert(len(rooms) - 1, Room(index_room))
        else:
            nb_full = int(''.join(c for c in line_content.split("{")[1] if c.isdigit()))
            rooms.insert(len(rooms) - 1, Room(index_room, False, nb_full))
    # endregion

    # region Assignations des chemins accessibles à partir d'une room
    for i, line_content in enumerate(data[last_room_index:]):
        line_content = line_content.strip().split("-")
        source_index = int(''.join(c for c in line_content[0] if c.isdigit()))
        destination_index = int(''.join(c for c in line_content[1] if c.isdigit()))

        for j in range(2):
            if j == 1:
                source_index, destination_index = destination_index, source_index
            current_room = next((room for room in rooms if room.index == source_index), None)
            current_room.append_destination(rooms[destination_index])
    # endregion

    Ant.nb_ants = nb_ant
    Room.rooms = rooms
