import sys, string, os, os.path, time, traceback, shutil
# run util library
utilLibPath = sys.argv[6]
execfile(utilLibPath)

print "Execute python script with WLST"
inputUser = sys.argv[1]
inputPassword = sys.argv[2]
inputHost = rf_prep_str(sys.argv[3])
inputPort = sys.argv[4]
inputProtocol = sys.argv[5]
inputAppName = sys.argv[7]
inputRevision = sys.argv[8]
inputFailFlag = sys.argv[9].lower()
inputLabel = rf_remove_pref(sys.argv[10], 6)
inputURL = inputProtocol + '://' + inputHost + ':' + inputPort

#print out list parameter
startApp_printInputs(inputUser, inputProtocol, inputHost, inputPort, inputAppName, inputRevision, inputLabel, inputFailFlag)

connect(inputUser.strip(), inputPassword.strip(), inputURL.strip())
custom()
cd('oracle.soa.config')
composite = findMBean('oracle.soa.config:partition=default,j2eeType=SCAComposite','"'+inputAppName+'"')
cd(composite)
compositeState = get('State')

failed = 1

if compositeState == 'on':
    if inputFailFlag == 'no':
        print 'Application' + inputAppName + ' is already active, exit'
        disconnect()
        sys.exit()
    else:
        raise 'Application is already active, job failed'
else:
    try:
        if inputLabel == '':
            print 'startComposite without label'
            sca_startComposite(inputHost, inputPort,inputUser,inputPassword,inputAppName,inputRevision)
        else:
            print 'startComposite with label'
            sca_startComposite(inputHost, inputPort,inputUser,inputPassword,inputAppName,inputRevision, inputLabel)
        print 'Composite started'
        failed = 0
    finally:
        if failed:
            print 'Composite failed to start'
        disconnect()
        sys.exit()

