# coding=utf-8
import cv2
import numpy as np
import os


def findAllFiles(root_dir, filter):
    """
    在指定目录查找指定类型文件

    :param root_dir: 查找目录
    :param filter: 文件类型
    :return: 路径、名称、文件全路径

    """

    print("Finding files ends with \'" + filter + "\' ...")
    separator = os.path.sep
    paths = []
    names = []
    files = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(filter):
                paths.append(parent + separator)
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    print (names.__len__().__str__() + " files have been found.")
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files


def sepLongImg(img_path, ratio_num=1.414, save_path="."):
    """
    分割长图

    :param img_path: 待分割影像路径
    :param ratio_num: 分割后影像的h/w值，默认为A4纸比例1.414
    :return: 分割后的影像list
    """

    img = cv2.imread(img_path)
    width = img.shape[1]
    height = img.shape[0]
    print "Whole image width:", width
    print "Whole image height:", height
    part_height = int(width * ratio_num)
    part_num = height / part_height
    parts = []
    for i in range(1, part_num + 1):
        print i, "/", part_num
        parts.append(img[(i - 1) * part_height:i * part_height, :])
    parts.append(img[part_num * part_height:, :])

    for i in range(len(parts)):
        cv2.imwrite(save_path + "/part_" + i.__str__().zfill(2) + ".png", parts[i])
    return parts


def joinPartImgs(img_list, save_path="total.png"):
    max_width = 0
    max_height = 0
    total_height = 0
    for item in img_list:
        width = item.shape[1]
        height = item.shape[0]
        total_height += height
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

    parts = []
    for i in range(len(img_list)):
        if img_list[i].shape[1] != max_width:
            tmp_img = np.zeros([img_list[i].shape[0], max_width, 3], np.uint8) + 255
            tmp_img[:img_list[i].shape[0], :img_list[i].shape[1], 0] = img_list[i][:, :, 0]
            tmp_img[:img_list[i].shape[0], :img_list[i].shape[1], 1] = img_list[i][:, :, 1]
            tmp_img[:img_list[i].shape[0], :img_list[i].shape[1], 2] = img_list[i][:, :, 2]
            parts.append(tmp_img)
        else:
            parts.append(img_list[i])

    total_img = parts[0]
    for i in range(1, len(parts)):
        total_img = np.vstack((total_img, parts[i]))
    cv2.imwrite(save_path, total_img)
    return total_img


if __name__ == '__main__':
    parts = []
    _, _, imgs = findAllFiles("./original", ".png")
    for item in imgs:
        parts.append(cv2.imread(item))
    joinPartImgs(parts, "total.png")
    sepLongImg("total.png", save_path="./parts")
