function varargout = ChangeConstGUI(varargin)
% CHANGECONSTGUI MATLAB code for ChangeConstGUI.fig
%      CHANGECONSTGUI, by itself, creates a new CHANGECONSTGUI or raises the existing
%      singleton*.
%
%      H = CHANGECONSTGUI returns the handle to a new CHANGECONSTGUI or the handle to
%      the existing singleton*.
%
%      CHANGECONSTGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CHANGECONSTGUI.M with the given input arguments.
%
%      CHANGECONSTGUI('Property','Value',...) creates a new CHANGECONSTGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ChangeConstGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ChangeConstGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ChangeConstGUI

% Last Modified by GUIDE v2.5 11-Sep-2018 17:22:53

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ChangeConstGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @ChangeConstGUI_OutputFcn, ...
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


% --- Executes just before ChangeConstGUI is made visible.
function ChangeConstGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ChangeConstGUI (see VARARGIN)

% Choose default command line output for ChangeConstGUI
handles.output = hObject;

handles.originalParams = varargin{1};
handles.validOutput = false;

% Update handles structure
guidata(hObject, handles);

% Handle no structure being passed to GUI
if nargin<4
    set(handles.editMax_radius,'String','???');
    set(handles.editMax_depth,'String','???');
    set(handles.editMax_order,'String','???');
    set(handles.editFixed_volume,'String','???');
    set(handles.editMin_diam,'String','???');
    set(handles.editL_branch,'String','???');
    set(handles.editL_fork,'String','???');
    set(handles.editBrcDRatio,'String','???');
    set(handles.editHv_distr,'String','???');
    set(handles.editDl,'String','???');
else
    set(handles.editMax_radius,'String',num2str(varargin{1}.max_radius));
    set(handles.editMax_depth,'String',num2str(varargin{1}.max_depth));
    set(handles.editMax_order,'String',num2str(varargin{1}.max_order));
    set(handles.editFixed_volume,'String',num2str(varargin{1}.fixed_volume));
    set(handles.editMin_diam,'String',num2str(varargin{1}.min_diam));
    set(handles.editL_branch,'String',num2str(varargin{1}.L_branch));
    set(handles.editL_fork,'String',num2str(varargin{1}.L_fork));
    set(handles.editBrcDRatio,'String',num2str(varargin{1}.brcDRatio));
    set(handles.editHv_distr,'String',num2str(varargin{1}.hv_distr));
    set(handles.editDl,'String',num2str(varargin{1}.dl));
end

% UIWAIT makes ChangeConstGUI wait for user response (see UIRESUME)
uiwait(handles.figure1);

% --- Outputs from this function are returned to the command line.
function varargout = ChangeConstGUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

params = struct('max_radius',   str2double(get(handles.editMax_radius,'String')), ...
                'max_depth',    str2double(get(handles.editMax_depth,'String')), ...
                'max_order',    str2double(get(handles.editMax_order,'String')), ...
                'fixed_volume', str2double(get(handles.editFixed_volume,'String')), ...
                'min_diam',     str2double(get(handles.editMin_diam,'String')), ...
                'L_branch',     str2double(get(handles.editL_branch,'String')), ...
                'L_fork',       str2double(get(handles.editL_fork,'String')), ...
                'brcDRatio',    str2double(get(handles.editBrcDRatio,'String')), ...
                'hv_distr',     str2double(get(handles.editHv_distr,'String')), ...
                'dl',           str2double(get(handles.editDl,'String')));

if(isempty(get(handles.editHv_distr,'String')))
    params.hv_distr = []; % hv_distr is not specified
end

if(handles.validOutput)
    varargout{1} = Parameters('userdef',params);
else
    varargout{1} = handles.originalParams;
end

delete(handles.figure1);


function editMax_radius_Callback(hObject, eventdata, handles)
% hObject    handle to editMax_radius (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editMax_radius as text
%        str2double(get(hObject,'String')) returns contents of editMax_radius as a double


% --- Executes during object creation, after setting all properties.
function editMax_radius_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editMax_radius (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbuttonOK.
function pushbuttonOK_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonOK (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.validOutput = true;
guidata(hObject, handles);
if(isequal(get(handles.figure1,'waitstatus'),'waiting'))
    uiresume(handles.figure1);
else
    delete(handles.figure1);
end

% --- Executes on button press in pushbuttonCancel.
function pushbuttonCancel_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonCancel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if(isequal(get(handles.figure1,'waitstatus'),'waiting'))
    uiresume(handles.figure1);
else
    delete(handles.figure1);
end


function editL_fork_Callback(hObject, eventdata, handles)
% hObject    handle to editL_fork (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editL_fork as text
%        str2double(get(hObject,'String')) returns contents of editL_fork as a double


% --- Executes during object creation, after setting all properties.
function editL_fork_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editL_fork (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editBrcDRatio_Callback(hObject, eventdata, handles)
% hObject    handle to editBrcDRatio (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editBrcDRatio as text
%        str2double(get(hObject,'String')) returns contents of editBrcDRatio as a double


% --- Executes during object creation, after setting all properties.
function editBrcDRatio_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editBrcDRatio (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editHv_distr_Callback(hObject, eventdata, handles)
% hObject    handle to editHv_distr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editHv_distr as text
%        str2double(get(hObject,'String')) returns contents of editHv_distr as a double


% --- Executes during object creation, after setting all properties.
function editHv_distr_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editHv_distr (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editDl_Callback(hObject, eventdata, handles)
% hObject    handle to editDl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editDl as text
%        str2double(get(hObject,'String')) returns contents of editDl as a double


% --- Executes during object creation, after setting all properties.
function editDl_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editDl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editMax_depth_Callback(hObject, eventdata, handles)
% hObject    handle to editMax_depth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editMax_depth as text
%        str2double(get(hObject,'String')) returns contents of editMax_depth as a double


% --- Executes during object creation, after setting all properties.
function editMax_depth_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editMax_depth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editMax_order_Callback(hObject, eventdata, handles)
% hObject    handle to editMax_order (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editMax_order as text
%        str2double(get(hObject,'String')) returns contents of editMax_order as a double


% --- Executes during object creation, after setting all properties.
function editMax_order_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editMax_order (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editFixed_volume_Callback(hObject, eventdata, handles)
% hObject    handle to editFixed_volume (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editFixed_volume as text
%        str2double(get(hObject,'String')) returns contents of editFixed_volume as a double


% --- Executes during object creation, after setting all properties.
function editFixed_volume_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editFixed_volume (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function editMin_diam_Callback(hObject, eventdata, handles)
% hObject    handle to editMin_diam (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editMin_diam as text
%        str2double(get(hObject,'String')) returns contents of editMin_diam as a double


% --- Executes during object creation, after setting all properties.
function editMin_diam_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editMin_diam (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
if(isequal(get(handles.figure1,'waitstatus'),'waiting'))
    uiresume(handles.figure1);
else
    delete(handles.figure1);
end



function editL_branch_Callback(hObject, eventdata, handles)
% hObject    handle to editL_branch (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editL_branch as text
%        str2double(get(hObject,'String')) returns contents of editL_branch as a double


% --- Executes during object creation, after setting all properties.
function editL_branch_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editL_branch (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
