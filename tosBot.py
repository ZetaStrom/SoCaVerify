import json
import requests
from bs4 import BeautifulSoup

localCheckFile = "def"

def writeJSfile(newFileName,objToDump):
    with open(newFileName, "w") as outfile:
        json.dump(objToDump, outfile)

def openCheckFile(checkFileLoc):
    f = open(checkFileLoc)
    data = json.load(f)
    f.close()
    return data

def parseChumba(checkFile="def"):  
    if checkFile=="def":   
        print("No Check file linked, please provide the file location of the check file.")
        return
    r = requests.get("https://www.chumbacasino.com/sweeps-rules")
    soup = BeautifulSoup(r.content, 'html5lib')
    txtBlocks = soup.find_all('p')
    if len(txtBlocks)>0:
        print("Found today's Chumba TOS!")
        #print(f"Found {len(txtBlocks)} paragraphs")
    else:
        print("Failed to find page")
    chumbaInfo={
                "version":txtBlocks[0].get_text(),
                "LastChumbaUpdate":txtBlocks[1].get_text(),
                "disclaimer":txtBlocks[2].get_text(), 
                "1stP":txtBlocks[3].get_text(),
                "2ndP":txtBlocks[4].get_text(),
                "3rdP":txtBlocks[5].get_text(),
                "4thP":txtBlocks[6].get_text(),
                "5thP":txtBlocks[7].get_text(),
                "6thP":txtBlocks[8].get_text(),
                "7thP":txtBlocks[9].get_text(),
                "8thP":txtBlocks[10].get_text(),
                "9thP":txtBlocks[11].get_text(),
                "10thP":txtBlocks[12].get_text(),
                "LastUpdated":"8/26/2023"
                }
    if checkFile!="none":
        print("Checking known TOS file...")
        knownTOS = openCheckFile(checkFile)
        cmnKeys = chumbaInfo.keys()
        isSame=True
        differences={}
        for key in cmnKeys:
            if knownTOS[key]!=chumbaInfo[key]:
                #print(f"Difference in TOS at location {key}")
                differences[key]=chumbaInfo[key]
                isSame=False
        if isSame:
            print("=== No changes found to Chumba TOS! ===")
        else:
            print("=== Differences Detected in Chumba TOS! ===")
            print(differences)
            print("...")
            print("Saving new TOS...")
            writeJSfile("newChumbaTOS_",chumbaInfo)
            print("Please update the LastUpdated part of the new TOS file with todays date")
        
    else:
        print("Saving new TOS...")
        writeJSfile("newChumbaTOS_",chumbaInfo)
        print("Saved Check File in local directory")

parseChumba(localCheckFile)