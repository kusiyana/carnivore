from pylab import *

import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import shapefile


fig = figure( figsize=(6,3.75) )
ax = fig.add_subplot(111)

sf = shapefile.Reader('testhayden.shp')
recs    = sf.records()
shapes  = sf.shapes()
Nshp    = len(shapes)

for nshp in xrange(Nshp):
    ptchs   = []
    pts     = array(shapes[nshp].points)
    prt     = shapes[nshp].parts
    par     = list(prt) + [pts.shape[0]]
    for pij in xrange(len(prt)):
        ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))
    ax.add_collection(PatchCollection(ptchs,facecolor='none',edgecolor='k', linewidths=.2))


ax.set_xlim(-1.361,-1.491)
ax.set_ylim(34.73,34.84)
ax.set_aspect(1)
savefig( 'andrews_example.png', fmt='png', dpi=100)