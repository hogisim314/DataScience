import sys
import itertools
# lk를 만드는 함수
def make_lk(candidateList,min_support_cnt):
    frequent_pattern=dict()
    for candidate in candidateList:
        if candidateList[candidate]>=min_support_cnt:
            frequent_pattern[candidate]=candidateList[candidate]
    return frequent_pattern
# association rule을 만드는 함수
def get_asso_rule(frequent_pattern_list, data, minimum_support):
    rules = []
    for fp in frequent_pattern_list:
        if len(fp)==0 or len(fp)==1: continue
        # len이 2 이상이여야 rule 만들수있음
        for size in range(1,len(fp)):
            combi=itertools.combinations(fp,size)
            # set중에서 combination을 돌면서 만들어준다.
            for left_side in combi:
                # combination 중 하나를 선택 한걸 left라고 친다. 
                right_side = []
                for pattern in fp :
                    if pattern not in left_side:
                        right_side.append(pattern)
                # combination left_side중 아닌걸 right_side에 넣어준다. 
                support = round(frequent_pattern_list[fp] * 100 / len(data), 2)
                confidence = round(frequent_pattern_list[fp] * 100 / frequent_pattern_list[left_side], 2)
                if (support>=minimum_support):
                    rules.append((left_side, right_side, support, confidence))
    return rules
# ck를 만드는 함수 
def make_ck(data,size):
    candidate=dict()
    for transaction in data:
        for item in itertools.combinations(transaction,size):
            item=tuple(sorted(item))
            if item in candidate:
                candidate[item] += 1
                # 있으면 갯수 ++
            else:
                candidate[item] = 1 # 없으면 그냥 1로 만들어줌
    return candidate
# apriori함수 size1 -> size2 -> size3 증가시킴
def apriori(data,min_support):
    frequent_pattern=dict()
    size=2
    candidateList=make_ck(data,1)
    prunedCand=make_lk(candidateList,min_support)
    frequent_pattern.update(prunedCand)
    while True:
        candidate_itemset=make_ck(data,size)
        prunedCand=make_lk(candidate_itemset,min_support)
        if not prunedCand:
            break
        frequent_pattern.update(prunedCand)
        size+=1
    return frequent_pattern

if __name__=="__main__":
    minimum_support=int(sys.argv[1])
    input_file=sys.argv[2]
    output_file=sys.argv[3]

    ifile=open(input_file,'r')
    lines=ifile.readlines()

    transactionList = []

    for line in lines:
        items=line.strip('\n').split('\t')
        new_items = []
        for item in items:
            new_items.append(int(item))
        transactionList.append(new_items)

    min_sup_cnt = minimum_support * len(transactionList) / 100
    frequent_pattern=apriori(transactionList,min_sup_cnt)
    rules=get_asso_rule(frequent_pattern,transactionList, minimum_support)
    ofile=open(output_file,'w')
    for rule in rules:
            left_side = '{' + ', '.join(map(str, rule[0])) + '}'
            right_side = '{' + ', '.join(map(str, rule[1])) + '}'
            support_formatted = "{:.2f}".format(rule[2])  # 소수점 두 자리까지 포맷팅
            confidence_formatted = "{:.2f}".format(rule[3])  # 소수점 두 자리까지 포맷팅
            ofile.write(f"{left_side}\t{right_side}\t{support_formatted}\t{confidence_formatted}\n")
    ifile.close()
    ofile.close()