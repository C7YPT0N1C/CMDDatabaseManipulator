import random
import time
import json
import os
import sys

Debug = 0

GenerationList = []
TestList = []

# 0 = Null, 1 = Live, 2 = Blank
#VerificationList = [1, 1, 2, 1, 1, 1, 2, 2]
VerificationList = []
VerificationFile = 'VerificationList.json'

TestAccuracy = 0
OverallAccuracy = 0

def SaveVerificationList(): # Saves VerificationList
    with open(VerificationFile, 'w') as file:
        json.dump(VerificationList, file)

def LoadVerificationList(): # Loads VerificationList
    global VerificationList
    if os.path.exists(VerificationFile):
        with open(VerificationFile, 'r') as file:
            VerificationList = json.load(file)
    else:
        SaveVerificationList()

def GenerateList(IndexCount):
    global GenerationList
    
    GenerationList = []

    for Index in range(IndexCount):
        Random = random.randint(1, 2)
    
        if Random == 1:
            GenerationList.append(1)
            
        if Random == 2:
            GenerationList.append(2)
    
    if Debug == 1:
        print("\nGeneration List = ", GenerationList)

def UpdateComparisonList():
    for Index in range(len(GenerationList)):
        VerificationList[Index] = ((VerificationList[Index] + GenerationList[Index]) / 2)
    
    if Debug == 1:
        print("Comparison List = ", VerificationList)

def StartStages(StageCount, IndexCount):
    global TestList
    global TestAccuracy

    print("Calculating...")

    RunStartTime = time.time()

    TestList = []

    RunAccuracy = 0

    ######################
    
    for Run in range(StageCount):
        LoadVerificationList()
        
        GenerateList(IndexCount)
        UpdateComparisonList()

        SaveVerificationList()
        
        # Update the progress in place
        sys.stdout.write(f"\rPROGRESS: {((Run + 1) / StageCount) * 100:.2f}%")
        sys.stdout.flush()

    ######################

    print("\nGeneration complete.")

    for Index in range(IndexCount):
        Random = random.randint(1, 2)
    
        if Random == 1:
            TestList.append(1)
            
        if Random == 2:
            TestList.append(2)
    
    print("\nVerification Test List = ", TestList)
    print("Verification List = ", VerificationList, "\n")

    for Index in range(len(TestList)):
        if TestList[Index] - VerificationList[Index] <= 0.5:
            print("Verification List Index", Index, "= TRUE")
            RunAccuracy = RunAccuracy + 1
        else:
            print("Verification List Index", Index, "= FALSE")
    
    RunEndTime = time.time()
    print("\nStage Calculation Time:", RunEndTime - RunStartTime, "seconds.")

    TestAccuracy = ((RunAccuracy / IndexCount) * 100)
    print("Stage Accuracy:", TestAccuracy, "%")

#######################################################################################################

def StartTest(StageNum, StageCount, IndexCount):
    global Debug

    global TestList
    global VerificationList

    global TestAccuracy
    global OverallAccuracy

    LoadVerificationList()

    if VerificationList == []: # Makes sure that the saved VerificationList isn't empty.
        print("Verification List Empty!")
        
        for Index in range (IndexCount):
            VerificationList.append(0)
        
        print("Verification List:", VerificationList)
        
        SaveVerificationList()
        LoadVerificationList()
    
    if len(VerificationList) != IndexCount: # Makes sure that the length of VerificationList is equal to IndexCount.
        print("Verification List Not Correct Size! Correcting.")
        
        #for Index in range (len(VerificationList) - IndexCount):
        #    VerificationList.append(0)

        VerificationList = []
        for Index in range (IndexCount):
            VerificationList.append(0)

        
        print("Verification List:", VerificationList)
        
        SaveVerificationList()
        LoadVerificationList()
    
    #if len(VerificationList) != (IndexCount):
    #    for Index in range(IndexCount - len(VerificationList)):
    #        VerificationList.append(0)

    print("\nInital Verification List = ", VerificationList)

    TestStartTime = time.time()

    for Stage in range(StageNum):
        print("\nSTAGE:", (Stage + 1)) # Print Test Loop Number

        #LoadVerificationList()

        StartStages(StageCount, IndexCount)

        if Stage == 0:
            OverallAccuracy = TestAccuracy
        else:
            OverallAccuracy = ((OverallAccuracy + TestAccuracy) / 2)

        #SaveVerificationList()
    
    TestEndTime = time.time()
    print("\nOVERALL TEST CALCULATION TIME:", TestEndTime - TestStartTime, "seconds.")
    print("TEST OVERALL ACCURACY:", OverallAccuracy, "%")

def Main():
    StageNumber = int(input("- How many stages?: "))
    StageCount = int(input("- How many loops per stage?: "))
    IndexLength = int(input("- How many indexes?: "))
    StartTest(StageNumber, StageCount, IndexLength)

Main()