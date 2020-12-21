
DistanceParallel is a python command for Rhino that provides a quick measurement of the distance between two parallel planar surfaces. The command can temporarily all unlock layers and objects to allow selection of surfaces.

v0.5.1
Installation
1. Download and unzip the folder
2. Move or copy the folder—DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}—into the Rhino "PythonPlugIns" folder. Create the "PythonPlugIns" folder if it doesn't already exist.

Mac: ~/Library/Application Support/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}
Win: C:/Users/<username>/AppData/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}

3. Restart Rhinoceros
4. Run the command by typing DistanceParallel in Rhino's command line.

Optionally add the command to a tool palette
Add the DistanceParallel command to a tool palette by creating a custom button. ￼The icon for the command can be found in the command dev/icons folder.

Mac: Distance_Parallel_Icon.pdf
Windows: Distance_Parallel_Icon.png

Add "!_DistanceParallel" to the script/macro editor for your custom button.

For more information on creating custom tool bars/palettes:
Customize Tool Palettes (Mac en-us)
Customize Tool Palettes (Windows en-us)

Utilization
Start the command by typing DistanceParallel into the command line. Select two parallel planar surfaces to measure the distance between them. The distance will be reported in the command history panel. The measurement will also be added to your clipboard (untested on Windows).
￼
Command Line Options
Unlock layers and Objects:
Temporarily unlock all visible objects and unlock layers to allow surface selection. Unlocked objects and layers will be relocked on completion of the command. This feature has not been thoroughly tested. If the script crashes it will leave layers and objects unlocked. Use with caution and test to your satisfaction on non critical work.

Results in Message Box:
Display result in a pop-up message box. The value of the measurement will be added to your clipboard (untested on Windows).

Caveats:

If the selected surfaces are not planar or parallel within the document tolerance, the command will report and terminate.
Surfaces within blocks are not always selectable. Polysurfaces can be selected, extrusions cannot. Explode blocks if necessary.
Meshes are not currently selectable for measurement.

Support Continued Development
If you find this plugin useful please donate to show your support for continued development.

About
Copyright ©2020 Matt Monforte. All Rights Reserved.

License
You can redistribute it and/or modify it under the terms of the GNU Lesser General Public License version 3 as published by the Free Software Foundation. https://www.gnu.org/licenses/
