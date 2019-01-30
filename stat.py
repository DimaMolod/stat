#!/usr/bin/env python
# coding: utf-8

import numpy as np
import saxsdocument
import os
import sys
import glob
import time

start_time = time.time()
def main(outFileName, *args):
    #args = glob.glob("data/*.dat")
    Is = np.array([])
    s = np.array([])
    lenS = []
    i = 0
    for file in args:
        if outFileName in file:
            continue
        doc = saxsdocument.read(file)
        dat = np.transpose(np.array(doc.curve[0]))
        i+=1
        if i == 1:
            s = dat[0]
            Is = dat[1]
        else:
            scat_vector = dat[0]
            intensity = dat[1]
            Is = np.vstack((Is,intensity))
            s = np.vstack((s,scat_vector))
            lenS.append(len(scat_vector))

    np.info(Is)
    In = np.transpose(Is)
    sPoints= Is.shape[1]
    len_n =min(lenS)
    mean_i = np.zeros(sPoints)
    stdv_i = np.zeros(sPoints)

    i=0
    for n in range(0, sPoints):
        av_i = np.mean(In[n])
        st_i = np.std(In[n])
        #av_i = sum(In[n])
        mean_i[i]=av_i
        stdv_i[i]=st_i
        i+=1

    mean_dat = np. vstack((s[0], mean_i, stdv_i))

    np.savetxt(outFileName,np.transpose(mean_dat), fmt='%f')

    print ("Averaged file is written..."+outFileName)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SyntaxError("Insufficient arguments")
    else:
        args = iter(sys.argv)
        isArgument = False
        for arg in args:
            if "=" in arg:
                a = arg.split("=")[0]
                n = arg.split("=")[1]
                if (a == "-o"):
                    main(n, *sys.argv[2:])
                    isArgument = True
        if (isArgument == False):
            main("mean.dat", *sys.argv[2:])
