"""Templates for curating cross section data from various sources (e.g. LxCAT).

Provides templates for curating raw and external (e.g. LxCAT) cross section data:

- parse and clean data (e.g. remove zeroes, set thresholds)
- augment the data (e.g. add additional metadata, create lumped cross sections)
- verify data
- write data to nepc formatted input files (i.e. .dat, .met, .mod)
"""
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Tuple
import re
import math
import numpy as np
import nepc
from nepc.util import util
from nepc.util import parser


class CurateCS(ABC):
    """Template method that contains the skeleton for curating cross section data.
    """
    def remove_zeros(self, csdata, debug=False):
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

    @abstractmethod
    def curate(self, datadir: str, species: str, title: str, units_e: str,
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


    def initialize_input(self, datadir: str, species: str,
                         title: str) -> List[str]:
        """Initialize input filelist for curation processes that read data from files.
        """
        filedir = f'{datadir}/raw/{self.datatype}/{species}/{title}'
        filelist = util.get_filelist(filedir, self.datatype)
        if len(filelist) == 0:
            raise Exception('No files to process.')
        else:
            print(f'Files in queue: {filelist}')
        return filelist

    def initialize_output(self, datadir: str, species: str, title: str) -> str:
        """Initialize output directory for curation process
        """
        outdir = f'{datadir}/cs/{self.datatype}/{species}/{title}'
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
                                                       lhs_b=cs['lhs_b'],
                                                       rhs_a=cs['rhs_a'],
                                                       rhs_b=cs['rhs_b'],
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

    @abstractproperty
    def datatype(self) -> str:
        """Provide data type for curation process
        """

class CurateQDB(CurateCS):
    """Template for curating QuantemolDB (QDB) cross section data
    """

    def curate(self, datadir: str, species: str, title: str, units_e=None,
               units_sigma=None, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Curation driver function for QDB text files.
        """
        next_cs_id, next_csdata_id = self.initialize_db(initialize_nepc, test,
                                                        debug, next_cs_id, next_csdata_id)
        filelist = self.initialize_input(datadir, species, title)
        outdir = self.initialize_output(datadir, species, title)
        csdata = self.get_csdata(filelist, debug=debug)
        csdata = self.clean_csdata(csdata, debug=debug)
        csdata = [self.augment_csdata(csdata, outdir, title, units_e, units_sigma, augment_dicts)]
        self.verify_csdata()
        next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)
        self.finalize(next_cs_id, next_csdata_id, test, debug)


    def get_csdata(self, filelist, debug=False):
        """Get cross section data for curation process.
        """
        import xml.etree.ElementTree as ET
        import os
        import csv

        csdata = dict()

        ns = {'uri': 'https://quantemoldb.com/qml'}
        tree = ET.parse(filelist[0])
        root = tree.getroot()

        def print_dict_val(dictionary, k):
            print(f'{k}: {dictionary[k]}')

        for child in root.findall('uri:dataset/uri:data_table/uri:column', ns):
            if child.attrib['name'] == 'eE' and child.attrib['units'] == 'eV':
                csdata['units_e'] = '1.0'
                if debug:
                    print_dict_val(csdata, 'units_e')
            elif child.attrib['name'] == 'sigma' and child.attrib['units'] == 'cm2':
                csdata['units_sigma'] = '1.0E-4'
                if debug:
                    print_dict_val(csdata, 'units_sigma')
            else:
                raise Exception('units not implemented')

        csdata['nrows'] = int(root.find('uri:dataset/uri:data_table/uri:nrows',
                                        ns).text)

        datafile_path = filelist[0].replace(
            os.path.basename(filelist[0]),
            root.find('uri:dataset/uri:data_table/uri:filename',
                      ns).text)
        if debug:
            print(f'Getting data from {datafile_path}.')

        csdata['data'] = []
        csdata['threshold'] = np.Inf
        with open(datafile_path, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                csdata['data'].append(row)
                csdata['threshold'] = min(csdata['threshold'], float(csdata['data'][-1][0]))

        csdata['data'] = np.asarray(csdata['data'])

        if len(csdata['data']) != csdata['nrows']:
            raise Exception(f'Failed to read in {csdata["nrows"]} as expected.')
        else:
            print(f'Read in {csdata["nrows"]} data points as expected.')
        return csdata


    def clean_csdata(self, csdata, debug=False):
        """Clean QDB cross section data during curation process.
        """
        self.remove_zeros([csdata], debug)
        return csdata 

    def augment_csdata(self, csdata, outdir, title, units_e, units_sigma,
                       augment_dicts=None, debug=False, test=False):

        csdata_augmented = csdata
        
        csdata_augmented['nepc_filename'] = outdir + '/' + title

        check_process_attr = ['lhs', 'rhs', 'lhs_hv', 'rhs_hv',
                              'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j']

        process_attr_values = nepc.process_attr(augment_dicts['process'],
                                                check_process_attr, test)

        process_attr_keys = {'lhs': ['lhs_a', 'lhs_b'],
                             'rhs': ['rhs_a', 'rhs_b'],
                             'lhs_v': ['lhs_v'],
                             'rhs_v': ['rhs_v'],
                             'lhs_hv': ['lhs_hv'],
                             'rhs_hv': ['rhs_hv'],
                             'lhs_j': ['lhs_j'],
                             'rhs_j': ['rhs_j']}

        for _, (key, value) in enumerate(process_attr_keys.items()):
            for v in value:
                csdata_augmented[v] = self.value(csdata_augmented, v)
            if sum(k in augment_dicts.keys() for k in value) != process_attr_values[key]:
                raise Exception(f'Mismatch in augment_dicts for {key}')

        for _, (key, value) in enumerate(augment_dicts.items()):
            csdata_augmented[key] = value
            if debug:
                print(f'csdata_augmented[{key}]: {csdata_augmented[key]}')

        return csdata_augmented

    def verify_csdata(self) -> None:
        """Verify cross setion data in curation process.
        """


    def __str__(self) -> str:
        return "QuantemolDB cross section curation"


    @property
    def datatype(self) -> str:
        """Provide data type for curation process
        """
        return "qdb"

class CurateGenerated(CurateCS):
    """Template for curating generated cross section data
    """

    def curate(self, datadir: str, species: str, title: str, units_e=None,
               units_sigma=None, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Curation driver function for generated cross section files.
        """
        next_cs_id, next_csdata_id = self.initialize_db(initialize_nepc, test,
                                                        debug, next_cs_id, next_csdata_id)
        print(f'next_cs_id: {next_cs_id}\tnext_csdata_id: {next_csdata_id}')
        #filelist = self.initialize_input(datadir, species, title)
        #outdir = self.initialize_output(datadir, species, title)
        #csdata = self.get_csdata(filelist, debug=debug)
        #csdata = self.clean_csdata(csdata, debug=debug)
        #csdata = [self.augment_csdata(csdata, outdir, title, units_e, units_sigma, augment_dicts)]
        #self.verify_csdata()
        #next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)
        #self.finalize(next_cs_id, next_csdata_id, test, debug)


    def get_csdata(self, filelist, debug=False):
        """Get cross section data for curation process.
        """
        import toml
        import os
        import csv

        metadata = toml.load()
        
        csdata = dict()

        csdata['nrows'] = int(root.find('uri:dataset/uri:data_table/uri:nrows',
                                        ns).text)

        datafile_path = filelist[0].replace(
            os.path.basename(filelist[0]),
            root.find('uri:dataset/uri:data_table/uri:filename',
                      ns).text)
        if debug:
            print(f'Getting data from {datafile_path}.')

        csdata['data'] = []
        csdata['threshold'] = np.Inf
        with open(datafile_path, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                csdata['data'].append(row)
                csdata['threshold'] = min(csdata['threshold'], float(csdata['data'][-1][0]))

        csdata['data'] = np.asarray(csdata['data'])

        if len(csdata['data']) != csdata['nrows']:
            raise Exception(f'Failed to read in {csdata["nrows"]} as expected.')
        else:
            print(f'Read in {csdata["nrows"]} data points as expected.')
        return csdata


    def clean_csdata(self, csdata, debug=False):
        """Clean QDB cross section data during curation process.
        """
        self.remove_zeros([csdata], debug)
        return csdata 

    def augment_csdata(self, csdata, outdir, title, units_e, units_sigma,
                       augment_dicts=None, debug=False, test=False):

        csdata_augmented = csdata
        
        csdata_augmented['nepc_filename'] = outdir + '/' + title

        check_process_attr = ['lhs', 'rhs', 'lhs_hv', 'rhs_hv',
                              'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j']

        process_attr_values = nepc.process_attr(augment_dicts['process'],
                                                check_process_attr, test)

        process_attr_keys = {'lhs': ['lhs_a', 'lhs_b'],
                             'rhs': ['rhs_a', 'rhs_b'],
                             'lhs_v': ['lhs_v'],
                             'rhs_v': ['rhs_v'],
                             'lhs_hv': ['lhs_hv'],
                             'rhs_hv': ['rhs_hv'],
                             'lhs_j': ['lhs_j'],
                             'rhs_j': ['rhs_j']}

        for _, (key, value) in enumerate(process_attr_keys.items()):
            for v in value:
                csdata_augmented[v] = self.value(csdata_augmented, v)
            if sum(k in augment_dicts.keys() for k in value) != process_attr_values[key]:
                raise Exception(f'Mismatch in augment_dicts for {key}')

        for _, (key, value) in enumerate(augment_dicts.items()):
            csdata_augmented[key] = value
            if debug:
                print(f'csdata_augmented[{key}]: {csdata_augmented[key]}')

        return csdata_augmented

    def verify_csdata(self) -> None:
        """Verify cross setion data in curation process.
        """


    def __str__(self) -> str:
        return "generated cross section curation"


    @property
    def datatype(self) -> str:
        """Provide data type for curation process
        """
        return "generated"

class CurateLxCAT(CurateCS):
    """Template for curating LXCat cross section data
    """


    def print_csdata_table(self, keys, csdata):
        """Print cross section data for debugging.
        """
        print('\t'.join(keys))
        print('===============================================================================')
        for cs in csdata:
            print('\t'.join([self.value(cs, key) for key in keys]))

    def curate(self, datadir: str, species: str, title: str, units_e: str,
               units_sigma: str, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Curation driver function for LXCat text files.
        """
        next_cs_id, next_csdata_id = self.initialize_db(initialize_nepc, test,
                                                        debug, next_cs_id, next_csdata_id)
        filelist = self.initialize_input(datadir, species, title)
        outdir = self.initialize_output(datadir, species, title)
        csdata = self.get_csdata(filelist, debug=debug)
        csdata = self.clean_csdata(csdata, debug=debug)
        csdata = self.augment_csdata(csdata, outdir, title, units_e, units_sigma, augment_dicts)
        self.verify_csdata()
        next_cs_id, next_csdata_id = self.write_csdata(csdata, next_cs_id, next_csdata_id)
        self.finalize(next_cs_id, next_csdata_id, test, debug)

    def get_csdata(self, filelist, debug=False):
        """Get cross section data from LxCAT formatted text file.
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
        self.remove_zeros(csdata, debug)
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
            cs['lhs_a'] = self.value(cs, 'lhs_a')
            cs['lhs_b'] = self.value(cs, 'lhs_b')
            cs['rhs_a'] = self.value(cs, 'rhs_a')
            cs['rhs_b'] = self.value(cs, 'rhs_b')
            cs['lhs_v'] = self.value(cs, 'lhs_v')
            cs['rhs_v'] = self.value(cs, 'rhs_v')
            cs['lhs_j'] = self.value(cs, 'lhs_j')
            cs['rhs_j'] = self.value(cs, 'rhs_j')
            cs['lhs_hv'] = self.value(cs, 'lhs_hv')
            cs['rhs_hv'] = self.value(cs, 'rhs_hv')

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
        threshold = np.Inf
        for cs in csdata:
            min_e = min(min_e, np.min(cs.data['e']))
            max_e = max(max_e, np.max(cs.data['e']))
            threshold = min(threshold, cs.metadata['threshold'])
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
        csdata_lumped = {}
        csdata_lumped['threshold'] = threshold
        csdata_lumped['data'] = np.asarray([[e_i, sigma_i] for e_i, sigma_i in zip(e_range, sigma)])
        return csdata_lumped


    def unique_metadata(self, csdata, key):
        return list(set([str(cs.metadata[key]) for cs in csdata]))


    def metadata_match(self, csdata, key):
        return [True] * (len(csdata) - 1) == [csdata[i-1].metadata[key] == csdata[i].metadata[key] for i in range(1, len(csdata))]

    def check_for_unmatched_metadata(self, csdata, keys):
        unmatched_metadata = []
        for key in keys:
            if not self.metadata_match(csdata, key):
                unmatched_metadata.append(str(key))
        if len(unmatched_metadata) > 0:
            raise Exception(f"Trying {self} with unmatched "
                            f"{' and '.join(unmatched_metadata)}.")


    def curate(self, datadir: str, species: str, title: str, units_e: str,
               units_sigma: str, augment_dicts=None, initialize_nepc=False,
               test=False, debug=False,
               next_cs_id=None, next_csdata_id=None, cs_ids=None) -> None:
        """Curation driver function for lumped cross sections.
        """
        next_cs_id, next_csdata_id = self.initialize_db(initialize_nepc, test,
                                                        debug, next_cs_id, next_csdata_id)
        outdir = self.initialize_output(datadir, species, title)
        csdata = self.get_csdata(cs_ids)
        csdata_lumped = [self.augment_csdata(csdata, outdir, title,
                                            units_e, units_sigma, augment_dicts, debug)]
        self.verify_csdata()
        next_cs_id, next_csdata_id = self.write_csdata(csdata_lumped, next_cs_id, next_csdata_id)
        self.finalize(next_cs_id, next_csdata_id, test, debug)


    def get_csdata(self, cs_ids) -> List[dict]:
        cnx, cursor = nepc.connect(local=True)
        csdata = nepc.CustomModel(cursor, cs_id_list=cs_ids).cs
        cnx.close()
        return csdata


    def augment_csdata(self, csdata, outdir, title, units_e, units_sigma,
                       augment_dicts=None, debug=False, test=False):

        consolidated_metadata = ['ref']
        matched_metadata = ['specie', 'units_e', 'units_sigma']
        self.check_for_unmatched_metadata(csdata, matched_metadata)

        csdata_lumped = self.lump(csdata)
        csdata_lumped['nepc_filename'] = outdir + '/' + title

        check_process_attr = ['lhs', 'rhs', 'lhs_hv', 'rhs_hv',
                              'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j']

        process_attr_values = nepc.process_attr(augment_dicts['process'],
                                                check_process_attr, test)

        process_attr_keys = {'lhs': ['lhs_a', 'lhs_b'],
                             'rhs': ['rhs_a', 'rhs_b'],
                             'lhs_v': ['lhs_v'],
                             'rhs_v': ['rhs_v'],
                             'lhs_hv': ['lhs_hv'],
                             'rhs_hv': ['rhs_hv'],
                             'lhs_j': ['lhs_j'],
                             'rhs_j': ['rhs_j']}

        for _, (key, value) in enumerate(process_attr_keys.items()):
            for v in value:
                csdata_lumped[v] = self.value(csdata_lumped, v)
            if sum(k in augment_dicts.keys() for k in value) != process_attr_values[key]:
                raise Exception(f'Mismatch in augment_dicts for {key}')

        for key in matched_metadata + consolidated_metadata:
            csdata_lumped[key] = ','.join(self.unique_metadata(csdata, key))
            if debug:
                print(f'csdata_lumped[{key}]: {csdata_lumped[key]}')

        for _, (key, value) in enumerate(augment_dicts.items()):
            csdata_lumped[key] = value
            if debug:
                print(f'csdata_lumped[{key}]: {csdata_lumped[key]}')

        return csdata_lumped

    def verify_csdata(self) -> None:
        pass

    def __str__(self) -> str:
        return "lumped cross section curation"

    @property
    def datatype(self) -> str:
        return "lumped"


def curate_client(curate_cs: CurateCS, datadir: str, species: str, title: str,
                  units_e=None, units_sigma=None, augment_dicts=None,
                  initialize_nepc=False, test=False,
                  debug=False, next_cs_id=None, next_csdata_id=None,
                  cs_ids=None) -> None:
    """Client code that calls the CurateCS.curate driver function to execute 
    the curation process.
    """
    print(f"Executing {curate_cs}.")

    curate_cs.curate(datadir, species, title,
                     units_e, units_sigma, augment_dicts,
                     initialize_nepc, test, debug, next_cs_id, next_csdata_id,
                     cs_ids)
