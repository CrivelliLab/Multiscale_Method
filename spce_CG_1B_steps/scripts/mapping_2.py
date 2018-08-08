#
# Python codes to create CG coordinates from the atomistic GRO file by using
# information from the XML file and write a final mergaed GRO coordinate
#
# Requried python libraries: groio
# Masa Watanabe July 11th, 2018
#
#

from xml.dom import minidom
import groio

# parse an xml file by name
mydoc = minidom.parse('water.xml')
collection = mydoc.documentElement

# Get all the movies in the collection
movies = collection.getElementsByTagName("cg_bead")
movie2 = collection.getElementsByTagName("maps")

tuple1 = []
tuple2 = []
for movie in movies:
    #name = movie.getElementsByTagName('name')[0]
    #print ("Name: %s" % name.childNodes[0].data)
    type0 = movie.getElementsByTagName('type')[0]
    print ("Type: %s" % type0.childNodes[0].data)
    tuple1.append(type0.childNodes[0].data)
    mapping = movie.getElementsByTagName('mapping')[0]
    print ("Mapping: %s" % mapping.childNodes[0].data)
    beads = movie.getElementsByTagName('beads')[0]
    print ("Beads: %s" % beads.childNodes[0].data)
    line = beads.childNodes[0].data
    beads_comp = line.split(" ")
    for i in beads_comp:
        if((i != "") & (i !="\n")):
            tuple2.append(i)

# Get all the movies in the collection
tuple3 = []
for movie in movie2:
    weights = movie.getElementsByTagName('weights')[0]
    print ("weights: %s" % weights.childNodes[0].data)
    tuple3.append(weights.childNodes[0].data)

#print (tuple2)
#print (tuple3)

#comps = i.split(":")

#Read a gro file
title, gro_atoms, box = groio.parse_file("aa.gro")

#atoms - dictionary
# attributes: ['resid', 'resname', 'atom_name', 'atomid', 'x', 'y', 'z']
#"%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f"

resid =[]
resname = []
atoms = []
mass = tuple3[0].split(" ")
for x in tuple2:
    comp = x.split(":")
    resid.append(comp[0])
    resname.append(comp[1])
    atoms.append(comp[2])

#
# Dictionary for CG components
d ={}
d["resid"]=resid
d["resname"]=resname
d["atoms"] = atoms
d["mass"] = mass

CG_list=[]

comx = 0.0
comy = 0.0
comz = 0.0
tmass = 0.0

resid  = gro_atoms[0]["resid"]

atomid = 1

for x in gro_atoms:
    #print (x)
    j = False
    k = False

    # Creating CG Groups
    #resid  = x["resid"]

    #comx = 0.0
    #comy = 0.0
    #comz = 0.0
    #tmass = 0.0

    if(x["resid"] == resid):
        res    = x["resname"]
        CG_res = d["resname"]   # CG Mapping

        for x3 in CG_res:
            if(x3 == res): j = True

        if(j):
            #print ("YES")
            CG_atoms = d["atoms"]
            jj = 0
            #comx = 0.0
            #comy = 0.0
            #comz = 0.0
            #tmass = 0.0

            for x4 in CG_atoms:
                if(x["atom_name"] == x4):
                    #print (d["mass"][jj], x4)
                    tmass = tmass + float(d["mass"][jj])
                    comx  =  comx + float(d["mass"][jj]) * float(x["x"])
                    comy  =  comy + float(d["mass"][jj]) * float(x["y"])
                    comz  =  comz + float(d["mass"][jj]) * float(x["z"])
                jj = jj +1

        #print (comx/tmass,comy/tmass,comz/tmass)
        j = False
    else:
        #print (comx/tmass,comy/tmass,comz/tmass)
        cg = {}
        cg["resid"] = resid
        cg["resname"] = res
        cg["atom_name"] = tuple1[0]
        cg["atomid"] = atomid
        cg["x"] = comx/tmass
        cg["y"] = comy/tmass
        cg["z"] = comz/tmass

        CG_list.append(cg)

        atomid = atomid + 1

        comx = 0.0
        comy = 0.0
        comz = 0.0
        tmass = 0.0

        resid  = x["resid"]
        res    = x["resname"]
        CG_res = d["resname"]   # CG Mapping

        for x3 in CG_res:
            if(x3 == res): j = True

        if(j):
            #print ("YES")
            CG_atoms = d["atoms"]
            jj = 0
            #comx = 0.0
            #comy = 0.0
            #comz = 0.0
            #tmass = 0.0

            for x4 in CG_atoms:
                if(x["atom_name"] == x4):
                    #print (d["mass"][jj], x4)
                    tmass = tmass + float(d["mass"][jj])
                    comx  =  comx + float(d["mass"][jj]) * float(x["x"])
                    comy  =  comy + float(d["mass"][jj]) * float(x["y"])
                    comz  =  comz + float(d["mass"][jj]) * float(x["z"])
                jj = jj +1

        #print (comx/tmass,comy/tmass,comz/tmass)
        j = False

#print (comx/tmass,comy/tmass,comz/tmass)
#print (CG_list[0])

atomid = atomid + 1

cg = {}
cg["resid"] = resid
cg["resname"] = res
cg["atom_name"] = tuple1[0]
cg["atomid"] = atomid
cg["x"] = comx/tmass
cg["y"] = comy/tmass
cg["z"] = comz/tmass

CG_list.append(cg)

#atoms - dictionary
# attributes: ['resid', 'resname', 'atom_name', 'atomid', 'x', 'y', 'z']

#
# Write CG only gro file
# with open("CG.gro", "w") as f:
#    for line in groio.write_gro(title, CG_list, box):
#        print(line, end='', file=f)

OutFile1 = open("CG.gro", "w")
for line in groio.write_gro(title, CG_list, box):
	OutFile1.write(line)

OutFile1.close()

#Renumber the atoms to avoid number above 100 000
#atoms = groio.renumber(atoms)
# d.get("resname")
# d.keys()

# Combining CG and Atom GRO files
AA = gro_atoms+CG_list
# Sorting by Resid
BB = sorted(AA, key=lambda x: (x['resid']))

# Renumbering atomid
j = 1
for x in BB:
    x["atomid"] = j
    j = j + 1

#
# Write a merged gro file
#
OutFile = open("fileout.gro",'w')
for line in groio.write_gro(title, BB, box):
	OutFile.write(line)

OutFile.close()
