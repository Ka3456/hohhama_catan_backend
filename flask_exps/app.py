from flask import Flask, render_template, redirect, url_for
import cv2
import numpy as np

app = Flask(__name__, static_folder='./static')
app.secret_key = b'random string...'




#データベース（仮）

#ログイン情報
login_inf=[]


#マップのデータ
land_indices = [2, 3, 1, 0, 5, 2, 3, 1, 0, 5, 2, 3, 1, 0, 5, 2, 3, 1, 0]  # 初期の land_indices
photo_indices = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 1, 0]  # 要調整


#個人の資源管理

player1 = [
    ("Score", 7),
    ("Wood", 5),
    ("Wheat", 4),
    ("Sheep", 3),
    ("Brick", 6),
    ("Iron", 2),
    ("Knights_Owned", 3),
    ("Knights_Used", 1),
    ("Monopoly_Cards", 2),
    ("Monopoly_Cards_Used", 4),
    ("Harvest_Cards", 5),
    ("Harvest_Cards_Used", 3),
    ("Roads_Owned", 5),
    ("Roads_Built", 2),
    ("Victory_Points", 4),
    ("Houses_Owned", 5),
    ("Houses_Available", 3),
    ("Cities_Owned", 5),
    ("Cities_Available", 2),
    ("Roads_Owned", 4),
    ("Roads_Available", 3)
]
player2 = [
    ("Score", 7),
    ("Wood", 5),
    ("Wheat", 4),
    ("Sheep", 3),
    ("Brick", 6),
    ("Iron", 2),
    ("Knights_Owned", 3),
    ("Knights_Used", 1),
    ("Monopoly_Cards", 2),
    ("Monopoly_Cards_Used", 4),
    ("Harvest_Cards", 5),
    ("Harvest_Cards_Used", 3),
    ("Roads_Owned", 5),
    ("Roads_Built", 2),
    ("Victory_Points", 4),
    ("Houses_Owned", 5),
    ("Houses_Available", 3),
    ("Cities_Owned", 5),
    ("Cities_Available", 2),
    ("Roads_Owned", 4),
    ("Roads_Available", 3)
]
player3 = [
    ("Score", 7),
    ("Wood", 5),
    ("Wheat", 4),
    ("Sheep", 3),
    ("Brick", 6),
    ("Iron", 2),
    ("Knights_Owned", 3),
    ("Knights_Used", 1),
    ("Monopoly_Cards", 2),
    ("Monopoly_Cards_Used", 4),
    ("Harvest_Cards", 5),
    ("Harvest_Cards_Used", 3),
    ("Roads_Owned", 5),
    ("Roads_Built", 2),
    ("Victory_Points", 4),
    ("Houses_Owned", 5),
    ("Houses_Available", 3),
    ("Cities_Owned", 5),
    ("Cities_Available", 2),
    ("Roads_Owned", 4),
    ("Roads_Available", 3)
]
player4 = [
    ("Score", 7),
    ("Wood", 5),
    ("Wheat", 4),
    ("Sheep", 3),
    ("Brick", 6),
    ("Iron", 2),
    ("Knights_Owned", 3),
    ("Knights_Used", 1),
    ("Monopoly_Cards", 2),
    ("Monopoly_Cards_Used", 4),
    ("Harvest_Cards", 5),
    ("Harvest_Cards_Used", 3),
    ("Roads_Owned", 5),
    ("Roads_Built", 2),
    ("Victory_Points", 4),
    ("Houses_Owned", 5),
    ("Houses_Available", 3),
    ("Cities_Owned", 5),
    ("Cities_Available", 2),
    ("Roads_Owned", 4),
    ("Roads_Available", 3)
]





#ここからがアプリのコード




@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')



@app.route('/index', methods=['GET'])
def index():

    #プレイヤーのデータを取得
    global player1
    global player2
    global player3
    global player4

    # 画像のパス
    map_path = './templates/images/map.png'
    land_path = './templates/images/land.png'
    settlement_path = './templates/images/settlement.png'

    # 画像の読み込み
    map_img = cv2.imread(map_path)
    land_img = cv2.imread(land_path)
    settlement_img = cv2.imread(settlement_path)

    # トリミングして新しい画像を作成
    global land_indices
    num_photos = 6
    photo_width = land_img.shape[1] // num_photos

    photo_imgs = []
    for photo_index in land_indices:
        x_start = photo_index * photo_width
        x_end = (photo_index + 1) * photo_width
        trimmed_photo = land_img[:, x_start:x_end, :]
        photo_imgs.append(trimmed_photo)

    # 新しい画像を表示したい座標 [(x1, y1), (x2, y2), ...] に重ねる
    photo_coordinates = [(136, 60), (206, 60), (275, 60), (103, 120), (173, 120),
                         (243, 120), (313, 120), (70, 177), (140, 177), (210, 177),
                         (280, 177), (345, 177), (104, 235), (174, 235), (245, 235),
                         (315, 235), (140, 293), (210, 293), (280, 293)]  # 座標を調整（要調整）

    for i, (x, y) in enumerate(photo_coordinates):
        if 0 <= x < map_img.shape[1] and 0 <= y < map_img.shape[0]:
            rows, cols, channels = photo_imgs[i].shape
            for j in range(rows):
                for k in range(cols):
                    if photo_imgs[i][j, k, 0] != 0 or photo_imgs[i][j, k, 1] != 0 or photo_imgs[i][j, k, 2] != 0:
                        map_img[y + j, x + k] = photo_imgs[i][j, k]

    # トリミングしたsettlement画像を合成
    global photo_indices   # 要調整
    num = 9
    settlement_width = settlement_img.shape[1] // num
    settlement_height = settlement_img.shape[0]

    # 手動で指定された座標
    settlement_coordinates = [(265, 60), (195, 60), (90, 155), (160, 155), (230, 155),
                              (300, 155), (370, 155), (124, 220), (195, 220), (55, 220),
                              (265, 220), (335, 220)]

    for i, (photo_index, (x, y)) in enumerate(zip(photo_indices, settlement_coordinates)):
        x_start = photo_index * settlement_width
        x_end = (photo_index + 1) * settlement_width
        trimmed_settlement = settlement_img[:, x_start:x_end, :]

        rows, cols, channels = trimmed_settlement.shape
        for j in range(rows):
            for k in range(cols):
                if trimmed_settlement[j, k, 0] != 0 or trimmed_settlement[j, k, 1] != 0 or trimmed_settlement[j, k, 2] != 0:
                    map_img[y + j, x + k] = trimmed_settlement[j, k]

    # 重ねた結果を保存して表示
    composite_path = './static/composite.png'
    cv2.imwrite(composite_path, map_img)

    return render_template('index.html', composite_path=composite_path, player1=player1, player2=player2, player3=player3, player4=player4 )    


# 新しいルートを追加
@app.route('/increment_index', methods=['GET'])
def increment_index():
    global photo_indices
    photo_indices[0] += 1  # 最初の要素を+1する
    return redirect(url_for('index'))


@app.route('/decreacement_index', methods=['GET'])
def decreacement_index():
    global photo_indices
    photo_indices[0] -= 1  # 最初の要素を-1する
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
