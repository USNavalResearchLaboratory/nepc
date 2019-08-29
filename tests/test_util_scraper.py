"""Verify whether the functions in scraper.py in the nepc module
work as intended"""
from os import path
import pdfplumber
import numpy as np
from nepc.util import scraper
from nepc.util import config

def test_wc_fxn():
    """Verify that the number of lines
    in a function is returned correctly
    in scraper.wc_fxn"""
    fil = open("example.txt", "w+")
    fil_length = 10
    for i in range(0, fil_length):
        fil.write("an example" + str(i) + "\n")
    fil.close()
    assert isinstance(scraper.wc_fxn("example.txt"), int)
    assert scraper.wc_fxn("example.txt") == fil_length

def test_get_pdf():
    """Verify that get_pdf returns an instance of the
    pdfplumber.PDF class"""
    pdf_filen = config.nepc_home() + '/ref/angus/16_29_buckman_2003.pdf'
    assert isinstance(scraper.get_pdf(pdf_filen), pdfplumber.PDF)
def test_rmfile():
    """Verify that a file that
    exists is removed by scraper.rmfile"""
    scraper.rmfile("example.txt")
    assert not path.exists("example.txt")

def test_mkdir_rmdir():
    """Verify that scraper.mkdir produces a directory and
    scraper.rmdir removes a directory"""
    scraper.mkdir(config.nepc_home() + "/test_mkdir")
    assert path.exists(config.nepc_home() + "/test_mkdir")
    scraper.rmdir(config.nepc_home() + "/test_mkdir")
    assert not path.exists(config.nepc_home() + "/test_mkdir")

def test_get_column_strings():
    """Verify that get_column_strings returns a list"""
    pdfex = scraper.get_pdf(config.nepc_home() + "/ref/angus/" + "20_zipf_et_al-" +
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
