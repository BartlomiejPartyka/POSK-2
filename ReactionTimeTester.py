from turtle import TurtleScreen, RawTurtle
from Timer import Timer
from random import randint
from math import floor
import asyncio

FONT_BIG = ('Arial', 20, 'bold')
FONT_SMALL = ('Arial', 16, 'normal')
CLICK_COLOR = '#1DDC1A'
DONTCLICK_COLOR = '#DC1A1A'


class ReactionTimeTester(TurtleScreen):

    def __init__(self, mode, canvas, cv_size, rounds):
        """

        :type mode: int
        :type canvas: Tkinter canvas obj
        """
        super().__init__(canvas)
        super().screensize(canvwidth=cv_size, canvheight=cv_size)
        self.MODE = mode
        self.times = []
        self.click = Click(canvas)
        self.dontclick = DontClick(canvas)
        if self.MODE == 1:
            self.dontclick.showturtle()
        self.SIZE = cv_size
        self.times = []
        self.HIT = False
        self.ROUNDS_NUMBER = int(rounds) + 1
        self.ROUNDS = self.ROUNDS_NUMBER
        self.CLICKED = False
        self.timer = Timer()
        self.results = []

    def new_round(self):
        border_l = -int(self.SIZE/2+20)
        border_h = int(self.SIZE/2-20)
        new_coors = (randint(border_l, border_h), randint(border_l, border_h))
        self.click.hideturtle()
        self.click.goto(new_coors)
        self.click.showturtle()
        if self.MODE == 1:
            new_coors = (randint(border_l, border_h), randint(border_l, border_h))
            self.dontclick.hideturtle()
            self.dontclick.goto(new_coors)
            self.dontclick.showturtle()

    def clicked(self, x, y):
        xcor = self.click.xcor()
        ycor = self.click.ycor()
        dx = abs(x-xcor)
        dy = abs(y-ycor)
        if dx <= 20 and dy <= 20:
            self.HIT = True

    async def player_click(self):
        self.timer.reset()
        self.listen()
        self.onscreenclick(self.clicked, 1)

    async def show_click(self):
        self.HIT = False
        self.new_round()
        await asyncio.sleep(2)

    async def play(self):
        for i in range(self.ROUNDS):
            await asyncio.gather(self.player_click(), self.show_click())
            self.timer.stop()
            formatted_time = floor(1000 * (self.timer.get_time() - 2))
            if self.HIT:
                self.times.append(formatted_time)
            else:
                self.times.append("Miss")
        self.create_results()
        self.click.hideturtle()
        if self.MODE == 1:
            self.dontclick.hideturtle()
        return self.get_results()

    def create_results(self):
        self.results = self.times
        t_sum = 0
        t_items = 0
        for t in self.times:
            if t != 'Miss':
                t_sum += t
                t_items += 1
        mean = round(t_sum / t_items, 2)
        accuracy = round(100 * t_items / (len(self.times) - 1), 2)
        self.results.append(mean)
        self.results.append(accuracy)

    def get_results(self):
        self.create_results()
        self.clear()
        return self.results


class Click(RawTurtle):

    def __init__(self, cv):
        super().__init__(cv)
        self.shape('circle')
        self.penup()
        self.fillcolor(CLICK_COLOR)


class DontClick(RawTurtle):

    def __init__(self, cv):
        super().__init__(cv)
        self.shape('circle')
        self.penup()
        self.fillcolor(DONTCLICK_COLOR)
        self.ht()

