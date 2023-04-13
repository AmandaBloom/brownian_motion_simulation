import random
import math

MOLE_RADIUS = 3
MOLE_MASS = 1
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

class Physics:
    def __init__(self, n: int, V_global: float) -> None:
        self.N = n
        self.Vg = V_global
        self.Moles = [Mole(self.Vg) for _ in range(n)]
        for i in range(len(self.Moles)):
            self.Moles[i].init_position()

        collide = self.get_collision_idx(self.Moles)
        while(len(collide) != 0):
            for j in range(len(collide)):
                self.Moles[j].init_position()
            collide = self.get_collision_idx(self.Moles)

    def get_collision_idx(self, mole_list) -> list[int]:
        collision = []
        for i in range(len(mole_list)):
            col = [j for j in range(len(mole_list)) if i != j and mole_list[i].x == mole_list[j].x and mole_list[i].y == mole_list[j].y]
            if col is not []:
                collision.extend(col)
        return collision

    def get_moles(self):
        return self.Moles

    def addMoles(self, n):
        new_moles = [Mole(self.Vg) for _ in range(n)]
        for i in range(len(new_moles)):
            new_moles[i].init_position()
        
        collide = self.get_collision_idx(new_moles)
        while(len(collide) != 0):
            for j in range(len(collide)):
                new_moles[j].init_position()
            collide = self.get_collision_idx(new_moles)
        self.Moles.extend(new_moles)
        self.N += n

    def delMoles(self, n):
        self.Moles = self.Moles[0:self.N-n]
        self.N -= n
        


    def setMoles(self, n: int) -> None:
        if n > self.N:
            self.addMoles(n-self.N)
        elif n < self.N:
            self.delMoles(self.N-n)


class Mole:
    def __init__(self, Vg: float) -> None:
        self.Vg = Vg
        self.x = None
        self.y = None
        self.r = MOLE_RADIUS
        self.mass = MOLE_MASS
        self.dx = None
        self.dy = None
        self.Vx = None
        self.Vy = None
    
    def init_position(self) -> None:
        self.x = random.randint(0+MOLE_RADIUS, SCREEN_WIDTH-MOLE_RADIUS)
        self.y = random.randint(0+MOLE_RADIUS, SCREEN_HEIGHT-MOLE_RADIUS)
        angle = random.uniform(0, 2*math.pi)
        self.Vx = self.Vg*math.sin(angle)
        self.Vy = self.Vg*math.cos(angle)
