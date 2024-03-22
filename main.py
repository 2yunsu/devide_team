#!/bin/python3

from random import choice
import random
from heapq import heappop, heappush, heapify
def create_player_list(filename, isset=True):
    # create a list of players from a file
    players = []
    file = open(filename, 'r', encoding="UTF-8")
    players = list(file.read().splitlines())
    random.shuffle(players)
    if isset:
        return set(players)
    else:
        return players
    
def select_n_players(players, n):
    original_type = type(players)
    if original_type == set:
        players_list = list(players)
    else:
        players_list = players
    selected_guys = []
    if len(players) < n:
        # print(f"player 수가 {len(players)}명이고 요청한 배정인원은 {n}명이어서 할당을 못합니다.")
        pass
    else:
        rand_list = list(range(len(players)))
        random.shuffle(rand_list)
        selected_guys = players_list[:n]
        players_list = players_list[n:]

    if original_type == set:
        return set(selected_guys), set(players_list)
    else:
        return selected_guys, players_list

def _matching(players, team_list):
    assert type(team_list) == list

    q = [[len(team_list[i]), i] for i in range(len(team_list))]
    heapify(q)
    for player in players:
        tnum, tidx = heappop(q)
        #tidx에 player를 집어넣자
        team_list[tidx].append(player)
        assert len(team_list[tidx]) == tnum+1
        heappush(q, [tnum+1, tidx])
    return team_list



    
'''
player_list와 team_list, team_list_genders필요
if 성비고려: 이것도 남자인원 여자인원 따로 for loop돌리면 될듯?
for player in player_list
min_boy_num
min_gril_num

else:
a = heapq 생성 (팀인덱스, 인원)
for player in player_list:
    tidx, tnum = heapq pop
    tidx팀에 player를 집어넣자


'''
#균일한 수로 사람 할당, 결과적으로 team_list에 있는 모든 팀들의 수가 고르게 분포됨
def match_players_randomly(players, team_list):
    original_type = type(players)
    if original_type == set:
        players_list = list(players)
    else:
        players_list = players[:]
    
    return _matching(players_list, team_list)


def divide_boy_and_girl_team_list(team_list, boys, girls):
    # NOTICE: boy girl team list만들고 boys와 girls에서 해당 이름을 삭제한다.
    boys_team_list = [[] for _ in range(len(team_list))]
    girls_team_list = [[] for _ in range(len(team_list))]
    for i, team in enumerate(team_list):
        for t in team:
            if t in boys:
                boys_team_list[i].append(t)
                boys.remove(t)
            elif t in girls:
                girls_team_list[i].append(t)
                girls.remove(t)
            else:
                #성별 고려 안함
                if random.random() < 0.5:
                    boys_team_list[i].append(t)
                    try:
                        boys.remove(t)
                    except KeyError:
                        pass
                else:
                    girls_team_list[i].append(t)
                    try:
                        girls.remove(t)
                    except KeyError:
                        pass
            
    return boys_team_list, girls_team_list  

def merge_boyteam_with_girlteam(boys_final, girls_final):
    assert len(boys_final) == len(girls_final)
    qboy = [[len(boys_final[i]), i] for i in range(len(boys_final))]
    qgirl = [[-len(girls_final[i]), i] for i in range(len(girls_final))]
    heapify(qboy)
    heapify(qgirl)
    final_team = [[] for _ in range(len(boys_final))]
    i = 0
    while len(qboy) > 0:
        _, bidx = heappop(qboy)
        _, gidx = heappop(qgirl)
        final_team[i].extend(boys_final[bidx])
        final_team[i].extend(girls_final[gidx])
        i += 1
    return final_team


    
ISSET = True # True면 boys, girls profs 모두 set으로 관리, 아니면 list로 관리
#남성, 여성, 교수님에 대한 set을 만듭니다.(중복가능)
#NOTICE: 교수님들 성별 고려해서 짜고 싶을때는 girls.txt, boys.txt에도 이름 적어주기
boys = create_player_list('boys.txt', ISSET)
girls = create_player_list('girls.txt', ISSET)
profs = create_player_list('professor.txt', ISSET)
# print(select_n_players(boys, 0))
# print(select_n_players(boys, 10))




#팀을 몇개로 구성할 겁니까?
team_num = int(input("팀은 몇 개로 구성할 겁니까?: "))
team_list = [[] for _ in range(team_num)]


#교수님&포닥분들을 각각 다른 팀에 배정 하시겠습니까?
prof_sep = input("교수님&포닥분들을 최대한 다른 팀에 배정 하시겠습니까?(Y or N): ")
if prof_sep.lower() == 'y':
    match_players_randomly(profs, team_list)
    
    
elif prof_sep.lower() == 'n':
    
    while len(profs) != 0:
        selected, profs = select_n_players(profs, 1)
        cnt = random.randint(0, team_num-1)
        team_list[cnt].append(next(iter(selected)))
        cnt %= team_num
else:
    raise NotImplementedError

#성비맞추기
boys_team_list, girls_team_list = divide_boy_and_girl_team_list(team_list, boys, girls)
boys_final = match_players_randomly(boys, boys_team_list)
girls_final = match_players_randomly(girls, girls_team_list)
final_team = merge_boyteam_with_girlteam(boys_final, girls_final)

print("FINAL TEAM")
f = open("teammatch.txt",'w')
for t in range(team_num):
    print(f"TEAM {t}: {final_team[t]}")
    f.write(f"TEAM {t}: {final_team[t]}\n")
