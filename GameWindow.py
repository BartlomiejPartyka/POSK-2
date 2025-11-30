import asyncio
from tkinter import *
import ReactionTimeTester as RTT

FONT_BIG = ('Arial', 20, 'bold')
FONT_SMALL = ('Arial', 16, 'normal')
SIZE = 600


class GameWindow(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        super().configure(bg='white')
        self.GAME_IS_ON = False
        self.MODE = IntVar()
        self.rounds = StringVar()
        self.configure(padx=30, pady=30, bg='white')
        self.play_area = Canvas(master, width=SIZE, height=SIZE)
        self.r1 = Radiobutton(master, text='Single color mode', variable=self.MODE, value=0, bg='white',
                              font=FONT_BIG)
        self.r2 = Radiobutton(master, text='Two-color mode', variable=self.MODE, value=1, bg='white', font=FONT_BIG)
        self.btn_start = Button(master, text='Start', bg='white', font=FONT_BIG, command=self.start)
        self.btn_stop = Button(master, text='Show menu', bg='white', font=FONT_BIG, command=self.show_btns)
        self.e = Entry(master, bg='white', font=FONT_SMALL, textvariable=self.rounds)
        self.show_btns()
        self.l1 = Label(master, text='Select mode, enter number of rounds\n(default - 5), and click "Start"\n\nNote: The program will start with an introductory round,\nwhich will not be counted in the statistics.\n\n',
                        bg='white', font=FONT_SMALL, width=50)
        self.label = Label(master, text='.', bg='white', font=FONT_SMALL, width=20)
        self.r1.select()
        self.results = []
        self.l1.grid(row=0, column=0)

    def start(self):
        self.play_area.grid(row=0, column=0)
        self.hide_btns()

    def stop(self):
        self.show_btns()

    def hide_btns(self):
        self.r1.grid_forget()
        self.r2.grid_forget()
        self.e.get()
        self.e.grid_forget()
        self.btn_start.grid_forget()
        self.btn_stop.grid(row=2, column=0)
        self.GAME_IS_ON = True
        self.start_game()

    def show_btns(self):
        self.btn_stop.grid_forget()
        self.r1.grid(row=1, column=0)
        self.r2.grid(row=2, column=0)
        self.e.grid(row=3, column=0)
        self.btn_start.grid(row=4, column=0)
        self.GAME_IS_ON = False

    def start_game(self):
        self.l1.grid_forget()
        if self.rounds.get() == '':
            rounds_var = 5
        else:
            rounds_var = self.rounds.get()
        rtt = RTT.ReactionTimeTester(self.MODE.get(), self.play_area, SIZE, rounds_var)
        self.results = asyncio.run(rtt.play())
        self.show_results()

    def show_results(self):
        text1 = ''
        lgt = len(self.results) - 2
        for ind in range(lgt):
            if ind == 0:
                pass
            elif ind == (lgt - 2):
                text1 += f'Mean        {self.results[ind]}ms\n'
            elif ind == (lgt - 1):
                text1 += f'Accuracy        {self.results[ind]}%\n'
            elif self.results[ind] != "Miss":
                text1 += f'{ind}.        {self.results[ind]}ms\n'
            else:
                text1 += f'{ind}.        {self.results[ind]}\n'
        self.l1.configure(text=text1, bg='white', font=FONT_SMALL, width=20)
        self.l1.grid(row=0, column=0)
        self.GAME_IS_ON = False
