# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time
class RunawayGame:
    def __init__(self, canvas, runner, chaser, follower, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.follower = follower
        self.catch_radius2 = catch_radius**2
        self.score = 0
        self.timeLeft=30
        
        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        
        self.follower.shape('turtle')
        self.follower.color('black')
        self.follower.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        
    def success(self):
        if  self.score >= 3:
            self.chaser.color('yellow')
            return True
        return False
    
    def catch(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    def is_catched(self):
        p = self.chaser.pos()
        q = self.follower.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def timer(self,timeLeft):
        return timeLeft-1
        
        
    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        self.follower.setpos((0,+init_dist / 2))
        

        
        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        


    def step(self):
        stime=time.time()
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        self.follower.run_ai(self.follower.pos(), self.follower.heading(), self.chaser)        
            # TODO) You can do something here and follows.
        if self.catch():
            self.score = self.score+1
            x=random.randint(-300,300)
            y=random.randint(-300,300)
            self.runner.setposition(x,y)
        if self.is_catched():
            self.timeLeft = 0
            self.chaser.color('black')
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        etime=time.time()
        self.timeLeft = self.timeLeft-(etime-stime)-0.1
        self.drawer.write(f'Time Left : {self.timeLeft:.1f}\n{self.score}/3')
        

            # Note) The following line should be the last of this function to keep the game playing
        if not self.success() and self.timeLeft>0 :
            self.canvas.ontimer(self.step, self.ai_timer_msec)
            

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=20):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 20)
        if mode in range(1,20):
            self.forward(self.step_move)
        elif mode == 0:
            self.left(self.step_turn)
        elif mode == 20:
            self.right(self.step_turn) 
        if ((self.xcor() > 350 or self.xcor() < -350) or (self.ycor() > 350 or self.ycor() < -350)):
            self.setheading(self.heading()+180)
            self.forward(20)
            
class FollowingMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading, manualMover):
        self.setheading(self.towards(manualMover.pos()))
        self.forward(random.randint(1, 10))

        
if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)
    follwer = FollowingMover(screen)
    game = RunawayGame(screen, runner, chaser, follwer)
    game.start()
    screen.mainloop()
