#Export Cleanup
#v1.0
#author Mitchell Mortenson

#Install instructions

# 1. Copy all code 
# 2. Paste into the Maya script editor under a Python tab 
# 3. Click 'Execute'
# 4. (Optional) Click 'Save script to shelf' to save this script to your current shelf


from maya import cmds
import maya.mel as mel

def makeFaceted():
    selectedObjs = cmds.ls (sl = True, s = True, l = True, typ = 'transform')
    for eachObj in selectedObjs:
        cmds.setAttr((eachObj + '.displaySmoothMesh'), 0)

def freezeTransforms():
    mel.eval('performFreezeTransformations(0)')

def resetPivots():
    selectedObjs = cmds.ls (sl = True, s = True, l = True, typ = 'transform')
    if (cmds.checkBoxGrp ('freezeTransforms_ui', q = True, v1 = True)):
        mel.eval('ResetTransformations')
        mel.eval('setTRSPinPivot false')
        cmds.refresh()       
    else:
        for eachObj in selectedObjs:
            cmds.xform(ws = True, a = True, piv = (0,0,0))
            cmds.xform(ws = True, a = True, rp = (0,0,0))
            cmds.xform(ws = True, a = True, sp = (0,0,0))
            mel.eval('setTRSPinPivot false')
            cmds.refresh()

def ResetToDefaultShader():
    mel.eval('sets -e -forceElement initialShadingGroup')

def deleteUnusedNodes():
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')

def deleteAllHistory():
    mel.eval("DeleteHistory")

def deleteNonDeformerHistory():
    mel.eval('doBakeNonDefHistory( 1, {"prePost" })')

def deletePreDeformerHistory():
    mel.eval('doBakeNonDefHistory( 1, {"pre" })')

# def changeHistoryCheckBox():
# 	if (cmds.checkBoxGrp ('deleteHistory_ui', q = True, v1 = True)):
# 		cmds.radioButton('deleteAllHistory_ui', ed = True, en = True)
# 		cmds.radioButton('deleteNonDeformerHistory_ui', ed = True, en = True)
# 		cmds.radioButton('deletePreDeformerHistory_ui', ed = True, en = True)
# 	else:
# 		cmds.radioButton('deleteAllHistory_ui', ed = True, en = False)
# 		cmds.radioButton('deleteNonDeformerHistory_ui', ed = True, en = False)
# 		cmds.radioButton('deletePreDeformerHistory_ui', ed = True, en = False)

def run(*args):
    selectedObjs = cmds.ls (sl = True, s = True, l = True, typ = 'transform')
    if (selectedObjs):
        if (cmds.checkBoxGrp ('makeFaceted_ui', q = True, v1 = True)):
            makeFaceted()

        if (cmds.checkBoxGrp ('freezeTransforms_ui', q = True, v1 = True)):
            freezeTransforms()
        
        if (cmds.checkBoxGrp ('ResetPivots_ui', q = True, v1 = True)):
            resetPivots()

        if (cmds.checkBoxGrp ('ResetToDefaultShader_ui', q = True, v1 = True)):
            ResetToDefaultShader()

        if (cmds.checkBoxGrp ('deleteHistory_ui', q = True, v1 = True)):
            if cmds.radioButton('deleteAllHistory_ui', q = True, select = True):
                deleteAllHistory()
            
            elif cmds.radioButton('deleteNonDeformerHistory_ui', q = True, select = True):
                deleteNonDeformerHistory()

            elif cmds.radioButton('deletePreDeformerHistory_ui', q = True, select = True):
                deletePreDeformerHistory()
    else:
        print "Select at least one object"

    if (cmds.checkBoxGrp ('deleteUnusedNodes_ui', q = True, v1 = True)):
        deleteUnusedNodes()
        
def exportCleanup():
    if(cmds.window('window1_ui', q = True, ex = True)):
        cmds.deleteUI('window1_ui')
    cmds.window('window1_ui', t = u'Export Cleanup', s = False, tlb = True)
    cmds.columnLayout(adj = True)
    cmds.checkBoxGrp('makeFaceted_ui', ncb = 1, l1 = u'Make Faceted', v1 = True)
    cmds.checkBoxGrp('freezeTransforms_ui', ncb = 1, l1 = u'Freeze Transforms', v1 = True)
    cmds.checkBoxGrp('ResetPivots_ui', ncb = 1, l1 = u'Reset Pivots', v1 = True)
    cmds.checkBoxGrp('deleteHistory_ui', ncb = 1, l1 = u'Delete History', v1 = True)
    cmds.radioCollection()
    cmds.radioButton('deleteAllHistory_ui', l = u'All History', select = True)
    cmds.radioButton('deleteNonDeformerHistory_ui', l = u'Non-Deformer History')
    cmds.radioButton('deletePreDeformerHistory_ui', l = u'History Before Deformers')
    cmds.checkBoxGrp('ResetToDefaultShader_ui', ncb = 1, l1 = u'Reset to Default Shader', v1 = False)
    cmds.checkBoxGrp('deleteUnusedNodes_ui', ncb = 1, l1 = u'Delete Unused Nodes', v1 = False)
    cmds.button(l = u'Run', c = run)
    cmds.showWindow('window1_ui')

exportCleanup()