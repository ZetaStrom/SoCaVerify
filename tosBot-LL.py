from playwright.sync_api import sync_playwright
import time 
import json

#Provide file path to the TOS json file here
checkFileLoc= r""

def writeJSfile(newFileName,objToDump):
    with open(newFileName, "w") as outfile:
        json.dump(objToDump, outfile)

def openCheckFile(checkFileLoc):
    f = open(checkFileLoc)
    data = json.load(f)
    f.close()
    return data

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://luckylandcasino.zendesk.com/hc/en-us/articles/360000868688-Official-Sweeps-Rules-")
    time.sleep(3)
    pTags = page.locator("p")
    h3Tags = page.locator("h3")
    time.sleep(1)
    llTerms = {}
    emptyPTags = []
    emptyHTags = []
    for i in range(pTags.count()):
        #print(f"Element {i}:")
        formattedP = pTags.nth(i).text_content().replace("  ","").replace("\t","").replace("\n","")
        if not(formattedP and formattedP.strip()):
            emptyPTags.append(i)
        else:
            llTerms["paragraph"+str(i)] = formattedP
    
    for i in range(h3Tags.count()):
        #print(f"Element {i}:")
        formattedH = h3Tags.nth(i).text_content().replace("  ","").replace("\n","")
        if not(formattedH and formattedH.strip()):
            emptyHTags.append(i)
        else: 
            llTerms["header"+str(i)] = formattedH
    if checkFileLoc!="":
        print("Checking known TOS file...")
        knownTOS = openCheckFile(checkFileLoc)
        cmnKeys = llTerms.keys()
        isSame=True
        differences={}
        for key in cmnKeys:
            if knownTOS[key]!=llTerms[key]:
                print(f"Difference in TOS at location {key}")
                differences[key]=llTerms[key]
                isSame=False
        if isSame:
            print("=== No changes found to Luckyland TOS! ===")
        else:
            print("=== Differences Detected in Lucky TOS! ===")
            print(differences)
            print("...")
            print("Saving new TOS...")
            writeJSfile("newLLandTOS_",llTerms)
    else:
        print("No check file detected. Please insert the path to the generated TOS file at the top of the script")
        print("Saving new TOS...")
        writeJSfile("LLandTos.json",llTerms)