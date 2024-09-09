import json
import os

running = True

Debug = 0

Database = 'Database.json'
LiveDatabase = []

def DatabaseManipulate(Operation, DatabaseIndex, Data):
    global Database
    global LiveDatabase

    if Operation == "Save": # Saves Database
        with open(Database, 'w') as file:
            json.dump(LiveDatabase, file)
        
        if Debug == 1:
            print("\nDatabase Saved Successfully.")

    if Operation == "Load": # Loads Database
        if os.path.exists(Database):
            with open(Database, 'r') as file:
                try:
                    LiveDatabase = json.load(file)
                except:
                    if Debug == 1:
                        print("\nDatabase Load Error! Resetting.")
                    
                    LiveDatabase = [[0], [0, 0], [0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
                    
                    if Debug == 1:
                        print("Database Reset. Retrying Load.")
                    DatabaseManipulate("Save", 0, "Null")
                    #DatabaseManipulate("Load", 0, "Null")

            if Debug == 1:
                print("\nDatabase Loaded Successfully.")
        else:
            if Debug == 1:
                print("\nDatabase Loaded Unsuccessfully. Saving state.")
            DatabaseManipulate("Save", "Null")

    if Operation == "Update" and Data != "Null": # Updates Database
        ListLength = len(Data)
        if Debug == 1:
            print("List Length:", ListLength)

        DatabaseManipulate("Load", 0 ,"Null")
        if Debug == 1:
            print("\nDatabase Data (Pre):", DatabaseIndex)

        if Debug == 1:
            print("ListDatabaseIndex:", DatabaseIndex)

        for Index in range (ListLength):
            if Debug == 1:
                print("Index:", Index)
            
            LiveDatabase[DatabaseIndex][Index] = Data[Index]
            
        if Debug == 1:
            print("Database Data (Post):", LiveDatabase)

        DatabaseManipulate("Save", 0 ,"Null")
    
    if Operation == "Display": # Displays Database
        DatabaseManipulate("Load", 0 ,"Null")
        print("Database:", LiveDatabase)

def UI():
    global Debug
    
    Debug = 1

    while running == True:
        Operation = input("\n-\ Do you want to Save (S), Load (L), Display (D) or Update (U) the Database? ")

        if Operation == "S":
            DatabaseManipulate("Save", 0 ,"Null")

        if Operation == "L":
            DatabaseManipulate("Load", 0 ,"Null")
        
        if Operation == "D":
            DatabaseManipulate("Display", 0, "Null")

        if Operation == "U":
            DatabaseIndex = int(input("Enter Database Index: "))
            Data = eval(input("Enter Data (in list format): "))
            DatabaseManipulate("Update", DatabaseIndex, Data)

        

UI()