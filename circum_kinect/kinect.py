import click
import circum.endpoint
import copy
import logging

from threading import Semaphore, Thread


logger = logging.getLogger(__name__)
tracking_semaphore = None
tracking_info = {"objects": []}
vector_info = []
updated = False


def _get_targets():
    raise NotImplementedError()
    return []


def _update_thread():
    global tracking_info
    global vector_info
    global updated

    while True:
        targets = _get_targets()

        tracking_semaphore.acquire()

        if targets and targets is not None:
            tracking_info["objects"] = \
                [{"x": target.xPosCm / 100, "y": target.yPosCm / 100, "z": target.zPosCm / 100} for target in targets]
            for i, target in enumerate(targets):
                logger.debug('Target #{}:\nx: {}\ny: {}\nz: {}\namplitude: {}\n'.format(
                    i + 1, target.xPosCm, target.yPosCm, target.zPosCm,
                    target.amplitude))
        else:
            tracking_info["objects"] = []

        updated = True

        tracking_semaphore.release()
        # time.sleep(update_interval)


def run_kinect(kinect_args: {}) -> {}:
    global updated
    ret = None
    tracking_semaphore.acquire()
    if updated:
        ret = copy.deepcopy(tracking_info)
        updated = False
    tracking_semaphore.release()
    return ret


@click.command()
@click.pass_context
def webcam(ctx):
    global tracking_semaphore
    tracking_semaphore = Semaphore()

    tracker_thread = Thread(target=_update_thread)
    tracker_thread.daemon = True
    tracker_thread.start()
    circum.endpoint.start_endpoint(ctx, "cam", run_kinect)
