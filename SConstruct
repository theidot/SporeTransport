#!/usr/local/bin/python2.7

from os import environ
import os.path

env = DefaultEnvironment(
    LATEX='/usr/texbin/pdflatex',
    LIBPATH=['/usr/local/lib', '/pkg/lib'],
    ENV = environ
)

env['TANGLE']    = '/usr/local/bin/notangle'
env['WEAVE']     = '/usr/local/bin/noweave'
env['ASYMPTOTE'] = '/pkg/bin/asy'
env['PYTHON3']   = '/usr/local/bin/python3'

######################################################################
# Builders
######################################################################

#Create tex from noweb
env.Append(BUILDERS = {'NWtoTeX' : Builder(action='$WEAVE -filter \'sed "/^@use /s/_/\\\\_/g;/^@defn /s/_/\\\\_/g"\' -n -delay $SOURCES > $TARGET', src_suffix='.nw', suffix='.tex')})

#Create py from noweb
env.Append(BUILDERS = {'NWtoPy' : Builder(action='$TANGLE -R${TARGET.file} $SOURCES > $TARGET', src_suffix='.nw', suffix='.py')})

######################################################################
# Documentation
######################################################################

transtex = env.NWtoTeX('TransportPDECauchy')
env.Depends(transtex, 'Disclaimer.tex')
transpdf = env.PDF(transtex)

fdtex = env.NWtoTeX('FiniteDifferences')
disclaimer = env.NWtoTeX('Disclaimer')
fdtest = env.NWtoTeX('FDTest')
fdcoeff = env.NWtoTeX('FDCoefficients')
env.Depends(fdtex, ['Disclaimer.tex', 'FDTest.tex', 'FDCoefficients.tex'])
fdpdf = env.PDF(fdtex)

pdf = [fdpdf, transpdf]

######################################################################
# Python files
######################################################################

TransportPDECauchy = env.NWtoPy(source=['TransportPDECauchy.nw', 'Disclaimer.nw'],
		                target='TransportPDECauchy.py')

AdvTransport1D = env.NWtoPy(source=['TransportPDECauchy.nw', 'Disclaimer.nw'],
		            target='AdvTransport1D.py')


DiffTransport1D = env.NWtoPy(source=['TransportPDECauchy.nw', 'Disclaimer.nw'],
		             target='DiffTransport1D.py')

FiniteDifferences = env.NWtoPy(source=['FiniteDifferences.nw', 'FDTest.nw', 'Disclaimer.nw', 'FDCoefficients.nw'],
		             target='FiniteDifferences.py')

sources = [TransportPDECauchy,
           AdvTransport1D,
           DiffTransport1D,
           FiniteDifferences]

######################################################################
# Default targets
######################################################################

env.Default([sources, pdf])






			    
		


