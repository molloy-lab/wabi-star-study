Startle installation instructions
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

**Step 2:** Switch gcc version and load relevant modules.
Type:
```
module load gcc/11.2.0
module load boost/1.80
module load cmake/3.22.1
gcc -v
```

**Step 3:** Export some relevant paths.
```
export GRDIR="/fs/cbcb-lab/ekmolloy"
export EXPATH="$GRDIR/group/external"
export SWPATH="$GRDIR/ekmolloy/lineage-tracing-study/software-built-on-EPYC-7313"
```

**Step 4:** Install CPLEX by downloading the installer into `$EXPATH/cplex-12.7-installer` and installing it into this directory `$EXPATH/cplex-12.7-install`. Note that I needed to use Firefox in order to download CPLEX installer with an academic license - Safari did not work!

**Step 5:** Download and build the LEMON library.
```
cd $SWPATH
mkdir lemon-1.3.1-install
wget http://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz
tar xvzf lemon-1.3.1.tar.gz 
cd lemon-1.3.1
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="$SWPATH/lemon-1.3.1-install" ..
make install
cd ../../
```

**Step 6:** Download Startle (commit: 50ac763).
```
git clone --recurse-submodules https://github.com/raphael-group/startle.git
cd startle
```

**Step 7:** Build the C++ NNI version of Startle.
```
mkdir build-nni
cd build-nni
cmake ..
make
cd ..
mv CMakeLists.txt CMakeLists_NNI.txt
```

**Step 8:** Build the ILP version of Startle.
```
mv CMakeLists_ILP.txt CMakeLists.txt
mkdir build
cd build
cmake -DLIBLEMON_ROOT="$SWPATH/lemon-1.3.1-install/" \
      -DCPLEX_INC_DIR="$EXPATH/cplex-12.7-install/cplex/include" \
      -DCPLEX_LIB_DIR="$EXPATH/cplex-12.7-install/cplex/lib/x86-64_linux/static_pic" \
      -DCONCERT_INC_DIR="$EXPATH/cplex-12.7-install/concert/include" \
      -DCONCERT_LIB_DIR="$EXPATH/cplex-12.7-install/concert/lib/x86-64_linux/static_pic" ..
make
cd ..
```

**Step 9:** Create a conda environment and install some dependencies of Startle.
```
conda create -n lts-startle
conda activate lts-startle
conda install python=3.8
conda install -c conda-forge biopython
conda install -c conda-forge funcy loguru tqdm networkx pandas numpy seaborn
conda install git pip
pip install git+https://github.com/YosefLab/Cassiopeia@master#egg=cassiopeia-lineage 
conda deactivate
```
Note that I said `y` when being asked to download and extract packages.
Also note I installed Cassiopeia on December 11, 2023 (commit: 2ca07df). 

**Step 10:** Download perl to `$EXPATH`, as it's required to run Startle-ILP.
```
cd $EXPATH
tar -zxvf perl-5.38.0.tar.gz
mkdir perl-5.38.0-install
cd perl-5.38.0
./Configure -des -Dprefix=$EXPATH/perl-5.38.0-install
make test
make install
```
Add the following line to `~/.bash_profile`:
```
export PATH="/fs/cbcb-lab/ekmolloy/group/software-compiled-on-EPYC-7313/perl-5.38.0-install/:$PATH"
```
and source the profile typing: `source ~/.bash_profile`.
Check that you are using the correct version of perl by typing `which perl` and `perl -v` and then install the perl dependencies for Startle-ILP:
```
perl -MCPAN -e'install Text::CSV'
perl -MCPAN -e'install Getopt::ArgParse'
```

**Step 11:** Try to run Startle-ILP on the example.
```
cd $SWPATH/startle
conda run -n lts-startle --live-stream perl scripts/startle_ilp.pl \
      -c examples/n100_m30_d0.2_s0_p0.2_character_matrix.csv \
      -m examples/n100_m30_d0.2_s0_p0.2_mutation_prior.csv \
      -o example_startle_ilp_output \
      --threads 1
```

**Step 12:** Try to run Startle-NNI on the example.
```
mkdir ../example_startle_nni_output
conda run -n lts-startle --live-stream python scripts/nj.py \
    examples/n100_m30_d0.2_s0_p0.2_character_matrix.csv \
    --output ../example_startle_nni_output/n100_m30_d0.2_s0_p0.2_seed_tree.newick
./build-nni/src/startle \
    large \
    examples/n100_m30_d0.2_s0_p0.2_character_matrix.csv \
    examples/n100_m30_d0.2_s0_p0.2_mutation_prior.csv \
    ../example_startle_nni_output/n100_m30_d0.2_s0_p0.2_seed_tree.newick  \
    --output ../example_startle_nni_output/n100_m30_d0.2_s0_p0.2_startle
```

