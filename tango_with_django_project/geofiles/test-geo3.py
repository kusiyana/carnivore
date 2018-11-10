import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

m = Basemap(llcrnrlon=-1.54,llcrnrlat=34.72,urcrnrlon=-1.26,urcrnrlat=35.16,
             resolution='i', projection='mill')

m.drawcoastlines()
m.fillcontinents()

m.drawmapboundary(fill_color='aqua')

s = m.readshapefile('testGeo2', 'Project_Name')

for xy, info in zip(m.Project_Name, m.Project_Name_info):
    if info['Status'] == 'Completed':
        poly = Polygon(xy, facecolor='red', alpha=0.4)
        plt.gca().add_patch(poly)
    elif info['Status'] == 'in progress':
        poly = Polygon(xy, facecolor='green', alpha=0.4)
        plt.gca().add_patch(poly)
    else:
        print info['Status'] 

plt.legend()
plt.show()