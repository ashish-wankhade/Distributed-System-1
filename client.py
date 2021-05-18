import socket
import os

PORT = 8010
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
ADDRESS = client.getsockname()[1]

while True:
    while True:
        message = input("For File Transfer Press 1\n"
                        "For Disconnecting Press 2\n"
                        "Enter Opertion - ")
        if message == '1' or message == '2':
            client.send(str(message).encode(FORMAT))
            break
        else:
            print("PLEASE ENTER '1' OR '2' ONLY")

    if int(message) == 2:
        print("DISCONNECTING...")
        break

    if int(message) == 1:
        filename = input("Enter Filename with EXTENSION - ")
        client.send(str(filename).encode(FORMAT))

        cwd = os.getcwd()
        listDir = os.listdir()
        newDir = str(cwd + "\\" + str(ADDRESS))

        if str(ADDRESS) not in listDir:
            os.mkdir(newDir)

        os.chdir(newDir)
        listClient = os.listdir()

        FileExist = str(str(ADDRESS) + "--" + filename)
        #ServerFolderExistorNot = client.recv(HEADER).decode(FORMAT)
        if FileExist not in listClient:
            action = "SEND FILE"
            client.send((action).encode())
            revievingFile = client.recv(HEADER).decode(FORMAT)
            if revievingFile == "SERVER IS SENDING FILE...":
                print(revievingFile)
                with open(f"{ADDRESS}--{filename}", 'wb') as fw:
                    data = client.recv(HEADER * 5)
                    if not data:
                        break
                    fw.write(data)
                fw.close()
                print("RECIEVED FILE...")
            else:
                print(f"FILE NAMED - {filename} DOES NOT EXISTS INSIDE SERVER FOLDER!")
        else:
            action = f"FILE NAMED - {filename} ALREADY EXISTS WITH CLIENT!!!"
            client.send((action).encode())
            print(action)
        os.chdir(cwd)
