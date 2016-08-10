#!/bin/bash

# 画像ディレクトリ定義
sourceDir='../data/face_only'
trainDir='../data/train'
testDir='../data/test'

# trainデータ格納用閾値
threshold=70

# カウンタ変数定義
cTrain=0
cTest=0

# 結果出力用CSV作成
trFile='trainDat.csv'
teFile='testDat.csv'

touch ${trFile}
touch ${teFile}

# 顔タイプ返却関数定義
function getFaceType () {

    case "$1" in
        "soy" ) echo 1;;
        "sio" ) echo 2;;
        "sauce" ) echo 3;;
        "miso" ) echo 4;;
    esac
}

# lsとsortを組み合わせてランダムに処理
for file in `ls ${sourceDir}/*.jpg | while read x; do echo -e "$RANDOM\t$x"; done | sort -k1,1n | cut -f 2-`; do
    # ファイル名成形
    bn=${file##*/}
    kw=${bn%%_*}

    key=`getFaceType ${kw}`

    if [ `expr $RANDOM % 100` -lt ${threshold} ] ; then
        #train用のデータ
        cp ${file} ${trainDir}/${bn}
        echo "${file},${key}" >> ${trFile}
        cTrain=$((cTrain+1))
    else
        #test用のデータ
        cp ${file} ${testDir}/${bn}
        echo "${file},${key}" >> ${teFile}
        cTest=$((cTest+1))
    fi
done

echo "Train:${cTrain}"
echo "Test:${cTest}"
