import cv2
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-ng",
			   "--next_gesture",
			   required=False,
			   help="Number of images to capture for a gesture")
ap.add_argument("-o",
				"--overwrite",
				required=False,
				help="Overwrite old captures")
args = vars(ap.parse_args())
next_gesture = 10 if not args["next_gesture"] else int(args["next_gesture"])

# constants for text
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
FONT_COLOR = (100, 255, 100)
THICKNESS = 2

class NoCameraDetectedError(Exception):
	pass

def generator(initial_value=0):
	i = initial_value
	while i<1000:
		yield i
		i+=1

def create_folder():
	try:
		global current_folder_iteration
		current_folder_iteration = next(folder_iterator)
		print(current_folder_iteration)
		current_folder = ''.join([root_folder_path, '/gesture_', str(current_folder_iteration)])
		os.makedirs(current_folder)
	except FileExistsError:
		# log that file already exists
		pass
	return current_folder

image_iterator = generator(1)
folder_iterator = generator(1)
top_left_corner = None
iteration = 0
root_folder_path = os.getcwd() + '/gestures_dataset'
current_folder = root_folder_path

try:
	capture = cv2.VideoCapture(0)
except cv2.error as e:	
	print("capture")


if capture.isOpened() == False:
	raise NoCameraDetectedError("Try changing the index")

current_folder = create_folder()

while(True):
	ret, frame = capture.read()
	height, width = frame.shape[:2]

	if top_left_corner == None:
		print(height, width)
		top_left_corner = (height // 55, int(width // 1.9))
		print(top_left_corner)

	key = cv2.waitKey(1)

	if key == ord('c'):
		iteration = next(image_iterator)
		cv2.imwrite(''.join([current_folder, '/gest_', str(current_folder_iteration), '_', str(iteration), '.jpg']), frame)

		if iteration % next_gesture == 0:
			current_folder = create_folder()
			image_iterator = generator(1)

	if key == ord('q') or key == 27:
		break

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

capture.release()
cv2.destroyAllWindows()
