import sys, string, os, os.path, time, traceback, shutil, commands

# run util library
utilLibPath = sys.argv[6]
execfile(utilLibPath)

print "Execute python script with WLST"
inputUser = rf_prep_str(sys.argv[1])
inputPassword = sys.argv[2]
inputHost = rf_prep_str(sys.argv[3])
inputPort = rf_prep_str(sys.argv[4])
inputProtocol = rf_prep_str(sys.argv[5])
inputAppName = rf_prep_str(sys.argv[7])
inputRevision = rf_prep_str(sys.argv[8])
inputFailFlag = rf_prep_str(sys.argv[9].lower())
inputLabel = rf_remove_pref(sys.argv[10], 6)
inputPartition = rf_remove_pref(sys.argv[11], 6)
inputTempPath = rf_prep_str(sys.argv[12])
inputOnlineMode = rf_prep_str(sys.argv[13])

inputURL = inputProtocol + '://' + inputHost + ':' + inputPort
#create backup folder and create file path for backup file
os.makedirs(inputTempPath)
filePath = inputTempPath + '/sca_deploy.out'

#print out list parameter
start_stop_App_printInputs(inputUser, inputProtocol, inputHost, inputPort, inputAppName, inputRevision, inputLabel, inputPartition, inputFailFlag)
if inputOnlineMode == 'YES':
    connect(inputUser, inputPassword, inputURL)
formatAppName = inputAppName + '[' + inputRevision + ']'

if inputPartition == '':
    inputPartition = 'default'

oldstdout=sys.stdout
sys.stdout = open(filePath,"w")
sca_listDeployedComposites(inputHost, inputPort, inputUser, inputPassword)
sys.stdout = oldstdout

deployStatus = checkDeployStatus(filePath, formatAppName, inputPartition)
if  deployStatus == 2:
    raise 'Wrong composite name or wrong revision, please input correct value!'
if deployStatus == 0:
    if  inputFailFlag == 'no':
        print 'Application' + inputAppName + ' is already active, exit'
        if inputOnlineMode == 'YES':
            disconnect()
        sys.exit()
    else:
        raise 'Application is already active, job failed'

try:
    if inputLabel == '':
        print 'startComposite without label'
        sca_startComposite(inputHost, inputPort,inputUser,inputPassword,inputAppName,inputRevision, partition=inputPartition)
    else:
        print 'startComposite with label'
        sca_startComposite(inputHost, inputPort,inputUser,inputPassword,inputAppName,inputRevision, inputLabel, partition=inputPartition)
    print 'Composite started'
    failed = 0
finally:
    if failed:
        print 'Composite failed to start'
    if inputOnlineMode == 'YES':
        disconnect()
    sys.exit()

close(filename)
os.remove(filename)