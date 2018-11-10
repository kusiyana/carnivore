#from lxml import etree
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import shapely.geometry
from shapely.prepared import prep
#from pysal.esda.mapclassify import Natural_Breaks as nb
from descartes import PolygonPatch
import fiona
from itertools import chain
import mpl_toolkits.basemap.pyproj as pyproj # Import the pyproj module
import csv
import shapefile


arc1960=pyproj.Proj("+init=EPSG:21036")
#arc1960=pyproj.Proj("+init=EPSG:4326")


shp = fiona.open('/Users/admin/Dropbox/CODING/PYTHON/sites/tango_with_django_project/geofiles/relions/PAs_UTM_1.shp')
bds = shp.bounds
shp.close()
extra = 0.01


ll = arc1960(bds[0], bds[1], inverse=True)
ur = arc1960(bds[2], bds[3], inverse=True)

coords = list(chain(ll, ur))
w, h = coords[2] - coords[0], coords[3] - coords[1]


#load in national parks area
map = Basemap(
	llcrnrlon=coords[0] - extra * w, 
	llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,
    resolution='i')

baseLocation = '/Users/admin/Dropbox/CODING/PYTHON/sites/tango_with_django_project/geofiles/shapefiles/'
shapeFileBase = 'HR_mod'
shapeFileBody = baseLocation + shapeFileBase + '_'
shapeFileExtension = '.shp'

shapeFileString = shapeFileBody + '2'
map.readshapefile(shapeFileString, 'lions3', color='red')
with fiona.open(shapeFileString + shapeFileExtension) as fiona_collection:
	sumAbundance = 0
	shapefile_record = fiona_collection.next()
	shape = shapely.geometry.asShape(shapefile_record['geometry'])
	with open('shapefiles/lionDensities.csv', 'rb') as f:
		reader = csv.reader(f, delimiter=';')
		for row in reader:
			point = shapely.geometry.Point(float(row[6]), float(row[7]))
			if shape.contains(point):
				x,y = map(float(row[6]), float(row[7]))
				map.plot(x, y, 'bo', markersize=2)
				sumAbundance = sumAbundance + float(row[5])

				#print sumAbundance				

sf = shapefile.Reader(shapeFileString + shapeFileExtension)
shapes = sf.shapes()
shapesNP = np.array(shapes[0].points).T
centroid = sum(shapesNP[0]) / len(shapesNP[0]), sum(shapesNP[1]) / len(shapesNP[0])
xC,yC = map(float(centroid[0]), float(centroid[1]))
map.plot(xC, yC, 'bo', markersize=12)
plt.show()




for shape in shapes:
	for vertex in shape.points:
		print vertex[0]
		break

		#x = [p[0] for p in points]
		#y = [p[1] for p in points]
		#centroid = (sum(x) / len(points), sum(y) / len(points))

	#for info, shape in zip(m.lions_info, m.lions):
	#x, y = zip(*shape) 
	#x, y = zip(*lions[0]) 
	#m.plot(x, y, marker=None,color='m')


#with fiona.open("testGeo2.shp") as fiona_collection:
#	shapefile_record = fiona_collection.next()
#	shape = shapely.geometry.asShape( shapefile_record['geometry'] )
#	point = shapely.geometry.Point(35.2, -1.3)
#	if shape.contains(point):
#		print "Found shape for point."
