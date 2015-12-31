#!/bin/bash

EXE=./AdvTrans1D.py

#
# Show command line parameters
#
./$EXE -h

vel=0.9 ;
dx=0.05 ;
dt=0.05 ;
J=200 ;
N=150 ;
update=10 ;

for method in BW ; do \
    echo "*** Integration method: $method ***" ; \
    echo "Ramp initial condition (sharp leading edge)" ; \
    $EXE -m $method -i 'lambda x: 0.0 if x < 1.0 or x > 2 else x-1.0'   -v $vel -x $dx -t $dt -J $J -N $N -u $update; \
    echo "Square-wave initial condition (sharp leading and trailing edges)" ; \
    $EXE -m $method -i 'lambda x: 0.0 if x < 1.0 or x > 2 else 1.0'     -v $vel -x $dx -t $dt -J $J -N $N -u $update ; \
    echo "Triangle initial condition (neither edge is sharp)" ; \
    $EXE -i 'lambda x: 0.0 if x < 1.0 or x > 2 else 1.0-2.0*abs(x-1.5)' -v $vel -x $dx -t $dt -J $J -N $N -u $update ; \
done ;
