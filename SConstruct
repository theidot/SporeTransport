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
env.Append(BUILDERS = {'NWtoTeX' : Builder(action='$WEAVE -filter \'sed "/^@use /s/_/\\\\_/g;/^@defn /s/_/\\\\_/g"\' -n -delay $SOURCE > $TARGET', src_suffix='.nw', suffix='.tex')})

#Create py from noweb
env.Append(BUILDERS = {'NWtoPy' : Builder(action='$TANGLE -R${TARGET.file} $SOURCE > $TARGET', src_suffix='.nw', suffix='.py')})

######################################################################
# Documentation
######################################################################

tex = env.NWtoTeX('TransportPDECauchy')
pdf = env.PDF(tex)
pdf = env.Depends(pdf, [tex])

######################################################################
# Python files
######################################################################

TransportPDECauchy = env.NWtoPy(source='TransportPDECauchy.nw',
		                target='TransportPDECauchy.py')

AdvTransport1D = env.NWtoPy(source='TransportPDECauchy.nw',
		            target='AdvTransport1D.py')


DiffTransport1D = env.NWtoPy(source='TransportPDECauchy.nw',
		             target='DiffTransport1D.py')

sources = [TransportPDECauchy, AdvTransport1D, DiffTransport1D]

######################################################################
# Default targets
######################################################################

env.Default([sources, pdf])






			    
		


