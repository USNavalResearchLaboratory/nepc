"""Templates for curating cross section data from various sources (e.g. LxCAT).

Provides templates for curating raw and external (e.g. LxCAT) cross section data:

- parse and clean data (e.g. remove zeroes, set thresholds)
- augment the data (e.g. add additional metadata, create lumped cross sections)
- verify data
- write data to nepc formatted input files (i.e. .dat, .met, .mod)
"""
from abc import ABC, abstractmethod
from typing import List, Tuple
import re
import os
import numpy as np
from nepc.util import util
from nepc.util import parser


class CurateCS(ABC):
    """Template method that contains the skeleton for curating cross section data.
    """
    def curate(self, datadir: str, outdir: str, title: str, units_e: str,
               units_sigma: str, augment_dicts=None, debug=False, **next_ids) -> None:
        """Skeleton of curation process.
        """
        filelist, next_cs_id, next_csdata_id = self.initialize(datadir, outdir, debug, **next_ids)
        csdata = self.get_csdata(filelist, debug=debug)
        csdata = self.clean_csdata(csdata, debug=debug)
        csdata = self.augment_csdata(csdata, outdir, title, units_e, units_sigma, augment_dicts)
        self.verify_csdata()
        next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)
        self.finalize(next_cs_id, next_csdata_id, debug)


    def initialize(self, datadir: str, outdir: str, debug=False,
                   **next_ids) -> Tuple[List[str], str, str]:
        """Initialize curation process.
        """
        def yes_or_no(question) -> bool:
            yes_no_answer = input(question + ' (Y|N) ').upper()
            if yes_no_answer == "Y" or yes_no_answer == "N":
                if yes_no_answer == "Y":
                    return True
                else:
                    return False
            else:
                return yes_or_no(question)

        filelist = os.listdir(datadir)
        if len(filelist) > 0:
            for filenames in enumerate(filelist):
                answer = yes_or_no(f'Process {filenames[1]}?')
                if answer:
                    filelist[filenames[0]] = f'{datadir}/{filenames[1]}'
                    print(f'Added {filenames[1]} to queue.')
                else:
                    filelist.pop(filenames[0])
                    print(f'Skipping {filenames[1]}.')

        if len(filelist) == 0:
            raise Exception('No files to process.')
        else:
            print(f'Files in queue: {filelist}')

        util.rmdir(outdir)
        util.mkdir(outdir)

        if debug:
            next_cs_id, next_csdata_id = (next_ids["next_cs_id"], next_ids["next_csdata_id"])
            print(f"next_cs_id: {next_cs_id}\nnext_csdata_id: {next_csdata_id}")
        else:
            next_cs_id, next_csdata_id = parser.get_next_ids()

        return filelist, next_cs_id, next_csdata_id


    @abstractmethod
    def get_csdata(self, filelist: str, debug=False):
        """Get cross section data for curation process.
        """

    @abstractmethod
    def clean_csdata(self, csdata: List[dict], debug=False) -> None:
        """Clean cross section data during curation process.
        """


    @abstractmethod
    def augment_csdata(self, csdata: List[dict], outdir: str,
                       title: str, units_e: str, units_sigma: str,
                       augment_dicts: List[List[dict]]) -> None:
        """Augment cross section data in curation process.
        """


    @abstractmethod
    def verify_csdata(self) -> None:
        """Verify cross setion data in curation process.
        """

    @abstractmethod
    def write_csdata(self, csdata: List[dict], next_cs_id: int, next_csdata_id: int) -> None:
        """Write cross section data to .dat, .met, and .mod files at end of curation process.
        """

    @abstractmethod
    def finalize(self, next_cs_id: int, next_csdata_id: int, debug=False) -> None:
        """Finalize cross section data curation process.
        """


