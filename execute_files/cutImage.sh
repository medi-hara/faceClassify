#!/bin/bash

# 画像ディレクトリ定義
out='../data/img_origin/'

# 画像処理スクリプト名定義
script='faceRecognize.py'

for file in `ls ${out}`; do
    python ${script} ${file}
done
