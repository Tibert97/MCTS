import random
import math
import time

class game_tree():
    def __init__(self, root,marker,parent, action, next_turn,ultimate):
        self.root = root
        self.visited = 0
        self.value = 0
        self.children = None
        self.marker = marker
        self.parent = parent
        self.done_action = action
        self.next_turn = next_turn
        self.ultimate = ultimate

    def selection(self):
        node = self
        while node.children:
            node = max(node.children, key = lambda c: c.upper_confidence_bound())
        return node
    
    def expansion(self,possible_actions,do_action_copied):
        self.children = list()
        if self.ultimate:
            if self.done_action:
                for action in possible_actions(self.root,self.done_action[1]):
                    self.children.append(game_tree(do_action_copied(self.root,action,self.next_turn),self.marker,self,action,self.next_turn*-1,self.ultimate))
            else:
                for action in possible_actions(self.root,None):
                    self.children.append(game_tree(do_action_copied(self.root,action,self.next_turn),self.marker,self,action,self.next_turn*-1,self.ultimate))
        else:
            for action in possible_actions(self.root):
                self.children.append(game_tree(do_action_copied(self.root,action,self.next_turn),self.marker,self,action,self.next_turn*-1,self.ultimate))
        if self.children:
            return random.choice(self.children)
        else:
            return self
    
    def rollout(self,reward_of_state,possible_actions,do_action):
        if self.ultimate:
            tmp_state = [[j for j in i] for i in self.root]
            if self.done_action:
                act = possible_actions(tmp_state,self.done_action[1])
            else:
                act = possible_actions(tmp_state,None)
        else:
            tmp_state = [i for i in self.root]
            act = possible_actions(tmp_state)


        turn = self.next_turn
        while reward_of_state(tmp_state,self.marker) == 0:
            if act: 
                chosen_action = random.choice(act)
                tmp_state = do_action(tmp_state,chosen_action,turn)
                turn *= -1
            else:
                break

            if self.ultimate:
                    act = possible_actions(tmp_state,chosen_action[1])
            else:
                act = possible_actions(tmp_state)

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
    

def monte_carlo_tree_search(state,marker,reward_of_state,possible_actions,do_action,do_action_copied,max_time,ultimate,last_action):
    root = game_tree(state,marker,None,last_action,marker,ultimate)
    start = time.time()
    while time.time() - start < max_time:
        child = root.selection()
        if child.visited == 0:
            res = child.rollout(reward_of_state,possible_actions,do_action)
            child.backpropagation(res)
        else:
            child = child.expansion(possible_actions,do_action_copied)
            res = child.rollout(reward_of_state,possible_actions,do_action)
            child.backpropagation(res)
    print(root.visited)
    return max(root.children, key = lambda c: c.visited).done_action