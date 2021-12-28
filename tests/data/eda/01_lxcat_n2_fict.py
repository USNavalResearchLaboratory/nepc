# %% [markdown]
# ***Summary: This notebook provides an overview of the nitrogen cross 
# sections from fict that are in NEPC.***

# %%
import nepc
from nepc.util import config
import numpy as np
import pandas as pd

# %%
pd.set_option('max_colwidth', 100)

# %% [markdown]
# ***NOTE: You may need to modify the `local` argument in the next command.  
# `local=True` points to a local copy of the NEPC database. 
# `local=False` points to a computer serving a NEPC MySQL database. 
# See `nepc.util.config.production()` and set the `$NEPC_PRODUCTION` environment variable.***

# %%
cnx, cursor = nepc.connect(local=False, test=True)

# %% [markdown]
# # Full fict dataset

# %%
fict = nepc.Model(cursor, "fict")

# %%
type(fict.summary())

# %%
fict.summary()

# %% [markdown]
# To inspect the `metadata` or `data` attribute of a particular cross section, use the `Model.subset` method.


# %%
fict.subset(metadata={'cs_id': 10})[0].metadata

# %% [markdown]
# # Electron-impact excitations provided by Model `fict`
# Note: the `fict`, `fict_min` or `fict_min2` models should **NOT** be used for simulations. These are populated with fictitious cross section data for testing and demonstration purposes only.

# See the `01_lxcat_n2_fict.py` script in  `curate` for details on how the data are curated starting from the LXCat text file.

# All excitations (pure electronic, rotational, and vibrational) of $\text{N}_2$ are from the ground electronic state, $\text{N}_2 (\text{X} {}^1\Sigma_g^+)$.

# There is no data in `fict` to support follow-on excitation of excited states.

# Vibrational excitations, $v_{0\rightarrow n}, n \in \{1, ..., 8\}$, of the ground electronic state, $\text{N}_2 (\text{X} {}^1\Sigma_g^+)$, are supported. $v_{0\rightarrow 1}$ is provided in two separate data sets. 

# Excitation from $\text{N}_2 (\text{X} {}^1\Sigma_g^+)$ to $\text{N}_2 (\text{A} {}^3\Sigma_u^+)$ are vibrationally resolved, but not completely. The cross sections are lumped into three fictitious vibronic levels: $v=(0-4)$, $v=(5-9)$, and $v=(10-)$.

# Cross sections for excitation to the three singlets above the $\text{N}_2$ ($a{}^{''}$ ${}^1\Sigma_g^+$) state are lumped together in the fictitious $\text{N}_2$ $(1SUM)_{Z-M}$) state.

# Rotational excitations within the $\text{N}_2 (\text{X} {}^1\Sigma_g^+)$ state are supported via the single level approximation to rotation (SLAR). Another option would be to use the cross sections for the resonance region (provided) along with the CAR approximation (not provided) in place of the SLAR approximation.

# De-excitation rates should be computed using detailed balance.

# %%
fict.plot(units_sigma=1E-20, process='excitation',
              plot_param_dict = {'linewidth':.8}, 
              #xlim_param_dict = {'left': 0.01, 'right': 120.0}, 
              ylog=True, xlog=True, max_plots=40, width=8, height=4) 

# %%
fict.plot(units_sigma=1E-20, process='excitation_v',
              plot_param_dict = {'linewidth':.8}, 
              #xlim_param_dict = {'left': 0.01, 'right': 120.0}, 
              ylog=True, xlog=True, max_plots=40, width=8, height=4) 

# %%
fict.plot(units_sigma=1E-20, process='ionization',
              plot_param_dict = {'linewidth':.8}, 
              #xlim_param_dict = {'left': 0.01, 'right': 120.0}, 
              ylog=True, xlog=True, max_plots=40, width=8, height=4) 

# %%
fict.plot(units_sigma=1E-20, process='total',
              plot_param_dict = {'linewidth':.8}, 
              #xlim_param_dict = {'left': 0.01, 'right': 120.0}, 
              ylog=True, xlog=True, max_plots=40, width=8, height=4) 

# %% [markdown]
# `fict_min`

# %% [markdown]
# The `fict_min2` model consists of five cross section data sets.

# 1. The `total` cross section (labelled "effective" in LxCat parlance) from the complete `fict` data set.

# 2. The `ionization_total` cross section from the complete `fict` data set.

# 3. An `excitation` cross section for rotational excitations within the $\text{N}_2 (\text{X} {}^1\Sigma_g^+)$ state using the single level approximation to rotation (SLAR). This, too, is directly from the complete `fict` data set.

# 4. (and 5.) Two `excitation_total` cross sections determined by interpolating and summing the electronic (and vibrational) excitations from the the $\text{N}_2 (\text{X} {}^1\Sigma_g^+)$ state. See the `02_fict_excitation_total.ipynb` Jupyter Notebook in  `methods` for details on how it is constructed.

# %%
fict_min2 = nepc.Model(cursor, "fict_min2")

# %%
fict_min2.summary()

# %%
fict_min2.plot(ylog=True, xlog=True, width=8, height=4) 

# %%
cnx.close()

# %%
