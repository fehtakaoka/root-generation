classdef RootStruct < handle
    % Root structure class (complex of axis)
    %
    % The program was based on the work described in the article:
    % DUPUY, L., T. FOURCAUD, AND A. STOKES. 2005b.
    % A numerical investigation into the influence of soil type and root 
    % architecture on tree anchorage. Plant and Soil 278: 119?134
    
    %% Class attributes
    properties (SetAccess = immutable)
        % global_lca - Global least common ancestor of the root structure
        global_lca   GlbLCA
        tapRoot      TapRoot % (Optional) Tap root
    end
    properties (SetAccess = private)
        axes         Axe    % List of all the axis
        glbAxeIndex  double % Global root index (within the root structure)
        glbNodeIndex double % Global node index (within the root structure)
        hAxisIndex   double % Global horizontal axis index
        finalVolume  double % Final volume after filling process
    end
    properties (Access = private)
        diamSet      double % Set containing all the diameters of the RS
    end
    properties (Constant)
        % params - Parameters of the root structure
        params      = Parameters();
        % vol_tolErr - Tolerance error of the final volume of the root
        % structure for matching it to the imposed fixed volume (0.1%)
        vol_tolErr  = 0.001;
        defaultView = [25 -40 4]; % Default camera position of the plot
        x_glb = [1 0 0]; % Global x-axis coordinates
        y_glb = [0 1 0]; % Global y-axis coordinates
        z_glb = [0 0 1]; % Global z-axis coordinates
    end
    
    %% Instance methods
    methods
        %% Constructor
        function obj = RootStruct(p)
            % RootStruct(params) creates a root structure with the parameteres p

            RootStruct.params.loadParams('parameters',p);
            
            obj.axes         = Axe.empty;
            obj.diamSet      = zeros(1,1000); % initial guess of the number of nodes
            obj.glbAxeIndex  = 0;
            obj.glbNodeIndex = 0;
            obj.hAxisIndex   = 0;

            % Creates a tap root if it is defined in the parameters
            if RootStruct.params.tap_root
                branches    = RootStruct.params.branch_tap;
                hasTaper    = RootStruct.params.taper_enable;
                obj.tapRoot = TapRoot(obj,branches,hasTaper);
                obj.global_lca = obj.tapRoot.lca;
                obj.addAxe(obj.tapRoot);
            end

            n_laterals  = RootStruct.params.n_laterals;
            if n_laterals > 0
                % First axe creation is dealt separtely from the rest so
                % that the global LCA is properly assigned
                if RootStruct.params.stochastic
                    dir = RootStruct.getSymRandDir(1,n_laterals);
                else
                    dir = RootStruct.getSymHorizDir(1,n_laterals);
                end

                if ~RootStruct.params.tap_root
                    % No tap root => first axe should bear the global lca
                    firstAxe = Axe(obj,1,dir,'global_lca',true);
                    obj.global_lca = firstAxe.lca;
                else
                    firstAxe = Axe(obj,1,dir);
                    obj.global_lca.appendInitAxe(firstAxe);
                end
                obj.addAxe(firstAxe);

                % Creation of the rest of the laterals
                for i = 2:n_laterals
                    if RootStruct.params.stochastic
                        dir = RootStruct.getSymRandDir(i,n_laterals);
                    else
                        dir = RootStruct.getSymHorizDir(i,n_laterals);
                    end

                    newAxe = Axe(obj,1,dir);
                    obj.global_lca.appendInitAxe(newAxe);
                    obj.addAxe(newAxe);
                end
            end
        end
        
        %% Auxiliary methods
        function addNodeDiamToSet(obj,node)
            % addNodeDiamToSet(node) sets the value of the node diameter
            % node.diam to the position node.id in the vector diamSet.
            % Note that duplicated values will occur in the vector. Thus,
            % it's necessary to perform union(diamSet,[]) to obtain the set
            % of all the node diameters of the root structure.
            
            lastNNodesGuess = length(obj.diamSet);
            if (node.id > lastNNodesGuess)
                % If there are more nodes than the last guess, double the
                % size of the vector
                obj.diamSet = [obj.diamSet zeros(1,lastNNodesGuess)];
            end
            
            obj.diamSet(node.id) = node.diam;
        end
        
        function dSet = getDiamSet(obj)
            % getDiamSet() returns the set containing all the diameters of
            % the root structure
            
            dSet = union(obj.diamSet,[]); % ordered set of the diameters
            dSet = dSet(2:end); % remove the element diam {0}
        end
        
        function dPairSet = getDiamPairSet(obj)
            % dPairSet() returns the set containing all the diameter pairs
            % of the root struct (i-th node diameter, (i+1)-th node
            % diameter)
            
            dPairSet = [];
            for i = 1:length(obj.global_lca.initAxis)
                dPairSet = [dPairSet; obj.global_lca.initAxis(i).getDiamPairs()];
            end
            
            dPairSet = table(dPairSet(:,1),dPairSet(:,2));
            dPairSet = union(dPairSet, table([],[])); % remove duplicates
            dPairSet = table2array(dPairSet);
        end
        
        function newIndex = getNewAxeIndex(obj,dir)
            % getNewAxeIndex(v) returns a new index for the creation of an
            % axe given its growth direction
            %
            % See also GETNEWNODEINDEX
            
            [r,c] = size(dir);
            if r == 1 && c == 3 && isa(dir,'double')
                if dir(3) == 0
                    % Horizontal axis (z = 0)
                    obj.hAxisIndex = obj.hAxisIndex + 1;
                end
                
                newIndex = obj.glbAxeIndex + 1;
                obj.glbAxeIndex = newIndex;
            else
                error('Invalid growth direction.');
            end
        end
        
        function newIndex = getNewNodeIndex(obj)
            % Methods that returns a new index for the creation of a node
            %
            % See also GETNEWAXEINDEX
            
            newIndex = obj.glbNodeIndex + 1;
            obj.glbNodeIndex = newIndex;
        end
        
        function addAxe(obj,axe)
            obj.axes(end+1) = axe;
        end
        
        function dir = getDetermGrowthDir(obj,prevDir)
            % getDetermGrowthDir(v) returns a deterministic growth direction 
            % for an apex, where v is the growth direction of the parent axe.
            % It respects the axis horizontal/vertical distribution of the 
            % root structure (defined in its parameters).
            % obs.: the direction in the xy plane (horizontal) is random.
            %
            % See also GETRANDOMGROWTHDIR, GETRANDOMBIASEDGROWTHDIR, PARAMETERS.
            
            theta = 2*pi*rand(1);
            phi   = 0;
            r     = 1;

            [x,y,z] = sph2cart(theta,phi,r);
            horz_dir = [x,y,z];
            
            if prevDir(3) == -1
                % Parent axe is oriented vertically => child axe must be
                % oriented horizontallly
                
                dir = horz_dir;
            else
                % Otherwise, the h/v distribution should be respected
