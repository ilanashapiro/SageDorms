dorm_name = []
room_number = []
dimensions = []
area = []
closet_type = []
window_type = []

roomsList = [[]]

with open("room_data.txt", "r") as rooms:
    line_num = 1
    roomNum = -1
    count = 0
    for line in rooms:
        line_tag = line.split(":")

        #if line_tag[0] == "Windows" or line_tag[0] == "Other" or line_tag[0] == "Bath":
        #    line_num = 0
        if len(line_tag) == 1:
            line_num = 1
            roomNum += 1
            roomsList.append([])
        if line_num == 1:
            room_name = line.split(" ")
            dorm_name.append(room_name[0])
            room_number.append(room_name[1])

            roomsList[roomNum].append(room_name[0].rstrip())
            roomsList[roomNum].append(room_name[1].replace("\n", "").rstrip())
        elif line_num == 2:
            dim = line.split("-")
            dimensions.append(dim[0])
            sq_ft = dim[1].strip().split(" ")
            area.append(int(sq_ft[0]))

            roomsList[roomNum].append(dim[0].rstrip())
            roomsList[roomNum].append(int(sq_ft[0]))
        else:
            roomsList[roomNum].append(line.replace("\xa0", " ").replace("\n","").rstrip())
        # elif line_num == 3:
        #     closet_type.append(line)
        #
        #     roomsList[roomNum].append(line)
        # elif line_num == 4:
        #     window_type.append(line)
        #
        #     roomsList[roomNum].append(line)
        #
        line_num += 1
        count+=1
        # print("count " + str(count))

outputFile = open("rooms.txt", "w") #create output file, name is from command line args
for room in roomsList:
    outputFile.write("$".join(map(str, room)) + "\n") #write number of blocks as first line of output
outputFile.close() #close output file

# print(len(dorm_name))
# print(len(room_number))
# print(len(dimensions))
# print(len(area))
# print(len(closet_type))
# print(len(window_type))
