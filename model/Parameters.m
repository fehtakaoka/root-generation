classdef Parameters < handle
    % Parameters class for the root structure: consists of all parameters
    % necessary to define a root structure and theirs associated methods.
    % Default values were taken from the heart-like root system.
    %
    % Parameters Properties:
    %     n_laterals - Number of main lateral roots
    %                  default value: 7
    %       tap_root - Presence of tap root
    %                  default value: true
    %       L_branch - Distance [m] between branching
    %                  default value: 0.2 m
    %     n_branches - Number of branches at each branching posistion
    %                  default value: 1
    %       hv_distr - Horizontal/vertical root distribution
    %                  default value: -1;
    %     branch_tap - Branching on tap root
    %                  default value: false
    %         L_fork - Distance [m] to the forking point
    %                  default value: 1.0 m
    %    fork_enable - Forking enabled in the root structure
    %                  default value: true
    %   taper_enable - Narrowing of tap root enabled
    %                  default value: true
    %     max_radius - Maximum radius of the root system [m]
    %                  default value: 3.0 m
    %      max_depth - Maximum depth of the root system [m]
    %                  default value: 1.0 m
    %      max_order - Maximum branching order of the root system
    %                  default value: 3rd order
    %   fixed_volume - Fixed root structure volume [m^3]
    %                  default value: 0.3 m^3
    %      brcDRatio - Theoretical coefficient of the ratio between the
    %                  diameters of a lateral root and its ancestor
    %                  default value: 0.45
    %             dl - Length [m] of the internode (distance between nodes)
    %                  default value: 0.1 m
    %     stochastic - Stochasticity of the root structure growth
    %                  default value: true
    %       min_diam - Minimum diameter [m] of a root segment
    %                  default value: 0.001 [m]
    %
    % Parameters Methods:
    %   Parameters - Creates a new parameter object from a parameter source
    %   loadParams - Assigns the parameters values to a Parameter object
    %   saveParams - Saves the current parameters in a MAT-file
    
    properties (SetAccess = private)
        n_laterals;   %For parameters information, see help Parameters
        tap_root;     %For parameters information, see help Parameters
        L_branch;     %For parameters information, see help Parameters
        L_fork;       %For parameters information, see help Parameters
        n_branches;   %For parameters information, see help Parameters
        hv_distr;     %For parameters information, see help Parameters
        branch_tap;   %For parameters information, see help Parameters
        fork_enable;  %For parameters information, see help Parameters
        taper_enable  %For parameters information, see help Parameters
        max_radius;   %For parameters information, see help Parameters
        max_depth;    %For parameters information, see help Parameters
        max_order;    %For parameters information, see help Parameters
        fixed_volume; %For parameters information, see help Parameters
        brcDRatio;    %For parameters information, see help Parameters
        dl;           %For parameters information, see help Parameters
        stochastic;   %For parameters information, see help Parameters
        min_diam;     %For parameters information, see help Parameters
    end
    
    methods (Access = private)
        function setDefault(obj)
            params = load('Heart-like');
            
            obj.n_laterals   = params.n_laterals;
            obj.tap_root     = params.tap_root;
            obj.L_branch     = params.L_branch;
            obj.n_branches   = params.n_branches;
            obj.hv_distr     = params.hv_distr;
            obj.branch_tap   = params.branch_tap;
            obj.L_fork       = params.L_fork;
            obj.fork_enable  = params.fork_enable;
            obj.taper_enable = params.taper_enable;
            obj.max_radius   = params.max_radius;
            obj.max_depth    = params.max_depth;
            obj.max_order    = params.max_order;
            obj.fixed_volume = params.fixed_volume;
            obj.brcDRatio    = params.brcDRatio;
            obj.dl           = params.dl;
            obj.stochastic   = params.stochastic;
            obj.min_diam     = params.min_diam;
        end
    end
    
    methods
        function obj = Parameters(src,arg)
            % PARAMETERS() creates a parameter object with default values
            % (heart-like root structure parameters).
            %
            % PARAMETERS('predef',type) creates a parameter object from the
            % parameters of a pre-defined root structure type ('heart', 
            % 'tap', 'herringbone' and 'plate').
            %
            % PARAMETERS('userdef',STRUCT) creates a parameter object from
            % the parameters of a root structure from a struct data.
            %
            % PARAMETERS('file',FILENAME) creates a parameter object from 
            % the parameters of a root structure from a MAT-file.
            %
            % Necessary parameters for deterministic growth
            %   - Initial apices' growth;
            %   - Branching direction;
            %   - Forking direction;
            % 1) Parameters('predef','Heart-like')
            % 2) Parameters('userdef',struct)
            % 3) Parameters('file','filename')
            
            obj.setDefault();
            
            if nargin > 0
                if strcmp(src,'predef')
                    obj.loadParams('file',arg);
                elseif strcmp(src,'userdef') || strcmp(src,'file')
                    obj.loadParams(src,arg);
                else
                    error('Unkown usage of constructor.');
                end
            end
        end
        
        function loadParams(obj,src,arg)
            % LOADPARAMS('userdef',STRUCT) loads the root structure parameters 
            % from a struct data to the current Parameters object.
            %
            % LOADPARAMS('file',FILENAME) loads the root structure parameters
            % from a MAT-file to the current Parameters object.
            %
            % LOADPARAMS('parameters',P) performs a copy of the Parameters
            % object P.
            %
            % Obs.: unkown parameters are ignored and it maintains the
            % values of the previous parameters in case not all of them
            % have been specified. For more information about the list of 
            % parameters check out the Parameters help.
            %
            % See also PARAMETERS, LOADPARAMS, MATFILE
            
            if strcmp(src,'parameters')
                obj.n_laterals   = arg.n_laterals;
                obj.tap_root     = arg.tap_root;
                obj.L_branch     = arg.L_branch;
                obj.n_branches   = arg.n_branches;
                obj.hv_distr     = arg.hv_distr;
                obj.branch_tap   = arg.branch_tap;
                obj.L_fork       = arg.L_fork;
                obj.fork_enable  = arg.fork_enable;
                obj.taper_enable = arg.taper_enable;
                obj.max_radius   = arg.max_radius;
                obj.max_depth    = arg.max_depth;
                obj.max_order    = arg.max_order;
                obj.fixed_volume = arg.fixed_volume;
                obj.brcDRatio    = arg.brcDRatio;
                obj.dl           = arg.dl;
                obj.stochastic   = arg.stochastic;
                obj.min_diam     = arg.min_diam;
            else
                if strcmp(src,'file')
                    params = load(arg);
                elseif strcmp(src,'userdef') && isstruct(arg)
                    params = arg;
                else
                    error('Unkown parameter source.');
                end

                if isfield(params,'n_laterals')
                    obj.n_laterals = params.n_laterals;
                end
                if isfield(params,'tap_root')
                    obj.tap_root = params.tap_root;
                end
                if isfield(params,'L_branch')
                    obj.L_branch = params.L_branch;
                end
                if isfield(params,'n_branches')
                    obj.n_branches = params.n_branches;
                end
                if isfield(params,'hv_distr')
                    obj.hv_distr = params.hv_distr;
                end
                if isfield(params,'branch_tap')
                    obj.branch_tap = params.branch_tap;
                end
                if isfield(params,'L_fork')
                    obj.L_fork = params.L_fork;
                end
                if isfield(params,'fork_enable')
                    obj.fork_enable = params.fork_enable;
                end
                if isfield(params,'taper_enable')
                    obj.taper_enable = params.taper_enable;
                end
                if isfield(params,'max_radius')
                    obj.max_radius = params.max_radius;
                end
                if isfield(params,'max_depth')
                    obj.max_depth = params.max_depth;
                end
                if isfield(params,'max_order')
                    obj.max_order = params.max_order;
                end
                if isfield(params,'fixed_volume')
                    obj.fixed_volume = params.fixed_volume;
                end
                if isfield(params,'brcDRatio')
                    obj.brcDRatio = params.brcDRatio;
                end
                if isfield(params,'dl')
                    obj.dl = params.dl;
                end
                if isfield(params,'stochastic')
                    obj.stochastic = params.stochastic;
                end
                if isfield(params,'min_diam')
                    obj.min_diam = params.min_diam;
                end
            end
        end
        
        function saveParams(obj,filename)
            % SAVEPARAMS(filename) saves the current parameters of the root
            % structure in a MAT-file.
            %
            % See also PARAMETERS, LOADPARAMS, MATFILE
            
            n_laterals   = obj.n_laterals;
            tap_root     = obj.tap_root;
            L_branch     = obj.L_branch;
            n_branches   = obj.n_branches;
            hv_distr     = obj.hv_distr;
            branch_tap   = obj.branch_tap;
            L_fork       = obj.L_fork;
            fork_enable  = obj.fork_enable;
            taper_enable = obj.taper_enable;
            max_radius   = obj.max_radius;
            max_depth    = obj.max_depth;
            max_order    = obj.max_order;
            fixed_volume = obj.fixed_volume;
            brcDRatio    = obj.brcDRatio;
            dl           = obj.dl;
            stochastic   = obj.stochastic;
            min_diam     = obj.min_diam;

            save(filename,...
                 'n_laterals', 'tap_root', 'L_branch', 'hv_distr',      ...
                 'branch_tap', 'L_fork', 'fork_enable', 'taper_enable', ...
                 'max_radius', 'max_depth', 'max_order', 'fixed_volume',...
                 'brcDRatio', 'dl', 'stochastic', 'min_diam');
        end
    end
end