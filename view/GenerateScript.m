function varargout = GenerateScript(varargin)
% GENERATESCRIPT MATLAB code for GenerateScript.fig
%      GENERATESCRIPT, by itself, creates a new GENERATESCRIPT or raises the existing
%      singleton*.
%
%      H = GENERATESCRIPT returns the handle to a new GENERATESCRIPT or the handle to
%      the existing singleton*.
%
%      GENERATESCRIPT('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GENERATESCRIPT.M with the given input arguments.
%
%      GENERATESCRIPT('Property','Value',...) creates a new GENERATESCRIPT or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before GenerateScript_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to GenerateScript_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GenerateScript

% Last Modified by GUIDE v2.5 04-Oct-2018 16:01:06

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GenerateScript_OpeningFcn, ...
                   'gui_OutputFcn',  @GenerateScript_OutputFcn, ...
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
% End initialization code - DO NOT EDIT


% --- Executes just before GenerateScript is made visible.
function GenerateScript_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to GenerateScript (see VARARGIN)

% Choose default command line output for GenerateScript
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes GenerateScript wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = GenerateScript_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

function editRootGamma_Callback(hObject, eventdata, handles)
% hObject    handle to editRootGamma (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRootGamma as text
%        str2double(get(hObject,'String')) returns contents of editRootGamma as a double


% --- Executes during object creation, after setting all properties.
function editRootGamma_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRootGamma (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editRootV_Callback(hObject, eventdata, handles)
% hObject    handle to editRootV (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRootV as text
%        str2double(get(hObject,'String')) returns contents of editRootV as a double


% --- Executes during object creation, after setting all properties.
function editRootV_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRootV (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editRootE_Callback(hObject, eventdata, handles)
% hObject    handle to editRootE (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRootE as text
%        str2double(get(hObject,'String')) returns contents of editRootE as a double


% --- Executes during object creation, after setting all properties.
function editRootE_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRootE (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editRootMOR_Callback(hObject, eventdata, handles)
% hObject    handle to editRootMOR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRootMOR as text
%        str2double(get(hObject,'String')) returns contents of editRootMOR as a double


% --- Executes during object creation, after setting all properties.
function editRootMOR_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRootMOR (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit14_Callback(hObject, eventdata, handles)
% hObject    handle to edit14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit14 as text
%        str2double(get(hObject,'String')) returns contents of edit14 as a double


% --- Executes during object creation, after setting all properties.
function edit14_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilE_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilE (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilE as text
%        str2double(get(hObject,'String')) returns contents of editSoilE as a double


% --- Executes during object creation, after setting all properties.
function editSoilE_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilE (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
                



function editSoilV_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilV (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilV as text
%        str2double(get(hObject,'String')) returns contents of editSoilV as a double


% --- Executes during object creation, after setting all properties.
function editSoilV_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilV (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilGamma_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilGamma (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilGamma as text
%        str2double(get(hObject,'String')) returns contents of editSoilGamma as a double


% --- Executes during object creation, after setting all properties.
function editSoilGamma_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilGamma (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilPhi_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilPhi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilPhi as text
%        str2double(get(hObject,'String')) returns contents of editSoilPhi as a double


% --- Executes during object creation, after setting all properties.
function editSoilPhi_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilPhi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilC_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilC (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilC as text
%        str2double(get(hObject,'String')) returns contents of editSoilC as a double


% --- Executes during object creation, after setting all properties.
function editSoilC_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilC (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilPsi_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilPsi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilPsi as text
%        str2double(get(hObject,'String')) returns contents of editSoilPsi as a double


% --- Executes during object creation, after setting all properties.
function editSoilPsi_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilPsi (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilDepth_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilDepth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilDepth as text
%        str2double(get(hObject,'String')) returns contents of editSoilDepth as a double


% --- Executes during object creation, after setting all properties.
function editSoilDepth_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilDepth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editSoilLxLy_Callback(hObject, eventdata, handles)
% hObject    handle to editSoilLxLy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editSoilLxLy as text
%        str2double(get(hObject,'String')) returns contents of editSoilLxLy as a double


% --- Executes during object creation, after setting all properties.
function editSoilLxLy_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editSoilLxLy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit22_Callback(hObject, eventdata, handles)
% hObject    handle to edit22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit22 as text
%        str2double(get(hObject,'String')) returns contents of edit22 as a double


% --- Executes during object creation, after setting all properties.
function edit22_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit21_Callback(hObject, eventdata, handles)
% hObject    handle to edit21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit21 as text
%        str2double(get(hObject,'String')) returns contents of edit21 as a double


% --- Executes during object creation, after setting all properties.
function edit21_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit20_Callback(hObject, eventdata, handles)
% hObject    handle to edit20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit20 as text
%        str2double(get(hObject,'String')) returns contents of edit20 as a double


% --- Executes during object creation, after setting all properties.
function edit20_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in generateButton.
function generateButton_Callback(hObject, eventdata, handles)
% hObject    handle to generateButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
invalid = false;
sim_params = struct( ...
                     'rootE', str2double(get(handles.editRootE,'String')), ...
                     'rootV', str2double(get(handles.editRootV,'String')), ...
                     'rootGamma', str2double(get(handles.editRootGamma,'String')), ...
                     'rootMOR', str2double(get(handles.editRootMOR,'String')), ...
                     'rootSegmentTaper', get(handles.checkboxRSegTaper,'Value'), ...
                     'soilE', str2double(get(handles.editSoilE,'String')), ...
                     'soilV', str2double(get(handles.editSoilV,'String')), ...
                     'soilGamma', str2double(get(handles.editSoilGamma,'String')), ...
                     'soilPhi', str2double(get(handles.editSoilPhi,'String')), ...
                     'soilC', str2double(get(handles.editSoilC,'String')), ...
                     'soilPsi', str2double(get(handles.editSoilPsi,'String')), ...
                     'soilDepth', str2double(get(handles.editSoilDepth,'String')), ...
                     'soilLxLy', str2double(get(handles.editSoilLxLy,'String')), ...
                     'rigidBarHeight', str2double(get(handles.editRigidBarHeight,'String')), ...
                     'rigidBarLateralDispl', str2double(get(handles.editRigidBarLateralDispl,'String')) ...
                    );
                
fields = fieldnames(sim_params);
for i = 1:numel(fields)
    if (isnan(sim_params.(fields{i})))
        invalid = true;
    end
end

cont = 'Yes';
if (invalid)
    cont = invalidEntries;
end

if (strcmp(cont,'Yes'))
    filename    = get(handles.editFileName,'String');
    modelname   = get(handles.editModelName,'String');
    description = get(handles.editDescr,'String');
    use3Delem   = get(handles.checkbox3D,'Value');
    
    if (isempty(description))
        sg = ScriptGenerator(handles.rootStruct,sim_params,filename,modelname,use3Delem);
    else
        sg = ScriptGenerator(handles.rootStruct,sim_params,filename,modelname,use3Delem,description);
    end
    
    sg.generateScript();
    
    handles.output = filename;
    % Update handles structure
    guidata(hObject, handles);
    
    delete(handles.figure1);
end


function editRigidBarHeight_Callback(hObject, eventdata, handles)
% hObject    handle to editRigidBarHeight (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRigidBarHeight as text
%        str2double(get(hObject,'String')) returns contents of editRigidBarHeight as a double


% --- Executes during object creation, after setting all properties.
function editRigidBarHeight_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRigidBarHeight (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editRigidBarLateralDispl_Callback(hObject, eventdata, handles)
% hObject    handle to editRigidBarLateralDispl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRigidBarLateralDispl as text
%        str2double(get(hObject,'String')) returns contents of editRigidBarLateralDispl as a double


% --- Executes during object creation, after setting all properties.
function editRigidBarLateralDispl_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRigidBarLateralDispl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editDescr_Callback(hObject, eventdata, handles)
% hObject    handle to editDescr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editDescr as text
%        str2double(get(hObject,'String')) returns contents of editDescr as a double


% --- Executes during object creation, after setting all properties.
function editDescr_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editDescr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editModelName_Callback(hObject, eventdata, handles)
% hObject    handle to editModelName (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editModelName as text
%        str2double(get(hObject,'String')) returns contents of editModelName as a double
if (~isempty(get(hObject,'String')))
    set(hObject,'BackgroundColor',[1,1,1]);
else
    set(hObject,'BackgroundColor',[1,1,0.7]);
end

if (~isempty(get(handles.editModelName,'String')) && ...
        ~isempty(get(hObject,'String')))
	set(handles.generateButton,'enable','on');
else
    set(handles.generateButton,'enable','off');
end

% --- Executes during object creation, after setting all properties.
function editModelName_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editModelName (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editFileName_Callback(hObject, eventdata, handles)
% hObject    handle to editFileName (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editFileName as text
%        str2double(get(hObject,'String')) returns contents of editFileName as a double
if (~isempty(get(hObject,'String')))
    set(hObject,'backgroundColor',[1,1,1]);
else
    set(hObject,'backgroundColor',[1,1,0.7]);
end

if (~isempty(get(handles.editModelName,'String')) && ...
        ~isempty(get(hObject,'String')))
	set(handles.generateButton,'enable','on');
else
    set(handles.generateButton,'enable','off');
end

% --- Executes during object creation, after setting all properties.
function editFileName_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editFileName (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in checkboxSimDescr.
function checkboxSimDescr_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxSimDescr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxSimDescr
if (get(hObject,'Value'))
    set(handles.editDescr,'enable','on');
else 
    set(handles.editDescr,'enable','off');
end


% --- Executes on button press in checkboxRSegTaper.
function checkboxRSegTaper_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxRSegTaper (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxRSegTaper


% --- Executes on button press in checkbox3D.
function checkbox3D_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox3D (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox3D
