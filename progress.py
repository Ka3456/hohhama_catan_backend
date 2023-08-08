import geometry
import random
#ここでゲームの進行を記述する

#Playerインスタンスを格納したリスト
players = []


#サイコロを振る
#1つ目のサイコロ、2つ目のサイコロ、2つの合計値を返す
def dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1,die2,die1+die2)

#初めにプレーヤーの選択(4人まで)
#TODO:名前とか入れる？（その場合はPlayer classの引数に名前が必要）
def player_selection():
    players_number = len(players)
    if players_number < 4:
        players.append(geometry.Player())

#まず最初に家と道を二つずつ設置
def initial_position():
    for i,player in enumerate(players):
        player_name = 'Player_'+ str(i+1)
        #TODO:データをどのようにやり取りするかを考える




