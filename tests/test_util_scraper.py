"""Verify whether the functions in scraper.py in the nepc module
work as intended"""
import os
import pdfplumber
import numpy as np
from nepc.util import scraper
from nepc.util import config

NEPC_HOME = config.nepc_home()


def test_wc_fxn():
    """Verify that scraper.wc_fxn returns the number of lines
    in a file"""
    filename = "temp.txt"
    f = open(filename, "w+")
    f_length = 10
    for i in range(0, f_length):
        f.write("a temp " + str(i) + "\n")
    f.close()
    assert isinstance(scraper.wc_fxn(filename), int)
    assert scraper.wc_fxn(filename) == f_length
    os.remove(filename)


def test_get_pdf():
    """Verify that get_pdf returns an instance of the
    pdfplumber.PDF class"""
    pdf_file = NEPC_HOME + '/ref/angus/16_29_buckman_2003.pdf'
    assert isinstance(scraper.get_pdf(pdf_file), pdfplumber.PDF)


def test_rmfile():
    """Verify that a file that
    exists is removed by scraper.rmfile"""
    filename = "temp.txt"
    with open(filename, 'a'):
        os.utime(filename, None)
    assert os.path.exists(filename)
    scraper.rmfile(filename)
    assert not os.path.exists(filename)


def test_mkdir_rmdir():
    """Verify that scraper.mkdir produces a directory and
    scraper.rmdir removes a directory"""
    testdir = NEPC_HOME + "/tests/testdir"
    scraper.mkdir(testdir)
    assert os.path.exists(testdir)
    scraper.rmdir(testdir)
    assert not os.path.exists(testdir)


def test_get_column_strings():
    """Verify that get_column_strings returns a list"""
    pdfex = scraper.get_pdf(NEPC_HOME + "/ref/angus/" + "20_zipf_et_al-" +
                            "1980-Journal_of_Geophysical_Research__Space_" +
                            "Physics.pdf")
    crop_dim_x = [120, 150, 180, 480]
    data_l = scraper.get_column_strings(pdf=pdfex, page_number=6,
                                        crop_dim_array=crop_dim_x)
    assert isinstance(data_l, list)


def test_text_array_to_float_array():
    """Verify that scraper.text_array_to_float_array returns an
    array of floats, converted from an array of strings"""
    text_array = np.array(['5.3', '2.9', '8.7', '5.4', '9.2', '3.3'])
    float_array = scraper.text_array_to_float_array(text_array)
    assert isinstance(float_array, np.ndarray)
