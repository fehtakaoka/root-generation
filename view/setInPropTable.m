function setInPropTable(propTable,varargin)
    % setInPropTable(propTable,'prop1','val1','prop2','val2',...) sets the 
    % string values in the respective properties of propTable.
    %
    % Properties are:
    %   - n_laterals
    %   - n_nodes
    %   - n_axis
    %   - vol
    %   - tap_root
    %   - hv_distr
    %   - stochastic
    %   - branch_tap
    %   - taper_enable
    %   - fork_enable
    %   - L_branch;
    %   - n_branches;
    %   - L_fork;
    %   - max_radius;
    %   - max_depth;
    %   - max_order;
    %   - fixed_volume;
    %   - brcDRatio;
    %   - dl;
    %
    % See also CLEARANDUPDATEPROPTABLE.
    
    if mod(nargin-1,2) == 0
        t = get(propTable,'Data');
        
        for i = 1:2:nargin-1
            index = indexInTable(varargin{i});
            
            val = varargin{i+1};
            if ~isstring(val) && ~ischar(val) && ~islogical(val)
                error('Property value must be a string/char vector');
            end
            if islogical(val)
                if val
                    val = 'true';
                else
                    val = 'false';
                end
            end
            
            t{index} = val;
            set(propTable,'Data',t);
        end
    else
        error('There is one property/value missing.');
    end
end

function id = indexInTable(prop)    
    switch prop
        case {'n_laterals'}
            id = 1;
        case {'n_nodes'}
            id = 2;
        case {'n_axis'}
            id = 3;
        case {'vol'}
            id = 4;
        case {'tap_root'}
            id = 5;
        case {'hv_distr'}
            id = 6;
        case {'stochastic'}
            id = 7;
        case {'branch_tap'}
            id = 8;
        case {'taper_enable'}
            id = 9;
        case {'fork_enable'}
            id = 10;
        case {'L_branch'}
            id = 11;
        case {'n_branches'}
            id = 12;
        case {'L_fork'}
            id = 13;
        case {'max_radius'}
            id = 14;
        case {'max_depth'}
            id = 15;
        case {'max_order'}
            id = 16;
        case {'fixed_volume'}
            id = 17;
        case {'brcDRatio'}
            id = 18;
        case {'dl'}
            id = 19;
        otherwise
            id = -1;
    end
end