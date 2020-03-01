import sys
import os
import csv
import subprocess
from collections import Counter
import re
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

namearr = []

resultFields = {"File_Hash","Predicted_Label"}

combinedFeatures={
    "name":0,
    "urls":0,
"dllcount":0,
"apicount":0,
    'Machine':0,
    'SizeOfOptionalHeader':0,
    'Characteristics':0,
"MajorLinkerVersion":0,
"MinorLinkerVersion":0,
    "NumberOfSections":0,
    "SizeOfCode":0,
    "SizeOfInitializedData":0,
    "SizeOfUninitializedData":0,
"BaseOfCode":0,
"BaseOfData":0,
    "ImageBase":0,
    "SectionAlignment":0,
    "FileAlignment":0,
"MajorOperatingSystemVersion":0,
"MinorOperatingSystemVersion":0,
    "MajorImageVersion":0,
    "MinorImageVersion":0,
"MajorSubsystemVersion":0,
"MinorSubsystemVersion":0,
"Reserved1":0,
    "SizeOfImage":0,
    "SizeOfHeaders":0,
    "CheckSum":0,
    "Subsystem":0,
    "DllCharacteristics":0,
"SizeOfStackReserve":0,
"SizeOfStackCommit":0,
"SizeOfHeapReserve": 0,
"SizeOfHeapCommit":0,
"LoaderFlags":0,
"NumberOfRvaAndSizes":0,
"SizeOfLoadConfiguration":0,
    "SizeOfRawData":0,
"maxSizeOfRawData":0,
"minSizeOfRawData":0,
"avgSizeOfRawData":0,
"Misc_VirtualSize":0,
"minMisc_VirtualSize":0,
"maxMisc_VirtualSize":0,
"avgMisc_VirtualSize":0,
"minEntropy":0,
"maxEntropy":0,
"avgEntropy":0,


"shgetdiskfreespacea":0,
"multinetgetconnectionperformancea":0,
"wnetgetresourceparentw":0,
"shqueryinfokeya":0,
"arrangeiconicwindows":0,
"pathiscontenttypea":0,
"ragobject":0,
"multinetgetconnectionperformancew":0,
"realgetwindowclassa":0,
"enumdateformatsw":0,
"getwindowmodulefilenamea":0,
"wnetgetresourceparenta":0,
"wnetaddconnectionw":0,
"wsaenumnamespaceprovidersw":0,
"sceanalyzesystem":0,
"setupinstallfilesfrominfsectiona":0,
"isbadhugereadptr":0,
"getmenucontexthelpi":0,
"shenumvaluea":0,
"shqueryvalueexa":0,
"setmenucontexthelpi":0,
"registerserver":0,
"setclasswor":0,
"checkcolorsingamut":0,
"impsetimew":0,
"wsaenumprotocolsa":0,
"getalttabinfoa":0,
"wsaunhookblockinghook":0,
"animatepalette":0,
"wscupdateprovider":0,
"wsalookupserviceen":0,
"wsalookupservicebeginw":0,
"sceissystemdatabase":0,
"scefreememory":0,
"setupgettargetpatha":0,
"setupgetsourcefilelocationa":0,
"setupcommitfilequeuea":0,
"sceopenprofile":0,
"jetrestore2":0,
"_mbslwr":0,
"readeventlogw":0,
"shgetthreadref":0,
"getprofilesectionw":0,
"addauditaccessobjectace":0,
"getthreadpriorityboost":0,

'call':0,'pop':0,'cmp':0,'jz':0,'lea':0,'test':0,'jmp':0,'add':0,'jnz':0,'retn':0,'xor':0,
'bt':0,'fdvip':0,'fild':0,'fstcw':0,'imul':0,'int':0,'nop':0,'pushf':0,'rdtsc':0,'sbb':0,'setb':0,'setle':0,'shld':0,'std':0
}

avgSection = {
"SizeOfRawData":0,
"Misc_VirtualSize":0
}
Arr = []
selection_query = "cut -f3|cut -f1-6 -d' '|tr -s ' '|cut -f1 -d' '"
def writeHeader():
    with open('./TestData.csv', 'w', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=combinedFeatures)
        writer.writeheader()

def writeCSV(row):
    with open('./TestData.csv', 'a', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=combinedFeatures)
        writer.writerow(row)

def writeResultCSV(rows):
   rows.to_csv("./static.csv",sep=",",encoding="utf-8", index=False)


def extractOpCode(filepath):
    query = "cat " + filepath + " | " + selection_query
    output = subprocess.check_output(query, shell=True).decode()
    list = output.split("\n")
    result = Counter(list)
    addKeyToFeaturesList(result)


def addKeyToFeaturesList(data):
    for key in data:
        if key in combinedFeatures.keys():
            combinedFeatures.update({key: data.get(key)})


def avgCalculator(avgKey, minKey, maxKey, value, existingValue):
    if existingValue > 0.0:
        minValue = float(combinedFeatures.get(minKey))
        maxValue = float(combinedFeatures.get(maxKey))
        if value < minValue:
            combinedFeatures.update({minKey:value})
        elif value > maxValue:
            combinedFeatures.update({maxKey:value})
        averageValue = round(float(float(combinedFeatures.get(maxKey)) + float(combinedFeatures.get(minKey))) / 2, 2)
        combinedFeatures.update({avgKey:averageValue})
    else:
        combinedFeatures.update({avgKey: value})
        combinedFeatures.update({minKey: value})
        combinedFeatures.update({maxKey: value})


