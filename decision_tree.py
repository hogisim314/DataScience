import random
import sys
import numpy as np
ratio_array = [] # ratio를 저장하는 배열 인덱스와 ratio값이 저장 [feature의 index, ratio]
label_cnt = {} # label의 개수를 저장하는 딕셔너리 {'risky': 5, 'safe': 9}
label_table = [] # label의 종류를 저장하는 배열 ['risky', 'safe']
feature_kind = {} # feature의 종류를 저장하는 딕셔너리 {'age': ['youth', 'middle_aged', 'senior'], 'credit_rating': ['fair', 'excellent'], 'income': ['high', 'low', 'medium'], 'student': ['no', 'yes']}
max_label=0
class tree_node:
    def __init__(self, index, value, feature,parent=None, label_list=None ,label=None): 
        self.index = index
        self.value = value
        self.feature = feature
        self.parent = parent
        self.label = label
        self.label_list = []
        self.child = []
        # index는 feature의 인덱스, value는 feature의 값, label은 label의 값

    def add_child(self, child):
        self.child.append(child)

    def add_label_list(self, index):
        self.label_list.append(index)

    def get_child(self):
        return self.child

    def get_index(self):
        return self.index

    def get_value(self):
        return self.value

    def get_feature(self):
        return self.feature
    
    def get_label(self):
        return self.label
    
    def get_label_list(self):
        return self.label_list
    
    def get_parent(self):
        return self.parent
    
    def set_parent(self, parent):
        self.parent = parent
    
    def set_label(self, label):
        self.label = label

    def set_feature(self, feature):
        self.feature = feature

    def is_leaf(self):
        return len(self.child) == 0

    def is_root(self):
        return self.index == None

def get_gain_ratio(index):
    return get_gain(index) / get_split_info()

def get_split_info():
    res = 0
    for key in info_table:
            res += -(sum(info_table[key].values()) / len(data)) * np.log2(sum(info_table[key].values()) / len(data))
    return res

def get_gain(index):
    return (get_info() - get_info(index))

def compute_info(array):
    info = 0
    for i in range(len(array)):
        info += -(array[i] / sum(array)) * np.log2(array[i] / sum(array))
    return info

def get_info(index=None):
    global info_table # feature value에 따른 label의 개수를 저장하는 딕셔너리
    info_table = {}
    res = 0
    if index == None:
        for label in label_table:
            res += -(label_cnt[label] / len(data)) * np.log2(label_cnt[label] / len(data))
    else:
        for i in range(len(data)):
            feature_value = data[i][index]
            label_value = data[i][-1]
            if feature_value not in info_table:
                info_table[feature_value] = {label_value: 1}
            else:
                if label_value not in info_table[feature_value]:
                    info_table[feature_value][label_value] = 1
                else:
                    info_table[feature_value][label_value] += 1
        for key in info_table:
            res += (sum(info_table[key].values()) / len(data)) * compute_info(list(info_table[key].values()))
    return res

def cnt_label():
    n = len(features)-1
    for i in range(len(data)):
        label_value = data[i][n]

        if label_value not in label_table:
            label_table.append(label_value)

        if label_value not in label_cnt:
            label_cnt[label_value] = 1
        else:  label_cnt[label_value] += 1
    return label_cnt

def make_decision_tree(node, index):
    if index == len(features)-1:
        return
    for feature_value in feature_kind[features[ratio_dict[index][0]]]:
        child = tree_node(ratio_dict[index][0], feature_value, features[ratio_dict[index][0]], node)
        node.add_child(child)
        make_decision_tree(child, index+1)

def majority_voting(label_list):
    cnt = {}
    for label in label_list:
        if label not in cnt:
            cnt[label] = 1
        else:
            cnt[label] += 1
    return max(cnt, key=cnt.get)
    
def dfs(node):
    if node.is_leaf():
        if len(node.get_label_list()) == 0:
            temp = node.get_parent()
            temp_max_label = get_temp_max_label(temp)
            while(len(temp_max_label) == 0):
                temp = temp.get_parent()
                temp_max_label = get_temp_max_label(temp)
            node.set_label(majority_voting(temp_max_label))
            return
        else:
            if len(node.get_label_list()) == 1:
                node.set_label(node.get_label_list()[0])
            else:
                node.set_label(majority_voting(node.get_label_list()))
        return
    for child in node.get_child():
        dfs(child)

def get_temp_max_label(node): # 부모 노드의 자식들의 레이블 리스트를 받아서 가장 많은 레이블을 반환
    temp_max_label = []
    for child in node.get_child():
        if child.is_leaf():
            if len(child.get_label_list()) == 0:
                continue
            else :
                temp_max_label += child.get_label_list()
        else:
            temp_max_label += get_temp_max_label(child)
    return temp_max_label
    

def test_dfs():
    index = 0
    for row, index in zip(test_data, range(len(test_data))):
        node = root
        found = False
        while not node.is_leaf():
            for child in node.get_child():
                if row[child.get_index()] == child.get_value():
                    node = child
                    found = True
                    break
            if found:
                found = False
                continue
            # 여기까지 온거면 node.get_child에 해당하는 값이 없는 경우
            # 그냥 랜덤으로 하나 선택
            node = random.choice(node.get_child())
        # 여기까지 왔으면 leaf node에 도달한 것 레이블 값 넣어주기
        row.append(node.get_label())
    # 이제 결과 파일 만들기
    test_features.append(features[-1])
    with open(dt_result,"w") as file:
        file.write("\t".join(test_features) + "\n")
        for row in test_data:
            file.write("\t".join(row) + "\n")

def tree_traverse():
    index = 1
    for row in data:
        index+=1
        node = root
        while not node.is_leaf():
            for child in node.get_child():
                if row[child.get_index()] == child.get_value():
                    node = child
                    break
            # 여기까지 온거면 node.get_child에 해당하는 값이 없는 경우
        node.add_label_list(row[-1])

def print_tree(node, stack=[]):
    if node.is_leaf():
        stack.append(node.get_label_list())
        stack.append(node.get_label())
        print(stack)
        stack.pop()
        stack.pop()
    for child in node.get_child():
        stack.append(child.get_value())
        print_tree(child, stack)
        stack.pop()

def input():
    global dt_train, dt_test, dt_result
    dt_train=sys.argv[1]
    dt_test=sys.argv[2]
    dt_result=sys.argv[3]
    # dt_traincopy = sys.argv[4]
    # dt_temp = sys.argv[5]

    with open(dt_train, "r") as file:
        global features, data
        features = file.readline().strip().split("\t")
        data = file.readlines()
        data = [line.strip().split("\t") for line in data]
        for row in data:
            for i in range(len(row)):
                if features[i] not in feature_kind:
                    feature_kind[features[i]] = [row[i]]
                else:
                    if row[i] not in feature_kind[features[i]]:
                        feature_kind[features[i]].append(row[i])
                
    with open(dt_test, "r") as file:
        global test_data, test_features
        test_features = file.readline().strip().split("\t")
        test_data = file.readlines()
        test_data = [line.strip().split("\t") for line in test_data]

if __name__=="__main__":
    input()
    cnt_label()
    for index in range(len(features)-1):
        get_gain_ratio(index)
        ratio_array.append([index, get_gain_ratio(index)])
    ratio_dict = sorted(ratio_array, reverse=True, key=lambda x: x[1])
    # 이제부터x decision tree 생성
    root = tree_node(None, None, None) # index가 None이면 root
    max_label = max(label_cnt, key=label_cnt.get)
    make_decision_tree(root, 0)
    tree_traverse()
    dfs(root)
    test_dfs()