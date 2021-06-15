# Script automatically generated on 24-Oct-2018 at 16:17 by RootGen
# Simulation description: 


from part              import *
from material          import *
from section           import *
from assembly          import *
from step              import *
from interaction       import *
from load              import *
from mesh              import *
from optimization      import *
from job               import *
from sketch            import *
from visualization     import *
from connectorBehavior import *

# Some of the variables of interest
modelname = 'oakdoww';
mdb.models.changeKey(fromName='Model-1', toName=modelname)
# Rigid bar variables
rigid_bar = {
	"height"       : 6.000,
	"lateralDispl" : 1.000,
}
# Soil variables
soil = {
	"Lx_Ly" : 5.000,
	"depth" : 3.000,
	"rho"   : 203.945,
	"E"     : 20000000.000,
	"nu"    : 0.300,
	"phi"   : 25.000,
	"psi"   : 0.000,
	"c"     : 1500.000,
	"abs_plastic_strain" : 0.000
}
# Root varaibles
root = {
	"init_diam" : 0.47116,
	"seg_dl"    : 0.100,
	"rho"       : 0.000,
	"E"         : 2000000000.000,
	"nu"        : 0.300,
	"sigma_r"   : 15000000.000,
	"plastic_strain": 0.000
}
# =========================================

# Soil part creation
mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(soil["Lx_Ly"], soil["Lx_Ly"]))
mdb.models[modelname].Part(dimensionality=THREE_D, name='Soil', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['Soil'].BaseSolidExtrude(depth=soil["depth"], sketch=
    mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']
# =========================================

# Soil material and section creation and assignment
mdb.models[modelname].Material(name='SoilMaterial')
mdb.models[modelname].materials['SoilMaterial'].Density(table=((soil["rho"], ), ))
mdb.models[modelname].materials['SoilMaterial'].Elastic(table=((soil["E"], soil["nu"]), ))
mdb.models[modelname].materials['SoilMaterial'].MohrCoulombPlasticity(table=((soil["phi"], 0.0), ))
mdb.models[modelname].materials['SoilMaterial'].mohrCoulombPlasticity.MohrCoulombHardening(table=((soil["c"], soil["abs_plastic_strain"]), ))
mdb.models[modelname].materials['SoilMaterial'].mohrCoulombPlasticity.TensionCutOff(dependencies=0, table=((0.0, 0.0), ), temperatureDependency=OFF)
mdb.models[modelname].HomogeneousSolidSection(material='SoilMaterial', name='SoilSection', thickness=None)
mdb.models[modelname].parts['Soil'].SectionAssignment(offset=0.0, offsetField=
    '', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models[modelname].parts['Soil'].cells.findAt(((soil["Lx_Ly"]/2, soil["Lx_Ly"]/2, 
    soil["depth"]/2), ), )), sectionName='SoilSection', thicknessAssignment=FROM_SECTION)
# =========================================

# Root material creation
mdb.models[modelname].Material(name='RootMaterial')
mdb.models[modelname].materials['RootMaterial'].Density(table=((root["rho"], ), ))
mdb.models[modelname].materials['RootMaterial'].Elastic(table=((root["E"], root["nu"]), ))
mdb.models[modelname].materials['RootMaterial'].Plastic(table=((root["sigma_r"], root["plastic_strain"]), ))
# =========================================

# Rigid bar creation
mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(root["init_diam"]/2, rigid_bar["height"]))
mdb.models[modelname].Part(dimensionality=THREE_D, name='RigidBar', type=DISCRETE_RIGID_SURFACE)
mdb.models[modelname].parts['RigidBar'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']
# =========================================

# Rigid bar reference point, interesting points and surfaces creation
mdb.models[modelname].parts['RigidBar'].ReferencePoint(point=(0.0, 0.0, 0.0))

mdb.models[modelname].parts['RigidBar'].PartitionFaceByShortestPath(faces=
    mdb.models[modelname].parts['RigidBar'].faces.findAt(((0.0, rigid_bar["height"], 0.0), )), 
    point1=(-root["init_diam"]/2,rigid_bar["height"],0.0), point2=(root["init_diam"]/2,rigid_bar["height"],0.0))
mdb.models[modelname].parts['RigidBar'].PartitionEdgeByPoint(edge=
    mdb.models[modelname].parts['RigidBar'].edges.findAt((0.0, rigid_bar["height"], 0.0), ), point=(0.0, rigid_bar["height"], 0.0))

mdb.models[modelname].parts['RigidBar'].Surface(name='RigidBarBottomSurf', 
    side1Faces=mdb.models[modelname].parts['RigidBar'].faces.findAt(((0.0, 0.0, 0.0), )))
# =========================================

# Transform into a shell element
mdb.models[modelname].parts['RigidBar'].RemoveCells(cellList=mdb.models[modelname].parts['RigidBar'].cells)
# =========================================

# Root segments section and profile creation
#    - P-1s234 : root segment profile with diameter 1.234 m
#    - S-1s234 : root segment section with diameter 1.234 m
mdb.models[modelname].CircularProfile(name='P-0s00388', r=0.00194)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00388', poissonRatio=
    0.0, profile='P-0s00388', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00388', r=0.00194)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00388', poissonRatio=
    0.0, profile='P-0s00388', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00501', r=0.00250)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00501', poissonRatio=
    0.0, profile='P-0s00501', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00549', r=0.00274)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00549', poissonRatio=
    0.0, profile='P-0s00549', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00716', r=0.00358)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00716', poissonRatio=
    0.0, profile='P-0s00716', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00952', r=0.00476)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00952', poissonRatio=
    0.0, profile='P-0s00952', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01387', r=0.00694)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01387', poissonRatio=
    0.0, profile='P-0s01387', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01387', r=0.00694)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01387', poissonRatio=
    0.0, profile='P-0s01387', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01387', r=0.00694)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01387', poissonRatio=
    0.0, profile='P-0s01387', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01527', r=0.00763)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01527', poissonRatio=
    0.0, profile='P-0s01527', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01591', r=0.00796)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01591', poissonRatio=
    0.0, profile='P-0s01591', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01663', r=0.00832)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01663', poissonRatio=
    0.0, profile='P-0s01663', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01663', r=0.00832)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01663', poissonRatio=
    0.0, profile='P-0s01663', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01782', r=0.00891)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01782', poissonRatio=
    0.0, profile='P-0s01782', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01908', r=0.00954)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01908', poissonRatio=
    0.0, profile='P-0s01908', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02016', r=0.01008)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02016', poissonRatio=
    0.0, profile='P-0s02016', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02016', r=0.01008)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02016', poissonRatio=
    0.0, profile='P-0s02016', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02016', r=0.01008)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02016', poissonRatio=
    0.0, profile='P-0s02016', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02032', r=0.01016)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02032', poissonRatio=
    0.0, profile='P-0s02032', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02090', r=0.01045)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02090', poissonRatio=
    0.0, profile='P-0s02090', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02543', r=0.01272)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02543', poissonRatio=
    0.0, profile='P-0s02543', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02545', r=0.01273)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02545', poissonRatio=
    0.0, profile='P-0s02545', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02638', r=0.01319)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02638', poissonRatio=
    0.0, profile='P-0s02638', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02741', r=0.01371)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02741', poissonRatio=
    0.0, profile='P-0s02741', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02846', r=0.01423)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02846', poissonRatio=
    0.0, profile='P-0s02846', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02998', r=0.01499)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02998', poissonRatio=
    0.0, profile='P-0s02998', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03225', r=0.01613)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03225', poissonRatio=
    0.0, profile='P-0s03225', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03438', r=0.01719)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03438', poissonRatio=
    0.0, profile='P-0s03438', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03554', r=0.01777)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03554', poissonRatio=
    0.0, profile='P-0s03554', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03554', r=0.01777)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03554', poissonRatio=
    0.0, profile='P-0s03554', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03661', r=0.01831)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03661', poissonRatio=
    0.0, profile='P-0s03661', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03961', r=0.01980)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03961', poissonRatio=
    0.0, profile='P-0s03961', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04006', r=0.02003)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04006', poissonRatio=
    0.0, profile='P-0s04006', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04006', r=0.02003)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04006', poissonRatio=
    0.0, profile='P-0s04006', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04006', r=0.02003)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04006', poissonRatio=
    0.0, profile='P-0s04006', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04281', r=0.02140)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04281', poissonRatio=
    0.0, profile='P-0s04281', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04314', r=0.02157)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04314', poissonRatio=
    0.0, profile='P-0s04314', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04437', r=0.02219)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04437', poissonRatio=
    0.0, profile='P-0s04437', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04516', r=0.02258)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04516', poissonRatio=
    0.0, profile='P-0s04516', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04645', r=0.02322)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04645', poissonRatio=
    0.0, profile='P-0s04645', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04748', r=0.02374)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04748', poissonRatio=
    0.0, profile='P-0s04748', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04952', r=0.02476)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04952', poissonRatio=
    0.0, profile='P-0s04952', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05263', r=0.02631)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05263', poissonRatio=
    0.0, profile='P-0s05263', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05283', r=0.02642)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05283', poissonRatio=
    0.0, profile='P-0s05283', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05422', r=0.02711)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05422', poissonRatio=
    0.0, profile='P-0s05422', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05422', r=0.02711)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05422', poissonRatio=
    0.0, profile='P-0s05422', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05652', r=0.02826)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05652', poissonRatio=
    0.0, profile='P-0s05652', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05688', r=0.02844)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05688', poissonRatio=
    0.0, profile='P-0s05688', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06190', r=0.03095)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06190', poissonRatio=
    0.0, profile='P-0s06190', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06190', r=0.03095)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06190', poissonRatio=
    0.0, profile='P-0s06190', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06259', r=0.03129)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06259', poissonRatio=
    0.0, profile='P-0s06259', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06306', r=0.03153)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06306', poissonRatio=
    0.0, profile='P-0s06306', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06323', r=0.03162)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06323', poissonRatio=
    0.0, profile='P-0s06323', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06663', r=0.03331)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06663', poissonRatio=
    0.0, profile='P-0s06663', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06855', r=0.03427)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06855', poissonRatio=
    0.0, profile='P-0s06855', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07452', r=0.03726)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07452', poissonRatio=
    0.0, profile='P-0s07452', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07897', r=0.03948)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07897', poissonRatio=
    0.0, profile='P-0s07897', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07897', r=0.03948)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07897', poissonRatio=
    0.0, profile='P-0s07897', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s08136', r=0.04068)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s08136', poissonRatio=
    0.0, profile='P-0s08136', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s08185', r=0.04092)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s08185', poissonRatio=
    0.0, profile='P-0s08185', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s08266', r=0.04133)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s08266', poissonRatio=
    0.0, profile='P-0s08266', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s08685', r=0.04342)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s08685', poissonRatio=
    0.0, profile='P-0s08685', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s09512', r=0.04756)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s09512', poissonRatio=
    0.0, profile='P-0s09512', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s09819', r=0.04910)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s09819', poissonRatio=
    0.0, profile='P-0s09819', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s09819', r=0.04910)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s09819', poissonRatio=
    0.0, profile='P-0s09819', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s09860', r=0.04930)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s09860', poissonRatio=
    0.0, profile='P-0s09860', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s10552', r=0.05276)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s10552', poissonRatio=
    0.0, profile='P-0s10552', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s10552', r=0.05276)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s10552', poissonRatio=
    0.0, profile='P-0s10552', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s11004', r=0.05502)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s11004', poissonRatio=
    0.0, profile='P-0s11004', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s11267', r=0.05634)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s11267', poissonRatio=
    0.0, profile='P-0s11267', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s11633', r=0.05816)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s11633', poissonRatio=
    0.0, profile='P-0s11633', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s11740', r=0.05870)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s11740', poissonRatio=
    0.0, profile='P-0s11740', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s12050', r=0.06025)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s12050', poissonRatio=
    0.0, profile='P-0s12050', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s12050', r=0.06025)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s12050', poissonRatio=
    0.0, profile='P-0s12050', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s12173', r=0.06086)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s12173', poissonRatio=
    0.0, profile='P-0s12173', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s12641', r=0.06321)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s12641', poissonRatio=
    0.0, profile='P-0s12641', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s13365', r=0.06683)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s13365', poissonRatio=
    0.0, profile='P-0s13365', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s13908', r=0.06954)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s13908', poissonRatio=
    0.0, profile='P-0s13908', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s14034', r=0.07017)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s14034', poissonRatio=
    0.0, profile='P-0s14034', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s14469', r=0.07234)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s14469', poissonRatio=
    0.0, profile='P-0s14469', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s14768', r=0.07384)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s14768', poissonRatio=
    0.0, profile='P-0s14768', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s16522', r=0.08261)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s16522', poissonRatio=
    0.0, profile='P-0s16522', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s16561', r=0.08281)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s16561', poissonRatio=
    0.0, profile='P-0s16561', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s19053', r=0.09526)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s19053', poissonRatio=
    0.0, profile='P-0s19053', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s24717', r=0.12359)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s24717', poissonRatio=
    0.0, profile='P-0s24717', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s25851', r=0.12925)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s25851', poissonRatio=
    0.0, profile='P-0s25851', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s27051', r=0.13525)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s27051', poissonRatio=
    0.0, profile='P-0s27051', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s28329', r=0.14165)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s28329', poissonRatio=
    0.0, profile='P-0s28329', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s29701', r=0.14850)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s29701', poissonRatio=
    0.0, profile='P-0s29701', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s31187', r=0.15594)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s31187', poissonRatio=
    0.0, profile='P-0s31187', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s32818', r=0.16409)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s32818', poissonRatio=
    0.0, profile='P-0s32818', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s34637', r=0.17318)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s34637', poissonRatio=
    0.0, profile='P-0s34637', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s36716', r=0.18358)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s36716', poissonRatio=
    0.0, profile='P-0s36716', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s39187', r=0.19594)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s39187', poissonRatio=
    0.0, profile='P-0s39187', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s42339', r=0.21170)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s42339', poissonRatio=
    0.0, profile='P-0s42339', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s47116', r=0.23558)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s47116', poissonRatio=
    0.0, profile='P-0s47116', temperatureVar=LINEAR)
