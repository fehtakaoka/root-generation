function disableUipanelParams(handles)
    % disableUipanelParams(handles) disables all of the GUI handles inside
    % the 'User-defined' option for the creation of a root structure.
    %
    % See also ENABLEUIPANELPARAMS.

    set(handles.editNbApices,'enable','off')
    set(handles.checkboxTapRoot,'enable','off')
    set(handles.checkboxStochastic,'enable','off')
    set(handles.checkboxBranchTap,'enable','off')
    set(handles.checkboxTaper,'enable','off')
    set(handles.checkboxForkEnable,'enable','off')
end