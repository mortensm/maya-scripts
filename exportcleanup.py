#Export Cleanup
#v1.1.4
#author Mitchell Mortenson


#Install instructions


# 1. Copy all code
# 2. Paste into the Maya script editor under a Python tab
# 3. Click 'Execute'
# 4. (Optional) Click 'Save script to shelf' to save this script to your current shelf



from maya import cmds
import maya.mel as mel


def makeFaceted():
    selectedObjs = cmds.ls (sl = True, l = True, dag = True, type = 'transform')
    for eachObj in selectedObjs:
        try:
            cmds.setAttr((eachObj + '.displaySmoothMesh'), 0)
        except:
            continue


def moveToOrigin(xAxis, yAxis, zAxis):
    originalSelectedObjs = cmds.ls(sl = True, l = True, type = 'transform')
    # https://stackoverflow.com/questions/50759124/maya-mel-script-drop-pivot-to-bottom-of-object
    selectedObjs = cmds.ls(sl = True, l = True, dag = True)
    topNodeList = []


    for eachObj in selectedObjs:
        topNode=cmds.ls(eachObj, l = True)[0].split("|")[1]


        topNodeList.append(topNode)


    topNodeList = list(dict.fromkeys(topNodeList))


    for eachTopNode in topNodeList:
        lowestY = 2147483647.0
        hightestY = -2147483647.0
        crtY = 0.0
        pos = []
        totalVCount = 0
        eachTopNodeGeoList = []
        allChildrenEachTopNode = cmds.listRelatives(eachTopNode, f = True, ad = True)
        aboveGrid = []
        belowGrid = []


        # center pivot of eachTopNode
        cmds.xform(eachTopNode, cp = True)


        # get all meshes in eachTopNode
        # https://stackoverflow.com/questions/21490307/select-all-by-type-geometry-equivalent-python-script
        for eachObj in allChildrenEachTopNode:
            eachObjType = cmds.ls(eachObj, l = True, showType = True)
            if eachObjType[1] == 'mesh':
                eachTopNodeGeoList.append(cmds.listRelatives(eachObjType[0], p = True, pa = True, f = True))
        if (yAxis == True):
            for eachGeo in eachTopNodeGeoList:
                vtxIdx = 0
                vCount = cmds.polyEvaluate(eachGeo[0], vertex = True)
                cmds.select(eachGeo[0])


                #Get vertex count
                #Loop through vertices
                for vtxIdx in range(0, int(vCount)):
                    pos = cmds.xform(((eachGeo[0]) + ".vtx[" + str(vtxIdx) + "]"), q = True, ws = True, t = True)


                    #Get vertex position
                    crtY = pos[1]


                    if crtY > 0:
                        aboveGrid.append(crtY)
                    else:
                        belowGrid.append(crtY)


                    if crtY < lowestY:
                        lowestY = crtY


                    if crtY > hightestY:
                        hightestY = crtY


                totalVCount = totalVCount + vCount


            # if 90%+ of the vertices are above the grid
            if len(aboveGrid) >= (.9 * totalVCount):
                cmds.move((lowestY * -1), eachTopNode, y = True, r = True, ls = True, wd = True,  puv = True)
                print eachTopNode + " is at least 90 percent above the grid"


            # if 90%+  of the vertices are below the grid
            elif len(belowGrid) >= (.9 * totalVCount):
                cmds.move((hightestY * -1), eachTopNode, y = True, r = True, ls = True, wd = True,  puv = True)
                print eachTopNode + " is at least 90 percent below the grid"


            # if 90%+ of the vertices are neither above or below the grid
            else:
                print eachTopNode + " cannot be determined in relation to the grid"


        if(xAxis == True):
            cmds.move(0, eachTopNode, x = True, ws = True, rpr = True,  puv = True)


        if(zAxis == True):
            cmds.move(0, eachTopNode, z = True, ws = True, rpr = True,  puv = True)


    cmds.select(originalSelectedObjs)


def freezeTransforms():
    mel.eval('performFreezeTransformations(0)')


def resetPivots():
    selectedObjs = cmds.ls (sl = True, l = True, dag = True, type = 'transform')
    if (cmds.checkBoxGrp ('freezeTransforms_ui', q = True, v1 = True)):
        mel.eval('setTRSPinPivot false')
        mel.eval('ResetTransformations')
        cmds.refresh()
    else:
        for eachObj in selectedObjs:
            mel.eval('setTRSPinPivot false')
            cmds.xform(ws = True, a = True, piv = (0,0,0))
            cmds.xform(ws = True, a = True, rp = (0,0,0))
            cmds.xform(ws = True, a = True, sp = (0,0,0))
            cmds.refresh()


def resetToDefaultShader():
    mel.eval('sets -e -forceElement initialShadingGroup')


def deleteUnusedNodes():
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')


def deleteAllHistory():
    mel.eval("DeleteHistory")


def deleteNonDeformerHistory():
    mel.eval('doBakeNonDefHistory( 1, {"prePost" })')


def deletePreDeformerHistory():
    mel.eval('doBakeNonDefHistory( 1, {"pre" })')


