# Script automatically generated on 06-Jun-2018 at 16:42 by RootGen
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
	"init_diam" : 0.31781,
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
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00150/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00150/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00150-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00150-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00333/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00333/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00333-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00333-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00340/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00340/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00340-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00340-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00495/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00495/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00495-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00495-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00756/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00756/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00756-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00756-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.00756/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00756/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s00756-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s00756-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01070/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01070/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01070-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01070-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.01262/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01262/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s01262-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s01262-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02356/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02356/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02356-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02356-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02804/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02804/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02804-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02804-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.02804/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02804/2, 0.0), point2=(0.00333/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00333/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s02804-0s00333', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s02804-0s00333'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.03908/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03908/2, 0.0), point2=(0.00756/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00756/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s03908-0s00756', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s03908-0s00756'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.03908/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03908/2, 0.0), point2=(0.00756/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00756/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s03908-0s00756', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s03908-0s00756'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.04732/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.04732/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s04732-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s04732-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.05272/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05272/2, 0.0), point2=(0.00495/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.00495/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s05272-0s00495', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s05272-0s00495'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.05847/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05847/2, 0.0), point2=(0.01070/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.01070/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s05847-0s01070', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s05847-0s01070'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.05956/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05956/2, 0.0), point2=(0.02804/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02804/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s05956-0s02804', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s05956-0s02804'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.07133/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.07133/2, 0.0), point2=(0.02356/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.02356/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s07133-0s02356', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s07133-0s02356'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.08685/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.08685/2, 0.0), point2=(0.03908/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.03908/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s08685-0s03908', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s08685-0s03908'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.10515/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.10515/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s10515-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s10515-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.10515/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.10515/2, 0.0), point2=(0.0, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))
mdb.models[modelname].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=mdb.models[modelname].sketches['__profile__'].geometry[5])
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s10515-0s00000', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s10515-0s00000'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.10733/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.10733/2, 0.0), point2=(0.05956/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.05956/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s10733-0s05956', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s10733-0s05956'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.11715/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.11715/2, 0.0), point2=(0.10515/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.10515/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s11715-0s10515', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s11715-0s10515'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.11715/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.11715/2, 0.0), point2=(0.10515/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.10515/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s11715-0s10515', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s11715-0s10515'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.12994/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.12994/2, 0.0), point2=(0.11715/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.11715/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s12994-0s11715', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s12994-0s11715'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.12994/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.12994/2, 0.0), point2=(0.11715/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.11715/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s12994-0s11715', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s12994-0s11715'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.14366/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.14366/2, 0.0), point2=(0.12994/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.12994/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s14366-0s12994', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s14366-0s12994'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.14366/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.14366/2, 0.0), point2=(0.12994/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.12994/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s14366-0s12994', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s14366-0s12994'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.15852/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.15852/2, 0.0), point2=(0.14366/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.14366/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s15852-0s14366', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s15852-0s14366'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.17482/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.17482/2, 0.0), point2=(0.15852/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.15852/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s17482-0s15852', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s17482-0s15852'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.19301/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.19301/2, 0.0), point2=(0.17482/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.17482/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s19301-0s17482', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s19301-0s17482'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.21381/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.21381/2, 0.0), point2=(0.19301/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.19301/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s21381-0s19301', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s21381-0s19301'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.23852/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.23852/2, 0.0), point2=(0.21381/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.21381/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s23852-0s21381', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s23852-0s21381'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.27004/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.27004/2, 0.0), point2=(0.23852/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.23852/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s27004-0s23852', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s27004-0s23852'].BaseSolidRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']


mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelname].sketches['__profile__'].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
mdb.models[modelname].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(0.31781/2, 0.0))
mdb.models[modelname].sketches['__profile__'].HorizontalConstraint(addUndoState=False, entity=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].geometry[2], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[3])
mdb.models[modelname].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=
    mdb.models[modelname].sketches['__profile__'].vertices[0], entity2=
    mdb.models[modelname].sketches['__profile__'].geometry[2])
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.31781/2, 0.0), point2=(0.27004/2, root["seg_dl"]))
mdb.models[modelname].sketches['__profile__'].Line(point1=(0.27004/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))
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
mdb.models[modelname].Part(dimensionality=THREE_D, name='RS-0s31781-0s27004', type=DEFORMABLE_BODY)
mdb.models[modelname].parts['RS-0s31781-0s27004'].BaseSolidRevolve(angle=360.0, 
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
mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-001', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-001', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-001', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-001', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-001', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-009', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-009', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-009', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-009', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-009', ), vector=(0,0,-0.1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-017', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-017', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-017', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-017', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-017', ), vector=(0,0,-0.2))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-032', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-032', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-032', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-032', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-032', ), vector=(0,0,-0.3))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-047', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-047', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-047', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-047', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-047', ), vector=(0,0,-0.4))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-074', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-074', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-074', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-074', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-074', ), vector=(0,0,-0.5))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-101', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-101', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-101', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-101', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-101', ), vector=(0,0,-0.6))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-143', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-143', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-143', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-143', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-143', ), vector=(0,0,-0.7))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-189', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-189', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-189', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-189', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-189', ), vector=(0,0,-0.8))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-247', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-247', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-247', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-247', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-247', ), vector=(0,0,-0.9))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-317', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-317', ))
mdb.models[modelname].rootAssembly.rotate(angle=0, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-317', ))
mdb.models[modelname].rootAssembly.rotate(angle=180, axisDirection=(1,0,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-317', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-317', ), vector=(0,0,-1))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-002', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-002', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-002', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-002', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-002', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-010', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-010', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-010', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-010', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-010', ), vector=(0.028694,0,-0.095795))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-018', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-018', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-018', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-018', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-018', ), vector=(0.057388,0,-0.19159))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-033', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-033', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-033', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-033', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-033', ), vector=(0.086082,0,-0.28738))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-048', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-048', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-048', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-048', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-048', ), vector=(0.11478,0,-0.38318))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-075', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-075', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-075', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-075', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-075', ), vector=(0.14347,0,-0.47897))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-102', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-102', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-102', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-102', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-102', ), vector=(0.17216,0,-0.57477))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-144', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-144', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-144', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-144', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-144', ), vector=(0.20086,0,-0.67056))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-190', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-190', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-190', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-190', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-190', ), vector=(0.22955,0,-0.76636))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-248', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-248', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-248', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-248', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-248', ), vector=(0.25825,0,-0.86215))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-318', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-318', ))
mdb.models[modelname].rootAssembly.rotate(angle=90, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-318', ))
mdb.models[modelname].rootAssembly.rotate(angle=163.3251, axisDirection=(6.1232e-17,1,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-318', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-318', ), vector=(0.28694,0,-0.95795))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-019', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-019', ))
mdb.models[modelname].rootAssembly.rotate(angle=-146.9838, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-019', ))
mdb.models[modelname].rootAssembly.rotate(angle=68.1189, axisDirection=(-0.83852,-0.54488,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-019', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-019', ), vector=(0.057388,0,-0.19159))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-040', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-040', ))
mdb.models[modelname].rootAssembly.rotate(angle=-146.9838, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-040', ))
mdb.models[modelname].rootAssembly.rotate(angle=68.1189, axisDirection=(-0.83852,-0.54488,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-040', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-040', ), vector=(0.0068258,0.077811,-0.15432))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-062', part=mdb.models[modelname].parts['RS-0s02804-0s00333'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-062', ))
mdb.models[modelname].rootAssembly.rotate(angle=-146.9838, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-062', ))
mdb.models[modelname].rootAssembly.rotate(angle=68.1189, axisDirection=(-0.83852,-0.54488,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-062', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-062', ), vector=(-0.043737,0.15562,-0.11705))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-082', part=mdb.models[modelname].parts['RS-0s00333-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-082', ))
mdb.models[modelname].rootAssembly.rotate(angle=-146.9838, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-082', ))
mdb.models[modelname].rootAssembly.rotate(angle=68.1189, axisDirection=(-0.83852,-0.54488,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-082', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-082', ), vector=(-0.094299,0.23343,-0.079785))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-063', part=mdb.models[modelname].parts['RS-0s01262-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-063', ))
mdb.models[modelname].rootAssembly.rotate(angle=-176.674, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-063', ))
mdb.models[modelname].rootAssembly.rotate(angle=65.4595, axisDirection=(-0.99832,-0.058018,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-063', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-063', ), vector=(-0.043737,0.15562,-0.11705))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-049', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-049', ))
mdb.models[modelname].rootAssembly.rotate(angle=62.9352, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-049', ))
mdb.models[modelname].rootAssembly.rotate(angle=132.7843, axisDirection=(0.455,0.89049,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-049', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-049', ), vector=(0.11478,0,-0.38318))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-089', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-089', ))
mdb.models[modelname].rootAssembly.rotate(angle=62.9352, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-089', ))
mdb.models[modelname].rootAssembly.rotate(angle=132.7843, axisDirection=(0.455,0.89049,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-089', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-089', ), vector=(0.18013,-0.033393,-0.4511))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-127', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-127', ))
mdb.models[modelname].rootAssembly.rotate(angle=62.9352, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-127', ))
mdb.models[modelname].rootAssembly.rotate(angle=132.7843, axisDirection=(0.455,0.89049,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-127', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-127', ), vector=(0.24549,-0.066786,-0.51903))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-103', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-103', ))
mdb.models[modelname].rootAssembly.rotate(angle=53.5055, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-103', ))
mdb.models[modelname].rootAssembly.rotate(angle=82.5224, axisDirection=(0.59475,0.80391,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-103', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-103', ), vector=(0.17216,0,-0.57477))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-174', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-174', ))
mdb.models[modelname].rootAssembly.rotate(angle=53.5055, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-174', ))
mdb.models[modelname].rootAssembly.rotate(angle=82.5224, axisDirection=(0.59475,0.80391,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-174', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-174', ), vector=(0.25187,-0.058969,-0.56176))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-191', part=mdb.models[modelname].parts['RS-0s05847-0s01070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-191', ))
mdb.models[modelname].rootAssembly.rotate(angle=-108.3423, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-191', ))
mdb.models[modelname].rootAssembly.rotate(angle=127.8293, axisDirection=(-0.31469,-0.94919,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-191', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-191', ), vector=(0.22955,0,-0.76636))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-304', part=mdb.models[modelname].parts['RS-0s01070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-304', ))
mdb.models[modelname].rootAssembly.rotate(angle=-108.3423, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-304', ))
mdb.models[modelname].rootAssembly.rotate(angle=127.8293, axisDirection=(-0.31469,-0.94919,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-304', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-304', ), vector=(0.15458,0.024856,-0.82769))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-319', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-319', ))
mdb.models[modelname].rootAssembly.rotate(angle=99.4307, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-319', ))
mdb.models[modelname].rootAssembly.rotate(angle=147.8099, axisDirection=(-0.16385,0.98648,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-319', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-319', ), vector=(0.28694,0,-0.95795))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-320', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-320', ))
mdb.models[modelname].rootAssembly.rotate(angle=16.7392, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-320', ))
mdb.models[modelname].rootAssembly.rotate(angle=174.7701, axisDirection=(0.95763,0.28802,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-320', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-320', ), vector=(0.28694,0,-0.95795))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-003', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-003', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-003', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-003', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-003', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-011', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-011', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-011', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-011', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-011', ), vector=(0.0091929,0.011527,-0.098907))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-020', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-020', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-020', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-020', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-020', ), vector=(0.018386,0.023055,-0.19781))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-034', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-034', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-034', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-034', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-034', ), vector=(0.027579,0.034582,-0.29672))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-050', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-050', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-050', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-050', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-050', ), vector=(0.036771,0.04611,-0.39563))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-076', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-076', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-076', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-076', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-076', ), vector=(0.045964,0.057637,-0.49454))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-104', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-104', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-104', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-104', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-104', ), vector=(0.055157,0.069165,-0.59344))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-145', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-145', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-145', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-145', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-145', ), vector=(0.06435,0.080692,-0.69235))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-192', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-192', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-192', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-192', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-192', ), vector=(0.073543,0.09222,-0.79126))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-249', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-249', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-249', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-249', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-249', ), vector=(0.082736,0.10375,-0.89016))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-321', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-321', ))
mdb.models[modelname].rootAssembly.rotate(angle=141.4286, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-321', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5213, axisDirection=(-0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-321', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-321', ), vector=(0.091929,0.11527,-0.98907))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-021', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-021', ))
mdb.models[modelname].rootAssembly.rotate(angle=-114.2384, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-021', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.5837, axisDirection=(-0.41053,-0.91184,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-021', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-021', ), vector=(0.018386,0.023055,-0.19781))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-041', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-041', ))
mdb.models[modelname].rootAssembly.rotate(angle=-114.2384, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-041', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.5837, axisDirection=(-0.41053,-0.91184,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-041', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-041', ), vector=(-0.031831,0.045664,-0.28128))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-064', part=mdb.models[modelname].parts['RS-0s02804-0s00333'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-064', ))
mdb.models[modelname].rootAssembly.rotate(angle=-114.2384, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-064', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.5837, axisDirection=(-0.41053,-0.91184,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-064', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-064', ), vector=(-0.082048,0.068273,-0.36475))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-083', part=mdb.models[modelname].parts['RS-0s00333-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-083', ))
mdb.models[modelname].rootAssembly.rotate(angle=-114.2384, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-083', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.5837, axisDirection=(-0.41053,-0.91184,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-083', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-083', ), vector=(-0.13227,0.090882,-0.44822))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-065', part=mdb.models[modelname].parts['RS-0s01262-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-065', ))
mdb.models[modelname].rootAssembly.rotate(angle=-152.5178, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-065', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.8192, axisDirection=(-0.88715,-0.46147,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-065', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-065', ), vector=(-0.082048,0.068273,-0.36475))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-051', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-051', ))
mdb.models[modelname].rootAssembly.rotate(angle=-75.3165, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-051', ))
mdb.models[modelname].rootAssembly.rotate(angle=160.6502, axisDirection=(0.25348,-0.96734,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-051', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-051', ), vector=(0.036771,0.04611,-0.39563))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-090', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-090', ))
mdb.models[modelname].rootAssembly.rotate(angle=-75.3165, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-090', ))
mdb.models[modelname].rootAssembly.rotate(angle=160.6502, axisDirection=(0.25348,-0.96734,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-090', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-090', ), vector=(0.0047201,0.037711,-0.48998))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-128', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-128', ))
mdb.models[modelname].rootAssembly.rotate(angle=-75.3165, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-128', ))
mdb.models[modelname].rootAssembly.rotate(angle=160.6502, axisDirection=(0.25348,-0.96734,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-128', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-128', ), vector=(-0.027331,0.029313,-0.58433))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-105', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-105', ))
mdb.models[modelname].rootAssembly.rotate(angle=167.1456, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-105', ))
mdb.models[modelname].rootAssembly.rotate(angle=178.1361, axisDirection=(-0.97494,0.22247,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-105', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-105', ), vector=(0.055157,0.069165,-0.59344))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-175', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-175', ))
mdb.models[modelname].rootAssembly.rotate(angle=167.1456, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-175', ))
mdb.models[modelname].rootAssembly.rotate(angle=178.1361, axisDirection=(-0.97494,0.22247,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-175', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-175', ), vector=(0.055881,0.072336,-0.69339))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-193', part=mdb.models[modelname].parts['RS-0s05847-0s01070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-193', ))
mdb.models[modelname].rootAssembly.rotate(angle=159.3069, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-193', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2098, axisDirection=(-0.93549,0.35336,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-193', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-193', ), vector=(0.073543,0.09222,-0.79126))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-305', part=mdb.models[modelname].parts['RS-0s01070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-305', ))
mdb.models[modelname].rootAssembly.rotate(angle=159.3069, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-305', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2098, axisDirection=(-0.93549,0.35336,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-305', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-305', ), vector=(0.078333,0.1049,-0.89033))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-004', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-004', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-004', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-004', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-004', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-012', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-012', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-012', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-012', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-012', ), vector=(-0.021811,0.09556,-0.019815))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-022', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-022', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-022', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-022', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-022', ), vector=(-0.043622,0.19112,-0.03963))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-035', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-035', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-035', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-035', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-035', ), vector=(-0.065433,0.28668,-0.059445))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-052', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-052', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-052', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-052', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-052', ), vector=(-0.087243,0.38224,-0.07926))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-077', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-077', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-077', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-077', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-077', ), vector=(-0.10905,0.4778,-0.099075))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-106', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-106', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-106', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-106', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-106', ), vector=(-0.13087,0.57336,-0.11889))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-146', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-146', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-146', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-146', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-146', ), vector=(-0.15268,0.66892,-0.13871))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-194', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-194', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-194', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-194', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-194', ), vector=(-0.17449,0.76448,-0.15852))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-250', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-250', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-250', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-250', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-250', ), vector=(-0.1963,0.86004,-0.17834))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-322', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-322', ))
mdb.models[modelname].rootAssembly.rotate(angle=-167.1429, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-322', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.4288, axisDirection=(-0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-322', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-322', ), vector=(-0.21811,0.9556,-0.19815))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-023', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-023', ))
mdb.models[modelname].rootAssembly.rotate(angle=-142.5718, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-023', ))
mdb.models[modelname].rootAssembly.rotate(angle=108.475, axisDirection=(-0.79412,-0.60777,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-023', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-023', ), vector=(-0.043622,0.19112,-0.03963))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-042', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-042', ))
mdb.models[modelname].rootAssembly.rotate(angle=-142.5718, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-042', ))
mdb.models[modelname].rootAssembly.rotate(angle=108.475, axisDirection=(-0.79412,-0.60777,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-042', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-042', ), vector=(-0.10127,0.26644,-0.071319))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-066', part=mdb.models[modelname].parts['RS-0s02804-0s00333'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-066', ))
mdb.models[modelname].rootAssembly.rotate(angle=-142.5718, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-066', ))
mdb.models[modelname].rootAssembly.rotate(angle=108.475, axisDirection=(-0.79412,-0.60777,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-066', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-066', ), vector=(-0.15891,0.34176,-0.10301))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-084', part=mdb.models[modelname].parts['RS-0s00333-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-084', ))
mdb.models[modelname].rootAssembly.rotate(angle=-142.5718, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-084', ))
mdb.models[modelname].rootAssembly.rotate(angle=108.475, axisDirection=(-0.79412,-0.60777,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-084', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-084', ), vector=(-0.21655,0.41708,-0.1347))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-067', part=mdb.models[modelname].parts['RS-0s01262-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-067', ))
mdb.models[modelname].rootAssembly.rotate(angle=-169.031, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-067', ))
mdb.models[modelname].rootAssembly.rotate(angle=95.708, axisDirection=(-0.98173,-0.19028,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-067', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-067', ), vector=(-0.15891,0.34176,-0.10301))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-053', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-053', ))
mdb.models[modelname].rootAssembly.rotate(angle=-117.695, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-053', ))
mdb.models[modelname].rootAssembly.rotate(angle=90.2496, axisDirection=(-0.46476,-0.88543,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-053', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-053', ), vector=(-0.087243,0.38224,-0.07926))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-091', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-091', ))
mdb.models[modelname].rootAssembly.rotate(angle=-117.695, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-091', ))
mdb.models[modelname].rootAssembly.rotate(angle=90.2496, axisDirection=(-0.46476,-0.88543,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-091', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-091', ), vector=(-0.17579,0.42871,-0.079696))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-129', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-129', ))
mdb.models[modelname].rootAssembly.rotate(angle=-117.695, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-129', ))
mdb.models[modelname].rootAssembly.rotate(angle=90.2496, axisDirection=(-0.46476,-0.88543,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-129', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-129', ), vector=(-0.26433,0.47519,-0.080131))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-130', part=mdb.models[modelname].parts['RS-0s00340-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-130', ))
mdb.models[modelname].rootAssembly.rotate(angle=-107.2607, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-130', ))
mdb.models[modelname].rootAssembly.rotate(angle=110.8873, axisDirection=(-0.29672,-0.95496,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-130', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-130', ), vector=(-0.26433,0.47519,-0.080131))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-107', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-107', ))
mdb.models[modelname].rootAssembly.rotate(angle=166.5636, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-107', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.6353, axisDirection=(-0.97263,0.23237,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-107', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-107', ), vector=(-0.13087,0.57336,-0.11889))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-176', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-176', ))
mdb.models[modelname].rootAssembly.rotate(angle=166.5636, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-176', ))
mdb.models[modelname].rootAssembly.rotate(angle=149.6353, axisDirection=(-0.97263,0.23237,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-176', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-176', ), vector=(-0.11912,0.62252,-0.20517))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-251', part=mdb.models[modelname].parts['RS-0s05272-0s00495'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-251', ))
mdb.models[modelname].rootAssembly.rotate(angle=-173.7516, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-251', ))
mdb.models[modelname].rootAssembly.rotate(angle=110.8507, axisDirection=(-0.99406,-0.10884,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-251', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-251', ), vector=(-0.1963,0.86004,-0.17834))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-397', part=mdb.models[modelname].parts['RS-0s00495-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-397', ))
mdb.models[modelname].rootAssembly.rotate(angle=-173.7516, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-397', ))
mdb.models[modelname].rootAssembly.rotate(angle=110.8507, axisDirection=(-0.99406,-0.10884,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-397', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-397', ), vector=(-0.20647,0.95293,-0.21393))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-323', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-323', ))
mdb.models[modelname].rootAssembly.rotate(angle=-147.4851, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-323', ))
mdb.models[modelname].rootAssembly.rotate(angle=117.269, axisDirection=(-0.84325,-0.53752,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-323', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-323', ), vector=(-0.21811,0.9556,-0.19815))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-324', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-324', ))
mdb.models[modelname].rootAssembly.rotate(angle=175.3735, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-324', ))
mdb.models[modelname].rootAssembly.rotate(angle=84.4312, axisDirection=(-0.99674,0.08066,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-324', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-324', ), vector=(-0.21811,0.9556,-0.19815))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-005', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-005', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-005', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-005', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-005', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-013', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-013', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-013', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-013', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-013', ), vector=(-0.012222,0.0058856,-0.099076))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-024', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-024', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-024', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-024', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-024', ), vector=(-0.024443,0.011771,-0.19815))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-036', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-036', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-036', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-036', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-036', ), vector=(-0.036665,0.017657,-0.29723))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-054', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-054', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-054', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-054', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-054', ), vector=(-0.048886,0.023542,-0.3963))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-078', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-078', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-078', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-078', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-078', ), vector=(-0.061108,0.029428,-0.49538))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-108', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-108', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-108', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-108', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-108', ), vector=(-0.07333,0.035314,-0.59445))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-147', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-147', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-147', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-147', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-147', ), vector=(-0.085551,0.041199,-0.69353))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-195', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-195', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-195', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-195', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-195', ), vector=(-0.097773,0.047085,-0.79261))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-252', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-252', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-252', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-252', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-252', ), vector=(-0.10999,0.05297,-0.89168))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-325', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-325', ))
mdb.models[modelname].rootAssembly.rotate(angle=-115.7143, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-325', ))
mdb.models[modelname].rootAssembly.rotate(angle=172.2038, axisDirection=(-0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-325', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-325', ), vector=(-0.12222,0.058856,-0.99076))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-025', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-025', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.5023, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-025', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.7648, axisDirection=(0.43048,-0.9026,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-025', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-025', ), vector=(-0.024443,0.011771,-0.19815))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-043', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-043', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.5023, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-043', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.7648, axisDirection=(0.43048,-0.9026,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-043', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-043', ), vector=(-0.099479,-0.024015,-0.25373))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-068', part=mdb.models[modelname].parts['RS-0s02804-0s00333'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-068', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.5023, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-068', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.7648, axisDirection=(0.43048,-0.9026,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-068', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-068', ), vector=(-0.17451,-0.059802,-0.30931))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-085', part=mdb.models[modelname].parts['RS-0s00333-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-085', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.5023, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-085', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.7648, axisDirection=(0.43048,-0.9026,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-085', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-085', ), vector=(-0.24955,-0.095588,-0.36489))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-069', part=mdb.models[modelname].parts['RS-0s01262-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-069', ))
mdb.models[modelname].rootAssembly.rotate(angle=-26.0904, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-069', ))
mdb.models[modelname].rootAssembly.rotate(angle=161.2041, axisDirection=(0.8981,-0.43979,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-069', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-069', ), vector=(-0.17451,-0.059802,-0.30931))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-055', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-055', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.3931, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-055', ))
mdb.models[modelname].rootAssembly.rotate(angle=128.9586, axisDirection=(-0.36476,0.9311,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-055', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-055', ), vector=(-0.048886,0.023542,-0.3963))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-092', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-092', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.3931, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-092', ))
mdb.models[modelname].rootAssembly.rotate(angle=128.9586, axisDirection=(-0.36476,0.9311,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-092', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-092', ), vector=(0.023516,0.051907,-0.45918))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-131', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-131', ))
mdb.models[modelname].rootAssembly.rotate(angle=111.3931, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-131', ))
mdb.models[modelname].rootAssembly.rotate(angle=128.9586, axisDirection=(-0.36476,0.9311,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-131', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-131', ), vector=(0.095918,0.080271,-0.52205))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-132', part=mdb.models[modelname].parts['RS-0s00340-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-132', ))
mdb.models[modelname].rootAssembly.rotate(angle=136.8105, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-132', ))
mdb.models[modelname].rootAssembly.rotate(angle=70.1082, axisDirection=(-0.72909,0.68441,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-132', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-132', ), vector=(0.095918,0.080271,-0.52205))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-109', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-109', ))
mdb.models[modelname].rootAssembly.rotate(angle=-98.9314, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-109', ))
mdb.models[modelname].rootAssembly.rotate(angle=178.3015, axisDirection=(-0.15525,-0.98787,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-109', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-109', ), vector=(-0.07333,0.035314,-0.59445))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-177', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-177', ))
mdb.models[modelname].rootAssembly.rotate(angle=-98.9314, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-177', ))
mdb.models[modelname].rootAssembly.rotate(angle=178.3015, axisDirection=(-0.15525,-0.98787,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-177', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-177', ), vector=(-0.076258,0.035774,-0.69441))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-196', part=mdb.models[modelname].parts['RS-0s05847-0s01070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-196', ))
mdb.models[modelname].rootAssembly.rotate(angle=-143.1531, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-196', ))
mdb.models[modelname].rootAssembly.rotate(angle=137.184, axisDirection=(-0.80024,-0.59968,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-196', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-196', ), vector=(-0.097773,0.047085,-0.79261))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-306', part=mdb.models[modelname].parts['RS-0s01070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-306', ))
mdb.models[modelname].rootAssembly.rotate(angle=-143.1531, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-306', ))
mdb.models[modelname].rootAssembly.rotate(angle=137.184, axisDirection=(-0.80024,-0.59968,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-306', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-306', ), vector=(-0.13853,0.10147,-0.86596))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-326', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-326', ))
mdb.models[modelname].rootAssembly.rotate(angle=-105.4153, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-326', ))
mdb.models[modelname].rootAssembly.rotate(angle=169.8975, axisDirection=(-0.26581,-0.96402,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-326', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-326', ), vector=(-0.12222,0.058856,-0.99076))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-327', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-327', ))
mdb.models[modelname].rootAssembly.rotate(angle=-133.3931, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-327', ))
mdb.models[modelname].rootAssembly.rotate(angle=174.0726, axisDirection=(-0.687,-0.72666,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-327', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-327', ), vector=(-0.12222,0.058856,-0.99076))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-006', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-006', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-006', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-006', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-006', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-014', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-014', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-014', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-014', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-014', ), vector=(-0.049186,-0.023687,-0.083784))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-026', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-026', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-026', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-026', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-026', ), vector=(-0.098372,-0.047373,-0.16757))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-037', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-037', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-037', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-037', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-037', ), vector=(-0.14756,-0.07106,-0.25135))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-056', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-056', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-056', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-056', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-056', ), vector=(-0.19674,-0.094747,-0.33513))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-079', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-079', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-079', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-079', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-079', ), vector=(-0.24593,-0.11843,-0.41892))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-110', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-110', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-110', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-110', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-110', ), vector=(-0.29512,-0.14212,-0.5027))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-148', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-148', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-148', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-148', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-148', ), vector=(-0.3443,-0.16581,-0.58649))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-197', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-197', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-197', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-197', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-197', ), vector=(-0.39349,-0.18949,-0.67027))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-253', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-253', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-253', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-253', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-253', ), vector=(-0.44267,-0.21318,-0.75405))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-328', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-328', ))
mdb.models[modelname].rootAssembly.rotate(angle=-64.2857, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-328', ))
mdb.models[modelname].rootAssembly.rotate(angle=146.9123, axisDirection=(0.43388,-0.90097,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-328', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-328', ), vector=(-0.49186,-0.23687,-0.83784))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-027', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-027', ))
mdb.models[modelname].rootAssembly.rotate(angle=138.7987, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-027', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5773, axisDirection=(-0.7524,0.65871,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-027', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-027', ), vector=(-0.098372,-0.047373,-0.16757))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-044', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-044', ))
mdb.models[modelname].rootAssembly.rotate(angle=138.7987, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-044', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5773, axisDirection=(-0.7524,0.65871,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-044', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-044', ), vector=(-0.088723,-0.036353,-0.26649))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-070', part=mdb.models[modelname].parts['RS-0s02804-0s00333'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-070', ))
mdb.models[modelname].rootAssembly.rotate(angle=138.7987, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-070', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5773, axisDirection=(-0.7524,0.65871,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-070', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-070', ), vector=(-0.079075,-0.025332,-0.36541))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-086', part=mdb.models[modelname].parts['RS-0s00333-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-086', ))
mdb.models[modelname].rootAssembly.rotate(angle=138.7987, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-086', ))
mdb.models[modelname].rootAssembly.rotate(angle=171.5773, axisDirection=(-0.7524,0.65871,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-086', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-086', ), vector=(-0.069427,-0.014311,-0.46433))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-087', part=mdb.models[modelname].parts['RS-0s00150-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-087', ))
mdb.models[modelname].rootAssembly.rotate(angle=-38.2472, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-087', ))
mdb.models[modelname].rootAssembly.rotate(angle=137.1456, axisDirection=(0.78535,-0.61906,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-087', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-087', ), vector=(-0.069427,-0.014311,-0.46433))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-057', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-057', ))
mdb.models[modelname].rootAssembly.rotate(angle=-72.5861, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-057', ))
mdb.models[modelname].rootAssembly.rotate(angle=135.9388, axisDirection=(0.29927,-0.95417,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-057', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-057', ), vector=(-0.19674,-0.094747,-0.33513))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-093', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-093', ))
mdb.models[modelname].rootAssembly.rotate(angle=-72.5861, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-093', ))
mdb.models[modelname].rootAssembly.rotate(angle=135.9388, axisDirection=(0.29927,-0.95417,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-093', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-093', ), vector=(-0.2631,-0.11556,-0.40699))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-133', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-133', ))
mdb.models[modelname].rootAssembly.rotate(angle=-72.5861, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-133', ))
mdb.models[modelname].rootAssembly.rotate(angle=135.9388, axisDirection=(0.29927,-0.95417,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-133', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-133', ), vector=(-0.32945,-0.13637,-0.47885))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-111', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-111', ))
mdb.models[modelname].rootAssembly.rotate(angle=-15.4934, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-111', ))
mdb.models[modelname].rootAssembly.rotate(angle=136.8884, axisDirection=(0.96366,-0.26713,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-111', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-111', ), vector=(-0.29512,-0.14212,-0.5027))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-178', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-178', ))
mdb.models[modelname].rootAssembly.rotate(angle=-15.4934, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-178', ))
mdb.models[modelname].rootAssembly.rotate(angle=136.8884, axisDirection=(0.96366,-0.26713,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-178', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-178', ), vector=(-0.31337,-0.20798,-0.5757))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-198', part=mdb.models[modelname].parts['RS-0s05847-0s01070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-198', ))
mdb.models[modelname].rootAssembly.rotate(angle=-88.8495, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-198', ))
mdb.models[modelname].rootAssembly.rotate(angle=100.4551, axisDirection=(0.02008,-0.9998,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-198', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-198', ), vector=(-0.39349,-0.18949,-0.67027))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-307', part=mdb.models[modelname].parts['RS-0s01070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-307', ))
mdb.models[modelname].rootAssembly.rotate(angle=-88.8495, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-307', ))
mdb.models[modelname].rootAssembly.rotate(angle=100.4551, axisDirection=(0.02008,-0.9998,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-307', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-307', ), vector=(-0.49181,-0.19147,-0.68842))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-329', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-329', ))
mdb.models[modelname].rootAssembly.rotate(angle=-45.3536, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-329', ))
mdb.models[modelname].rootAssembly.rotate(angle=134.6245, axisDirection=(0.70273,-0.71146,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-329', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-329', ), vector=(-0.49186,-0.23687,-0.83784))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-330', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-330', ))
mdb.models[modelname].rootAssembly.rotate(angle=-96.2085, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-330', ))
mdb.models[modelname].rootAssembly.rotate(angle=154.1063, axisDirection=(-0.10815,-0.99414,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-330', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-330', ), vector=(-0.49186,-0.23687,-0.83784))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-007', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-007', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-007', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-007', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-007', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-015', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-015', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-015', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-015', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-015', ), vector=(-0.021991,-0.096351,-0.015262))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-028', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-028', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-028', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-028', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-028', ), vector=(-0.043983,-0.1927,-0.030523))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-038', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-038', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-038', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-038', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-038', ), vector=(-0.065974,-0.28905,-0.045785))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-058', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-058', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-058', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-058', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-058', ), vector=(-0.087966,-0.3854,-0.061047))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-080', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-080', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-080', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-080', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-080', ), vector=(-0.10996,-0.48175,-0.076309))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-112', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-112', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-112', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-112', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-112', ), vector=(-0.13195,-0.5781,-0.09157))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-149', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-149', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-149', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-149', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-149', ), vector=(-0.15394,-0.67445,-0.10683))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-199', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-199', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-199', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-199', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-199', ), vector=(-0.17593,-0.77081,-0.12209))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-254', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-254', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-254', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-254', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-254', ), vector=(-0.19792,-0.86716,-0.13736))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-331', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-331', ))
mdb.models[modelname].rootAssembly.rotate(angle=-12.8571, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-331', ))
mdb.models[modelname].rootAssembly.rotate(angle=98.7786, axisDirection=(0.97493,-0.22252,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-331', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-331', ), vector=(-0.21991,-0.96351,-0.15262))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-029', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-029', ))
mdb.models[modelname].rootAssembly.rotate(angle=43.1862, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-029', ))
mdb.models[modelname].rootAssembly.rotate(angle=81.9717, axisDirection=(0.72913,0.68437,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-029', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-029', ), vector=(-0.043983,-0.1927,-0.030523))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-045', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-045', ))
mdb.models[modelname].rootAssembly.rotate(angle=43.1862, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-045', ))
mdb.models[modelname].rootAssembly.rotate(angle=81.9717, axisDirection=(0.72913,0.68437,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-045', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-045', ), vector=(0.023784,-0.2649,-0.016557))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-071', part=mdb.models[modelname].parts['RS-0s02804-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-071', ))
mdb.models[modelname].rootAssembly.rotate(angle=43.1862, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-071', ))
mdb.models[modelname].rootAssembly.rotate(angle=81.9717, axisDirection=(0.72913,0.68437,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-071', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-071', ), vector=(0.09155,-0.3371,-0.0025911))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-059', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-059', ))
mdb.models[modelname].rootAssembly.rotate(angle=-42.5895, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-059', ))
mdb.models[modelname].rootAssembly.rotate(angle=99.8117, axisDirection=(0.73622,-0.67674,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-059', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-059', ), vector=(-0.087966,-0.3854,-0.061047))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-094', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-094', ))
mdb.models[modelname].rootAssembly.rotate(angle=-42.5895, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-094', ))
mdb.models[modelname].rootAssembly.rotate(angle=99.8117, axisDirection=(0.73622,-0.67674,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-094', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-094', ), vector=(-0.15465,-0.45795,-0.078088))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-134', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-134', ))
mdb.models[modelname].rootAssembly.rotate(angle=-42.5895, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-134', ))
mdb.models[modelname].rootAssembly.rotate(angle=99.8117, axisDirection=(0.73622,-0.67674,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-134', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-134', ), vector=(-0.22133,-0.53049,-0.095129))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-135', part=mdb.models[modelname].parts['RS-0s00340-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-135', ))
mdb.models[modelname].rootAssembly.rotate(angle=-116.1008, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-135', ))
mdb.models[modelname].rootAssembly.rotate(angle=128.6747, axisDirection=(-0.43995,-0.89802,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-135', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-135', ), vector=(-0.22133,-0.53049,-0.095129))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-113', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-113', ))
mdb.models[modelname].rootAssembly.rotate(angle=41.7239, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-113', ))
mdb.models[modelname].rootAssembly.rotate(angle=126.4341, axisDirection=(0.74636,0.66554,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-113', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-113', ), vector=(-0.13195,-0.5781,-0.09157))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-179', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-179', ))
mdb.models[modelname].rootAssembly.rotate(angle=41.7239, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-179', ))
mdb.models[modelname].rootAssembly.rotate(angle=126.4341, axisDirection=(0.74636,0.66554,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-179', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-179', ), vector=(-0.078403,-0.63815,-0.15096))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-200', part=mdb.models[modelname].parts['RS-0s05847-0s01070'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-200', ))
mdb.models[modelname].rootAssembly.rotate(angle=-33.1065, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-200', ))
mdb.models[modelname].rootAssembly.rotate(angle=108.8771, axisDirection=(0.83766,-0.5462,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-200', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-200', ), vector=(-0.17593,-0.77081,-0.12209))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-308', part=mdb.models[modelname].parts['RS-0s01070-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-308', ))
mdb.models[modelname].rootAssembly.rotate(angle=-33.1065, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-308', ))
mdb.models[modelname].rootAssembly.rotate(angle=108.8771, axisDirection=(0.83766,-0.5462,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-308', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-308', ), vector=(-0.22761,-0.85007,-0.15445))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-332', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-332', ))
mdb.models[modelname].rootAssembly.rotate(angle=7.7209, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-332', ))
mdb.models[modelname].rootAssembly.rotate(angle=101.8024, axisDirection=(0.99093,0.13435,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-332', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-332', ), vector=(-0.21991,-0.96351,-0.15262))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-333', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-333', ))
mdb.models[modelname].rootAssembly.rotate(angle=-33.0511, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-333', ))
mdb.models[modelname].rootAssembly.rotate(angle=94.6708, axisDirection=(0.83818,-0.54539,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-333', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-333', ), vector=(-0.21991,-0.96351,-0.15262))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-008', part=mdb.models[modelname].parts['RS-0s31781-0s27004'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-008', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-008', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-008', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-008', ), vector=(0,0,0))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-016', part=mdb.models[modelname].parts['RS-0s27004-0s23852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-016', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-016', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-016', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-016', ), vector=(0.056478,-0.070821,-0.042364))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-030', part=mdb.models[modelname].parts['RS-0s23852-0s21381'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-030', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-030', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-030', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-030', ), vector=(0.11296,-0.14164,-0.084729))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-039', part=mdb.models[modelname].parts['RS-0s21381-0s19301'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-039', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-039', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-039', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-039', ), vector=(0.16943,-0.21246,-0.12709))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-060', part=mdb.models[modelname].parts['RS-0s19301-0s17482'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-060', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-060', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-060', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-060', ), vector=(0.22591,-0.28328,-0.16946))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-081', part=mdb.models[modelname].parts['RS-0s17482-0s15852'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-081', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-081', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-081', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-081', ), vector=(0.28239,-0.3541,-0.21182))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-114', part=mdb.models[modelname].parts['RS-0s15852-0s14366'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-114', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-114', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-114', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-114', ), vector=(0.33887,-0.42492,-0.25419))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-150', part=mdb.models[modelname].parts['RS-0s14366-0s12994'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-150', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-150', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-150', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-150', ), vector=(0.39534,-0.49574,-0.29655))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-201', part=mdb.models[modelname].parts['RS-0s12994-0s11715'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-201', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-201', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-201', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-201', ), vector=(0.45182,-0.56656,-0.33891))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-255', part=mdb.models[modelname].parts['RS-0s11715-0s10515'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-255', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-255', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-255', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-255', ), vector=(0.5083,-0.63739,-0.38128))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-334', part=mdb.models[modelname].parts['RS-0s10515-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-334', ))
mdb.models[modelname].rootAssembly.rotate(angle=38.5714, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-334', ))
mdb.models[modelname].rootAssembly.rotate(angle=115.0648, axisDirection=(0.78183,0.62349,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-334', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-334', ), vector=(0.56478,-0.70821,-0.42364))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-031', part=mdb.models[modelname].parts['RS-0s10733-0s05956'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-031', ))
mdb.models[modelname].rootAssembly.rotate(angle=63.5599, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-031', ))
mdb.models[modelname].rootAssembly.rotate(angle=125.4964, axisDirection=(0.44526,0.8954,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-031', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-031', ), vector=(0.11296,-0.14164,-0.084729))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-046', part=mdb.models[modelname].parts['RS-0s05956-0s02804'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-046', ))
mdb.models[modelname].rootAssembly.rotate(angle=63.5599, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-046', ))
mdb.models[modelname].rootAssembly.rotate(angle=125.4964, axisDirection=(0.44526,0.8954,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-046', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-046', ), vector=(0.18585,-0.17789,-0.14279))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-072', part=mdb.models[modelname].parts['RS-0s02804-0s00333'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-072', ))
mdb.models[modelname].rootAssembly.rotate(angle=63.5599, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-072', ))
mdb.models[modelname].rootAssembly.rotate(angle=125.4964, axisDirection=(0.44526,0.8954,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-072', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-072', ), vector=(0.25875,-0.21414,-0.20086))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-088', part=mdb.models[modelname].parts['RS-0s00333-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-088', ))
mdb.models[modelname].rootAssembly.rotate(angle=63.5599, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-088', ))
mdb.models[modelname].rootAssembly.rotate(angle=125.4964, axisDirection=(0.44526,0.8954,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-088', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-088', ), vector=(0.33165,-0.25039,-0.25892))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-073', part=mdb.models[modelname].parts['RS-0s01262-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-073', ))
mdb.models[modelname].rootAssembly.rotate(angle=82.5544, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-073', ))
mdb.models[modelname].rootAssembly.rotate(angle=87.6602, axisDirection=(0.12959,0.99157,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-073', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-073', ), vector=(0.25875,-0.21414,-0.20086))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-061', part=mdb.models[modelname].parts['RS-0s08685-0s03908'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-061', ))
mdb.models[modelname].rootAssembly.rotate(angle=60.1504, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-061', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4811, axisDirection=(0.49772,0.86734,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-061', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-061', ), vector=(0.22591,-0.28328,-0.16946))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-095', part=mdb.models[modelname].parts['RS-0s03908-0s00756'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-095', ))
mdb.models[modelname].rootAssembly.rotate(angle=60.1504, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-095', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4811, axisDirection=(0.49772,0.86734,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-095', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-095', ), vector=(0.31058,-0.33187,-0.14778))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-136', part=mdb.models[modelname].parts['RS-0s00756-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-136', ))
mdb.models[modelname].rootAssembly.rotate(angle=60.1504, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-136', ))
mdb.models[modelname].rootAssembly.rotate(angle=77.4811, axisDirection=(0.49772,0.86734,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-136', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-136', ), vector=(0.39525,-0.38046,-0.12611))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-115', part=mdb.models[modelname].parts['RS-0s07133-0s02356'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-115', ))
mdb.models[modelname].rootAssembly.rotate(angle=67.2796, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-115', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.4431, axisDirection=(0.38623,0.9224,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-115', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-115', ), vector=(0.33887,-0.42492,-0.25419))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-180', part=mdb.models[modelname].parts['RS-0s02356-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-180', ))
mdb.models[modelname].rootAssembly.rotate(angle=67.2796, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-180', ))
mdb.models[modelname].rootAssembly.rotate(angle=123.4431, axisDirection=(0.38623,0.9224,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-180', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-180', ), vector=(0.41583,-0.45715,-0.3093))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-256', part=mdb.models[modelname].parts['RS-0s05272-0s00495'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-256', ))
mdb.models[modelname].rootAssembly.rotate(angle=30.0106, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-256', ))
mdb.models[modelname].rootAssembly.rotate(angle=151.6498, axisDirection=(0.86593,0.50016,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-256', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-256', ), vector=(0.5083,-0.63739,-0.38128))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-398', part=mdb.models[modelname].parts['RS-0s00495-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-398', ))
mdb.models[modelname].rootAssembly.rotate(angle=30.0106, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-398', ))
mdb.models[modelname].rootAssembly.rotate(angle=151.6498, axisDirection=(0.86593,0.50016,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-398', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-398', ), vector=(0.53205,-0.6785,-0.46929))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-335', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-335', ))
mdb.models[modelname].rootAssembly.rotate(angle=35.1978, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-335', ))
mdb.models[modelname].rootAssembly.rotate(angle=91.9684, axisDirection=(0.81717,0.5764,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-335', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-335', ), vector=(0.56478,-0.70821,-0.42364))

mdb.models[modelname].rootAssembly.Instance(dependent=ON, name='RSid-336', part=mdb.models[modelname].parts['RS-0s04732-0s00000'])
mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-336', ))
mdb.models[modelname].rootAssembly.rotate(angle=43.6185, axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-336', ))
mdb.models[modelname].rootAssembly.rotate(angle=138.0473, axisDirection=(0.72395,0.68985,0), axisPoint=(0.0, 0.0, 0.0), instanceList=('RSid-336', ))
mdb.models[modelname].rootAssembly.translate(instanceList=('RSid-336', ), vector=(0.56478,-0.70821,-0.42364))

# =========================================

# Root structure part and instance creation by merging all root segments
inst = mdb.models[modelname].rootAssembly.instances
mdb.models[modelname].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=[v for k, v in inst.items()], 
    keepIntersections=OFF, name='RootStruct', originalInstances=DELETE)

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

