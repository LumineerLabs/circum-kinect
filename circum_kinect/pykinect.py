from pykinect import nui
from pykinect.nui import JointId


def init_pykinect():
    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True
    return kinect


def pykinect_update_thread(kinect):
    skeletons = kinect.skeleton_engine.get_next_frame().SkeletonData

    # TODO: add sensor specific information (joints)
    tracking = [
        {
            "x": data.SkeletonPositions[JointId.ShoulderCenter][0],
            "y": data.SkeletonPositions[JointId.ShoulderCenter][1],
            "z": data.SkeletonPositions[JointId.ShoulderCenter][2]
        }
        for data in skeletons
    ]

    return tracking, True
