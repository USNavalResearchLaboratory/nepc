"""Templates for curating cross section data from various sources (e.g. LxCAT).

Provides templates for curating raw and external (e.g. LxCAT) cross section data:

- parse and clean data (e.g. remove zeroes, set thresholds)
- augment the data (e.g. add additional metadata, create lumped cross sections)
- verify data
- write data to nepc formatted input files (i.e. .dat, .met, .mod)
"""
from abc import ABC, abstractmethod
from typing import List, Tuple
from nepc.util import util
from nepc.util import parser
import numpy as np
import re
import os


class CurateCS(ABC):
    """Template method that contains the skeleton for curating cross section data.
    """
    def curate(self, datadir: str, outdir: str, states: dict, title: str, units_e: str, units_sigma: str, augment_dicts=None, debug=False, **next_ids) -> None:
        """Skeleton of curation process.
        """
        filelist, next_cs_id, next_csdata_id = self.initialize(datadir, outdir, debug, **next_ids)
        csdata = self.get_csdata(filelist, debug=debug)
        csdata = self.clean_csdata(csdata, debug=debug)
        csdata = self.augment_csdata(csdata, outdir, states, title, units_e, units_sigma, augment_dicts)
        self.verify_csdata()
        next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)
        self.finalize(next_cs_id, next_csdata_id)


    def initialize(self, datadir: str, outdir: str, debug=False, **next_ids) -> Tuple[List[str], str, str]:

        def askYesNoQuestion(question):
            YesNoAnswer = input(question).upper()
            if YesNoAnswer == "Y" or YesNoAnswer == "N":
                return YesNoAnswer  
            else:
                return askYesNoQuestion(question)
         
        filelist = os.listdir(datadir)
        if len(filelist) > 0:
            for filenames in enumerate(filelist):
                answer = askYesNoQuestion(f'Process {filenames[1]}? (Y/N): ')
                if answer == "Y":
                    filelist[filenames[0]] = f'{datadir}/{filenames[1]}'
                    print(f'Added {filenames[1]} to queue.')
                elif answer == "N":
                    filelist.pop(filenames[0])
                    print(f'Skipping {filenames[1]}.')

        if len(filelist) == 0:
            print('No files to process. Exiting')
            exit
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
    def get_csdata(self):
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

    def value(self, csdata_i, key):
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
        print('\t'.join(keys))
        print('===============================================================================')
        for cs, i in zip(csdata, range(len(csdata))):
            print('\t'.join([self.value(cs, key) for key in keys]))

    def get_csdata(self, filelist, debug=False):
        csdata = []
        for datafile in filelist:
            csdata += parser.parse(datafile, debug=debug)
        if debug: print(f"Length of csdata: {len(csdata)}")
        return csdata

    def clean_csdata(self, csdata, debug=False):
        def remove_zeros_at_end(csdata):
            for cs in csdata:
                i = len(cs['data']) - 1
                while cs['data'][i][1] == 0.0:
                    if debug: print('removing {} from csdata[{}][\'data\']'.format(cs['data'][i], i))
                    cs['data'].pop(i)
                    i -= 1

        def remove_zeros_at_beginning(csdata):
            for cs in csdata:
                while cs['data'][0][1] == 0.0 and cs['data'][1][1] == 0.0:
                    if debug: print('removing {} from csdata[{}][\'data\']'.format(cs['data'], 0))
                    cs['data'].pop(0)
        remove_zeros_at_beginning(csdata)
        remove_zeros_at_end(csdata)
        keys = ['specie',
                'process',
                'units_e',
                'units_sigma',
                'lhs_a',
                'rhs_a',
                'lhs_v',
                'rhs_v',
                'threshold',
                'nepc_filename']
        
        return csdata


    def augment_csdata(self, csdata, outdir, states, title, units_e, units_sigma, augment_dicts=None):

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


    def finalize(self, next_cs_id, next_csdata_id) -> None:
        parser.write_next_id_to_file(next_cs_id, next_csdata_id)
        print(f'next_cs_id: {next_cs_id}\nnext_csdata_id: {next_csdata_id}')


    def __str__(self) -> str:
        return "LxCAT curation process"

def curate_client(curate_cs: CurateCS, datadir: str, outdir: str, states: dict, title: str, 
                  units_e: str, units_sigma: str, augment_dicts=None, debug=False, **next_ids) -> None:
    """Client code that calls the CurateCS template to execute the curation process.
    """

    print(f"Executing {curate_cs}.")
    
    curate_cs.curate(datadir, outdir, states, title, units_e, units_sigma, augment_dicts, debug, **next_ids)
