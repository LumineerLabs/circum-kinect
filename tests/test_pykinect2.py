from unittest.mock import call, patch

from circum_kinect.pykinect2 import init_pykinect2, pykinect2_update_thread


class FakePosition:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class FakeJoint:
    def __init__(self, tracking_state, x=0, y=0, z=0):
        self.Position = FakePosition(x, y, z)
        self.TrackingState = tracking_state


class FakeBody:
    def __init__(self, is_tracked):
        self.is_tracked = is_tracked
        self.joints = {}

    def set_joint(self, joint_id, position):
        self.joints[joint_id] = position


class FakeBodyFrame:
    def __init__(self, bodies):
        self.bodies = bodies


class FakeKinect:
    def __init__(self, has_new_body_frame, max_body_count=0):
        self.has_new_body_frame = lambda: has_new_body_frame
        self.max_body_count = max_body_count
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def get_last_body_frame(self):
        return FakeBodyFrame(self.bodies)


def test_no_skeleton_frame():
    kinect = FakeKinect(False, 100)

    tracking, updated = pykinect2_update_thread(kinect)

    assert not updated
    assert tracking == []


def test_one_skeleton():
    kinect = FakeKinect(True, 1)
    body = FakeBody(True)
    body.set_joint(20, FakeJoint(True, x=0, y=1, z=2))
    kinect.add_body(body)

    tracking, updated = pykinect2_update_thread(kinect)

    assert updated
    assert tracking == [{'x': 0, 'y': 1, 'z': 2}]


def test_multiple_skeletons():
    kinect = FakeKinect(True, 2)
    body1 = FakeBody(True)
    body1.set_joint(20, FakeJoint(True, x=0, y=1, z=2))
    kinect.add_body(body1)
    body2 = FakeBody(True)
    body2.set_joint(20, FakeJoint(True, x=3, y=4, z=5))
    kinect.add_body(body2)

    tracking, updated = pykinect2_update_thread(kinect)

    assert updated
    assert tracking == [{'x': 0, 'y': 1, 'z': 2}, {'x': 3, 'y': 4, 'z': 5}]


def test_untracked_skeletons():
    kinect = FakeKinect(True, 2)
    body1 = FakeBody(False)
    body1.set_joint(20, FakeJoint(True, x=0, y=1, z=2))
    kinect.add_body(body1)
    body2 = FakeBody(True)
    body2.set_joint(20, FakeJoint(True, x=3, y=4, z=5))
    kinect.add_body(body2)

    tracking, updated = pykinect2_update_thread(kinect)

    assert updated
    assert tracking == [{'x': 3, 'y': 4, 'z': 5}]


def test_untracked_joint():
    kinect = FakeKinect(True, 2)
    body1 = FakeBody(True)
    body1.set_joint(20, FakeJoint(False, x=0, y=1, z=2))
    kinect.add_body(body1)
    body2 = FakeBody(True)
    body2.set_joint(20, FakeJoint(True, x=3, y=4, z=5))
    kinect.add_body(body2)

    tracking, updated = pykinect2_update_thread(kinect)

    assert updated
    assert tracking == [{'x': 3, 'y': 4, 'z': 5}]


def test_init():
    with patch("pykinect2.PyKinectRuntime.PyKinectRuntime") as runtime:
        init_pykinect2()
        runtime.assert_has_calls([call(32)])