%                 aux = RootStruct.params.hv_distr;
%                 aux = aux/sum(aux);
%                 horz_fixed_perc = aux(1);
%                 horz_perc = obj.hAxisIndex/obj.glbAxeIndex;
%                 if horz_perc > horz_fixed_perc
%                     % There are more horizontal axis than specified => vert
%                     dir = [0 0 -1];
%                 else
%                     dir = horz_dir;
%                 end
                
                draw = rand(1);
                aux = RootStruct.params.hv_distr;
                aux = aux/sum(aux); % normalize the frequency
                horz_prob = aux(1);
                if draw < horz_prob
                    dir = horz_dir;
                else
                    dir = [0 0 -1];
                end
            end
        end
        
        function nact = numberOfActiveAxes(obj)
            % numberOfActiveAxes() returns the number of the active axes in
            % the root structure.
            %
            % See also GROW, STEPGROW
            
            nact = 0;
            
            for i = 1:length(obj.axes)
                if ~obj.axes(i).apex.killed
                    nact = nact + 1;
                end
            end
        end
        
        function prune(obj)
            % PRUNE() removes all the invalid nodes within the root struct,
            % i.e. nodes with diameter smaller than a minimum or nodes that
            % are outside the defined boundaries.
            %
            % Obs.: the diameters of the remaining nodes (valid ones) are
            % added to the root struct's diameter set.
            %
            % See also Axe/prune.
            
            initAxes = obj.global_lca.initAxis;
            
            for i = 1:length(initAxes)
                initAxes(i).prune();
            end
        end
        
        function pruneFromNode(obj,node)
            % Recursive method that removes/prunes from the root structure 
            % the entire structure followed by the node 'node' (i.e. all
            % the descendents nodes of 'node').
            %
            % Hip.: pruning shall never be started from the global least
            % commom ancestor of the root structure.
            
            % Tree transversal is done as depth-first post-order search
            if ~isempty(node)
                obj.pruneFromNode(node.next);
                
                % By this point, all the descendent structure is already
                % deleted
                node.next = Node.empty;
                
                if ~isempty(node.ramif)
                    obj.pruneFromNode(node.ramif);
                    node.ramif = Node.empty;
                end
                if isa(node,'ForkedNode')
                    obj.pruneFromNode(node.left);
                    obj.pruneFromNode(node.right);
                    node.left  = Node.empty;
                    node.right = Node.empty;
                end
                if node == node.axe.lca
                    % If the node is its axe's lca, delete the axe as well,
                    % because all of its descendents were deleted
                    delete(node.axe);
                    obj.glbAxeIndex = obj.glbAxeIndex - 1;
                end
                delete(node);
                obj.glbNodeIndex = obj.glbNodeIndex - 1;
            end
        end
        
        function node = getNodeFromGlbIndex(obj,index)
            for i = 1:length(obj.axes)
                 node = obj.axes(i).getNodeFromGlbIndex(index);
                 if (~isempty(node))
                     return
                 end
            end
        end
        
        function axe = getAxeFromGlbIndex(obj,index)
            for i = 1:length(obj.axes)
                 axe = obj.axes(i).getAxeFromGlbIndex(index);
                 if (~isempty(axe))
                     return
                 end
            end
        end
        
        %% Main methods
        function grow(obj)
            % GROW() makes the entire root structure grow until there is
            % no active apex, i.e. that still satisfies boundary conditions
            %
            % See also STEPGROW, AXE.GROWAXE
            
            disp('-> Starting growing process from the initial apices ...');
            
            % Progress bar
            f = waitbar(0,'Starting growing process ...');
            pause(.5);
            
            nact = obj.numberOfActiveAxes;
            while (nact > 0)
                for i = 1:length(obj.axes)
                    obj.axes(i).growAxe();
                end
                
                nact = obj.numberOfActiveAxes;
                
                % Update progress bar
                txt = sprintf('#Active axes: %d of %d total axes',nact,obj.glbAxeIndex);
                waitbar((obj.glbAxeIndex-nact)/obj.glbAxeIndex,f,txt);
            end
            
            disp('-> Growing process ended successifully.');
            
            % Close progress bar
            close(f);
            
            if (~RootStruct.params.stochastic && ~isempty(RootStruct.params.hv_distr))
                disp(['-> Final H/V distribution: (' ... 
                    num2str(obj.hAxisIndex/obj.glbAxeIndex) ...
                    ',' num2str(1-(obj.hAxisIndex/obj.glbAxeIndex)) ')']);
            end
        end
        
        function stepGrow(obj)
            % Test method that grows step-by-step the entire root structure
            % until there is no active apex, i.e. that still satisfies
            % boundary conditions.
            %
            % See also GROW
            
            for i = 1:length(obj.axes)
                obj.axes(i).growAxe();
            end
            
            if (~RootStruct.params.stochastic && ~isempty(RootStruct.params.hv_distr))
                disp(['-> H/V distribution: (' ... 
                    num2str(obj.hAxisIndex/obj.glbAxeIndex) ...
                    ',' num2str(1-(obj.hAxisIndex/obj.glbAxeIndex)) ')']);
            end
        end
        
        function str = fill(obj)
            % FILL() fills the root structure's volume, by setting all of
            % the component nodes' diamater, to match the fixed volume.
            %
            % obs.: it determines the initial diamater (global least common
            % ancestor node diamater), from which all of the descentents'
            % diamaters can be evaluated). Also, note that, as the diameter
            % variation or mother-daughter coefficient might not be linear,
            % an analytical solution is not always possible. A numeric
            % method is thus utilized to compute the initial diamater.
            
            % Numerical method to achieve the fixed root structure volume
            % (bisection): the desired initial diamater lies in the
            % interval [d_min,d_max]
            
            fixed_volume = RootStruct.params.fixed_volume;
            max_depth = RootStruct.params.max_depth;
            N = 15; % "Safety coefficient" for initial guess
            
            % Initial guess for the diameter interval [d_min, d_max]
            d_max = 2*N*sqrt(fixed_volume/(pi*max_depth));
            d_min = 0;
            
            vol  = 0;
            iter = 1;
            itermax = 100; % Maximum number of iterations before aborting
            
            str = '-> Starting filling volume process ...';
            
            % Progress bar
            f = waitbar(0,'Starting filling volume process ...');
            pause(.5);
            
            while iter < itermax
                diam = (d_max + d_min)/2;
                for i = 1:length(obj.global_lca.initAxis)
                    axe = obj.global_lca.initAxis(i);
                    
                    axe.lca.diam = diam;
                    axe.updateGeometry();
                    vol = vol + axe.getVolume();
                end
                  
                % Update progress bar
                relErr = abs(vol - fixed_volume)/fixed_volume;
                txt = sprintf(['Iteration #%d of %d: Initial diameter: %f\n' ...
                    'Relative error: %f%%\n' ...
                    'Error tolerance: %f%%'],iter,itermax,diam,relErr,RootStruct.vol_tolErr);
                waitbar(iter/itermax,f,txt);
                
                % Stop criterion for the numeric method
                if abs(vol - fixed_volume) < ...
                      (RootStruct.vol_tolErr)*fixed_volume
                    err = 100*abs(vol - fixed_volume)/fixed_volume;
                    obj.finalVolume = vol;
                    break;
                end
                
                % Since the total volume function f(d) is monotonically
                % increasing with respect to the initial diameter, if
                % f((d_max+d_min)/2) > fixed_volume, then f(d_min) <
                % fixed_volume. Thus the desired diameter lies in the
                % sub-interval [d_min ; (d_max+d_min)/2]. Otherwise, it
                % lies in the sub-interval [(d_max+d_min)/2 ; d_max].
                if vol > fixed_volume
                    d_max = (d_max+d_min)/2;
                else
                    d_min = (d_max+d_min)/2;
                end
                
                vol  = 0;
                iter = iter + 1;
            end
            
            if iter < itermax
                str = [str newline ...
                        '-> Filling volume process ended successifully:' newline ...
                        ' |-> Method converged to a final volume of '    ...
                        num2str(vol) ' m^3 (an error of ' num2str(err)   ...
                        '%)' newline '     with an initial diameter of ' ...
                        num2str(diam) ' m at iteration #' ...
                        num2str(iter) '!'];
                    
                disp(str);
            else
                error('Filling process failed to converge');
            end
            
            % Now that we have determined the value for the initial
            % diameter we can prune/delete the nodes with small diameters
            obj.prune();
            
            % Close progress bar
            close(f);
        end
        
        %% Display methods
        function str = printRootStruct(obj)
            str = [];
            for i = 1:length(obj.global_lca.initAxis)
                axe = obj.global_lca.initAxis(i);
                str = [str newline printAxe(axe)];
            end
        end
        
        function drawRootStruct(obj,drawNodes,drawEdges,drawRadiusBoundary,varargin)
            % Method that draws the entire root structure
            %
            % List of parameters: (obj,drawNodes,drawEdges,drawRBoundary,*campos*)
            %   |-> (RootStructure) obj: root structure to be drew
            %   |-> (boolean) drawNodes: allow/disable drawing of nodes
            %   |-> (boolean) drawEdges: allow/disable drawing of edges
            %   |-> (boolean) drawRBoundary: allow/disable drawing of one
            %   of the boundary conditions (radius) - hemisphere
            %   |-> (1x3 double) campos: optional argument to set the view
            %   of the plot to the camera position 'campos'
            %
            % obs.: axis in the plot are limited by the boundary conditions
            
            %figure
            %title('Visual representation of the complete root structure');
            for i = 1:length(obj.global_lca.initAxis)
                axe = obj.global_lca.initAxis(i);
                drawAxe(axe,drawNodes,drawEdges);
            end
            
            xy_limit = RootStruct.params.max_radius;
            z_limit  = RootStruct.params.max_depth;
            xlim([-xy_limit +xy_limit]);
            ylim([-xy_limit +xy_limit]);
            zlim([-z_limit 0]);
            
            if drawRadiusBoundary
                [X,Y,Z] = cylinder(RootStruct.params.max_radius);
                Z(Z==1) = -RootStruct.params.max_depth;
                surf(X,Y,Z,'FaceColor','yellow','FaceAlpha',0.05);
            end
            
            if nargin == 5
                % Specified camera position
                campos(varargin{1});
            else
                campos(RootStruct.defaultView);
            end
            
            hold off
            grid on;
        end
    end
    
    %% Static methods
    methods(Static)
        function next_diam = getNextNodeDiameter(node_k)
            % getNextNodeDiameter(axe, diam, l_k) returns the diameter of
            % the (k+1)-th node, where diam and l_k are, respectively, the
            % diameter and the distance from the axe's insertion point to
            % the k-th node's tip. It implements the taper equation of the
            % article.
            %
            % obs.: although the diameters in the formula are given in
            % centimeters, the arguments to this method must be given in
            % meters.
            
            axe = node_k.axe;
            node_diam = node_k.diam;
            % According to the formula, l is the distance from the
            % axe's insertion point to the *tip* of the k-th node
            l_k = getDistance(axe.lca, node_k) + RootStruct.params.dl;
            
            if ((isa(axe,'TapRoot') && ~axe.hasTaper) || isa(node_k,'OffsetNode'))
                next_diam = node_diam;
            else
                dl = RootStruct.params.dl;
                % Increment (12*dl*(l_k)^(-0.6)) is in centimeters
                next_diam = node_diam - (12/100)*dl*(l_k)^(-0.6);
            end            
        end
        
        % !! Deprecated !!
        function next_diam = getNextNodeDiameter2(axe, node_diam, l_k)
            % getNextNodeDiameter(axe, diam, l_k) returns the diameter of
            % the (k+1)-th node, where diam and l_k are, respectively, the
            % diameter and the distance from the axe's insertion point to
            % the k-th node's tip. It implements the taper equation of the
            % article.
            %
            % obs.: although the diameters in the formula are given in
            % centimeters, the arguments to this method must be given in
            % meters.
            
            if ((isa(axe,'TapRoot') && ~axe.hasTaper))
                next_diam = node_diam;
            else
                dl = RootStruct.params.dl;
                % Increment (12*dl*(l_k)^(-0.6)) is in centimeters
                next_diam = node_diam - (12/100)*dl*(l_k)^(-0.6);
            end            
        end
        
        function branch_diam = getBranchDiameter(mother_diam)
            branch_diam = (RootStruct.params.brcDRatio)*mother_diam;
        end
        
        function reached = geomBoundaryIsReached(pos)
            % Method that checks whether any of the geometrical boundary
            % conditions are reached (radius, depth).
            %
            % See also ORDERBOUNDARYISREACHED, BOUNDARYISREACHED
            
            reached = false;
            
            % Radius in cylindrical coordinates
            r = sqrt(pos(1)^2 + pos(2)^2);
            
            if r > RootStruct.params.max_radius
                reached = true;
            elseif pos(3) < -RootStruct.params.max_depth
                reached = true;
            elseif pos(3) > 0
                reached = true;
            end
        end
        
        function reached = topoBoundaryIsReached(order)
            % Method that checks whether the topological boundary condition
            % is reached (maximum branching order)
            %
            % See also GEOMBOUNDARYISREACHED, BOUNDARYISREACHED
            
            reached = (order > RootStruct.params.max_order);
        end
        
        function reached = boundaryIsReached(pos, order)
            % Method that checks whether any of the boundary conditions are
            % reached
            %
            % See also GEOMBOUNDARYISREACHED, ORDERBOUNDARYISREACHED
            
            reached = RootStruct.geomBoundaryIsReached(pos)    || ...
                      RootStruct.topoBoundaryIsReached(order);
        end
        
        function dir = getRandomGrowthDir()
            % Method that returns a random growth direction for an initial
            % apex
            %
            % See also GETDETERMGROWTHDIR
            
