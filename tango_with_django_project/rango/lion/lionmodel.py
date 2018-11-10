				
#!/usr/bin/python
# Filename: lion.py
from pylab import *
from rango.models import Pride
from rango.models import Lion
from rango.models import Trajectory

from django.db.models import Count
import random
import math
import numpy	
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
from scipy.stats import norm

class lion(object):
	max_lions_per_pride = 30
	lionMatrixSize = 100
	prideMatrixSize = 100
	time_unit = 1 # day
	max_movement_per_time_unit = 100 # thousands of degrees
	min_movement_per_time_unit = 0
	degreeScaleFactor = 1000 # factor by which degrees specified in "max_movement_per_time_unit" is scaled
	median_survival_age = 5
	risk_dying_per_day_day = 0.00044
	prideName = ''
	newPrideId = 0
	xlimit = 50
	ylimit = 50
	scaleLionFactor = 4 #factor by which shapefile lions are scaled to create "unborn" population

	#shapefile declarations
	baseLocation = '/Users/Hayden/Dropbox/CODING/PYTHON/sites/tango_with_django_project/geofiles/shapefiles/'
	shapeFileBase = 'HR_mod'
	shapeFileString = baseLocation + shapeFileBase + '_'
	shapeFileExtension = '.shp'

	lionDensityFile = baseLocation + 'lionDensities.csv'
	numberLionsAlive = 0 # number of lions alive


	numPossibleLions = 30
	timeSteps = 10
	parameterArrayLength = 14 #0. lionID, 1.parent_m, 2.parent_f, 3. prideId, 4.name, 5. age, 6. sex, 7. satiety, 8. roving 9. alive, 10. pregnant, 11. pregnancy duration, 12. 


	maleSurvivalArray = np.array([0.6, 0.75, 0.5, 0.6, 0.6, 0.64, 0.64, 0.59, 0.56, 0.53, 0.5, 0.47, 0.44, 0.41, 0.38, 0.35, 0]) #ages 0 - 17 assumes year on year value
	maleReproductionArray = np.array([0, 0, 0, 0, 0.5, 0.75, 1, 1, 1, 0.75, 0.5, 0.5, 0.5, 0.25, 0.1, 0.1, 0.1, 0])

	femaleSurvivalArray = np.array([0.57, 0.74, 0.8, 0.88, 0.88, 0.9, 0.9, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.1, 0])
	femaleReproductionArray = np.array([0, 0, 0, 0.25, 0.75, 1, 1,  1, 1, 1, 1, 0.75, 0.5, 0.25, 0.1, 0, 0, 0])

	prideArray = np.array([3])

	def initialiseLions2(self):
		"Initialise lion matrix from starting parameters"
		lionMatrixLength = self.numPossibleLions* self.timeSteps
		lionParameters = np.zeros((self.numPossibleLions, 10), dtype=np.int)
		lionCoords = np.zeros((self.numPossibleLions, 2))
		lionCount = self.shapefileLions(1)
		centroid = self.centroid(1)
		for lion in range(0, lionCount):
			lionParameters[lion][0] = lion
			lionParameters[lion][4] = 3 # pride ID
			lionParameters[lion][5] = 365 * 2 # age (days)
			lionParameters[lion][6] = randint(1,3) #1 = male, 2 = female
			lionParameters[lion][7] = 10 #10 = fully satieted, 0 = starving
			lionParameters[lion][9] = 1
			lionCoords[lion][0] = centroid[0]
			lionCoords[lion][1] = centroid[1]
		print lionCoords
		#lionParameters[0][6] = 1
		#lionParameters[1][6] = 2
		self.moveLions2(lionCoords, lionParameters)
		self.setAliveLions(lionParameters)
		self.breedLions2(lionParameters)
		print self.reproductiveProbability(6205, 2)
		print self.reproductiveProbability(2400, 1)

		#print'{:6f}'.format(self.reproductiveProbability(2300, 1))
		
		return lionCoords


	def setAliveLions(self, lionParameters):
		"Return number of alive lions from lion paramater matrix"
		numberLionsAlive = np.sum(lionParameters, axis = 0)
		self.numberLionsAlive = numberLionsAlive


	def moveLions2(self, lionCoords, lionParameters):
		"Loop through n lions in database and move each one"
		#np.copyto(newLionMatrix, lionMatrix)
		numberAlive = np.sum(lionParameters, axis = 0)
		print 'number alive is ' + str(numberAlive[9])
		for lion in range(0, numberAlive[9]):
			lionCoords[lion][0] = lionCoords[lion][0] + float((random.randint(self.min_movement_per_time_unit, self.max_movement_per_time_unit)))/self.degreeScaleFactor
			lionCoords[lion][1] = lionCoords[lion][1] + float((random.randint(self.min_movement_per_time_unit, self.max_movement_per_time_unit)))/self.degreeScaleFactor
		return (lionCoords)



	def getBreedingPair(self, lionParameters):
		"""
		Retreive pair of breeding lions from array
		"""
		aliveLions = lionParameters[np.where(lionParameters[:,9] == 1)]
		femaleLions = aliveLions[np.where(aliveLions[:,6] == 2)]
		maleLions = aliveLions[np.where(aliveLions[:,6] == 1)]

		#select male lion



	def breedLions2(self, lionParameters):
		"Breed lions with criterion"
		aliveLions = lionParameters[np.where(lionParameters[:,9] == 1)]
		femaleLions = aliveLions[np.where(aliveLions[:,6] == 2)]
		maleLions = aliveLions[np.where(aliveLions[:,6] == 1)]
		print lionParameters

		lionCondition = 1
		print 'lion condition' + str(lionCondition)
		if lionCondition:
			litterSize = self.calcLitterSize()
			print 'litter size is ' + str(litterSize)
			data = np.array(range(1,7))
			print data
		#aliveIndexes = np.where(lionParameters[:,9])[0]
		#for lion in aliveIndexes:
	#		print lion

		print 'alive lions'
		print str(aliveLions)
		print 'female lions'
		print str (femaleLions)
		print 'male lions'
		print str (maleLions)




	def calcLitterSize(self):
		"Calculate litter size for breeding female for given mating event"
		rand = randint(0,100)
		if rand > 0 and rand < 6:
			cubs = 1
		elif rand >= 6 and rand < 30:
			cubs = 2
		elif rand >= 30 and rand < 70:
			cubs = 3
		elif rand >= 70 and rand < 95:
			cubs = 4
		elif rand >= 95 and rand < 99:
			cubs = 5
		else:
			cubs = 6
		return cubs


	def reproductiveProbability(self, ageDays, sex):
		"""
		Return probability of male reproduction given age
		- gives reproduction probability per day
		parameters: ageDays - number of days since birth
					sex - male (1) or female (2)
		output: reproductive probability per day for given sex
		"""
		if sex is 1: #male
			repArray = self.maleReproductionArray
		else:
			repArray = self.femaleReproductionArray
		index = int(round(ageDays / 365, 0))
		if repArray[index] == 1:
			normalisedNumber = 0.9999
		else:
			normalisedNumber = repArray[index]

		dailyReproductionProbability = 1 - (pow(10, (log10(1 - normalisedNumber )) / 365))
		return (dailyReproductionProbability)

	def survivalProbability(self, ageDays, sex):
		"""
		Return survival probability of lions given age
		- gives survival probability per day
		parameters: ageDays - number of days since birth
					sex - male (1) or female (2)
		output: survival probability per day for given sex
		"""
		if sex is 1: #male
			repArray = self.maleSurvivalArray
		else:
			repArray = self.femaleSurvivalArray
		index = int(round(ageDays / 365, 0))	
		dailySurvivalProbability = pow(10, (log10(repArray[index]) / 365))
		return (dailySurvivalProbability)










	def initialisePrides(self):
		"Initialise prides if none exist in database."
		Pride.objects.all().delete()
		for i in range (0,lion.prideMatrixSize):
			#print (i)
			prideName = "pride" + str(i + 1)
			posx = 0 #random.randint(0, lion.xlimit)
			posy = 0 #random.randint(0, lion.ylimit)
			#print (prideName)
			pride_list = Pride.objects.all
			P = Pride.objects.get_or_create(name=prideName, posx = posx, posy = posy, alive = 0)[0]
			P.save()

		pride_list = Pride.objects.all
		return 1


	def initialiseLions(self):
		Lion.objects.all().delete()
		Trajectory.objects.all().delete()

		for i in range (0, self.lionMatrixSize):
			lionName = "lion" + str(i + 1)

			#pride = Pride.objects.order_by('?').first()			
			self.lion_dict = {'pride': 0}
			self.lion_dict['age'] = 0
			self.lion_dict['sex'] = 1
			self.lion_dict['alive'] = 0
			self.lion_dict['died_how'] = 0
			self.lion_dict['satiety'] = 0 # out of 10
			self.lion_dict['roving'] = 0
			self.wildebeest_dict = {'availability': 0}
			L = Lion.objects.get_or_create(name=lionName, age=self.lion_dict['age'], sex=self.lion_dict['sex'], posx =  0, posy = 0, satiety = self.lion_dict['satiety'], roving = self.lion_dict['roving'], parent=1)[0]
			L.save()

		def buildLionsFromShapefile(self):
			print 'test'
			#cheese_blog = Blog.objects.get(name="Cheddar Talk")

		return 1


	def shapefileLions(self, shapefileIndex):
		"Count lions from single shapefile given pixel density information"
		shapeFileBody = self.baseLocation + self.shapeFileBase + '_'
		shapeFileString = shapeFileBody + str(int(shapefileIndex))
		with fiona.open(shapeFileString + self.shapeFileExtension) as fiona_collection:
			sumAbundance = 0
			shapefile_record = fiona_collection.next()
			shape = shapely.geometry.asShape(shapefile_record['geometry'])
			with open(self.lionDensityFile, 'rb') as densityFile:
				reader = csv.reader(densityFile, delimiter=';')
				for row in reader:
					point = shapely.geometry.Point(float(row[6]), float(row[7]))
					if shape.contains(point):
						sumAbundance = sumAbundance + float(row[5])
						#print sumAbundance				
		return int(round(sumAbundance))


	def killAllLions(self):
		 Lion.objects.all().delete()
		 Pride.objects.all().delete()


	def makeNewLion(self, prideId = None, age = 0, centroid = [0,0], aliveStatus = 1):
		"Initialise lion population if none exists in database. Writes lion object to database"
		#if prideId < 1:
		#	pride = Pride.objects.order_by('?').first()
		#else:
		try:
			pride = Pride.objects.get(name = 'pride' + str(prideId))
		except Pride.DoesNotExist:
			pride = lambda: None
			pass

		lion = Lion.objects.filter(pride_id__isnull = True, alive = 0).first()
		lion.posx= centroid[0]
		lion.posy = centroid[1]
		lion.pride_id = pride.id
		lion.age = age
		lion.alive = aliveStatus
		pride.alive = aliveStatus
		#pride.id = prideId
		lion.save()
		pride.save()

		return 1
		
		# end of initialise


	def makeNewPride(self):
		 	try:
				latestPrideId = Pride.objects.latest('id').id
				print 'latest pride id'
				print latestPrideId
			except:
				latestPrideId = 1
				pass

			prideName = "pride" + str(latestPrideId + 1)
			P = Pride(name=prideName, posx=50, posy=50)
			P.save()
			self.prideName = prideName
			self.newPrideId = P.id
			return P.id


	def movePrides(self):
		"Move all prides around within the stipulated area by x and y"
		#q = Lion.objects.annotate(Count('name'))
		lionEntries = Pride.objects.filter(alive = 1)
		context_dict = {'old': 0, "new": 0}
		prideCount = Pride.objects.filter(alive = 1).count()
		oldPosition = numpy.zeros((prideCount + 1, 2))
		newPosition = numpy.zeros((prideCount + 1, 2))

		i = 0
		for n in lionEntries:
			self.rand_seed = random.seed()
			posxNew = n.posx + random.randint(self.min_movement_per_time_unit, self.max_movement_per_time_unit) * random.randint(-1,1)
			if posxNew < 0:
				posxNew = 0
			
			if posxNew > self.park_width:
				posxNew = self.park_width
			
			posyNew = n.posy + random.randint(self.min_movement_per_time_unit, self.max_movement_per_time_unit) * random.randint(-1,1)

			if posyNew < 0:
				posyNew = 0
			
			if posyNew > self.park_length:
				posyNew = self.park_length

			oldPosition[i][0] = n.posx
			oldPosition[i][1] = n.posy

			newPosition[i][0] = posxNew
			newPosition[i][1] = posyNew
			
			context_dict = {'old': oldPosition, "new": newPosition}
			#n.posx = posxNew
			#n.posy = posyNew
			#n.save()
			i = i + 1
		return context_dict

	def moveLions(self):
		"Loop through n lions in database and move each one"
		lionEntries = Lion.objects.filter(alive = 1)
		for lion in lionEntries:
			xNew = lion.posx + float((random.randint(self.min_movement_per_time_unit, self.max_movement_per_time_unit)))/self.degreeScaleFactor
			yNew = lion.posy + float((random.randint(self.min_movement_per_time_unit, self.max_movement_per_time_unit)))/self.degreeScaleFactor

			lion.posx = xNew
			lion.posy = yNew
			lion.save()
		return (1)


	def writeTrajectory(self, elapsedTime = 1, dt = 1):
		"Write trajectories to database at time t"
		i = 0
		print ('i is' + str(i))
		lionEntries = Lion.objects.all()
		i = 0
		for lion in lionEntries:
			trajectory = Trajectory()
			trajectory.age = lion.age
			trajectory.lion_id = lion.id
			trajectory.posx = lion.posx
			trajectory.posy = lion.posy
			trajectory.roving = lion.roving
			trajectory.alive = lion.alive		
			trajectory.satiety = lion.satiety
			trajectory.dt = dt
			trajectory.elapsedtime = elapsedTime
			print ('i is' + str(i))
			i += 1
			trajectory.save()


		return (lionEntries)



	def breedPride(self):
		"Breed pride probabilistically in terms of food supply"
		breed_probability = (1 - 1/(1 + math.exp(self.wildebeest_dict['availability'] - 10)))
	#	print 'breed_probability is ' , breed_probability
		self.rand_seed = random.seed()
		rand = random.random()
		if rand >= breed_probability:
			result = 1
		else:
			result = 0
		return result
	
	
	def deathByOldAgePride(self):
		death_probability_scale= ((1 - 1/(1 + math.exp(self.lion_dict['age'] - self.median_survival_age))) + 1) * self.risk_dying_per_day_day
		
		prob_of_death_at_age = 1 - math.exp(-death_probability_scale * self.lion_dict['age'] * 365 )
		return 1
	#	print 'death probability is ' , prob_of_death_at_age
	
	def dIEdR(self, iE1, iE2):
		prideCount = numpy.shape(iE1)[0]
		dIEMatrix = numpy.zeros((prideCount))
		i = 0
		for dIE in dIEMatrix:
			j = 0
			for dIE in dIEMatrix:
				if j != i:
					l = 1

					#dIEMatrix[i] = -1 * (iE1[i] - iE2[i])
				j = j+1
			i = i+1
		print (dIEMatrix)
		return 1

	def interactionEnergy(self, positionMatrix):
		prideCount = numpy.shape(positionMatrix)[0]
		iE = numpy.zeros((prideCount, prideCount))
		i = 0
		for position1 in positionMatrix:
			j = 0
			for position2 in positionMatrix:
				if j != i:
					iE[i, j] = -1 * (1/(((positionMatrix[i][0] - positionMatrix[j][0]) **2) + ((positionMatrix[i][1] - positionMatrix[j][1]) **2) ** 0.5))
				j = j+1
			i = i+1
		return(iE)
		print (iE)



	def centroid(self, shapefileIndex):
		"Calculate centre of mass of a shapefile polygon"
		shapeFileBody = self.baseLocation + self.shapeFileBase + '_'
		shapeFileString = shapeFileBody + str(int(shapefileIndex))
		sf = shapefile.Reader(shapeFileString + self.shapeFileExtension)
		shapes = sf.shapes()
		shapesNP = np.array(shapes[0].points).T
		centroid = (sum(shapesNP[0]) / len(shapesNP[0]), sum(shapesNP[1]) / len(shapesNP[0]))
		return centroid


	def PolygonArea(corners):
		"Calculate area of a shapefile polygon"
		n = len(corners) # of corners
		area = 0.0
		for i in range(n):
			j = (i + 1) % n
			area += corners[i][0] * corners[j][1]
			area -= corners[j][0] * corners[i][1]
		area = abs(area) / 2.0
		return area


	def bestPolygonRadius(area):
		"Calculate the circle that best matches the polygonarea"
		radius = math.sqrt(area/math.pi)
		return radius


	def basemap(test):
		arc1960=pyproj.Proj("+init=EPSG:21036")
		shp = fiona.open('/Users/admin/Dropbox/CODING/PYTHON/sites/tango_with_django_project/geofiles/relions/PAs_UTM_1.shp')
		bds = shp.bounds
		shp.close()
		extra = 0.01
		ll = arc1960(bds[0], bds[1], inverse=True)
		ur = arc1960(bds[2], bds[3], inverse=True)

		coords = list(chain(ll, ur))
		w, h = coords[2] - coords[0], coords[3] - coords[1]
		map = Basemap(
	llcrnrlon=coords[0] - extra * w, 
	llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,
    resolution='i')
		plt.show()
		return 1




#	def expendEnergy(self):
		

#	def feedPride(self)
#		"Feed a pride of lions."
		
		

# End of class lion
#end of module lion.py
