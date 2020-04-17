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


class game_tree():
    def __init__(self, root,marker,parent, action, next_turn):
        self.root = root
        self.visited = 0
        self.value = 0
        self.children = None
        self.marker = marker
        self.parent = parent
        self.done_action = action
        self.next_turn = next_turn

    def selection(self):
        node = self
        while node.children:
            node = max(node.children, key = lambda c: c.upper_confidence_bound())
        return node
    
    def expansion(self):
        self.children = list()
        for action in possible_actions(self.root):
            self.children.append(game_tree(do_action_copied(self.root,action,self.next_turn),self.marker,self,action,self.next_turn*-1))
        if self.children:
            return random.choice(self.children)
        else:
            return self
    
    def rollout(self):
        tmp_state = [i for i in self.root]
        turn = self.next_turn
        while reward_of_state(tmp_state,self.marker) == 0:
            act = possible_actions(tmp_state)
            if act: 
                tmp_state = do_action(tmp_state,random.choice(act),turn)
                turn *= -1
            else:
                break
        return reward_of_state(tmp_state,self.marker)

    def backpropagation(self,result):
        node = self
        while node is not None:
            node.visited += 1
            node.value += result
            node = node.parent

    def upper_confidence_bound(self):
        if self.visited == 0:
            return math.inf
        else:
            return ((self.value*self.next_turn)/self.visited + math.sqrt(2)* math.sqrt(math.log(self.parent.visited)/self.visited))
    

def monte_carlo_tree_search(state,marker):
    root = game_tree(state,marker,None,None,marker)
    start = time.time()
    while time.time() - start < 1:
        child = root.selection()
        if child.visited == 0:
            res = child.rollout()
            child.backpropagation(res)
        else:
            child = child.expansion()
            res = child.rollout()
            child.backpropagation(res)
    return max(root.children, key = lambda c: c.visited).done_action


def create_board():
    board = [0 for _ in range(9)]
    opponent = -1
    player = 1
    turn = random.choice([-1,1])
    return board,player,opponent,turn


