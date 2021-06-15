classdef GlbLCA < Node
    % Global LCA node of the root structure
    % Necessary so that the exported files won't have ambiguities. Also, it
    % has no defined axe bearing it
    
    %% Class attributes
    properties (SetAccess = private)
        initAxis Axe    % List of all initial axis of the root structure
    end
    properties (Access = private)
        counter = 0;    % Counter to avoid creation of creation of two lcas
    end
    
    %% Class methods
    methods
        function obj = GlbLCA(rootStruct_, axe_, coord_)
            obj@Node(rootStruct_, axe_, coord_);
            obj.counter = obj.counter + 1;
            if obj.counter > 1
                error('A root structure cannot have more than one global LCA.');
            end
            obj.initAxis = axe_;
        end
        
        function appendInitAxe(obj,axe)
            obj.initAxis(end+1) = axe;
        end
    end
end