# -*- coding: utf-8 -*-

import sys
import cv2

# 引数格納
params = sys.argv
argc = len(params)

if(argc != 2):
    print '引数を指定して実行してください。'
    quit()

# 画像ディレクトリ定義
inDir = "../data/img_origin/"
outDir = "../data/face_only/"
errDir = "../data/error/"

#HAAR分類器ロード　※必要に応じて変更してください。
cascade_path = "/usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"

# 執筆時デフォルトで含まれている顔認識データセット
# haarcascade_frontalface_default.xml
# haarcascade_frontalface_alt.xml
# haarcascade_frontalface_alt2.xml
# haarcascade_frontalface_alt_tree.xml
# haarcascade_profileface.xml

image_path = inDir + params[1]

print image_path

#ファイル読み込み
image = cv2.imread(image_path)
if(image is None):
    print '画像を開けません。'
    quit()

#グレースケール変換
image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

#物体認識（顔認識）の実行
facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

if len(facerect) == 1:
    print "顔認識に成功しました。"
    print facerect

    #検出した顔の処理
    for rect in facerect:
        #顔だけ切り出して保存
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]
        dst = image[y:y+height, x:x+width]
        new_image_path = outDir + params[1]
        cv2.imwrite(new_image_path, dst)

elif len(facerect) > 1:
    # 複数顔が検出された場合はスキップ
    print "顔が複数認識されました"
    print facerect

    if len(facerect) > 0:
        color = (255, 255, 255) #白
        for rect in facerect:
            #検出した顔を囲む矩形の作成
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)

        #認識結果の保存
        new_image_path = errDir + params[1]
        cv2.imwrite(new_image_path, image)

    quit()

else:
    # 顔検出に失敗した場合もスキップ
    print "顔が認識できません。"
    quit()
