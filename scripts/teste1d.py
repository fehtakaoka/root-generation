# Script automatically generated on 23-Oct-2018 at 15:26 by RootGen
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
modelname = 'teste1d';
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
	"init_diam" : 0.31149,
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
mdb.models[modelname].CircularProfile(name='P-0s00103', r=0.00051)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00103', poissonRatio=
    0.0, profile='P-0s00103', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00103', r=0.00051)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00103', poissonRatio=
    0.0, profile='P-0s00103', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00498', r=0.00249)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00498', poissonRatio=
    0.0, profile='P-0s00498', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00498', r=0.00249)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00498', poissonRatio=
    0.0, profile='P-0s00498', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00498', r=0.00249)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00498', poissonRatio=
    0.0, profile='P-0s00498', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00581', r=0.00290)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00581', poissonRatio=
    0.0, profile='P-0s00581', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00605', r=0.00303)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00605', poissonRatio=
    0.0, profile='P-0s00605', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00718', r=0.00359)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00718', poissonRatio=
    0.0, profile='P-0s00718', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s00948', r=0.00474)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s00948', poissonRatio=
    0.0, profile='P-0s00948', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01001', r=0.00500)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01001', poissonRatio=
    0.0, profile='P-0s01001', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01112', r=0.00556)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01112', poissonRatio=
    0.0, profile='P-0s01112', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01154', r=0.00577)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01154', poissonRatio=
    0.0, profile='P-0s01154', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01233', r=0.00617)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01233', poissonRatio=
    0.0, profile='P-0s01233', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01290', r=0.00645)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01290', poissonRatio=
    0.0, profile='P-0s01290', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01290', r=0.00645)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01290', poissonRatio=
    0.0, profile='P-0s01290', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01327', r=0.00664)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01327', poissonRatio=
    0.0, profile='P-0s01327', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01583', r=0.00792)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01583', poissonRatio=
    0.0, profile='P-0s01583', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01583', r=0.00792)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01583', poissonRatio=
    0.0, profile='P-0s01583', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01720', r=0.00860)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01720', poissonRatio=
    0.0, profile='P-0s01720', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01751', r=0.00875)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01751', poissonRatio=
    0.0, profile='P-0s01751', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s01896', r=0.00948)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s01896', poissonRatio=
    0.0, profile='P-0s01896', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02106', r=0.01053)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02106', poissonRatio=
    0.0, profile='P-0s02106', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02106', r=0.01053)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02106', poissonRatio=
    0.0, profile='P-0s02106', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02127', r=0.01064)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02127', poissonRatio=
    0.0, profile='P-0s02127', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02196', r=0.01098)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02196', poissonRatio=
    0.0, profile='P-0s02196', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02471', r=0.01236)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02471', poissonRatio=
    0.0, profile='P-0s02471', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02811', r=0.01406)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02811', poissonRatio=
    0.0, profile='P-0s02811', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02950', r=0.01475)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02950', poissonRatio=
    0.0, profile='P-0s02950', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02950', r=0.01475)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02950', poissonRatio=
    0.0, profile='P-0s02950', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s02992', r=0.01496)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s02992', poissonRatio=
    0.0, profile='P-0s02992', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03358', r=0.01679)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03358', poissonRatio=
    0.0, profile='P-0s03358', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03454', r=0.01727)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03454', poissonRatio=
    0.0, profile='P-0s03454', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03823', r=0.01911)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03823', poissonRatio=
    0.0, profile='P-0s03823', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03823', r=0.01911)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03823', poissonRatio=
    0.0, profile='P-0s03823', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s03891', r=0.01945)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s03891', poissonRatio=
    0.0, profile='P-0s03891', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04080', r=0.02040)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04080', poissonRatio=
    0.0, profile='P-0s04080', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04181', r=0.02090)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04181', poissonRatio=
    0.0, profile='P-0s04181', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04448', r=0.02224)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04448', poissonRatio=
    0.0, profile='P-0s04448', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04728', r=0.02364)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04728', poissonRatio=
    0.0, profile='P-0s04728', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04728', r=0.02364)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04728', poissonRatio=
    0.0, profile='P-0s04728', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04879', r=0.02440)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04879', poissonRatio=
    0.0, profile='P-0s04879', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s04988', r=0.02494)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s04988', poissonRatio=
    0.0, profile='P-0s04988', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05437', r=0.02718)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05437', poissonRatio=
    0.0, profile='P-0s05437', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05563', r=0.02781)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05563', poissonRatio=
    0.0, profile='P-0s05563', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05669', r=0.02834)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05669', poissonRatio=
    0.0, profile='P-0s05669', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s05669', r=0.02834)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s05669', poissonRatio=
    0.0, profile='P-0s05669', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06649', r=0.03325)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06649', poissonRatio=
    0.0, profile='P-0s06649', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s06849', r=0.03425)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s06849', poissonRatio=
    0.0, profile='P-0s06849', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07144', r=0.03572)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07144', poissonRatio=
    0.0, profile='P-0s07144', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07332', r=0.03666)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07332', poissonRatio=
    0.0, profile='P-0s07332', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07583', r=0.03791)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07583', poissonRatio=
    0.0, profile='P-0s07583', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s07674', r=0.03837)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s07674', poissonRatio=
    0.0, profile='P-0s07674', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s08750', r=0.04375)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s08750', poissonRatio=
    0.0, profile='P-0s08750', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s09067', r=0.04533)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s09067', poissonRatio=
    0.0, profile='P-0s09067', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s09883', r=0.04942)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s09883', poissonRatio=
    0.0, profile='P-0s09883', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s10449', r=0.05224)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s10449', poissonRatio=
    0.0, profile='P-0s10449', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s11083', r=0.05542)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s11083', poissonRatio=
    0.0, profile='P-0s11083', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s11298', r=0.05649)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s11298', poissonRatio=
    0.0, profile='P-0s11298', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s12362', r=0.06181)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s12362', poissonRatio=
    0.0, profile='P-0s12362', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s13734', r=0.06867)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s13734', poissonRatio=
    0.0, profile='P-0s13734', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s14017', r=0.07009)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s14017', poissonRatio=
    0.0, profile='P-0s14017', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s15220', r=0.07610)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s15220', poissonRatio=
    0.0, profile='P-0s15220', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s16850', r=0.08425)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s16850', poissonRatio=
    0.0, profile='P-0s16850', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s18669', r=0.09335)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s18669', poissonRatio=
    0.0, profile='P-0s18669', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s20749', r=0.10374)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s20749', poissonRatio=
    0.0, profile='P-0s20749', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s23220', r=0.11610)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s23220', poissonRatio=
    0.0, profile='P-0s23220', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s26372', r=0.13186)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s26372', poissonRatio=
    0.0, profile='P-0s26372', temperatureVar=LINEAR)

mdb.models[modelname].CircularProfile(name='P-0s31149', r=0.15575)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='S-0s31149', poissonRatio=
    0.0, profile='P-0s31149', temperatureVar=LINEAR)
# =========================================

# Root segment part creation
mdb.models[modelname].Part(dimensionality=THREE_D, name='Root', type=DEFORMABLE_BODY)

root = mdb.models[modelname].parts['Root']
root.ReferencePoint(point=(0.0, 0.0, 0.0))

