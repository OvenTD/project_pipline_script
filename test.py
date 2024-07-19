import maya.cmds as cmds
import maya.mel as mel
import os

# # As mentioned in the OP, you will need to source the following scripts (working in Maya 2018)
# MAYA_LOCATION = os.environ['MAYA_LOCATION']
# mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikGlobalUtils.mel"')
# mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikCharacterControlsUI.mel"')
# mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikDefinitionOperations.mel"')

# This queries all the menu items via DAG path (I believe)
allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)

# This will iterate over each menu item in the dropdown list until it hits the desired imported mocap rig name
# and changes the source rig to your mocap rig
i = 1
for item in allSourceChar:
	# This is the name of the option menu that lives in the HIK window globally
	optMenu = "hikSourceList|OptionMenu"
	sourceChar = cmds.menuItem(item, query=True, label=True)
	print(sourceChar)
	# IMPORTANT! On this check, notice the space before "newSourceHere"; I found this is how the dropdown 
    # menu in HIK stores the different strings so be sure to include that first space before your string
	if sourceChar == " MotionCaptureHumanIK":
		cmds.optionMenu(optMenu, edit=True, select=i)
		mel.eval('hikUpdateCurrentSourceFromUI()')
		mel.eval('hikUpdateContextualUI()')
		mel.eval('hikControlRigSelectionChangedCallback')
		break
			
	i+=1