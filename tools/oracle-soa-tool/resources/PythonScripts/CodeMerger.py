'''
Created on Nov 29, 2014

@author: Hunghq
'''
import sys, os, re, fnmatch, shutil, datetime, time
from os import listdir
from os.path import isfile, join

START_TAG_PATTERN = r'^#(.*)\sSTART$'
START_TAG_FORMATTER = r'^#%s\sSTART$'
END_TAG_FORMATTER = r'^#%s\sEND$'

print "-----------------------------------MERGE CODE REGIONS-------------------------------"
#print "Number of arguments: %s" % len(sys.argv)
if len(sys.argv) == 4:
    inputProcessDir = sys.argv[1]
    inputIncludeDir = sys.argv[2]
    inputFilePattern = sys.argv[3] #"Empty means all files"
elif len(sys.argv) == 1:
    inputProcessDir = os.path.dirname(os.path.realpath(__file__))
    inputIncludeDir = os.path.join(inputProcessDir, "includes")
    inputFilePattern = "*.py"
else:
    raise 'Invalid argument. \nUsage:\njython CodeMerger.py "Path to the directory to process" "Path to the directory containing includes" "File pattern"'

print "Directory to process: " + inputProcessDir
print "Directory containing includes: " + inputIncludeDir
print "File pattern: " + inputFilePattern

#Create backup directory
timestamp = time.time()
timestampStr = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H-%M-%S')
backupDir = join(inputProcessDir, "backup " + timestampStr)
if not os.path.exists(backupDir):
    os.makedirs(backupDir)

newContent = ""
includes = {}
indent = 4
fileCount = 0
noMergeCount = 0
def log(message, length=indent, useSpace=False):
    global indent
    if length is not None:    
        indent = length
    
    if useSpace:
        print " %s%s" % (" " * indent, message)
    else: 
        print "/%s%s" % ("-" * indent, message)

def readFileContent(filePath):    
    fo = open(filePath, "r")
    #log('Reading fi: ' + fi.name, None, True)
    tmp = fo.read()
    fo.close()
    return tmp

def execute(regions):    
    global newContent
    log('Process regions:', 4)
    for region in regions:
        log(region, 8)
        matchStart = re.search(START_TAG_FORMATTER % region, newContent, re.MULTILINE)
        if matchStart:
            matchEnd = re.search(END_TAG_FORMATTER % region, newContent, re.MULTILINE)
            if matchEnd:                                                                         
                log("Replacing", None, True)
                newContent = newContent[:matchStart.end()] + "\n" + includes[region] + "\n" + newContent[matchEnd.start():]                           
            else:
                raise "No end tag found for region: " + region
                break;
    
def locateIncludeFile(region):
    onlyfiles = [ f for f in listdir(inputIncludeDir) if isfile(join(inputIncludeDir, f))]
    for fileName in onlyfiles:
        fileNameWithoutExtension = os.path.splitext(fileName)[0]
        if(fileNameWithoutExtension == region):
            log(fileName, 8)        
            return os.path.join(inputIncludeDir, fileName)
    raise "Cannot locate the include fi for region: " + region

def processFile(fileName):   
    global newContent
    global includes
    global noMergeCount
    filePath = os.path.join(inputProcessDir, fileName)
    print '[%s] INPUT FILE: %s' % (fileCount, fileName)
    newContent = readFileContent(filePath)
    regions = re.findall(START_TAG_PATTERN, newContent, re.MULTILINE)
    if len(regions) > 0:
        log('Locate include files...', 4)
        seen = set()
        for region in regions:
            # Strips the fi extension if it is in region name.
            region = os.path.splitext(region)[0]
            if region not in seen:
                seen.add(region)
                if not includes.has_key(region):            
                    includes[region] = readFileContent(locateIncludeFile(region))                
            else:
                raise "A duplicate code region is found in " + fileName    
        
        execute(regions)
        log('Merge completed', 4)    
        shutil.copy(filePath, backupDir)
        updateFile = open(filePath, "w")
        updateFile.write(newContent)
        updateFile.close()
    else:
        log('No merge is required.')
        noMergeCount = noMergeCount + 1
    
# Read files in the input directory and process one by one
onlyfiles = [ f for f in listdir(inputProcessDir) if isfile(join(inputProcessDir, f)) ]
for fi in onlyfiles:
    if inputFilePattern == "" or fnmatch.fnmatch(fi, inputFilePattern):        
        if(fi != os.path.basename(__file__)):   
            fileCount = fileCount + 1;     
            processFile(fi)
print "-----------------------------------COMPLETED-------------------------------"
print "Process completed for \t%s file(s)" % fileCount
print "Merge completed for \t%s file(s)" % (fileCount - noMergeCount) 
print "Merge not required for \t%s file(s)" % noMergeCount
