import random
import math
import time

def reward_of_substate(state,marker):
    good = 3*marker
    bad = -3*marker
    if sum(state[0:3]) == good or sum(state[3:6]) == good or sum(state[6:9]) == good or state[0]+ state[3]+state[6] == good or state[1]+ state[4]+state[7] == good or state[2]+ state[5]+state[8] == good or state[0]+ state[4]+state[8] == good or state[2]+ state[4]+state[6] == good:
        return 1
    elif sum(state[0:3]) == bad or sum(state[3:6]) == bad or sum(state[6:9]) == bad or state[0]+ state[3]+state[6] == bad or state[1]+ state[4]+state[7] == bad or state[2]+ state[5]+state[8] == bad or state[0]+ state[4]+state[8] == bad or state[2]+ state[4]+state[6] == bad:
        return -1
    else:
        return 0

def reward_of_state(state,marker):
    good = 3*marker
    bad = -3*marker
    if reward_of_substate(state[0],marker)+reward_of_substate(state[1],marker)+reward_of_substate(state[2],marker) == good or reward_of_substate(state[3],marker)+reward_of_substate(state[4],marker)+reward_of_substate(state[5],marker) == good or reward_of_substate(state[6],marker)+reward_of_substate(state[7],marker)+reward_of_substate(state[8],marker) == good or reward_of_substate(state[0],marker)+ reward_of_substate(state[3],marker)+reward_of_substate(state[6],marker) == good or reward_of_substate(state[1],marker)+ reward_of_substate(state[4],marker)+reward_of_substate(state[7],marker)== good or reward_of_substate(state[2],marker)+ reward_of_substate(state[5],marker)+reward_of_substate(state[8],marker) == good or reward_of_substate(state[0],marker)+ reward_of_substate(state[4],marker)+reward_of_substate(state[8],marker) == good or reward_of_substate(state[2],marker)+ reward_of_substate(state[4],marker)+reward_of_substate(state[6],marker)== good:
        return 1
    elif reward_of_substate(state[0],marker)+reward_of_substate(state[1],marker)+reward_of_substate(state[2],marker) == bad or reward_of_substate(state[3],marker)+reward_of_substate(state[4],marker)+reward_of_substate(state[5],marker) == bad or reward_of_substate(state[6],marker)+reward_of_substate(state[7],marker)+reward_of_substate(state[8],marker) == bad or reward_of_substate(state[0],marker)+ reward_of_substate(state[3],marker)+reward_of_substate(state[6],marker) == bad or reward_of_substate(state[1],marker)+ reward_of_substate(state[4],marker)+reward_of_substate(state[7],marker) == bad or reward_of_substate(state[2],marker)+ reward_of_substate(state[5],marker)+reward_of_substate(state[8],marker) == bad or reward_of_substate(state[0],marker)+ reward_of_substate(state[4],marker)+reward_of_substate(state[8],marker) == bad or reward_of_substate(state[2],marker)+ reward_of_substate(state[4],marker)+reward_of_substate(state[6],marker) == bad:
        return -1
    else:
        return 0

def possible_actions(state,last_played):
    if not last_played or reward_of_substate(state[last_played],1) != 0:
        actions = list()
        if reward_of_state(state,1) != 0:
            return actions
        for h,sub_board in enumerate(state):
            if reward_of_substate(sub_board,1) != 0:
                continue
            for i,s in enumerate(sub_board):
                if s == 0:
                    actions.append((h,i))
        return actions
    actions = list()
    if reward_of_state(state,1) != 0:
        return actions

    for i,s in enumerate(state[last_played]):
        if s == 0:
            actions.append((last_played,i))
    return actions

def do_action(state,action,marker):
    if action == None:
        return None
    state[action[0]][action[1]] = marker
    return state

def do_action_copied(state,action,marker):
    new_state = [[i for i in j] for j in state]
    new_state[action[0]][action[1]] = marker
    return new_state

def print_board(state):
    for i in range(9):
        print(state[i][:3])
        print(state[i][3:6])
        print(state[i][6:])
        print()


def create_board():
    board = [[0 for _ in range(9)] for __ in range(9)]
    opponent = -1
    player = 1
    turn = random.choice([-1,1])
    return board,player,opponent,turn



