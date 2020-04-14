#1.0
#Some code used from https://community.zivadynamics.com/d/46-mirror-the-tissues-and-attchments/13

#########INSTRUCTIONS##########
#Copy and paste into maya script editor
#Run

from maya import cmds
import zBuilder.zMaya
import maya.cmds as mc
import zBuilder.builders.ziva as zva

def lefttoright(args=none):
	zBuilder.zMaya.rename_ziva_nodes()
	selection = mc.ls(sl = True)
	for obj in selection :
	    mc.select(obj)
	    zObj = zva.Ziva()
	    zObj.retrieve_from_scene_selection()
	    zObj.string_replace( '^l_', 'r_' )
	    zObj.string_replace( '^L_', 'R_' )
	    zObj.string_replace( '_l_', '_r_' )
	    zObj.string_replace( '_L_', '_R_' )
	    zObj.build()

def righttoleft(args=none):
	zBuilder.zMaya.rename_ziva_nodes()
	selection = mc.ls(sl = True)
	for obj in selection :
	    mc.select(obj)
	    zObj = zva.Ziva()
	    zObj.retrieve_from_scene_selection()
	    zObj.string_replace( '^r_', 'l_' )
	    zObj.string_replace( '^R_', 'L_' )
	    zObj.string_replace( '_r_', '_l_' )
	    zObj.string_replace( '_R_', '_L_' )
	    zObj.build()
        
def ziva_mirrorUI():
	if(cmds.window('window1_ui',q=True,ex=True)):cmds.deleteUI('window1_ui')
	cmds.window('window1_ui',t=u'Ziva_Mirror')
	cmds.columnLayout(adj=True)
	cmds.menuBarLayout()
	cmds.button(l=u'L--->R',c=lefttoright)
	cmds.button(l=u'R--->L',c=righttoleft)
	cmds.showWindow('window1_ui')
ziva_mirrorUI()
