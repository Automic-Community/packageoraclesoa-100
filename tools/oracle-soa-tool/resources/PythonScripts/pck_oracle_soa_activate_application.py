import sys, string, os, os.path, time, traceback, shutil 

# run util library
utilLibPath = sys.argv[6]
execfile(utilLibPath)

print "Execute python script with WLST"
inputUser = rf_prep_str(sys.argv[1])
inputPassword = sys.argv[2]
inputHost = rf_prep_str(sys.argv[3])
inputPort = sys.argv[4]
inputProtocol = sys.argv[5]
inputApplication = rf_prep_str(sys.argv[7])
inputRevision = rf_prep_str(sys.argv[8])
inputLabel = rf_prep_str(sys.argv[9])
inputPartition = rf_prep_str(sys.argv[10])
inputOnlineMode = rf_prep_str(sys.argv[11])

failed = 1;
try:
    url = '%s://%s:%s' % (inputProtocol, inputHost, inputPort)
    if inputOnlineMode == 'YES':
        connect(inputUser, inputPassword, url)

    if inputPartition == None:
        inputPartition = 'default';

    sca_listDeployedComposites(inputHost, inputPort, inputUser, inputPassword)

    sca_activateComposite(inputHost,
        inputPort, 
        inputUser, 
        inputPassword, 
        inputApplication, 
        inputRevision, 
        label=inputLabel, 
        partition=inputPartition);
    failed = 0;

except Exception, detail:
    print 'Exception: ', detail;
    dumpStack();
if inputOnlineMode == 'YES':
    disconnect('true');
exit('y', failed);