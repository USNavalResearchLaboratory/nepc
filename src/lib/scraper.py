import pdfplumber
import re
import os
import shutil
import numpy as np
from IPython import display


def getPDF(pdfFilename):
    return pdfplumber.open(pdfFilename)


def rmdir(outdir):
    # Try to remove tree; if failed show an error using try...except on screen
    try:
        shutil.rmtree(outdir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def rmfile(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(filename + " does not exist")


def mkdir(outdir):
    try:
        os.mkdir(outdir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def getTableData(pdf, pageNumber, cropDimArray,
                 locateTables=False, omitRegexp=''):
    pg = pdf.pages[pageNumber]
    # data = [[] for i in range(len(cropDimArray))]
    data = np.empty(shape=(0, 2))
    for i in range(len(cropDimArray)):
        pgCropped = pg.crop(cropDimArray[i])
        if (locateTables):
            display(pgCropped.to_image().reset().draw_rects(pgCropped.chars))
        else:
            textSpaceDelim = pgCropped.extract_text().split("\n")
            for j in range(len(textSpaceDelim)):
                if (omitRegexp == '' or not(
                        bool(re.search(omitRegexp, textSpaceDelim[j])))):
                    textArray = textSpaceDelim[j].split(' ')
                    data = np.append(data, [[float(textArray[0]),
                                             float(textArray[1])]], axis=0)
    return data


def get_column_data(pdf, pageNumber, cropDimArray,
                    locateTables=False, omitRegexp=''):
    pg = pdf.pages[pageNumber]
    data = np.empty(shape=(0, 1))
    for i in range(len(cropDimArray)):
        pgCropped = pg.crop(cropDimArray[i])
        if (locateTables):
            display(pgCropped.to_image().reset().draw_rects(pgCropped.chars))
        else:
            textSpaceDelim = pgCropped.extract_text().split("\n")
            for j in range(len(textSpaceDelim)):
                if (omitRegexp == '' or not(
                        bool(re.search(omitRegexp, textSpaceDelim[j])))):
                    data = np.append(
                        data, [[float(textSpaceDelim[j])]],
                        axis=0)
    return data


def textArrayToFloatArray(textArray, omitRegexp=''):
    data = np.empty(shape=(0, 1))
    for i in range(len(textArray)):
        if (omitRegexp == '' or not(
                bool(re.search(omitRegexp, textArray[i])))):
            data = np.append(data, [[float(textArray[i])]], axis=0)
    return data


def getColumnStrings(pdf, pageNumber, cropDimArray,
                     locateTables=False, omitRegexp=''):
    pg = pdf.pages[pageNumber]
    data = []
    pgCropped = pg.crop(cropDimArray)
    if (locateTables):
        display(pgCropped.to_image().reset().draw_rects(pgCropped.chars))
    else:
        textSpaceDelim = pgCropped.extract_text().split("\n")
        for j in range(len(textSpaceDelim)):
            if (omitRegexp == '' or not(
                    bool(re.search(omitRegexp, textSpaceDelim[j])))):
                # textArray = textSpaceDelim[j].split(' ')
                # data.append([textArray[0], textArray[1]])
                data.append(textSpaceDelim[j])
    return data


# TODO: standardize filenames; build them in the write functions
def writeDataToFile(dataArray, filename):
    f = open(filename, "x")
    for i in range(len(dataArray)):
        f.write("\t"+str(dataArray[i, 0])+"\t"+str(dataArray[i, 1])+"\n")
    f.close()


def writeMetaDataToFile(
        filename, specie, process, units_e, units_sigma, ref, lhsA='\\N',
        lhsB='\\N', rhsA='\\N', rhsB='\\N', wavelength='\\N', lhs_v='\\N',
        rhs_v='\\N', lhs_j='\\N', rhs_j='\\N', background='\\N', lpu='\\N',
        upu='\\N'):
    f = open(filename, "x")
    f.write(
        "\t".join(
            ('',
             specie,
             process,
             str(units_e),
             str(units_sigma),
             ref,
             lhsA,
             lhsB,
             rhsA,
             rhsB,
             str(wavelength),
             str(lhs_v),
             str(rhs_v),
             str(lhs_j),
             str(rhs_j),
             background,
             str(lpu),
             str(upu))))
    f.close()


def writeCSToFile(
        filename, dataArray, specie, process, units_e, units_sigma, ref,
        lhsA='\\N', lhsB='\\N', rhsA='\\N', rhsB='\\N', wavelength='\\N',
        lhs_v='\\N', rhs_v='\\N', lhs_j='\\N', rhs_j='\\N', background='\\N',
        lpu='\\N', upu='\\N'):
    writeDataToFile(dataArray, filename+".dat")
    writeMetaDataToFile(filename+".met", specie, process, units_e, units_sigma,
                        ref, lhsA, lhsB, rhsA, rhsB, wavelength, lhs_v, rhs_v,
                        lhs_j, rhs_j, background, lpu, upu)


def writeModelsToFile(filename, modelsArray):
    f = open(filename, "x")
    for i in range(len(modelsArray)):
        f.write(str(modelsArray[i])+"\n")
    f.close()
