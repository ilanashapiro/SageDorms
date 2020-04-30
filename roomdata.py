roomsList = [[]]

with open("room_data.txt", "r") as rooms:
    line_num = 1
    roomNum = -1
    count = 0
    bathroom = False
    other = False
    for line in rooms:
        line_tag = line.split(":")

        if len(line_tag) == 1:
            if (other and not bathroom):
                roomsList[roomNum].insert(-1, "")
            line_num = 1
            roomNum += 1
            other = False
            bathroom = False
            roomsList.append([])

        if line_num == 1:
            room_name = line.split(" ")
            dorm_name = room_name[0]
            room_number = room_name[1]
            roomsList[roomNum].append(dorm_name.rstrip())
            roomsList[roomNum].append(room_number.replace("\n", "").rstrip())

        elif line_num == 2:
            dim = line.split("-")
            dimensions = dim[0])
            sq_ft = dim[1].strip().split(" ")
            area = int(sq_ft[0])
            roomsList[roomNum].append(dimensions.rstrip().replace('\'', 'ft').replace('"', 'in'))
            roomsList[roomNum].append(area)

        else:
            roomsList[roomNum].append(line.replace("\xa0", " ").replace("\n","").replace('\'', "ft").replace('"', "in").rstrip())
            if "Bath:" in line:
                bathroom = True
            if "Other:" in line:
                other = True

        line_num += 1
        count+=1

outputFile = open("rooms.txt", "w") #create output file, name is from command line args
for room in roomsList:
    outputFile.write("$".join(map(str, room)) + "\n") # set $ as delimeter
outputFile.close() #close output file
