# Script automatically generated on 06-Jun-2018 at 21:22 by RootGen
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
modelname = 'testmodel';
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
	"init_diam" : 0.31144,
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
mdb.models[modelname].HomogeneousSolidSection(material='RootMaterial', name='RootSection', thickness=None)
# =========================================

# Root segments part creation
#    - RS-1s234 : root segment with diameter 1.234 m, if not tapered
#    - RS-1s234-1s123 : root segment with initial diameter 1.234 m
# and final diameter 1.123 m, if tapered
mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00208/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00208/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00208-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00208-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00222/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00222/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00222-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00222-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00494/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00494/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00494-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00494-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00494/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00494/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00494-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00494-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00494/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00494/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00494-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00494-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00578/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00578/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00578-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00578-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00946/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00946/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00946-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00946-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01285/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01285/2, 0.0), point2=(0.00494/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00494/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01285-0s00494', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01285-0s00494'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01285/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01285/2, 0.0), point2=(0.00494/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00494/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01285-0s00494', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01285-0s00494'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01285/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01285/2, 0.0), point2=(0.00494/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00494/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01285-0s00494', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01285-0s00494'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01325/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01325/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01325-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01325-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01401/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01401/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01401-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01401-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01406/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01406/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01406-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01406-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01535/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01535/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01535-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01535-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01627/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01627/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01627-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01627-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01718/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01718/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01718-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01718-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02070/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02070/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02070-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02070-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02102/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02102/2, 0.0), point2=(0.01285/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01285/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02102-0s01285', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02102-0s01285'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02102/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02102/2, 0.0), point2=(0.01285/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01285/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02102-0s01285', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02102-0s01285'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02549/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02549/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02549-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02549-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02549/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02549/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02549-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02549-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02945/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02945/2, 0.0), point2=(0.02102/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02102/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02945-0s02102', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02945-0s02102'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02945/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02945/2, 0.0), point2=(0.02102/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02102/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02945-0s02102', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02945-0s02102'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02990/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02990/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02990-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02990-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.03615/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03615/2, 0.0), point2=(0.01535/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01535/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s03615-0s01535', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s03615-0s01535'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.03818/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03818/2, 0.0), point2=(0.02945/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02945/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s03818-0s02945', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s03818-0s02945'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.03818/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03818/2, 0.0), point2=(0.02945/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02945/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s03818-0s02945', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s03818-0s02945'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.03935/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03935/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s03935-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s03935-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.04445/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04445/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s04445-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s04445-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.04558/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04558/2, 0.0), point2=(0.01406/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01406/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s04558-0s01406', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s04558-0s01406'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.04723/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04723/2, 0.0), point2=(0.03818/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03818/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s04723-0s03818', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s04723-0s03818'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.04723/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04723/2, 0.0), point2=(0.03818/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03818/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s04723-0s03818', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s04723-0s03818'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.04985/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04985/2, 0.0), point2=(0.00208/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00208/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s04985-0s00208', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s04985-0s00208'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.05664/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05664/2, 0.0), point2=(0.04723/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04723/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s05664-0s04723', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s05664-0s04723'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.05664/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05664/2, 0.0), point2=(0.04723/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04723/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s05664-0s04723', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s05664-0s04723'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.06086/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06086/2, 0.0), point2=(0.03615/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03615/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s06086-0s03615', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s06086-0s03615'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.06178/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06178/2, 0.0), point2=(0.01401/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01401/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s06178-0s01401', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s06178-0s01401'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.06645/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06645/2, 0.0), point2=(0.05664/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05664/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s06645-0s05664', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s06645-0s05664'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.06645/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06645/2, 0.0), point2=(0.05664/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05664/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s06645-0s05664', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s06645-0s05664'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.06847/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06847/2, 0.0), point2=(0.02070/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02070/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s06847-0s02070', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s06847-0s02070'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.07670/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.07670/2, 0.0), point2=(0.06645/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06645/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s07670-0s06645', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s07670-0s06645'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.08745/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.08745/2, 0.0), point2=(0.07670/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.07670/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s08745-0s07670', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s08745-0s07670'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.09238/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.09238/2, 0.0), point2=(0.06086/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.06086/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s09238-0s06086', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s09238-0s06086'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.09335/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.09335/2, 0.0), point2=(0.04558/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04558/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s09335-0s04558', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s09335-0s04558'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.09879/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.09879/2, 0.0), point2=(0.08745/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.08745/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s09879-0s08745', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s09879-0s08745'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.11079/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.11079/2, 0.0), point2=(0.09879/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.09879/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s11079-0s09879', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s11079-0s09879'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.12357/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.12357/2, 0.0), point2=(0.11079/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.11079/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s12357-0s11079', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s12357-0s11079'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.13729/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.13729/2, 0.0), point2=(0.12357/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.12357/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s13729-0s12357', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s13729-0s12357'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.14015/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.14015/2, 0.0), point2=(0.09238/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.09238/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s14015-0s09238', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s14015-0s09238'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.15215/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.15215/2, 0.0), point2=(0.13729/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.13729/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s15215-0s13729', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s15215-0s13729'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.16846/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.16846/2, 0.0), point2=(0.15215/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.15215/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s16846-0s15215', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s16846-0s15215'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.18665/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.18665/2, 0.0), point2=(0.16846/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.16846/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s18665-0s16846', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s18665-0s16846'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.20744/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.20744/2, 0.0), point2=(0.18665/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.18665/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s20744-0s18665', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s20744-0s18665'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.23215/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.23215/2, 0.0), point2=(0.20744/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.20744/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s23215-0s20744', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s23215-0s20744'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.26367/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.26367/2, 0.0), point2=(0.23215/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.23215/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s26367-0s23215', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s26367-0s23215'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.31144/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.31144/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s31144-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s31144-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.31144/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.31144/2, 0.0), point2=(0.26367/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.26367/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s31144-0s26367', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s31144-0s26367'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.31144/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.31144/2, 0.0), point2=(0.31144/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.31144/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[3], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[5], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[6])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s31144-0s31144', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s31144-0s31144'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']

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

