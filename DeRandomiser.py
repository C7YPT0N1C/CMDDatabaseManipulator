import random
import time
import json
import os
import sys

Debug = 0

GenerationList = []
TestList = []

# 1 = Live, 2 = Blank
VerificationList = [1, 1, 2, 1, 1, 1, 2, 2]
VerificationFile = 'VerificationList.json'

TestAccuracy = 0
OverallAccuracy = 0

def SaveVerificationList():
    with open(VerificationFile, 'w') as file:
        json.dump(VerificationList, file)

def LoadVerificationList():
    global VerificationList
    if os.path.exists(VerificationFile):
        with open(VerificationFile, 'r') as file:
            VerificationList = json.load(file)
    else:
        SaveVerificationList()

def GenerateList(Count):
    global GenerationList
    
    GenerationList = []

    for Index in range(Count):
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

def StartRun(RunCount, IndexCount):
    global TestList
    global TestAccuracy
    
    LoadVerificationList()

    print("Calculating...")

    RunStartTime = time.time()

    TestList = []

    RunAccuracy = 0

    ######################
    
    for Run in range(RunCount):
        GenerateList(IndexCount)
        UpdateComparisonList()
        
        # Update the progress in place
        sys.stdout.write(f"\rPROGRESS: {((Run + 1) / RunCount) * 100:.2f}%")
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
    print("\nCurrent Run Calculation Time:", RunEndTime - RunStartTime, "seconds.")

    TestAccuracy = ((RunAccuracy / IndexCount) * 100)
    print("Current Run Accuracy:", TestAccuracy, "%")

    SaveVerificationList()

def StartTest(ActivateDebug, TestNum, RunCount, IndexCount):
    global Debug

    global TestList

    global TestAccuracy
    global OverallAccuracy

    if ActivateDebug == True:
        Debug = 1
    else:
        Debug = 0

    TestStartTime = time.time()

    for Test in range(TestNum):
        print("\nTEST:", (Test + 1)) # Print Test Loop Number

        StartRun(RunCount, IndexCount)

        if Test == 0:
            OverallAccuracy = TestAccuracy
        else:
            OverallAccuracy = ((OverallAccuracy + TestAccuracy) / 2)
    
    TestEndTime = time.time()
    print("\nOVERALL CALCULATION TIME:", TestEndTime - TestStartTime, "seconds.")
    print("OVERALL ACCURACY:", OverallAccuracy, "%")

StartTest(False, 5, 1000, 8)