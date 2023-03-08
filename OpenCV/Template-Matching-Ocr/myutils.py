import cv2


def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True  # 大到小排序

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1  # 基於y座標排序
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 找出可以包圍所有點的最小矩形 返回(x, y, w, h)
    # 基於boundingBoxes的x座標去排序
    (boundingBoxes, cnts) = zip(*sorted(zip(boundingBoxes, cnts), key=lambda x: x[0][i], reverse=reverse))
    return (cnts, boundingBoxes)


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    else:
        ratio = width / float(w)  # 等比例縮放
        dim = (width, int(h * ratio))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized