MACHINA installation instructions
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

**Step 4:** Download Gurobi following the instructions [here](https://ca.cs.uni-bonn.de/doku.php?id=tutorial:gurobi-install). 
```
cd $SWPATH
wget https://packages.gurobi.com/10.0/gurobi10.0.1_linux64.tar.gz
tar -xzvf gurobi10.0.3_linux64.tar.gz
cd gurobi1003/linux64/src/build/
make
cp libgurobi_c++.a ../../lib/
cd ../../../
```
Now copy the key file here (i.e., put it in `gurobi1003`) and then add the following variable to `~/.bash_profile`:
```
export GUROBI_HOME="/fs/cbcb-lab/ekmolloy/ekmolloy/lineage-tracing-study/software-built-on-EPYC-7313/gurobi1003/linux64"
export GRB_LICENSE_FILE="/fs/cbcb-lab/ekmolloy/ekmolloy/lineage-tracing-study/software-built-on-EPYC-7313/gurobi1003/gurobi.lic"
export GRB_LICENSE_KEY="/fs/cbcb-lab/ekmolloy/ekmolloy/lineage-tracing-study/software-built-on-EPYC-7313/gurobi1003/gurobi.lic"
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"
```

Lastly, test gurobi:
```
source ~/.bash_profile
gurobi.sh
```

**Step 5:** Download and build MACHINA (commit ac71282).
```
cd $SWPATH
git clone https://github.com/raphael-group/machina
cd machina
```
Edit `CMakeLists.txt` so that it uses variable `GUROBI_ROOT` and `BOOST_ROOT`, as shown here: [CMakeLists_MACHINA.txt](CMakeLists_MACHINA.txt).
Continue with build.
```
mkdir build
cd build
cmake -DLIBLEMON_ROOT="$SWPATH/lemon-1.3.1-install/" \
      -DGUROBI_ROOT="$SWPATH/gurobi1003/linux64/" \
      -DBOOST_ROOT="/fs/cbcb-software/RedHat-8-x86_64/local/boost/1.80/" ..
VERBOSE=1 make
```

**Step 6:** Test if MACHINA worked.
Test `pmh_sankoff`.
```
mkdir ../example_machina_output
./build/pmh_sankoff \
    -p LOv,ROv \
    -c data/mcpherson_2016/coloring.txt data/mcpherson_2016/patient1.tree \
    data/mcpherson_2016/patient1.labeling \
    -o ../example_machina_output \
    2> ../example_machina_output/pmh_sankoff_result.txt
```
Test `pmh`.
```
mkdir ../example_machina_constrained_output
./build/pmh \
    -p LOv \
    -c data/mcpherson_2016/coloring.txt \
    data/mcpherson_2016/patient1.tree \
    data/mcpherson_2016/patient1.labeling \
    -o ../example_machina_constrained_output/ \
    > ../example_machina_constrained_output/result.txt
```
Test `pmh_tr`.
```
mkdir ../example_machina_tr_output
./build/pmh_tr \
    -p LOv \
    -c data/mcpherson_2016/coloring.txt \
    data/mcpherson_2016/patient1.tree \
    data/mcpherson_2016/patient1.labeling \
    -o ../example_machina_tr_output/ \
    > ../example_machina_tr_output/result.txt
```
Note that you often need to source your bash profile again before running.
