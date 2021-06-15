classdef Axe < handle & matlab.mixin.Heterogeneous
    % Axe class (components of root structure and complex of nodes)
    
    %% Class attributes
    properties (SetAccess = immutable)
        id         uint32     % Indentification/index within the root structure
        rootStruct RootStruct % Root structure bearing the axe
        order      uint8      % Branching order
        lca        Node       % Least common ancestor of the axe (= first node)
    end
    properties (SetAccess = protected)
        growth_dir double     % Direction of the axe's growth
        apex       Node       % Axe's tip (= last node)
        lastRamPos double     % Last ramification position within the axe
    end
    properties (Access = private)
        lastLcaDiam double    % Auxiliary variable to check geometry consistency
    end
    properties (Dependent)
        n_nodes               % Number of nodes
        len                   % Length [m] of the axe at a growth instant
    end
    
    %% Instance methods
    methods
        %% Constructor
        function obj = Axe(rootStruct_,order_,growth_dir_,varargin)
            % AXE(r,1,d) constructs an order 1 Axe object in the root structure r
            % that grows in the direction d;
            %
            % The following attributes can be specified (otherwise, they
            % will take the default value):
            %  - coord: coordinate of the first node (lca) (default: origin);
            %  - global_lca: let the axe bear the global lca of the root structure (default: false);
            %  - lastRamPos: last ramification position (default: lca's coordinate);
            %
            % Note that an axe is only allowed to have a global lca if
            % there is no tap root in the root structure. Moreover, only
            % one axe in the root structure can have the global lca.
            % Important: coord and global_lca should not be specified
            % simultaneously.
            %
            % Exemples of common usages:
            %  - For initial axes (laterals):
            %   Axe(r,1,dir) creates a primary axe (order 1) with its 1st 
            %   node at the origin that grows in the direction dir.
            %   Obs.: for the tap root (if exisits), use the constructor of
            %   the class TapRoot.
            %
            %   Axe(r,1,dir,'global_lca',true) creates a primary axe with its
            %   1st node at the origin that grows in the direction dir and
            %   bears the root structure global lca.
            %
            %  - For ramifications (branch or fork):
            %   Axe(r,o,dir,'coord',c,'lastRamPos',v) 
            %   creates an order 'o' axe @ coordinate 'c' that grows in the
            %   direction dir and whose last ramification position was 'v'.
            %      obs.: last ramification position in an order >1 axe must
            %      be the position of the node that generated this new axe 
            %      (not the lca of this new axe)
            %
            % See also TAPROOT, GLBLCA.
            
            if mod((nargin-3),2) == 1
                % There is one property with no assigned value
                error('Not enough input arguments');
            else
                obj.rootStruct = rootStruct_;
                obj.id         = getNewAxeIndex(obj.rootStruct,growth_dir_);
                obj.order      = order_;
                obj.growth_dir = growth_dir_;
                obj.lastLcaDiam = -1;
                
                % Default values of optional attributes
                obj.lca        = Node.empty;
                obj.apex       = Node.empty;
                obj.lastRamPos = double.empty;
                coord          = [0 0 0];
                createGlbLCA   = false;
                
                for i = 1:2:(nargin-3)
                    prop = varargin{i};
                    val  = varargin{i+1};
                    
                    if strcmp(prop,'coord')
                        coord = val;
                    elseif strcmp(prop,'global_lca')
                        createGlbLCA = val;
                    elseif strcmp(prop,'lastRamPos')
                        obj.lastRamPos = val;
                    else
                        error(['Unkown attribute ' prop '.'])
                    end
                end
                
                if createGlbLCA
                    obj.lca = GlbLCA(obj.rootStruct,obj,coord);
                else
                    % Axe should not bear the global lca
                    if (obj.order > 1)
                        % OffsetNode and second node are located at the
                        % same position, since diameters haven't yet been
                        % assigned
                        obj.lca = OffsetNode(obj.rootStruct,obj,coord);
                        newNode = Node(obj.rootStruct,obj,coord);
                        
                        obj.lca.next = newNode;
                        obj.apex     = newNode;
                    else
                        obj.lca = Node(obj.rootStruct,obj,coord);
                    end
                end
                if isempty(obj.lastRamPos)
                    obj.lastRamPos = obj.lca.coord;
                end
                
                if (isempty(obj.apex))
                    obj.apex = obj.lca;
                end
            end
        end
        
        %% Getters and setters
        function set.apex(obj,node)
            if isempty(node)
                % Empty apex at creation is allowed
                obj.apex = Node.empty;
            else
                % Since the apex is the last node of the axe, it should have no
                % node pointed at in the 'next' attribute
                if isempty(node.next)
                    obj.apex = node;
                else
                    error('Property ''apex'' should have no next node');
                end 
            end
        end
        
        function set.growth_dir(obj,dir)
            [r,c] = size(dir);
            if r == 1 && c == 3 && isa(dir,'double')
                 obj.growth_dir = dir/norm(dir);
            else
                error(['Property ''growth_dir'' must be an 1x3 double ' ...
                      'array']);
            end
        end
        
        function set.lastRamPos(obj,pos)
            if isempty(pos)
                % Empty lastRamPos at creation is allowed
                obj.lastRamPos = double.empty;
            else
                [r,c] = size(pos);
                if r == 1 && c == 3 && isa(pos,'double') && pos(3) <= 0
                     obj.lastRamPos = pos;
                else
                    error(['Property ''lastRamPos'' must be an 1x3 double ' ...
                          'array with a negative z coordinate']);
                end
            end
        end
        
        function n_nodes = get.n_nodes(obj)
            % Method to get the number of nodes composing the axe
            n_nodes = 0;
            p = obj.lca;
            while(~isempty(p))
                n_nodes = n_nodes + 1;
                p = p.next;
            end
        end
        
        function len = get.len(obj)
            % Method that calculates the length of the axe
            if (obj.order > 1)
                k = 2; % OffsetNode is not taken into account
            else
                k = 1;
            end
            len = (obj.n_nodes-k)*(RootStruct.params.dl);
        end
        
        %% Auxiliary methods
        function node = nodeFromIndex(obj,i)
            % nodeFromIndex(i) returns the ith node from the axe
            if ((i < 1) || (i > obj.n_nodes))
                error('Index out of boundary');
            end
            
            node = obj.lca;
            for j = 1:(i-1)
                node = node.next;
            end
        end
        
        function node = getNodeFromGlbIndex(obj,index)
            node = Node.empty();
            p = obj.lca;
            
            while(~isempty(p))
                if(index == p.id)
                    node = p;
                    return
                end
                
                if isa(p,'ForkedNode')
                    if ~isempty(p.left)
                        node = p.left.axe.getNodeFromGlbIndex(index);
                    end
                    if ~isempty(p.right)
                        node = p.right.axe.getNodeFromGlbIndex(index);
                    end
                end
                if ~isempty(p.ramif)
                    for i = 1:length(p.ramif)
                        node = p.ramif(i).axe.getNodeFromGlbIndex(index);
                    end
                end
                if (~isempty(node))
                    return
                end
                
                p = p.next;
            end
        end
        
        function axe = getAxeFromGlbIndex(obj,index)
            axe = Axe.empty();
            
            if(index == obj.id)
                axe = obj;
                return
            end
            
            p = obj.lca;
            while(~isempty(p))
                if isa(p,'ForkedNode')
                    if ~isempty(p.left)
                        axe = p.left.axe.getAxeFromGlbIndex(index);
                    end
                    if ~isempty(p.right)
                        axe = p.right.axe.getAxeFromGlbIndex(index);
                    end
                end
                if ~isempty(p.ramif)
                    for i = 1:length(p.ramif)
                        axe = p.ramif(i).axe.getAxeFromGlbIndex(index);
                    end
                end
                if (~isempty(axe))
                    return
                end
                
                p = p.next;
            end
        end
        
        function willFork = nextNodeWillFork(obj)
            % nextNodeWillFork() checks if the next increment node can fork
            % according to the distance rule and if forking is allowed.
            %
            % See also CANBRANCH.
            
            willFork = false;
            
            if RootStruct.params.fork_enable
                dir = obj.growth_dir;
                newCoord = obj.apex.coord + dir*(RootStruct.params.dl);
                forkDist = RootStruct.params.L_fork;

                willFork = getDistanceFromPos(obj.lca, newCoord) >= ...
                                forkDist;
            end
        end
        
        function willBranch = canBranch(obj)
            % canBranch() checks if the apex can branch according only to
            % the distance rule (if distance > branch distance => branch)
            % and if branching in tap root is allowed (if applicable).
            %
            % obs.: branching condition according to the article's one, but
            % its usage does not allow the requirement for the horizontal/
            % vertical axis distribution parameter to be met.
            %
            % See also CANBRANCH2, NEXTNODEWILLFORK.
            
            willBranch = false;

            if RootStruct.params.tap_root ...
                    && obj.rootStruct.tapRoot == obj ...
                    && ~RootStruct.params.branch_tap
                % The current axe is the root structure's tap root and it
                % should not branch (according to the parameters)
                return;
            end
            
            willBranch = getDistanceFromPos(obj.apex,obj.lastRamPos) >= ...
                            RootStruct.params.L_branch;
        end
        
        function willBranch = canBranch2(obj)
            % canBranch() checks if the apex can branch according to the
            % following rules:
            %  - distance rule (if distance > branch distance => branch)
            %  - if the axe is vertical and the current horizontal/vertical
            %  distribution is so that the percentage of horiz. axis is
            %  less than the fixed percentage of horz. axis
            %  - if branching in tap root is allowed (if applicable).
            %
            % obs.: modified version of the branching operation of the
            % article so that the specified horizontal/vertical
            % distribution parameter can be reached.
            %
            % See also CANBRANCH2, NEXTNODEWILLFORK.
            
            willBranch = false;

            if RootStruct.params.tap_root ...
                    && obj.rootStruct.tapRoot == obj ...
                    && ~RootStruct.params.branch_tap
                % The current axe is the root structure's tap root and it
                % should not branch (according to the parameters)
                return;
            elseif ~RootStruct.params.stochastic
                aux = RootStruct.params.hv_distr;
                aux = aux/sum(aux);
                horz_fixed_perc = aux(1);
                horz_perc = obj.rootStruct.hAxisIndex/obj.rootStruct.glbAxeIndex;
                
                if obj.growth_dir(3) == -1 ...
                        && horz_perc > horz_fixed_perc
                    % The current axe is oriented vertically and there should
                    % be less horizontal axis than there are currently.
                    % obs.: a vertical axe branch is oriented horizontally.
                    return;
                end
            end
            
            willBranch = getDistanceFromPos(obj.apex,obj.lastRamPos) >= ...
                            RootStruct.params.L_branch;
        end
        
        function incr(obj)
            % Method that increments a root segment (node) at the axe's tip
            % respecting boundary conditions of the root structure.
            % Moreover, if the increment node satisfies the condition to
            % fork, it will be created as a ForkedNode object
            %
            % See also BRANCH, FORK, GROWAXE
            
            dir = obj.growth_dir;
            newCoord = obj.apex.coord + dir*(RootStruct.params.dl);
            
            % Test if the boundary conditions haven't been reached
            if ~RootStruct.boundaryIsReached(newCoord, obj.order)
                if obj.nextNodeWillFork()
                    newNode = ForkedNode(obj.rootStruct, obj, newCoord);
                else
                    newNode = Node(obj.rootStruct, obj, newCoord);
                end
                
                obj.apex.next = newNode;
                obj.apex = obj.apex.next; % new node is the new apex
            else
                % If geometrical boundaries are reached, the axe cannot
                % grow anymore
                if RootStruct.geomBoundaryIsReached(newCoord)
                    killApex(obj.apex);
                end
                % Otherwise, if only the topological boundary is reached 
                % (branching order), the axe can still grow, but cannot
                % fork nor branch
            end
        end
        
        function branch(obj)
            % Method that creates a new branch (lateral root) respecting
            % boundary conditions of the root structure
            %
            % See also INCR, FORK, GROWAXE
            
            offset = 2*pi*rand(1); % azimuth direction offset
            n_branches = RootStruct.params.n_branches;
            for i = 1:n_branches
                % new growth direction calculation
                if RootStruct.params.stochastic
                    newDir = RootStruct.getRandomBiasedGrowthDir(obj.growth_dir);
                else
                    if isa(obj,'TapRoot')
                        newDir = RootStruct.getSymHorizDir(i,n_branches,offset);
                    else
                        newDir = obj.rootStruct.getDetermGrowthDir(obj.growth_dir);
                    end
                end

                newPos   = obj.apex.coord;
                newOrder = obj.order + 1;

                % Test if the boundary conditions aren't reached for the new node
                if ~RootStruct.boundaryIsReached(newPos, newOrder)
                    newAxe  = Axe(obj.rootStruct,newOrder,newDir, ...
                                  'coord',      newPos, ...
                                  'lastRamPos', newPos);

                    obj.apex.ramif(end+1) = newAxe.lca;
                    obj.lastRamPos = obj.apex.coord;
                    obj.rootStruct.addAxe(newAxe);
                end
                
                if ~isa(obj,'TapRoot')
                    % Only the tap root allows multiple branching at the
                    % same point
                    break;
                end
            end
        end
        
        function fork(obj)
            % Method that forks the axe (and kills its apex), creating two
            % new axes, whose growth direction vectors, r1 and r2, togeter 
            % with the forked axe's, d, are coplanar. Also, r1 and r2 have 
            % the same angle with d. Thus, the sum of r1 with r2 results in
            % a colinear vector with d (r1 + r2 = k.d).
            % It also respects boundary conditions of the root structure.
            %
            % See also INCR, BRANCH, GROWAXE
            
            d = obj.growth_dir;
            
            [TH,PHI,~] = cart2sph(d(1),d(2),d(3));
            % Random forking direction for the first axe whose mean is the 
            % direction of the mother's axe growth (normally distributed 
            % with standard deviation obtained empirically varying values)
            stdev1 = 0.4; stdev2 = stdev1;
            theta = TH  + stdev1*randn(1);  % azimuthal angle
            phi   = PHI + stdev2*randn(1);  % polar angle
            r     = 1;                      % unit length
            
            [x1,y1,z1] = sph2cart(theta,phi,r);
            r1 = [x1,y1,z1];
            k  = 2*dot(r1,d); % norm of the sum of the two growth direction
            
            % Since r1 + r2 = k.d => r2 = k.d - r1
            r2 = k*d - r1;
            
            newPos1  = obj.apex.coord;
            newPos2  = obj.apex.coord;
            newOrder = obj.order + 1;
            
            forked = false;
            
            % Test if the boundary conditions aren't reached for the "2nd"
            % node of the new axes, because the first one (LCA) corresponds
            % to the OffsetNode, which is at the same location as the 
            % current axe's apex (an already validated position)
            if ~RootStruct.boundaryIsReached(newPos1, newOrder)
                newAxe = Axe(obj.rootStruct,newOrder,r1,   ...
                             'coord',      newPos1, ...
                             'lastRamPos', newPos1);
                
                obj.apex.left = newAxe.lca;
                obj.rootStruct.addAxe(newAxe);
                
                forked = true;
            end
            if ~RootStruct.boundaryIsReached(newPos2, newOrder)
                newAxe = Axe(obj.rootStruct,newOrder,r2,   ...
                             'coord',      newPos1, ...
                             'lastRamPos', newPos2);
                
                obj.apex.right = newAxe.lca;
                obj.rootStruct.addAxe(newAxe);
                
                forked = true;
            end
            
            if forked
                % Mother root should not grow anymore, since it's been forked
                killApex(obj.apex);
            end
            % If the mother root was not forked, the axe can still grow
        end
        
        function dPairs = getDiamPairs(obj)
            % getDiamPairs() returns a vector of diameter pairs given by
            %         (ith node diameter, (i+1)th node diameter)
            % of the current axe and all of its descendants
            
            p = obj.lca;
            n = obj.n_nodes;
            dPairs = zeros(n,2);
            k = 1;
            while(~isempty(p))
                dPairs(k,1) = p.diam;
                if isempty(p.next)
                    dPairs(k,2) = 0;
                else
                    dPairs(k,2) = p.next.diam;
                end
                
                diamPairsAux = [];
                if ~isempty(p.ramif)
                    for i = 1:length(p.ramif)
                        newPairs = p.ramif(i).axe.getDiamPairs();
                        diamPairsAux = [diamPairsAux; newPairs];
                    end
                end
                if isa(p,'ForkedNode')
                    if ~isempty(p.left)
                        newPairs = p.left.axe.getDiamPairs();
                        diamPairsAux = [diamPairsAux; newPairs];
                    end
                    if ~isempty(p.right)
                        newPairs = p.right.axe.getDiamPairs();
                        diamPairsAux = [diamPairsAux; newPairs];
                    end 
                end
                
                dPairs = [dPairs; diamPairsAux];
                
                p = p.next;
                k = k+1;
            end
        end
        
        function checkGeomConsistency(obj)
            p = obj.lca;
            
            while(~isempty(p.next))
                if(~isa(p,'OffsetNode'))
                    dist = p.getDistance(p.next);
                    err  = 1E-10;
                    if(abs(dist - RootStruct.params.dl) > err)
                        error(['Incosistent root struct geometry between nodes' ...
                               p.toStr() ' and ' p.next.toStr() ' in axe ' obj.toStr()]);
                    end
                end
                
                if(geomBoundaryIsReached(p.next.coord))
                    error(['Node ' p.next.toStr() 'is outside the geometrical boundaries']);
                end
                
                p = p.next;
            end
        end
            
        function u = getOrthogonalDirection(obj)
            % getOrthogonalDirection() returns a vector that is orthogonal
            % to the growing direction of the current axe.
            
            v = obj.growth_dir;
            
            if (v(2) ~= 0)
                u = [1 -v(1)/v(2) 0];
            else
                u = [0 1 0];
            end
        end
        
        %% Main methods
        function growAxe(obj)
            % Method that manages the axe's growth (increments, branches
            % and forks) respecting the boundary conditions of the root
            % structure
            %
            % See also INCR, BRANCH, FORK
            
            if ~obj.apex.killed
                % Creation of a new root segment
                obj.incr();

                % Fork if conditions are met (verified at the incr method).
                % Here we only verify if the node is a ForkedNode (it will
                % be if its distance from the insertion point is greater
                % than the fork distance parameter)
                if isa(obj.apex,'ForkedNode')
                    obj.fork();
                % Only branch if the node wasn't forked
                elseif obj.canBranch()
                    obj.branch();
                end
            end
        end
        
        function updateGeometry(obj)
            % UPDATEGEOMETRY() updates the geometry of the current axe and 
            % all of its descendents based on the *updated* geometry of its
            % lca.
            %
            % Obs.: order-1 axes don't change their nodes position, only
            % their diameters.
            %
            % See also getVolume, Axe/prune
            
            p = obj.lca;
            
            if (p.diam == obj.lastLcaDiam)
                % Nothing has changed since the last update
                return
            else
                obj.lastLcaDiam = p.diam;
            end
            
            if (obj.order > 1)
                % Current axe's lca corresponds to the OffsetNode.
                % Therefore its position might have been changed.
                offset  = obj.lca.len;  % Parent/Ascending node radius
                % Surface position
                surfPos = obj.lca.coord + obj.growth_dir*offset;
            end
            
            % Iterative traversal along the current axe and recursive call
            % for ramifications.
            i = 0;
            while ~isempty(p.next)
                if (obj.order > 1)
                    % Update coordinates of the next node in the axe
                    % obs.: order-1 axes don't change position
                    p.next.coord = surfPos + i*(RootStruct.params.dl)*obj.growth_dir;
                end
                
                % Update diameter of the next node in the axe
                p.next.diam = RootStruct.getNextNodeDiameter(p);
                
                % Update geometry for the descending axes
                descDiam  = RootStruct.getBranchDiameter(p.diam);
                descCoord = p.next.coord;
                descLen   = p.next.diam/2;
                if isa(p.next,'ForkedNode')
                    if ~isempty(p.next.left)
                        p.next.left.updateGeometry(descCoord,descDiam,descLen);
                        p.next.left.axe.updateGeometry();
                    end
                    if ~isempty(p.next.right)
                        p.next.right.updateGeometry(descCoord,descDiam,descLen);
                        p.next.right.axe.updateGeometry();
                    end
                end
                if ~isempty(p.next.ramif)
                    for j = 1:length(p.next.ramif)
                        p.next.ramif(j).updateGeometry(descCoord,descDiam,descLen);
                        p.next.ramif(j).axe.updateGeometry();
                    end
                end
                
                p = p.next;
                i = i+1;
            end
        end
        
        function vol = getVolume(obj)
            % GETVOLUME() returns the total volume of the current axe and
            % all of its descendents.
            %
            % See also: UPDATEGEOMETRY, GETSEGMENTVOLUME.
            
            p = obj.lca;
            vol = 0;
            
            if (p.diam ~= obj.lastLcaDiam)
                error('Attempt to calculate the volume of an axe whose geometry hasn''t been updated');
            end
            
            while ~isempty(p)
                if (RootStruct.boundaryIsReached(p.coord,p.axe.order))
                    % To avoid that ramifications after this node that are
                    % within the boundaries contribute to the volume. Nodes
                    % are pruned from the first invalid node.
                    break
                end
                
                vol = vol + Axe.getSegmentVolume(p);
                
                if isa(p,'ForkedNode')
                    if ~isempty(p.left)
                        vol = vol + p.left.axe.getVolume();
                    end
                    if ~isempty(p.right)
                        vol = vol + p.right.axe.getVolume();
                    end
                end
                if ~isempty(p.ramif)
                    for i = 1:length(p.ramif)
                        vol = vol + p.ramif(i).axe.getVolume();
                    end
                end
                
                p = p.next;
            end
        end
        
        function prune(obj)
            % PRUNE() removes all the invalid nodes within the current axe 
            % and all its descendents, i.e. nodes with diameter smaller 
            % than a minimum or nodes that are outside the defined 
            % boundaries.
            % As this method is supposed to be used only after determining
            % the initial diameter that gives the desired final volume, it
            % also fills the node diameter set of the root struct.
            %
            % See also RootStruct/prune, pruneFromNode.
            
            % Two pointers (ant.next == p) for traversal
            ant = Node.empty();
            p = obj.lca;

            while (~isempty(p))
                if ((p.diam < RootStruct.params.min_diam) || ...
                    (RootStruct.boundaryIsReached(p.coord, p.axe.order)))
                    
                    obj.rootStruct.pruneFromNode(p);
                    if (~isempty(ant))
                        ant.next = Node.empty;
                    end
                    break;
                else
                    % Only add the diameter to the set when we know it's the
                    % final valid diameter
                    obj.rootStruct.addNodeDiamToSet(p);
                end

                if (isa(p,'ForkedNode'))
                    if (~isempty(p.left))
                        p.left.axe.prune();
                    end
                    if (~isempty(p.right))
                        p.right.axe.prune();
                    end
                end
                if (~isempty(p.ramif))
                    for i = 1:length(p.ramif)
                        p.ramif(i).axe.prune();
                    end
                end

                ant = p;
                p = p.next;
            end
        end
        
        %% Display methods
        function str = toStr(obj)
            % Method that returns the string containing the axe's id

            str = ['a' num2str(obj.id)];
        end
        
        function str = printAxe(obj)
            % Method to print the axe's structure according to the MTG code
            % syntax
            
            % Prints all the descendent nodes starting from 'obj.lca'. An
            % empty axe is passed as an argument, because it needs a
            % reference of an axe to verify if the starting node belongs to
            % it
            str = printNodesFromAxe(Axe.empty,obj.lca,false);
            disp(str)
        end
        
        function str = printNodesFromAxe(axe,node,bracketOpened)
            % Recursive method that prints the nodes in the axe starting by
            % the node 'node' according to the MTG file syntax
            %
            % See also PRINTAXE
            
            str = [];

            if ~isequal(node.axe,axe)
                % Entered a new axe
                str = [str node.axe.toStr '/']; 
                axe = node.axe;
            end
            str = [str node.toStr];

            if isa(node,'ForkedNode')
                if ~isempty(node.left)
                    str = [str '[+'];
                    bracketOpened = true;
                    str = [str printNodesFromAxe(axe, node.left, ...
                                                  bracketOpened)];
                end
                if ~isempty(node.right)
                    str = [str '[+'];
                    bracketOpened = true;
                    str = [str printNodesFromAxe(axe, node.right, ...
                                                  bracketOpened)];
                end
            end
            if ~isempty(node.ramif)
                for i = 1:length(node.ramif)
                    str = [str '[+'];
                    bracketOpened = true;
                    str = [str ...
                           printNodesFromAxe(axe,node.ramif(i),bracketOpened)];
                end
            end
            if ~isempty(node.next)
                if str(end) == ']'
                    str = [str '['];
                end
                str = [str '<' ...
                       printNodesFromAxe(axe,node.next,bracketOpened)];
            else
                if bracketOpened
                    str = [str ']'];
                end
            end
        end
        
        function str = printNodeCoords(obj)
            p = obj.lca;
            
            str = [obj.toStr ':' newline];
            while (~isempty(p))
                if (isa(p,'ForkedNode')) || (~isempty(p.ramif))
                    str = [str '*'];
                end
                str = [str p.toStr ': [' num2str(p.coord) ']' newline];
                p = p.next;
            end
        end
        
        function drawAxe(obj,drawNodes,drawEdges)
            % Method that draws the axe as a scatter 3D plot, where the 
            % points represents the nodes and the lines, the edges
            %
            % Important: hold off must be called after the method so that
            % others plot won't superpose to the drawing!
            
            nodeColor = rand(1,3);
            Axe.plotNodes(obj.lca,obj.lca,nodeColor,drawNodes,drawEdges);
            % obs.: As there is no edge before the first one, the edge will
            % be plotted between the lca node and itself
        end
        
        function pos = getPositioningStruct(obj)
            % getPositioningStruct() is a recursive method that returns a
            % struct array for positioning the axe (and all of its 
            % descendants) in space. Different lines of the array
            % correspond to different axes.
            % The required parameters to position each root segment of the
            % axes correspond to the Euler angles of rotation and the
            % translation (coordinate of the node/root segment), that can
            % be obtained from the node array of the axe.
            % 
            % Fields of the struct returned:
            %   - alpha : first Euler angle of rotation about the z-axis
            %   - beta  : second Euler angle of rotation about the new x'-axis
            %   - nodes : nodes belonging to the axe
            %
            % Obs: all the root segments belonging to one axe will have the
            % same orientation, and therefore, rotation.
            %
            % See also ROOTSTRUCT.GETEULERANGLES
            
            [alpha, beta] = RootStruct.getEulerAngles(obj.growth_dir);
            pos = struct('alpha',alpha,'beta',beta,'nodes',[]);
            
            p = obj.lca;
            n = obj.n_nodes;
            nodes = Node.empty(0,n);
            k = 1;
            while(~isempty(p))
                nodes(k) = p;
                
                pos2 = [];
                if ~isempty(p.ramif)
                    for i = 1:length(p.ramif)
                        pos3 = p.ramif(i).axe.getPositioningStruct();
                        pos2 = [pos2; pos3];
                    end
                end
                if isa(p,'ForkedNode')
                    if ~isempty(p.left)
                        pos3 = p.left.axe.getPositioningStruct();
                        pos2 = [pos2; pos3];
                    end
                    if ~isempty(p.right)
                        pos3 = p.right.axe.getPositioningStruct();
                        pos2 = [pos2; pos3];
                    end 
                end
                
                pos = [pos; pos2];
                
                p = p.next;
                k = k+1;
            end
            
            pos(1).nodes = nodes;
        end
    end
    
    %% Static methods
    methods(Static)
        function plotNodes(p,ant,nodeColor,drawNodes,drawEdges)
            % Recursive method that plots the nodes in the axe
            %
            % See also DRAWAXE
            
            hold on
            if drawNodes
                p.plot(nodeColor);
            end

            hold on
            if drawEdges
                n_points = 3; % number of points of the line plot
                p1 = ant.coord;
                p2 = p.coord;
                % "line equation" from p1 to p2: parametric equation, where 
                % linspace gives the varying parameter
                edge = repmat(p1,n_points,1) + ...
                        (linspace(0,1,n_points))'*(p2-p1);
                plot3(edge(:,1),edge(:,2),edge(:,3), ...
                      'Color', [139/255,69/255,19/255], 'LineWidth', 2);
            end

            % Call the plotNodes method for the next/ramification node
            if ~isempty(p.next)
                Axe.plotNodes(p.next,p,nodeColor,drawNodes,drawEdges);
            end
            if ~isempty(p.ramif)
                for i = 1:length(p.ramif)
                    Axe.plotNodes(p.ramif(i),p,nodeColor,drawNodes,drawEdges);
                end
            end
            if isa(p,'ForkedNode')
                if ~isempty(p.left)
                    Axe.plotNodes(p.left,p,nodeColor,drawNodes,drawEdges);
                end
                if ~isempty(p.right)
                    Axe.plotNodes(p.right,p,nodeColor,drawNodes,drawEdges);
                end 
            end
        end
        
        function vol = getSegmentVolume(node)
            % GETSEGMENTVOLUME(node) returns the volume of the internode
            % starting from node (hip.: cilindrical segments).
            %
            % Obs. 1: the method returns zero if:
            %   - node is an OffsetNode;
            %   - node has no next node (no internode);
            %   - node diameter is smaller than the minimum defined;
            % Obs. 2: an error is displayed if the distance between node
            % and the next one doesn't correspond to dl.
            
            vol = 0;
            if (isa(node,'OffsetNode'))
                % OffsetNode is an interior node of the ascending axe.
                % Therefore it doesn't contribute to the total volume.
                return
            elseif (RootStruct.geomBoundaryIsReached(node.coord))
                % Node is outside the geometric boundaries
                return
            elseif (isempty(node.next))
                % Next node is empty => no internode => no segment volume
                return
            elseif (node.diam < RootStruct.params.min_diam)
                % Node diameter is smaller than the minimum
                return
            else
                dist = node.getDistance(node.next);
                err = 1E-6;
                if(abs(dist - RootStruct.params.dl) > err)
                    % Guarantee consistency of distances
                    error('Distance between consecutives nodes is not consistent.');
                end
                
                % Cilindrical segment volume calculation
                diam = node.diam;
                vol = (RootStruct.params.dl)*pi*(diam/2)^2;
            end
        end
    end
end