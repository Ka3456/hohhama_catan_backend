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
# owned_resources: 所有している資源
# owned_nodes：　所有しているノードのリスト（道カウントされるノード：道の途中で家を建てる場合は含まない）
# owned_roads：　所有している道のリスト
# owned_houses：　所有している家のリスト
# owned_towns：　所有している街のリスト
# owned_cards：　所有しているカードのリスト
# longest_road：　最長の道の長さ
# has_longest_road：　道賞判定
# dispatched_most_knights：　騎士賞判定
# score：　スコア
owned_resources = {'wood':0,'soil':0,'grain':0,'sheep':0,'iron':0}
class Player(object):
    def __init__(self, owned_resources = owned_resources, owned_nodes = [], owned_roads = [], owned_houses = [], owned_towns=[], owned_cards=[] \
             ,longest_road=0, has_longest_road=False, dispatched_most_knights=False,score=0):
        self.owned_nodes = owned_nodes
        self.owned_resources =  owned_resources
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
        #まず資源があるかを確かめる
        if (self.owned_resources['wood'] >= 1) and (self.owned_resources['soil'] >= 1):
            #そもそも道がおけるノードかどうかを確かめる
            for i, node in enumerate(road):
                if node in self.owned_nodes:
                    #その道がすでに占有されていないことを確かめる
                    if roads_ownership[road] == 'NoPlayer':
                        #資源の消費
                        self.owned_resources['wood'] -= 1
                        self.owned_resources['soil'] -= 1
                        #owned_roadsに道の所有権を更新
                        self.owned_roads.append(roads)
                        roads_ownership[road] = player_name
                        #もしも道の向こう側に何も建造物が立っていない場合、owned_nodesにそのノードを追加する
                        if nodes_ownership[road[(i+1)%2]-1].player == 'NoPlayer':
                            self.owned_nodes.append(road[(i+1)%2])


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
                        #nodes_ownershipの所有権を書き換え
                        nodes_ownership[house_node -1].building == 'House'
                        nodes_ownership[house_node -1].player == player_name
                        #TODO:家を他のプレイヤーの道の途中に置いた場合、そのプレイヤーのowned_nodesからそのノードを消去する機能


    def set_town(self):
        pass
    def get_card(self):
        pass
    #最長の道を計算
    def calculate_longest_roads(self):
        pass

player1 = Player()

