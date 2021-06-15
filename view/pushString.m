function pushString(listbox,str)
    % pushString(listbox,str) pushes the string str to the output listbox
    % of the GUI
    %
    % See also CLEAROUTPUT.

    contents = get(listbox,'String');
    if isa(contents,'cell')
        contents{end+1} = str;
    else
        contents = {contents; str};
    end
    index = size(contents,1);

    set(listbox,'String',contents);
    set(listbox,'Value',index);
end