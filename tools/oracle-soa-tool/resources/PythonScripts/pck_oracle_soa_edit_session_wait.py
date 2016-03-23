print "Execute python script with WLST"
failed = 1    
try:
  edit()    
  startEdit(300000,1800000)   
except:
   raise 'ERROR: Edit session wait block problem. Job failed'