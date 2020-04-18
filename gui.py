import tkinter as tk
import random
import sys 
import os
import mcts_general as mcts
import tictactoe as ttt
import ultimatetictactoe as uttt

def mark(button):
    global buttons
    if buttons[button]['text'] is '':
        buttons[button].configure(text = 'X')
        clicked_button.set(button)

def ai_mark_uttt(button):
    global buttons
    buttons[button[0]*9+button[1]].configure(text = 'O')

def ai_mark(button):
    global buttons
    buttons[button].configure(text = 'O')

def restart_program():
    #https://stackoverflow.com/questions/41655618/restart-program-tkinter
    python = sys.executable
    os.execl(python, python, * sys.argv)

def close_window(window):
    window.destroy()

class tic_tac_toe_board(tk.Frame):
    def __init__(self,root,height, width):
        global buttons
        global button_nr
        tk.Frame.__init__(self,root)
        for i in range(3):
            tk.Grid.columnconfigure(self,i,weight = 1)
            tk.Grid.rowconfigure(self,i,weight = 1)
            for j in range(3):
                button_nr += 1
                button = tk.Button(self, height = height, width = width, command = lambda x = button_nr: mark(x))
                button.grid(row = i, column = j, sticky = 'news')
                buttons.append(button)  

class ultimate_tic_tac_toe_board(tk.Frame):
    global buttons
    global boards
    global button_nr
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        for i in range(3):
            tk.Grid.columnconfigure(self,i,weight = 1)
            tk.Grid.rowconfigure(self,i,weight = 1)
            for j in range(3):
                board = tic_tac_toe_board(root, height = 1, width = 1)
                board.grid(row = i, column = j, sticky = 'news',padx = 10, pady =10)
                boards.append(board)  

class Controls(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.button_new = tk.Button(self,text = 'New game', height = 5, width = 20,command = lambda: restart_program())
        self.button_new.pack()
        self.button_close = tk.Button(self,text = 'Close', height = 5, width = 20,command = lambda: close_window(window))
        self.button_close.pack()

class StartScreen(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.button_ttt = tk.Button(self,text = 'Tic Tic Toe', height = 5, width = 20,command = lambda: start_ttt())
        self.button_ttt.pack()
        self.button_uttt = tk.Button(self,text = 'Ultimate Tic Tac Toe', height = 5, width = 20,command = lambda: start_uttt())
        self.button_uttt.pack()

def start_ttt():
    new_window = tk.Toplevel()
    global button_nr
    button_nr = -1
    new_ttt_board(new_window)
    board, player_marker, opponent_marker, turn = ttt.create_board()

    while ttt.reward_of_state(board,player_marker) == 0 and ttt.possible_actions(board):
        if turn == 1:
            while clicked_button.get() not in ttt.possible_actions(board):
                buttons[0].wait_variable(clicked_button)
            board = ttt.do_action(board, clicked_button.get(), player_marker)
            mark(clicked_button.get())

        if turn == -1:  
            ai_action = mcts.monte_carlo_tree_search(board,opponent_marker,ttt.reward_of_state,ttt.possible_actions,ttt.do_action,ttt.do_action_copied, max_time = 1, ultimate = False, last_action=None)
            board = ttt.do_action(board, ai_action, opponent_marker)
            ai_mark(ai_action)
        
        turn *= -1

    result = ttt.reward_of_state(board,player_marker)
    if result == 1:
        print('You won')
    elif result == -1:
        print('You lost')
    else:
        print('Draw')
    tk.mainloop()

def uttt_button_to_action(value):
    board = int(value/9)
    button = value%9
    return (board,button)

def start_uttt():
    global button_nr
    button_nr = -1
    new_window = tk.Toplevel()

    last_action = None
    new_uttt_board(new_window)
    board, player_marker, opponent_marker, turn = uttt.create_board()

    while uttt.reward_of_state(board,player_marker) == 0 and uttt.possible_actions(board,None):
        if turn == 1:
            buttons[0].wait_variable(clicked_button)
            action = clicked_button.get()
            action_tuple = uttt_button_to_action(action)
            board = uttt.do_action(board, action_tuple, player_marker)
            mark(action)
            last_action = action_tuple

        if turn == -1:  
            ai_action = mcts.monte_carlo_tree_search(board,opponent_marker,uttt.reward_of_state,uttt.possible_actions,uttt.do_action,uttt.do_action_copied, max_time = 5,ultimate = True, last_action=last_action)
            board = uttt.do_action(board, ai_action, opponent_marker)
            ai_mark_uttt(ai_action)
            last_action = ai_action
        
        turn *= -1

    result = ttt.reward_of_state(board,player_marker)
    if result == 1:
        print('You won')
    elif result == -1:
        print('You lost')
    else:
        print('Draw')
    tk.mainloop()

def new_ttt_board(window):
    global buttons
    global clicked_button
    global screen
    global controls
    buttons = []
    clicked_button = tk.IntVar()
    clicked_button.set('1000000')
    
    tk.Grid.rowconfigure(window,0,weight = 1)
    tk.Grid.columnconfigure(window,0,weight = 1)
    screen = tic_tac_toe_board(window, height = 5, width = 5)
    controls = Controls(window)
    controls.grid(row = 1, column = 0, columnspan = 3,sticky = 'news')
    screen.grid(row = 0, column =0,  sticky = 'news')
    window.columnconfigure(0, weight = 1)
    window.columnconfigure(1,weight = 1)

def new_uttt_board(window):
    global buttons
    global clicked_button
    global screen
    global controls
    global boards
    buttons = []
    boards = list()
    clicked_button = tk.IntVar()
    clicked_button.set('1000000')
    
    tk.Grid.rowconfigure(window,0,weight = 1)
    tk.Grid.columnconfigure(window,0,weight = 1)
    screen = ultimate_tic_tac_toe_board(window)
    controls = Controls(window)
    controls.grid(row = 10, column = 0, columnspan = 3,sticky = 'news')
    screen.grid(row = 0, column =0,  sticky = 'news')
    window.columnconfigure(0, weight = 1)
    window.columnconfigure(1,weight = 1)


def new_game():
    global board, player_marker, opponent_marker, turn
    board, player_marker, opponent_marker, turn = ttt.create_board()
    

global button_nr
global buttons
global clicked_button
window = tk.Tk()
start = StartScreen(window)
start.pack()
tk.mainloop()