%             % It has to be orieted downwards ? (phi < 0) <=> (z < 0)
%             r     = 1;                          % unit length
%             theta = 2*pi*rand(1);               % azimuthal angle
%             stdev = 0.3;
%             phi   = -1; % arbitrary initial value just to enter the loop
%             while phi > 0
%                 phi = -(pi/4) + stdev*randn(1); % polar angle
%             end
%             
%             [x,y,z] = sph2cart(theta,phi,r);

            x = 2*(rand(1)-0.5); %  [-1; +1]
            y = 2*(rand(1)-0.5); %  [-1; +1]
            z = -0.8*rand(1);    % [-.8;  0]

            dir = [x y z];
            dir = dir/norm(dir);
        end
        
        function dir = getRandomBiasedGrowthDir(gdir)
            % getRandomBiasedGrowthDir(v) returns a random growth direction,
            % whose mean is the direction v, for an initial apex.
            %
            % See also GETRANDOMGROWTHDIR, GETDETERMGROWTHDIR.
            
            [TH,PHI,~] = cart2sph(gdir(1),gdir(2),gdir(3));
            % Random branching direction whose mean is the direction of the
            % mother's axe growth (normally distributed with standard
            % deviation obtained empirically varying values)
            stdev1 = 0.6; stdev2 = stdev1;
            theta = TH  + stdev1*randn(1);  % azimuthal angle
            phi   = PHI + stdev2*randn(1);  % polar angle
            r     = 1;                      % unit length
            
            % !! phi: elevation angle FROM the xy plane
            [x,y,z] = sph2cart(theta,phi,r);
            dir = [x y z];
        end
        
        function dir = getSymHorizDir(index,total,offset)
            % getSymHorzDir(i,n) gets the i-th horizontal direction of a
            % set of n total horizontal directions axi-symmetrically
            % distributed
            %
            % getSymHorzDir(index,total,offset) gets the i-th horizontal 
            % direction of a set of n total horizontal directions
            % axi-symmetrically distributed with an azimuth angle offset.
            %
            % obs.: method used to get the direction at creation of the
            % main lateral roots (in the deterministic case) and for the 
            % branching directions in the tap root of the herring-bone like
            % root system.
            %
            % See also GETSYMRANDDIR.
            
            aux = 0;
            if nargin == 3
                aux = offset;
            end
            
            theta = (index-1)*2*pi/total + aux;
            phi   = 0;

            [x,y,z] = sph2cart(theta,phi,1);

            dir = [x,y,z];
        end

        function dir = getSymRandDir(index,total,offset)
            % getSymRandDir(index,total) gets the i-th random direction
            % of a set of n total random directions axi-symmetrically 
            % distributed.
            %
            % getSymRandDir(index,total,offset) gets the i-th random 
            % direction of a set of 'total' random directions 
            % axi-symmetrically distributed with an azimuth angle offset.
            %
            % obs.: method used to get the direction at creation of the
            % main lateral roots (in the stochastic case).
            %
            % See also GETSYMHORIZDIR.
            
            aux = 0;
            if nargin == 3
                aux = offset;
            end
            
            theta = (index-1)*2*pi/total + aux;
            phi   = -(pi/2)*rand(1,1);

            [x,y,z] = sph2cart(theta,phi,1);

            dir = [x y z];
        end
        
        function [alpha, beta] = getEulerAngles(Z)
            % getEulerAngles(Z) returns the Euler angles [alpha, beta] for
            % rotating the coordinate system to obtain one in which the z'
            % axis points to Z and the direction of the x/y axis is
            % arbitrary
            %
            % Obs. 1: Z must have unity norm;
            % Obs. 2: since the choice for the direction of the x or y axis
            % of the axe is arbitrary, there is no need for the Euler angle
            % gamma.
            %
            % See also AXE.GETPOSITIONINGSTRUCT
            
            y = RootStruct.y_glb; % Global coordinates of the y axis
            z = RootStruct.z_glb; % Global coordinates of the z axis

            Z3 = dot(Z, z); % projection along the z-axis
            Z2 = dot(Z, y); % projection along the y-axis

            alpha = 0; % in case ||Z3|| = 1, alpha is zero
            if (Z3^2 ~= 1)
                alpha = acos(-Z2/sqrt(1-Z3^2));
            end
            beta  = acos(Z3);

            % We should take into account that the image of the function
            % acos is limited to [0;pi]. Therefore, since cos(.) is even,
            % there are two solutions, one positive and one negative.
            alphaS = [alpha -alpha];
            betaS  = [beta  -beta];

            % Test all the possible combinations
            for i = 1:2
                for j = 1:2
                    alpha = alphaS(i);
                    beta  = betaS(j);

                    Z_glb = [sin(alpha)*sin(beta); -cos(alpha)*sin(beta); cos(beta)];

                    % Due to numerical errors of the trigonometric
                    % functions, an error tolerance must be specified
                    err_tol = 1e-10;
                    if (norm(Z'-Z_glb) < err_tol)
                        return;
                    end
                end
            end
        end
    end
end