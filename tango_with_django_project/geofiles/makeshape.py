import shapefile
import sys
import os
import shutil

def find_column(fields, column_name):
    for fieldno in range(len(fields)):
        if ( fields[fieldno][0] == column_name ):
            print("Column number: {0} is {1}".format(fieldno,column_name))
            return fieldno - 1
    print ("Sorry ... I could not find a field named " + column_name + "\n");
    sys.exit(-1)


def write_named_shapes(inputshp, outputdir, outputshp):
    sf = shapefile.Reader(inputshp);
    shapes = sf.shapes() # shp file contents
    fields = sf.fields   # headers
    records = sf.records() # dbf file contents
    FULLNAME = find_column(sf.fields, 'FULLNAME')
    
    for shapeno in range(len(shapes)):
        shapename = records[shapeno][FULLNAME]
        if ( len(shapename.rstrip()) > 0 ):
            print(str(shapeno) + " -> " + shapename)
    
    sw = shapefile.Writer(shapefile.POLYGON)
    sw.fields = sf.fields
    for shapeno in range(len(shapes)):
        shapename = records[shapeno][FULLNAME]
        if ( len(shapename.rstrip()) > 0 ):
            sw.records.append(records[shapeno])
            sw.shapes().append( shapes[shapeno] )
    
    shutil.rmtree(outputdir, ignore_errors=True)
    os.mkdir(outputdir)
    filename = outputdir + "/" + outputshp
    sw.save(filename)
    shutil.copyfile(inputshp + ".prj", filename+".prj")
    print(filename + " created");


if __name__ == '__main__' :
    datadir = "../data/40027_Cleveland_County/"
    write_named_shapes( datadir + "/tl_2009_40027_areawater",
                        datadir + "/ch03", "cleveland_county_waterbodies" )
