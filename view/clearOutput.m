function clearOutput(listboxOutput)
    % clearOutput(listboxOutput) clears the output listbox of the GUI.
    %
    % See also PUSHSTRING.
    
    contents = {};
    index = 1;

    set(listboxOutput,'String',contents);
    set(listboxOutput,'Value',index);
end