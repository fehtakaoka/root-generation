classdef TapRoot < Axe
    % Taproot class
    %
    
    properties (SetAccess = private)
        branches logical % Whether or not it branches
        hasTaper logical % Whether or not it has taper
    end
    methods
        function obj = TapRoot(rootStruct_,branches_,hasTaper_)
            obj@Axe(rootStruct_,1,[0,0,-1],'global_lca',true);
            obj.branches = branches_;
            obj.hasTaper = hasTaper_;
        end
    end
end