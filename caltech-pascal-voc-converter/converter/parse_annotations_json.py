#!/usr/bin/python

'''
input annotations file path that generated by caltech/convert_annotations.py.

return train and test images annotations sorted list.
'''

import json
import sys
from .filter import caltech_reasonable_filter
from .config import *


def parse(json_file_path, dataset_config):

    train_annos = []
    test_annos = []

    train_set = dataset_config["train_set"]
    test_set = dataset_config["test_set"]

    # for record objects and iamges num
    train_img_sum = 0
    test_img_sum = 0
    train_obj_sum = 0
    test_obj_sum = 0

    with open(json_file_path, 'r') as json_file:

        data = json.load(json_file)

        # into a video set
        for s in data.keys():
            print("set for: {}".format(s))
            # into a video
            for v in data[s].keys():
                frame_num = data[s][v]["nFrame"]
                print(
                    "* * * start process {}_{}, frame numbers: {} ...".format(s, v, frame_num))
                all_frames = data[s][v]["frames"]
                # into a frame(also a image)
                for idx in all_frames.keys():

                    # fps interval
                    if dataset_config["fps_interval"] != 0 and\
                        not (int(idx) >= dataset_config["fps_interval"] - 1 and
                             int(idx) % dataset_config["fps_interval"] == dataset_config["fps_interval"] - 1):   # Caltech dataset fps interval
                        continue

                    img_name = "{}_{}_{}.png".format(s, v, idx)
                    print("process: {}".format(img_name))
                    # print("process image: {}".format(img_name))

                    # into a pedestrian object in the image
                    if len(all_frames[idx]) == 0:
                        print("no object in: {}".format(img_name))
                        exit(-1)

                    img_recorded_flag = False
                    for obj in all_frames[idx]:

                        # reasonable filter
                        if dataset_config["version"] == "reasonable" and\
                                not dataset_config["reasonable_filter"](obj):
                            continue

                        pos = obj["pos"]
                        pos[2] = pos[2] + pos[0]
                        pos[3] = pos[3] + pos[1]
                        pos = [str(i) for i in pos]

                        obj_anno = img_name + ' ' + ' '.join(pos)

                        # record objects and images
                        if s in train_set:
                            train_annos.append(obj_anno)
                            train_obj_sum += 1
                            if not img_recorded_flag:
                                train_img_sum += 1
                                img_recorded_flag = True
                        elif s in test_set:
                            test_annos.append(obj_anno)
                            test_obj_sum += 1
                            if not img_recorded_flag:
                                test_img_sum += 1
                                img_recorded_flag = True
                        else:
                            print("unknown set error.")
                            exit(-1)

                    obj_num = len(all_frames[idx])
                    print("process {} {} object.".format(img_name, obj_num))
                print("* * * end process {}_{}...".format(v, s))
    print("process all images done\ntrain images: {}, train objests: {}\ntest images: {}, test objects: {}.".format(
        train_img_sum, train_obj_sum, test_img_sum, test_obj_sum))
    train_annos = sort_by_name(train_annos)
    test_annos = sort_by_name(test_annos)
    return (train_annos, test_annos)


# define annotations list compare function
def name_cmp(x, y):

    def get_id(name):
        return name.split(' ')[0].split('.')[0].split('_')[-1]

    x_id = get_id(x)
    y_id = get_id(y)
    if int(x_id) > int(y_id):
        return 1
    if int(x_id) < int(y_id):
        return -1
    return 0


def sort_by_name(annos):

    return sorted(annos, name_cmp)


if __name__ == "__main__":

    anno_json = sys.argv[1]
    dataset = sys.argv[2]

    if dataset == 'all':
        dataset_config = caltech_reasonable_config
        caltech_reasonable_config["version"] = "all"
    elif dataset == 'reasonable':
        dataset_config = caltech_reasonable_config
        caltech_reasonable_config["version"] = "reasonable"
    elif dataset == 'inria':
        dataset_config = inria_config
    elif dataset == 'eth':
        dataset_config = eth_reasonable_config
    else:
        print("unidentify dataset input")
        exit(-1)

    train_annos, test_annos = parse(anno_json, dataset_config)

    # print(train_annos)
    # print(test_annos)
