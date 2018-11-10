import numpy as np
import pandas as pd
import sys
sys.path.append('/Users/Hayden/Dropbox/CODING/PYTHON/sites/tango_with_django_project/rango/lion')
#sys.path.append('/Users/Hayden/Dropbox/CODING/PYTHON/sites/tango_with_django_project/rango')

import lionmodel
#lion = np.array([[0],[0], [1, 1, 0, 1, 'lion1', 1, 1, 1, 0, 0, 0, 1]])


numLions = 5
timeSteps = 10
lionMatrixLength = numLions* timeSteps
parameterArrayLength = 14

lion = np.zeros((lionMatrixLength, numLions, 14)) # lionID, time, parameters (1 - 14)



for t in range(0, lion.shape[0]):
	for lionCount in range(0, lion.shape[1]):
		print lion[t][lionCount][0]




#liondF = pd.DataFrame(lionFull, columns=[['lion_id', 'time'], 'miscellaneous'])
#print liondF.loc['lion_id']
#lionh = np.array([['lion_id'],['t'], ['dt', 'lion_id', 'parent_id', 'pride_id', 'name', 'age', 'sex', 'satiety', 'posx', 'posy', 'roving', 'alive']])