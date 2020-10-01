"""Templates for curating cross section data from various sources (e.g. LxCAT).

Provides templates for curating raw and external (e.g. LxCAT) cross section data:

- parse and clean data (e.g. remove zeroes, set thresholds)
- augment the data (e.g. add additional metadata, create lumped cross sections)
- verify data
- write data to nepc formatted input files (i.e. .dat, .met, .mod)
"""
from abc import ABC, abstractclassmethod, abstractmethod


class CurateCS(ABC):
    """Template method that contains the skeleton for curating cross section data.
    """


    def curate(self) -> None:
        """Skeleton of curation process.
        """

        self.initialize()
        self.get_csdata()
        self.clean_csdata()
        self.augment_csdata()
        self.verify_csdata()
        self.write_csdata()
        self.finalize()


    @abstractmethod
    def initialize(self) -> None:
        pass


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

    def initialize(self) -> None:
        pass


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

def curate_client(curate_cs: CurateCS) -> None:
    """Client code that calls the CurateCS template to execute the curation process.
    """

    print(f"Executing {curate_cs}.")
    curate_cs.curate()