# =========================================

# Root segment part creation
mdb.models[modelname].Part(dimensionality=THREE_D, name='Root', type=DEFORMABLE_BODY)

rootpart = mdb.models[modelname].parts['Root']
rootpart.ReferencePoint(point=(0.0, 0.0, 0.0))

# Node datum points creation
rootpart.DatumPointByCoordinate(coords=(0,0,0))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b1')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.1))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b5')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.2))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b9')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.2))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b10')
rootpart.DatumPointByCoordinate(coords=(-0.019649,0.00073113,-0.39495))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b11')
rootpart.DatumPointByCoordinate(coords=(-0.029677,0.0011043,-0.49444))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b25')
rootpart.DatumPointByCoordinate(coords=(-0.039705,0.0014774,-0.59394))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b41')
rootpart.DatumPointByCoordinate(coords=(-0.039705,0.0014774,-0.59394))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b42')
rootpart.DatumPointByCoordinate(coords=(-0.096673,0.0089814,-0.63789))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b43')
rootpart.DatumPointByCoordinate(coords=(-0.17542,0.019354,-0.69865))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b65')
rootpart.DatumPointByCoordinate(coords=(-0.25416,0.029727,-0.75941))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b95')
rootpart.DatumPointByCoordinate(coords=(-0.049733,0.0018506,-0.69343))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b57')
rootpart.DatumPointByCoordinate(coords=(-0.059761,0.0022237,-0.79293))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b79')
rootpart.DatumPointByCoordinate(coords=(-0.069789,0.0025969,-0.89242))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b105')
rootpart.DatumPointByCoordinate(coords=(-0.069789,0.0025969,-0.89242))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b106')
rootpart.DatumPointByCoordinate(coords=(-0.071889,0.0030669,-0.93994))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b107')
rootpart.DatumPointByCoordinate(coords=(-0.079817,0.00297,-0.99192))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b142')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.3))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b21')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.4))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b29')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.4))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b30')
rootpart.DatumPointByCoordinate(coords=(-0.021224,0.072118,-0.55602))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b31')
rootpart.DatumPointByCoordinate(coords=(-0.03348,0.11376,-0.6461))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b61')
rootpart.DatumPointByCoordinate(coords=(-0.045735,0.1554,-0.73619))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b89')
rootpart.DatumPointByCoordinate(coords=(-0.057991,0.19705,-0.82628))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b111')
rootpart.DatumPointByCoordinate(coords=(-0.057991,0.19705,-0.82628))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b112')
rootpart.DatumPointByCoordinate(coords=(-0.052726,0.21024,-0.87349))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b113')
rootpart.DatumPointByCoordinate(coords=(-0.042048,0.23699,-0.96925))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b173')
rootpart.DatumPointByCoordinate(coords=(-0.070246,0.23869,-0.91636))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b150')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.5))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b53')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.6))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b69')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.7))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b99')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.7))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b100')
rootpart.DatumPointByCoordinate(coords=(0.010068,-0.017137,-0.84717))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b101')
rootpart.DatumPointByCoordinate(coords=(0.016847,-0.028676,-0.94627))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b171')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.8))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b132')
rootpart.DatumPointByCoordinate(coords=(0,0,-0.9))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b176')
rootpart.DatumPointByCoordinate(coords=(0,0,-1))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b222')
rootpart.DatumPointByCoordinate(coords=(0,0,-1))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b223')
rootpart.DatumPointByCoordinate(coords=(0,0,0))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b2')
rootpart.DatumPointByCoordinate(coords=(0.064729,0,-0.076224))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b6')
rootpart.DatumPointByCoordinate(coords=(0.12946,0,-0.15245))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b12')
rootpart.DatumPointByCoordinate(coords=(0.12946,0,-0.15245))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b13')
rootpart.DatumPointByCoordinate(coords=(0.27056,-0.071117,-0.26831))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b14')
rootpart.DatumPointByCoordinate(coords=(0.34257,-0.10741,-0.32744))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b26')
rootpart.DatumPointByCoordinate(coords=(0.41459,-0.14371,-0.38658))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b44')
rootpart.DatumPointByCoordinate(coords=(0.41459,-0.14371,-0.38658))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b45')
rootpart.DatumPointByCoordinate(coords=(0.46862,-0.12195,-0.42947))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b46')
rootpart.DatumPointByCoordinate(coords=(0.54332,-0.091874,-0.48877))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b66')
rootpart.DatumPointByCoordinate(coords=(0.61802,-0.061798,-0.54806))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b96')
rootpart.DatumPointByCoordinate(coords=(0.4866,-0.18,-0.44571))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b58')
rootpart.DatumPointByCoordinate(coords=(0.55861,-0.2163,-0.50484))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b80')
rootpart.DatumPointByCoordinate(coords=(0.55861,-0.2163,-0.50484))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b81')
rootpart.DatumPointByCoordinate(coords=(0.58838,-0.24501,-0.54113))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b82')
rootpart.DatumPointByCoordinate(coords=(0.64249,-0.29718,-0.60708))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b128')
rootpart.DatumPointByCoordinate(coords=(0.63063,-0.2526,-0.56397))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b108')
rootpart.DatumPointByCoordinate(coords=(0.70264,-0.28889,-0.62311))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b143')
rootpart.DatumPointByCoordinate(coords=(0.70264,-0.28889,-0.62311))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b144')
rootpart.DatumPointByCoordinate(coords=(0.72687,-0.29132,-0.6557))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b145')
rootpart.DatumPointByCoordinate(coords=(0.78642,-0.29729,-0.73581))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b217')
rootpart.DatumPointByCoordinate(coords=(0.77465,-0.32519,-0.68224))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b183')
rootpart.DatumPointByCoordinate(coords=(0.84667,-0.36148,-0.74137))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b237')
rootpart.DatumPointByCoordinate(coords=(0.91868,-0.39778,-0.8005))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b294')
rootpart.DatumPointByCoordinate(coords=(0.91868,-0.39778,-0.8005))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b295')
rootpart.DatumPointByCoordinate(coords=(0.92371,-0.39606,-0.82245))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b296')
rootpart.DatumPointByCoordinate(coords=(0.99069,-0.43407,-0.85964))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b332')
rootpart.DatumPointByCoordinate(coords=(0.99069,-0.43407,-0.85964))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b333')
rootpart.DatumPointByCoordinate(coords=(0.99915,-0.44126,-0.87277))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b334')
rootpart.DatumPointByCoordinate(coords=(0.99069,-0.43407,-0.85964))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b335')
rootpart.DatumPointByCoordinate(coords=(1.0059,-0.43884,-0.86597))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b336')
rootpart.DatumPointByCoordinate(coords=(0.19419,0,-0.22867))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b22')
rootpart.DatumPointByCoordinate(coords=(0.25892,0,-0.3049))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b32')
rootpart.DatumPointByCoordinate(coords=(0.25892,0,-0.3049))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b33')
rootpart.DatumPointByCoordinate(coords=(0.30591,-0.0013404,-0.47158))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b34')
rootpart.DatumPointByCoordinate(coords=(0.33304,-0.0021144,-0.56782))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b62')
rootpart.DatumPointByCoordinate(coords=(0.36017,-0.0028883,-0.66407))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b90')
rootpart.DatumPointByCoordinate(coords=(0.3873,-0.0036623,-0.76031))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b114')
rootpart.DatumPointByCoordinate(coords=(0.3873,-0.0036623,-0.76031))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b115')
rootpart.DatumPointByCoordinate(coords=(0.36093,0.020714,-0.79409))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b116')
rootpart.DatumPointByCoordinate(coords=(0.30745,0.070158,-0.86261))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b174')
rootpart.DatumPointByCoordinate(coords=(0.41444,-0.0044363,-0.85656))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b151')
rootpart.DatumPointByCoordinate(coords=(0.44157,-0.0052102,-0.95281))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b191')
rootpart.DatumPointByCoordinate(coords=(0.32365,0,-0.38112))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b54')
rootpart.DatumPointByCoordinate(coords=(0.38838,0,-0.45735))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b70')
rootpart.DatumPointByCoordinate(coords=(0.38838,0,-0.45735))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b71')
rootpart.DatumPointByCoordinate(coords=(0.45693,-0.026415,-0.59489))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b72')
rootpart.DatumPointByCoordinate(coords=(0.5009,-0.043355,-0.68309))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b125')
rootpart.DatumPointByCoordinate(coords=(0.54486,-0.060295,-0.7713))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b160')
rootpart.DatumPointByCoordinate(coords=(0.54486,-0.060295,-0.7713))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b161')
rootpart.DatumPointByCoordinate(coords=(0.55306,-0.067593,-0.81915))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b162')
rootpart.DatumPointByCoordinate(coords=(0.56975,-0.082457,-0.91662))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b220')
rootpart.DatumPointByCoordinate(coords=(0.58883,-0.077234,-0.8595))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b198')
rootpart.DatumPointByCoordinate(coords=(0.63279,-0.094174,-0.94771))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b254')
rootpart.DatumPointByCoordinate(coords=(0.63279,-0.094174,-0.94771))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b255')
rootpart.DatumPointByCoordinate(coords=(0.65444,-0.088747,-0.96916))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b256')
rootpart.DatumPointByCoordinate(coords=(0.4531,0,-0.53357))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b102')
rootpart.DatumPointByCoordinate(coords=(0.51783,0,-0.60979))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b133')
rootpart.DatumPointByCoordinate(coords=(0.51783,0,-0.60979))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b134')
rootpart.DatumPointByCoordinate(coords=(0.59852,-0.029374,-0.72244))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b135')
rootpart.DatumPointByCoordinate(coords=(0.65548,-0.050112,-0.80197))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b214')
rootpart.DatumPointByCoordinate(coords=(0.71245,-0.070849,-0.8815))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b270')
rootpart.DatumPointByCoordinate(coords=(0.71245,-0.070849,-0.8815))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b271')
rootpart.DatumPointByCoordinate(coords=(0.71635,-0.075302,-0.92241))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b272')
rootpart.DatumPointByCoordinate(coords=(0.76941,-0.091587,-0.96103))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b315')
rootpart.DatumPointByCoordinate(coords=(0.58256,0,-0.68602))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b177')
rootpart.DatumPointByCoordinate(coords=(0.64729,0,-0.76224))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b225')
rootpart.DatumPointByCoordinate(coords=(0.71202,0,-0.83847))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b289')
rootpart.DatumPointByCoordinate(coords=(0.71202,0,-0.83847))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b290')
rootpart.DatumPointByCoordinate(coords=(0.82257,-0.045922,-0.8692))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b291')
rootpart.DatumPointByCoordinate(coords=(0.91202,-0.08308,-0.89406))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b374')
rootpart.DatumPointByCoordinate(coords=(1.0015,-0.12024,-0.91892))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b392')
rootpart.DatumPointByCoordinate(coords=(1.0909,-0.1574,-0.94379))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b418')
rootpart.DatumPointByCoordinate(coords=(1.0909,-0.1574,-0.94379))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b419')
rootpart.DatumPointByCoordinate(coords=(1.1079,-0.16599,-0.93358))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b420')
rootpart.DatumPointByCoordinate(coords=(1.1804,-0.19455,-0.96865))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b437')
rootpart.DatumPointByCoordinate(coords=(1.2698,-0.23171,-0.99352))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b454')
rootpart.DatumPointByCoordinate(coords=(0.71202,0,-0.83847))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b292')
rootpart.DatumPointByCoordinate(coords=(0.72443,0.045922,-0.95253))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b293')
rootpart.DatumPointByCoordinate(coords=(0,0,0))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b3')
rootpart.DatumPointByCoordinate(coords=(-0.017453,0.03023,-0.09371))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b7')
rootpart.DatumPointByCoordinate(coords=(-0.034907,0.06046,-0.18742))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b15')
rootpart.DatumPointByCoordinate(coords=(-0.034907,0.06046,-0.18742))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b16')
rootpart.DatumPointByCoordinate(coords=(-0.14089,0.11018,-0.34453))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b17')
rootpart.DatumPointByCoordinate(coords=(-0.19499,0.13556,-0.42472))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b27')
rootpart.DatumPointByCoordinate(coords=(-0.24908,0.16094,-0.50491))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b47')
rootpart.DatumPointByCoordinate(coords=(-0.24908,0.16094,-0.50491))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b48')
rootpart.DatumPointByCoordinate(coords=(-0.25142,0.1619,-0.57721))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b49')
rootpart.DatumPointByCoordinate(coords=(-0.25465,0.16324,-0.67715))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b67')
rootpart.DatumPointByCoordinate(coords=(-0.25788,0.16457,-0.77709))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b97')
rootpart.DatumPointByCoordinate(coords=(-0.30317,0.18632,-0.58509))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b59')
rootpart.DatumPointByCoordinate(coords=(-0.35727,0.21169,-0.66528))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b83')
rootpart.DatumPointByCoordinate(coords=(-0.35727,0.21169,-0.66528))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b84')
rootpart.DatumPointByCoordinate(coords=(-0.37953,0.21956,-0.71498))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b85')
rootpart.DatumPointByCoordinate(coords=(-0.41999,0.23386,-0.8053))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b129')
rootpart.DatumPointByCoordinate(coords=(-0.41136,0.23707,-0.74547))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b109')
rootpart.DatumPointByCoordinate(coords=(-0.46545,0.26245,-0.82565))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b146')
rootpart.DatumPointByCoordinate(coords=(-0.51955,0.28783,-0.90584))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b184')
rootpart.DatumPointByCoordinate(coords=(-0.51955,0.28783,-0.90584))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b185')
rootpart.DatumPointByCoordinate(coords=(-0.51768,0.28866,-0.94005))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b186')
rootpart.DatumPointByCoordinate(coords=(-0.57364,0.31321,-0.98603))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b238')
rootpart.DatumPointByCoordinate(coords=(-0.05236,0.09069,-0.28113))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b23')
rootpart.DatumPointByCoordinate(coords=(-0.069813,0.12092,-0.37484))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b35')
rootpart.DatumPointByCoordinate(coords=(-0.069813,0.12092,-0.37484))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b36')
rootpart.DatumPointByCoordinate(coords=(-0.041385,0.030606,-0.51985))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b37')
rootpart.DatumPointByCoordinate(coords=(-0.02497,-0.021543,-0.60358))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b63')
rootpart.DatumPointByCoordinate(coords=(-0.0085549,-0.073693,-0.68731))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b91')
rootpart.DatumPointByCoordinate(coords=(0.0078602,-0.12584,-0.77104))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b117')
rootpart.DatumPointByCoordinate(coords=(0.0078602,-0.12584,-0.77104))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b118')
rootpart.DatumPointByCoordinate(coords=(0.0091906,-0.17512,-0.77037))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b119')
rootpart.DatumPointByCoordinate(coords=(0.011889,-0.27508,-0.76901))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b175')
rootpart.DatumPointByCoordinate(coords=(0.024275,-0.17799,-0.85477))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b152')
rootpart.DatumPointByCoordinate(coords=(0.04069,-0.23014,-0.93851))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b192')
rootpart.DatumPointByCoordinate(coords=(-0.087266,0.15115,-0.46855))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b55')
rootpart.DatumPointByCoordinate(coords=(-0.10472,0.18138,-0.56226))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b73')
rootpart.DatumPointByCoordinate(coords=(-0.10472,0.18138,-0.56226))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b74')
rootpart.DatumPointByCoordinate(coords=(-0.22089,0.25007,-0.64037))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b75')
rootpart.DatumPointByCoordinate(coords=(-0.2954,0.29412,-0.69046))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b126')
rootpart.DatumPointByCoordinate(coords=(-0.3699,0.33817,-0.74056))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b163')
rootpart.DatumPointByCoordinate(coords=(-0.3699,0.33817,-0.74056))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b164')
rootpart.DatumPointByCoordinate(coords=(-0.40046,0.37659,-0.74097))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b165')
rootpart.DatumPointByCoordinate(coords=(-0.46272,0.45484,-0.74182))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b221')
rootpart.DatumPointByCoordinate(coords=(-0.4444,0.38222,-0.79065))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b199')
rootpart.DatumPointByCoordinate(coords=(-0.5189,0.42627,-0.84074))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b257')
rootpart.DatumPointByCoordinate(coords=(-0.5189,0.42627,-0.84074))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b258')
rootpart.DatumPointByCoordinate(coords=(-0.53175,0.42879,-0.86878))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b259')
rootpart.DatumPointByCoordinate(coords=(-0.5934,0.47031,-0.89083))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b308')
rootpart.DatumPointByCoordinate(coords=(-0.6679,0.51436,-0.94092))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b354')
rootpart.DatumPointByCoordinate(coords=(-0.6679,0.51436,-0.94092))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b355')
rootpart.DatumPointByCoordinate(coords=(-0.68225,0.51033,-0.94708))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b356')
rootpart.DatumPointByCoordinate(coords=(-0.7424,0.55841,-0.99102))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b382')
rootpart.DatumPointByCoordinate(coords=(-0.12217,0.21161,-0.65597))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b103')
rootpart.DatumPointByCoordinate(coords=(-0.13963,0.24184,-0.74968))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b136')
rootpart.DatumPointByCoordinate(coords=(-0.13963,0.24184,-0.74968))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b137')
rootpart.DatumPointByCoordinate(coords=(-0.13833,0.30218,-0.87782))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b138')
rootpart.DatumPointByCoordinate(coords=(-0.13741,0.34478,-0.96829))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b215')
rootpart.DatumPointByCoordinate(coords=(-0.15708,0.27207,-0.84339))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b178')
rootpart.DatumPointByCoordinate(coords=(-0.17453,0.3023,-0.9371))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b226')
rootpart.DatumPointByCoordinate(coords=(-0.17453,0.3023,-0.9371))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b227')
rootpart.DatumPointByCoordinate(coords=(-0.17453,0.3023,-0.9371))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b229')
rootpart.DatumPointByCoordinate(coords=(0,0,0))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b4')
rootpart.DatumPointByCoordinate(coords=(-0.019803,-0.0343,-0.091822))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b8')
rootpart.DatumPointByCoordinate(coords=(-0.039607,-0.068601,-0.18364))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b18')
rootpart.DatumPointByCoordinate(coords=(-0.039607,-0.068601,-0.18364))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b19')
rootpart.DatumPointByCoordinate(coords=(-0.011543,-0.23048,-0.2904))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b20')
rootpart.DatumPointByCoordinate(coords=(0.0027797,-0.3131,-0.34489))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b28')
rootpart.DatumPointByCoordinate(coords=(0.017102,-0.39572,-0.39938))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b50')
rootpart.DatumPointByCoordinate(coords=(0.017102,-0.39572,-0.39938))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b51')
rootpart.DatumPointByCoordinate(coords=(0.0529,-0.42791,-0.45338))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b52')
rootpart.DatumPointByCoordinate(coords=(0.10238,-0.47239,-0.52803))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b68')
rootpart.DatumPointByCoordinate(coords=(0.15187,-0.51688,-0.60268))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b98')
rootpart.DatumPointByCoordinate(coords=(0.031425,-0.47834,-0.45386))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b60')
rootpart.DatumPointByCoordinate(coords=(0.045748,-0.56096,-0.50835))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b86')
rootpart.DatumPointByCoordinate(coords=(0.045748,-0.56096,-0.50835))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b87')
rootpart.DatumPointByCoordinate(coords=(0.086289,-0.59145,-0.52966))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b88')
rootpart.DatumPointByCoordinate(coords=(0.15997,-0.64686,-0.5684))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b130')
rootpart.DatumPointByCoordinate(coords=(0.060071,-0.64358,-0.56284))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b110')
rootpart.DatumPointByCoordinate(coords=(0.074394,-0.7262,-0.61732))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b147')
rootpart.DatumPointByCoordinate(coords=(0.074394,-0.7262,-0.61732))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b148')
rootpart.DatumPointByCoordinate(coords=(0.061036,-0.73143,-0.65539))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b149')
rootpart.DatumPointByCoordinate(coords=(0.0282,-0.74429,-0.74897))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b218')
rootpart.DatumPointByCoordinate(coords=(0.088716,-0.80882,-0.67181))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b187')
rootpart.DatumPointByCoordinate(coords=(0.10304,-0.89144,-0.7263))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b239')
rootpart.DatumPointByCoordinate(coords=(0.11736,-0.97406,-0.78078))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b298')
rootpart.DatumPointByCoordinate(coords=(0.11736,-0.97406,-0.78078))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b299')
rootpart.DatumPointByCoordinate(coords=(0.1288,-0.99107,-0.79025))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b300')
rootpart.DatumPointByCoordinate(coords=(0.13168,-1.0567,-0.83527))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b340')
rootpart.DatumPointByCoordinate(coords=(0.13168,-1.0567,-0.83527))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b341')
rootpart.DatumPointByCoordinate(coords=(0.13561,-1.0726,-0.84037))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b342')
rootpart.DatumPointByCoordinate(coords=(0.13168,-1.0567,-0.83527))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b343')
rootpart.DatumPointByCoordinate(coords=(0.13249,-1.068,-0.84816))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b344')
rootpart.DatumPointByCoordinate(coords=(-0.05941,-0.1029,-0.27547))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b24')
rootpart.DatumPointByCoordinate(coords=(-0.079213,-0.1372,-0.36729))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b38')
rootpart.DatumPointByCoordinate(coords=(-0.079213,-0.1372,-0.36729))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b39')
rootpart.DatumPointByCoordinate(coords=(-0.15205,-0.29223,-0.39284))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b40')
rootpart.DatumPointByCoordinate(coords=(-0.19411,-0.38175,-0.4076))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b64')
rootpart.DatumPointByCoordinate(coords=(-0.23616,-0.47127,-0.42235))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b92')
rootpart.DatumPointByCoordinate(coords=(-0.23616,-0.47127,-0.42235))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b93')
rootpart.DatumPointByCoordinate(coords=(-0.2247,-0.4945,-0.47503))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b94')
rootpart.DatumPointByCoordinate(coords=(-0.20517,-0.53408,-0.56476))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b131')
rootpart.DatumPointByCoordinate(coords=(-0.27822,-0.56079,-0.43711))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b120')
rootpart.DatumPointByCoordinate(coords=(-0.32028,-0.6503,-0.45186))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b153')
rootpart.DatumPointByCoordinate(coords=(-0.32028,-0.6503,-0.45186))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b154')
rootpart.DatumPointByCoordinate(coords=(-0.33909,-0.67505,-0.47847))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b155')
rootpart.DatumPointByCoordinate(coords=(-0.38508,-0.73553,-0.5435))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b219')
rootpart.DatumPointByCoordinate(coords=(-0.36233,-0.73982,-0.46662))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b193')
rootpart.DatumPointByCoordinate(coords=(-0.40439,-0.82934,-0.48138))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b247')
rootpart.DatumPointByCoordinate(coords=(-0.40439,-0.82934,-0.48138))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b248')
rootpart.DatumPointByCoordinate(coords=(-0.42582,-0.84415,-0.48508))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b249')
rootpart.DatumPointByCoordinate(coords=(-0.44645,-0.91886,-0.49613))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b303')
rootpart.DatumPointByCoordinate(coords=(-0.48851,-1.0084,-0.51089))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b345')
rootpart.DatumPointByCoordinate(coords=(-0.48851,-1.0084,-0.51089))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b346')
rootpart.DatumPointByCoordinate(coords=(-0.48645,-1.0203,-0.5045))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b347')
rootpart.DatumPointByCoordinate(coords=(-0.53056,-1.0979,-0.52564))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b378')
rootpart.DatumPointByCoordinate(coords=(-0.57262,-1.1874,-0.5404))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b401')
rootpart.DatumPointByCoordinate(coords=(-0.57262,-1.1874,-0.5404))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b402')
rootpart.DatumPointByCoordinate(coords=(-0.57326,-1.1897,-0.54116))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b403')
rootpart.DatumPointByCoordinate(coords=(-0.57262,-1.1874,-0.5404))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b404')
rootpart.DatumPointByCoordinate(coords=(-0.57403,-1.1895,-0.54036))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b405')
rootpart.DatumPointByCoordinate(coords=(-0.099017,-0.1715,-0.45911))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b56')
rootpart.DatumPointByCoordinate(coords=(-0.11882,-0.2058,-0.55093))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b76')
rootpart.DatumPointByCoordinate(coords=(-0.11882,-0.2058,-0.55093))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b77')
rootpart.DatumPointByCoordinate(coords=(-0.11371,-0.22047,-0.70609))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b78')
rootpart.DatumPointByCoordinate(coords=(-0.11043,-0.22988,-0.8056))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b127')
rootpart.DatumPointByCoordinate(coords=(-0.10715,-0.23929,-0.9051))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b166')
rootpart.DatumPointByCoordinate(coords=(-0.13862,-0.2401,-0.64276))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b104')
rootpart.DatumPointByCoordinate(coords=(-0.15843,-0.2744,-0.73458))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b139')
rootpart.DatumPointByCoordinate(coords=(-0.15843,-0.2744,-0.73458))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b140')
rootpart.DatumPointByCoordinate(coords=(-0.17569,-0.36109,-0.84526))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b141')
rootpart.DatumPointByCoordinate(coords=(-0.18788,-0.42228,-0.92341))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b216')
rootpart.DatumPointByCoordinate(coords=(-0.17823,-0.3087,-0.8264))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b179')
rootpart.DatumPointByCoordinate(coords=(-0.19803,-0.343,-0.91822))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b231')
rootpart.DatumPointByCoordinate(coords=(-0.19803,-0.343,-0.91822))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b232')
rootpart.DatumPointByCoordinate(coords=(-0.19803,-0.343,-0.91822))
rootpart.features.changeKey(fromName='Datum pt-1', toName='b234')

