# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

# Some of the variables of interest
modelname = 'ModeloTeste';
mdb.models.changeKey(fromName='Model-1', toName=modelname)
# Soil variables
soil = {
	"Lx_Ly" : 5.000,
	"depth" : 3.000,
	"rho"   : 2000.000,
	"E"     : 20000000.000,
	"nu"    : 0.300,
	"phi"   : 0.436,
	"psi"   : 0.000,
	"c"     : 1500.000,
	"abs_plastic_strain" : 0.000
}
# Root varaibles
root = {
	"init_diam" : 1.000,
	"seg_dl"    : 2.000,
	"rho"       : 4800.000,
	"E"         : 2000000000.000,
	"nu"        : 0.300,
	"sigma_r"   : 15000000.000,
	"plastic_strain": 0.000
}
# =========================================

# Soil sketch creation
mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models[modelname].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(soil['Lx_Ly'], soil['Lx_Ly']))
mdb.models[modelname].Part(dimensionality=THREE_D, name='Soil', type=
    DEFORMABLE_BODY)
mdb.models[modelname].parts['Soil'].BaseSolidExtrude(depth=soil['depth'], sketch=
    mdb.models[modelname].sketches['__profile__'])
del mdb.models[modelname].sketches['__profile__']
# =========================================================================================

# Creating datum point to reference the defined origin (middle of the top surfacce of the soil)
mdb.models[modelname].parts['Soil'].DatumPointByCoordinate(coords=
    (soil['Lx_Ly']/2, soil['Lx_Ly']/2, soil['depth']))
mdb.models[modelname].parts['Soil'].features.changeKey(fromName='Datum pt-1', 
    toName='DefinedOrigin')
# =========================================================================================

# Soil material and section creation and assignment
mdb.models[modelname].Material(name='SoilMaterial')
mdb.models[modelname].materials['SoilMaterial'].Density(table=((2000.0, ), ))
mdb.models[modelname].materials['SoilMaterial'].Elastic(table=((20000000.0, 
    0.3), ))
mdb.models[modelname].materials['SoilMaterial'].MohrCoulombPlasticity(table=((
    0.437, 0.0), ))
mdb.models[modelname].materials['SoilMaterial'].mohrCoulombPlasticity.MohrCoulombHardening(
    table=((1500.0, 0.0), ))
mdb.models[modelname].materials['SoilMaterial'].mohrCoulombPlasticity.TensionCutOff(
    dependencies=0, table=((0.0, 0.0), ), temperatureDependency=OFF)
mdb.models[modelname].HomogeneousSolidSection(material='SoilMaterial', name=
    'SoilSection', thickness=None)
mdb.models[modelname].parts['Soil'].SectionAssignment(offset=0.0, offsetField=
    '', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models[modelname].parts['Soil'].cells.findAt(((soil['Lx_Ly']/2, soil['Lx_Ly']/2, 
    soil['depth']/2), ), )), sectionName='SoilSection', thicknessAssignment=FROM_SECTION)
# =========================================================================================

# Root material creation
mdb.models[modelname].Material(name='RootMaterial')
mdb.models[modelname].materials['RootMaterial'].Density(table=((4800.0, ), ))
mdb.models[modelname].materials['RootMaterial'].Elastic(table=((2000000000.0, 0.49),))
# =========================================================================================

# Root nodes creation
mdb.models[modelname].Part(dimensionality=THREE_D, name='Root', type=
    DEFORMABLE_BODY)

root = mdb.models[modelname].parts['Root']
root.ReferencePoint(point=(0.0, 0.0, 0.0))

root.DatumPointByCoordinate(coords=(0.0,0.0,0.0))
root.features.changeKey(fromName='Datum pt-1', toName='b1')

root.DatumPointByCoordinate(coords=(0.0,0.0,-0.5))
root.features.changeKey(fromName='Datum pt-1', toName='b2')
root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b1'].id], root.datums[root.features['b2'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b1b2')
reg = Region(edges = root.getFeatureEdges('b1b2'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0.0, 1.0, 0.0), region=reg)
mdb.models[modelname].CircularProfile(name='Circ1', r=0.1)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='BSection1', poissonRatio=
    0.0, profile='Circ1', temperatureVar=LINEAR)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='BSection1', thicknessAssignment=FROM_SECTION)

root.DatumPointByCoordinate(coords=(0.0,0.0,-1.0))
root.features.changeKey(fromName='Datum pt-1', toName='b3')
root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b2'].id], root.datums[root.features['b3'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b2b3')
reg = Region(edges = root.getFeatureEdges('b2b3'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0.0, 1.0, 0.0), region=reg)
mdb.models[modelname].CircularProfile(name='Circ1', r=0.1)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='BSection1', poissonRatio=
    0.0, profile='Circ1', temperatureVar=LINEAR)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='BSection1', thicknessAssignment=FROM_SECTION)

root.DatumPointByCoordinate(coords=(0.0,0.0,-1.5))
root.features.changeKey(fromName='Datum pt-1', toName='b4')
root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b3'].id], root.datums[root.features['b4'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b3b4')
reg = Region(edges = root.getFeatureEdges('b3b4'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0.0, 1.0, 0.0), region=reg)
mdb.models[modelname].CircularProfile(name='Circ1', r=0.1)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='BSection1', poissonRatio=
    0.0, profile='Circ1', temperatureVar=LINEAR)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='BSection1', thicknessAssignment=FROM_SECTION)

root.DatumPointByCoordinate(coords=(0.5,0.0,-0.5))
root.features.changeKey(fromName='Datum pt-1', toName='b5')
root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b2'].id], root.datums[root.features['b5'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b2b5')
reg = Region(edges = root.getFeatureEdges('b2b5'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(0.0, 1.0, 0.0), region=reg)
mdb.models[modelname].CircularProfile(name='Circ2', r=0.05)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='BSection2', poissonRatio=
    0.0, profile='Circ2', temperatureVar=LINEAR)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='BSection2', thicknessAssignment=FROM_SECTION)

root.DatumPointByCoordinate(coords=(0.0,0.5,-1.0))
root.features.changeKey(fromName='Datum pt-1', toName='b6')
root.WirePolyLine(mergeType=IMPRINT, meshable=ON,
    points=((root.datums[root.features['b3'].id], root.datums[root.features['b6'].id]),))
root.features.changeKey(fromName='Wire-1', toName='b3b6')
reg = Region(edges = root.getFeatureEdges('b3b6'))
root.assignBeamSectionOrientation(method=N1_COSINES, n1=(1.0, 0.0, 0.0), region=reg)
mdb.models[modelname].CircularProfile(name='Circ2', r=0.05)
mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='RootMaterial', name='BSection2', poissonRatio=
    0.0, profile='Circ2', temperatureVar=LINEAR)
root.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
    region=reg, sectionName='BSection2', thicknessAssignment=FROM_SECTION)