def moveToOriginCheckBox(arg):
    cmds.checkBoxGrp ('moveToOriginXYZ_ui', edit = True, en = arg)


def changeHistoryCheckBox(arg):
    cmds.radioButton('deleteAllHistory_ui', edit = True, en = arg)
    cmds.radioButton('deleteNonDeformerHistory_ui', edit = True, en = arg)
    cmds.radioButton('deletePreDeformerHistory_ui', edit = True, en = arg)


def changeFreezeTransformsCheckBox(arg):
    cmds.checkBoxGrp ('moveToOrigin_ui', edit = True, en = arg)
    cmds.checkBoxGrp ('moveToOriginXYZ_ui', edit = True, en = arg)


def run(*args):
    selectedObjs = cmds.ls (sl = True, l = True, type = 'transform')
    if (selectedObjs):
        if (cmds.checkBoxGrp ('makeFaceted_ui', q = True, v1 = True)):
            makeFaceted()


        if (cmds.checkBoxGrp ('moveToOrigin_ui', q = True, v1 = True)):
            if (cmds.checkBoxGrp ('freezeTransforms_ui', q = True, v1 = True)):
                if (cmds.checkBoxGrp('moveToOriginXYZ_ui', q = True, v1 = True)):
                    xAxis = True
                else:
                    xAxis = False


                if (cmds.checkBoxGrp('moveToOriginXYZ_ui', q = True, v2 = True)):
                    yAxis = True
                else:
                    yAxis = False


                if (cmds.checkBoxGrp('moveToOriginXYZ_ui', q = True, v3 = True)):
                    zAxis = True
                else:
                    zAxis = False


                if ((xAxis == True) or (yAxis == True) or (zAxis == True)):
                    freezeTransforms()
                    moveToOrigin(xAxis, yAxis, zAxis)
                else:
                    print "No axis is checked. Skipping move to origin"


        if (cmds.checkBoxGrp ('freezeTransforms_ui', q = True, v1 = True)):
            freezeTransforms()


        if (cmds.checkBoxGrp ('ResetPivots_ui', q = True, v1 = True)):
            resetPivots()


        if (cmds.checkBoxGrp ('resetToDefaultShader_ui', q = True, v1 = True)):
            resetToDefaultShader()


        if (cmds.checkBoxGrp ('deleteHistory_ui', q = True, v1 = True)):
            if cmds.radioButton('deleteAllHistory_ui', q = True, select = True):
                deleteAllHistory()


            elif cmds.radioButton('deleteNonDeformerHistory_ui', q = True, select = True):
                deleteNonDeformerHistory()


            elif cmds.radioButton('deletePreDeformerHistory_ui', q = True, select = True):
                deletePreDeformerHistory()
    else:
        cmds.warning ("Select at least one object")


    if (cmds.checkBoxGrp ('deleteUnusedNodes_ui', q = True, v1 = True)):
        deleteUnusedNodes()


def exportCleanup_ui():
    if(cmds.window('exportCleanupWindow_ui', q = True, ex = True)):
        cmds.deleteUI('exportCleanupWindow_ui')
    cmds.window('exportCleanupWindow_ui', t = u'Export Cleanup', s = True, tlb = True, wh = (153, 231), rtf = False)
    cmds.columnLayout(adj = True)
    cmds.checkBoxGrp('makeFaceted_ui', ncb = True, l1 = u'Make Faceted', v1 = True)
    cmds.checkBoxGrp('freezeTransforms_ui', ncb = True, l1 = u'Freeze Transforms', v1 = True, cc = changeFreezeTransformsCheckBox)
    cmds.checkBoxGrp('ResetPivots_ui', ncb = True, l1 = u'Reset Pivots', v1 = True)
    cmds.checkBoxGrp('moveToOrigin_ui', ncb = True, l1 = u'Move to Origin', v1 = True, cc = moveToOriginCheckBox)
    cmds.checkBoxGrp('moveToOriginXYZ_ui', cw = [[1, 30], [2, 30], [3, 30]], ncb = 3, l=u' ', l1 = u'X', l2 = u'Y', l3 = u'Z', v1 = True, v2 = True, v3 = True)
    cmds.checkBoxGrp('deleteHistory_ui', ncb = True, l1 = u'Delete History', v1 = True, cc = changeHistoryCheckBox)
    cmds.radioCollection()
    cmds.radioButton('deleteAllHistory_ui', l = u'All History', select = True)
    cmds.radioButton('deleteNonDeformerHistory_ui', l = u'Non-Deformer History')
    cmds.radioButton('deletePreDeformerHistory_ui', l = u'History Before Deformers')
    cmds.checkBoxGrp('resetToDefaultShader_ui', ncb = True, l1 = u'Reset to Default Shader', v1 = False)
    cmds.checkBoxGrp('deleteUnusedNodes_ui', ncb = True, l1 = u'Delete Unused Nodes', v1 = False)
    cmds.button('Run_ui', l = u'Run', c = run)
    cmds.showWindow('exportCleanupWindow_ui')


exportCleanup_ui()

