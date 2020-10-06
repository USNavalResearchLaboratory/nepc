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
import math
import numpy as np
import pandas as pd
import nepc
from nepc.util import util
from nepc.util import parser


class CurateCS(ABC):
    """Template method that contains the skeleton for curating cross section data.
    """
    @abstractmethod
    def curate(self, datadir: str, datatype: str, species: str, title: str, units_e: str,
               units_sigma: str, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Main driver for curation process.
        """

    def initialize_db(self, initialize_nepc=False, test=False, debug=False,
                      next_cs_id=None, next_csdata_id=None) -> Tuple[int]:
        """Initialize the nepc database and get the next cs and csdata IDs
        """
        if test:
            test_str = "test "
        else:
            test_str = ""

        if initialize_nepc and debug:
            raise Exception(f'You tried to initialize NEPC {test_str}database with debug info.')

        if initialize_nepc:
            init_answer = util.yes_or_no(f'Are you sure you want to '
                                         f'initialize the NEPC {test_str}database?')
            if init_answer:
                parser.write_next_id_to_file(1, 1, test)

        if not debug:
            next_cs_id, next_csdata_id = parser.get_next_ids(test)

        print(f"next_cs_id: {next_cs_id}\nnext_csdata_id: {next_csdata_id}")
        return next_cs_id, next_csdata_id


    def initialize_input(self, datadir: str, datatype: str, species: str,
                         title: str) -> List[str]:
        """Initialize input filelist for curation processes that read data from files.
        """
        filedir = f'{datadir}/raw/{datatype}/{species}/{title}'
        filelist = util.get_filelist(filedir)
        if len(filelist) == 0:
            raise Exception('No files to process.')
        else:
            print(f'Files in queue: {filelist}')
        return filelist

    def initialize_output(self, datadir: str, species: str, title: str) -> str:
        """Initialize output directory for curation process
        """
        outdir = f'{datadir}/cs/{species}/{title}'
        util.rmdir(outdir)
        util.mkdir(outdir)
        return outdir


    @abstractmethod
    def get_csdata(self) -> None:
        """Get cross section data for curation process.
        """

    def clean_csdata(self) -> None:
        """Clean cross section data during curation process.
        """


    def augment_csdata(self) -> None:
        """Augment cross section data in curation process.
        """


    @abstractmethod
    def verify_csdata(self) -> None:
        """Verify cross setion data in curation process.
        """

    def write_csdata(self, csdata: List[dict], next_cs_id: int, next_csdata_id: int):
        """Write cross section data to .dat, .met, and .mod files at end of curation process.
        """
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


    def finalize(self, next_cs_id: int, next_csdata_id: int, test=False, debug=False) -> None:
        """Finalize cross section data curation process.
        """
        if not debug:
            parser.write_next_id_to_file(next_cs_id, next_csdata_id, test)
        print(f'next_cs_id: {next_cs_id}\nnext_csdata_id: {next_csdata_id}')


class CurateLxCAT(CurateCS):
    """Template for curating LXCat cross section data

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

    def curate(self, datadir: str, datatype: str, species: str, title: str, units_e: str,
               units_sigma: str, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Curation driver function for LXCat text files.
        """
        next_cs_id, next_csdata_id = self.initialize_db(initialize_nepc, test,
                                                        debug, next_cs_id, next_csdata_id)
        filelist = self.initialize_input(datadir, datatype, species, title)
        outdir = self.initialize_output(datadir, species, title)
        csdata = self.get_csdata(filelist, debug=debug)
        csdata = self.clean_csdata(csdata, debug=debug)
        csdata = self.augment_csdata(csdata, outdir, title, units_e, units_sigma, augment_dicts)
        self.verify_csdata()
        next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)
        self.finalize(next_cs_id, next_csdata_id, test, debug)

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


    def __str__(self) -> str:
        return "LXCat cross section curation"

    @property
    def datatype(self) -> str:
        """Provide data type for curation process
        """
        return "lxcat"

class CurateLumped(CurateCS):
    """Template for creating lumped cross sections from cross sections already
    in the database.
    """
    def log_interp(self, zz, xx, yy):
        logz = np.log10(zz)
        logx = np.log10(xx)
        logy = np.log10(yy)
        return np.power(10.0, np.interp(logz, logx, logy, right=-1000.0))

    def lump(self, csdata):
        min_e = np.Inf
        max_e = -np.Inf
        for cs in csdata:
            min_e = min(min_e, np.min(cs.data['e']))
            max_e = max(max_e, np.max(cs.data['e']))
        print(f'min_e: {min_e}')
        print(f'max_e: {max_e}')

        e_range_low = math.floor(math.log10(min_e))
        e_range_high = math.ceil(math.log10(max_e))
        print(f'e_range_low: {e_range_low}')
        print(f'e_range_high: {e_range_high}')

        e_range = np.logspace(e_range_low, e_range_high, (e_range_high - e_range_low) * 100 + 1)

        sigma = [0.0 for _ in range(len(e_range))]
        for e, i in zip(e_range, range(len(e_range))):    
            for cs in csdata:
                sigma_i = self.log_interp(e, cs.data['e'], cs.data['sigma'])
                if ~np.isnan(sigma_i):
                    sigma[i] += sigma_i
        sigma_nan = np.isnan(sigma)
        sigma = np.array(sigma)
        e_range = e_range[~sigma_nan]
        sigma = sigma[~sigma_nan]
        eps = 1.0E-24
        sigma[np.abs(sigma) < eps] = 0.0
        #csdata_lumped = {'e': e_range,
        #                 'sigma': sigma}
        csdata_lumped = np.asarray([[e_i, sigma_i] for e_i, sigma_i in zip(e_range, sigma)])
        return csdata_lumped


    def unique_metadata(self, csdata, key):
        return list(set([cs.metadata[key] for cs in csdata]))


    def metadata_match(self, csdata, key):
        return [True] * (len(csdata) - 1) == [csdata[i-1].metadata[key] == csdata[i].metadata[key] for i in range(1, len(csdata))]

    def check_for_unmatched_metadata(self, csdata, keys):
        unmatched_metadata = []
        for key in keys:
            if not self.metadata_match(csdata, key):
                unmatched_metadata.append(str(key))
        if len(unmatched_metadata) > 0:
            raise Exception(f"Trying to lump cross sections with unmatched "
                            f"{' and '.join(unmatched_metadata)}.")


    def curate(self, datadir: str, datatype: str, species: str, title: str, units_e: str,
               units_sigma: str, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Curation driver function for lumped cross sections.
        """
        next_cs_id, next_csdata_id = self.initialize_db(initialize_nepc, test,
                                                        debug, next_cs_id, next_csdata_id)
        outdir = self.initialize_output(datadir, species, title)
        csdata = self.get_csdata(cs_ids)
        csdata_lumped = self.augment_csdata(csdata, outdir, title,
                                            units_e, units_sigma, augment_dicts, debug)
        self.verify_csdata()
        #next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)

        phelps_min_excitation_total = nepc.CustomCS(metadata={'specie': 'N2',
                                                              'process': 'excitation_total',
                                                              'units_e': 1.0,
                                                              'units_sigma': 1.0,
                                                              'ref': '\\N',
                                                              'lhsA': 'N2(X1Sigmag+)',
                                                              'lhsB': None,
                                                              'rhsA': 'N2*',
                                                              'rhsB': None,
                                                              'threshold': 0.02,
                                                              'wavelength': -1.0,
                                                              'lhs_v': -1,
                                                              'rhs_v': -1,
                                                              'lhs_j': -1,
                                                              'rhs_j': -1,
                                                              'background': 'Sum of excitations (electronic, vibrational, and rotational) in Phelps complete model.',
                                                              'lpu': -1.0,
                                                              'upu': -1.0,
                                                              'lhsA_long': 'N${}_2$ (X ${}^1\\Sigma_g^+$)',
                                                              'lhsB_long': None,
                                                              'rhsA_long': 'N${}_2^*$',
                                                              'rhsB_long': None,
                                                              'e_on_lhs': 1,
                                                              'e_on_rhs': 1,
                                                              'hv_on_lhs': 0,
                                                              'hv_on_rhs': 0,
                                                              'v_on_lhs': 0,
                                                              'v_on_rhs': 0,
                                                              'j_on_lhs': 0,
                                                              'j_on_rhs': 0},
                                                    data=csdata_lumped)

        
        cs_name = outdir + '/phelps_min_excitation_total'
        next_csdata_id = parser.write_data_to_file(data_array=csdata_lumped,
                                                   filename=cs_name+'.dat',
                                                   start_csdata_id=next_csdata_id)
        next_cs_id = parser.write_metadata_to_file(filename=cs_name+'.met',
                                                   cs_id=next_cs_id,
                                                   specie=phelps_min_excitation_total.metadata['specie'],
                                                   process=phelps_min_excitation_total.metadata['process'],
                                                   lhs_a=phelps_min_excitation_total.metadata['lhsA'],
                                                   rhs_a=phelps_min_excitation_total.metadata['rhsA'],
                                                   lhs_v=phelps_min_excitation_total.metadata['lhs_v'],
                                                   rhs_v=phelps_min_excitation_total.metadata['rhs_v'],
                                                   units_e=phelps_min_excitation_total.metadata['units_e'],
                                                   units_sigma=phelps_min_excitation_total.metadata[
                                                       'units_sigma'],
                                                   threshold=phelps_min_excitation_total.metadata['threshold'],
                                                   ref=phelps_min_excitation_total.metadata['ref'],
                                                   background=phelps_min_excitation_total.metadata['background'])
        parser.write_models_to_file(filename=cs_name+'.mod',
                                    models_array=['phelps', 'phelps_min'])
        #self.finalize(next_cs_id, next_csdata_id, test, debug)

        cnx, cursor = nepc.connect(local=True)
        
        n_phelps_excitation_e_j = nepc.CustomModel(cursor, "phelps", metadata={'process': 'excitation'})
        
        n_phelps_excitation_e = n_phelps_excitation_e_j.cs[2:]
        
        n_phelps_excitation_j = n_phelps_excitation_e_j.cs[1]
        
        n_phelps_excitation_v = nepc.CustomModel(cursor, "phelps", metadata={'process': 'excitation_v'})
       
        csdata_lumped = self.lump(n_phelps_excitation_e)
        phelps_min2_excitation_total_e = nepc.CustomCS(metadata={'specie': 'N2',
                                                             'process': 'excitation_total',
                                                             'units_e': 1.0,
                                                             'units_sigma': 1.0,
                                                             'ref': '\\N',
                                                             'lhsA': 'N2(X1Sigmag+)',
                                                             'lhsB': None,
                                                             'rhsA': 'N2*',
                                                             'rhsB': None,
                                                             'threshold': 6.17,
                                                             'wavelength': -1.0,
                                                             'lhs_v': -1,
                                                             'rhs_v': -1,
                                                             'lhs_j': -1,
                                                             'rhs_j': -1,
                                                             'background': 'Sum of electronic excitations in Phelps complete model.',
                                                             'lpu': -1.0,
                                                             'upu': -1.0,
                                                             'lhsA_long': 'N${}_2$ (X ${}^1\\Sigma_g^+$)',
                                                             'lhsB_long': None,
                                                             'rhsA_long': 'N${}_2^*$',
                                                             'rhsB_long': None,
                                                             'e_on_lhs': 1,
                                                             'e_on_rhs': 1,
                                                             'hv_on_lhs': 0,
                                                             'hv_on_rhs': 0,
                                                             'v_on_lhs': 0,
                                                             'v_on_rhs': 0,
                                                             'j_on_lhs': 0,
                                                             'j_on_rhs': 0},
                                                    data={'e': list(range(100)),
                                                          'sigma': list(range(100))})
        
        
        cs_name = outdir + '/phelps_min2_excitation_total_e'
        next_csdata_id = parser.write_data_to_file(data_array=csdata_lumped,
                                                    filename=cs_name+'.dat',
                                                    start_csdata_id=next_csdata_id)
        next_cs_id = parser.write_metadata_to_file(filename=cs_name+'.met',
                                                    cs_id=next_cs_id,
                                                    specie=phelps_min2_excitation_total_e.metadata['specie'],
                                                    process=phelps_min2_excitation_total_e.metadata['process'],
                                                    lhs_a=phelps_min2_excitation_total_e.metadata['lhsA'],
                                                    rhs_a=phelps_min2_excitation_total_e.metadata['rhsA'],
                                                    lhs_v=phelps_min2_excitation_total_e.metadata['lhs_v'],
                                                    rhs_v=phelps_min2_excitation_total_e.metadata['rhs_v'],
                                                    units_e=phelps_min2_excitation_total_e.metadata['units_e'],
                                                    units_sigma=phelps_min2_excitation_total_e.metadata['units_sigma'],
                                                    threshold=phelps_min2_excitation_total_e.metadata['threshold'],
                                                    ref=phelps_min2_excitation_total_e.metadata['ref'],
                                                    background=phelps_min2_excitation_total_e.metadata['background'])
        parser.write_models_to_file(filename=cs_name+'.mod',
                                     models_array=['phelps', 'phelps_min2', 'phelps_min2_dr'])
        
        
        csdata_lumped = self.lump(n_phelps_excitation_v.cs)
        
        phelps_min2_excitation_total_v = nepc.CustomCS(metadata={'specie': 'N2',
                                                             'process': 'excitation_total',
                                                             'units_e': 1.0,
                                                             'units_sigma': 1.0,
                                                             'ref': '\\N',
                                                             'lhsA': 'N2(X1Sigmag+)',
                                                             'lhsB': None,
                                                             'rhsA': 'N2(X1Sigmag+)_v1-8)',
                                                             'rhsB': None,
                                                             'threshold': 0.29,
                                                             'wavelength': -1.0,
                                                             'lhs_v': -1,
                                                             'rhs_v': -1,
                                                             'lhs_j': -1,
                                                             'rhs_j': -1,
                                                             'background': 'Sum of vibrational excitations for N2(X) state in Phelps complete model.',
                                                             'lpu': -1.0,
                                                             'upu': -1.0,
                                                             'lhsA_long': 'N${}_2$ (X ${}^1\\Sigma_g^+$)',
                                                             'lhsB_long': None,
                                                             'rhsA_long': 'N${}_2$ (X ${}^1\Sigma_g^+ v=(1-8)$)',
                                                             'rhsB_long': None,
                                                             'e_on_lhs': 1,
                                                             'e_on_rhs': 1,
                                                             'hv_on_lhs': 0,
                                                             'hv_on_rhs': 0,
                                                             'v_on_lhs': 0,
                                                             'v_on_rhs': 0,
                                                             'j_on_lhs': 0,
                                                             'j_on_rhs': 0},
                                                    data={'e': list(range(100)),
                                                          'sigma': list(range(100))})

        cs_name = outdir + '/phelps_min2_excitation_total_v'
        next_csdata_id = parser.write_data_to_file(data_array=csdata_lumped,
                                                    filename=cs_name+'.dat',
                                                    start_csdata_id=next_csdata_id)
        next_cs_id = parser.write_metadata_to_file(filename=cs_name+'.met',
                                                    cs_id=next_cs_id,
                                                    specie=phelps_min2_excitation_total_v.metadata['specie'],
                                                    process=phelps_min2_excitation_total_v.metadata['process'],
                                                    lhs_a=phelps_min2_excitation_total_v.metadata['lhsA'],
                                                    rhs_a=phelps_min2_excitation_total_v.metadata['rhsA'],
                                                    lhs_v=phelps_min2_excitation_total_v.metadata['lhs_v'],
                                                    rhs_v=phelps_min2_excitation_total_v.metadata['rhs_v'],
                                                    units_e=phelps_min2_excitation_total_v.metadata['units_e'],
                                                    units_sigma=phelps_min2_excitation_total_v.metadata['units_sigma'],
                                                    threshold=phelps_min2_excitation_total_v.metadata['threshold'],
                                                    ref=phelps_min2_excitation_total_v.metadata['ref'],
                                                    background=phelps_min2_excitation_total_v.metadata['background'])
        parser.write_models_to_file(filename=cs_name+'.mod',
                                     models_array=['phelps', 'phelps_min2', 'phelps_min2_dr'])
        

        self.finalize(next_cs_id, next_csdata_id, test, debug)


    def get_csdata(self, cs_ids) -> List[dict]:
        cnx, cursor = nepc.connect(local=True)
        csdata = nepc.CustomModel(cursor, cs_id_list=cs_ids).cs
        return csdata


    def augment_csdata(self, csdata, outdir, title, units_e, units_sigma,
                       augment_dicts=None, debug=False):

        self.check_for_unmatched_metadata(csdata, ['specie', 'units_e', 'units_sigma'])

        lumped_metadata = dict()
        for key in ['specie', 'units_e', 'units_sigma', 'ref']:
            lumped_metadata[key] = self.unique_metadata(csdata, key)
            if debug:
                print(f'lumped_metadata[{key}]: {lumped_metadata[key]}')
        
        for _, (key, value) in enumerate(augment_dicts.items()):
            lumped_metadata[key] = value
            if debug:
                print(f'lumped_metadata[{key}]: {lumped_metadata[key]}')
        
        csdata = self.lump(csdata)
        return csdata

    def verify_csdata(self) -> None:
        pass

    def __str__(self) -> str:
        return "Lumped cross section curation"

    @property
    def datatype(self) -> str:
        return "lumped"


def curate_client(curate_cs: CurateCS, datadir: str, species: str, title: str,
                  units_e: str, units_sigma: str, augment_dicts=None,
                  initialize_nepc=False, test=False,
                  debug=False, next_cs_id=None, next_csdata_id=None,
                  cs_ids=None) -> None:
    """Client code that calls the CurateCS.curate driver function to execute 
    the curation process.
    """
    print(f"Executing {curate_cs}.")

    curate_cs.curate(datadir, curate_cs.datatype, species, title,
                     units_e, units_sigma, augment_dicts,
                     initialize_nepc, test, debug, next_cs_id, next_csdata_id,
                     cs_ids)
