#Ziva Mirror
#1.0.1
#author Mitchell Mortenson

#Some code used from https://community.zivadynamics.com/d/46-mirror-the-tissues-and-attchments/13

#########INSTRUCTIONS##########
# 1. Copy all code
# 2. Paste into the Maya script editor under a Python tab
# 3. Click 'Execute'
# 4. (Optional) Click 'Save script to shelf' to save this script to your current shelf

from maya import cmds
import zBuilder.zMaya
import zBuilder.builders.ziva as zva

def lefttoright(args=none):
	zBuilder.zMaya.rename_ziva_nodes()
	selection = cmds.ls(sl = True)
	for obj in selection :
	    cmds.select(obj)
	    zObj = zva.Ziva()
	    zObj.retrieve_from_scene_selection()
	    zObj.string_replace( '^l_', 'r_' )
	    zObj.string_replace( '^L_', 'R_' )
	    zObj.string_replace( '_l_', '_r_' )
	    zObj.string_replace( '_L_', '_R_' )
	    zObj.build()

def righttoleft(args=none):
	zBuilder.zMaya.rename_ziva_nodes()
	selection = cmds.ls(sl = True)
	for obj in selection :
	    cmds.select(obj)
	    zObj = zva.Ziva()
	    zObj.retrieve_from_scene_selection()
	    zObj.string_replace( '^r_', 'l_' )
	    zObj.string_replace( '^R_', 'L_' )
	    zObj.string_replace( '_r_', '_l_' )
	    zObj.string_replace( '_R_', '_L_' )
	    zObj.build()

def ziva_mirrorUI():
	if(cmds.window('ziva_mirrorUI_ui',q=True,ex=True)):cmds.deleteUI('ziva_mirrorUI_ui')
	cmds.window('ziva_mirrorUI_ui',t=u'Ziva_Mirror')
	cmds.columnLayout(adj=True)
	cmds.menuBarLayout()
	cmds.button(l=u'L--->R',c=lefttoright)
	cmds.button(l=u'R--->L',c=righttoleft)
	cmds.showWindow('ziva_mirrorUI_ui')
ziva_mirrorUI()
