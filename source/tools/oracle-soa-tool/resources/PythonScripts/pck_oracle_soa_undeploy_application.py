import sys, string, os, os.path, time, traceback, shutil, threading

# run util library
utilLibPath = sys.argv[6]
execfile(utilLibPath)

print "Execute python script with WLST"
inputUser = rf_prep_str(sys.argv[1])
inputPassword = rf_prep_str(sys.argv[2])
inputHost = rf_prep_str(sys.argv[3])
inputPort = rf_prep_str(sys.argv[4])
inputProtocol = rf_prep_str(sys.argv[5])
inputAppName = rf_prep_str(sys.argv[7])
inputRevision = rf_prep_str(sys.argv[8])
inputPartition = rf_prep_str(sys.argv[9])
inputOnlineMode = rf_prep_str(sys.argv[10])
inputTimeOut  = int(sys.argv[11])

failed = 1
try:
    url = '%s://%s:%s' % (inputProtocol, inputHost, inputPort)

    if inputOnlineMode == 'YES':
        connect(inputUser, inputPassword, url);

    if inputPartition == None:
        inputPartition = 'default';

    sca_listDeployedComposites(inputHost, inputPort, inputUser, inputPassword)

    if inputTimeOut == -1:
        sca_undeployComposite(url
          ,inputAppName
          ,inputRevision
          ,user=inputUser
          ,password=inputPassword
          ,partition=inputPartition);
    else:
        userP = 'user=' + inputUser;
        passwordP = 'password=' + inputPassword;
        partitionP = 'partition=' + inputPartition;
        timeoutP = 'timeout=' + str(inputTimeOut);
        print "\nExecuting with " + timeoutP + " (s)"
        t = threading.Timer(inputTimeOut + 60, sca_undeployComposite, args=(url
          ,inputAppName
          ,inputRevision
          ,userP
          ,passwordP 
          ,partitionP
          ,timeoutP,))
        t.start();
        print "Timed out!"
    failed = 0;

except Exception, detail:
    print 'Exception: ', detail;
    dumpStack();
if inputOnlineMode == 'YES':
    disconnect('true');
exit('y', failed);