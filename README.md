# DistanceParallel Rhino Command
![icons_](/dev/icons/Distance_Parallel_Icon.png)
DistanceParallel is a custom python command for [Rhinoceros 3d CAD modeler](https://www.rhino3d.com) that measures the distance between two parallel planar surfaces.

* v0.5.1.1
* Tested on Rhino V6 for Mac
* Tested on Rhino V7-beta for Mac
* Untested on Windows

## Utilization
Start the command by typing _DistanceParallel_ into the command line. Select two parallel planar surfaces to measure the distance between them. The distance will be reported in the _command history panel_. The measurement will also be added to your clipboard (untested on Windows).

![animated gif](/assets/DistanceParallel-Usage1.gif?raw=true)

### Command Line Options
* ##### Unlock layers and Objects - beta
  Temporarily unlock all visible objects and unlock layers to allow surface selection. Unlocked objects and layers will be relocked on completion of the command. This feature has not been thoroughly tested. If the script crashes it will leave layers and objects unlocked. Use with caution and test to your satisfaction on non critical work.
* ##### Results in Message Box
  Display result in a pop-up message box. The value of the measurement will be added to your clipboard (untested on Windows)

**Caveats:**
If the selected surfaces are not planar or parallel within the document tolerance, the command will report and terminate.

Surfaces within blocks are not always selectable. Polysurfaces can be selected, extrusions cannot. Explode blocks if necessary.

Meshes are not currently selectable for measurement.

## Installation
1. Download and the _**dev**_ folder and unzip if necessary.
2. Create a folder called _**DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}**_ inside of the Rhino _**PythonPlugIns**_ folder. Create the _PythonPlugIns_ folder if it doesn't already exist.
  * Mac: ~/Library/Application Support/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}
  * Win: C:/Users/\<username\>/AppData/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}

5. Put the _**dev**_ folder and all of its contents into _**DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}**_.
4. Restart Rhinoceros
5. Run the command by typing DistanceParallel in Rhino's command line.

#### Optional: Add the command to a tool palette
Add the DistanceParallel command to a tool palette by creating a custom button.

The icon for the command can be found in the command _dev/icons_ folder.
* Mac: _Distance_Parallel_Icon.**pdf**_
* Windows: _Distance_Parallel_Icon.**png**_

Add "_!\_DistanceParallel_" to the script/macro editor for your custom button.
![](/assets/DistanceParallel_Button_Script.png?raw=true)

For more information on creating custom tool bars/palettes:

[Customize Tool Palettes (Mac en-us)](https://docs.mcneel.com/rhino/6mac/help/en-us/index.htm#macpreferencesandsettings/commands.htm)

[Customize Tool Palettes (Windows en-us)](https://docs.mcneel.com/rhino/7/help/en-us/index.htm#toolbarsandmenus/customize_toolbars.htm)

## Support Continued Development
If you find this plugin useful please donate to show your support for continued development.

##### Future enhancements
* Test on Windows
* Test in Rhino 8
* Measure between planar meshes
* Tolerance settings
* Unit conversions
* Rewrite in C#
* Improve selection highlighting
* Create Installer and or
* Work with Rhino Package Manager
* Add additional measurements

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=ME5KQ5YZJ9VM2)
\$3, \$7 or \$11 to MonSalon

## About
* Copyright ©2020 Matt Monforte. All Rights Reserved.
* [MonSalon.org](https://monsalon.org) Web Development
* [ClickWhirDing.com](https://ClickWhirDing.com) Tinkering

## License
You can redistribute it and/or modify it under the terms of the GNU Lesser General Public License version 3 as published by the Free Software Foundation. https://www.gnu.org/licenses/
