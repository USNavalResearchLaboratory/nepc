from nepc.methods import thomson

def test_length_lists():
	value = len(thomson.ionen_cross_N2p)
	assert value == len(thomson.reduced_ion_N2p)

def test_length_lists_2():
	value = len(thomson.ionen_cross_N2p)
	assert value == len(thomson.f_of_reduced_ion_N2p)

def test_funcGuess_type():
	valuetype = type(thomson.coeff_funcGuess_2)
	assert valuetype == numpy.ndarray
