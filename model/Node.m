classdef Node < handle & matlab.mixin.Heterogeneous
    % Node class (components of axe)
    
    %% Class attributes
    properties (SetAccess = immutable)
        % id - Indentification/index within the root structure
        id         uint32
        rootStruct RootStruct % Root structure bearing the axe
        axe        Axe        % Axe to which it belongs
    end
    properties
        coord      double     % Absolute coordinate of the node
    end
    properties
        next       Node       % Next node in the axe (operation '<')
        ramif      Node       % Ramification node (operation '+')
        killed     logical    % Flag to indicate the death of an apex
        % diam - Diameter of the axe at that node (= -1, if it is not yet 
        % calculated - calculation of the diameter is done at the end of
        % the growing process)
        diam       double
    end
    
    %% Class methods
    methods
        %% Constructor
        function obj = Node(rootStruct_, axe_, coord_)
            % Constructor of the class Node:
            % List of parameters (rootStruct_, axe_, coord_):
            %   - rootStruct_ : root structure bearing the node
            %   - axe_        : axe bearing the node
            %   - coord_      : coordinates where the node will be placed
            obj.id         = 0;
            if ~isempty(rootStruct_)
                obj.id     = getNewNodeIndex(rootStruct_);
            end
            obj.rootStruct = rootStruct_;
            obj.axe        = axe_;
            obj.next       = Node.empty;
            obj.coord      = coord_;
            obj.ramif      = Node.empty;
            obj.killed     = false;
            obj.diam       = -1;
        end
        
        %% Getters and setters
        function set.coord(obj,pos)
            [r,c] = size(pos);
            if r == 1 && c == 3 && isa(pos,'double')
                 obj.coord = pos;
            else
                error(['Property ''coord'' must be an 1x3 double ' ...
                      'array']);
            end
        end
        
        %% Auxiliary methods
        function dist = getDistance(obj,node2)
            % Method that returns the euclidiean distance between two nodes
            %
            % See also GETDISTANCEFROMPOS
            
            node1 = obj;
            dist = node1.coord - node2.coord;
            dist = norm(dist);
        end
        
        function dist = getDistanceFromPos(obj,pos)
            % Method that returns the euclidiean distance between the 
            % current node and the position pos [x y z]
            %
            % See also GETDISTANCE
            
            dist = obj.coord - pos;
            dist = norm(dist);
        end
        
        function killApex(obj)
            % Method that marks the apex to be killed (won't grown anymore)
            obj.killed = true;
        end
        
        %% Display methods
        function str = toStr(obj)
            % Method that returns the string containing the node's id
            str = ['b' num2str(obj.id) '{' num2str(obj.diam) '}'];
        end
        
        function plot(obj,nodeColor)
            scatter3(obj.coord(1),obj.coord(2),obj.coord(3), 75, ...
                         'MarkerEdgeColor','k', ...
                         'MarkerFaceColor',nodeColor)
        end
        
        function str = getFeatureName(obj)
            % getFeatureName returns the string identifying the current
            % node in the list of features of the root struct in Abaqus
            % Format: b*id* (e.g. b12)
            
            str = ['b' num2str(obj.id)];
        end
        
        function str = getProfileName(obj)
            % getProfileNameWithDiam(diam) returns the string containing 
            % the profile name of the internode with diameter 'diam'
            % according to the syntax convention. For usage in Abaqus.
            %
            % - Syntax convention:
            % Section and profile names are distinguished by their
            % diameters (e.g. root segment has diameter 1.234 =>
            % Profile name: P-1s234 and
            % Section name: S-1s234)
            
            str = Node.getProfileNameFromDiam(obj.diam);
        end
        
        function str = getSectionName(obj)
            % getSectionName() returns the string containing the section
            % name of the internode started by the current node according 
            % to the syntax convention. For usage in Abaqus.
            %
            % - Syntax convention:
            % Section and profile names are distinguished by their
            % diameters (e.g. root segment has diameter 1.234 =>
            % Profile name: P-1s234 and
            % Section name: S-1s234)
            
            str = Node.getSectionNameFromDiam(obj.diam);
        end
        
        function str = getPartName(obj,taper)
            % getPartName(taper) returns the string containing the part
            % name of the current node according to the syntax convention
            % for tapered or not tapered root segments. For usage in Abaqus.
            
            % Syntax convention:
            % Root segment part names are distinguished by their diameters
            % (e.g. root segment has diameter 1.234 => its part name will 
            % be RS-1s234, if not tapered; root segment has initial 
            % diameter 1.234 and final diameter 1.123 => its part name will
            % be RS-1s234-1s123)
            
            d1 = obj.diam;
            if(obj.diam > 0)
                strDiam1 = sprintf('%.5f', d1);
                if taper
                    if ~isempty(obj.next)
                        d2 = obj.next.diam;
                    else
                        d2 = 0;
                    end
                    strDiam2 = sprintf('%.5f', d2);
                    str = sprintf('RS-%ds%s-%ds%s', floor(d1), strDiam1(3:end), floor(d2), strDiam2(3:end));
                else
                    str = sprintf('RS-%ds%s', floor(d1), strDiam1(3:end));
                end
            else
                error('Error: attempt to obtain root segment part name without assigned diameter.');
            end
        end
        
        function str = getAssemblyName(obj)
            str = sprintf('%0*d', numel(num2str(obj.rootStruct.glbNodeIndex)), obj.id);
            str = ['RSid-' str];
        end
    end
    
    %% Static methods
    methods(Static)
        function str = getProfileNameFromDiam(diam)
            % See also getProfileName()
            
            strDiam = sprintf('%.5f', diam);
            str = sprintf('P-%ds%s', floor(diam), strDiam(3:end));
        end
        
        function str = getSectionNameFromDiam(diam)
            % See also getSectionName()
            
            str = Node.getProfileNameFromDiam(diam);
            str = ['S' str(2:end)];
        end
    end
end