class CurateLxCAT(CurateCS):
    """Template for curating LxCAT cross section data

    Parameters
    ----------
    CurateCS : [type]
        [description]
    """

    def value(self, csdata_i, key):
        """Provide cross section data as strings. Provide default
        values for certain cross section data types.
        """
        float_keys = ['threshold']
        int_keys = ['lhs_v', 'rhs_v']

        if key in csdata_i.keys():
            if csdata_i[key] == '':
                if key in float_keys or key in int_keys:
                    return '-1'
                else:
                    return '\\N'
            else:
                return str(csdata_i[key])
        else:
            if key in float_keys or key in int_keys:
                return '-1'
            else:
                return '\\N'

    def print_csdata_table(self, keys, csdata):
        """Print cross section data for debugging.
        """
        print('\t'.join(keys))
        print('===============================================================================')
        for cs in csdata:
            print('\t'.join([self.value(cs, key) for key in keys]))

    def get_csdata(self, filelist, debug=False):
        """Get cross section data from LxCAT formatting text file.
        """
        csdata = []
        for datafile in filelist:
            csdata += parser.parse(datafile, debug=debug)
        if debug:
            print(f"Length of csdata: {len(csdata)}")
        return csdata

    def clean_csdata(self, csdata, debug=False):
        """Clean LxCAT cross section data during curation process.
        """
        def remove_zeros(csdata):
            """Remove data points from cross section data with zero cross section.
            """
            for cs in csdata:
                i = len(cs['data']) - 1
                while cs['data'][i][1] == 0.0:
                    if debug:
                        print('removing {} from csdata[{}][\'data\']'.format(cs['data'][i], i))
                    cs['data'].pop(i)
                    i -= 1

                while cs['data'][0][1] == 0.0 and cs['data'][1][1] == 0.0:
                    if debug:
                        print('removing {} from csdata[{}][\'data\']'.format(cs['data'], 0))
                    cs['data'].pop(0)

        remove_zeros(csdata)

        return csdata


    def augment_csdata(self, csdata, outdir, title, units_e, units_sigma,
                       augment_dicts=None):

        for cs, i in zip(csdata, range(len(csdata))):

            cs['specie'] = self.value(cs, 'target')
            cs['units_e'] = units_e
            cs['units_sigma'] = units_sigma
            cs['background'] = self.value(cs, 'comment')
            cs['nepc_filename'] = outdir + '/' + title + '_' + str(i)
            cs['data'] = np.asarray(cs['data'])
            cs['ref'] = self.value(cs, 'ref')
            cs['threshold'] = self.value(cs, 'threshold')
            cs['lhs_v'] = self.value(cs, 'lhs_v')
            cs['rhs_v'] = self.value(cs, 'rhs_v')

            if augment_dicts is not None:
                for cs_dict, augment_dict in augment_dicts:
                    matched = True
                    for key in cs_dict:
                        if matched and key in cs and re.search(cs_dict[key], cs[key]) is None:
                            matched = False
                    if matched:
                        for key in augment_dict.keys():
                            cs[key] = augment_dict[key]

        return csdata

    def verify_csdata(self) -> None:
        pass

    def write_csdata(self, csdata, next_cs_id, next_csdata_id):
        for cs in csdata:
            next_csdata_id = parser.write_data_to_file(data_array=cs['data'],
                                                       filename=cs['nepc_filename']+'.dat',
                                                       start_csdata_id=next_csdata_id)
            next_cs_id = parser.write_metadata_to_file(filename=cs['nepc_filename']+'.met',
                                                       cs_id=next_cs_id,
                                                       specie=cs['specie'],
                                                       process=cs['process'],
                                                       lhs_a=cs['lhs_a'],
                                                       rhs_a=cs['rhs_a'],
                                                       lhs_v=cs['lhs_v'],
                                                       rhs_v=cs['rhs_v'],
                                                       units_e=cs['units_e'],
                                                       units_sigma=cs['units_sigma'],
                                                       threshold=cs['threshold'],
                                                       ref=cs['ref'],
                                                       background=cs['background'])
            parser.write_models_to_file(filename=cs['nepc_filename']+'.mod',
                                        models_array=cs['models'])
        return next_cs_id, next_csdata_id


    def finalize(self, next_cs_id, next_csdata_id, debug=False) -> None:
        if not debug:
            parser.write_next_id_to_file(next_cs_id, next_csdata_id)
        print(f'next_cs_id: {next_cs_id}\nnext_csdata_id: {next_csdata_id}')


    def __str__(self) -> str:
        return "LxCAT curation process"

def curate_client(curate_cs: CurateCS, datadir: str, outdir: str, title: str,
                  units_e: str, units_sigma: str, augment_dicts=None,
                  debug=False, **next_ids) -> None:
    """Client code that calls the CurateCS template to execute the curation process.
    """
    print(f"Executing {curate_cs}.")

    curate_cs.curate(datadir, outdir, title, units_e, units_sigma, augment_dicts, debug, **next_ids)
