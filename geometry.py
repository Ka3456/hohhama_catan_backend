import random
#道を全部書き出す　（始点,終点） （始点 < 終点）
roads = [(i,i+1) for i in range(1,54)]+[(j,3*j+7) for j in range(1,6)]+[(8+3*k,27+5*k) for k in range(0,6)]+[(9+3*l,30+5*l) for l in range(0,5)]

# カード一覧
# guard: 騎士
# road_building: 街道
# discovery: 収穫
# monoploy: 独占
# score: 得点
# カードの枚数の内訳は適当
cards = ['guard']*8 + ['road_building']*2 + ['discovery']*2 + ['monopoly']*2 + ['score']*2
shared_resources_among_players =  {'wood':0,'soil':0,'grain':0,'sheep':0,'steel':0}


#Nodeのクラスを作成
#next_roads: そのノードに隣接している道
#next_nodes: そのノードに隣接しているノード
#building: 何が建造されているか　（'Nothing': 何もなし　'House': 家　'Town': 街）
#player: 誰の建造物か　（'NoPlayer'：誰でもない　'Player_{i}'：プレイヤーi （i=1,2,3,4））
class Node(object):
    def __init__(self,next_roads = [],next_nodes=[],building = 'Nothing',player = 'NoPlayer'):
         self.next_roads = next_roads
         self.next_nodes = next_nodes
         self.building = building
         self.player = player


nodes_ownership = []
#node_1からnode_54までのインスタンスを作成してnodes_ownershipにリストとして格納
for i in range(1,55):
    next_roads = []
    next_nodes = []
    for road in roads:
        if i in road:
            next_roads.append(road)
            for node in road:
                if node != i:
                    next_nodes.append(node)

    exec('node_'+str(i)+ '= Node(next_roads = '+str(next_roads)+',next_nodes = '+str(next_nodes)+')')
    exec('nodes_ownership.append(node_{})'.format(str(i)))

#roadsの所有権を記した辞書を作成（'NoPlayer'：誰でもない　'Player_{i}'：プレイヤーi （i=1,2,3,4））
roads_ownership = {}
for road in roads:
    roads_ownership[road] = 'NoPlayer'




