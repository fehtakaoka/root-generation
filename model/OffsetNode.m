classdef OffsetNode < Node
    % OffsetNode represents an internal 'virtual' node inside an axe so that the
    % first node of the ramification starts growing outside the bearing axe
    %
    % Note: due to the fact that this node doesn't correspond to a physical
    % node in the structure (its purpose is to position the begining of the
    % ramification properly), it isn't the axe lca. The next node is the
    % lca.
    
    %% Class attributes
    properties
        % len - Length of the offset internode. It corresponds to the
        % radius of the parent node.
        len  double
    end
    
    %% Class methods
    methods
        function obj = OffsetNode(rootStruct_, axe_, coord_)
            obj@Node(rootStruct_, axe_, coord_);
            obj.len = 0;
        end
        
        function updateGeometry(obj,coord_,diam_,len_)
            obj.coord = coord_;
            obj.diam  = diam_;
            obj.len   = len_;
        end
    end
end