import bpy
import mathutils
from mathutils import Matrix
import math

import json
import os
import time

path = 'D:\\Documents\\HackathonProject\\HealthAR\\blender_python'

files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

for f in files:
    with open(f) as file:
        x = json.loads(file.read())
        print(x)


bone_names = ['body', 'collarBone.L', 'collarBone.R', 'armUpper.L', 'armUpper.R', 'armLower.L', 'armLower.R', 'leg.L', 'leg.R', 'legUpper.L', 'legUpper.R', 'legLower.L', 'legLower.R']

bone_names = ['body', 'collarBone.R', 'armUpper.R', 'armLower.R', 'collarBone.L', 'armUpper.L', 'armLower.L']
keypoints = [{"score":0.9925291538238525,"part":"nose","position":{"x":297.1353295967404,"y":134.90062092625817}},{"score":0.9712863564491272,"part":"leftEye","position":{"x":307.5435797912253,"y":122.20358737679415}},{"score":0.9619162678718567,"part":"rightEye","position":{"x":284.33341635149077,"y":123.02925065506336}},{"score":0.7947087287902832,"part":"leftEar","position":{"x":318.2902483751545,"y":130.2879040740257}},{"score":0.7984864115715027,"part":"rightEar","position":{"x":274.4218901725812,"y":131.75480687341025}},{"score":0.9964147806167603,"part":"leftShoulder","position":{"x":347.1360693139545,"y":204.32153036428053}},{"score":0.9872980713844299,"part":"rightShoulder","position":{"x":244.88229180459922,"y":207.09421734477198}},{"score":0.9862083792686462,"part":"leftElbow","position":{"x":362.98105013572564,"y":282.08946405455123}},{"score":0.9921452403068542,"part":"rightElbow","position":{"x":225.31996689273814,"y":294.7860420581906}},{"score":0.8998027443885803,"part":"leftWrist","position":{"x":367.31549451580156,"y":352.5993098769077}},{"score":0.9793730974197388,"part":"rightWrist","position":{"x":209.9702100161105,"y":361.4304090100665}},{"score":0.9982525706291199,"part":"leftHip","position":{"x":334.2824584616106,"y":362.08377749420873}},{"score":0.9706612229347229,"part":"rightHip","position":{"x":270.92697747009623,"y":372.98093573991645}},{"score":0.9759436845779419,"part":"leftKnee","position":{"x":354.05296368787515,"y":468.7743750283884}},{"score":0.8085767030715942,"part":"rightKnee","position":{"x":285.41500457936087,"y":480.055840514427}},{"score":0.47188472747802734,"part":"leftAnkle","position":{"x":356.0935560323424,"y":507.54267492959667}},{"score":0.28076109290122986,"part":"rightAnkle","position":{"x":275.61823009771143,"y":522.2142419149709}}]


armature = bpy.data.objects['Armature']
bpy.ops.object.mode_set(mode='POSE')


def pointX(num):
    return num * 3

def pointY(num):
    return num * 3 + 1


def findAngle(p1, p2):
    # Rotation about Z-axis
    slopeZ = (p1['y'] - p2['y'])/(p1['x'] - p2['x'])
    angleZ = math.atan(slopeZ)

    return angleZ


def findDistance(p1, p2):
    dist = math.sqrt(math.pow((p1['x'] - p2['x']), 2) + math.pow((p1['y'] - p2['y']), 2))

    return dist


def bone_name_mapping(index):

    if index in [0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16]:
        return None
    else:
        return bone_names[index-2]


for x_index in range(len(x)):
    for i in range(int(len(x[x_index]['people'][0]['pose_keypoints_2d'])/3)):

        if i == 1:
            bname = 'collarBone.R'
        elif i == 2:
            bname = 'armUpper.R'
        elif i == 3:
            bname = 'armLower.R'
        elif i == 5:
            bname = 'armUpper.L'
        elif i == 6:
            bname = 'armLower.L'
        else:
            bname = None

        # bname = bone_names[i-1]
        if (bname):

            j = x[x_index]

            bone = armature.pose.bones[bname]
            bone.rotation_mode = 'XYZ'

            def point(num):
                return  {
                    'x': j['people'][0]['pose_keypoints_2d'][pointX(num)],
                    'y': j['people'][0]['pose_keypoints_2d'][pointY(num)]
                }

            def scale_distance_Points(num):
                return {
                    'x': x[0]['people'][0]['pose_keypoints_2d'][pointX(num)],
                    'y': x[0]['people'][0]['pose_keypoints_2d'][pointY(num)]
                }

            scale_distance = findDistance(scale_distance_Points(i), scale_distance_Points(i+1))
            distance = findDistance(point(i), point(i+1))
    
            # rotation about z-axis
            # if (keypoints[i+2]['position']['x'] < keypoints[i]['position']['x']):
            if (j['people'][0]['pose_keypoints_2d'][pointX(i)] < j['people'][0]['pose_keypoints_2d'][pointX(i+1)]):
                angleZ = math.pi * distance / scale_distance + math.pi
            else:
                angleZ = math.pi * distance / scale_distance # scale_distance is the distance max distance TODO: """DONE""" take max distance at the starting

            # rotation about x-axis (done by using y coordinates)
            # if (keypoints[i+2]['position']['y'] < keypoints[i]['position']['y']):
            if (j['people'][0]['pose_keypoints_2d'][pointY(i)] < j['people'][0]['pose_keypoints_2d'][pointY(i+1)]):
                angleX = math.pi * distance / scale_distance
            else:
                angleX = -1* math.pi * distance / scale_distance

            # rotation about y-axis (using the slope of the line)
            angleY = findAngle(point(i), point(i+1))

            rot_mat_X = Matrix.Rotation(angleX, 4, 'X')
            rot_mat_Y = Matrix.Rotation(angleY, 4, 'Y')
            rot_mat_Z = Matrix.Rotation(math.radians(0), 4, 'Z')

            # decompose world_matrix's components, and from them assemble 4x4 matrices
            orig_loc, orig_rot, orig_scale = bone.matrix.decompose()
            orig_loc_mat = Matrix.Translation(orig_loc)
            orig_rot_mat = orig_rot.to_matrix().to_4x4()
            orig_scale_mat = Matrix.Scale(orig_scale[0],4,(1,0,0)) @ Matrix.Scale(orig_scale[1],4,(0,1,0)) @ Matrix.Scale(orig_scale[2],4,(0,0,1))

            # assemble the new matrix
            bone.matrix = orig_loc_mat @ rot_mat_X @ rot_mat_Y @ rot_mat_Z @ orig_scale_mat
            
        armature.keyframe_insert(data_path='rotation_euler', frame=i*24)
