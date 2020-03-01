import csv
import os
import re
import subprocess
from collections import Counter
from Main.Section import *


commonPath  = "/home/manikant/Documents/CS698/midterm/Static_Analysis_RAWDATA/"
selection_query = "cut -f3|cut -f1-6 -d' '|tr -s ' '|cut -f1 -d' '"
apis = set()
opcode = set()
malwareApis = {}
benignApis = {}

malwareArr = []
benignArr = []
Arr = []


def writeHeader():
    with open('./TraningData.csv', 'w', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=combinedFeatures)
        writer.writeheader()

def writeCSV(rows):
    with open('./TraningData.csv', 'a', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=combinedFeatures)
        writer.writerow(rows)


def extractOpCode(filepath):
    query = "cat "+filepath+" | "+selection_query
    output = subprocess.check_output(query, shell=True).decode()
    list = output.split("\n")
    result = Counter(list)
    addKeyToFeaturesList(result)

def addKeyToFeaturesList(data):
    for key in data:
        if key in combinedFeatures.keys():
            combinedFeatures.update({key: combinedFeatures.get(key)+data.get(key)})

def extractStrings(filepath):
    with open(filepath, "r") as file:
        #'''Extract all the URL, IP address and DLL counts'''
        result = file.read().lower()
        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', result)
        dlls = re.findall("([\w\.-]+[d,D][l,L][l,L])", result)
        ips = re.findall(ipregex, result)
        if len(urls)>0:
            combinedFeatures.update({"urls":len(urls)})
            addKeyToFeaturesList(Counter(urls))
        if len(dlls)>0:
            combinedFeatures.update({"apicount":len(dlls)})
            combinedFeatures.update({"dllcount":len(set(dlls))})
            addKeyToFeaturesList(Counter(urls))
        if len(ips)>0:
            combinedFeatures.update({"ipcount": len(ips)})

def processLine(file):
    for line in file:
        if line != "\n":
            splitedItem = " ".join(line.split())
            arr = splitedItem.split(" ")
            if len(arr)==4:
                key = arr[2].strip(":").strip(" ")
                value = arr[3]
                if(key in combinedFeatures.keys()):
                    try:
                        if key in avgSection.keys():
                            if key=="SizeOfRawData":
                                existingValue = round(float(combinedFeatures.get("avgSizeOfRawData")),2)
                                avgCalculator("avgSizeOfRawData", "minSizeOfRawData", "maxSizeOfRawData", int(value,16), existingValue)
                            elif key =="Misc_VirtualSize":
                                existingValue = round(float(combinedFeatures.get("avgMisc_VirtualSize")), 2)
                                avgCalculator("avgMisc_VirtualSize", "minMisc_VirtualSize", "maxMisc_VirtualSize", int(value,16),existingValue)
                        else:
                            if int(value, 16)>0:
                                combinedFeatures.update({key: int(value, 16)})
                    except ValueError:
                        combinedFeatures.update({key: 0})

            if "Entropy:" in line:
                getEntropy(line)
            else:
                return



def extractAPIs(filepath, type):
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

def getEntropy(line):
    result = line.split(" ")
    key = result[0].strip(":")
    value = round(float(result[1].strip(" ")),2)
    existingValue = float(combinedFeatures.get("avgEntropy"))
    avgCalculator("avgEntropy", "minEntropy", "maxEntropy", value, existingValue)




def extractPEHEader(filepath, type):
    with open(filepath, "r",encoding='latin-1') as file:
        for eachLine  in file:
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



def extractBenignData():
    directory = commonPath +"Benign/"
    for file_folder in os.listdir(directory):
        combinedFeatures.update({}.fromkeys(combinedFeatures,0))
        combinedFeatures.update({"category": 'B'})
        print("extracting : " + file_folder)
        for filename in os.listdir(directory + file_folder):
            if filename == "Opcodes.txt":
                extractOpCode(directory + file_folder + "/" + filename)
            if filename == "Structure_Info.txt":
                extractPEHEader(directory + file_folder + "/" + filename, type="benign")
                extractAPIs(directory + file_folder  + "/" + filename, type="benign")
            elif filename == "String.txt":
                extractStrings(directory + file_folder + "/" + filename)
        print("extraction Done : " + file_folder)
        Arr.append(combinedFeatures.copy())

def extractMalwareData():
    directory = commonPath + "Malware/"
    for file_folder in os.listdir(directory):
        for folderEachType in os.listdir(directory + file_folder):
            print("extracting : " + file_folder)
            combinedFeatures.update({}.fromkeys(combinedFeatures, 0))
            combinedFeatures.update({"category": 'M'})
            for filename in os.listdir(directory + file_folder + "/" + folderEachType):
                if filename == "Opcodes.txt":
                    extractOpCode(directory + file_folder+"/"+ folderEachType + "/" + filename)
                elif filename == "Structure_Info.txt":
                    extractPEHEader(directory + file_folder+"/"+ folderEachType + "/" + filename, type="malware")
                    extractAPIs(directory + file_folder + "/" + folderEachType + "/" + filename, type="malware")
                elif filename == "String.txt":
                    extractStrings(directory + file_folder+"/"+ folderEachType + "/" + filename)
            print("extraction Done : " + file_folder)
            Arr.append(combinedFeatures.copy())
def main():
    extractBenignData()
    extractMalwareData()
    writeHeader()
    for el in Arr:
        writeCSV(el)


if __name__ == '__main__':
    main()