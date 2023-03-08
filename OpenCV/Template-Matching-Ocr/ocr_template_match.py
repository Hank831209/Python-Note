"""
任務: 信用卡數字辨識
先透過形態學、邊緣檢測、二值化、比對長寬比例等圖像預處理操作將信用卡數字區塊切出來，
再透過模板匹配的方式對數字進行一一對應看是否相同來完成

檢測流程:
1. 讀去數字匹配模板，並完成切分，即0123456789 --> 0, 1, 2...
2. 從信用卡上找出感興趣的區域(卡號):
2.1. tophat: 增強圖片中感興趣的明亮物體
2.2. Sobel邊緣檢測 找出連載一起的物體的邊緣
2.3. THRESH_OTSU、閉操作(先膨脹再侵蝕)，將區塊內部的黑色部分補滿
2.4. 依據長寬比例篩過濾掉不感興趣的輪廓
3. 從感興趣的區域(信用卡號)中切出數字並與模板進行匹配，即1234 --> 1, 2, 3..
"""
import numpy as np
import argparse
import cv2
import myutils

# 參數設置
parser = argparse.ArgumentParser()
parser.add_argument("--image", default=r"images/credit_card_02.png", help="path to input image")
parser.add_argument("--template", default=r"ocr_a_reference.png", help="path to template OCR-A image")
opt = vars(parser.parse_args())

# 繪圖程式
def cv_show(name, img):
	cv2.imshow(name, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
 
# 讀取模板圖像
img = cv2.imread(opt["template"])
cv_show('img', img)
# 灰階圖
ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv_show('Gray', ref)
# 二值化, 黑底白字
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]  
cv_show('ref_THRESH_BINARY_INV', ref)

# 計算輪廓
# cv2.findContours(): 輸入二值圖(黑白的)，不是灰度圖
# cv2.RETR_EXTERNAL: 只檢測外輪廓
# cv2.CHAIN_APPROX_SIMPLE: 只保留終點座標

refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# -1: 要畫所有的輪廓
cv2.drawContours(img, refCnts, -1, (0,0,255), 3) 
cv_show('img',img)
print("總共幾個輪廓: ", len(refCnts))
# cnts: 所有輪廓點, boundingBoxes: xywh
refCnts, refBoundingBoxes = myutils.sort_contours(refCnts, method="left-to-right")  # 排序: 左到右
digits = {}

# 遍歷每一個bbox，從原始圖像(ref黑底白字)切出模板並保存
for (idx, b) in enumerate(refBoundingBoxes):
	(x, y, w, h) = b
	roi = ref[y:y + h, x:x + w]  # 切出模板的外接矩形
	roi = cv2.resize(roi, (57, 88))
	cv_show("roi", roi)
	digits[idx] = roi  # 每個數字對應一個模板並保存

# 初始化卷積核
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 對輸入圖像進行預處理
image = cv2.imread(opt["image"])
cv_show('image', image)
image = myutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv_show('gray', gray)

# 禮帽: 用於增強圖片中感興趣的明亮物體
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel) 
cv_show('tophat',tophat) 

# ksize=-1 等同於用3*3的
gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)

# 正規化
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
gradX = gradX.astype("uint8")

print (np.array(gradX).shape)
cv_show('gradX', gradX)

# 閉操作(先膨脹再侵蝕)，將靠近的數字區塊連在一起
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel) 
cv_show('gradX', gradX)

# THRESH_OTSU自動尋找適合的閥值，適合雙峰，須把閥值參數設置為0
thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 
cv_show('thresh', thresh)

# 閉操作(先膨脹再侵蝕)，將區塊內部的黑色部分補滿
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
cv_show('thresh',thresh)

# 計算輪廓
threshCnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = threshCnts
cur_img = image.copy()
cv2.drawContours(cur_img, cnts, -1, (0,0,255), 3) 
cv_show('img', cur_img)


# 遍歷輪廓
locs = []
for c in cnts:
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)  # 長寬比

	# 選擇合適的區域(根據長寬比例)
	if ar > 2.5 and ar < 4.0:

		if (w > 40 and w < 55) and (h > 10 and h < 20):
			# 滿足要求的保存
			locs.append((x, y, w, h))

# 左到右排序
locs = sorted(locs, key=lambda x:x[0])
output = []

# 遍歷每個輪廓的每個數字
for (i, (gX, gY, gW, gH)) in enumerate(locs):
	# initialize the list of group digits
	groupOutput = []

	# 取的輪廓再寬一些
	group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
	cv_show('group', group)
	# 預處理
	group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	cv_show('group',group)
	# 把每一組輪廓再切分，ex: 5412, 8787...
	digitCnts, hierarchy = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	digitCnts = myutils.sort_contours(digitCnts, method="left-to-right")[0]
	
	# 計算每一組中的每一個數值，ex: 5, 4, 1, 2...
	for c in digitCnts:
		# 找到当前数值的轮廓，resize成合适的的大小
		(x, y, w, h) = cv2.boundingRect(c)
		roi = group[y:y + h, x:x + w]
		roi = cv2.resize(roi, (57, 88))
		cv_show('roi',roi)

		# 匹配分數
		scores = []

		# 計算模板匹配分數
		# key, value
		for (digit, digitROI) in digits.items():
			# 模板匹配
			result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
			(_, max_score, _, _) = cv2.minMaxLoc(result)  # min, max, min_loc, max_loc
			scores.append(max_score)

		# 得到最適合的數字
		groupOutput.append(str(np.argmax(scores)))

	# 畫圖
	cv2.rectangle(image, (gX - 5, gY - 5), (gX + gW + 5, gY + gH + 5), (0, 0, 255), 1)
	cv2.putText(image, "".join(groupOutput), (gX, gY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

	# 得到结果
	output.extend(groupOutput)

# 打印结果
print("Credit Card #: {}".format("".join(output)))
cv2.imshow("Image", image)
cv2.waitKey(0)