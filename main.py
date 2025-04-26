import subprocess
import cv2 as cv
import os


run_args = ['python', '/Users/dudi/PycharmProjects/IllegalActions/yolov5/detect.py', '--weights',
            '/Users/dudi/PycharmProjects/IllegalActions/yolov5/runs/train/exp1/best-2.pt', '--source', 'validation_set',
            '--save-txt', '--project', 'currently_detected']
classes_dict = {0: 'cigarette', 1: 'helmet', 2: 'person'}


def results():
    result = subprocess.run(run_args, capture_output=True, text=True)
    folder_str = result.stderr.split()[-1]
    return folder_str[:folder_str.rfind('/')]


destination_path = results()
images_detected_classes = {}
for dirname, _, filenames in os.walk(destination_path):
    for filename in filenames:
        temp = []
        if any(i in filename for i in ['.jpg', '.png', 'jpeg']):
            cv.imshow(f'{filename}', cv.imread(f'{destination_path}/{filename}'))
        else:
            with open(f'{destination_path}/labels/{filename}', 'r') as f:
                classes = [int(i.split(' ')[0]) for i in f.readlines()]
                for i in classes:
                    temp.append(classes_dict[i])
            images_detected_classes[filename[:filename.rfind('.')]] = temp
for i in images_detected_classes.keys():
    current_frame = images_detected_classes[i]
    if 'person' in current_frame:
        if 'cigarette' in current_frame:
            print(f'{i}: Fine for smoking')
        if 'helmet' not in current_frame:
            print(f'{i}: Fine for safety')
subprocess.run('rm -rf /Users/dudi/PycharmProjects/IllegalActions/currently_detected/*', shell=True)
cv.waitKey(0)
