function varargout = RootGen(varargin)
% ROOTGEN MATLAB code for RootGen.fig
%      ROOTGEN, by itself, creates a new ROOTGEN or raises the existing
%      singleton*.
%
%      H = ROOTGEN returns the handle to a new ROOTGEN or the handle to
%      the existing singleton*.
%
%      ROOTGEN('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ROOTGEN.M with the given input arguments.
%
%      ROOTGEN('Property','Value',...) creates a new ROOTGEN or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Ro otGen_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to RootGen_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Last Modified by GUIDE v2.5 20-Sep-2018 12:27:45

% Begin initialization code - DO NOT CHANGE
addpath(genpath(pwd));
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @RootGen_OpeningFcn, ...
                   'gui_OutputFcn',  @RootGen_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT CHANGE


% --- Executes just before RootGen is made visible.
function RootGen_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to RootGen (see VARARGIN)

% Choose default command line output for RootGen
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes RootGen wait for user response (see UIRESUME)
% uiwait(handles.RootGen);

handles.rootStruct = RootStruct.empty();
handles.params     = RootStruct.params.empty();
guidata(hObject,handles) % save the changes to the structure

% --- Outputs from this function are returned to the command line.
function varargout = RootGen_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


function editNbApices_Callback(hObject, eventdata, handles)
% hObject    handle to editNbApices (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editNbApices as text
%        str2double(get(hObject,'String')) returns contents of editNbApices as a double


% --- Executes during object creation, after setting all properties.
function editNbApices_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editNbApices (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: options controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonOK.
function pushbuttonOK_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonOK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

set(handles.pushbuttonFill,'enable','off');

validEntries = true;
if get(handles.radiobuttonUserDef,'Value')
    if isempty(get(handles.editNbApices,'String'))
        str = '-> Enter a number of initial apices';
        pushString(handles.listboxOutput,str);
        validEntries = false;
    else
        params = struct('n_laterals',   str2double(get(handles.editNbApices,'String')), ...
                        'tap_root',     logical(get(handles.checkboxTapRoot,'Value')), ...
                        'stochastic',   logical(get(handles.checkboxStochastic,'Value')), ...
                        'branch_tap',   logical(get(handles.checkboxBranchTap,'Value')), ...
                        'taper_enable', logical(get(handles.checkboxTaper,'Value')), ...
                        'fork_enable',  logical(get(handles.checkboxForkEnable,'Value')));

        handles.params.loadParams('userdef',params);
    end
elseif get(handles.radiobuttonPreDef,'Value')
    contents = cellstr(get(handles.popupmenuPreDef,'String'));
    predefRootStruct = contents{get(handles.popupmenuPreDef,'Value')};
    
    handles.params = Parameters('predef',predefRootStruct);
elseif get(handles.radiobuttonFromFile,'Value')
    contents = cellstr(get(handles.popupmenuFromFile,'String'));
    fileRootStruct = contents{get(handles.popupmenuFromFile,'Value')};
    
    handles.params = Parameters('predef',fileRootStruct);
end

guidata(hObject, handles);

if validEntries
    cla
    campos(RootStruct.defaultView);
    clearOutput(handles.listboxOutput);
    
    handles.rootStruct = RootStruct(handles.params);
    guidata(hObject,handles) % save the changes to the structure
    
    str = '---------------- / RootGen Application Output / ----------------';
    pushString(handles.listboxOutput,str);
    str = '-> Root structure created.';
    pushString(handles.listboxOutput,str);
    
    set(handles.pushbuttonStepGrow,'enable','on');
    set(handles.pushbuttonGrowth,'enable','on');
    set(handles.pushbuttonPrint,'enable','on');
    set(handles.pushbuttonDraw,'enable','on');
    set(handles.checkboxNodes,'enable','on');
    set(handles.checkboxEdges,'enable','on');
    set(handles.checkboxBoundary,'enable','on');
    
    clearAndUpdatePropTable(handles.propTable);
end


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over editNbApices.
function editNbApices_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to editNbApices (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on key press with focus on editNbApices and none of its controls.
function editNbApices_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to editNbApices (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbuttonPrint.
function pushbuttonPrint_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonPrint (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
r   = handles.rootStruct;
str = printRootStruct(r);

pushString(handles.listboxOutput,str);


% --- Executes on button press in pushbuttonDraw.
function pushbuttonDraw_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonDraw (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
r = handles.rootStruct;
drawNodes    = get(handles.checkboxNodes,'Value');
drawEdges    = get(handles.checkboxEdges,'Value');
drawBoundary = get(handles.checkboxBoundary,'Value');

cla

if r.defaultView == campos
    % The user didn't change the camera position
    drawRootStruct(r,drawNodes,drawEdges,drawBoundary);
else
    drawRootStruct(r,drawNodes,drawEdges,drawBoundary,campos);
end


% --- Executes on button press in pushbuttonFill.
function pushbuttonFill_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonFill (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
r   = handles.rootStruct;
str = fill(r);

pushString(handles.listboxOutput,str);
setInPropTable(handles.propTable, ...
                'n_nodes',num2str(r.glbNodeIndex), ...
                'n_axis',num2str(r.glbAxeIndex), ...
                'vol',[num2str(r.finalVolume, '%1.5f') ' m^3']);



% --- Executes on button press in pushbuttonGrowth.
function pushbuttonGrowth_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonGrowth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
r   = handles.rootStruct;
str = '-> Starting growing process from the initial apices ...';
pushString(handles.listboxOutput,str);
grow(r);
str = '-> Growing process ended successifully.';
pushString(handles.listboxOutput,str);

set(handles.pushbuttonFill,'enable','on');

setInPropTable(handles.propTable, ...
               'n_nodes',num2str(r.glbNodeIndex), ...
               'n_axis', num2str(r.glbAxeIndex));


% --- Executes on button press in checkboxNodes.
function checkboxNodes_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxNodes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxNodes


% --- Executes on button press in checkboxEdges.
function checkboxEdges_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxEdges (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxEdges


% --- Executes on button press in checkboxBoundary.
function checkboxBoundary_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxBoundary (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxBoundary


% --- Executes on selection change in listboxOutput.
function listboxOutput_Callback(hObject, eventdata, handles)
% hObject    handle to listboxOutput (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns listboxOutput contents as cell array
%        contents{get(hObject,'Value')} returns selected item from listboxOutput


% --- Executes during object creation, after setting all properties.
function listboxOutput_CreateFcn(hObject, eventdata, handles)
% hObject    handle to listboxOutput (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonClear.
function pushbuttonClear_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonClear (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
clearOutput(handles.listboxOutput);


% --------------------------------------------------------------------
function File_Callback(hObject, eventdata, handles)
% hObject    handle to File (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function ExportMTG_Callback(hObject, eventdata, handles)
% hObject    handle to ExportMTG (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function Options_Callback(hObject, eventdata, handles)
% hObject    handle to Options (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function Help_Callback(hObject, eventdata, handles)
% hObject    handle to Help (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function About_Callback(hObject, eventdata, handles)
% hObject    handle to About (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
openfig('about');

% --------------------------------------------------------------------
function ChangeConsts_Callback(hObject, eventdata, handles)
% hObject    handle to ChangeConsts (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
params = ChangeConstGUI(handles.params);
handles.params = params;
guidata(hObject, handles);
clearAndUpdatePropTable(handles.propTable);


% --- Executes during object creation, after setting all properties.
function propTable_CreateFcn(hObject, eventdata, handles)
% hObject    handle to propTable (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
m = size(get(hObject,'Data'),1);
t = cell(m,1);
for i = 1:m
    t{i} = '???';
end
set(hObject,'Data',t);

% --- Executes when entered data in editable cell(s) in propTable.
function propTable_CellEditCallback(hObject, eventdata, handles)
% hObject    handle to propTable (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.TABLE)
%	Indices: row and column indices of the cell(s) edited
%	PreviousData: previous data for the cell(s) edited
%	EditData: string(s) entered by the user
%	NewData: EditData or its converted form set on the Data property. Empty if Data was not changed
%	Error: error string when failed to convert EditData to appropriate value for Data
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbuttonStepGrow.
function pushbuttonStepGrow_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonStepGrow (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
r   = handles.rootStruct;

if r.numberOfActiveAxes > 0
    stepGrow(r);
    str = '-> Step growth completed';
else
    str = '-> Root structure is already totally grown';
    set(handles.pushbuttonFill,'enable','on');
end

pushString(handles.listboxOutput,str);
setInPropTable(handles.propTable, ...
               'n_nodes',num2str(r.glbNodeIndex), ...
               'n_axis', num2str(r.glbAxeIndex));

r = handles.rootStruct;
drawNodes    = get(handles.checkboxNodes,'Value');
drawEdges    = get(handles.checkboxEdges,'Value');
drawBoundary = get(handles.checkboxBoundary,'Value');

cla

if r.defaultView == campos
    % The user didn't change the camera position
    drawRootStruct(r,drawNodes,drawEdges,drawBoundary);
else
    drawRootStruct(r,drawNodes,drawEdges,drawBoundary,campos);
end


% --- Executes on button press in radiobuttonTapRoot.
function radiobuttonTapRoot_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonTapRoot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonTapRoot
set(handles.checkboxTaper,'enable','on');
set(handles.editNbApices,'enable','off');


% --- Executes on button press in radiobuttonN0.
function radiobuttonN0_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonN0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonN0
set(handles.checkboxTaper,'enable','off');
set(handles.editNbApices,'enable','on');


% --- Executes on button press in checkboxTaper.
function checkboxTaper_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxTaper (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxTaper


% --- Executes during object creation, after setting all properties.
function RootStructPlot_CreateFcn(hObject, eventdata, handles)
% hObject    handle to RootStructPlot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: place code in OpeningFcn to populate RootStructPlot
campos(RootStruct.defaultView);


% --- Executes during object creation, after setting all properties.
function RootGen_CreateFcn(hObject, eventdata, handles)
% hObject    handle to RootGen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes on selection change in popupmenuPreDef.
function popupmenuPreDef_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenuPreDef (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenuPreDef contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenuPreDef


% --- Executes during object creation, after setting all properties.
function popupmenuPreDef_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenuPreDef (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

predefParamsFiles = dir('parameters/predef/*.mat');
predefParamsFiles = {predefParamsFiles.name}';
for i = 1:length(predefParamsFiles)
    predefParamsFiles{i} = predefParamsFiles{i}(1:end-4);
end

set(hObject,'String',predefParamsFiles);


% --- Executes on button press in radiobuttonUserDef.
function radiobuttonUserDef_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonUserDef (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonUserDef
enableUipanelParams(handles);
set(handles.ChangeConsts,'enable','on');
set(handles.popupmenuPreDef,'enable','off');
set(handles.popupmenuFromFile,'enable','off');

if(isempty(handles.rootStruct))
    handles.params = Parameters();
else
    handles.params = handles.rootStruct.params;
end
guidata(hObject, handles);

% --- Executes on button press in radiobuttonPreDef.
function radiobuttonPreDef_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonPreDef (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonPreDef
set(handles.popupmenuPreDef,'enable','on');
set(handles.popupmenuFromFile,'enable','off');
set(handles.ChangeConsts,'enable','off');
disableUipanelParams(handles);


% --- Executes on button press in checkboxTapRoot.
function checkboxTapRoot_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxTapRoot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxTapRoot
if get(hObject, 'Value')
    set(handles.checkboxBranchTap,'enable','on')
    set(handles.checkboxTaper,'enable','on')
else
    set(handles.checkboxBranchTap,'enable','off')
    set(handles.checkboxTaper,'enable','off')
end


% --- Executes on button press in checkboxStochastic.
function checkboxStochastic_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxStochastic (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxStochastic


% --- Executes on button press in checkboxBranchTap.
function checkboxBranchTap_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxBranchTap (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxBranchTap


% --- Executes on button press in checkboxForkEnable.
function checkboxForkEnable_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxForkEnable (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxForkEnable


% --- Executes on selection change in popupmenuFromFile.
function popupmenuFromFile_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenuFromFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenuFromFile contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenuFromFile


% --- Executes during object creation, after setting all properties.
function popupmenuFromFile_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenuFromFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in radiobuttonFromFile.
function radiobuttonFromFile_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonFromFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonFromFile
set(handles.popupmenuFromFile,'enable','on');
set(handles.popupmenuPreDef,'enable','off');
set(handles.ChangeConsts,'enable','off');
disableUipanelParams(handles);

savedParamsFiles = dir('parameters/saved/*.mat');
savedParamsFiles = {savedParamsFiles.name}';
savedParamsFiles = ['Select a MAT-file';savedParamsFiles];
for i = 2:length(savedParamsFiles)
    savedParamsFiles{i} = savedParamsFiles{i}(1:end-4);
end

set(handles.popupmenuFromFile,'String',savedParamsFiles);


% --------------------------------------------------------------------
function WorkspaceOutput_Callback(hObject, eventdata, handles)
% hObject    handle to WorkspaceOutput (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str = '-> No RootStruct object still created.';

if isfield(handles,'rootStruct')
    str = '-> RootStruct object exported to the workspace as the variable ''r''.';
	assignin('base', 'r', handles.rootStruct);
end

pushString(handles.listboxOutput,str);


% --------------------------------------------------------------------
function GenScript_Callback(hObject, eventdata, handles)
% hObject    handle to GenScript (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
GenerateScript_handle = [];

if isfield(handles,'rootStruct')
    % open GenerateScript and save the handle
    GenerateScript_handle = GenerateScript();
    % obtain data in GenerateScript_handle
    GenerateScript_data = guidata(GenerateScript_handle);
    % add field for root structure
    GenerateScript_data.rootStruct = handles.rootStruct;
    % save the GenerateScript data 
    guidata(GenerateScript_handle, GenerateScript_data);
else
    pushString(handles.listboxOutput,'-> No RootStruct object still created.');
end


% --------------------------------------------------------------------
function WriteParams_Callback(hObject, eventdata, handles)
% hObject    handle to WriteParams (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

str = SaveParamsGUI(handles.params);
if(~isempty(str))
    pushString(handles.listboxOutput,str);
end



function edit3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3 as text
%        str2double(get(hObject,'String')) returns contents of edit3 as a double


% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
