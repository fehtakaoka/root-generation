function enableUipanelParams(handles)
    % enableUipanelParams(handles) enables all of the GUI handles inside
    % the 'User-defined' option for the creation of a root structure.
    %
    % See also DISABLEUIPANELPARAMS.

    set(handles.editNbApices,'enable','on')
    set(handles.checkboxTapRoot,'enable','on')
    set(handles.checkboxStochastic,'enable','on')
    set(handles.checkboxForkEnable,'enable','on')
    
    if(get(handles.checkboxTapRoot,'Value'))
        set(handles.checkboxBranchTap,'enable','on')
        set(handles.checkboxTaper,'enable','on')
    end
end