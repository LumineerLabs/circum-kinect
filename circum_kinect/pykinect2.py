import logging

from pykinect2 import PyKinectRuntime
from pykinect2.PyKinectV2 import FrameSourceTypes_Body, JointType_SpineShoulder, TrackingState_NotTracked


logger = logging.getLogger(__name__)


def init_pykinect2():
    kinect2 = PyKinectRuntime.PyKinectRuntime(FrameSourceTypes_Body)
    return kinect2


def pykinect2_update_thread(kinect2):
    if kinect2.has_new_body_frame():
        logger.debug(f"new body frame with {kinect2.max_body_count} bodies!")
        targets = kinect2.get_last_body_frame()
    else:
        targets = None

    tracking = []
    updated = False

    if targets and targets is not None:
        updated = True
        for i in range(0, kinect2.max_body_count):
            target = targets.bodies[i]
            if not target.is_tracked:
                continue

            joints = target.joints

            # use the Spine Shoulder joint as a shortcut for center of mass
            spine_shoulder = joints[JointType_SpineShoulder]

            if spine_shoulder.TrackingState == TrackingState_NotTracked:
                continue

            # TODO: add sensor specific details (joints, joint normals, hand positions, face tracking, etc.)
            track = {
                "x": spine_shoulder.Position.x,
                "y": spine_shoulder.Position.y,
                "z": spine_shoulder.Position.z
            }

            tracking.append(track)

    return tracking, updated
