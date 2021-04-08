import pytest
import sys
from unittest.mock import MagicMock

pykinect = MagicMock()
pykinect2 = MagicMock()

@pytest.fixture
def pykinect_mock():
    return pykinect

@pytest.fixture
def pykinect2_mock():
    return pykinect2

module = type(sys)('pykinect')
sys.modules['pykinect'] = module

module = type(sys)('pykinect.nui')
module.Runtime = pykinect
module.JointId = pykinect
sys.modules['pykinect.nui'] = module

module = type(sys)('pykinect2')
module.PyKinectRuntime = pykinect2
sys.modules['pykinect2'] = module

module = type(sys)('pykinect2.PyKinectV2')
module.FrameSourceTypes_Body = 32
module.JointType_SpineShoulder = 20
module.TrackingState_NotTracked = 0
sys.modules['pykinect2.PyKinectV2'] = module