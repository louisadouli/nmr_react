import os

def readTextFiles():
    directory_addr= os.getcwd()+'\\texts'
    files = os.listdir(directory_addr)
    result={'Mn': [], 'Mw':[], 'D':[]}

    for file in files:   
        f = open(directory_addr+'/'+file, "r")
        mn=None
        mw=None
        d=None



        for line in f.readlines():

            if 'Mn:' in line:
                mn=float(line.split(' ')[2].split('\t')[:-1][0])
            if 'Mw:' in line:
                mw=float(line.split(' ')[2].split('\t')[:-1][0])
            if 'D:' in line:
                d=float(line.split(' ')[2])

                
        result['D'].append(d)    
        result['Mn'].append(mn)    
        result['Mw'].append(mw)

    return result