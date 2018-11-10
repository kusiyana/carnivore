from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import shapefile as shp

map = Basemap(llcrnrlon=0,llcrnrlat=0,urcrnrlon=90,urcrnrlat=90, resolution='l', projection='mill') #, lat_0 = 39.5, lon_0 = 1)

sf = shp.Reader("testhayden.shp")

for rec in enumerate(sf.records()[:3]):
	print rec[0] + 1, ": ", rec[1]
	point = feature.shape.points[0]
	rec = feature.record[0]
	print point[0], point[1], rec


#plt.figure()
#for shape in sf.shapeRecords():
#    x = [i[0] for i in shape.shape.points[:]]
#    y = [i[1] for i in shape.shape.points[:]]
#    plt.plot(x,y)
#plt.show()
#map.drawmapboundary(fill_color='aqua')
#map.fillcontinents(color='#ddaa66',lake_color='aqua')

#map.readshapefile('testhayden', 'comarques')

#plt.show()