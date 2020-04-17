import tkinter as tk
import random
import sys 
import os
import mcts_tic_tac_toe as ttt

def mark(button):
    global buttons
    if buttons[button]['text'] is '':
        buttons[button].configure(text = 'X')
        clicked_button.set(button)

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
    global buttons
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        button_nr = -1
        for i in range(3):
            tk.Grid.columnconfigure(self,i,weight = 1)
            tk.Grid.rowconfigure(self,i,weight = 1)
            for j in range(3):
                button_nr += 1
                button = tk.Button(self, height = 5, width = 5, command = lambda x = button_nr: mark(x))
                button.grid(row = i, column = j, sticky = 'news')
                buttons.append(button)  

class Controls(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.button_new = tk.Button(self,text = 'New game', height = 5, width = 20,command = lambda: restart_program())
        self.button_new.pack()
        self.button_close = tk.Button(self,text = 'Close', height = 5, width = 20,command = lambda: close_window(window))
        self.button_close.pack()

def new_board(window):
    global buttons
    global clicked_button
    global screen
    global controls
    buttons = []
    clicked_button = tk.IntVar()
    clicked_button.set('1000000')
    
    tk.Grid.rowconfigure(window,0,weight = 1)
    tk.Grid.columnconfigure(window,0,weight = 1)
    screen = tic_tac_toe_board(window)
    controls = Controls(window)
    controls.grid(row = 1, column = 0, columnspan = 3,sticky = 'news')
    screen.grid(row = 0, column =0,  sticky = 'news')
    window.columnconfigure(0, weight = 1)
    window.columnconfigure(1,weight = 1)


def new_game():
    global board, player_marker, opponent_marker, turn
    board, player_marker, opponent_marker, turn = ttt.create_board()
    

global buttons
global clicked_button
window = tk.Tk()
new_board(window)
board, player_marker, opponent_marker, turn = ttt.create_board()

while ttt.reward_of_state(board,player_marker) == 0 and ttt.possible_actions(board):
    if turn == 1:
        action = 10
        while clicked_button.get() not in ttt.possible_actions(board):
            buttons[0].wait_variable(clicked_button)
        board = ttt.do_action(board, clicked_button.get(), player_marker)
        mark(clicked_button.get())

    if turn == -1:  
        ai_action = ttt.monte_carlo_tree_search(board,opponent_marker)
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


