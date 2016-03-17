#pck_weblogic_utils START
# remove chars if first char or last one are commas
def rf_trim_comma(str): 
    if str[:1] == ',': 
      str = str[1:len(str)] 
  
    if str[len(str) - 1:] == ',': 
      str = str[:len(str) - 1] 
  
    return str 
  
# remove all chars, spaces if they are first or last chars   
def rf_prep_str(val): 
    if val == None: 
        return None 
  
    i = len(val) 
    if i == 0: 
        return None 
  
    retval = val.strip() 
    retval = rf_trim_comma(retval) 
  
    j = len(retval) 
  
    if i != j: 
        retval = rf_prep_str(retval) 
  
    return retval 
  
# 'servername': 'abc', 'nodename': 'abc'  
def rf_prep_svrs_nodes(str1, str2): 
    arr1 = rf_prep_svrs(str1) 
    arr2 = rf_prep_svrs(str2) 
  
    if len(arr1) != len(arr2): 
        raise 'Unequal no. of elements in each string array' 
    else: 
        retarr = [] 
        for item1, item2 in zip(arr1, arr2): 
            # node_server = {\nodename\: item2.strip(), \servername\: item1.strip()} 
            node_server = {'nodename': item2.strip(), 'servername': item1.strip()} 
            retarr.append(node_server) 
        return retarr 
  
# Split string by comma, return array  
def rf_prep_svrs(str1): 
    if str1 == None: 
        return None 
    if len(str1) == 0: 
        return None 
  
    str1 = rf_prep_str(str1) 
    if str1 == None: 
        return [] 
    arr1 = str1.split(','); 
  
    retarr = [] 
    for item1 in arr1: 
       if len(item1.strip()) > 0: 
         retarr.append(item1.strip()) 
  
    return retarr 

# remove all space char(which is before or after comma char) in comma delimited string	
def rf_prep_comma_delim_str(str1):
    if str1 == None: 
        return None 
    if len(str1) == 0: 
        return None 
    retarr = rf_prep_svrs(str1)
    retstr = ','.join(retarr)
    return retstr
	
# check str are yes/true or no/false 
def to_t_f(str): 
    if str.lower() == 'yes' or str.lower() == 'true': 
       str = 'true'  
    elif str.lower() == 'no' or str.lower() == 'false': 
       str = 'false'  
    return str  
  
# return True or False when input string is yes/true or no/false 
def to_boolean(input): 
    if input.lower() == 'yes' or input.lower() == 'true': 
       return True  
    elif input.lower() == 'no' or input.lower() == 'false': 
       return False  
    elif input == '':
        return False
    raise "Invalid boolean string: " + input
  
# return string of characters in ASCII code for integer iterator arr  
def byte_array_to_string(arr): 
     str = '' 
     for b in arr: 
       str += chr(b) 
     return str 
  
# write iterator to file, default separator is double pipes    
def writeReport(m, filePath, separator="||"):
     report_file = open(filePath, 'w')
     for list in m.items(): 
       str = "%s%s%s\n" % (list[0], separator, list[1]) 
       report_file.write(str) 
     report_file.close()
  
  
def checkResourceExists(name, type): 
    if getMBean('/' + type + 's/' + name) is None: 
        return false 
    else: 
        return true 
  
  
def checkAppExistsInAppDeployments(name): 
  found = false 
  try:    
    cd('/') 
    for app in cmo.getAppDeployments(): 
      appName = app.getName() 
      cd('/AppDeployments/' + appName) 
      applicationName = get('ApplicationName')   
      if  applicationName == name: 
        found = true  
        break    
  except Exception: 
    return found 
  return found 

def checkAppExists(name,version,targets,libraryModule): 
  """ Check application exist in specific version and at specific targets
      Keyword arguments:
      name -- application/library name
      version -- application version identifier (declared in manifest). 
                 If blank, the active version will be used
      targets -- deployment targets which should be checked
  """
  found = false   
  try: 
    appBean = None
    if (version is None or version.strip() == ''):
      appBean = getAppMBeanCore(name, version, True, libraryModule)
    else:
      appBean = getAppMBean(name, version)   
    if appBean is None:
      return found 
    if (targets is None or targets.strip() == ''):      
      cd('/')
      targets = cmo.getAdminServerName()
      print 'Input targets is blank, using \"'+targets+'\"" target by default!'
    for target in appBean.getTargets():
      if (target.getName() in rf_prep_svrs(targets)):        
        found = true
        print 'Application \"'+name+'\" was deployed to target \"'+target.getName()+'\".'
        break
  except Exception: 
    return found 
  return found

