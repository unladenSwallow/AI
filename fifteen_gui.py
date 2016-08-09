'''
Created on Jul 14, 2016

@author: Les
'''
import Tkinter
import time


class fifteen_gui:
    
    def __init__(self):
        self.top = Tkinter.Tk()
        
        
    def make_board(self, board):
        self.frame = Tkinter.Frame(self.top, width = 250, height = 250)
        self.canvas = Tkinter.Canvas(self.frame, bg="black",  width = 250, height = 250)
        left = 10
        right = 60
        gap = 2
        size = 50
        board_count = 0
        top_x = left
        bott_x = right 
        top_y = left
        bott_y = right
        for row in range(1,5):
            for col in range(1,5):
                self.canvas.create_rectangle(top_x, top_y, bott_x, bott_y, fill = "green")
                txt_x = (top_x + bott_x) / 2
                txt_y = (top_y + bott_y) / 2
                self.canvas.create_text(txt_x, txt_y, text = board[board_count])
                board_count += 1
                top_x = bott_x + gap
                bott_x = bott_x + size + gap
            top_y = bott_y + gap
            bott_y = bott_y + size + gap 
            top_x = left
            bott_x = right
        self.canvas.pack()
        self.frame.pack()
        
    def main_loop(self, path):
        while path.empty() == False:
            self.top.after(1000, self.make_board(path.pop().state))
        self.top.mainloop()   
        
            