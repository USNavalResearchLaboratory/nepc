import pdfplumber
import re
import sys
import os
import shutil
import numpy as np

def getPDF(pdfFilename):
    if (sys.platform == 'linux'):
        pdf = pdfplumber.open(pdfFilename)
    return pdf

def removeOutdir(outdir):
    ## Try to remove tree; if failed show an error using try...except on screen
    try:
        shutil.rmtree(outdir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

    try:
        os.mkdir(outdir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def getTableData(pdf,pageNumber,cropDimArray,locateTables=False,omitRegexp=''):
    pg = pdf.pages[pageNumber]
    #data = [[] for i in range(len(cropDimArray))]
    data = np.empty(shape=(0,2))
    for i in range(len(cropDimArray)):
        pgCropped = pg.crop(cropDimArray[i])
        if (locateTables):
            display(pgCropped.to_image().reset().draw_rects(pgCropped.chars))
        else:
            textSpaceDelim = pgCropped.extract_text().split("\n")
            for j in range(len(textSpaceDelim)):
                        if (omitRegexp == '' or not(bool(re.search(omitRegexp, textSpaceDelim[j])))):
                            textArray = textSpaceDelim[j].split(' ')
                            data=np.append(data,[[float(textArray[0]),
						  float(textArray[1])]],axis=0)
    return data

def writeDataToFile(dataArray,filename):
	f = open(filename, "x")
	for i in range(len(dataArray)): 
		f.write("\t"+str(dataArray[i,0])+"\t"+str(dataArray[i,1])+"\n")
	f.close()

def writeMetaDataToFile(filename,specie,process,units_e,units_sigma,ref,lhs='',rhs='',hv='',background='',lpu='',upu=''):
    f = open(filename, "x")
    f.write("\t".join(('',specie,process,str(units_e),str(units_sigma),ref,lhs,rhs,str(hv),background,str(lpu),str(upu))))
    f.close()


