# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from pylab import *
sys.path.append('/Users/Hayden/Dropbox/CODING/PYTHON/sites/tango_with_django_project/rango/lion')
import lionmodel
from rango.models import Category
from rango.models import Page
from rango.models import Pride
from rango.models import Lion
from rango.models import Trajectory
import json 
    
def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    category_list = Category.objects.order_by('name')[:5]
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Render the response and return to the client.
    return render_to_response('rango/index.html', context_dict, context)
  
def showPrides(request):
    "Show list of all lion prides in database"
    context = RequestContext(request)
    pride_list = Pride.objects.all
    context_dict = {'prides': pride_list}
    return render_to_response('rango/show_prides.html', context_dict, context)


def showLions(request):
    "Show list of all lions in database"
    context = RequestContext(request)
    lion_list = Lion.objects.filter(alive = 1)
    context_dict = {'lions': lion_list}
    return render_to_response('rango/show_lions.html', context_dict, context)



def lion(request):
    context = RequestContext(request)
    lion = lionmodel.lion()
    positions = lion.movePrides()
    print (positions)
    interactionEOld = lion.interactionEnergy(positions['old'])
    interactionENew = lion.interactionEnergy(positions['new'])
    iE = lion.dIEdR(positions['old'], positions['new'])
    return 1


def initialise2(request):
    context = RequestContext(request)
    lion = lionmodel.lion()
    lion.initialiseLions2()
    
    context_dict = {'lionCount': 2} 
    return render_to_response('rango/initialise.html', context_dict, context)


def initialise(request):
    context = RequestContext(request)
    lion = lionmodel.lion()
    lion.initialisePrides()
    lion.initialiseLions()
    lions = Lion.objects.all()
    lionCount = Lion.objects.all().count()
    print 'lion count is ' + str(lionCount)
    context_dict = {'lionCount': lionCount} 
    return render_to_response('rango/initialise.html', context_dict, context)


def buildLionsFromShapefiles(request, shapefileIndex = 3):
    "initialise individual lions for a given shapefile"
    context = RequestContext(request)
    lion = lionmodel.lion()
    lionCount = lion.shapefileLions(shapefileIndex)
    centroid = lion.centroid(shapefileIndex)
    for i in range(1, (lionCount + 1)):
        lion.makeNewLion(shapefileIndex, centroid = centroid, aliveStatus = 1, age = 2)
    try:
        lions = Lion.objects.filter(alive = 1)
    except Lion.DoesNotExist:    
        pass

    #create extra "not yet living" lions
    for j in range(1, (lion.scaleLionFactor * lionCount) + 1):
        lion.makeNewLion(shapefileIndex, age = 0, centroid = centroid, aliveStatus = 0)

    context_dict = {'lions': lions, 'lionCount': lionCount, 'shapefileIndex': shapefileIndex, 'centroid': centroid}
    return render_to_response('rango/build_lions_from_shapefiles.html', context_dict, context)



def runSimulation(request):
    context = RequestContext(request)
    lion = lionmodel.lion()
    tStart = 0
    tEnd = 100
    t = tStart
    dt = 1
    lion.writeTrajectory(t) # initialise trajectories at t = 0
    t += dt
    while (t < tEnd):
        lion.moveLions()
        lion.writeTrajectory(t)
        t += dt

    context_dict = {'status': 'running', 'tStart': tStart, 'tEnd': tEnd, 'dt': dt, 'maxMovement': lion.max_movement_per_time_unit, 'minMovement': lion.min_movement_per_time_unit}
    return render_to_response('rango/run_simulation.html', context_dict, context)

def viewSimulation(request):
    context = RequestContext(request)
    context_dict = {'status': 1}
    return render_to_response('rango/view_simulation.html', context_dict, context)









def deleteAll(request):
    "delete all prides"
    context = RequestContext(request)
    lion = lionmodel.lion()
    lion.killAllLions()
    return redirect('lions.views.showPrides', quizNumber=3)



	
    for i in range(0,1):
        lion.movePrides()
     #   print 'jo'
       # lion.movePrides()
        # loop through each lion in the database
		#print lionvar.lion_dict
        #prideName = lion.makeNewPride()



        #prideTest = Pride.objects.get(name='wtf')
       

		#lionWriteTest = 	#end for
        #b = Book.objects.all()[0]
        #b.authors.count()
        #lion_x_array = []
        #t = []
	
    #for i in range(0, 30):
	#	lionvar.movePride()
#		lionvar.breedPride()
		#lionvar.deathByOldAgePride()
		#lion_x_array.append(lionvar.pride_dict['posx'])
		#t.append(i)
		#print lionvar.pride_dict['posx'], lionvar.pride_dict['posy']
	#end for

	#print lion_x_array
#	figure()
#	plot(1)
#	plot(lion_x_array, lion_x_array)
#	plot(t, Z, label='Zombies')
#	show()


	context_dict = {'category': 'test'}
	#print context_dict['category']
	return render_to_response('rango/lion.html', context_dict, context)


def viewTrajectories(request, elapsedTime = 1):
    context = RequestContext(request)
    try:
        trajectories = Trajectory.objects.filter(elapsedtime=elapsedTime)
        contextDict = {'trajectories': trajectories}

    except Trajectory.DoesNotExist:
        pass

    lion = lionmodel.lion()

    #print contextDict
    return render_to_response('rango/view_trajectories.html', contextDict, context)


def ajaxTrajectories(request, elapsedTime = 2):
    "Provide trajectories for successive times to other scripts - called by Ajax"
    context = RequestContext(request)
    trajectories = Trajectory.objects.filter(elapsedtime=elapsedTime, alive=1)
    trajectoryLength = len(trajectories)
    contextDict = {'trajectories': trajectories, "trajectoryLength": trajectoryLength}
    return render_to_response('rango/ajax_trajectories.html', contextDict, context)
    
def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = category_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('rango/category.html', context_dict, context)
    
    
from rango.forms import CategoryForm
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/add_category.html', {'form': form}, context)


from rango.forms import PageForm
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_page.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'form': form},
             context)
