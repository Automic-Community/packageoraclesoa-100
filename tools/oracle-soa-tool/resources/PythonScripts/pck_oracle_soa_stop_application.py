import sys, string, os, os.path, time, traceback, shutil
# run util library
utilLibPath = sys.argv[6]
execfile(utilLibPath)

print "Execute python script with WLST"
inputUser = sys.argv[1]
inputPassword = sys.argv[2]
inputHost = sys.argv[3]
inputPort = sys.argv[4]
inputProtocol = sys.argv[5]
inputAppName = sys.argv[7]
inputRevision = sys.argv[8]
inputFailFlag = sys.argv[9].lower()
inputLabel = rf_remove_pref(sys.argv[10], 6)
inputPartition = rf_remove_pref(sys.argv[11], 6)
inputTempPath = sys.argv[12]

inputURL = inputProtocol + '://' + inputHost + ':' + inputPort
#create backup folder and create file path for backup file
os.makedirs(inputTempPath)
filePath = inputTempPath + '/sca_deploy.out'

#print out list parameter
start_stop_App_printInputs(inputUser, inputProtocol, inputHost, inputPort, inputAppName, inputRevision, inputLabel, inputPartition, inputFailFlag)

connect(inputUser.strip(), inputPassword.strip(), inputURL.strip())
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
if deployStatus == 1:
    if  inputFailFlag == 'no':
        print 'Application' + inputAppName + ' is already stopped, exit'
        disconnect()
        sys.exit()
    else:
        raise 'Application is already active, job failed'

try:
    if inputLabel == '':
        print 'stopComposite without label'
        sca_stopComposite(inputHost, inputPort,inputUser,inputPassword,inputAppName,inputRevision, partition=inputPartition)
    else:
        print 'stopComposite with label'
        sca_stopComposite(inputHost, inputPort,inputUser,inputPassword,inputAppName,inputRevision, inputLabel, partition=inputPartition)
    failed = 0
finally:
    if failed:
        print 'Composite failed to stop'
    else:
        print 'Composite stopped'
    disconnect()
    sys.exit()

close(filename)
os.remove(filename)