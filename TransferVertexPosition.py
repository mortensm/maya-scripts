#Transfer Vertex Position
#v2.0
#author Mitchell Mortenson

#Install instructions

# 1. Copy all code 
# 2. Paste into the Maya script editor under a Python tab 
# 3. Click 'Execute'
# 4. (Optional) Click 'Save script to shelf' to save this script to your current shelf


from maya import cmds


origVerteciesPosList = []

def getVertecies(*args):
    selOrigVertecies = cmds.ls(sl = True, l = True, flatten = True)
    global origVerteciesPosList
    origVerteciesPosList = []
    for eachOrigVertex in selOrigVertecies:
        # eachOrigVertexMesh = eachOrigVertex.split(".")[0]
        # eachOrigVertexNumTmp = eachOrigVertex.split("[")[1]
        # eachOrigVertexNum = eachOrigVertexNumTmp.split("]")[0]
        eachOrigVertexPos = cmds.xform(eachOrigVertex, q = True, ws = True, t = True)
        origVerteciesPosList.append(eachOrigVertexPos)
        print eachOrigVertex + ": " + str(eachOrigVertexPos)
    print "Got " + str(len(origVerteciesPosList)) + " vertecies"


def putVertecies(*args):
    # origVerteciesPosList = getVertecies()
    selTargVertecies = cmds.ls(sl = True, l = True, flatten = True)
    putVerteciesCount = 0
    for eachTargVertex in selTargVertecies:
        cmds.xform(eachTargVertex, ws = True, t = origVerteciesPosList[putVerteciesCount])
        putVerteciesCount += 1

def transferVertexPosition(*args):
    selectedObjs = cmds.ls(sl = True, l = True)
    if (len(selectedObjs) == 2):
        orgMesh = selectedObjs[0]
        targMesh = selectedObjs[1]

        numOfVertOrgMesh = cmds.polyEvaluate(orgMesh, vertex = True)
        numOfVertTargMesh = cmds.polyEvaluate(targMesh, vertex = True)
        print str(numOfVertOrgMesh) + " verts"

        if (numOfVertOrgMesh == numOfVertTargMesh):
            vertexIDOrgMesh = 0

            while vertexIDOrgMesh != numOfVertOrgMesh:
                getVertPos = cmds.xform((str(orgMesh) + ".vtx[" + str(vertexIDOrgMesh) + "]"), q = True, ws = True, t = True)
                print "vert " + str(vertexIDOrgMesh + 1)  + ": " + str(getVertPos)
                cmds.xform((str(targMesh) + ".vtx[" + str(vertexIDOrgMesh) + "]"), ws = True, t = getVertPos)
                vertexIDOrgMesh += 1

            pivTransOrigMesh = cmds.xform((orgMesh), q = True, a = True, ws = True, piv = True)
            cmds.xform((targMesh),  a = True, ws = True, piv = [pivTransOrigMesh[0], pivTransOrigMesh[1], pivTransOrigMesh[2]])
    else:
        print "Select two objects"

def transferVertexPosition_ui():
    if(cmds.window('window1_ui', q = True, ex = True)): cmds.deleteUI('window1_ui')
    cmds.window('window1_ui', s = False, t = u'Transfer Vertex Position', tlb = True, wh = (150, 18), rtf = True)
    cmds.columnLayout(adj = True)
    cmds.separator()
    cmds.text(l = u'Select both the original mesh and the target mesh in that order, then click Run', ww = True)
    cmds.button(l = u'Run', c = transferVertexPosition)
    cmds.separator(h=20)
    cmds.text(l = u'Select the vertecies in order that you want to transfer, then click Get Vertex Positions', ww = True)
    cmds.button(l = u'Get Vertex Positions', c = getVertecies)
    cmds.text(l = u'\nSelect the vertecies in the same order on the target mesh that you want to transfer, then click Transfer Vertex Positions', ww = True)
    cmds.button(l = u'Transfer Vertex Positions', c = putVertecies)
    cmds.showWindow('window1_ui')

transferVertexPosition_ui()