# Node datum points creation
root.DatumPointByCoordinate(coords=(0,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1')
root.DatumPointByCoordinate(coords=(0,0,-0.1))
root.features.changeKey(fromName='Datum pt-1', toName='b7')
root.DatumPointByCoordinate(coords=(0,0,-0.2))
root.features.changeKey(fromName='Datum pt-1', toName='b13')
root.DatumPointByCoordinate(coords=(0,0,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b19')
root.DatumPointByCoordinate(coords=(0,0,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b20')
root.DatumPointByCoordinate(coords=(-0.052915,-0.14648,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b21')
root.DatumPointByCoordinate(coords=(-0.08689,-0.24053,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b51')
root.DatumPointByCoordinate(coords=(-0.12086,-0.33458,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b67')
root.DatumPointByCoordinate(coords=(-0.15484,-0.42864,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b89')
root.DatumPointByCoordinate(coords=(-0.15484,-0.42864,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b90')
root.DatumPointByCoordinate(coords=(-0.15484,-0.42864,-0.33572))
root.features.changeKey(fromName='Datum pt-1', toName='b91')
root.DatumPointByCoordinate(coords=(-0.15484,-0.42864,-0.43572))
root.features.changeKey(fromName='Datum pt-1', toName='b152')
root.DatumPointByCoordinate(coords=(-0.18881,-0.52269,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b139')
root.DatumPointByCoordinate(coords=(-0.22279,-0.61674,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b168')
root.DatumPointByCoordinate(coords=(-0.25677,-0.71079,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b206')
root.DatumPointByCoordinate(coords=(-0.25677,-0.71079,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b207')
root.DatumPointByCoordinate(coords=(-0.25677,-0.71079,-0.31236))
root.features.changeKey(fromName='Datum pt-1', toName='b208')
root.DatumPointByCoordinate(coords=(-0.29074,-0.80484,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b266')
root.DatumPointByCoordinate(coords=(0,0,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b22')
root.DatumPointByCoordinate(coords=(0.12296,-0.09559,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b23')
root.DatumPointByCoordinate(coords=(0.20191,-0.15697,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b52')
root.DatumPointByCoordinate(coords=(0.28086,-0.21834,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b68')
root.DatumPointByCoordinate(coords=(0.35981,-0.27972,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b92')
root.DatumPointByCoordinate(coords=(0.35981,-0.27972,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b93')
root.DatumPointByCoordinate(coords=(0.32638,-0.26713,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b94')
root.DatumPointByCoordinate(coords=(0.2328,-0.23189,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b153')
root.DatumPointByCoordinate(coords=(0.43876,-0.34109,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b140')
root.DatumPointByCoordinate(coords=(0.51771,-0.40247,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b169')
root.DatumPointByCoordinate(coords=(0.59666,-0.46384,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b209')
root.DatumPointByCoordinate(coords=(0.59666,-0.46384,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b210')
root.DatumPointByCoordinate(coords=(0.60856,-0.46054,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b211')
root.DatumPointByCoordinate(coords=(0.67561,-0.52522,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b267')
root.DatumPointByCoordinate(coords=(0,0,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b24')
root.DatumPointByCoordinate(coords=(0.12891,0.087403,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b25')
root.DatumPointByCoordinate(coords=(0.21168,0.14352,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b53')
root.DatumPointByCoordinate(coords=(0.29444,0.19964,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b69')
root.DatumPointByCoordinate(coords=(0.37721,0.25576,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b95')
root.DatumPointByCoordinate(coords=(0.37721,0.25576,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b96')
root.DatumPointByCoordinate(coords=(0.37721,0.25576,-0.33572))
root.features.changeKey(fromName='Datum pt-1', toName='b97')
root.DatumPointByCoordinate(coords=(0.37721,0.25576,-0.43572))
root.features.changeKey(fromName='Datum pt-1', toName='b154')
root.DatumPointByCoordinate(coords=(0.45998,0.31188,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b141')
root.DatumPointByCoordinate(coords=(0.54275,0.368,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b170')
root.DatumPointByCoordinate(coords=(0.62552,0.42412,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b212')
root.DatumPointByCoordinate(coords=(0.62552,0.42412,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b213')
root.DatumPointByCoordinate(coords=(0.62552,0.42412,-0.31236))
root.features.changeKey(fromName='Datum pt-1', toName='b214')
root.DatumPointByCoordinate(coords=(0.70829,0.48024,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b268')
root.DatumPointByCoordinate(coords=(0,0,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b26')
root.DatumPointByCoordinate(coords=(-0.04329,0.14961,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b27')
root.DatumPointByCoordinate(coords=(-0.071086,0.24567,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b54')
root.DatumPointByCoordinate(coords=(-0.098882,0.34173,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b70')
root.DatumPointByCoordinate(coords=(-0.12668,0.43779,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b98')
root.DatumPointByCoordinate(coords=(-0.12668,0.43779,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b99')
root.DatumPointByCoordinate(coords=(-0.10244,0.41155,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b100')
root.DatumPointByCoordinate(coords=(-0.034586,0.33809,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b155')
root.DatumPointByCoordinate(coords=(-0.15447,0.53385,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b142')
root.DatumPointByCoordinate(coords=(-0.18227,0.6299,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b171')
root.DatumPointByCoordinate(coords=(-0.21006,0.72596,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b215')
root.DatumPointByCoordinate(coords=(-0.21006,0.72596,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b216')
root.DatumPointByCoordinate(coords=(-0.22189,0.72237,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b217')
root.DatumPointByCoordinate(coords=(-0.23786,0.82202,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b269')
root.DatumPointByCoordinate(coords=(0,0,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b28')
root.DatumPointByCoordinate(coords=(-0.15566,0.0050597,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b29')
root.DatumPointByCoordinate(coords=(-0.25561,0.0083084,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b55')
root.DatumPointByCoordinate(coords=(-0.35556,0.011557,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b71')
root.DatumPointByCoordinate(coords=(-0.4555,0.014806,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b101')
root.DatumPointByCoordinate(coords=(-0.4555,0.014806,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b102')
root.DatumPointByCoordinate(coords=(-0.4555,0.014806,-0.33572))
root.features.changeKey(fromName='Datum pt-1', toName='b103')
root.DatumPointByCoordinate(coords=(-0.4555,0.014806,-0.43572))
root.features.changeKey(fromName='Datum pt-1', toName='b156')
root.DatumPointByCoordinate(coords=(-0.55545,0.018054,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b143')
root.DatumPointByCoordinate(coords=(-0.6554,0.021303,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b172')
root.DatumPointByCoordinate(coords=(-0.75535,0.024552,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b218')
root.DatumPointByCoordinate(coords=(-0.75535,0.024552,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b219')
root.DatumPointByCoordinate(coords=(-0.75535,0.024552,-0.31236))
root.features.changeKey(fromName='Datum pt-1', toName='b220')
root.DatumPointByCoordinate(coords=(-0.85529,0.027801,-0.3))
root.features.changeKey(fromName='Datum pt-1', toName='b270')
root.DatumPointByCoordinate(coords=(0,0,-0.4))
root.features.changeKey(fromName='Datum pt-1', toName='b45')
root.DatumPointByCoordinate(coords=(0,0,-0.5))
root.features.changeKey(fromName='Datum pt-1', toName='b61')
root.DatumPointByCoordinate(coords=(0,0,-0.6))
root.features.changeKey(fromName='Datum pt-1', toName='b77')
root.DatumPointByCoordinate(coords=(0,0,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b119')
root.DatumPointByCoordinate(coords=(0,0,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b120')
root.DatumPointByCoordinate(coords=(0.029426,-0.15294,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b121')
root.DatumPointByCoordinate(coords=(0.04832,-0.25114,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b191')
root.DatumPointByCoordinate(coords=(0.067213,-0.34934,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b249')
root.DatumPointByCoordinate(coords=(0.086107,-0.44754,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b295')
root.DatumPointByCoordinate(coords=(0.086107,-0.44754,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b296')
root.DatumPointByCoordinate(coords=(0.086107,-0.44754,-0.73572))
root.features.changeKey(fromName='Datum pt-1', toName='b297')
root.DatumPointByCoordinate(coords=(0.086107,-0.44754,-0.83572))
root.features.changeKey(fromName='Datum pt-1', toName='b382')
root.DatumPointByCoordinate(coords=(0.105,-0.54574,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b359')
root.DatumPointByCoordinate(coords=(0.12389,-0.64393,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b429')
root.DatumPointByCoordinate(coords=(0.14279,-0.74213,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b503')
root.DatumPointByCoordinate(coords=(0.14279,-0.74213,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b504')
root.DatumPointByCoordinate(coords=(0.14501,-0.75429,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b505')
root.DatumPointByCoordinate(coords=(0.16168,-0.84033,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b584')
root.DatumPointByCoordinate(coords=(0,0,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b122')
root.DatumPointByCoordinate(coords=(0.15455,-0.019275,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b123')
root.DatumPointByCoordinate(coords=(0.25378,-0.031651,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b192')
root.DatumPointByCoordinate(coords=(0.35301,-0.044028,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b250')
root.DatumPointByCoordinate(coords=(0.45224,-0.056404,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b298')
root.DatumPointByCoordinate(coords=(0.45224,-0.056404,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b299')
root.DatumPointByCoordinate(coords=(0.46246,-0.090629,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b300')
root.DatumPointByCoordinate(coords=(0.49107,-0.18645,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b383')
root.DatumPointByCoordinate(coords=(0.55147,-0.06878,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b360')
root.DatumPointByCoordinate(coords=(0.6507,-0.081156,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b430')
root.DatumPointByCoordinate(coords=(0.74993,-0.093532,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b506')
root.DatumPointByCoordinate(coords=(0.74993,-0.093532,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b507')
root.DatumPointByCoordinate(coords=(0.74866,-0.081242,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b508')
root.DatumPointByCoordinate(coords=(0.84917,-0.10591,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b585')
root.DatumPointByCoordinate(coords=(0,0,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b124')
root.DatumPointByCoordinate(coords=(0.06609,0.14103,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b125')
root.DatumPointByCoordinate(coords=(0.10852,0.23158,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b193')
root.DatumPointByCoordinate(coords=(0.15096,0.32213,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b251')
root.DatumPointByCoordinate(coords=(0.19339,0.41268,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b301')
root.DatumPointByCoordinate(coords=(0.19339,0.41268,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b302')
root.DatumPointByCoordinate(coords=(0.19339,0.41268,-0.73572))
root.features.changeKey(fromName='Datum pt-1', toName='b303')
root.DatumPointByCoordinate(coords=(0.19339,0.41268,-0.83572))
root.features.changeKey(fromName='Datum pt-1', toName='b384')
root.DatumPointByCoordinate(coords=(0.23583,0.50323,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b361')
root.DatumPointByCoordinate(coords=(0.27826,0.59378,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b431')
root.DatumPointByCoordinate(coords=(0.3207,0.68433,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b509')
root.DatumPointByCoordinate(coords=(0.3207,0.68433,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b510')
root.DatumPointByCoordinate(coords=(0.30921,0.68887,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b511')
root.DatumPointByCoordinate(coords=(0.36313,0.77488,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b586')
root.DatumPointByCoordinate(coords=(0,0,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b126')
root.DatumPointByCoordinate(coords=(-0.1137,0.10643,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b127')
root.DatumPointByCoordinate(coords=(-0.18671,0.17477,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b194')
root.DatumPointByCoordinate(coords=(-0.25971,0.24311,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b252')
root.DatumPointByCoordinate(coords=(-0.33272,0.31145,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b304')
root.DatumPointByCoordinate(coords=(-0.33272,0.31145,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b305')
root.DatumPointByCoordinate(coords=(-0.33914,0.27632,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b306')
root.DatumPointByCoordinate(coords=(-0.35712,0.17795,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b385')
root.DatumPointByCoordinate(coords=(-0.40572,0.37979,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b362')
root.DatumPointByCoordinate(coords=(-0.47873,0.44813,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b432')
root.DatumPointByCoordinate(coords=(-0.55173,0.51647,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b512')
root.DatumPointByCoordinate(coords=(-0.62474,0.58481,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b587')
root.DatumPointByCoordinate(coords=(-0.62474,0.58481,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b588')
root.DatumPointByCoordinate(coords=(-0.6295,0.58806,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b589')
root.DatumPointByCoordinate(coords=(0,0,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b128')
root.DatumPointByCoordinate(coords=(-0.13636,-0.075247,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b129')
root.DatumPointByCoordinate(coords=(-0.22392,-0.12356,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b195')
root.DatumPointByCoordinate(coords=(-0.31147,-0.17188,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b253')
root.DatumPointByCoordinate(coords=(-0.39902,-0.22019,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b307')
root.DatumPointByCoordinate(coords=(-0.39902,-0.22019,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b308')
root.DatumPointByCoordinate(coords=(-0.39902,-0.22019,-0.73572))
root.features.changeKey(fromName='Datum pt-1', toName='b309')
root.DatumPointByCoordinate(coords=(-0.39902,-0.22019,-0.83572))
root.features.changeKey(fromName='Datum pt-1', toName='b386')
root.DatumPointByCoordinate(coords=(-0.48658,-0.2685,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b363')
root.DatumPointByCoordinate(coords=(-0.57413,-0.31682,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b433')
root.DatumPointByCoordinate(coords=(-0.66169,-0.36513,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b513')
root.DatumPointByCoordinate(coords=(-0.66169,-0.36513,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b514')
root.DatumPointByCoordinate(coords=(-0.65293,-0.37385,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b515')
root.DatumPointByCoordinate(coords=(-0.74924,-0.41345,-0.7))
root.features.changeKey(fromName='Datum pt-1', toName='b590')
root.DatumPointByCoordinate(coords=(0,0,-0.8))
root.features.changeKey(fromName='Datum pt-1', toName='b162')
root.DatumPointByCoordinate(coords=(0,0,-0.9))
root.features.changeKey(fromName='Datum pt-1', toName='b198')
root.DatumPointByCoordinate(coords=(0,0,-1))
root.features.changeKey(fromName='Datum pt-1', toName='b256')
root.DatumPointByCoordinate(coords=(0,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b2')
root.DatumPointByCoordinate(coords=(0.1,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b8')
root.DatumPointByCoordinate(coords=(0.2,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b14')
root.DatumPointByCoordinate(coords=(0.3,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b30')
root.DatumPointByCoordinate(coords=(0.3,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b31')
root.DatumPointByCoordinate(coords=(0.39871,-0.031921,0))
root.features.changeKey(fromName='Datum pt-1', toName='b32')
root.DatumPointByCoordinate(coords=(0.49386,-0.06269,0))
root.features.changeKey(fromName='Datum pt-1', toName='b56')
root.DatumPointByCoordinate(coords=(0.58901,-0.093459,0))
root.features.changeKey(fromName='Datum pt-1', toName='b72')
root.DatumPointByCoordinate(coords=(0.68416,-0.12423,0))
root.features.changeKey(fromName='Datum pt-1', toName='b104')
root.DatumPointByCoordinate(coords=(0.68416,-0.12423,0))
root.features.changeKey(fromName='Datum pt-1', toName='b105')
root.DatumPointByCoordinate(coords=(0.69606,-0.13171,0))
root.features.changeKey(fromName='Datum pt-1', toName='b106')
root.DatumPointByCoordinate(coords=(0.77931,-0.155,0))
root.features.changeKey(fromName='Datum pt-1', toName='b144')
root.DatumPointByCoordinate(coords=(0.4,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b46')
root.DatumPointByCoordinate(coords=(0.5,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b62')
root.DatumPointByCoordinate(coords=(0.6,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b78')
root.DatumPointByCoordinate(coords=(0.7,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b130')
root.DatumPointByCoordinate(coords=(0.7,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b131')
root.DatumPointByCoordinate(coords=(0.70358,0.068575,0))
root.features.changeKey(fromName='Datum pt-1', toName='b132')
root.DatumPointByCoordinate(coords=(0.7088,0.16844,0))
root.features.changeKey(fromName='Datum pt-1', toName='b196')
root.DatumPointByCoordinate(coords=(0.71402,0.2683,0))
root.features.changeKey(fromName='Datum pt-1', toName='b254')
root.DatumPointByCoordinate(coords=(0.8,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b163')
root.DatumPointByCoordinate(coords=(0.9,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b199')
root.DatumPointByCoordinate(coords=(1,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b257')
root.DatumPointByCoordinate(coords=(1.1,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b327')
root.DatumPointByCoordinate(coords=(1.1,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b328')
root.DatumPointByCoordinate(coords=(1.1,0,-0.043751))
root.features.changeKey(fromName='Datum pt-1', toName='b329')
root.DatumPointByCoordinate(coords=(1.1,0,-0.14375))
root.features.changeKey(fromName='Datum pt-1', toName='b461')
root.DatumPointByCoordinate(coords=(1.2,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b389')
root.DatumPointByCoordinate(coords=(1.3,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b463')
root.DatumPointByCoordinate(coords=(1.4,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b556')
root.DatumPointByCoordinate(coords=(1.4,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b557')
root.DatumPointByCoordinate(coords=(1.4,0,-0.028343))
root.features.changeKey(fromName='Datum pt-1', toName='b558')
root.DatumPointByCoordinate(coords=(1.5,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b641')
root.DatumPointByCoordinate(coords=(1.6,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b733')
root.DatumPointByCoordinate(coords=(1.7,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b836')
root.DatumPointByCoordinate(coords=(1.7,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b837')
root.DatumPointByCoordinate(coords=(1.7,0,-0.014749))
root.features.changeKey(fromName='Datum pt-1', toName='b838')
root.DatumPointByCoordinate(coords=(1.8,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b948')
root.DatumPointByCoordinate(coords=(1.9,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1064')
root.DatumPointByCoordinate(coords=(2,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1192')
root.DatumPointByCoordinate(coords=(2,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1193')
root.DatumPointByCoordinate(coords=(2,0,-0.0024916))
root.features.changeKey(fromName='Datum pt-1', toName='b1194')
root.DatumPointByCoordinate(coords=(0,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b3')
root.DatumPointByCoordinate(coords=(0.030902,0.095106,0))
root.features.changeKey(fromName='Datum pt-1', toName='b9')
root.DatumPointByCoordinate(coords=(0.061803,0.19021,0))
root.features.changeKey(fromName='Datum pt-1', toName='b15')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,0))
root.features.changeKey(fromName='Datum pt-1', toName='b33')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,0))
root.features.changeKey(fromName='Datum pt-1', toName='b34')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,-0.10374))
root.features.changeKey(fromName='Datum pt-1', toName='b35')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,-0.20374))
root.features.changeKey(fromName='Datum pt-1', toName='b57')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,-0.30374))
root.features.changeKey(fromName='Datum pt-1', toName='b73')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b107')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b108')
root.DatumPointByCoordinate(coords=(0.10128,0.29645,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b109')
root.DatumPointByCoordinate(coords=(0.092705,0.28532,-0.50374))
root.features.changeKey(fromName='Datum pt-1', toName='b145')
root.DatumPointByCoordinate(coords=(0.12361,0.38042,0))
root.features.changeKey(fromName='Datum pt-1', toName='b47')
root.DatumPointByCoordinate(coords=(0.15451,0.47553,0))
root.features.changeKey(fromName='Datum pt-1', toName='b63')
root.DatumPointByCoordinate(coords=(0.18541,0.57063,0))
root.features.changeKey(fromName='Datum pt-1', toName='b79')
root.DatumPointByCoordinate(coords=(0.18541,0.57063,0))
root.features.changeKey(fromName='Datum pt-1', toName='b80')
root.DatumPointByCoordinate(coords=(0.18541,0.57063,-0.0761))
root.features.changeKey(fromName='Datum pt-1', toName='b81')
root.DatumPointByCoordinate(coords=(0.18541,0.57063,-0.1761))
root.features.changeKey(fromName='Datum pt-1', toName='b149')
root.DatumPointByCoordinate(coords=(0.18541,0.57063,-0.2761))
root.features.changeKey(fromName='Datum pt-1', toName='b178')
root.DatumPointByCoordinate(coords=(0.21631,0.66574,0))
root.features.changeKey(fromName='Datum pt-1', toName='b133')
root.DatumPointByCoordinate(coords=(0.24721,0.76085,0))
root.features.changeKey(fromName='Datum pt-1', toName='b164')
root.DatumPointByCoordinate(coords=(0.27812,0.85595,0))
root.features.changeKey(fromName='Datum pt-1', toName='b200')
root.DatumPointByCoordinate(coords=(0.30902,0.95106,0))
root.features.changeKey(fromName='Datum pt-1', toName='b258')
root.DatumPointByCoordinate(coords=(0.30902,0.95106,0))
root.features.changeKey(fromName='Datum pt-1', toName='b259')
root.DatumPointByCoordinate(coords=(0.35282,0.92817,0))
root.features.changeKey(fromName='Datum pt-1', toName='b260')
root.DatumPointByCoordinate(coords=(0.44145,0.88187,0))
root.features.changeKey(fromName='Datum pt-1', toName='b377')
root.DatumPointByCoordinate(coords=(0.33992,1.0462,0))
root.features.changeKey(fromName='Datum pt-1', toName='b330')
root.DatumPointByCoordinate(coords=(0.37082,1.1413,0))
root.features.changeKey(fromName='Datum pt-1', toName='b390')
root.DatumPointByCoordinate(coords=(0.40172,1.2364,0))
root.features.changeKey(fromName='Datum pt-1', toName='b464')
root.DatumPointByCoordinate(coords=(0.40172,1.2364,0))
root.features.changeKey(fromName='Datum pt-1', toName='b465')
root.DatumPointByCoordinate(coords=(0.3736,1.2186,0))
root.features.changeKey(fromName='Datum pt-1', toName='b466')
root.DatumPointByCoordinate(coords=(0.43262,1.3315,0))
root.features.changeKey(fromName='Datum pt-1', toName='b559')
root.DatumPointByCoordinate(coords=(0.46353,1.4266,0))
root.features.changeKey(fromName='Datum pt-1', toName='b642')
root.DatumPointByCoordinate(coords=(0.49443,1.5217,0))
root.features.changeKey(fromName='Datum pt-1', toName='b734')
root.DatumPointByCoordinate(coords=(0.49443,1.5217,0))
root.features.changeKey(fromName='Datum pt-1', toName='b735')
root.DatumPointByCoordinate(coords=(0.48227,1.5069,0))
root.features.changeKey(fromName='Datum pt-1', toName='b736')
root.DatumPointByCoordinate(coords=(0.52533,1.6168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b839')
root.DatumPointByCoordinate(coords=(0.55623,1.7119,0))
root.features.changeKey(fromName='Datum pt-1', toName='b949')
root.DatumPointByCoordinate(coords=(0.58713,1.807,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1065')
root.DatumPointByCoordinate(coords=(0.58713,1.807,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1066')
root.DatumPointByCoordinate(coords=(0.58817,1.8134,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1067')
root.DatumPointByCoordinate(coords=(0.61803,1.9021,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1195')
root.DatumPointByCoordinate(coords=(0,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b4')
root.DatumPointByCoordinate(coords=(-0.080902,0.058779,0))
root.features.changeKey(fromName='Datum pt-1', toName='b10')
root.DatumPointByCoordinate(coords=(-0.1618,0.11756,0))
root.features.changeKey(fromName='Datum pt-1', toName='b16')
root.DatumPointByCoordinate(coords=(-0.24271,0.17634,0))
root.features.changeKey(fromName='Datum pt-1', toName='b36')
root.DatumPointByCoordinate(coords=(-0.24271,0.17634,0))
root.features.changeKey(fromName='Datum pt-1', toName='b37')
root.DatumPointByCoordinate(coords=(-0.20263,0.27202,0))
root.features.changeKey(fromName='Datum pt-1', toName='b38')
root.DatumPointByCoordinate(coords=(-0.16399,0.36426,0))
root.features.changeKey(fromName='Datum pt-1', toName='b58')
root.DatumPointByCoordinate(coords=(-0.12536,0.4565,0))
root.features.changeKey(fromName='Datum pt-1', toName='b74')
root.DatumPointByCoordinate(coords=(-0.08673,0.54873,0))
root.features.changeKey(fromName='Datum pt-1', toName='b110')
root.DatumPointByCoordinate(coords=(-0.08673,0.54873,0))
root.features.changeKey(fromName='Datum pt-1', toName='b111')
root.DatumPointByCoordinate(coords=(-0.077153,0.53844,0))
root.features.changeKey(fromName='Datum pt-1', toName='b112')
root.DatumPointByCoordinate(coords=(-0.048098,0.64097,0))
root.features.changeKey(fromName='Datum pt-1', toName='b146')
root.DatumPointByCoordinate(coords=(-0.32361,0.23511,0))
root.features.changeKey(fromName='Datum pt-1', toName='b48')
root.DatumPointByCoordinate(coords=(-0.40451,0.29389,0))
root.features.changeKey(fromName='Datum pt-1', toName='b64')
root.DatumPointByCoordinate(coords=(-0.48541,0.35267,0))
root.features.changeKey(fromName='Datum pt-1', toName='b82')
root.DatumPointByCoordinate(coords=(-0.48541,0.35267,0))
root.features.changeKey(fromName='Datum pt-1', toName='b83')
root.DatumPointByCoordinate(coords=(-0.55787,0.37594,0))
root.features.changeKey(fromName='Datum pt-1', toName='b84')
root.DatumPointByCoordinate(coords=(-0.65308,0.40652,0))
root.features.changeKey(fromName='Datum pt-1', toName='b150')
root.DatumPointByCoordinate(coords=(-0.74829,0.4371,0))
root.features.changeKey(fromName='Datum pt-1', toName='b179')
root.DatumPointByCoordinate(coords=(-0.56631,0.41145,0))
root.features.changeKey(fromName='Datum pt-1', toName='b134')
root.DatumPointByCoordinate(coords=(-0.64721,0.47023,0))
root.features.changeKey(fromName='Datum pt-1', toName='b165')
root.DatumPointByCoordinate(coords=(-0.72812,0.52901,0))
root.features.changeKey(fromName='Datum pt-1', toName='b201')
root.DatumPointByCoordinate(coords=(-0.72812,0.52901,0))
root.features.changeKey(fromName='Datum pt-1', toName='b202')
root.DatumPointByCoordinate(coords=(-0.77746,0.50378,0))
root.features.changeKey(fromName='Datum pt-1', toName='b203')
root.DatumPointByCoordinate(coords=(-0.8665,0.45827,0))
root.features.changeKey(fromName='Datum pt-1', toName='b316')
root.DatumPointByCoordinate(coords=(-0.80902,0.58779,0))
root.features.changeKey(fromName='Datum pt-1', toName='b261')
root.DatumPointByCoordinate(coords=(-0.88992,0.64656,0))
root.features.changeKey(fromName='Datum pt-1', toName='b331')
root.DatumPointByCoordinate(coords=(-0.97082,0.70534,0))
root.features.changeKey(fromName='Datum pt-1', toName='b391')
root.DatumPointByCoordinate(coords=(-1.0517,0.76412,0))
root.features.changeKey(fromName='Datum pt-1', toName='b467')
root.DatumPointByCoordinate(coords=(-1.0517,0.76412,0))
root.features.changeKey(fromName='Datum pt-1', toName='b468')
root.DatumPointByCoordinate(coords=(-1.0806,0.74756,0))
root.features.changeKey(fromName='Datum pt-1', toName='b469')
root.DatumPointByCoordinate(coords=(-1.1326,0.8229,0))
root.features.changeKey(fromName='Datum pt-1', toName='b560')
root.DatumPointByCoordinate(coords=(-1.2135,0.88168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b643')
root.DatumPointByCoordinate(coords=(-1.2944,0.94046,0))
root.features.changeKey(fromName='Datum pt-1', toName='b737')
root.DatumPointByCoordinate(coords=(-1.3753,0.99923,0))
root.features.changeKey(fromName='Datum pt-1', toName='b840')
root.DatumPointByCoordinate(coords=(-1.3753,0.99923,0))
root.features.changeKey(fromName='Datum pt-1', toName='b841')
root.DatumPointByCoordinate(coords=(-1.3753,0.99923,-0.014749))
root.features.changeKey(fromName='Datum pt-1', toName='b842')
root.DatumPointByCoordinate(coords=(-1.4562,1.058,0))
root.features.changeKey(fromName='Datum pt-1', toName='b950')
root.DatumPointByCoordinate(coords=(-1.5371,1.1168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1068')
root.DatumPointByCoordinate(coords=(-1.618,1.1756,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1196')
root.DatumPointByCoordinate(coords=(-1.618,1.1756,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1197')
root.DatumPointByCoordinate(coords=(-1.6194,1.1735,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1198')
root.DatumPointByCoordinate(coords=(0,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b5')
root.DatumPointByCoordinate(coords=(-0.080902,-0.058779,0))
root.features.changeKey(fromName='Datum pt-1', toName='b11')
root.DatumPointByCoordinate(coords=(-0.1618,-0.11756,0))
root.features.changeKey(fromName='Datum pt-1', toName='b17')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,0))
root.features.changeKey(fromName='Datum pt-1', toName='b39')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,0))
root.features.changeKey(fromName='Datum pt-1', toName='b40')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,-0.10374))
root.features.changeKey(fromName='Datum pt-1', toName='b41')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,-0.20374))
root.features.changeKey(fromName='Datum pt-1', toName='b59')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,-0.30374))
root.features.changeKey(fromName='Datum pt-1', toName='b75')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b113')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b114')
root.DatumPointByCoordinate(coords=(-0.23409,-0.16523,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b115')
root.DatumPointByCoordinate(coords=(-0.24271,-0.17634,-0.50374))
root.features.changeKey(fromName='Datum pt-1', toName='b147')
root.DatumPointByCoordinate(coords=(-0.32361,-0.23511,0))
root.features.changeKey(fromName='Datum pt-1', toName='b49')
root.DatumPointByCoordinate(coords=(-0.40451,-0.29389,0))
root.features.changeKey(fromName='Datum pt-1', toName='b65')
root.DatumPointByCoordinate(coords=(-0.48541,-0.35267,0))
root.features.changeKey(fromName='Datum pt-1', toName='b85')
root.DatumPointByCoordinate(coords=(-0.48541,-0.35267,0))
root.features.changeKey(fromName='Datum pt-1', toName='b86')
root.DatumPointByCoordinate(coords=(-0.42032,-0.39209,0))
root.features.changeKey(fromName='Datum pt-1', toName='b87')
root.DatumPointByCoordinate(coords=(-0.33478,-0.44389,0))
root.features.changeKey(fromName='Datum pt-1', toName='b151')
root.DatumPointByCoordinate(coords=(-0.24924,-0.49569,0))
root.features.changeKey(fromName='Datum pt-1', toName='b180')
root.DatumPointByCoordinate(coords=(-0.56631,-0.41145,0))
root.features.changeKey(fromName='Datum pt-1', toName='b135')
root.DatumPointByCoordinate(coords=(-0.64721,-0.47023,0))
root.features.changeKey(fromName='Datum pt-1', toName='b166')
root.DatumPointByCoordinate(coords=(-0.72812,-0.52901,0))
root.features.changeKey(fromName='Datum pt-1', toName='b204')
root.DatumPointByCoordinate(coords=(-0.80902,-0.58779,0))
root.features.changeKey(fromName='Datum pt-1', toName='b262')
root.DatumPointByCoordinate(coords=(-0.80902,-0.58779,0))
root.features.changeKey(fromName='Datum pt-1', toName='b263')
root.DatumPointByCoordinate(coords=(-0.80902,-0.58779,-0.049417))
root.features.changeKey(fromName='Datum pt-1', toName='b264')
root.DatumPointByCoordinate(coords=(-0.80902,-0.58779,-0.14942))
root.features.changeKey(fromName='Datum pt-1', toName='b378')
root.DatumPointByCoordinate(coords=(-0.88992,-0.64656,0))
root.features.changeKey(fromName='Datum pt-1', toName='b332')
root.DatumPointByCoordinate(coords=(-0.97082,-0.70534,0))
root.features.changeKey(fromName='Datum pt-1', toName='b392')
root.DatumPointByCoordinate(coords=(-1.0517,-0.76412,0))
root.features.changeKey(fromName='Datum pt-1', toName='b470')
root.DatumPointByCoordinate(coords=(-1.1326,-0.8229,0))
root.features.changeKey(fromName='Datum pt-1', toName='b561')
root.DatumPointByCoordinate(coords=(-1.1326,-0.8229,0))
root.features.changeKey(fromName='Datum pt-1', toName='b562')
root.DatumPointByCoordinate(coords=(-1.1326,-0.8229,-0.028343))
root.features.changeKey(fromName='Datum pt-1', toName='b563')
root.DatumPointByCoordinate(coords=(-1.2135,-0.88168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b644')
root.DatumPointByCoordinate(coords=(-1.2944,-0.94046,0))
root.features.changeKey(fromName='Datum pt-1', toName='b738')
root.DatumPointByCoordinate(coords=(-1.3753,-0.99923,0))
root.features.changeKey(fromName='Datum pt-1', toName='b843')
root.DatumPointByCoordinate(coords=(-1.4562,-1.058,0))
root.features.changeKey(fromName='Datum pt-1', toName='b951')
root.DatumPointByCoordinate(coords=(-1.4562,-1.058,0))
root.features.changeKey(fromName='Datum pt-1', toName='b952')
root.DatumPointByCoordinate(coords=(-1.4562,-1.058,-0.010532))
root.features.changeKey(fromName='Datum pt-1', toName='b953')
root.DatumPointByCoordinate(coords=(-1.5371,-1.1168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1069')
root.DatumPointByCoordinate(coords=(-1.618,-1.1756,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1199')
root.DatumPointByCoordinate(coords=(0,0,0))
root.features.changeKey(fromName='Datum pt-1', toName='b6')
root.DatumPointByCoordinate(coords=(0.030902,-0.095106,0))
root.features.changeKey(fromName='Datum pt-1', toName='b12')
root.DatumPointByCoordinate(coords=(0.061803,-0.19021,0))
root.features.changeKey(fromName='Datum pt-1', toName='b18')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,0))
root.features.changeKey(fromName='Datum pt-1', toName='b42')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,0))
root.features.changeKey(fromName='Datum pt-1', toName='b43')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,-0.10374))
root.features.changeKey(fromName='Datum pt-1', toName='b44')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,-0.20374))
root.features.changeKey(fromName='Datum pt-1', toName='b60')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,-0.30374))
root.features.changeKey(fromName='Datum pt-1', toName='b76')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b116')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b117')
root.DatumPointByCoordinate(coords=(0.082584,-0.29507,-0.40374))
root.features.changeKey(fromName='Datum pt-1', toName='b118')
root.DatumPointByCoordinate(coords=(0.092705,-0.28532,-0.50374))
root.features.changeKey(fromName='Datum pt-1', toName='b148')
root.DatumPointByCoordinate(coords=(0.12361,-0.38042,0))
root.features.changeKey(fromName='Datum pt-1', toName='b50')
root.DatumPointByCoordinate(coords=(0.15451,-0.47553,0))
root.features.changeKey(fromName='Datum pt-1', toName='b66')
root.DatumPointByCoordinate(coords=(0.18541,-0.57063,0))
root.features.changeKey(fromName='Datum pt-1', toName='b88')
root.DatumPointByCoordinate(coords=(0.21631,-0.66574,0))
root.features.changeKey(fromName='Datum pt-1', toName='b136')
root.DatumPointByCoordinate(coords=(0.21631,-0.66574,0))
root.features.changeKey(fromName='Datum pt-1', toName='b137')
root.DatumPointByCoordinate(coords=(0.21631,-0.66574,-0.068668))
root.features.changeKey(fromName='Datum pt-1', toName='b138')
root.DatumPointByCoordinate(coords=(0.21631,-0.66574,-0.16867))
root.features.changeKey(fromName='Datum pt-1', toName='b197')
root.DatumPointByCoordinate(coords=(0.21631,-0.66574,-0.26867))
root.features.changeKey(fromName='Datum pt-1', toName='b255')
root.DatumPointByCoordinate(coords=(0.24721,-0.76085,0))
root.features.changeKey(fromName='Datum pt-1', toName='b167')
root.DatumPointByCoordinate(coords=(0.27812,-0.85595,0))
root.features.changeKey(fromName='Datum pt-1', toName='b205')
root.DatumPointByCoordinate(coords=(0.30902,-0.95106,0))
root.features.changeKey(fromName='Datum pt-1', toName='b265')
root.DatumPointByCoordinate(coords=(0.33992,-1.0462,0))
root.features.changeKey(fromName='Datum pt-1', toName='b333')
root.DatumPointByCoordinate(coords=(0.33992,-1.0462,0))
root.features.changeKey(fromName='Datum pt-1', toName='b334')
root.DatumPointByCoordinate(coords=(0.33992,-1.0462,-0.043751))
root.features.changeKey(fromName='Datum pt-1', toName='b335')
root.DatumPointByCoordinate(coords=(0.33992,-1.0462,-0.14375))
root.features.changeKey(fromName='Datum pt-1', toName='b462')
root.DatumPointByCoordinate(coords=(0.37082,-1.1413,0))
root.features.changeKey(fromName='Datum pt-1', toName='b393')
root.DatumPointByCoordinate(coords=(0.40172,-1.2364,0))
root.features.changeKey(fromName='Datum pt-1', toName='b471')
root.DatumPointByCoordinate(coords=(0.43262,-1.3315,0))
root.features.changeKey(fromName='Datum pt-1', toName='b564')
root.DatumPointByCoordinate(coords=(0.43262,-1.3315,0))
root.features.changeKey(fromName='Datum pt-1', toName='b565')
root.DatumPointByCoordinate(coords=(0.43262,-1.3315,-0.028343))
root.features.changeKey(fromName='Datum pt-1', toName='b566')
root.DatumPointByCoordinate(coords=(0.46353,-1.4266,0))
root.features.changeKey(fromName='Datum pt-1', toName='b645')
root.DatumPointByCoordinate(coords=(0.49443,-1.5217,0))
root.features.changeKey(fromName='Datum pt-1', toName='b739')
root.DatumPointByCoordinate(coords=(0.52533,-1.6168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b844')
root.DatumPointByCoordinate(coords=(0.52533,-1.6168,0))
root.features.changeKey(fromName='Datum pt-1', toName='b845')
root.DatumPointByCoordinate(coords=(0.52533,-1.6168,-0.014749))
root.features.changeKey(fromName='Datum pt-1', toName='b846')
root.DatumPointByCoordinate(coords=(0.55623,-1.7119,0))
root.features.changeKey(fromName='Datum pt-1', toName='b954')
root.DatumPointByCoordinate(coords=(0.58713,-1.807,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1070')
root.DatumPointByCoordinate(coords=(0.61803,-1.9021,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1200')
root.DatumPointByCoordinate(coords=(0.61803,-1.9021,0))
root.features.changeKey(fromName='Datum pt-1', toName='b1201')
root.DatumPointByCoordinate(coords=(0.61803,-1.9021,-0.0024916))
root.features.changeKey(fromName='Datum pt-1', toName='b1202')

# Internodes creation
root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1'].id], root.datums[root.features['b7'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1b7')

reg = Region(edges = root.getFeatureEdges('b1b7'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b7'].id], root.datums[root.features['b13'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b7b13')

reg = Region(edges = root.getFeatureEdges('b7b13'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b13'].id], root.datums[root.features['b19'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b13b19')

reg = Region(edges = root.getFeatureEdges('b13b19'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b20'].id], root.datums[root.features['b21'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b20b21')

reg = Region(edges = root.getFeatureEdges('b20b21'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b21'].id], root.datums[root.features['b51'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b21b51')

reg = Region(edges = root.getFeatureEdges('b21b51'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b51'].id], root.datums[root.features['b67'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b51b67')

reg = Region(edges = root.getFeatureEdges('b51b67'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b67'].id], root.datums[root.features['b89'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b67b89')

reg = Region(edges = root.getFeatureEdges('b67b89'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b90'].id], root.datums[root.features['b91'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b90b91')

reg = Region(edges = root.getFeatureEdges('b90b91'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b91'].id], root.datums[root.features['b152'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b91b152')

reg = Region(edges = root.getFeatureEdges('b91b152'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b89'].id], root.datums[root.features['b139'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b89b139')

reg = Region(edges = root.getFeatureEdges('b89b139'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b139'].id], root.datums[root.features['b168'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b139b168')

reg = Region(edges = root.getFeatureEdges('b139b168'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b168'].id], root.datums[root.features['b206'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b168b206')

reg = Region(edges = root.getFeatureEdges('b168b206'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b207'].id], root.datums[root.features['b208'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b207b208')

reg = Region(edges = root.getFeatureEdges('b207b208'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b206'].id], root.datums[root.features['b266'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b206b266')

reg = Region(edges = root.getFeatureEdges('b206b266'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.36124,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b22'].id], root.datums[root.features['b23'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b22b23')

reg = Region(edges = root.getFeatureEdges('b22b23'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b23'].id], root.datums[root.features['b52'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b23b52')

reg = Region(edges = root.getFeatureEdges('b23b52'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b52'].id], root.datums[root.features['b68'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b52b68')

reg = Region(edges = root.getFeatureEdges('b52b68'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b68'].id], root.datums[root.features['b92'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b68b92')

reg = Region(edges = root.getFeatureEdges('b68b92'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b93'].id], root.datums[root.features['b94'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b93b94')

reg = Region(edges = root.getFeatureEdges('b93b94'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,2.6554,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b94'].id], root.datums[root.features['b153'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b94b153')

reg = Region(edges = root.getFeatureEdges('b94b153'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,2.6554,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b92'].id], root.datums[root.features['b140'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b92b140')

reg = Region(edges = root.getFeatureEdges('b92b140'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b140'].id], root.datums[root.features['b169'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b140b169')

reg = Region(edges = root.getFeatureEdges('b140b169'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b169'].id], root.datums[root.features['b209'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b169b209')

reg = Region(edges = root.getFeatureEdges('b169b209'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b210'].id], root.datums[root.features['b211'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b210b211')

reg = Region(edges = root.getFeatureEdges('b210b211'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-3.6087,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b209'].id], root.datums[root.features['b267'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b209b267')

reg = Region(edges = root.getFeatureEdges('b209b267'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.2863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b24'].id], root.datums[root.features['b25'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b24b25')

reg = Region(edges = root.getFeatureEdges('b24b25'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b25'].id], root.datums[root.features['b53'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b25b53')

reg = Region(edges = root.getFeatureEdges('b25b53'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b53'].id], root.datums[root.features['b69'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b53b69')

reg = Region(edges = root.getFeatureEdges('b53b69'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b69'].id], root.datums[root.features['b95'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b69b95')

reg = Region(edges = root.getFeatureEdges('b69b95'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b96'].id], root.datums[root.features['b97'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b96b97')

reg = Region(edges = root.getFeatureEdges('b96b97'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b97'].id], root.datums[root.features['b154'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b97b154')

reg = Region(edges = root.getFeatureEdges('b97b154'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b95'].id], root.datums[root.features['b141'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b95b141')

reg = Region(edges = root.getFeatureEdges('b95b141'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b141'].id], root.datums[root.features['b170'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b141b170')

reg = Region(edges = root.getFeatureEdges('b141b170'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b170'].id], root.datums[root.features['b212'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b170b212')

reg = Region(edges = root.getFeatureEdges('b170b212'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b213'].id], root.datums[root.features['b214'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b213b214')

reg = Region(edges = root.getFeatureEdges('b213b214'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b212'].id], root.datums[root.features['b268'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b212b268')

reg = Region(edges = root.getFeatureEdges('b212b268'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.4749,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b26'].id], root.datums[root.features['b27'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b26b27')

reg = Region(edges = root.getFeatureEdges('b26b27'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b27'].id], root.datums[root.features['b54'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b27b54')

reg = Region(edges = root.getFeatureEdges('b27b54'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b54'].id], root.datums[root.features['b70'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b54b70')

reg = Region(edges = root.getFeatureEdges('b54b70'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b70'].id], root.datums[root.features['b98'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b70b98')

reg = Region(edges = root.getFeatureEdges('b70b98'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b99'].id], root.datums[root.features['b100'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b99b100')

reg = Region(edges = root.getFeatureEdges('b99b100'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.92375,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b100'].id], root.datums[root.features['b155'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b100b155')

reg = Region(edges = root.getFeatureEdges('b100b155'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.92375,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b98'].id], root.datums[root.features['b142'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b98b142')

reg = Region(edges = root.getFeatureEdges('b98b142'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b142'].id], root.datums[root.features['b171'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b142b171')

reg = Region(edges = root.getFeatureEdges('b142b171'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b171'].id], root.datums[root.features['b215'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b171b215')

reg = Region(edges = root.getFeatureEdges('b171b215'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b216'].id], root.datums[root.features['b217'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b216b217')

reg = Region(edges = root.getFeatureEdges('b216b217'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-3.2866,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b215'].id], root.datums[root.features['b269'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b215b269')

reg = Region(edges = root.getFeatureEdges('b215b269'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.28936,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b28'].id], root.datums[root.features['b29'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b28b29')

reg = Region(edges = root.getFeatureEdges('b28b29'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b29'].id], root.datums[root.features['b55'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b29b55')

reg = Region(edges = root.getFeatureEdges('b29b55'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b55'].id], root.datums[root.features['b71'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b55b71')

reg = Region(edges = root.getFeatureEdges('b55b71'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b71'].id], root.datums[root.features['b101'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b71b101')

reg = Region(edges = root.getFeatureEdges('b71b101'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b102'].id], root.datums[root.features['b103'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b102b103')

reg = Region(edges = root.getFeatureEdges('b102b103'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b103'].id], root.datums[root.features['b156'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b103b156')

reg = Region(edges = root.getFeatureEdges('b103b156'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b101'].id], root.datums[root.features['b143'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b101b143')

reg = Region(edges = root.getFeatureEdges('b101b143'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b143'].id], root.datums[root.features['b172'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b143b172')

reg = Region(edges = root.getFeatureEdges('b143b172'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b172'].id], root.datums[root.features['b218'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b172b218')

reg = Region(edges = root.getFeatureEdges('b172b218'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b219'].id], root.datums[root.features['b220'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b219b220')

reg = Region(edges = root.getFeatureEdges('b219b220'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b218'].id], root.datums[root.features['b270'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b218b270')

reg = Region(edges = root.getFeatureEdges('b218b270'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,30.7653,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b19'].id], root.datums[root.features['b45'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b19b45')

reg = Region(edges = root.getFeatureEdges('b19b45'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b45'].id], root.datums[root.features['b61'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b45b61')

reg = Region(edges = root.getFeatureEdges('b45b61'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b61'].id], root.datums[root.features['b77'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b61b77')

reg = Region(edges = root.getFeatureEdges('b61b77'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b77'].id], root.datums[root.features['b119'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b77b119')

reg = Region(edges = root.getFeatureEdges('b77b119'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b120'].id], root.datums[root.features['b121'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b120b121')

reg = Region(edges = root.getFeatureEdges('b120b121'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b121'].id], root.datums[root.features['b191'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b121b191')

reg = Region(edges = root.getFeatureEdges('b121b191'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b191'].id], root.datums[root.features['b249'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b191b249')

reg = Region(edges = root.getFeatureEdges('b191b249'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b249'].id], root.datums[root.features['b295'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b249b295')

reg = Region(edges = root.getFeatureEdges('b249b295'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b296'].id], root.datums[root.features['b297'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b296b297')

reg = Region(edges = root.getFeatureEdges('b296b297'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b297'].id], root.datums[root.features['b382'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b297b382')

reg = Region(edges = root.getFeatureEdges('b297b382'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b295'].id], root.datums[root.features['b359'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b295b359')

reg = Region(edges = root.getFeatureEdges('b295b359'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b359'].id], root.datums[root.features['b429'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b359b429')

reg = Region(edges = root.getFeatureEdges('b359b429'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b429'].id], root.datums[root.features['b503'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b429b503')

reg = Region(edges = root.getFeatureEdges('b429b503'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b504'].id], root.datums[root.features['b505'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b504b505')

reg = Region(edges = root.getFeatureEdges('b504b505'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.18297,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b503'].id], root.datums[root.features['b584'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b503b584')

reg = Region(edges = root.getFeatureEdges('b503b584'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.1924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b122'].id], root.datums[root.features['b123'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b122b123')

reg = Region(edges = root.getFeatureEdges('b122b123'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b123'].id], root.datums[root.features['b192'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b123b192')

reg = Region(edges = root.getFeatureEdges('b123b192'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b192'].id], root.datums[root.features['b250'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b192b250')

reg = Region(edges = root.getFeatureEdges('b192b250'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b250'].id], root.datums[root.features['b298'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b250b298')

reg = Region(edges = root.getFeatureEdges('b250b298'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b299'].id], root.datums[root.features['b300'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b299b300')

reg = Region(edges = root.getFeatureEdges('b299b300'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.29861,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b300'].id], root.datums[root.features['b383'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b300b383')

reg = Region(edges = root.getFeatureEdges('b300b383'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.29861,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b298'].id], root.datums[root.features['b360'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b298b360')

reg = Region(edges = root.getFeatureEdges('b298b360'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b360'].id], root.datums[root.features['b430'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b360b430')

reg = Region(edges = root.getFeatureEdges('b360b430'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b430'].id], root.datums[root.features['b506'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b430b506')

reg = Region(edges = root.getFeatureEdges('b430b506'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b507'].id], root.datums[root.features['b508'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b507b508')

reg = Region(edges = root.getFeatureEdges('b507b508'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.10386,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b506'].id], root.datums[root.features['b585'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b506b585')

reg = Region(edges = root.getFeatureEdges('b506b585'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,8.0179,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b124'].id], root.datums[root.features['b125'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b124b125')

reg = Region(edges = root.getFeatureEdges('b124b125'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b125'].id], root.datums[root.features['b193'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b125b193')

reg = Region(edges = root.getFeatureEdges('b125b193'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b193'].id], root.datums[root.features['b251'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b193b251')

reg = Region(edges = root.getFeatureEdges('b193b251'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b251'].id], root.datums[root.features['b301'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b251b301')

reg = Region(edges = root.getFeatureEdges('b251b301'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b302'].id], root.datums[root.features['b303'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b302b303')

reg = Region(edges = root.getFeatureEdges('b302b303'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b303'].id], root.datums[root.features['b384'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b303b384')

reg = Region(edges = root.getFeatureEdges('b303b384'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b301'].id], root.datums[root.features['b361'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b301b361')

reg = Region(edges = root.getFeatureEdges('b301b361'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b361'].id], root.datums[root.features['b431'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b361b431')

reg = Region(edges = root.getFeatureEdges('b361b431'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b431'].id], root.datums[root.features['b509'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b431b509')

reg = Region(edges = root.getFeatureEdges('b431b509'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b510'].id], root.datums[root.features['b511'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b510b511')

reg = Region(edges = root.getFeatureEdges('b510b511'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,2.5297,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b509'].id], root.datums[root.features['b586'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b509b586')

reg = Region(edges = root.getFeatureEdges('b509b586'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.46863,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b126'].id], root.datums[root.features['b127'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b126b127')

reg = Region(edges = root.getFeatureEdges('b126b127'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b127'].id], root.datums[root.features['b194'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b127b194')

reg = Region(edges = root.getFeatureEdges('b127b194'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b194'].id], root.datums[root.features['b252'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b194b252')

reg = Region(edges = root.getFeatureEdges('b194b252'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b252'].id], root.datums[root.features['b304'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b252b304')

reg = Region(edges = root.getFeatureEdges('b252b304'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b305'].id], root.datums[root.features['b306'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b305b306')

reg = Region(edges = root.getFeatureEdges('b305b306'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.18278,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b306'].id], root.datums[root.features['b385'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b306b385')

reg = Region(edges = root.getFeatureEdges('b306b385'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.18278,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b304'].id], root.datums[root.features['b362'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b304b362')

reg = Region(edges = root.getFeatureEdges('b304b362'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b362'].id], root.datums[root.features['b432'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b362b432')

reg = Region(edges = root.getFeatureEdges('b362b432'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b432'].id], root.datums[root.features['b512'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b432b512')

reg = Region(edges = root.getFeatureEdges('b432b512'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b512'].id], root.datums[root.features['b587'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b512b587')

reg = Region(edges = root.getFeatureEdges('b512b587'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0683,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b588'].id], root.datums[root.features['b589'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b588b589')

reg = Region(edges = root.getFeatureEdges('b588b589'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.4631,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01112', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b128'].id], root.datums[root.features['b129'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b128b129')

reg = Region(edges = root.getFeatureEdges('b128b129'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b129'].id], root.datums[root.features['b195'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b129b195')

reg = Region(edges = root.getFeatureEdges('b129b195'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s14017', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b195'].id], root.datums[root.features['b253'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b195b253')

reg = Region(edges = root.getFeatureEdges('b195b253'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11298', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b253'].id], root.datums[root.features['b307'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b253b307')

reg = Region(edges = root.getFeatureEdges('b253b307'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09067', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b308'].id], root.datums[root.features['b309'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b308b309')

reg = Region(edges = root.getFeatureEdges('b308b309'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b309'].id], root.datums[root.features['b386'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b309b386')

reg = Region(edges = root.getFeatureEdges('b309b386'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04080', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b307'].id], root.datums[root.features['b363'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b307b363')

reg = Region(edges = root.getFeatureEdges('b307b363'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07144', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b363'].id], root.datums[root.features['b433'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b363b433')

reg = Region(edges = root.getFeatureEdges('b363b433'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05437', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b433'].id], root.datums[root.features['b513'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b433b513')

reg = Region(edges = root.getFeatureEdges('b433b513'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03891', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b514'].id], root.datums[root.features['b515'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b514b515')

reg = Region(edges = root.getFeatureEdges('b514b515'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.0047,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01751', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b513'].id], root.datums[root.features['b590'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b513b590')

reg = Region(edges = root.getFeatureEdges('b513b590'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.8122,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02471', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b119'].id], root.datums[root.features['b162'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b119b162')

reg = Region(edges = root.getFeatureEdges('b119b162'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b162'].id], root.datums[root.features['b198'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b162b198')

reg = Region(edges = root.getFeatureEdges('b162b198'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b198'].id], root.datums[root.features['b256'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b198b256')

reg = Region(edges = root.getFeatureEdges('b198b256'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b2'].id], root.datums[root.features['b8'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b2b8')

reg = Region(edges = root.getFeatureEdges('b2b8'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b8'].id], root.datums[root.features['b14'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b8b14')

reg = Region(edges = root.getFeatureEdges('b8b14'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s26372', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b14'].id], root.datums[root.features['b30'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b14b30')

reg = Region(edges = root.getFeatureEdges('b14b30'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s23220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b31'].id], root.datums[root.features['b32'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b31b32')

reg = Region(edges = root.getFeatureEdges('b31b32'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.0924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b32'].id], root.datums[root.features['b56'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b32b56')

reg = Region(edges = root.getFeatureEdges('b32b56'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.0924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b56'].id], root.datums[root.features['b72'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b56b72')

reg = Region(edges = root.getFeatureEdges('b56b72'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.0924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07332', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b72'].id], root.datums[root.features['b104'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b72b104')

reg = Region(edges = root.getFeatureEdges('b72b104'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.0924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04879', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b105'].id], root.datums[root.features['b106'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b105b106')

reg = Region(edges = root.getFeatureEdges('b105b106'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.59,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02196', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b104'].id], root.datums[root.features['b144'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b104b144')

reg = Region(edges = root.getFeatureEdges('b104b144'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.0924,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02811', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b30'].id], root.datums[root.features['b46'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b30b46')

reg = Region(edges = root.getFeatureEdges('b30b46'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s20749', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b46'].id], root.datums[root.features['b62'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b46b62')

reg = Region(edges = root.getFeatureEdges('b46b62'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s18669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b62'].id], root.datums[root.features['b78'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b62b78')

reg = Region(edges = root.getFeatureEdges('b62b78'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16850', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b78'].id], root.datums[root.features['b130'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b78b130')

reg = Region(edges = root.getFeatureEdges('b78b130'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s15220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b131'].id], root.datums[root.features['b132'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b131b132')

reg = Region(edges = root.getFeatureEdges('b131b132'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.052253,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06849', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b132'].id], root.datums[root.features['b196'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b132b196')

reg = Region(edges = root.getFeatureEdges('b132b196'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.052253,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06849', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b196'].id], root.datums[root.features['b254'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b196b254')

reg = Region(edges = root.getFeatureEdges('b196b254'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.052253,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03358', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b130'].id], root.datums[root.features['b163'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b130b163')

reg = Region(edges = root.getFeatureEdges('b130b163'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s13734', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b163'].id], root.datums[root.features['b199'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b163b199')

reg = Region(edges = root.getFeatureEdges('b163b199'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12362', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b199'].id], root.datums[root.features['b257'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b199b257')

reg = Region(edges = root.getFeatureEdges('b199b257'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11083', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b257'].id], root.datums[root.features['b327'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b257b327')

reg = Region(edges = root.getFeatureEdges('b257b327'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09883', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b328'].id], root.datums[root.features['b329'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b328b329')

reg = Region(edges = root.getFeatureEdges('b328b329'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04448', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b329'].id], root.datums[root.features['b461'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b329b461')

reg = Region(edges = root.getFeatureEdges('b329b461'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04448', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b327'].id], root.datums[root.features['b389'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b327b389')

reg = Region(edges = root.getFeatureEdges('b327b389'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s08750', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b389'].id], root.datums[root.features['b463'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b389b463')

reg = Region(edges = root.getFeatureEdges('b389b463'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07674', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b463'].id], root.datums[root.features['b556'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b463b556')

reg = Region(edges = root.getFeatureEdges('b463b556'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06649', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b557'].id], root.datums[root.features['b558'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b557b558')

reg = Region(edges = root.getFeatureEdges('b557b558'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02992', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b556'].id], root.datums[root.features['b641'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b556b641')

reg = Region(edges = root.getFeatureEdges('b556b641'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b641'].id], root.datums[root.features['b733'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b641b733')

reg = Region(edges = root.getFeatureEdges('b641b733'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04728', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b733'].id], root.datums[root.features['b836'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b733b836')

reg = Region(edges = root.getFeatureEdges('b733b836'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03823', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b837'].id], root.datums[root.features['b838'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b837b838')

reg = Region(edges = root.getFeatureEdges('b837b838'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01720', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b836'].id], root.datums[root.features['b948'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b836b948')

reg = Region(edges = root.getFeatureEdges('b836b948'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02950', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b948'].id], root.datums[root.features['b1064'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b948b1064')

reg = Region(edges = root.getFeatureEdges('b948b1064'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02106', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1064'].id], root.datums[root.features['b1192'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1064b1192')

reg = Region(edges = root.getFeatureEdges('b1064b1192'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01290', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1193'].id], root.datums[root.features['b1194'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1193b1194')

reg = Region(edges = root.getFeatureEdges('b1193b1194'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s00581', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b3'].id], root.datums[root.features['b9'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b3b9')

reg = Region(edges = root.getFeatureEdges('b3b9'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b9'].id], root.datums[root.features['b15'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b9b15')

reg = Region(edges = root.getFeatureEdges('b9b15'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s26372', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b15'].id], root.datums[root.features['b33'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b15b33')

reg = Region(edges = root.getFeatureEdges('b15b33'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s23220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b34'].id], root.datums[root.features['b35'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b34b35')

reg = Region(edges = root.getFeatureEdges('b34b35'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b35'].id], root.datums[root.features['b57'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b35b57')

reg = Region(edges = root.getFeatureEdges('b35b57'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b57'].id], root.datums[root.features['b73'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b57b73')

reg = Region(edges = root.getFeatureEdges('b57b73'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07332', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b73'].id], root.datums[root.features['b107'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b73b107')

reg = Region(edges = root.getFeatureEdges('b73b107'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04879', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b108'].id], root.datums[root.features['b109'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b108b109')

reg = Region(edges = root.getFeatureEdges('b108b109'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.77027,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02196', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b107'].id], root.datums[root.features['b145'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b107b145')

reg = Region(edges = root.getFeatureEdges('b107b145'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02811', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b33'].id], root.datums[root.features['b47'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b33b47')

reg = Region(edges = root.getFeatureEdges('b33b47'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s20749', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b47'].id], root.datums[root.features['b63'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b47b63')

reg = Region(edges = root.getFeatureEdges('b47b63'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s18669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b63'].id], root.datums[root.features['b79'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b63b79')

reg = Region(edges = root.getFeatureEdges('b63b79'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16850', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b80'].id], root.datums[root.features['b81'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b80b81')

reg = Region(edges = root.getFeatureEdges('b80b81'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07583', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b81'].id], root.datums[root.features['b149'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b81b149')

reg = Region(edges = root.getFeatureEdges('b81b149'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07583', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b149'].id], root.datums[root.features['b178'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b149b178')

reg = Region(edges = root.getFeatureEdges('b149b178'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04181', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b79'].id], root.datums[root.features['b133'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b79b133')

reg = Region(edges = root.getFeatureEdges('b79b133'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s15220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b133'].id], root.datums[root.features['b164'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b133b164')

reg = Region(edges = root.getFeatureEdges('b133b164'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s13734', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b164'].id], root.datums[root.features['b200'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b164b200')

reg = Region(edges = root.getFeatureEdges('b164b200'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12362', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b200'].id], root.datums[root.features['b258'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b200b258')

reg = Region(edges = root.getFeatureEdges('b200b258'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11083', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b259'].id], root.datums[root.features['b260'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b259b260')

reg = Region(edges = root.getFeatureEdges('b259b260'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9142,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04988', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b260'].id], root.datums[root.features['b377'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b260b377')

reg = Region(edges = root.getFeatureEdges('b260b377'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.9142,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04988', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b258'].id], root.datums[root.features['b330'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b258b330')

reg = Region(edges = root.getFeatureEdges('b258b330'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09883', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b330'].id], root.datums[root.features['b390'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b330b390')

reg = Region(edges = root.getFeatureEdges('b330b390'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s08750', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b390'].id], root.datums[root.features['b464'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b390b464')

reg = Region(edges = root.getFeatureEdges('b390b464'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07674', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b465'].id], root.datums[root.features['b466'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b465b466')

reg = Region(edges = root.getFeatureEdges('b465b466'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.5866,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03454', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b464'].id], root.datums[root.features['b559'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b464b559')

reg = Region(edges = root.getFeatureEdges('b464b559'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06649', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b559'].id], root.datums[root.features['b642'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b559b642')

reg = Region(edges = root.getFeatureEdges('b559b642'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b642'].id], root.datums[root.features['b734'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b642b734')

reg = Region(edges = root.getFeatureEdges('b642b734'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04728', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b735'].id], root.datums[root.features['b736'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b735b736')

reg = Region(edges = root.getFeatureEdges('b735b736'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.82398,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02127', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b734'].id], root.datums[root.features['b839'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b734b839')

reg = Region(edges = root.getFeatureEdges('b734b839'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03823', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b839'].id], root.datums[root.features['b949'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b839b949')

reg = Region(edges = root.getFeatureEdges('b839b949'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02950', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b949'].id], root.datums[root.features['b1065'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b949b1065')

reg = Region(edges = root.getFeatureEdges('b949b1065'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02106', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1066'].id], root.datums[root.features['b1067'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1066b1067')

reg = Region(edges = root.getFeatureEdges('b1066b1067'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.16304,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s00948', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1065'].id], root.datums[root.features['b1195'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1065b1195')

reg = Region(edges = root.getFeatureEdges('b1065b1195'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01290', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b4'].id], root.datums[root.features['b10'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b4b10')

reg = Region(edges = root.getFeatureEdges('b4b10'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b10'].id], root.datums[root.features['b16'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b10b16')

reg = Region(edges = root.getFeatureEdges('b10b16'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s26372', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b16'].id], root.datums[root.features['b36'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b16b36')

reg = Region(edges = root.getFeatureEdges('b16b36'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s23220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b37'].id], root.datums[root.features['b38'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b37b38')

reg = Region(edges = root.getFeatureEdges('b37b38'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.41884,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b38'].id], root.datums[root.features['b58'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b38b58')

reg = Region(edges = root.getFeatureEdges('b38b58'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.41884,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b58'].id], root.datums[root.features['b74'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b58b74')

reg = Region(edges = root.getFeatureEdges('b58b74'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.41884,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07332', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b74'].id], root.datums[root.features['b110'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b74b110')

reg = Region(edges = root.getFeatureEdges('b74b110'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.41884,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04879', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b111'].id], root.datums[root.features['b112'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b111b112')

reg = Region(edges = root.getFeatureEdges('b111b112'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.93073,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02196', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b110'].id], root.datums[root.features['b146'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b110b146')

reg = Region(edges = root.getFeatureEdges('b110b146'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.41884,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02811', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b36'].id], root.datums[root.features['b48'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b36b48')

reg = Region(edges = root.getFeatureEdges('b36b48'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s20749', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b48'].id], root.datums[root.features['b64'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b48b64')

reg = Region(edges = root.getFeatureEdges('b48b64'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s18669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b64'].id], root.datums[root.features['b82'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b64b82')

reg = Region(edges = root.getFeatureEdges('b64b82'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16850', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b83'].id], root.datums[root.features['b84'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b83b84')

reg = Region(edges = root.getFeatureEdges('b83b84'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.1137,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07583', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b84'].id], root.datums[root.features['b150'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b84b150')

reg = Region(edges = root.getFeatureEdges('b84b150'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.1137,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07583', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b150'].id], root.datums[root.features['b179'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b150b179')

reg = Region(edges = root.getFeatureEdges('b150b179'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,3.1137,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04181', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b82'].id], root.datums[root.features['b134'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b82b134')

reg = Region(edges = root.getFeatureEdges('b82b134'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s15220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b134'].id], root.datums[root.features['b165'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b134b165')

reg = Region(edges = root.getFeatureEdges('b134b165'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s13734', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b165'].id], root.datums[root.features['b201'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b165b201')

reg = Region(edges = root.getFeatureEdges('b165b201'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12362', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b202'].id], root.datums[root.features['b203'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b202b203')

reg = Region(edges = root.getFeatureEdges('b202b203'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.9563,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05563', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b203'].id], root.datums[root.features['b316'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b203b316')

reg = Region(edges = root.getFeatureEdges('b203b316'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.9563,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05563', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b201'].id], root.datums[root.features['b261'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b201b261')

reg = Region(edges = root.getFeatureEdges('b201b261'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11083', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b261'].id], root.datums[root.features['b331'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b261b331')

reg = Region(edges = root.getFeatureEdges('b261b331'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09883', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b331'].id], root.datums[root.features['b391'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b331b391')

reg = Region(edges = root.getFeatureEdges('b331b391'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s08750', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b391'].id], root.datums[root.features['b467'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b391b467')

reg = Region(edges = root.getFeatureEdges('b391b467'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07674', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b468'].id], root.datums[root.features['b469'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b468b469')

reg = Region(edges = root.getFeatureEdges('b468b469'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.7408,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03454', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b467'].id], root.datums[root.features['b560'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b467b560')

reg = Region(edges = root.getFeatureEdges('b467b560'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06649', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b560'].id], root.datums[root.features['b643'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b560b643')

reg = Region(edges = root.getFeatureEdges('b560b643'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b643'].id], root.datums[root.features['b737'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b643b737')

reg = Region(edges = root.getFeatureEdges('b643b737'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04728', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b737'].id], root.datums[root.features['b840'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b737b840')

reg = Region(edges = root.getFeatureEdges('b737b840'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03823', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b841'].id], root.datums[root.features['b842'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b841b842')

reg = Region(edges = root.getFeatureEdges('b841b842'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01720', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b840'].id], root.datums[root.features['b950'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b840b950')

reg = Region(edges = root.getFeatureEdges('b840b950'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02950', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b950'].id], root.datums[root.features['b1068'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b950b1068')

reg = Region(edges = root.getFeatureEdges('b950b1068'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02106', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1068'].id], root.datums[root.features['b1196'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1068b1196')

reg = Region(edges = root.getFeatureEdges('b1068b1196'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01290', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1197'].id], root.datums[root.features['b1198'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1197b1198')

reg = Region(edges = root.getFeatureEdges('b1197b1198'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.69021,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s00581', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b5'].id], root.datums[root.features['b11'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b5b11')

reg = Region(edges = root.getFeatureEdges('b5b11'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b11'].id], root.datums[root.features['b17'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b11b17')

reg = Region(edges = root.getFeatureEdges('b11b17'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s26372', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b17'].id], root.datums[root.features['b39'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b17b39')

reg = Region(edges = root.getFeatureEdges('b17b39'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s23220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b40'].id], root.datums[root.features['b41'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b40b41')

reg = Region(edges = root.getFeatureEdges('b40b41'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b41'].id], root.datums[root.features['b59'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b41b59')

reg = Region(edges = root.getFeatureEdges('b41b59'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b59'].id], root.datums[root.features['b75'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b59b75')

reg = Region(edges = root.getFeatureEdges('b59b75'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07332', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b75'].id], root.datums[root.features['b113'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b75b113')

reg = Region(edges = root.getFeatureEdges('b75b113'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04879', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b114'].id], root.datums[root.features['b115'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b114b115')

reg = Region(edges = root.getFeatureEdges('b114b115'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-0.77613,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02196', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b113'].id], root.datums[root.features['b147'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b113b147')

reg = Region(edges = root.getFeatureEdges('b113b147'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02811', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b39'].id], root.datums[root.features['b49'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b39b49')

reg = Region(edges = root.getFeatureEdges('b39b49'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s20749', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b49'].id], root.datums[root.features['b65'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b49b65')

reg = Region(edges = root.getFeatureEdges('b49b65'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s18669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b65'].id], root.datums[root.features['b85'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b65b85')

reg = Region(edges = root.getFeatureEdges('b65b85'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16850', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b86'].id], root.datums[root.features['b87'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b86b87')

reg = Region(edges = root.getFeatureEdges('b86b87'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.6513,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07583', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b87'].id], root.datums[root.features['b151'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b87b151')

reg = Region(edges = root.getFeatureEdges('b87b151'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.6513,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07583', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b151'].id], root.datums[root.features['b180'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b151b180')

reg = Region(edges = root.getFeatureEdges('b151b180'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,1.6513,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04181', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b85'].id], root.datums[root.features['b135'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b85b135')

reg = Region(edges = root.getFeatureEdges('b85b135'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s15220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b135'].id], root.datums[root.features['b166'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b135b166')

reg = Region(edges = root.getFeatureEdges('b135b166'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s13734', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b166'].id], root.datums[root.features['b204'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b166b204')

reg = Region(edges = root.getFeatureEdges('b166b204'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12362', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b204'].id], root.datums[root.features['b262'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b204b262')

reg = Region(edges = root.getFeatureEdges('b204b262'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11083', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b263'].id], root.datums[root.features['b264'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b263b264')

reg = Region(edges = root.getFeatureEdges('b263b264'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04988', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b264'].id], root.datums[root.features['b378'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b264b378')

reg = Region(edges = root.getFeatureEdges('b264b378'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04988', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b262'].id], root.datums[root.features['b332'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b262b332')

reg = Region(edges = root.getFeatureEdges('b262b332'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09883', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b332'].id], root.datums[root.features['b392'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b332b392')

reg = Region(edges = root.getFeatureEdges('b332b392'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s08750', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b392'].id], root.datums[root.features['b470'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b392b470')

reg = Region(edges = root.getFeatureEdges('b392b470'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07674', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b470'].id], root.datums[root.features['b561'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b470b561')

reg = Region(edges = root.getFeatureEdges('b470b561'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06649', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b562'].id], root.datums[root.features['b563'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b562b563')

reg = Region(edges = root.getFeatureEdges('b562b563'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02992', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b561'].id], root.datums[root.features['b644'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b561b644')

reg = Region(edges = root.getFeatureEdges('b561b644'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b644'].id], root.datums[root.features['b738'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b644b738')

reg = Region(edges = root.getFeatureEdges('b644b738'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04728', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b738'].id], root.datums[root.features['b843'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b738b843')

reg = Region(edges = root.getFeatureEdges('b738b843'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03823', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b843'].id], root.datums[root.features['b951'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b843b951')

reg = Region(edges = root.getFeatureEdges('b843b951'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02950', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b952'].id], root.datums[root.features['b953'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b952b953')

reg = Region(edges = root.getFeatureEdges('b952b953'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01327', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b951'].id], root.datums[root.features['b1069'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b951b1069')

reg = Region(edges = root.getFeatureEdges('b951b1069'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02106', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1069'].id], root.datums[root.features['b1199'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1069b1199')

reg = Region(edges = root.getFeatureEdges('b1069b1199'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.3764,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01290', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b6'].id], root.datums[root.features['b12'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b6b12')

reg = Region(edges = root.getFeatureEdges('b6b12'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s31149', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b12'].id], root.datums[root.features['b18'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b12b18')

reg = Region(edges = root.getFeatureEdges('b12b18'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s26372', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b18'].id], root.datums[root.features['b42'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b18b42')

reg = Region(edges = root.getFeatureEdges('b18b42'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s23220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b43'].id], root.datums[root.features['b44'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b43b44')

reg = Region(edges = root.getFeatureEdges('b43b44'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b44'].id], root.datums[root.features['b60'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b44b60')

reg = Region(edges = root.getFeatureEdges('b44b60'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s10449', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b60'].id], root.datums[root.features['b76'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b60b76')

reg = Region(edges = root.getFeatureEdges('b60b76'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07332', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b76'].id], root.datums[root.features['b116'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b76b116')

reg = Region(edges = root.getFeatureEdges('b76b116'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04879', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b117'].id], root.datums[root.features['b118'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b117b118')

reg = Region(edges = root.getFeatureEdges('b117b118'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,-1.0377,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02196', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b116'].id], root.datums[root.features['b148'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b116b148')

reg = Region(edges = root.getFeatureEdges('b116b148'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02811', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b42'].id], root.datums[root.features['b50'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b42b50')

reg = Region(edges = root.getFeatureEdges('b42b50'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s20749', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b50'].id], root.datums[root.features['b66'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b50b66')

reg = Region(edges = root.getFeatureEdges('b50b66'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s18669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b66'].id], root.datums[root.features['b88'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b66b88')

reg = Region(edges = root.getFeatureEdges('b66b88'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s16850', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b88'].id], root.datums[root.features['b136'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b88b136')

reg = Region(edges = root.getFeatureEdges('b88b136'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s15220', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b137'].id], root.datums[root.features['b138'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b137b138')

reg = Region(edges = root.getFeatureEdges('b137b138'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06849', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b138'].id], root.datums[root.features['b197'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b138b197')

reg = Region(edges = root.getFeatureEdges('b138b197'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06849', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b197'].id], root.datums[root.features['b255'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b197b255')

reg = Region(edges = root.getFeatureEdges('b197b255'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03358', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b136'].id], root.datums[root.features['b167'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b136b167')

reg = Region(edges = root.getFeatureEdges('b136b167'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s13734', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b167'].id], root.datums[root.features['b205'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b167b205')

reg = Region(edges = root.getFeatureEdges('b167b205'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s12362', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b205'].id], root.datums[root.features['b265'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b205b265')

reg = Region(edges = root.getFeatureEdges('b205b265'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s11083', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b265'].id], root.datums[root.features['b333'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b265b333')

reg = Region(edges = root.getFeatureEdges('b265b333'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s09883', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b334'].id], root.datums[root.features['b335'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b334b335')

reg = Region(edges = root.getFeatureEdges('b334b335'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04448', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b335'].id], root.datums[root.features['b462'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b335b462')

reg = Region(edges = root.getFeatureEdges('b335b462'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04448', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b333'].id], root.datums[root.features['b393'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b333b393')

reg = Region(edges = root.getFeatureEdges('b333b393'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s08750', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b393'].id], root.datums[root.features['b471'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b393b471')

reg = Region(edges = root.getFeatureEdges('b393b471'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s07674', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b471'].id], root.datums[root.features['b564'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b471b564')

reg = Region(edges = root.getFeatureEdges('b471b564'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s06649', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b565'].id], root.datums[root.features['b566'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b565b566')

reg = Region(edges = root.getFeatureEdges('b565b566'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02992', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b564'].id], root.datums[root.features['b645'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b564b645')

reg = Region(edges = root.getFeatureEdges('b564b645'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s05669', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b645'].id], root.datums[root.features['b739'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b645b739')

reg = Region(edges = root.getFeatureEdges('b645b739'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s04728', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b739'].id], root.datums[root.features['b844'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b739b844')

reg = Region(edges = root.getFeatureEdges('b739b844'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s03823', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b845'].id], root.datums[root.features['b846'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b845b846')

reg = Region(edges = root.getFeatureEdges('b845b846'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01720', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b844'].id], root.datums[root.features['b954'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b844b954')

reg = Region(edges = root.getFeatureEdges('b844b954'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02950', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b954'].id], root.datums[root.features['b1070'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b954b1070')

reg = Region(edges = root.getFeatureEdges('b954b1070'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s02106', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1070'].id], root.datums[root.features['b1200'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1070b1200')

reg = Region(edges = root.getFeatureEdges('b1070b1200'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1,0.32492,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s01290', thicknessAssignment=FROM_SECTION)

root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1201'].id], root.datums[root.features['b1202'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1201b1202')

reg = Region(edges = root.getFeatureEdges('b1201b1202'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0,1,0), region=reg)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='S-0s00581', thicknessAssignment=FROM_SECTION)

# =========================================

