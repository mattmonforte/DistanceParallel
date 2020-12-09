# DistanceParallel Command
* version 0.5.0.2
* Copyright &copy;2020 Matt Monforte
* [ClickWhirDing.com](https://ClickWhirDing.com) Contract Engineering
* [MonSalon.org](https://monsalon.org) Web Development

DistanceParallel is a python command for [Rhinoceros 3d CAD modeling software](https://www.rhino3d.com) that measures the distance between two parallel planar surfaces.

Note: this custom command has only been tested in Mac version 6.0 and 7.0-beta of Rhinoceros.

## Installation
1. Download and unzip the _**dev**_ folder.
2. Create a folder called _**DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}**_ inside of the Rhino _**PythonPlugIns**_ folder. Create the _PythonPlugIns_ folder if it doesn't already exist.
  * Mac: ~/Library/Application Support/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}
  * Win: C:/Users/\<username\>/AppData/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}

5. Put the _**dev**_ folder and all of its contents into _**DistanceParallel{c92ade5c-25c3-4adf-be7c-f64c5609bff2}**_.
4. Restart Rhinoceros
5. Run the command by typing DistanceParallel in Rhino's command line.

##### Optional: Add the command to a tool palette
Add the DistanceParallel command to a tool palette by creating a custom button.
![](/dev/icons/Distance_Parallel_Icon.png?raw=true)
The icon for the command can be found in the command _dev/icons_ folder.
* Mac: _Distance_Parallel_Icon.**pdf**_
* Windows: _Distance_Parallel_Icon.**png**_

Add "_!\_DistanceParallel_" to the script/macro editor for your custom button.
![](/assets/DistanceParallel_Button_Script.png?raw=true)

For more information on creating custom tool bars/palettes:
[Customize Tool Palettes (Mac en-us)](https://docs.mcneel.com/rhino/6mac/help/en-us/index.htm#macpreferencesandsettings/commands.htm)
[Customize Tool Palettes (Windows en-us)](https://docs.mcneel.com/rhino/7/help/en-us/index.htm#toolbarsandmenus/customize_toolbars.htm)

## Utilization
Start the command by typing _DistanceParallel_ into the command line. Select two parallel planar surfaces to measure the distance between them. The distance will be reported in the _command history panel_. The measurement will also be added to your clipboard (untested on Windows).

![](/assets/DistanceParallel-Usage2.gif?raw=true)

#### Command Line Options
* ##### Unlock layers and Objects - beta
  Temporarily unlock all visible objects and unlock layers to allow surface selection. Unlocked objects and layers will be relocked on completion of the command. This feature has not been thoroughly tested. If the script crashes it will leave layers and objects unlocked. Use with caution and test to your satisfaction on non critical work.
* ##### Results in Message Box
  Display result in a pop-up message box. The value of the measurement will be added to your clipboard (untested on Windows)


**Notes:**
If the selected surfaces are not planar or parallel within the document tolerance, the command will report and terminate.

Surfaces within blocks are not always selectable. Polysurfaces can be selected, extrusions cannot. Explode blocks if necessary.

Meshes are not currently selectable for measurement.

## Support Continued Development
If you find this plugin useful please donate to show your support for continued development.

##### Future enhancements
* Test on Windows
* Test in Rhino 8
* Measure between planar meshes
* Unit conversions
* Rewrite in C#
* Improve selection highlighting
* Create Installer and or
* Work with Rhino Package Manager
* Add additional measurements

<form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="hosted_button_id" value="ME5KQ5YZJ9VM2" />
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
</form>
$3, $7 or $11

## License
You can redistribute it and/or modify it under the terms of the GNU Lesser General Public License version 3 as published by the Free Software Foundation. https://www.gnu.org/licenses/
