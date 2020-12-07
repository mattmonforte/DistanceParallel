# DistanceParallel Command
* version 0.5.0.1
* Copyright &copy;2020 Matt Monforte
* [ClickWhirDing.com](https://ClickWhirDing.com) Contract Engineering
* [MonSalon.org](https://monsalon.org) Web Developement

DistanceParallel is a python command for [Rhinoceros 3d CAD modeling software](https://www.rhino3d.com) that measures the distance between two parallel planar surfaces.-


## Installation
1. Download and unzip the folder .
2. Move or copy the unzipped folder (DistanceParallel {guid}) into the Rhino _PythonPlugIns_ folder. Create the folder if it doesn't already exist.
  * Mac: ~/Library/Application Support/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel {guid}
  * Win: C:/Users/<username>/AppData/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/DistanceParallel {guid}
4. Restart Rhinoceros
5. Run the command by typing DistanceParallel in Rhino's command line.

##### Optional: Add the command to a tool palette

Add the DistanceParallel command to a tool palette by creating a custom button.
![](/dev/icons/Distance_Parallel_Icon.png?raw=true)
The icon for the command can be found in the command _dev/icons_ folder.
Use the _Distance_Parallel_Icon.**pdf**_ file for Mac and the _Distance_Parallel_Icon.**png**_ file for Windows.

Add _!\_DistanceParallel_ to the script/macro editor for your custom button.
![](/assets/DistanceParallel_Button_Script.png?raw=true)

For more information on creating custom tool bars/palettes:
[Customize Tool Palettes (Mac en-us)](https://docs.mcneel.com/rhino/6mac/help/en-us/index.htm#macpreferencesandsettings/commands.htm)
[Customize Tool Palettes (Windows en-us)](https://docs.mcneel.com/rhino/7/help/en-us/index.htm#toolbarsandmenus/customize_toolbars.htm)


## Usage

Start the command by typing _DistanceParallel_ into the command line. Select two surfaces to measure the distance between. The distance will be reported in the history and optionally in a popup window. The measurement will also be added to your clipboard (untested on widows).

Unlock layers and Objects

Popup results



## Support Continued Development
If you find this plugin useful please donate to show your support for continued development.

##### Future enhancements
* Test on Windows
* Test in Rhino 8
* Measure distance between planar meshes
* Rewrite in C#
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
