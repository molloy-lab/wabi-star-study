#!/bin/bash

module load Python3/3.10.4

NLINS=( 50 )
NCASS=( 10 30 )
CLENS=( 1 3 10 )
MUTPS=( 0.1 )
DOUTS=( 0.0 0.05 0.15 0.20 )

for NLIN in ${NLINS[@]}; do
    for NCAS in ${NCASS[@]}; do
        for CLEN in ${CLENS[@]}; do
            for MUTP in ${MUTPS[@]}; do
                for DOUT in ${DOUTS[@]}; do
                    for SEED in `seq -f "%02g" 1 20`; do
                        python3.10 simulate_data_from_startle_paper.py \
                            -n $NLIN \
			    -m $NCAS \
			    -l $CLEN \
			    -p $MUTP \
			    -d $DOUT \
			    -s $SEED
                    done
                done
            done
        done
    done
done

