from math import sqrt
import random

class Segment:

    def __init__(self, x1, y1, x2, y2):
        self.A = (x1, y1)
        self.B = (x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cartesian = self.cartesianEq()
    
    def inBetween(self, S):
        x, y = S
        a, b, c = self.cartesian
        if self.aligned(x, y):
            if abs(x-self.x1) + abs(self.x2 - x) == abs(self.x2-self.x1) and abs(y - self.y1) + abs(self.y2 - y) == abs(self.y2-self.y1):
                return True
        return False
    
    def aligned(self, x, y):
        a, b, c = self.cartesian
        return abs(a*x + b*y + c) <= 0.00001
    
    def cartesianEq(self):
        b, a = -(self.x2-self.x1), self.y2-self.y1
        c = -b*self.y1 -a*self.x1
        return a, b, c
    
    def same_slope(self, seg2):

        a2, b2, c2 = seg2.cartesian
        a, b, c = self.cartesian

        if a == 0:
            return a2 == 0
        if a2 == 0:
            return a == 0
        if b == 0:
            return b2 == 0
        if b2 == 0:
            return b == 0
        return b/a == b2/a2
    
    def intersection(self, segment2):
        a2, b2, c2 = segment2.cartesian
        a, b, c = self.cartesian
        if self.same_slope(segment2):
            return None
        # cas ou la premiere droite est parallelle a l'axe des absisses
        if a == 0:
            y = -c/b
            x = c - c2 + ((c*b2)-(c*b))/(b)
        else:
            k = a2/a
            b3, c3 = k*b, k*c
            y = (c2-c3)/(b3-b2)
            x = (-c - b*y)/a

        return x, y
    
    def __repr__(self):
        return "\npoint 1 (" + str(self.x1) + ", " + str(self.y1) + ")" + " point 2 (" + str(self.x2) + ", " + str(self.y2) + ")"


class Entity:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    
    def lineInRectangle(self, seg):
        seg1 = Segment(self.x, self.y            , self.x + self.width, self.y)
        seg2 = Segment(self.x+ self.width        , self.y            , self.x + self.width, self.y+self.height)
        seg3 = Segment(self.x, self.y            , self.x            , self.y + self.height)
        seg4 = Segment(self.x                    , self.y+self.height, self.x + self.width, self.y+self.height)
        a = (seg1.intersection(seg))
        b = (seg2.intersection(seg))
        c = (seg3.intersection(seg))
        d = (seg4.intersection(seg))
        if a != None:
            a = seg1.inBetween(a)
        else:
            a = False
        if b != None:
            b = seg2.inBetween(b)
        else:
            b = False
        if c != None:
            c = seg3.inBetween(c)
        else:
            c = False
        if d != None:
            d = seg4.inBetween(d)
        else:
            d = False
        return a or b or c or d


    def check_collision(self, e):
        """ check if this entity collide with another entity """
        return (
            self.in_rect(e.x, e.y) or
            self.in_rect(e.x + e.width, e.y) or
            self.in_rect(e.x + e.width, e.y + e.height) or
            self.in_rect(e.x, e.y + e.height)
        )
    def get_position(self):
        return self.x, self.y
        
    def in_rect(self, x, y):
        """ check if (x,y) is in this entity """

        return x >= self.x and x <= self.x + self.width and y >= self.y and y <=  self.y + self.height
    
    def move(self, dx, dy):
        """ move the entity """
        self.x += dx
        self.y += dy
    
    def get_center(self):
        return self.x + self.width/2, self.y + self.height/2
    
    def limit(self, w, h):
        self.x = max(0, self.x)
        self.y = max(0, self.y)
        self.x = min(w - self.width, self.x)
        self.y = min(h - self.height, self.y)
    
    def clip(self, a, b, w, h):

        self.x = max(a, self.x)
        self.y = max(b, self.y)
        self.x = min(w - self.width, self.x)
        self.y = min(h - self.height, self.y)

    def get_distance(self, e):
        return sqrt((e.y - self.y)**2 + (e.x - self.x)**2)
    
    def to_rect(self):
        return [self.x, self.y, self.width, self.height]
    
    def move_speed(self, dx, dy, speed):

        vx = 1/sqrt(2) * speed
        vy = 1/sqrt(2) * speed

        self.x += vx * dx
        self.y += vy * dy