# Internodes creation
rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1'].id], root.datums[root.features['b5'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b1b5')

reg = Region(edges = root.getFeatureEdges('b1b5'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s47116', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b5'].id], root.datums[root.features['b9'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b5b9')

reg = Region(edges = root.getFeatureEdges('b5b9'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s42339', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b10'].id], root.datums[root.features['b11'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b10b11')

reg = Region(edges = root.getFeatureEdges('b10b11'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s19053', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b11'].id], root.datums[root.features['b25'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b11b25')

reg = Region(edges = root.getFeatureEdges('b11b25'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s19053', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b25'].id], root.datums[root.features['b41'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b25b41')

reg = Region(edges = root.getFeatureEdges('b25b41'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16561', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b42'].id], root.datums[root.features['b43'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b42b43')

reg = Region(edges = root.getFeatureEdges('b42b43'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,7.5916,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07452', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b43'].id], root.datums[root.features['b65'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b43b65')

reg = Region(edges = root.getFeatureEdges('b43b65'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,7.5916,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07452', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b65'].id], root.datums[root.features['b95'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b65b95')

reg = Region(edges = root.getFeatureEdges('b65b95'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,7.5916,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04006', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b41'].id], root.datums[root.features['b57'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b41b57')

reg = Region(edges = root.getFeatureEdges('b41b57'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14469', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b57'].id], root.datums[root.features['b79'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b57b79')

reg = Region(edges = root.getFeatureEdges('b57b79'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12641', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b79'].id], root.datums[root.features['b105'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b79b105')

reg = Region(edges = root.getFeatureEdges('b79b105'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11004', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b106'].id], root.datums[root.features['b107'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b106b107')

reg = Region(edges = root.getFeatureEdges('b106b107'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,4.4678,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04952', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b105'].id], root.datums[root.features['b142'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b105b142')

reg = Region(edges = root.getFeatureEdges('b105b142'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,26.8745,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09512', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b9'].id], root.datums[root.features['b21'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b9b21')

reg = Region(edges = root.getFeatureEdges('b9b21'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s39187', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b21'].id], root.datums[root.features['b29'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b21b29')

reg = Region(edges = root.getFeatureEdges('b21b29'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s36716', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b30'].id], root.datums[root.features['b31'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b30b31')

reg = Region(edges = root.getFeatureEdges('b30b31'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.2943,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16522', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b31'].id], root.datums[root.features['b61'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b31b61')

reg = Region(edges = root.getFeatureEdges('b31b61'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.2943,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16522', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b61'].id], root.datums[root.features['b89'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b61b89')

reg = Region(edges = root.getFeatureEdges('b61b89'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.2943,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s13908', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b89'].id], root.datums[root.features['b111'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b89b111')

reg = Region(edges = root.getFeatureEdges('b89b111'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.2943,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11740', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b112'].id], root.datums[root.features['b113'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b112b113')

reg = Region(edges = root.getFeatureEdges('b112b113'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.39909,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05283', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b113'].id], root.datums[root.features['b173'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b113b173')

reg = Region(edges = root.getFeatureEdges('b113b173'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.39909,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05283', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b111'].id], root.datums[root.features['b150'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b111b150')

reg = Region(edges = root.getFeatureEdges('b111b150'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.2943,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09860', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b29'].id], root.datums[root.features['b53'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b29b53')

reg = Region(edges = root.getFeatureEdges('b29b53'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s34637', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b53'].id], root.datums[root.features['b69'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b53b69')

reg = Region(edges = root.getFeatureEdges('b53b69'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s32818', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b69'].id], root.datums[root.features['b99'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b69b99')

reg = Region(edges = root.getFeatureEdges('b69b99'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31187', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b100'].id], root.datums[root.features['b101'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b100b101')

reg = Region(edges = root.getFeatureEdges('b100b101'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.58749,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14034', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b101'].id], root.datums[root.features['b171'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b101b171')

reg = Region(edges = root.getFeatureEdges('b101b171'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.58749,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14034', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b99'].id], root.datums[root.features['b132'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b99b132')

reg = Region(edges = root.getFeatureEdges('b99b132'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s29701', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b132'].id], root.datums[root.features['b176'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b132b176')

reg = Region(edges = root.getFeatureEdges('b132b176'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s28329', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b176'].id], root.datums[root.features['b222'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b176b222')

reg = Region(edges = root.getFeatureEdges('b176b222'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s27051', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b2'].id], root.datums[root.features['b6'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b2b6')

reg = Region(edges = root.getFeatureEdges('b2b6'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s47116', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b6'].id], root.datums[root.features['b12'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b6b12')

reg = Region(edges = root.getFeatureEdges('b6b12'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s42339', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b13'].id], root.datums[root.features['b14'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b13b14')

reg = Region(edges = root.getFeatureEdges('b13b14'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s19053', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b14'].id], root.datums[root.features['b26'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b14b26')

reg = Region(edges = root.getFeatureEdges('b14b26'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s19053', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b26'].id], root.datums[root.features['b44'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b26b44')

reg = Region(edges = root.getFeatureEdges('b26b44'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16561', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b45'].id], root.datums[root.features['b46'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b45b46')

reg = Region(edges = root.getFeatureEdges('b45b46'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-2.4836,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07452', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b46'].id], root.datums[root.features['b66'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b46b66')

reg = Region(edges = root.getFeatureEdges('b46b66'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-2.4836,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07452', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b66'].id], root.datums[root.features['b96'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b66b96')

reg = Region(edges = root.getFeatureEdges('b66b96'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-2.4836,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04006', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b44'].id], root.datums[root.features['b58'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b44b58')

reg = Region(edges = root.getFeatureEdges('b44b58'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14469', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b58'].id], root.datums[root.features['b80'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b58b80')

reg = Region(edges = root.getFeatureEdges('b58b80'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12641', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b81'].id], root.datums[root.features['b82'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b81b82')

reg = Region(edges = root.getFeatureEdges('b81b82'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0371,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05688', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b82'].id], root.datums[root.features['b128'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b82b128')

reg = Region(edges = root.getFeatureEdges('b82b128'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0371,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05688', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b80'].id], root.datums[root.features['b108'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b80b108')

reg = Region(edges = root.getFeatureEdges('b80b108'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11004', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b108'].id], root.datums[root.features['b143'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b108b143')

reg = Region(edges = root.getFeatureEdges('b108b143'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09512', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b144'].id], root.datums[root.features['b145'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b144b145')

reg = Region(edges = root.getFeatureEdges('b144b145'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,9.9776,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04281', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b145'].id], root.datums[root.features['b217'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b145b217')

reg = Region(edges = root.getFeatureEdges('b145b217'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,9.9776,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04281', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b143'].id], root.datums[root.features['b183'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b143b183')

reg = Region(edges = root.getFeatureEdges('b143b183'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s08136', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b183'].id], root.datums[root.features['b237'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b183b237')

reg = Region(edges = root.getFeatureEdges('b183b237'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06855', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b237'].id], root.datums[root.features['b294'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b237b294')

reg = Region(edges = root.getFeatureEdges('b237b294'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05652', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b295'].id], root.datums[root.features['b296'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b295b296')

reg = Region(edges = root.getFeatureEdges('b295b296'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-2.9333,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02543', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b294'].id], root.datums[root.features['b332'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b294b332')

reg = Region(edges = root.getFeatureEdges('b294b332'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9841,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04516', thicknessAssignment=FROM_SECTION)

rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b333'].id], root.datums[root.features['b334'].id]),))
rootpart.features.changeKey(fromName='Wire-1', toName='b333b334')

reg = Region(edges = root.getFeatureEdges('b333b334'))
rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.1765,0), region=reg)
rootpart.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02032', thicknessAssignment=FROM_SECTION)

