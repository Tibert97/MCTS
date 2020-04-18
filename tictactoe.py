import random
import math
import time

def reward_of_state(state,marker):
    good = 3*marker
    bad = -3*marker
    if sum(state[0:3]) == good or sum(state[3:6]) == good or sum(state[6:9]) == good or state[0]+ state[3]+state[6] == good or state[1]+ state[4]+state[7] == good or state[2]+ state[5]+state[8] == good or state[0]+ state[4]+state[8] == good or state[2]+ state[4]+state[6] == good:
        return 1
    elif sum(state[0:3]) == bad or sum(state[3:6]) == bad or sum(state[6:9]) == bad or state[0]+ state[3]+state[6] == bad or state[1]+ state[4]+state[7] == bad or state[2]+ state[5]+state[8] == bad or state[0]+ state[4]+state[8] == bad or state[2]+ state[4]+state[6] == bad:
        return -1
    else:
        return 0

def possible_actions(state):
    actions = list()
    if reward_of_state(state,1) != 0:
        return actions
    for i,s in enumerate(state):
        if s == 0:
            actions.append(i)
    return actions


def do_action(state,action,marker):
    if action == None:
        return None
    state[action] = marker
    return state

def do_action_copied(state,action,marker):
    new_state = [i for i in state]
    new_state[action] = marker
    return new_state

def print_board(state):
    print(state[:3])
    print(state[3:6])
    print(state[6:])


def create_board():
    board = [0 for _ in range(9)]
    opponent = -1
    player = 1
    turn = random.choice([-1,1])
    return board,player,opponent,turn


