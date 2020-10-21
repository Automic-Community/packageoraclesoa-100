import sys, string, os, os.path, time, traceback, shutil, threading 

# run util library
utilLibPath = sys.argv[6]
execfile(utilLibPath)

print "Execute python script with WLST"
inputUser = rf_prep_str(sys.argv[1])
inputPassword = sys.argv[2]
inputHost = rf_prep_str(sys.argv[3])
inputPort = rf_prep_str(sys.argv[4])
inputProtocol = rf_prep_str(sys.argv[5])
inputSar = rf_prep_str(sys.argv[7])
inputOverwrite = sys.argv[8]
inputForceDefault = sys.argv[9]
inputConfigPlan = rf_prep_str(sys.argv[10])
inputPartition = rf_prep_str(sys.argv[11])
inputOnlineMode = rf_prep_str(sys.argv[12])
inputTimeOut  = int(sys.argv[13])

failed = 1;
try:
    sar_path_tmp=inputSar.replace('\\','/');
    configPlanPath_tmp = None;

    if inputConfigPlan != None:
        configPlanPath_tmp = inputConfigPlan.replace('\\','/');

    if inputPartition == None:
        inputPartition='default';

    inputServerURL = '%s://%s:%s' % (inputProtocol, inputHost, inputPort);

    if inputOnlineMode == 'YES':
        connect(inputUser, inputPassword, inputServerURL);
        
    sca_listDeployedComposites(inputHost, inputPort, inputUser, inputPassword)

    if inputTimeOut == -1:
        sca_deployComposite(inputServerURL
          ,sar_path_tmp
          ,to_boolean(inputOverwrite)
          ,user=inputUser
          ,password=inputPassword
          ,forceDefault=to_boolean(inputForceDefault)
          ,configplan=configPlanPath_tmp 
          ,partition=inputPartition);
    else:
        userP = 'user=' + inputUser;
        passwordP = 'password=' + inputPassword;
        forceDefaultP = 'forceDefault=' + str(to_boolean(inputForceDefault));
        configplanP = 'configplan=' + str(configPlanPath_tmp);
        partitionP = 'partition=' + inputPartition;
        timeoutP = 'timeout=' + str(inputTimeOut);
        print "\nExecuting with " + timeoutP + " (s)"
        t = threading.Timer(inputTimeOut + 60, sca_deployComposite, args=(inputServerURL
          ,sar_path_tmp
          ,to_boolean(inputOverwrite)
          ,userP
          ,passwordP
          ,forceDefaultP
          ,configplanP 
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