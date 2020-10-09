"""Process fictitious N2 cross sections from LxCAT.
"""
from nepc.curate.curate import CurateLxCAT, curate_client
from nepc.util import config


NEPC_HOME = config.nepc_home()
datadir = NEPC_HOME + "/tests/data"

states = {
    'X1': 'N2(X1Sigmag+)',
    'B3': 'N2(B3Pig)',
    'W3': 'N2(W3Deltau)',
    'B\'3': 'N2(Bp3Sigmau-)',
    'a\'1': 'N2(ap1Sigmau-)',
    'a1': 'N2(a1Pig)',
    'w1': 'N2(w1Deltau)',
    'C3': 'N2(C3Piu)',
    'E3': 'N2(E3Sigmag+)',
    'a\'\'1': 'N2(ap1Sigmag+)',
    'B2SIGMA': 'N2+(B2Sigmau+)',
    'SUM': 'N2(1SUM)_Z-M',
    'N2\\^\\+': 'N2+'
}

augment_dicts = [[{'kind': 'EXCITATION'},
                  {'process': 'excitation',
                   'lhs_a': states['X1'],
                   'models': ['fict']}]]

for key in states.keys():
    augment_dicts.append([{'product': key},
                          {'rhs_a': states[key]}])

for i in range(9):
    augment_dicts.append([{'kind': 'EXCITATION',
                           'product': f'v{i}',
                           'background': f'V={i}'},
                          {'process': 'excitation_v',
                           'lhs_a': f'{states["X1"]}',
                           'rhs_a': f'{states["X1"]}',
                           'lhs_v': '0',
                           'rhs_v': f'{i}',
                           'models': ['fict']}])

augment_dicts = augment_dicts + [
    [{'product': 'v1res',
      'background': 'V=1'},
     {'rhs_a': 'N2(X1Sigmag+)',
      'lhs_v': 0,
      'rhs_v': 1}],
    [{'product': 'v0-4',
      'background': 'V=0-4'},
     {'rhs_a': 'N2(A3Sigmau+)_v0-4',
      'lhs_v': '-1',
      'rhs_v': '-1',
      'process': 'excitation'}],
    [{'product': 'v5-9',
      'background': 'V=5-9'},
     {'rhs_a': 'N2(A3Sigmau+)_v5-9',
      'lhs_v': '-1',
      'rhs_v': '-1',
      'process': 'excitation'}],
    [{'product': 'v10-',
      'background': 'V=10-'},
     {'rhs_a': 'N2(A3Sigmau+)_v10-',
      'lhs_v': '-1',
      'rhs_v': '-1',
      'process': 'excitation'}],
    [{'kind': 'IONIZATION',
      'product': 'N2\^\+'},
     {'process': 'ionization_total',
      'lhs_a': states['X1'],
      'rhs_a': 'N2+',
      'models': ['fict', 'fict_min', 'fict_min2']}],
    [{'kind': 'EXCITATION',
      'product': 'rot',
      'background': 'SLAR'},
     {'process': 'excitation',
      'lhs_a': states['X1'],
      'rhs_a': 'N2(X1Sigmag+)_jSLAR',
      'models': ['fict', 'fict_min2']}],
    [{'kind': 'IONIZATION',
      'product': 'B2SIGMA'},
     {'process': 'ionization',
      'lhs_a': states['X1'],
      'rhs_a': states['B2SIGMA'],
      'models': ['fict']}],
    [{'kind': 'EFFECTIVE'},
     {'process': 'total',
      'lhs_a': 'N2',
      'rhs_a': 'N2',
      'models': ['fict',
                 'fict_min',
                 'fict_min2']}],
    [{'kind': 'EXCITATION',
      'product': 'rot',
      'background': 'SCHULZ'},
     {'process': 'excitation',
      'lhs_a': states['X1'],
      'rhs_a': 'N2(X1Sigmag+)_jSCHULZ',
      'models': ['fict']}]]

curate_client(CurateLxCAT(),
              datadir,
              species='n2',
              title='fict',
              units_e='1.0',
              units_sigma='1.0',
              augment_dicts=augment_dicts,
              initialize_nepc=True,
              test=True)