def isActiveVersion(appNameWithVersion):    
    domainRuntime()
    cd('/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
    isActive = cmo.isActiveVersion(appNameWithVersion)
    
    #Go back to server config
    serverConfig()
    if(isActive == 1):
        print appNameWithVersion + ' is the active version'
        return True
    else:
        print appNameWithVersion + ' is not the active version'
        return False    

  
def getAppMBean(name, version):
    return getAppMBeanCore(name, version, False, libraryModule)
    
def getAppMBeanCore(name, version, useActiveVersion, libraryModule):
    """Returns an application object with the provided version.
        Keyword arguments:
        name -- application/library name
        version -- application version identifier (declared in manifest). If blank, the first version found is returned
        useActiveVersion -- if true, version argument is ignored, only the active version is returned (an application may have 0 or 1 active version)         
    """
    print 'getApplication/Library: name = %s, version = %s, useActiveVersion = %s' % (name, version, useActiveVersion) 
    if(useActiveVersion is True):
        version = ''
        
    mb = None 
    try:    
        cd('/')
        appLib = ''
        appLibDir = ''
        if libraryModule == 'true':
            appLib = cmo.getLibraries()
            appLibDir = '/Libraries/'
        elif libraryModule == 'false':
            appLib = cmo.getAppDeployments()
            appLibDir = '/AppDeployments/'
         
        for app in appLib: 
          appNameWithVersion = app.getName() #Format of appNameWithVersion is appName#version
          cd(appLibDir + appNameWithVersion) 
          applicationName = get('ApplicationName')   
          appVersion = get('VersionIdentifier')
          if  applicationName == name or appNameWithVersion == name: 
            if  version == '':
                if(useActiveVersion is False):
                    mb = getMBean(appLibDir + appNameWithVersion) 
                    break
                else:
                    if(isActiveVersion(appNameWithVersion) is True):
                        mb = getMBean(appLibDir + appNameWithVersion)                  
                        break                    
            else:
                if appVersion == version: 
                    mb = getMBean(appLibDir + appNameWithVersion) 
                    break    
    except Exception: 
        return mb 
    return mb

# Split string by delimiter, return array  
def rf_prep_svrs_delimiter(str1, delimiter): 
    if str1 == None: 
        return None 
    if len(str1) == 0: 
        return None 
  
    str1 = rf_prep_str(str1) 
    delimiter= delimiter.strip()
    
    if str1 == None: 
        return [] 
    arr1 = str1.split(delimiter); 
  
    retarr = [] 
    for item1 in arr1: 
       if len(item1.strip()) > 0: 
         retarr.append(item1.strip()) 
  
    return retarr 

# Options
def getOptions(inputOptions):
    paramMaps={
        'adminMode': 'false',
        'altDD': '',
        'altWlsDD': '',
        'archiveVersion': '',
        'block': 'true',
        'clusterDeploymentTimeout': 0,
        'createPlan': 'false',
        'defaultSubmoduleTargets': 'true',
        'deploymentPrincipalName': '',
        'deploymentOrder': 100,
        'forceUndeployTimeout': 0,
        'gracefulIgnoreSessions': 'false',
        'gracefulProductionToAdmin': 'false',
        'libImplVersion': '',
        'libraryModule': 'false',
        'libSpecVersion': '',
        'planStageMode': '',
        'planVersion': '',
        'remote': 'false',
        'retireGracefully': '',
        'retireTimeout': -1,
        'rmiGracePeriod': -1,
        'securityModel': '',
        'securityValidationEnabled': 'false',
        'timeout': 300000,
        'upload': 'false',
        'versionIdentifier': ''
    }
    # check if inputOptions = empty
    if inputOptions is None or inputOptions.strip() == '': 
        return paramMaps
    
    params = rf_prep_svrs_delimiter(inputOptions, ',')
    for param in params:
        eachParam = rf_prep_svrs_delimiter(param, '=')
        if len(eachParam) != 2:
            raise 'Input must be specified as name-value pairs'
        paramMaps[eachParam[0]] = eachParam[1]    
    return paramMaps

#pck_weblogic_utils END

inputAppName = sys.argv[4]
inputPackage = sys.argv[5]
inputTargets = sys.argv[6]
inputSubmodule = sys.argv[7]
inputStagingMode = sys.argv[8]
inputVersionIdentifier = sys.argv[9]
inputArchiveVersion = sys.argv[10]
inputPlanPath = sys.argv[11]
inputCreatePlan = sys.argv[12]
inputRemote = sys.argv[13]
inputUpload = sys.argv[14]
inputTimeout = sys.argv[15]
inputOptions = sys.argv[16]

def printParam(name, value):  
  if name is None:
    return None
  if value is None:
    value = ''
  print name + ': ' + value
  
def printInputs():
    printParam('User',sys.argv[1])
    #printParam('pass',sys.argv[2])
    printParam('Host and port',rf_prep_str(sys.argv[3]))
    printParam('Application Name',rf_prep_str(inputAppName))
    printParam('WebLogic package',rf_prep_str(inputPackage))
    printParam('Targets',rf_prep_comma_delim_str(inputTargets))
    printParam('Submodule Targets',rf_prep_comma_delim_str(inputSubmodule))
    printParam('Staging Mode',rf_prep_str(inputStagingMode))
    printParam('Version Identifier',rf_prep_str(inputVersionIdentifier))
    printParam('Archive Version',rf_prep_str(inputArchiveVersion))
    printParam('Plan path',rf_prep_str(inputPlanPath))
    printParam('Create Plan',to_t_f(inputCreatePlan))
    printParam('Remote',to_t_f(inputRemote))
    printParam('Upload',to_t_f(inputUpload))
    printParam('Timeout',inputTimeout)
    printParam('Options',inputOptions)
            
    
printInputs()

connect(sys.argv[1].strip(), sys.argv[2].strip(), sys.argv[3].strip())
import sys, string, os, os.path, time, traceback, shutil 
    

appName = rf_prep_str(inputAppName)
appTargets = rf_prep_comma_delim_str(inputTargets)
appVersion = rf_prep_str(inputVersionIdentifier)

paramsMaps = getOptions(rf_prep_str(inputOptions))
libraryModule=to_t_f(rf_prep_str(paramsMaps['libraryModule']))

if checkAppExists(appName,appVersion,appTargets,libraryModule):
  raise 'ERROR: The application/library \"'+ inputAppName +'\" was deployed before!'

#pck_weblogic_edit_session_wait START
print "Execute python script with WLST"
failed = 1    
try:
  edit()    
  startEdit(300000,1800000)   
except:
   raise 'ERROR: Edit session wait block problem. Job failed'
#pck_weblogic_edit_session_wait END

try: 
    path_tmp=inputPackage.replace('\\','/')   

    planPath_tmp = ''    
    if inputPlanPath != '':
        planPath_tmp = inputPlanPath.replace ('\\','/') 
        print 'converted plan path:'+planPath_tmp    
    
    
    
    progress=deploy(appName=appName
      ,path=rf_prep_str(path_tmp)
      ,targets=appTargets
      ,subModuleTargets=rf_prep_comma_delim_str(inputSubmodule)  
      ,stageMode=rf_prep_str(inputStagingMode)
      ,versionIdentifier=appVersion
      ,planPath=rf_prep_str(planPath_tmp) 
      ,adminMode=to_t_f(rf_prep_str(paramsMaps['adminMode']))
      ,altDD=rf_prep_str(paramsMaps['altDD'])
      ,altWlsDD=rf_prep_str(paramsMaps['altWlsDD'])
      ,archiveVersion=rf_prep_str(inputArchiveVersion)
      ,block=to_t_f(rf_prep_str(paramsMaps['block']))
      ,clusterDeploymentTimeout=int(paramsMaps['clusterDeploymentTimeout'])
      ,createPlan=to_t_f(inputCreatePlan)
      ,defaultSubmoduleTargets=to_t_f(rf_prep_str(paramsMaps['defaultSubmoduleTargets']))
      ,deploymentPrincipalName=rf_prep_str(paramsMaps['deploymentPrincipalName'])
      ,deploymentOrder=int(paramsMaps['deploymentOrder'])
      ,forceUndeployTimeout=int(paramsMaps['forceUndeployTimeout'])
      ,gracefulIgnoreSessions=to_t_f(rf_prep_str(paramsMaps['gracefulIgnoreSessions']))
      ,gracefulProductionToAdmin=to_t_f(rf_prep_str(paramsMaps['gracefulProductionToAdmin']))
      ,libImplVersion=rf_prep_str(paramsMaps['libImplVersion'])
      ,libraryModule=libraryModule
      ,libSpecVersion=(rf_prep_str(paramsMaps['libSpecVersion']))
      ,planStageMode=rf_prep_str(paramsMaps['planStageMode'])
      ,planVersion=rf_prep_str(paramsMaps['planVersion'])
      ,remote=to_t_f(inputRemote)
      ,retireGracefully=rf_prep_str(paramsMaps['retireGracefully'])
      ,retireTimeout=int(paramsMaps['retireTimeout'])
      ,rmiGracePeriod=int(paramsMaps['rmiGracePeriod'])
      ,securityModel=rf_prep_str(paramsMaps['securityModel'])
      ,securityValidationEnabled=to_t_f((rf_prep_str(paramsMaps['securityValidationEnabled'])))
      ,timeout=int(inputTimeout)
      ,upload=to_t_f(inputUpload)
      )   
    save()
    activate(block='true')

    count = 0    
    # checking deployment action is in progress and wait for 3 minute
    while progress.isRunning() and count < 180:
      print 'Deploying application...'
      time.sleep(5)
      count = count + 5
    progress.printStatus()      

    if progress.isCompleted() and not progress.isFailed():
      print 'Application \"'+ inputAppName +'\" is deployed successfully!'
      failed=0    

#pck_weblogic_edit_finally_block START
finally:                    
   if failed:               
    print 'Job failed. finally block info:'      
    try:                    
      edit()                
      undo('true', 'y')      
      print 'undo is done'  
    except:                 
      print 'undo not done'    
   try:                    
      edit()                
      c2 = getConfigManager() 
      if c2.getCurrentEditor() is not None:  
         stopEdit('y')         
         print 'edit session was active. stopEdit is done'   
   except:                 
      print 'stopEdit not done, try cancelEdit'  
         
      try:                     
        edit()                   
        cancelEdit('y')             
        print 'cancelEdit is done'   
      except:                         
        print 'cancelEdit not done.'        
   disconnect('true') 
   exit('y', failed)

#pck_weblogic_edit_finally_block END
