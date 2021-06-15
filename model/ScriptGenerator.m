classdef ScriptGenerator < handle
    % Python script generator class for the automatic simulation in
    % Abaqus/CAE
    
    %% Class attributes
    properties (SetAccess = immutable)
        fileID                % Python script file identifier
        modelName  char       % Abaqus model name
        use3Delem             % Model root segments as 3D elements
        descr      char       % Optional simulation description
        rstruct    RootStruct % Root struct
        sim_params struct     % Simulation parameters
    end
    
    %% Instance methods
    methods
        %% Constructor and auxiliary methods
        function obj = ScriptGenerator(rs,sim_params,filename,modelname,use3Delem,description)
            % ScriptGenerator(rs,sim_params,filename,modelname,use3Delem) 
            % creates a handle to a ScriptGenerator object whose script 
            % will be saved as *filename*.py under the scripts folder with 
            % root struct rs and simulation parameters sim_params. In 
            % Abaqus the model name will be given by modelname.
            %
            % ScriptGenerator(rs,sim_params,filename,modelname,use3Delem,descr)
            % creates a handle to a ScriptGenerator object whose script 
            % will be saved as *filename*.py with root struct rs, 
            % simulation parameters sim_params and description descr in its
            % header. In Abaqus, the model name will be given by modelname.
            %
            % If use3Delem is true, the root segments are modelled as three
            % dimensional elements in Abaqus, otherwise, they are modelled
            % as one dimensional beams.
            
            if ispc
                filename = [pwd '\scripts\' filename '.py'];
            else
                filename = [pwd '/scripts/' filename '.py'];
            end
            [fileID,errmsg] = fopen(filename, 'w');
            
            if (fileID == -1)
                error(['Error creating file : ' errmsg]);
            end
            
            obj.fileID     = fileID;
            obj.use3Delem  = use3Delem;
            obj.rstruct    = rs;
            obj.sim_params = sim_params;
            obj.modelName  = modelname;
            if (nargin == 6)
                obj.descr  = description;
            end
        end
        
        %% Main methods
        function generateScript(obj)
            % Generates the full script for the complete simulation of the
            % root structure
            
            obj.writeHeader();
            obj.writeCreateSoil();
            obj.writeCreateRootMaterial();
            obj.writeCreateRigidBar();
            
            if(obj.use3Delem)
                obj.writeCreate3DRootSegments();
                obj.writeCreateInstanceCsys();
                obj.writeInstanceRootSegments();
                obj.writeMergeRootSegments();
                obj.writeAssignSectionToRootStruct();
                obj.writeInstanceSoil();
                obj.writeMergeSoilAndRootStruct();
                obj.writeInstanceRootSegmentForRigidBar();
            else
                obj.writeCreateRootSectionAndProfile();
                obj.writeCreate1DRootSegments();
                obj.writeMesh1DRoot();
                obj.writeInstanceSoil();
            end
            
            obj.closeFile();
        end
        
        function write(obj,str)
            % Writes a string to the end of the file script and jumps one
            % line
            fprintf(obj.fileID, [str newline]);
        end
        
        function closeFile(obj)
            % Closes the file handler
            status = fclose(obj.fileID);
            
            if (status == 1)
                error('Error closing the file.');
            end
        end
        
        function writeComment(obj,comment)
            % Writes comment lines to the file script. Comments can have
            % multiple lines given by 'newline'.
            
            str = ['# ' comment];
            for i = 1:length(str)
                if (str(i) == newline)
                    str = [str(1:i) '# ' str(i+1:end)];
                end
            end
            
            obj.write(str);
        end
        
        function writeHLine(obj)
            obj.writeComment('=========================================');
            obj.writeNewLines(1);
        end
        
        function writeNewLines(obj,n)
            % Writes n lines to the end of the script file
            
            for i = 1:n
                obj.write('');
            end
        end
        
        function writeHeader(obj)
            % Writes the script's header, which contains: date, simulation
            % description (given by the user), library imports, simulation
            % variables
            
            p = obj.sim_params;
            
            c = clock;
            str = ['Script automatically generated on ' date ' at ' ...
                   num2str(c(4)) ':' num2str(c(5)) ' by RootGen' ...
                   newline ...
                   'Simulation description: ' newline obj.descr];
            obj.writeComment(str);
            obj.writeNewLines(1);
               
            str = [ 'from part              import *' newline ...
                    'from material          import *' newline ...
                    'from section           import *' newline ...
                    'from assembly          import *' newline ...
                    'from step              import *' newline ...
                    'from interaction       import *' newline ...
                    'from load              import *' newline ...
                    'from mesh              import *' newline ...
                    'from optimization      import *' newline ...
                    'from job               import *' newline ...
                    'from sketch            import *' newline ...
                    'from visualization     import *' newline ...
                    'from connectorBehavior import *'];
            obj.write(str);
            obj.writeNewLines(1);
            
            obj.writeComment('Some of the variables of interest');
            str = ['modelname = ''' obj.modelName ''';'];
            obj.write(str);
            obj.write('mdb.models.changeKey(fromName=''Model-1'', toName=modelname)')
            
            obj.writeComment('Rigid bar variables');
            str = [ ...
                    'rigid_bar = {' newline ...
                        '\t"height"       : %.3f,' newline ...
                        '\t"lateralDispl" : %.3f,' newline ...
                    '}' newline
                  ];
            fprintf(obj.fileID,str,p.rigidBarHeight,p.rigidBarLateralDispl);
            
            obj.writeComment('Soil variables');
            str = [ ...
                    'soil = {' newline ...
                        '\t"Lx_Ly" : %.3f,' newline ...
                        '\t"depth" : %.3f,' newline ...
                        '\t"rho"   : %.3f,' newline ...
                        '\t"E"     : %.3f,' newline ...
                        '\t"nu"    : %.3f,' newline ...
                        '\t"phi"   : %.3f,' newline ...
                        '\t"psi"   : %.3f,' newline ...
                        '\t"c"     : %.3f,' newline ...
                        '\t"abs_plastic_strain" : %.3f' newline ...
                    '}' newline
                  ];
            fprintf(obj.fileID, str, ...
                p.soilLxLy, p.soilDepth, p.soilGamma/9.80655, p.soilE, ...
                p.soilV, p.soilPhi, p.soilPsi, p.soilC, 0);
            
            obj.writeComment('Root varaibles');
            str = [ ...
                    'root = {' newline ...
                        '\t"init_diam" : %.5f,' newline ...
                        '\t"seg_dl"    : %.3f,' newline ...
                        '\t"rho"       : %.3f,' newline ...
                        '\t"E"         : %.3f,' newline ...
                        '\t"nu"        : %.3f,' newline ...
                        '\t"sigma_r"   : %.3f,' newline ...
                        '\t"plastic_strain": %.3f' newline ...
                    '}' newline
                  ];
            fprintf(obj.fileID, str, ...
                obj.rstruct.global_lca.diam, obj.rstruct.params.dl , ...
                p.rootGamma/9.80655, p.rootE, p.rootV, p.rootMOR, 0);
            
            obj.writeHLine()
        end
        
        function writeCreateSoil(obj)
            % Soil sketch creation
            obj.writeComment('Soil part creation');
            
            str = [ ...
                'mdb.models[modelname].ConstrainedSketch(name=''__profile__'', sheetSize=20.0)' newline ...
                'mdb.models[modelname].sketches[''__profile__''].rectangle(point1=(0.0, 0.0), point2=(soil["Lx_Ly"], soil["Lx_Ly"]))' newline ...
                'mdb.models[modelname].Part(dimensionality=THREE_D, name=''Soil'', type=DEFORMABLE_BODY)' newline ...
                'mdb.models[modelname].parts[''Soil''].BaseSolidExtrude(depth=soil["depth"], sketch=' newline ...
                '    mdb.models[modelname].sketches[''__profile__''])' newline ...
                'del mdb.models[modelname].sketches[''__profile__'']' ...
                  ];
            obj.write(str);
            obj.writeHLine()
            
            % Soil material and section creation and assignment
            obj.writeComment('Soil material and section creation and assignment');
            
            str = [ ...
                    'mdb.models[modelname].Material(name=''SoilMaterial'')' newline ...
                    'mdb.models[modelname].materials[''SoilMaterial''].Density(table=((soil["rho"], ), ))' newline ...
                    'mdb.models[modelname].materials[''SoilMaterial''].Elastic(table=((soil["E"], soil["nu"]), ))' newline ...
                    'mdb.models[modelname].materials[''SoilMaterial''].MohrCoulombPlasticity(table=((soil["phi"], 0.0), ))' newline ...
                    'mdb.models[modelname].materials[''SoilMaterial''].mohrCoulombPlasticity.MohrCoulombHardening(table=((soil["c"], soil["abs_plastic_strain"]), ))' newline ...
                    'mdb.models[modelname].materials[''SoilMaterial''].mohrCoulombPlasticity.TensionCutOff(dependencies=0, table=((0.0, 0.0), ), temperatureDependency=OFF)' newline ...
                    'mdb.models[modelname].HomogeneousSolidSection(material=''SoilMaterial'', name=''SoilSection'', thickness=None)' newline ...
                    'mdb.models[modelname].parts[''Soil''].SectionAssignment(offset=0.0, offsetField=' newline ...
                    '    '''', offsetType=MIDDLE_SURFACE, region=Region(' newline ...
                    '    cells=mdb.models[modelname].parts[''Soil''].cells.findAt(((soil["Lx_Ly"]/2, soil["Lx_Ly"]/2, ' newline ...
                    '    soil["depth"]/2), ), )), sectionName=''SoilSection'', thicknessAssignment=FROM_SECTION)' ...
                  ];
            
            obj.write(str);
            obj.writeHLine()
        end
        
        function writeCreateInstanceCsys(obj)
            obj.writeComment('Creation of the coordinate system of the instance module');
            
            str = 'mdb.models[modelname].rootAssembly.DatumCsysByDefault(CARTESIAN)';
               
            obj.write(str);
            obj.writeHLine()
        end
        
        function writeInstanceSoil(obj)
            obj.writeComment('Soil instance and positioning');
            
            str = ['mdb.models[modelname].rootAssembly.Instance(dependent=ON, name=''Soil'', part=mdb.models[modelname].parts[''Soil''])' newline ...
                   'mdb.models[modelname].rootAssembly.translate(instanceList=(''Soil'', ), vector=(-soil["Lx_Ly"]/2, -soil["Lx_Ly"]/2, -3))'];
               
            obj.write(str);
            obj.writeHLine()
        end
        
        function writeCreateRootMaterial(obj)
            % Root material creation
            
            obj.writeComment('Root material creation');
            
            str = [ ...
                    'mdb.models[modelname].Material(name=''RootMaterial'')' newline ...
                    'mdb.models[modelname].materials[''RootMaterial''].Density(table=((root["rho"], ), ))' newline ...
                    'mdb.models[modelname].materials[''RootMaterial''].Elastic(table=((root["E"], root["nu"]), ))' newline ...
                    'mdb.models[modelname].materials[''RootMaterial''].Plastic(table=((root["sigma_r"], root["plastic_strain"]), ))' ...
                  ];
              
            if(obj.use3Delem)
                str = [str newline ...
                    'mdb.models[modelname].HomogeneousSolidSection(material=''RootMaterial'', name=''RootSection'', thickness=None)' ...
                    ];
            end
            
            obj.write(str);
            obj.writeHLine();
        end
        
        function writeCreate3DRootSegments(obj)
            % Root segments creation
            
            obj.writeComment('Root segments part creation');
            obj.writeComment('   - RS-1s234 : root segment with diameter 1.234 m, if not tapered');
            obj.writeComment(['   - RS-1s234-1s123 : root segment with initial diameter 1.234 m' newline ...
                                'and final diameter 1.123 m, if tapered']);

            if obj.sim_params.rootSegmentTaper
                % Root segments with variable cross section (w/ taper)
                
                diamPairs  = obj.rstruct.getDiamPairSet();
                nDiamPairs = length(diamPairs);
                
                for i = 1:nDiamPairs
                    d1  = diamPairs(i,1);
                    d2  = diamPairs(i,2);
                    str = ScriptGenerator.getTaperedRootSegmentPartCreationStr(d1, d2);
                       
                    obj.write(str);
                    if (i < nDiamPairs)
                        obj.writeNewLines(1);
                    end
                end
            else
                % Root segments with constant cross section (no taper)
                
                diams  = obj.rstruct.getDiamSet();
                nDiams = length(diams);
                for i = 1:nDiams
                    % Root segment part names are distinguished by their
                    % diameters (e.g. root segment has diameter 1.234
                    % => its part name will be RS-1s234)
                    d = diams(i);
                    
                    strDiam      = sprintf('%.5f', d);
                    strPartName  = sprintf('RS-%ds%s', floor(d), strDiam(3:end));

                    str = [ ...
                            'mdb.models[modelname].ConstrainedSketch(name=''__profile__'', sheetSize=10.0)' newline ...
                            'mdb.models[modelname].sketches[''__profile__''].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))' newline ...
                            'mdb.models[modelname].sketches[''__profile__''].FixedConstraint(entity=mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                            'mdb.models[modelname].sketches[''__profile__''].rectangle(point1=(0.0, 0.0), point2=(' strDiam '/2, root["seg_dl"]))' newline ...
                            'mdb.models[modelname].Part(dimensionality=THREE_D, name=''' strPartName ''', type=DEFORMABLE_BODY)' newline ...
                            'mdb.models[modelname].parts[''' strPartName '''].BaseSolidRevolve(angle=360.0, ' newline ...
                            '    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches[''__profile__''])' newline ...
                            'del mdb.models[modelname].sketches[''__profile__'']' ...
                          ];

                    obj.write(str);
                    if (i < nDiams)
                        obj.writeNewLines(1);
                    end
                end
            end            

            obj.writeHLine()
        end
        
        function writeCreateRootSectionAndProfile(obj)
            % This method is only required if the root segments are
            % modelled as one dimensional beam elements
            
            obj.writeComment('Root segments section and profile creation');
            obj.writeComment('   - P-1s234 : root segment profile with diameter 1.234 m');
            obj.writeComment('   - S-1s234 : root segment section with diameter 1.234 m');
            
            diams  = obj.rstruct.getDiamSet();
            nDiams = numel(diams);
            
            for i = 1:nDiams
                % Section and profile names are distinguished by their
                % diameters (e.g. root segment has diameter 1.234 =>
                % Profile name: P-1s234 and
                % Section name: S-1s234)
                diam = diams(i);
                strRadius  = sprintf('%.5f', diam/2);
                strProfile = Node.getProfileNameFromDiam(diam);
                strSection = Node.getSectionNameFromDiam(diam);
                
                str = [ ...
                        'mdb.models[modelname].CircularProfile(name=''' strProfile ''', r=' strRadius ')' newline ...
                        'mdb.models[modelname].BeamSection(consistentMassMatrix=False, integration=' newline ...
                        '    DURING_ANALYSIS, material=''RootMaterial'', name=''' strSection ''', poissonRatio=' newline ...
                        '    0.0, profile=''' strProfile ''', temperatureVar=LINEAR)' ...
                      ];

                obj.write(str);
                if (i < nDiams)
                    obj.writeNewLines(1);
                end
            end
            
            obj.writeHLine();
        end
        
        function writeCreateNodeDatumPoints(obj,axe)
            % Recursive method that writes in the python script the code 
            % for creating the datum points corresponding to each node
            
            p = axe.lca;
            
            while(~isempty(p))
                obj.write(ScriptGenerator.createDatumPointStr(p));
                
                if (isa(p,'ForkedNode'))
                    if (~isempty(p.left))
                        obj.writeCreateNodeDatumPoints(p.left.axe);
                    end
                    if (~isempty(p.right))
                        obj.writeCreateNodeDatumPoints(p.right.axe);
                    end
                end
                if (~isempty(p.ramif))
                    for i = 1:length(p.ramif)
                        obj.writeCreateNodeDatumPoints(p.ramif(i).axe);
                    end
                end
                
                p = p.next;
            end
        end
        
        function writeCreateInternodes(obj,axe)
            % Auxiliary recursive method that writes in the python script
            % the code for assigning the section and beam section
            % orientation for each axe
            
            p = axe.lca;
            
            while(~isempty(p.next))
                obj.write(ScriptGenerator.createWireStr(p,p.next));
                obj.write(ScriptGenerator.assingSectionStr(p,p.next));
                
                if (isa(p.next,'ForkedNode'))
                    if (~isempty(p.next.left))
                        obj.writeCreateInternodes(p.next.left.axe);
                    end
                    if (~isempty(p.next.right))
                        obj.writeCreateInternodes(p.next.right.axe);
                    end
                end
                if (~isempty(p.next.ramif))
                    for i = 1:length(p.next.ramif)
                        obj.writeCreateInternodes(p.next.ramif(i).axe);
                    end
                end
                
                p = p.next;
            end
        end
        
        function writeCreate1DRootSegments(obj)
            % Root segments creation
            
            obj.writeComment('Root segment part creation');
            
            str = ['mdb.models[modelname].Part(dimensionality=THREE_D, name=''Root'', type=DEFORMABLE_BODY)' newline newline ...
                   'rootpart = mdb.models[modelname].parts[''Root'']' newline ...
                   'rootpart.ReferencePoint(point=(0.0, 0.0, 0.0))' newline ...
                   ];
               
            obj.write(str);
            
            iAxis = obj.rstruct.global_lca.initAxis;
            
            obj.writeComment('Node datum points creation');
            for i = 1:numel(iAxis)
                obj.writeCreateNodeDatumPoints(iAxis(i));
            end
            
            obj.writeNewLines(1);
            obj.writeComment('Internodes creation');
            for i = 1:numel(iAxis)
                obj.writeCreateInternodes(iAxis(i));
            end
            
            obj.writeHLine()
        end
        
        function writeMesh1DRoot(obj)
            obj.writeComment('Root structure meshing');
            
            dl = num2str(obj.rstruct.params.dl);
            
            str = [ ...
                    'root.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=' dl ')' newline ...
                    'root.generateMesh()' ...
                  ];
              
            obj.write(str);
            obj.writeHLine();
        end
        
        function writeInstanceRootSegmentForRigidBar(obj)
            obj.writeComment('Auxiliary root segment instance for fixing rigid bar onto');
            
            partName = obj.rstruct.global_lca.getPartName(obj.sim_params.rootSegmentTaper);
            assemblyName = 'AuxiliaryRootStruct';
            
            str = [ ...
                    'mdb.models[modelname].rootAssembly.Instance(dependent=ON, name=''' assemblyName ''', part=mdb.models[modelname].parts[''' partName '''])' newline ...
                    'mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=(''' assemblyName ''', ))' newline ...
                    'mdb.models[modelname].parts[''' partName '''].Surface(name=''RootTopSurf'', ' newline ...
                    '    side1Faces=mdb.models[modelname].parts[''' partName '''].faces.findAt(((0.0, root["seg_dl"], 0.0), )))' newline ...
                   ];
               
            obj.write(str);
            obj.writeHLine();
        end
        
        function writeMergeAuxiliaryRootSegment(obj)
            
        end
        
        function writeInstanceRootSegments(obj)
            obj.writeComment('Root segments instancing and positioning');
            
            x = RootStruct.x_glb;
            for i = 1:length(obj.rstruct.global_lca.initAxis)
                axe = obj.rstruct.global_lca.initAxis(i);
                pos = axe.getPositioningStruct();
                
                % For each descendant axe of initAxis(i)
                for j = 1:length(pos)
                    alpha = pos(j).alpha;
                    beta  = pos(j).beta;
                    nodes = pos(j).nodes;

                    % Rotation matrix of angle alpha about the z-axis
                    R = [[cos(alpha) -sin(alpha) 0]; [sin(alpha) cos(alpha) 0]; [0 0 1]];
                    % Coordinates of the new x-axis after the rotation about the z-axis by angle alpha
                    x_dir_alpha = R*x';

                    x_dir_alpha_str = ['(' num2str(x_dir_alpha(1)) ',' num2str(x_dir_alpha(2)) ',' num2str(x_dir_alpha(3)) ')'];
                    alpha = (180/pi)*alpha;
                    beta  = (180/pi)*beta;

                    for k = 1:length(nodes)
                        partName     = nodes(k).getPartName(obj.sim_params.rootSegmentTaper);
                        assemblyName = nodes(k).getAssemblyName();
                        transVector  = ['(' num2str(nodes(k).coord(1)) ',' num2str(nodes(k).coord(2)) ',' num2str(nodes(k).coord(3)) ')'];

                        str = [ ...
                            'mdb.models[modelname].rootAssembly.Instance(dependent=ON, name=''' assemblyName ''', part=mdb.models[modelname].parts[''' partName '''])' newline ...
                            'mdb.models[modelname].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=(''' assemblyName ''', ))' newline ...
                            'mdb.models[modelname].rootAssembly.rotate(angle=' num2str(alpha) ', axisDirection=(0.0, 0.0, 1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=(''' assemblyName ''', ))' newline ...
                            'mdb.models[modelname].rootAssembly.rotate(angle=' num2str(beta)  ', axisDirection=' x_dir_alpha_str ', axisPoint=(0.0, 0.0, 0.0), instanceList=(''' assemblyName ''', ))' newline ...
                            'mdb.models[modelname].rootAssembly.translate(instanceList=(''' assemblyName ''', ), vector=' transVector ')' newline ...
                          ];
                      
                        obj.write(str);
                    end
                end
            end

            obj.writeHLine()
        end
        
        function writeCreateRigidBar(obj)
            obj.writeComment('Rigid bar creation');

            str = [ ...
                    'mdb.models[modelname].ConstrainedSketch(name=''__profile__'', sheetSize=10.0)' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].rectangle(point1=(0.0, 0.0), point2=(root["init_diam"]/2, rigid_bar["height"]))' newline ...
                    'mdb.models[modelname].Part(dimensionality=THREE_D, name=''RigidBar'', type=DISCRETE_RIGID_SURFACE)' newline ...
                    'mdb.models[modelname].parts[''RigidBar''].BaseSolidRevolve(angle=360.0, ' newline ...
                    '    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches[''__profile__''])' newline ...
                    'del mdb.models[modelname].sketches[''__profile__'']' ...
                  ];

            obj.write(str);
            obj.writeHLine()
            
            obj.writeComment('Rigid bar reference point, interesting points and surfaces creation');
            
            str = [ ...
                    'mdb.models[modelname].parts[''RigidBar''].ReferencePoint(point=(0.0, 0.0, 0.0))' newline newline ...
                    'mdb.models[modelname].parts[''RigidBar''].PartitionFaceByShortestPath(faces=' newline ...
                    '    mdb.models[modelname].parts[''RigidBar''].faces.findAt(((0.0, rigid_bar["height"], 0.0), )), ' newline ...
                    '    point1=(-root["init_diam"]/2,rigid_bar["height"],0.0), point2=(root["init_diam"]/2,rigid_bar["height"],0.0))' newline ...
                    'mdb.models[modelname].parts[''RigidBar''].PartitionEdgeByPoint(edge=' newline ...
                    '    mdb.models[modelname].parts[''RigidBar''].edges.findAt((0.0, rigid_bar["height"], 0.0), ), point=(0.0, rigid_bar["height"], 0.0))' newline newline ...
                    'mdb.models[modelname].parts[''RigidBar''].Surface(name=''RigidBarBottomSurf'', ' newline ...
                    '    side1Faces=mdb.models[modelname].parts[''RigidBar''].faces.findAt(((0.0, 0.0, 0.0), )))' ...
                   ];
               
            obj.write(str);
            obj.writeHLine()
            
            obj.writeComment('Transform into a shell element');
            
            str = 'mdb.models[modelname].parts[''RigidBar''].RemoveCells(cellList=mdb.models[modelname].parts[''RigidBar''].cells)';
            
            obj.write(str);
            obj.writeHLine()
        end
        
        function writeMergeRootSegments(obj)
            obj.writeComment('Root structure part and instance creation by merging all root segments');
            
            str = [ ...
                    'inst = mdb.models[modelname].rootAssembly.instances' newline ...
                    'mdb.models[modelname].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, ' newline ...
                    '    instances=[v for k, v in inst.items()], ' newline ...
                    '    keepIntersections=OFF, name=''RootStruct'', originalInstances=DELETE)' newline ...
                   ];
               
            obj.write(str);
            obj.writeHLine()
        end
        
        function writeAssignSectionToRootStruct(obj)
            obj.writeComment('Root structure section assignment');
            
            str = [...
                    'mdb.models[modelname].parts[''RootStruct''].SectionAssignment(offset=0.0, ' newline ...
                    '    offsetField='''', offsetType=MIDDLE_SURFACE, region=Region(cells=mdb.models[modelname].parts[''RootStruct''].cells),' newline ...
                    '    sectionName=''RootSection'', thicknessAssignment=FROM_SECTION)' newline ...
                   ];
            
            obj.write(str);
            obj.writeHLine()
        end
        
        function writeMergeSoilAndRootStruct(obj)
            obj.writeComment('Soil structure part and instance creation by merging root structure and soil');
            
            str = [ ...
                    'mdb.models[modelname].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, ' newline ...
                    '    instances=(mdb.models[modelname].rootAssembly.instances[''RootStruct-1''], ' newline ...
                    '               mdb.models[modelname].rootAssembly.instances[''Soil'']), ' newline ...
                    'keepIntersections=ON, name=''SoilStructure'', originalInstances=DELETE)' newline ...
                   ];
               
            obj.write(str);
            obj.writeHLine()
        end
    end
    
    %% Static methods
    methods(Static)
        function str = getTaperedRootSegmentPartCreationStr(d1, d2)
            % Method that retunrs the corresponding str of commands to
            % generate a root segment part with initial diameter d1 and
            % final diameter of d2. It also resolves for singularity.
            % Singularity happens when root segment corresponds to the last
            % one in the axe bearing it (next diameter does not exist =>
            % set to zero => degenerated line in sketch)
            
            strDiam1     = sprintf('%.5f', d1);
            strDiam2     = sprintf('%.5f', d2);
            strPartName  = sprintf('RS-%ds%s-%ds%s', floor(d1), strDiam1(3:end), floor(d2), strDiam2(3:end));

            if (d2 == 0)
                str = [ ...
                        'mdb.models[modelname].ConstrainedSketch(name=''__profile__'', sheetSize=20.0)' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].FixedConstraint(entity=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].Line(point1=(0.0, 0.0), point2=(' strDiam1 '/2, 0.0))' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].HorizontalConstraint(' newline ...
                        '    addUndoState=False, entity=mdb.models[modelname].sketches[''__profile__''].geometry[3])' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].PerpendicularConstraint(addUndoState=False, entity1=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].geometry[2], entity2=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].geometry[3])' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].CoincidentConstraint(addUndoState=False, entity1=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].vertices[0], entity2=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].Line(point1=(' strDiam1 '/2, 0.0), point2=(0.0, root["seg_dl"]))' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].CoincidentConstraint(addUndoState=False, entity1=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].vertices[2], entity2=' newline ...
                        '    mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))' newline ...
                        'mdb.models[modelname].sketches[''__profile__''].VerticalConstraint(' newline ...
                        '    addUndoState=False, entity=mdb.models[modelname].sketches[''__profile__''].geometry[5])' newline ...
                        'mdb.models[modelname].Part(dimensionality=THREE_D, name=''' strPartName ''', type=DEFORMABLE_BODY)' newline ...
                        'mdb.models[modelname].parts[''' strPartName '''].BaseSolidRevolve(angle=360.0, ' newline ...
                        '    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches[''__profile__''])' newline ...
                        'del mdb.models[modelname].sketches[''__profile__'']' newline ...
                       ];
            else
                str = [ ...
                    'mdb.models[modelname].ConstrainedSketch(name=''__profile__'', sheetSize=10.0)' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].FixedConstraint(entity=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].Line(point1=(0.0, 0.0), point2=(' strDiam1 '/2, 0.0))' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].HorizontalConstraint(addUndoState=False, entity=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[3])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].PerpendicularConstraint(addUndoState=False, entity1=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[2], entity2=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[3])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].CoincidentConstraint(addUndoState=False, entity1=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].vertices[0], entity2=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].Line(point1=(' strDiam1 '/2, 0.0), point2=(' strDiam2 '/2, root["seg_dl"]))' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].Line(point1=(' strDiam2 '/2, root["seg_dl"]), point2=(0.0, root["seg_dl"]))' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].HorizontalConstraint(addUndoState=False, entity=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[5])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].CoincidentConstraint(addUndoState=False, entity1=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].vertices[3], entity2=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[2])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].Line(point1=(0.0, root["seg_dl"]), point2=(0.0, 0.0))' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].VerticalConstraint(addUndoState=' newline ...
                    '    False, entity=mdb.models[modelname].sketches[''__profile__''].geometry[6])' newline ...
                    'mdb.models[modelname].sketches[''__profile__''].PerpendicularConstraint(' newline ...
                    '    addUndoState=False, entity1=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[5], entity2=' newline ...
                    '    mdb.models[modelname].sketches[''__profile__''].geometry[6])' newline ...
                    'mdb.models[modelname].Part(dimensionality=THREE_D, name=''' strPartName ''', type=DEFORMABLE_BODY)' newline ...
                    'mdb.models[modelname].parts[''' strPartName '''].BaseSolidRevolve(angle=360.0, ' newline ...
                    '    flipRevolveDirection=OFF, sketch=mdb.models[modelname].sketches[''__profile__''])' newline ...
                    'del mdb.models[modelname].sketches[''__profile__'']' newline ...
                   ];
            end
        end
        
        function str = createDatumPointStr(node)
            name = node.getFeatureName();
            x = node.coord(1); x = num2str(x);
            y = node.coord(2); y = num2str(y);
            z = node.coord(3); z = num2str(z);
            str = ['rootpart.DatumPointByCoordinate(coords=(' x ',' y ',' z '))' newline ...
                   'rootpart.features.changeKey(fromName=''Datum pt-1'', toName=''' name ''')'];
        end
        
        function str = createWireStr(node1,node2)
            name1 = node1.getFeatureName();
            name2 = node2.getFeatureName();
            
            str = [ ...
                      'rootpart.WirePolyLine(mergeType=IMPRINT, meshable=ON,' newline ...
                      '    points=((root.datums[root.features[''' name1 '''].id], root.datums[root.features[''' name2 '''].id]),))' newline ...
                      'rootpart.features.changeKey(fromName=''Wire-1'', toName=''' name1 name2 ''')' newline ...
                  ];
        end
        
        function str = assingSectionStr(node1,node2)
            featEdge = [node1.getFeatureName() node2.getFeatureName()];
            
            dir = node2.axe.getOrthogonalDirection();
            x = num2str(dir(1));
            y = num2str(dir(2));
            z = num2str(dir(3));
            ortDir = ['(' x ',' y ',' z ')'];
            sectionStr = node1.getSectionName();
            
            str = [ ...
                    'reg = Region(edges = root.getFeatureEdges(''' featEdge '''))' newline ...
                    'rootpart.assignBeamSectionOrientation(method=N1_COSINES, n1=' ortDir ', region=reg)' newline ...
                    'rootpart.SectionAssignment(offset=0.0, offsetField='''', offsetType=MIDDLE_SURFACE,' newline ...
                    '    region=reg, sectionName=''' sectionStr ''', thicknessAssignment=FROM_SECTION)' newline ...
                  ];
        end
    end
end