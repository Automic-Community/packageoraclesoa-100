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