# Creation of the coordinate system of the instance module
mdb.models[modelname].rootAssembly.DatumCsysByDefault(CARTESIAN)
# =========================================

# Root segments instancing and positioning
mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-001', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-001', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-001', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-001', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-001', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-007', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-007', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-007', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-007', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-007', ), vector=(0,0,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-013', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-013', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-013', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-013', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-013', ), vector=(0,0,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-019', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-019', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-019', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-019', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-019', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-035', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-035', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-035', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-035', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-035', ), vector=(0,0,-0.4))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-051', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-051', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-051', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-051', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-051', ), vector=(0,0,-0.5))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-067', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-067', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-067', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-067', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-067', ), vector=(0,0,-0.6))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-096', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-096', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-096', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-096', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-096', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-132', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-132', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-132', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-132', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-132', ), vector=(0,0,-0.8))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-168', part=mdb.models[modelname].parts['RS-0s31144-0s31144'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-168', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-168', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-168', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-168', ), vector=(0,0,-0.9))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-213', part=mdb.models[modelname].parts['RS-0s31144-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-213', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-213', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-213', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-213', ), vector=(0,0,-1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-020', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-020', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-020', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.36771,0.92994,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-020', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-020', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-041', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-041', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-041', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.36771,0.92994,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-041', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-041', ), vector=(0.092994,0.036771,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-057', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-057', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-057', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.36771,0.92994,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-057', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-057', ), vector=(0.18599,0.073541,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-076', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-076', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-076', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.36771,0.92994,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-076', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-076', ), vector=(0.27898,0.11031,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-109', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-109', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-109', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.36771,0.92994,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-109', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-109', ), vector=(0.37198,0.14708,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-077', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-077', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-077', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-077', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-077', ), vector=(0.27898,0.11031,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-021', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-021', ))
mdb.models[modelname].rootAssembly.rotate(angle=-176.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-021', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.99805,-0.062342,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-021', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-021', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-042', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-042', ))
mdb.models[modelname].rootAssembly.rotate(angle=-176.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-042', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.99805,-0.062342,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-042', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-042', ), vector=(-0.0062342,0.099805,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-058', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-058', ))
mdb.models[modelname].rootAssembly.rotate(angle=-176.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-058', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.99805,-0.062342,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-058', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-058', ), vector=(-0.012468,0.19961,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-078', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-078', ))
mdb.models[modelname].rootAssembly.rotate(angle=-176.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-078', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.99805,-0.062342,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-078', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-078', ), vector=(-0.018702,0.29942,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-110', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-110', ))
mdb.models[modelname].rootAssembly.rotate(angle=-176.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-110', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.99805,-0.062342,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-110', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-110', ), vector=(-0.024937,0.39922,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-079', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-079', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-079', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-079', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-079', ), vector=(-0.018702,0.29942,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-022', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-022', ))
mdb.models[modelname].rootAssembly.rotate(angle=-104.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-022', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.24913,-0.96847,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-022', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-022', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-043', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-043', ))
mdb.models[modelname].rootAssembly.rotate(angle=-104.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-043', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.24913,-0.96847,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-043', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-043', ), vector=(-0.096847,0.024913,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-059', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-059', ))
mdb.models[modelname].rootAssembly.rotate(angle=-104.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-059', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.24913,-0.96847,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-059', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-059', ), vector=(-0.19369,0.049825,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-080', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-080', ))
mdb.models[modelname].rootAssembly.rotate(angle=-104.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-080', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.24913,-0.96847,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-080', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-080', ), vector=(-0.29054,0.074738,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-111', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-111', ))
mdb.models[modelname].rootAssembly.rotate(angle=-104.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-111', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.24913,-0.96847,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-111', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-111', ), vector=(-0.38739,0.09965,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-081', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-081', ))
mdb.models[modelname].rootAssembly.rotate(angle=-63.5131, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-081', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.44599,-0.89504,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-081', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-081', ), vector=(-0.29054,0.074738,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-023', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-023', ))
mdb.models[modelname].rootAssembly.rotate(angle=-32.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-023', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.84409,-0.53621,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-023', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-023', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-044', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-044', ))
mdb.models[modelname].rootAssembly.rotate(angle=-32.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-044', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.84409,-0.53621,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-044', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-044', ), vector=(-0.053621,-0.084409,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-060', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-060', ))
mdb.models[modelname].rootAssembly.rotate(angle=-32.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-060', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.84409,-0.53621,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-060', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-060', ), vector=(-0.10724,-0.16882,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-082', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-082', ))
mdb.models[modelname].rootAssembly.rotate(angle=-32.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-082', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.84409,-0.53621,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-082', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-082', ), vector=(-0.16086,-0.25323,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-112', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-112', ))
mdb.models[modelname].rootAssembly.rotate(angle=-32.4258, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-112', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.84409,-0.53621,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-112', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-112', ), vector=(-0.21448,-0.33763,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-083', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-083', ))
mdb.models[modelname].rootAssembly.rotate(angle=5.0837, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-083', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99607,0.088611,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-083', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-083', ), vector=(-0.16086,-0.25323,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-024', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-024', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-024', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.7708,0.63708,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-024', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-024', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-045', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-045', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-045', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.7708,0.63708,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-045', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-045', ), vector=(0.063708,-0.07708,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-061', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-061', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-061', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.7708,0.63708,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-061', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-061', ), vector=(0.12742,-0.15416,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-084', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-084', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-084', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.7708,0.63708,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-084', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-084', ), vector=(0.19112,-0.23124,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-113', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-113', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.5742, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-113', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.7708,0.63708,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-113', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-113', ), vector=(0.25483,-0.30832,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-085', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-085', ))
mdb.models[modelname].rootAssembly.rotate(angle=107.1004, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-085', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.29405,0.95579,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-085', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-085', ), vector=(0.19112,-0.23124,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-097', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-097', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-097', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.21737,0.97609,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-097', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-097', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-161', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-161', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-161', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.21737,0.97609,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-161', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-161', ), vector=(0.097609,-0.021737,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-206', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-206', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-206', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.21737,0.97609,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-206', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-206', ), vector=(0.19522,-0.043475,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-249', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-249', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-249', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.21737,0.97609,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-249', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-249', ), vector=(0.29283,-0.065212,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-302', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-302', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-302', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.21737,0.97609,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-302', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-302', ), vector=(0.39044,-0.086949,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-250', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-250', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-250', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-250', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-250', ), vector=(0.29283,-0.065212,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-098', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-098', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-098', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.86114,0.50836,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-098', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-098', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-162', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-162', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-162', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.86114,0.50836,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-162', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-162', ), vector=(0.050836,0.086114,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-207', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-207', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-207', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.86114,0.50836,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-207', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-207', ), vector=(0.10167,0.17223,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-251', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-251', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-251', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.86114,0.50836,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-251', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-251', ), vector=(0.15251,0.25834,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-303', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-303', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-303', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.86114,0.50836,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-303', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-303', ), vector=(0.20334,0.34446,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-252', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-252', ))
mdb.models[modelname].rootAssembly.rotate(angle=119.3741, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-252', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.49051,0.87144,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-252', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-252', ), vector=(0.15251,0.25834,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-099', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-099', ))
mdb.models[modelname].rootAssembly.rotate(angle=-138.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-099', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.74959,-0.6619,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-099', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-099', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-163', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-163', ))
mdb.models[modelname].rootAssembly.rotate(angle=-138.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-163', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.74959,-0.6619,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-163', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-163', ), vector=(-0.06619,0.074959,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-208', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-208', ))
mdb.models[modelname].rootAssembly.rotate(angle=-138.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-208', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.74959,-0.6619,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-208', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-208', ), vector=(-0.13238,0.14992,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-253', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-253', ))
mdb.models[modelname].rootAssembly.rotate(angle=-138.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-253', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.74959,-0.6619,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-253', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-253', ), vector=(-0.19857,0.22488,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-304', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-304', ))
mdb.models[modelname].rootAssembly.rotate(angle=-138.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-304', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.74959,-0.6619,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-304', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-304', ), vector=(-0.26476,0.29984,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-254', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-254', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-254', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-254', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-254', ), vector=(-0.19857,0.22488,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-100', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-100', ))
mdb.models[modelname].rootAssembly.rotate(angle=-66.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-100', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.39787,-0.91744,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-100', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-100', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-164', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-164', ))
mdb.models[modelname].rootAssembly.rotate(angle=-66.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-164', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.39787,-0.91744,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-164', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-164', ), vector=(-0.091744,-0.039787,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-209', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-209', ))
mdb.models[modelname].rootAssembly.rotate(angle=-66.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-209', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.39787,-0.91744,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-209', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-209', ), vector=(-0.18349,-0.079574,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-255', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-255', ))
mdb.models[modelname].rootAssembly.rotate(angle=-66.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-255', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.39787,-0.91744,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-255', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-255', ), vector=(-0.27523,-0.11936,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-305', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-305', ))
mdb.models[modelname].rootAssembly.rotate(angle=-66.5548, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-305', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.39787,-0.91744,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-305', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-305', ), vector=(-0.36698,-0.15915,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-256', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-256', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.9295, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-256', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.76683,0.64184,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-256', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-256', ), vector=(-0.27523,-0.11936,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-101', part=mdb.models[modelname].parts['RS-0s14015-0s09238'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-101', ))
mdb.models[modelname].rootAssembly.rotate(angle=5.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-101', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99549,0.094894,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-101', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-101', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-165', part=mdb.models[modelname].parts['RS-0s09238-0s06086'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-165', ))
mdb.models[modelname].rootAssembly.rotate(angle=5.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-165', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99549,0.094894,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-165', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-165', ), vector=(0.0094894,-0.099549,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-210', part=mdb.models[modelname].parts['RS-0s06086-0s03615'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-210', ))
mdb.models[modelname].rootAssembly.rotate(angle=5.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-210', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99549,0.094894,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-210', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-210', ), vector=(0.018979,-0.1991,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-257', part=mdb.models[modelname].parts['RS-0s03615-0s01535'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-257', ))
mdb.models[modelname].rootAssembly.rotate(angle=5.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-257', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99549,0.094894,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-257', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-257', ), vector=(0.028468,-0.29865,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-306', part=mdb.models[modelname].parts['RS-0s01535-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-306', ))
mdb.models[modelname].rootAssembly.rotate(angle=5.4452, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-306', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99549,0.094894,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-306', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-306', ), vector=(0.037958,-0.39819,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-258', part=mdb.models[modelname].parts['RS-0s01627-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-258', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-258', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-258', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-258', ), vector=(0.028468,-0.29865,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-002', part=mdb.models[modelname].parts['RS-0s31144-0s26367'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-002', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-002', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-002', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-002', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-008', part=mdb.models[modelname].parts['RS-0s26367-0s23215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-008', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-008', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-008', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-008', ), vector=(0.1,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-014', part=mdb.models[modelname].parts['RS-0s23215-0s20744'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-014', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-014', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-014', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-014', ), vector=(0.2,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-025', part=mdb.models[modelname].parts['RS-0s20744-0s18665'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-025', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-025', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-025', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-025', ), vector=(0.3,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-036', part=mdb.models[modelname].parts['RS-0s18665-0s16846'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-036', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-036', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-036', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-036', ), vector=(0.4,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-052', part=mdb.models[modelname].parts['RS-0s16846-0s15215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-052', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-052', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-052', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-052', ), vector=(0.5,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-068', part=mdb.models[modelname].parts['RS-0s15215-0s13729'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-068', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-068', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-068', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-068', ), vector=(0.6,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-102', part=mdb.models[modelname].parts['RS-0s13729-0s12357'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-102', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-102', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-102', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-102', ), vector=(0.7,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-133', part=mdb.models[modelname].parts['RS-0s12357-0s11079'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-133', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-133', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-133', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-133', ), vector=(0.8,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-169', part=mdb.models[modelname].parts['RS-0s11079-0s09879'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-169', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-169', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-169', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-169', ), vector=(0.9,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-214', part=mdb.models[modelname].parts['RS-0s09879-0s08745'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-214', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-214', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-214', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-214', ), vector=(1,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-272', part=mdb.models[modelname].parts['RS-0s08745-0s07670'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-272', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-272', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-272', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-272', ), vector=(1.1,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-332', part=mdb.models[modelname].parts['RS-0s07670-0s06645'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-332', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-332', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-332', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-332', ), vector=(1.2,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-400', part=mdb.models[modelname].parts['RS-0s06645-0s05664'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-400', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-400', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-400', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-400', ), vector=(1.3,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-480', part=mdb.models[modelname].parts['RS-0s05664-0s04723'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-480', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-480', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-480', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-480', ), vector=(1.4,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-555', part=mdb.models[modelname].parts['RS-0s04723-0s03818'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-555', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-555', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-555', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-555', ), vector=(1.5,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-637', part=mdb.models[modelname].parts['RS-0s03818-0s02945'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-637', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-637', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-637', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-637', ), vector=(1.6,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-727', part=mdb.models[modelname].parts['RS-0s02945-0s02102'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-727', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-727', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-727', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-727', ), vector=(1.7,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-824', part=mdb.models[modelname].parts['RS-0s02102-0s01285'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-824', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-824', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-824', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-824', ), vector=(1.8,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-929', part=mdb.models[modelname].parts['RS-0s01285-0s00494'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-929', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-929', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-929', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-929', ), vector=(1.9,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1043', part=mdb.models[modelname].parts['RS-0s00494-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1043', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1043', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1043', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1043', ), vector=(2,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-026', part=mdb.models[modelname].parts['RS-0s09335-0s04558'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-026', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-026', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-026', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-026', ), vector=(0.3,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-046', part=mdb.models[modelname].parts['RS-0s04558-0s01406'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-046', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-046', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-046', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-046', ), vector=(0.3,0,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-062', part=mdb.models[modelname].parts['RS-0s01406-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-062', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-062', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-062', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-062', ), vector=(0.3,0,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-103', part=mdb.models[modelname].parts['RS-0s06178-0s01401'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-103', ))
mdb.models[modelname].rootAssembly.rotate(angle=-152.0158, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-103', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.88308,-0.46923,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-103', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-103', ), vector=(0.7,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-166', part=mdb.models[modelname].parts['RS-0s01401-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-166', ))
mdb.models[modelname].rootAssembly.rotate(angle=-152.0158, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-166', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.88308,-0.46923,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-166', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-166', ), vector=(0.65308,0.088308,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-273', part=mdb.models[modelname].parts['RS-0s03935-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-273', ))
mdb.models[modelname].rootAssembly.rotate(angle=13.0064, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-273', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.97434,0.22506,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-273', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-273', ), vector=(1.1,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-481', part=mdb.models[modelname].parts['RS-0s02549-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-481', ))
mdb.models[modelname].rootAssembly.rotate(angle=-5.0071, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-481', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99618,-0.087278,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-481', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-481', ), vector=(1.4,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-728', part=mdb.models[modelname].parts['RS-0s01325-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-728', ))
mdb.models[modelname].rootAssembly.rotate(angle=-118.7736, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-728', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.48135,-0.87653,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-728', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-728', ), vector=(1.7,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1044', part=mdb.models[modelname].parts['RS-0s00222-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1044', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1044', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1044', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1044', ), vector=(2,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-003', part=mdb.models[modelname].parts['RS-0s31144-0s26367'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-003', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-003', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-003', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-003', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-009', part=mdb.models[modelname].parts['RS-0s26367-0s23215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-009', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-009', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-009', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-009', ), vector=(0.030902,0.095106,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-015', part=mdb.models[modelname].parts['RS-0s23215-0s20744'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-015', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-015', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-015', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-015', ), vector=(0.061803,0.19021,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-027', part=mdb.models[modelname].parts['RS-0s20744-0s18665'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-027', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-027', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-027', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-027', ), vector=(0.092705,0.28532,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-037', part=mdb.models[modelname].parts['RS-0s18665-0s16846'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-037', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-037', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-037', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-037', ), vector=(0.12361,0.38042,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-053', part=mdb.models[modelname].parts['RS-0s16846-0s15215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-053', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-053', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-053', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-053', ), vector=(0.15451,0.47553,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-069', part=mdb.models[modelname].parts['RS-0s15215-0s13729'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-069', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-069', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-069', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-069', ), vector=(0.18541,0.57063,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-104', part=mdb.models[modelname].parts['RS-0s13729-0s12357'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-104', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-104', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-104', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-104', ), vector=(0.21631,0.66574,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-134', part=mdb.models[modelname].parts['RS-0s12357-0s11079'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-134', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-134', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-134', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-134', ), vector=(0.24721,0.76085,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-170', part=mdb.models[modelname].parts['RS-0s11079-0s09879'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-170', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-170', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-170', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-170', ), vector=(0.27812,0.85595,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-215', part=mdb.models[modelname].parts['RS-0s09879-0s08745'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-215', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-215', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-215', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-215', ), vector=(0.30902,0.95106,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-274', part=mdb.models[modelname].parts['RS-0s08745-0s07670'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-274', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-274', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-274', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-274', ), vector=(0.33992,1.0462,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-333', part=mdb.models[modelname].parts['RS-0s07670-0s06645'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-333', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-333', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-333', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-333', ), vector=(0.37082,1.1413,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-401', part=mdb.models[modelname].parts['RS-0s06645-0s05664'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-401', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-401', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-401', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-401', ), vector=(0.40172,1.2364,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-482', part=mdb.models[modelname].parts['RS-0s05664-0s04723'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-482', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-482', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-482', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-482', ), vector=(0.43262,1.3315,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-556', part=mdb.models[modelname].parts['RS-0s04723-0s03818'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-556', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-556', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-556', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-556', ), vector=(0.46353,1.4266,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-638', part=mdb.models[modelname].parts['RS-0s03818-0s02945'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-638', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-638', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-638', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-638', ), vector=(0.49443,1.5217,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-729', part=mdb.models[modelname].parts['RS-0s02945-0s02102'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-729', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-729', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-729', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-729', ), vector=(0.52533,1.6168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-825', part=mdb.models[modelname].parts['RS-0s02102-0s01285'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-825', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-825', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-825', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-825', ), vector=(0.55623,1.7119,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-930', part=mdb.models[modelname].parts['RS-0s01285-0s00494'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-930', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-930', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-930', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-930', ), vector=(0.58713,1.807,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1045', part=mdb.models[modelname].parts['RS-0s00494-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1045', ))
mdb.models[modelname].rootAssembly.rotate(angle=162, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1045', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1045', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1045', ), vector=(0.61803,1.9021,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-028', part=mdb.models[modelname].parts['RS-0s09335-0s04558'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-028', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-028', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-028', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-028', ), vector=(0.092705,0.28532,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-047', part=mdb.models[modelname].parts['RS-0s04558-0s01406'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-047', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-047', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-047', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-047', ), vector=(0.092705,0.28532,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-063', part=mdb.models[modelname].parts['RS-0s01406-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-063', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-063', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-063', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-063', ), vector=(0.092705,0.28532,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-070', part=mdb.models[modelname].parts['RS-0s06847-0s02070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-070', ))
mdb.models[modelname].rootAssembly.rotate(angle=-52.4094, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-070', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.61002,-0.79239,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-070', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-070', ), vector=(0.18541,0.57063,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-119', part=mdb.models[modelname].parts['RS-0s02070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-119', ))
mdb.models[modelname].rootAssembly.rotate(angle=-52.4094, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-119', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.61002,-0.79239,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-119', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-119', ), vector=(0.10617,0.50963,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-216', part=mdb.models[modelname].parts['RS-0s04445-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-216', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-216', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-216', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-216', ), vector=(0.30902,0.95106,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-402', part=mdb.models[modelname].parts['RS-0s02990-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-402', ))
mdb.models[modelname].rootAssembly.rotate(angle=-73.6736, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-402', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.28111,-0.95968,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-402', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-402', ), vector=(0.40172,1.2364,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-639', part=mdb.models[modelname].parts['RS-0s01718-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-639', ))
mdb.models[modelname].rootAssembly.rotate(angle=39.1772, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-639', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.7752,0.63172,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-639', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-639', ), vector=(0.49443,1.5217,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-931', part=mdb.models[modelname].parts['RS-0s00578-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-931', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-931', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-931', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-931', ), vector=(0.58713,1.807,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-004', part=mdb.models[modelname].parts['RS-0s31144-0s26367'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-004', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-004', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-004', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-004', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-010', part=mdb.models[modelname].parts['RS-0s26367-0s23215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-010', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-010', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-010', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-010', ), vector=(-0.080902,0.058779,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-016', part=mdb.models[modelname].parts['RS-0s23215-0s20744'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-016', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-016', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-016', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-016', ), vector=(-0.1618,0.11756,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-029', part=mdb.models[modelname].parts['RS-0s20744-0s18665'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-029', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-029', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-029', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-029', ), vector=(-0.24271,0.17634,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-038', part=mdb.models[modelname].parts['RS-0s18665-0s16846'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-038', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-038', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-038', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-038', ), vector=(-0.32361,0.23511,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-054', part=mdb.models[modelname].parts['RS-0s16846-0s15215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-054', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-054', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-054', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-054', ), vector=(-0.40451,0.29389,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-071', part=mdb.models[modelname].parts['RS-0s15215-0s13729'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-071', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-071', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-071', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-071', ), vector=(-0.48541,0.35267,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-105', part=mdb.models[modelname].parts['RS-0s13729-0s12357'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-105', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-105', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-105', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-105', ), vector=(-0.56631,0.41145,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-135', part=mdb.models[modelname].parts['RS-0s12357-0s11079'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-135', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-135', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-135', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-135', ), vector=(-0.64721,0.47023,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-171', part=mdb.models[modelname].parts['RS-0s11079-0s09879'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-171', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-171', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-171', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-171', ), vector=(-0.72812,0.52901,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-217', part=mdb.models[modelname].parts['RS-0s09879-0s08745'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-217', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-217', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-217', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-217', ), vector=(-0.80902,0.58779,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-275', part=mdb.models[modelname].parts['RS-0s08745-0s07670'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-275', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-275', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-275', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-275', ), vector=(-0.88992,0.64656,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-334', part=mdb.models[modelname].parts['RS-0s07670-0s06645'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-334', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-334', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-334', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-334', ), vector=(-0.97082,0.70534,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-403', part=mdb.models[modelname].parts['RS-0s06645-0s05664'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-403', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-403', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-403', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-403', ), vector=(-1.0517,0.76412,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-483', part=mdb.models[modelname].parts['RS-0s05664-0s04723'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-483', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-483', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-483', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-483', ), vector=(-1.1326,0.8229,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-557', part=mdb.models[modelname].parts['RS-0s04723-0s03818'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-557', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-557', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-557', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-557', ), vector=(-1.2135,0.88168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-640', part=mdb.models[modelname].parts['RS-0s03818-0s02945'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-640', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-640', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-640', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-640', ), vector=(-1.2944,0.94046,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-730', part=mdb.models[modelname].parts['RS-0s02945-0s02102'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-730', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-730', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-730', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-730', ), vector=(-1.3753,0.99923,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-826', part=mdb.models[modelname].parts['RS-0s02102-0s01285'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-826', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-826', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-826', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-826', ), vector=(-1.4562,1.058,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-932', part=mdb.models[modelname].parts['RS-0s01285-0s00494'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-932', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-932', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-932', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-932', ), vector=(-1.5371,1.1168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1046', part=mdb.models[modelname].parts['RS-0s00494-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1046', ))
mdb.models[modelname].rootAssembly.rotate(angle=-126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1046', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1046', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1046', ), vector=(-1.618,1.1756,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-030', part=mdb.models[modelname].parts['RS-0s09335-0s04558'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-030', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-030', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-030', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-030', ), vector=(-0.24271,0.17634,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-048', part=mdb.models[modelname].parts['RS-0s04558-0s01406'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-048', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-048', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-048', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-048', ), vector=(-0.24271,0.17634,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-064', part=mdb.models[modelname].parts['RS-0s01406-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-064', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-064', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-064', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-064', ), vector=(-0.24271,0.17634,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-072', part=mdb.models[modelname].parts['RS-0s06847-0s02070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-072', ))
mdb.models[modelname].rootAssembly.rotate(angle=78.2814, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-072', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.20311,0.97916,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-072', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-072', ), vector=(-0.48541,0.35267,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-120', part=mdb.models[modelname].parts['RS-0s02070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-120', ))
mdb.models[modelname].rootAssembly.rotate(angle=78.2814, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-120', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.20311,0.97916,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-120', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-120', ), vector=(-0.38749,0.33236,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-172', part=mdb.models[modelname].parts['RS-0s04985-0s00208'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-172', ))
mdb.models[modelname].rootAssembly.rotate(angle=-106.0148, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-172', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.27588,-0.96119,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-172', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-172', ), vector=(-0.72812,0.52901,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-263', part=mdb.models[modelname].parts['RS-0s00208-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-263', ))
mdb.models[modelname].rootAssembly.rotate(angle=-106.0148, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-263', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.27588,-0.96119,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-263', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-263', ), vector=(-0.82423,0.5566,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-404', part=mdb.models[modelname].parts['RS-0s02990-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-404', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-404', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-404', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-404', ), vector=(-1.0517,0.76412,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-731', part=mdb.models[modelname].parts['RS-0s01325-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-731', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-731', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-731', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-731', ), vector=(-1.3753,0.99923,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1047', part=mdb.models[modelname].parts['RS-0s00222-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1047', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1047', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1047', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1047', ), vector=(-1.618,1.1756,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-005', part=mdb.models[modelname].parts['RS-0s31144-0s26367'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-005', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-005', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-005', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-005', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-011', part=mdb.models[modelname].parts['RS-0s26367-0s23215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-011', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-011', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-011', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-011', ), vector=(-0.080902,-0.058779,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-017', part=mdb.models[modelname].parts['RS-0s23215-0s20744'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-017', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-017', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-017', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-017', ), vector=(-0.1618,-0.11756,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-031', part=mdb.models[modelname].parts['RS-0s20744-0s18665'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-031', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-031', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-031', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-031', ), vector=(-0.24271,-0.17634,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-039', part=mdb.models[modelname].parts['RS-0s18665-0s16846'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-039', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-039', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-039', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-039', ), vector=(-0.32361,-0.23511,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-055', part=mdb.models[modelname].parts['RS-0s16846-0s15215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-055', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-055', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-055', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-055', ), vector=(-0.40451,-0.29389,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-073', part=mdb.models[modelname].parts['RS-0s15215-0s13729'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-073', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-073', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-073', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-073', ), vector=(-0.48541,-0.35267,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-106', part=mdb.models[modelname].parts['RS-0s13729-0s12357'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-106', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-106', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-106', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-106', ), vector=(-0.56631,-0.41145,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-136', part=mdb.models[modelname].parts['RS-0s12357-0s11079'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-136', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-136', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-136', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-136', ), vector=(-0.64721,-0.47023,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-173', part=mdb.models[modelname].parts['RS-0s11079-0s09879'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-173', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-173', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-173', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-173', ), vector=(-0.72812,-0.52901,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-218', part=mdb.models[modelname].parts['RS-0s09879-0s08745'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-218', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-218', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-218', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-218', ), vector=(-0.80902,-0.58779,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-276', part=mdb.models[modelname].parts['RS-0s08745-0s07670'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-276', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-276', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-276', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-276', ), vector=(-0.88992,-0.64656,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-335', part=mdb.models[modelname].parts['RS-0s07670-0s06645'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-335', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-335', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-335', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-335', ), vector=(-0.97082,-0.70534,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-405', part=mdb.models[modelname].parts['RS-0s06645-0s05664'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-405', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-405', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-405', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-405', ), vector=(-1.0517,-0.76412,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-484', part=mdb.models[modelname].parts['RS-0s05664-0s04723'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-484', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-484', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-484', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-484', ), vector=(-1.1326,-0.8229,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-558', part=mdb.models[modelname].parts['RS-0s04723-0s03818'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-558', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-558', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-558', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-558', ), vector=(-1.2135,-0.88168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-641', part=mdb.models[modelname].parts['RS-0s03818-0s02945'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-641', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-641', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-641', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-641', ), vector=(-1.2944,-0.94046,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-732', part=mdb.models[modelname].parts['RS-0s02945-0s02102'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-732', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-732', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-732', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-732', ), vector=(-1.3753,-0.99923,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-827', part=mdb.models[modelname].parts['RS-0s02102-0s01285'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-827', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-827', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-827', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-827', ), vector=(-1.4562,-1.058,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-933', part=mdb.models[modelname].parts['RS-0s01285-0s00494'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-933', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-933', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-933', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-933', ), vector=(-1.5371,-1.1168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1048', part=mdb.models[modelname].parts['RS-0s00494-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1048', ))
mdb.models[modelname].rootAssembly.rotate(angle=-54, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1048', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.58779,-0.80902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1048', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1048', ), vector=(-1.618,-1.1756,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-032', part=mdb.models[modelname].parts['RS-0s09335-0s04558'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-032', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-032', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-032', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-032', ), vector=(-0.24271,-0.17634,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-049', part=mdb.models[modelname].parts['RS-0s04558-0s01406'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-049', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-049', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-049', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-049', ), vector=(-0.24271,-0.17634,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-065', part=mdb.models[modelname].parts['RS-0s01406-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-065', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-065', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-065', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-065', ), vector=(-0.24271,-0.17634,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-074', part=mdb.models[modelname].parts['RS-0s06847-0s02070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-074', ))
mdb.models[modelname].rootAssembly.rotate(angle=131.938, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-074', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.66833,0.74387,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-074', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-074', ), vector=(-0.48541,-0.35267,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-121', part=mdb.models[modelname].parts['RS-0s02070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-121', ))
mdb.models[modelname].rootAssembly.rotate(angle=131.938, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-121', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.66833,0.74387,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-121', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-121', ), vector=(-0.41102,-0.28584,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-219', part=mdb.models[modelname].parts['RS-0s04445-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-219', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-219', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-219', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-219', ), vector=(-0.80902,-0.58779,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-485', part=mdb.models[modelname].parts['RS-0s02549-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-485', ))
mdb.models[modelname].rootAssembly.rotate(angle=-117.4126, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-485', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.46039,-0.88771,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-485', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-485', ), vector=(-1.1326,-0.8229,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-828', part=mdb.models[modelname].parts['RS-0s00946-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-828', ))
mdb.models[modelname].rootAssembly.rotate(angle=-117.4294, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-828', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.46066,-0.88758,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-828', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-828', ), vector=(-1.4562,-1.058,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-006', part=mdb.models[modelname].parts['RS-0s31144-0s26367'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-006', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-006', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-006', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-006', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-012', part=mdb.models[modelname].parts['RS-0s26367-0s23215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-012', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-012', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-012', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-012', ), vector=(0.030902,-0.095106,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-018', part=mdb.models[modelname].parts['RS-0s23215-0s20744'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-018', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-018', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-018', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-018', ), vector=(0.061803,-0.19021,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-033', part=mdb.models[modelname].parts['RS-0s20744-0s18665'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-033', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-033', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-033', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-033', ), vector=(0.092705,-0.28532,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-040', part=mdb.models[modelname].parts['RS-0s18665-0s16846'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-040', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-040', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-040', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-040', ), vector=(0.12361,-0.38042,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-056', part=mdb.models[modelname].parts['RS-0s16846-0s15215'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-056', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-056', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-056', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-056', ), vector=(0.15451,-0.47553,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-075', part=mdb.models[modelname].parts['RS-0s15215-0s13729'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-075', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-075', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-075', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-075', ), vector=(0.18541,-0.57063,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-107', part=mdb.models[modelname].parts['RS-0s13729-0s12357'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-107', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-107', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-107', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-107', ), vector=(0.21631,-0.66574,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-137', part=mdb.models[modelname].parts['RS-0s12357-0s11079'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-137', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-137', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-137', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-137', ), vector=(0.24721,-0.76085,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-174', part=mdb.models[modelname].parts['RS-0s11079-0s09879'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-174', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-174', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-174', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-174', ), vector=(0.27812,-0.85595,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-220', part=mdb.models[modelname].parts['RS-0s09879-0s08745'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-220', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-220', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-220', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-220', ), vector=(0.30902,-0.95106,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-277', part=mdb.models[modelname].parts['RS-0s08745-0s07670'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-277', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-277', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-277', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-277', ), vector=(0.33992,-1.0462,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-336', part=mdb.models[modelname].parts['RS-0s07670-0s06645'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-336', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-336', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-336', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-336', ), vector=(0.37082,-1.1413,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-406', part=mdb.models[modelname].parts['RS-0s06645-0s05664'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-406', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-406', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-406', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-406', ), vector=(0.40172,-1.2364,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-486', part=mdb.models[modelname].parts['RS-0s05664-0s04723'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-486', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-486', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-486', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-486', ), vector=(0.43262,-1.3315,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-559', part=mdb.models[modelname].parts['RS-0s04723-0s03818'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-559', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-559', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-559', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-559', ), vector=(0.46353,-1.4266,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-642', part=mdb.models[modelname].parts['RS-0s03818-0s02945'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-642', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-642', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-642', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-642', ), vector=(0.49443,-1.5217,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-733', part=mdb.models[modelname].parts['RS-0s02945-0s02102'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-733', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-733', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-733', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-733', ), vector=(0.52533,-1.6168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-829', part=mdb.models[modelname].parts['RS-0s02102-0s01285'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-829', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-829', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-829', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-829', ), vector=(0.55623,-1.7119,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-934', part=mdb.models[modelname].parts['RS-0s01285-0s00494'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-934', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-934', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-934', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-934', ), vector=(0.58713,-1.807,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1049', part=mdb.models[modelname].parts['RS-0s00494-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1049', ))
mdb.models[modelname].rootAssembly.rotate(angle=18, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1049', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.95106,0.30902,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1049', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1049', ), vector=(0.61803,-1.9021,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-034', part=mdb.models[modelname].parts['RS-0s09335-0s04558'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-034', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-034', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-034', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-034', ), vector=(0.092705,-0.28532,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-050', part=mdb.models[modelname].parts['RS-0s04558-0s01406'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-050', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-050', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-050', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-050', ), vector=(0.092705,-0.28532,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-066', part=mdb.models[modelname].parts['RS-0s01406-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-066', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-066', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-066', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-066', ), vector=(0.092705,-0.28532,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-108', part=mdb.models[modelname].parts['RS-0s06178-0s01401'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-108', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.3495, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-108', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.54974,0.83533,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-108', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-108', ), vector=(0.21631,-0.66574,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-167', part=mdb.models[modelname].parts['RS-0s01401-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-167', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.3495, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-167', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.54974,0.83533,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-167', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-167', ), vector=(0.29985,-0.61077,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-278', part=mdb.models[modelname].parts['RS-0s03935-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-278', ))
mdb.models[modelname].rootAssembly.rotate(angle=-90.8096, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-278', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.01413,-0.9999,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-278', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-278', ), vector=(0.33992,-1.0462,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-487', part=mdb.models[modelname].parts['RS-0s02549-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-487', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-487', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-487', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-487', ), vector=(0.43262,-1.3315,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-734', part=mdb.models[modelname].parts['RS-0s01325-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-734', ))
mdb.models[modelname].rootAssembly.rotate(angle=4.0633, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-734', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.99749,0.070859,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-734', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-734', ), vector=(0.52533,-1.6168,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-1050', part=mdb.models[modelname].parts['RS-0s00222-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1050', ))
mdb.models[modelname].rootAssembly.rotate(angle=117.4855, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1050', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(-0.46152,0.88713,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-1050', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-1050', ), vector=(0.61803,-1.9021,0))

# =========================================

# Root structure part and instance creation by merging all root segments
inst = mdb.models[modelname].rootAssembly.instances
mdb.models[modelname].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=[v for k, v in inst.items()], 
    keepIntersections=OFF, name='RootStruct', originalInstances=DELETE)

# =========================================

# Root structure section assignment
mdb.models[modelname].parts['RootStruct'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(cells=mdb.models[modelname].parts['RootStruct'].cells),
    sectionName='RootSection', thicknessAssignment=FROM_SECTION)

# =========================================

# Soil instance and positioning
mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='Soil', part=mdb.models[modelname].parts['Soil'])
mdb.models[modelname].rootAssembly.translate(instanceList=('Soil', ), vector=(-soil["Lx_Ly"]/2, -soil["Lx_Ly"]/2, -3))
# =========================================

# Soil structure part and instance creation by merging root structure and soil
mdb.models[modelname].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models[modelname].rootAssembly.instances['RootStruct-1'], 
               mdb.models[modelname].rootAssembly.instances['Soil']), 
keepIntersections=ON, name='SoilStructure', originalInstances=DELETE)

# =========================================

