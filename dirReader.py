def searchAllDirectories(ftp, filenames):
    global counter
    files.sort()
    traverse(ftp, filenames, ftp)
    
def traverse(ftp, filenames, path)
    try:
     for name in filenames:
        ftp.cwd(name)
        if name != "all" and counter < 5:   
           path =path + "/" + name
      
    except ftplib.error_perm:
        print "%s is not a directory, continuing" % name
        #make dir...
        #download ..
         
        print "downloading " 
        urllib.urlretrieve(path + "/" + name)
        
        path = ftp
        return
    except TimeoutException:
        print "%s caused a timeout after 10 seconds" % name
        return
    else:
        signal.alarm(0)  # resets alarm      

   
