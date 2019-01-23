import cv2
import argparse
import os
import logging

import logging
import sys


# setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# constants for text
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
FONT_COLOR = (100, 255, 100)
THICKNESS = 2


class NoCameraDetectedError(Exception):
    pass


# Helper functions


def get_stream():
    """
    Try to get the stream from the camera and return it

    :return:
    """
    logger.debug("Getting the stream from the camera")
    try:
        stream = cv2.VideoCapture(0)
    except cv2.error as e:
        logger.error(e)
        exit(1)

    if not stream.isOpened():
        logger.error("NoCameraDetectedError: Try changing the index of the camera")
        exit(1)

    return stream


def print_text_on_frame(frame, top_left_corner, iteration):
    """
    Printout the gesture count and the images for that gesture count

    :param frame:
    :param top_left_corner:
    :param iteration:
    :return:
    """
    logger.debug("Printing text on frame")
    text_size = cv2.getTextSize('Image count:', FONT, FONT_SCALE, THICKNESS)[0]

    cv2.putText(frame,
                ''.join(["Image count:", str(iteration)]),
                top_left_corner,
                FONT,
                FONT_SCALE,
                FONT_COLOR,
                THICKNESS)
    cv2.putText(frame,
                ''.join(["Gesture count:", str(current_folder_iteration)]),
                (top_left_corner[0], top_left_corner[1] + text_size[1] + 10),
                FONT,
                FONT_SCALE,
                FONT_COLOR,
                THICKNESS)

    cv2.imshow('frame', frame)


def generator(initial_value=0):
    i = initial_value
    while i < 1000:
        yield i
        i += 1


def create_folder(root_folder_path, folder_iterator):
    """
    Create folders for the dataset

    :param root_folder_path:
    :param folder_iterator:
    :return:
    """

    logger.debug(f"Creating folder for gesture number: {folder_iterator}")
    try:
        global current_folder_iteration
        current_folder_iteration = next(folder_iterator)

        logger.debug(current_folder_iteration)

        current_folder = ''.join([root_folder_path, '/gesture_', str(current_folder_iteration)])
        os.makedirs(current_folder)
    except FileExistsError:
        logger.warning(f"File already exists, so not creating a new one: {current_folder}")
        pass

    return current_folder


def run_gesture_collection(camera_index, next_gesture):
    """
    Initialize the stream create folders to save the images and end on keypress ('q')

    :param camera_index:
    :param next_gesture:
    :return:
    """

    # initialize variables
    image_iterator = generator(1)
    folder_iterator = generator(1)
    top_left_corner = None
    iteration = 0
    root_folder_path = os.getcwd() + '/gestures_dataset'

    stream = get_stream()

    current_folder = create_folder(root_folder_path, folder_iterator)

    while (True):
        ret, frame = stream.read()
        height, width = frame.shape[:2]

        if not top_left_corner:
            top_left_corner = (height // 55, int(width // 1.9))

        # key capture and handling
        key = cv2.waitKey(1)

        if key == ord('c'):
            iteration = next(image_iterator)
            cv2.imwrite(''.join([current_folder, '/gest_', str(current_folder_iteration), '_', str(iteration), '.jpg']),
                        frame)

            if iteration % next_gesture == 0:
                current_folder = create_folder(root_folder_path, folder_iterator)
                image_iterator = generator(1)

        if key == ord('q') or key == 27:
            logger.debug("Exiting program... Goodbye!")
            break

        print_text_on_frame(frame, top_left_corner, iteration)

    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--images-per-gesture",
                    required=False,
                    help="Number of images to capture for a gesture")
    # TODO: Implement this functionality
    # ap.add_argument("-o",
    #                 "--overwrite",
    #                 required=False,
    #                 action="store_true",
    #                 help="Overwrite old images")
    ap.add_argument("--camera-index",
                    required=False,
                    default=0,
                    help="Index of the camera to use")
    args = vars(ap.parse_args())

    camera_index = args['camera_index']
    next_gesture = 10 if not args["images_per_gesture"] else int(args["images_per_gesture"])

    run_gesture_collection(camera_index=camera_index, next_gesture=next_gesture)
