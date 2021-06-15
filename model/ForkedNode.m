classdef ForkedNode < Node
    % Forked node of the axe
    
    %% Class attributes
    properties
        left  Node      % Left node
        right Node      % Right node
    end
    
    %% Class methods
    methods
        function obj = ForkedNode(rootStruct_, axe_, coord_)
            obj@Node(rootStruct_, axe_, coord_);
            obj.left = Node.empty;
            obj.left = Node.empty;
        end
    end
end