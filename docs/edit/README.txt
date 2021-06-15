RootGen documentation readme

In order to generate automatically a new uml for the class diagram:
  - Use the m2uml Matlab program:
    - Use "addpath()", to add the path to the model package of the RootGen program, so that Matlab knows where the class files are.
    - Run the following code: "[~] = m2uml.run(<class_diagram_title>,{<class1>,<class2>,...},{<arrows>})"
      - Where <class_diagram_title>, <class1>, <class2>, ..., <arrows>, should be changed
    - For more information, please refer to: https://www.mathworks.com/examples/matlab/community/19411-m2uml-generates-uml-class-diagrams#5

In order to edit the documentation:
  - Open "class_diagram.uml" with an text editor;
    - For syntax, please refer to: http://plantuml.com
    - To export the associated .svg file, go to https://www.planttext.com
    - To export the associated .pdf, convert the .svg file to a .pdf file
  - Open "Representation of classes.pages" with Pages;