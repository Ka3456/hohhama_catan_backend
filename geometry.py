#道を全部書き出す　（始点,終点） （始点 < 終点）
roads = [(i,i+1) for i in range(1,54)]+[(j,3*j+7) for j in range(1,6)]+[(8+3*k,27+5*k) for k in range(0,6)]+[(9+3*l,30+5*l) for l in range(0,5)]


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
# owned_nodes：　所有しているノードのリスト
# owned_roads：　所有している道のリスト
# owned_houses：　所有している家のリスト
# owned_towns：　所有している街のリスト
# owned_cards：　所有しているカードのリスト
# longest_road：　最長の道の長さ
# has_longest_road：　道賞判定
# dispatched_most_knights：　騎士賞判定
# score：　スコア
class Player(object):
    def __init__(self, owned_nodes = [], owned_roads = [], owned_houses = [], owned_towns=[], owned_cards=[] \
             ,longest_road=0, has_longest_road=False, dispatched_most_knights=False,score=0):
        self.owned_nodes = owned_nodes
        self.owned_roads = owned_roads
        self.owned_houses = owned_houses
        self.owned_towns = owned_towns
        self.cards = owned_cards
        self.longest_road = longest_road
        self.has_longest_road = has_longest_road
        self.dispatched_most_knights = dispatched_most_knights
        self.score = score

    def set_initial_nodes(self):
        pass
    
    #新たな道をセットする関数 input: road (tuple), player_name (str)
    #roads_ownershipを結果に応じて更新
    #road：　新たに作る道 (始点, 終点) (始点 < 終点)
    #player_name：　道を新たに作成したプレイヤーに合わせて 'Player_{i}' (i=1,2,3,4)とする
    def set_road(self, road, player_name):
        global roads_ownership
        for i, node in enumerate(road):
            if node in self.owned_nodes:
                if roads_ownership[road] == 'NoPlayer':
                    if nodes_ownership[road[(i+1)%2]-1].player == 'NoPlayer':
                        self.owned_nodes.append(road[(i+1)%2])
                        self.owned_roads.append(roads)
                        roads_ownership[road] = player_name

    def set_house(self, house_node, player_name):
        pass
    def set_town(self):
        pass
    def get_card(self):
        pass
    #最長の道を計算
    def calculate_longest_roads(self):
        pass

player1 = Player()