**Step 13:** Record packages installed in our environment by typing
```
conda list -n lts-startle
```
and saving
```
# packages in environment at /nfshomes/ekmolloy/.conda/envs/lts-startle:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
biopython                 1.79             py38h497a2fe_1    conda-forge
blas                      1.0                    openblas  
bottleneck                1.3.5            py38h7deecbd_0  
brotli                    1.0.9                h9c3ff4c_4    conda-forge
bzip2                     1.0.8                h7b6447c_0  
c-ares                    1.19.1               h5eee18b_0  
ca-certificates           2023.08.22           h06a4308_0  
cassiopeia-lineage        2.0.0                    pypi_0    pypi
clarabel                  0.6.0                    pypi_0    pypi
colorama                  0.4.6              pyhd8ed1ab_0    conda-forge
contourpy                 1.0.5            py38hdb19cb5_0  
curl                      8.4.0                hdbd6064_1  
cvxpy                     1.4.1                    pypi_0    pypi
cycler                    0.12.1             pyhd8ed1ab_0    conda-forge
ecos                      2.0.12                   pypi_0    pypi
expat                     2.5.0                h6a678d5_0  
fonttools                 4.25.0             pyhd3eb1b0_0  
freetype                  2.10.4               h0708190_1    conda-forge
funcy                     2.0                pyhd8ed1ab_0    conda-forge
gdbm                      1.18                 hd4cb3f1_4  
gettext                   0.21.0               h39681ba_1  
giflib                    5.2.1                h36c2ea0_2    conda-forge
git                       2.40.1          pl5340h36fbf9e_1  
icu                       73.1                 h6a678d5_0  
itolapi                   4.1.2                    pypi_0    pypi
jpeg                      9e                   h166bdaf_1    conda-forge
kiwisolver                1.4.4            py38h6a678d5_0  
krb5                      1.20.1               h143b758_1  
lcms2                     2.12                 h3be6417_0  
ld_impl_linux-64          2.38                 h1181459_1  
lerc                      3.0                  h295c915_0  
libblas                   3.9.0           15_linux64_openblas    conda-forge
libcblas                  3.9.0           15_linux64_openblas    conda-forge
libcurl                   8.4.0                h251f7ec_1  
libdeflate                1.17                 h5eee18b_1  
libedit                   3.1.20221030         h5eee18b_0  
libev                     4.33                 h7f8727e_1  
libffi                    3.4.4                h6a678d5_0  
libgcc-ng                 11.2.0               h1234567_1  
libgfortran-ng            13.2.0               h69a702a_0    conda-forge
libgfortran5              13.2.0               ha4646dd_0    conda-forge
libgomp                   11.2.0               h1234567_1  
liblapack                 3.9.0           15_linux64_openblas    conda-forge
libnghttp2                1.57.0               h2d74bed_0  
libopenblas               0.3.20          pthreads_h78a6416_0    conda-forge
libpng                    1.6.39               h5eee18b_0  
libssh2                   1.10.0               hdbd6064_2  
libstdcxx-ng              11.2.0               h1234567_1  
libtiff                   4.5.1                h6a678d5_0  
libwebp                   1.3.2                h11a3e52_0  
libwebp-base              1.3.2                h5eee18b_0  
libxml2                   2.10.4               hf1b16e4_1  
llvmlite                  0.41.1                   pypi_0    pypi
loguru                    0.7.2            py38h578d9bd_1    conda-forge
lz4-c                     1.9.4                h6a678d5_0  
matplotlib-base           3.6.2            py38h945d387_0  
munkres                   1.1.4              pyh9f0ad1d_0    conda-forge
ncurses                   6.4                  h6a678d5_0  
networkx                  2.8.8              pyhd8ed1ab_0    conda-forge
ngs-tools                 1.8.5                    pypi_0    pypi
numba                     0.58.1                   pypi_0    pypi
numexpr                   2.8.4            py38hd2a5715_1  
numpy                     1.22.3           py38h99721a1_2    conda-forge
openssl                   3.0.12               h7f8727e_0  
osqp                      0.6.3                    pypi_0    pypi
packaging                 23.2               pyhd8ed1ab_0    conda-forge
pandas                    2.0.3            py38h1128e8f_0  
parameterized             0.9.0                    pypi_0    pypi
patsy                     0.5.4              pyhd8ed1ab_0    conda-forge
pcre2                     10.42                hebb0a14_0  
perl                      5.34.0               h5eee18b_2  
pillow                    9.4.0            py38h6a678d5_1  
pip                       23.3.1           py38h06a4308_0  
plotly                    5.18.0                   pypi_0    pypi
pybind11                  2.11.1                   pypi_0    pypi
pyparsing                 3.1.1              pyhd8ed1ab_0    conda-forge
pyseq-align               1.0.2                    pypi_0    pypi
python                    3.8.18               h955ad1f_0  
python-dateutil           2.8.2              pyhd8ed1ab_0    conda-forge
python-tzdata             2023.3             pyhd8ed1ab_0    conda-forge
python_abi                3.8                      2_cp38    conda-forge
pytz                      2023.3.post1       pyhd8ed1ab_0    conda-forge
qdldl                     0.1.7.post0              pypi_0    pypi
readline                  8.2                  h5eee18b_0  
scipy                     1.8.1            py38h1ee437e_0    conda-forge
scs                       3.2.4.post1              pypi_0    pypi
seaborn                   0.13.0               hd8ed1ab_0    conda-forge
seaborn-base              0.13.0             pyhd8ed1ab_0    conda-forge
setuptools                68.0.0           py38h06a4308_0  
shortuuid                 1.0.11                   pypi_0    pypi
six                       1.16.0             pyh6c4a22f_0    conda-forge
sqlite                    3.41.2               h5eee18b_0  
statsmodels               0.14.0           py38ha9d4c09_0  
tenacity                  8.2.3                    pypi_0    pypi
tk                        8.6.12               h1ccaba5_0  
tqdm                      4.66.1             pyhd8ed1ab_0    conda-forge
wheel                     0.41.2           py38h06a4308_0  
xz                        5.4.5                h5eee18b_0  
zlib                      1.2.13               h5eee18b_0  
zstd                      1.5.5                hc292b87_0 
```
