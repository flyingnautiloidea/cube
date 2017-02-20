#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy

#文字定义三维坐标轴：蓝色法向是x轴＋，红色法向是y轴＋，白色法向是z轴＋

#定义阶数。
N = 2

#定义整体旋转矩阵，包含3个子旋转矩阵，每个子旋转矩阵的含义是在各个坐标轴的正向看，顺时针旋转90度。这个矩阵用于初始化所有反转矩阵时候使用的。
rotateMatrix = [
#绕x顺时针
[[1,0,0],[0,0,1],[0,-1,0]],
#绕y顺时针
[[0,0,1],[0,1,0],[-1,0,0]],
#绕z顺时针
[[0,1,0],[-1,0,0],[0,0,1]]
]

#实现反转动作的罗列,最终结构：［
# ［［］，［］，［］，［］］，
# ［［］，［］，［］，［］］，
# ［［］，［］，［］，［］］，
# ］(其中每个“［］”均是一个3*3的矩阵。)
rotateMatrixAll = [

]


#初始化方格位置矩阵。如针对二阶魔方，有24个面，依次定义个个面中点的坐标。每行定义一个颜色，每行的顺序是代表了这个方格的唯一位置。
#在定义向量的过程中，我们默认方格的边长是2.
OriginalMatrix = [
# #前／蓝
# [],
# #后／绿
# [],
# #左／橘
# [],
# #右／红
# [],
# #上／白
# [],
# #下／黑
# [],
]

#初始化模仿块方格坐标的函数

#初始化block边界判断矩阵。
blockBorder = []

#根据block编号获得坐标“相对”值
blockToAxisQueryTable = []

#用于初始化方格的原始坐标用的
def initOriginalMatirx(N):
    #前：先初始化“前／蓝”一个面，然后直接各种旋转，得到所有的。
    axisMax = blockToAxisQueryTable[0]
    axisMin = blockToAxisQueryTable[N-1]
    frontArray = []
    for z in range(N):
        for y in range(N):
            frontArray.append( [ axisMax , blockToAxisQueryTable[N-1-y] , blockToAxisQueryTable[z]] )
    #目前我们获得了一个frontarray，这样我们进行旋转操作，一次获取后、左、右、上、下的坐标，并依次添加到矩阵中
    #后
    backArray = numpy.array(frontArray).dot(rotateMatrixAll[1][1])
    #左
    leftArray = numpy.array(frontArray).dot(rotateMatrixAll[2][0])
    #右
    rightArray = numpy.array(frontArray).dot(rotateMatrixAll[2][2])
    #上
    upArray = numpy.array(frontArray).dot(rotateMatrixAll[1][0])
    #下
    downArray = numpy.array(frontArray).dot(rotateMatrixAll[1][2])
    #讲所有的6个面依次添加如矩阵中
    OriginalMatrix.append(frontArray)
    OriginalMatrix.append(backArray)
    OriginalMatrix.append(leftArray)
    OriginalMatrix.append(rightArray)
    OriginalMatrix.append(upArray)
    OriginalMatrix.append(downArray)


#初始化一个边界block表。
def initBlockBorderTable(N):
    # for borderNumber in range(1):
    blockBorder.append(0)
    blockBorder.append(N-1)

#根据block可以查询到当前坐标轴的坐标是多少，这个初始化一个向量，用来被查找。
def initBlockQueryAxis(N):
    currentAxis = N-1
    for blockCounter in range(N):
        blockToAxisQueryTable.append(currentAxis)
        currentAxis = currentAxis - 2
        # if currentAxis == 0 :
        #     currentAxis = 2 * (-1)
        # elif currentAxis == 1 :
        #     currentAxis = 1 * (-1)
        #     print(currentAxis)
        # else :
        #     currentAxis = currentAxis - 2

#补全翻滚矩阵。
def completeRotateMatrix(rotateMatrix,rotateMatrixAll):
    for counter in range(3):
        forEachAxis = []
        atomRotate = rotateMatrix[counter]
        forEachAxis.append(atomRotate)
        numpyM = numpy.array(atomRotate)
        numpyTemp = numpyM
        for rotateTime in range(3):
            numpyTemp = numpyTemp.dot(numpyM)
            forEachAxis.append(numpyTemp)
        rotateMatrixAll.append(forEachAxis)

