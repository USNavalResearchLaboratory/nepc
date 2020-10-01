"""Templates for curating cross section data from various sources (e.g. LxCAT).

Provides templates for curating raw and external (e.g. LxCAT) cross section data:

- parse and clean data (e.g. remove zeroes, set thresholds)
- augment the data (e.g. add additional metadata, create lumped cross sections)
- verify data
- write data to nepc formatted input files (i.e. .dat, .met, .mod)
"""
from abc import ABC, abstractclassmethod, abstractmethod
from typing import List, Tuple
from nepc.util import util
from nepc.util import parser

class CurateCS(ABC):
    """Template method that contains the skeleton for curating cross section data.
    """



    def curate(self, datadir: str, outdir: str) -> Tuple[List[str], str, str]:
        """Skeleton of curation process.
        """
        datafiles, next_cs_id, next_csdata_id = self.initialize(datadir, outdir)
        self.get_csdata()
        self.clean_csdata()
        self.augment_csdata()
        self.verify_csdata()
        self.write_csdata()
        self.finalize()
        return datafiles, next_cs_id, next_csdata_id

    def initialize(self, datadir: str, outdir: str) -> Tuple[List[str], str, str]:
        datafiles = [datadir + '/Phelps.txt']

        util.rmdir(outdir)
        util.mkdir(outdir)

        debug = True

        if debug:
            next_cs_id, next_csdata_id = (424, 202224)
        else:
            next_cs_id, next_csdata_id = parser.get_next_ids()

        return datafiles, next_cs_id, next_csdata_id




    @abstractmethod
    def get_csdata(self) -> None:
        pass

    @abstractmethod
    def clean_csdata(self) -> None:
        pass


    @abstractmethod
    def augment_csdata(self) -> None:
        pass


    @abstractmethod
    def verify_csdata(self) -> None:
        pass

    @abstractmethod
    def write_csdata(self) -> None:
        pass

    @abstractmethod
    def finalize(self) -> None:
        pass


class CurateLxCAT(CurateCS):
    """Template for curating LxCAT cross section data

    Parameters
    ----------
    CurateCS : [type]
        [description]
    """

    def get_csdata(self) -> None:
        pass

    def clean_csdata(self) -> None:
        pass


    def augment_csdata(self) -> None:
        pass


    def verify_csdata(self) -> None:
        pass

    def write_csdata(self) -> None:
        pass

    def finalize(self) -> None:
        pass


    def __str__(self) -> str:
        return "LxCAT curation process"

def curate_client(curate_cs: CurateCS, datadir: str, outdir: str) -> Tuple[List[str], str, str]:
    """Client code that calls the CurateCS template to execute the curation process.
    """

    print(f"Executing {curate_cs}.")
    datafiles, next_cs_id, next_csdata_id = curate_cs.curate(datadir, outdir)
    return datafiles, next_cs_id, next_csdata_id

