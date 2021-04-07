import copy
import logging
from threading import Semaphore, Thread

import circum.endpoint

import click


logger = logging.getLogger(__name__)
tracking_semaphore = None
tracking_info = {"objects": []}
vector_info = []
updated = False


def _get_targets():
    raise NotImplementedError()
    return []


def _update_thread(kinect_update_fn, kinect):
    global tracking_info
    global vector_info
    global updated

    while True:

        tracking_semaphore.acquire()

        tracks, new = kinect_update_fn(kinect)
        if new:
            updated = True
            tracking_info["objects"] = tracks
            logger.debug(f'got: {tracking_info}')

        tracking_semaphore.release()
        # time.sleep(update_interval)


def run_kinect(kinect_args: {}) -> {}:
    global updated
    ret = None
    tracking_semaphore.acquire()
    if updated:
        logger.debug(f"sending {tracking_info}")
        ret = copy.deepcopy(tracking_info)
        updated = False
    tracking_semaphore.release()
    return ret


def _kinect(ctx,
            version: str):
    global tracking_semaphore
    tracking_semaphore = Semaphore()

    if version == '1':
        try:
            from circum_kinect.pykinect import init_pykinect, pykinect_update_thread
        except Exception as e:
            logger.error("Unable to load pykinect, is the package installed? Try `pip3 install pykinect`.")
            raise e
        kinect = init_pykinect()
        kinect_update_fn = pykinect_update_thread
    elif version == '2':
        try:
            from circum_kinect.pykinect2 import init_pykinect2, pykinect2_update_thread
        except Exception as e:
            logger.error("Unable to load pykinect2, is the package installed? Try `pip3 install pykinect2`.")
            raise e
        kinect = init_pykinect2()
        kinect_update_fn = pykinect2_update_thread
    else:
        raise ValueError(f"Unsupported version {version}. Only versions 1 and 2 are supported")

    tracker_thread = Thread(target=_update_thread, args=[kinect_update_fn, kinect])
    tracker_thread.daemon = True
    tracker_thread.start()
    circum.endpoint.start_endpoint(ctx, "kinect", run_kinect)


@click.command()
@click.option('--version',
              required=False,
              type=click.Choice(['1', '2'], case_sensitive=False),
              default='2',
              help='PyKinect version to use.')
@click.pass_context
def kinect(ctx,
           version: str):
    _kinect(ctx, version)
