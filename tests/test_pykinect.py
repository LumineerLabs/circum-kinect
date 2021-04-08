from unittest.mock import MagicMock, call

from circum_kinect.pykinect import init_pykinect, pykinect_update_thread

from pykinect.nui import JointId


class FakeFrame:
    def __init__(self, skeletons):
        self.SkeletonData = skeletons


class FakeSkeleton:
    def __init__(self, position):
        self.SkeletonPositions = position


def test_init(pykinect_mock):
    init_pykinect()

    pykinect_mock.assert_has_calls([call()])
    assert pykinect_mock.enabled


def test_update_thread_one_skeleton(pykinect_mock):
    frame = FakeFrame([FakeSkeleton({JointId.ShoulderCenter: [0, 1, 2]})])
    pykinect_mock.skeleton_engine = MagicMock()
    pykinect_mock.skeleton_engine.get_next_frame = MagicMock()
    pykinect_mock.skeleton_engine.get_next_frame.side_effect = [frame]

    pykinect_mock.attach_mock(pykinect_mock.skeleton_engine.get_next_frame, "get_next_frame")

    tracks, updated = pykinect_update_thread(pykinect_mock)

    assert updated
    assert tracks == [{'x': 0, 'y': 1, 'z': 2}]


def test_update_thread_multiple_skeletons(pykinect_mock):
    frame = FakeFrame([
        FakeSkeleton({JointId.ShoulderCenter: [0, 1, 2]}),
        FakeSkeleton({JointId.ShoulderCenter: [3, 4, 5]}),
    ])
    pykinect_mock.skeleton_engine = MagicMock()
    pykinect_mock.skeleton_engine.get_next_frame = MagicMock()
    pykinect_mock.skeleton_engine.get_next_frame.side_effect = [frame]

    pykinect_mock.attach_mock(pykinect_mock.skeleton_engine.get_next_frame, "get_next_frame")

    tracks, updated = pykinect_update_thread(pykinect_mock)

    assert updated
    assert tracks == [
        {'x': 0, 'y': 1, 'z': 2},
        {'x': 3, 'y': 4, 'z': 5}
    ]
