# Copyright (c) 2020 Huawei Technologies Co., Ltd.
# Licensed under CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike 4.0 International) (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
#
# The code is released for academic research use only. For commercial use, please contact Huawei Technologies Co., Ltd.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import os
import sys

import numpy as np
import random
import imageio
import pickle
from natsort import natsort
from tqdm import tqdm

def get_img_paths(dir_path, wildcard='*.png'):
    return natsort.natsorted(glob.glob(dir_path + '/' + wildcard))

def create_all_dirs(path):
    if "." in path.split("/")[-1]:
        dirs = os.path.dirname(path)
    else:
        dirs = path
    os.makedirs(dirs, exist_ok=True)

def to_pklv4(obj, path, vebose=False):
    create_all_dirs(path)
    with open(path, 'wb') as f:
        pickle.dump(obj, f, protocol=4)
    if vebose:
        print("Wrote {}".format(path))


def random_crop(img0, img1, size):
    THRESHOLD = 0.8
    h, w, c = img0.shape
    is_valid = False
    count = 0
    while is_valid == False and count < 10:
        count += 1
        h_start = np.random.randint(0, h - size)
        h_end = h_start + size

        w_start = np.random.randint(0, w - size)
        w_end = w_start + size

        is_valid = (img0[h_start:h_end, w_start:w_end] > 0 ).sum() / size ** 2 > THRESHOLD

    return img0[h_start:h_end, w_start:w_end], img1[h_start:h_end, w_start:w_end]


def imread(img_path):
    img = imageio.imread(img_path)
    if len(img.shape) == 2:
        # img = np.stack([img, ] * 3, axis=2)
        img = np.expand_dims(img, axis=2)
    return img


def to_pklv4_1pct(obj, path, vebose):
    n = int(round(len(obj) * 0.01))
    path = path.replace(".", "_1pct.")
    to_pklv4(obj[:n], path, vebose=True)


def main(dir_path_lr, dir_path_hr):
    hrs = []
    lqs = []

    img_paths_lr = get_img_paths(dir_path_lr)
    img_paths_hr = get_img_paths(dir_path_hr)
    for lr_path, hr_path in tqdm(zip(img_paths_lr, img_paths_hr)):
        lr = imread(lr_path)
        hr = imread(hr_path)
        for i in range(10):
            lr_crop, hr_crop = random_crop(lr, hr, 160)
            hrs.append(lr_crop)
            lqs.append(hr_crop)

    shuffle_combined(hrs, lqs)

    hrs_path = get_out_path(dir_path_lr)
    to_pklv4(hrs, hrs_path, vebose=True)
    to_pklv4_1pct(hrs, hrs_path, vebose=True)

    lqs_path = get_out_path(dir_path_hr)
    to_pklv4(lqs, lqs_path, vebose=True)
    to_pklv4_1pct(lqs, lqs_path, vebose=True)


def get_out_path(dir_path):
    base_dir = os.path.dirname(dir_path)
    condition = os.path.basename(base_dir)
    name = os.path.basename(dir_path)
    hrs_path = os.path.join(base_dir, 'pkls', condition + '_' + name + '.pklv4')
    return hrs_path

def shuffle_combined(hrs, lqs):
    combined = list(zip(hrs, lqs))
    random.shuffle(combined)
    hrs[:], lqs[:] = zip(*combined)


if __name__ == "__main__":
    dir_path_lr, dir_path_hr = sys.argv[1], sys.argv[2]
    assert os.path.isdir(dir_path_lr)
    assert os.path.isdir(dir_path_hr)
    main(dir_path_lr, dir_path_hr)
