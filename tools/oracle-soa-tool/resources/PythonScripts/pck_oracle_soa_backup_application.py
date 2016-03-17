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

  
def getAppMBean(name, version, libraryModule):
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
inputVersion = sys.argv[5]
inputBackupDir = sys.argv[6]
inputBackupReport = sys.argv[7]
inputUseActiveVersion = sys.argv[8] #if true, the active version will be backed up instead of the first version found.
inputOptions = sys.argv[9]

def printInputs():
    print 'User: ' + sys.argv[1]
    #print 'pass: ' + sys.argv[2]
    print 'Host and port: ' + sys.argv[3]
    print 'Application name: ' + inputAppName
    print 'WebLogic/Archive version: ' + inputVersion        
    print 'Backup Directory: ' + inputBackupDir                
    print 'Backup Report: ' + inputBackupReport
    print 'Options: ' + inputOptions
        
printInputs()

connect(sys.argv[1].strip(), sys.argv[2].strip(), sys.argv[3].strip()) 
import sys, string, os, os.path, time, traceback, shutil 
  
appName = rf_prep_str(inputAppName)

# Dictionary param-value
paramsMaps = getOptions(rf_prep_str(inputOptions))
libraryModule = to_t_f(rf_prep_str(paramsMaps['libraryModule']))

appBean = getAppMBeanCore(appName, inputVersion, to_boolean(inputUseActiveVersion), libraryModule)
m = {} 

if appBean is not None: 
    #Print options to backup file
    options = ''
    deploymentOrder = appBean.getDeploymentOrder()
    if deploymentOrder is not None:
        options = 'deploymentOrder=' + str(deploymentOrder)
    
    libModule = appBean.getType()
    if libModule is not None:
        if libModule == 'Library':
            options += ',libraryModule=true'
            
    m.setdefault('UC4RB_WEBLOGIC_OPTIONS', options) 
    
    appPlanPath = appBean.getAbsolutePlanPath() 
    if appPlanPath is not None: 
        dst = os.path.join(inputBackupDir, os.path.basename(appPlanPath)) 
        shutil.copy(appPlanPath, dst ) 
        m.setdefault('UC4RB_WEBLOGIC_PLAN_PATH', dst ) 

    appPath  = appBean.getAbsoluteSourcePath()     
    if appPath is not None: 
        print 'appPath: ' + appPath 
        dst = os.path.join(inputBackupDir, os.path.basename(appPath))
        if dst is not None:
            print 'dst: ' + dst 
        if os.path.isdir(appPath): 
            shutil.copytree(appPath, dst, true ) 
        else: 
            shutil.copy( appPath, dst ) 
        m.setdefault('UC4RB_WEBLOGIC_PACKAGE', dst )
        m.setdefault('UC4RB_WEBLOGIC_PACKAGE_BAK', appPath )

    appStagingMode = appBean.getStagingMode() 
    if appStagingMode is not None: 
           m.setdefault('UC4RB_WEBLOGIC_STAGING', appStagingMode ) 

    appVersionIdentifier = appBean.getVersionIdentifier()    
        
    if appVersionIdentifier is not None: 
        print 'appVersionIdentifier: ' + appVersionIdentifier
        m.setdefault('UC4RB_WEBLOGIC_VERSION', appVersionIdentifier ) 

    appTargets = None 
    for target in appBean.getTargets(): 
        if appTargets is None: 
            appTargets = "%s" % (target.getName()) 
        else: 
            appTargets = "%s,%s" % (appTargets, target.getName()) 
    if appTargets is not None: 
        m.setdefault('UC4RB_WEBLOGIC_TARGETS', appTargets ) 

    appSubModuleTargets = None 
    for subdeployment in appBean.getSubDeployments():                      
        for  subdeployment_target in subdeployment.getTargets(): 
            if appSubModuleTargets is None: 
                appSubModuleTargets = "%s@%s" % ( subdeployment.getName() , subdeployment_target.getName() ) 
            else: 
                appSubModuleTargets = "%s,%s@%s" % ( appSubModuleTargets, subdeployment.getName() , subdeployment_target.getName() ) 
    if appSubModuleTargets is not None: 
        m.setdefault('UC4RB_WEBLOGIC_SUB_TARGETS', appSubModuleTargets ) 

    # Check the appPath if it is in AdminServer upload folder => set UPLOAD_MODE = YES otherwise UPLOAD_MODE = NO    
    cd('/')
    rootDir = cmo.getRootDirectory()
    adminServerName = cmo.getAdminServerName()
    cd('/Servers/'+adminServerName)
    uploadDir = cmo.getUploadDirectoryName()
    if uploadDir.startswith('.'):
      uploadDir = rootDir + uploadDir[1:len(uploadDir)]
    if appPath.startswith(uploadDir):
      m.setdefault('UPLOAD_MODE','YES')
    else:
      m.setdefault('UPLOAD_MODE','NO')
    
    m.setdefault('IS_APP_EXIST', 'YES' )
    
    print "Backup finished successfully."
else: 
    if appName is None:
        appName = ''
    print 'The application \"' + appName + '\" doesn\'t exist' 
    m.setdefault('IS_APP_EXIST', 'NO' ) 

writeReport( m, inputBackupReport ) 