# #初始化boder向量［0，N－1］
# def initBlockBorder(N):
#     for axisNumber in range(2):
#         borderVector = []
#         borderVector.append(0)
#         borderVector.append(N-1)
#         blockBorder.append(borderVector)

#根据block，和N的值，获取坐标的value。这块最好做个映射（查表），直接获取值，而不用计算。
def blockToAxisValue(axisBlockNum):
    axisValueList = []
    #1.1首先先直接获取直接看到的值。
    axisValueList.append(blockToAxisQueryTable[axisBlockNum])
    #1.2其次判断当前block是否在边界上，如果在，那么list中，需要再增加一个axis值。（最终返回2个结果）
    if axisBlockNum in blockBorder:
        if axisBlockNum == 0 :
            axisValue = axisBlockNum + 1
            axisValueList.append(axisValue)
        else :
            axisValue = axisBlockNum - 1
            axisValueList.append(axisValue)
    return axisValueList

# #需要根据block得到筛选坐标轴的值，这个值有可能是2个，所以，用一个list保存。
# def getAxisValue():
#     for

#执行魔方动作的函数,注意，要判断目标方格的执行边界（尤其是最外层的，总是涉及到一整个面的旋转）根据坐标值和blockNum，完全可以确定应该如何操作矩阵了。
def atomExecutor(originalMatrix , rotateMatrixAll , axisChoice , axisBlockNum , clockwiseTimes , traceFile):
    #首先获取旋转矩阵
    axisMetixChoice = rotateMatrixAll[axisChoice]
    theRotateMetrix = axisMetixChoice[clockwiseTimes-1]
    #获取坐标值，注意，这个坐标可能是1个值，也可能是2个值，因此是一个矩阵结构（理解成list也行）
    axisValueList = blockToAxisValue(axisBlockNum)
    listSize = len(axisValueList)

    #操作执行器,尝试循环100次
    for round in range(10000):
        #针对2阶魔方，有6个可动选项，每个选项有0，1，2，3倍的90度动作。
        #可动块区域选项配置，结果也应该提供
        axisChoice = random.randint(0,2)
        axisBlockNum = random.randint(0,N-1)
        #90度旋转倍数配置
        clockwiseTimes = random.randint(1, 4)
        #以下针对原始矩阵中符合条件的向量进行旋转操作(以下是遍历＋操作过程)
        for sides in range( 6 ):
            allGridsInOneSide = OriginalMatrix[sides]
            for gridCount in range(N * N):
                singleGrid = allGridsInOneSide[gridCount]
                for axisCount in range(listSize):
                    if singleGrid[axisChoice] == axisValueList[axisCount]:
                        singleGrid = singleGrid.dot(theRotateMetrix)

    traceFile.write(str(OriginalMatrix) + "\n")
    traceFile.write("##########################" + "\n")







#首先整个实现，目前是基于一次操作，10000次；针对10000次结果进行节点收敛，获取一个｛地址－value｝数据结构进行归并，得到最后的网络路径值；不断的这个过程，最终结果会趋向于收敛。
if __name__ == "__main__":
    #初始化一个block边界表［0，N-1］
    initBlockBorderTable(N)
    blockBorder = numpy.array(blockBorder)

    #初始化"block-坐标值"表
    initBlockQueryAxis(N)
    blockToAxisQueryTable = numpy.array(blockToAxisQueryTable)

    #初始化旋转矩阵：旋转矩阵补全，这步要先写，因为接下来构建魔方各个面的矩阵的时候，需要它。
    completeRotateMatrix(rotateMatrix,rotateMatrixAll)
    rotateMatrixAll = numpy.array(rotateMatrixAll)

    #初始化魔方矩阵，2DOriginalMatrix
    originalMatrix = initOriginalMatirx(N)
    OriginalMatrix = numpy.array(OriginalMatrix)

    #打开一个文件，用于保存状态
    traceFile = open('./traceRoute','w')

    atomExecutor(originalMatrix ,rotateMatrixAll,  axisChoice , axisBlockNum , clockwiseTimes ,traceFile)

    #文件关闭
    traceFile.close()