def processLine(file):
    for line in file:
        if line != "\n":
            splitedItem = " ".join(line.split())
            arr = splitedItem.split(" ")
            if len(arr) == 4:
                key = arr[2].strip(":").strip(" ")
                value = arr[3]
                if (key in combinedFeatures.keys()):
                    try:
                        if key in avgSection.keys():
                            if key == "SizeOfRawData":
                                existingValue = round(float(combinedFeatures.get("avgSizeOfRawData")), 2)
                                avgCalculator("avgSizeOfRawData", "minSizeOfRawData", "maxSizeOfRawData",
                                              int(value, 16), existingValue)
                            elif key == "Misc_VirtualSize":
                                existingValue = round(float(combinedFeatures.get("avgMisc_VirtualSize")), 2)
                                avgCalculator("avgMisc_VirtualSize", "minMisc_VirtualSize", "maxMisc_VirtualSize",
                                              int(value, 16), existingValue)
                        else:
                            if int(value, 16) > 0:
                                combinedFeatures.update({key: int(value, 16)})
                    except ValueError:
                        combinedFeatures.update({key: 0})

            if "Entropy:" in line:
                getEntropy(line)
        else:
            return



def getEntropy(line):
    result = line.split(" ")
    key = result[0].strip(":")
    value = round(float(result[1].strip(" ")),2)
    existingValue = float(combinedFeatures.get("avgEntropy"))
    avgCalculator("avgEntropy", "minEntropy", "maxEntropy", value, existingValue)


def extractStrings(filepath):
    with open(filepath, "r") as file:
        #'''Extract all the URL, IP address and DLL counts'''
        result = file.read().lower()
        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', result)
        dlls = re.findall("([\w\.-]+[d,D][l,L][l,L])", result)
        if len(urls)>0:
            combinedFeatures.update({"urls":len(urls)})
            addKeyToFeaturesList(Counter(urls))
        if len(dlls)>0:
            combinedFeatures.update({"apicount":len(dlls)})
            combinedFeatures.update({"dllcount":len(set(dlls))})
            addKeyToFeaturesList(Counter(urls))



def extractAPIs(filepath):
    with open(filepath, "r",encoding='latin-1') as file:
        regexp = re.compile(r'dll[\.]\w+')
        data = file.read().lower()
        result = Counter(re.findall(regexp, data))
        for api in result:
            if api != None:
                value = result.get(api)
                api = api.strip("dll.").strip(" ")
                if api in combinedFeatures.keys():
                    combinedFeatures.update({api: int(combinedFeatures.get(api))+value})

def extractPEHeader(filepath):
    with open(filepath, "r", encoding='latin-1') as file:
        for eachLine in file:
            if "[IMAGE_DOS_HEADER]" in eachLine:
                processLine(file)
            elif "[IMAGE_NT_HEADERS]" in eachLine:
                processLine(file)
            elif "[IMAGE_OPTIONAL_HEADER]" in eachLine:
                processLine(file)
            elif "[IMAGE_FILE_HEADER]" in eachLine:
                processLine(file)
            elif "[IMAGE_OPTIONAL_HEADER]" in eachLine:
                processLine(file)
            elif "[IMAGE_SECTION_HEADER]" in eachLine:
                processLine(file)
            elif "[IMAGE_IMPORT_DESCRIPTOR]" in eachLine:
                processLine(file)


def startProcessing(directory):
    for file_folder in os.listdir(directory)[:10]:
        combinedFeatures.update({}.fromkeys(combinedFeatures, 0))
        combinedFeatures.update({"name":file_folder})
        namearr.append(file_folder)
        print("extracting : " + file_folder)
        for filename in os.listdir(directory + "/"+ file_folder):
            if filename == "Opcodes.txt":
                extractOpCode(directory + "/" +file_folder + "/" + filename)
            elif filename == "Structure_Info.txt":
                extractPEHeader(directory + "/" +file_folder + "/" + filename)
                extractAPIs(directory + "/"+ file_folder + "/" + filename)
            elif filename == "String.txt":
                extractStrings(directory + "/" +file_folder + "/" + filename)
        Arr.append(combinedFeatures.copy())

def main():
    if len(sys.argv)<2:
        print("Usage: static.py <absolute_path> to files directory")
        sys.exit(0)
    else:
        PATH = sys.argv[1]
        print("PATH: " , PATH)
        startProcessing(PATH)
        writeHeader()
        for el in Arr:
            writeCSV(el)


def testWithModel():
    #Standard PCA component
    std_pca = pickle.load(open("./PCA.pkl", "rb"))

    model = pickle.load(open("./scriptedModel.sav", "rb"))
    df = pd.read_csv("./TestData.csv",sep=",")

    df = df.loc[(df != 0).any(axis=1)]
    df = df.fillna(0)
    df = df.drop(['name'],axis=1)
    X_test = df

    #Applying original PCA. which was applied at the time of training.
    X_test = std_pca.transform(X_test)

    yhat = model.predict(X_test)
    result= pd.DataFrame({'File_Hash': namearr, 'Predicted_Label': yhat})
    writeResultCSV(result)
    print(result)


if __name__ == '__main__':
    main()
    print("*****************************")
    print("****Extraction Completed*****")
    print("*****************************")
    print("*****Predicting Category*****")
    testWithModel()
    print("\nProcess Completed Results are placed in static.csv")
    print("\nPath Analyzed: ", sys.argv[1])



