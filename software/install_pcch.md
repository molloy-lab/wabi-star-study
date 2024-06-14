PCCH Installation Instructions
===

Analyses were run on the CBCB Nexus Cluster, using nodes with 32 AMD EPYC-7313 cores and 2TB of RAM; see [here](https://wiki.umiacs.umd.edu/umiacs/index.php/Nexus/CBCB).

Reminder to check [maintenance windows](https://wiki.umiacs.umd.edu/umiacs/index.php/MonthlyMaintenanceWindow) when submitting long jobs.

Interactive jobs
---
```
alias swork="srun --pty --ntasks=1 --mem=4GB --constraint=EPYC-7313 --qos=highmem --partition=cbcb --account=cbcb --time 08:00:00 bash"
```

**Step 1:** Start interactive job because need to do build on EPYC-7313
```
swork
uname -n
```
and check you are on CBCB node (got `cbcb17.umiacs.umd.edu`).

**Step 2:** Set-up conda environment for PCCH.
```
conda create -n lts-pcch
conda activate lts-pcch
conda install python=3.8
conda install git pip
pip install gurobipy
pip install networkx
pip install scipy
conda deactivate
```

**Step 3**: Check that Gurobi variables are set from installing it for [MACHINA](install_machina.md). 
```
echo $GRB_LICENSE_KEY
echo $LD_LIBRARY_PATH
```

**Step 4:** Download PCCH.
```
git clone https://github.com/elkebir-group/PCCH.git
```

**Step 5:** Test PCCH.
```
cd PCCH
conda run -n lts-pcch --live-stream python PCCH.py \
    simulation/sim_data/c_0_l_0_s_2_1_1.tree \
    simulation/sim_data/c_0_l_0_s_2_1_1.labeling
mkdir ../example_pcch_output
mv T-o.* ../example_pcch_output
```

**Step 6:** Then install [graphviz](https://www.graphviz.org/download/) and use command:
```
dot T-o.dot -Tpng -o image.png
```

**Step 7:** Record packages installed in our environment by typing
```
conda list -n lts-pcch
```
and saving
```
# packages in environment at /nfshomes/ekmolloy/.conda/envs/lts-pcch:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-forge
_openmp_mutex             4.5                       2_gnu    conda-forge
bzip2                     1.0.8                hd590300_5    conda-forge
ca-certificates           2023.11.17           hbcca054_0    conda-forge
ld_impl_linux-64          2.40                 h41732ed_0    conda-forge
libffi                    3.4.2                h7f98852_5    conda-forge
libgcc-ng                 13.2.0               h807b86a_3    conda-forge
libgomp                   13.2.0               h807b86a_3    conda-forge
libnsl                    2.0.1                hd590300_0    conda-forge
libsqlite                 3.44.2               h2797004_0    conda-forge
libuuid                   2.38.1               h0b41bf4_0    conda-forge
libzlib                   1.2.13               hd590300_5    conda-forge
ncurses                   6.4                  h59595ed_2    conda-forge
numpy                     1.24.4                   pypi_0    pypi
openssl                   3.2.0                hd590300_1    conda-forge
pip                       23.3.1             pyhd8ed1ab_0    conda-forge
python                    3.8.18          hd12c33a_0_cpython    conda-forge
readline                  8.2                  h8228510_1    conda-forge
setuptools                68.2.2             pyhd8ed1ab_0    conda-forge
tk                        8.6.13          noxft_h4845f30_101    conda-forge
wheel                     0.42.0             pyhd8ed1ab_0    conda-forge
xz                        5.2.6                h166bdaf_0    conda-forge
```