# Playerクラスを定義
# owned_resources: 所有している資源
# owned_nodes：　所有しているノードのリスト（道カウントされるノード：道の途中で家を建てる場合は含まない）
# owned_roads：　所有している道のリスト
# owned_houses：　所有している家のリスト
# owned_towns：　所有している街のリスト
# owned_cards：　所有しているカードのリスト
# obstacles: ブロックされているノードのリスト
# longest_road：　最長の道の長さ
# has_longest_road：　道賞判定
# dispatched_most_knights：　騎士賞判定
# score：　スコア
#TODO: 街とか家とか道の作成できる限界を設定
owned_resources = {'wood':0,'soil':0,'grain':0,'sheep':0,'steel':0}
owned_cards = {'guard':0,'road_building':0,'discovery':0,'monopoly':0,'score':0}
class Player(object):
    def __init__(self, owned_resources = owned_resources, owned_nodes = [], owned_roads = [], owned_houses = [], owned_towns=[], owned_cards=owned_cards \
             ,obstacles = [],longest_road=0, has_longest_road=False, dispatched_most_knights=False,score=0):
        self.owned_nodes = owned_nodes
        self.owned_resources =  owned_resources
        self.owned_roads = owned_roads
        self.owned_houses = owned_houses
        self.owned_towns = owned_towns
        self.owned_cards = owned_cards
        self.obstacles = obstacles
        self.longest_road = longest_road
        self.has_longest_road = has_longest_road
        self.dispatched_most_knights = dispatched_most_knights
        self.score = score

    #最初に新たな家をセットする関数 input: house_node (int), player_name (str)
    #nodes_ownershipとself.owned_nodesを結果に応じて更新
    #house_node：　新たに作る家のノード
    #player_name：　家を新たに作成したプレイヤーに合わせて 'Player_{i}' (i=1,2,3,4)とする
    def set_initial_nodes(self, house_node, player_name):
        global nodes_ownership
        #家を置こうとしているノードが占有されていないことを確かめる
        if nodes_ownership[house_node -1].player == 'NoPlayer':
            #家を置こうとしている隣接のノードが占有されていないならばcounterが隣接ノードの数と同じになる。
            counter = 0
            for next_node in nodes_ownership[house_node -1].next_nodes:
                if nodes_ownership[next_node -1].player == 'NoPlayer':
                    counter += 1
            #もし隣接ノードに全て家がなかったら家を建てることができる
            if len(nodes_ownership[house_node -1].next_nodes) == counter:
                #owned_housesに追加
                self.owned_houses.append(house_node)
                #nodes_ownershipの所有権を書き換え
                nodes_ownership[house_node -1].building == 'House'
                nodes_ownership[house_node -1].player == player_name
    
    #新たな道をセットする関数 input: road (tuple), player_name (str)
    #roads_ownershipを結果に応じて更新
    #road：　新たに作る道 (始点, 終点) (始点 < 終点)
    #player_name：　道を新たに作成したプレイヤーに合わせて 'Player_{i}' (i=1,2,3,4)とする
    def set_road(self, road, player_name):
        global roads_ownership
        #まず資源があるかを確かめる
        if (self.owned_resources['wood'] >= 1) and (self.owned_resources['soil'] >= 1):
            #そもそも道がおけるノードかどうかを確かめる
            for i, node in enumerate(road):
                if node in self.owned_nodes:
                    #その道がすでに占有されていないことを確かめる
                    if roads_ownership[road] == 'NoPlayer':
                        #資源（木1 土1）の消費
                        self.owned_resources['wood'] -= 1
                        self.owned_resources['soil'] -= 1
                        #owned_roadsに道の所有権を更新
                        self.owned_roads.append(roads)
                        roads_ownership[road] = player_name
                        #もしも道の向こう側に何も建造物が立っていない場合、owned_nodesにそのノードを追加する
                        if nodes_ownership[road[(i+1)%2]-1].player == 'NoPlayer':
                            self.owned_nodes.append(road[(i+1)%2])

    #新たな家をセットする関数 input: house_node (int), player_name (str)
    #nodes_ownershipとself.owned_nodesを結果に応じて更新
    #house_node：　新たに作る家のノード
    #player_name：　家を新たに作成したプレイヤーに合わせて 'Player_{i}' (i=1,2,3,4)とする
    def set_house(self, house_node, player_name):
        global nodes_ownership
        #まず資源があるかどうかを確かめる
        if (self.owned_resources['wood'] >= 1) and (self.owned_resources['soil'] >= 1) and (self.owned_resources['grain'] >= 1) and (self.owned_resources['sheep'] >= 1):
            #次に家を置こうとしているノードが占有されていないことを確かめる
            if house_node in self.owned_nodes:
                if nodes_ownership[house_node -1].player == 'NoPlayer':
                    #家を置こうとしている隣接のノードが占有されていないならばcounterが隣接ノードの数と同じになる。
                    counter = 0
                    for next_node in nodes_ownership[house_node -1].next_nodes:
                        if nodes_ownership[next_node -1].player == 'NoPlayer':
                            counter += 1
                    #もし隣接ノードに全て家がなかったら家を建てることができる
                    if len(nodes_ownership[house_node -1].next_nodes) == counter:
                        #資源（木1 土1 麦1 羊1）を消費
                        self.owned_resources['wood'] -= 1
                        self.owned_resources['soil'] -= 1
                        self.owned_resources['grain'] -= 1
                        self.owned_resources['sheep'] -= 1
                        #owned_housesに追加
                        self.owned_houses.append(house_node)
                        #nodes_ownershipの所有権を書き換え
                        nodes_ownership[house_node -1].building == 'House'
                        nodes_ownership[house_node -1].player == player_name
                        #TODO:家を他のプレイヤーの道の途中に置いた場合、そのプレイヤーのowned_nodesからそのノードを消去する機能


    #新たな街をセットする関数 input: house_node (int), player_name (str)
    #nodes_ownershipとself.owned_nodesを結果に応じて更新
    #house_node：　新たに作る街のノード
    #player_name： 街を新たに作成したプレイヤーに合わせて 'Player_{i}' (i=1,2,3,4)とする
    def set_town(self,town_node, player_name):
        global nodes_ownership
        #資源があるかどうかを確かめる
        if (self.owned_resources['grain'] >= 2) and (self.owned_resources['steel'] >= 3):
            #街を置こうとしているノードに自身の家があるかどうかを確かめる
            if town_node in self.house_nodes:
                #資源（麦2 鉄3）を消費
                self.owned_resources['grain'] -= 2
                self.owned_resources['steel'] -= 3
                #owned_townsに追加
                self.owned_towns.append(town_node)
                #nodes_ownershipの所有権を書き換え
                nodes_ownership[town_node -1].building == 'Town'
        return

    #新たにカードを引く関数  
    def get_card(self):
        global cards
        #資源があるかどうかを確かめる
        if (self.owned_resources['grain'] >= 2) and (self.owned_resources['sheep'] >= 1) and (self.owned_resources['steel'] >= 1):
            #cards（カードの資源）がゼロでないことを確認
            if len(cards) > 0:
                #card(カードの資源)からランダムに1枚取り出し
                random_number = random.randrange(len(cards))
                card = cards.pop(random_number)
                self.owned_cards[card] += 1
        return
    
    def longest_search(self, starting_node):
        #初めは始点を考える
        pathes = [[starting_node]]
        #カウンターで経路深さを計算
        counter = 1
        while True:
            path_len = len(pathes)
            for road in self.owned_roads:
                for path in pathes:
                    #もし既にループがある場合はスキップ
                    if path[-1] in path[:-1]:
                        continue
                    #
                    if path[-1] in self.obstacles:
                        break
                    for i in range(2):
                        if road[i] == path[-1]:
                                #次のノードの候補
                                nextnode_candidate = road[(i+1)%2]
                                #これが来た道でない場合はノードを追加
                                if path[-2] != nextnode_candidate:
                                    path_copied = path.copy().append(nextnode_candidate)
                                    pathes.append(path_copied)       
            counter += 1
            #もし1イテレーションでノードが追加されなくなったらループから脱却
            if len(pathes) == path_len:
                break
        
        return counter



    #最長の道を計算
    def calculate_longest_roads(self):
        longest_path_candidate = 0
        for node in self.owned_nodes:
            path_length = self.longest_search(node)
            if path_length > longest_path_candidate:
                longest_path_candidate = path_length
        self.longest_road = path_length

        return

    # ある始点から最長長さを算出するアルゴリズム
    # starting_nodeからの最長経路長を求める
    

            

        


player1 = Player()

