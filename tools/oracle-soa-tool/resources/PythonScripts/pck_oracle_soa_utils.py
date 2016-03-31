#pck_weblogic_utils START
# remove chars if first char or last one are commas
#from selenium.webdriver.remote.utils import return_value_if_exists

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

def checkAppExists(name,version,targets):
  """ Check application exist in specific version and at specific targets
      Keyword arguments:
      name -- application name
      version -- application version identifier (declared in manifest).
                 If blank, the active version will be used
      targets -- deployment targets which should be checked
  """
  found = false
  try:
    appBean = None
    if (version is None or version.strip() == ''):
      appBean = getAppMBeanCore(name, version, True)
    else:
      appBean = getAppMBean(name, version)
    if appBean is None:
      return found
    # if (targets is None or targets.strip() == ''):
      # cd('/')
      # targets = cmo.getAdminServerName()
      # print 'Input targets is blank, using \"'+targets+'\"" target by default!'
    for target in appBean.getTargets():
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
    return getAppMBeanCore(name, version, False)

def getAppMBeanCore(name, version, useActiveVersion):
    """Returns an application object with the provided version.
        Keyword arguments:
        name -- application name
        version -- application version identifier (declared in manifest). If blank, the first version found is returned
        useActiveVersion -- if true, version argument is ignored, only the active version is returned (an application may have 0 or 1 active version)
    """
    print 'getApplication: name = %s, version = %s, useActiveVersion = %s' % (name, version, useActiveVersion)
    if(useActiveVersion is True):
        version = ''

    mb = None
    try:
        cd('/')
        for app in cmo.getAppDeployments():
          appNameWithVersion = app.getName() #Format of appNameWithVersion is appName#version
          cd('/AppDeployments/' + appNameWithVersion)
          applicationName = get('ApplicationName')
          appVersion = get('VersionIdentifier')
          if  applicationName == name or appNameWithVersion == name:
            if  version == '':
                if(useActiveVersion is False):
                    mb = getMBean('/AppDeployments/' + appNameWithVersion)
                    break
                else:
                    if(isActiveVersion(appNameWithVersion) is True):
                        mb = getMBean('/AppDeployments/' + appNameWithVersion)
                        break
            else:
                if appVersion == version:
                    mb = getMBean('/AppDeployments/' + appNameWithVersion)
                    break
    except Exception:
        return mb
    return mb

def start_stop_App_printInputs(inputUser, inputProtocol, inputHost, inputPort, inputAppName, inputRevision, inputLabel, inputPartition, inputFailFlag):
    print 'User: ' + inputUser
    print 'Host and port: ' + inputProtocol + '://' + inputHost + ':' + inputPort
    print 'Composite name: ' + inputAppName
    print 'Revision: ' + inputRevision
    print 'Label: ' + inputLabel
    print 'Partition: ' + inputPartition
    print 'Fail Flag: ' + inputFailFlag

def findMBean(prefix, name):
    # get a listing of everything in the current directory
    mydirs = ls(returnMap='true');

    # we're going to use a regular expression for our test
    pattern = java.util.regex.Pattern.compile(str(prefix) + str('.*name=') + str(name) + str('.*$'));

    # loop through the listing
    for mydir in mydirs:
        x = java.lang.String(mydir);
        matcher = pattern.matcher(x);
        # if we find a match, add it to the found list
        while matcher.find():
            return x;

def rf_remove_pref(str, index):
    if len(str) != 0 and len(str) >= index:
      str = str[index:len(str)]

    return str

def checkDeployStatus(filename, formatAppName, partition):
    returnValue = 2
    for line in open(filename):
        if formatAppName in str(line) and 'state=on' in str(line) and 'partition=' + partition in str(line):
            returnValue = 0
        if formatAppName in str(line) and 'state=off' in str(line) and 'partition=' + partition in str(line):
            returnValue = 1
    return returnValue

#pck_weblogic_utils END