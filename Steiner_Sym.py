import math

EPSILON = 0.000001

class Vector():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({round(self.x, 1)}, {round(self.y, 1)})"

    def copy(self):
        return Vector(self.x, self.y)

    """ return a perpendicular vector with same norme"""
    def get_perp(self):
        return Vector(self.y, -self.x)

    def get_norme(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self, norme=1):
        if norme == 0 : raise Exception("nul norm")
        tmp_norme = self.get_norme()
        self.x = self.x * norme/tmp_norme
        self.y = self.y * norme/tmp_norme
        return self

    def inverse(self):
        self.x = -self.x
        self.y = -self.y
        return self

    def add(self, v):
        self.x += v.x
        self.y += v.y
        return self

    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        return self

    def dist(v1, v2):
        return math.sqrt((v2.y - v1.y)**2 + (v2.x - v1.x)**2)

def isBetween(x, y, p3:Vector, p4:Vector):
    # get max and min x
    if p3.x <= p4.x:
        x_min = p3.x
        x_max = p4.x
    else:
        x_min = p4.x
        x_max = p3.x
    # get max and min y
    if p3.y <= p4.y:
        y_min = p3.y
        y_max = p4.y
    else:
        y_min = p4.y
        y_max = p3.y
    
    return x_min <= x <= x_max and y_min <= y <= y_max

""" 
return the intersection point between the staight line (p1 p2) and (p3 p4)
only if it is between the two points p3 and p4
"""
def instersection(p1:Vector, p2:Vector, p3:Vector, p4:Vector):
    a1 = (p1.y - p2.y)/(p1.x - p2.x)
    b1 = p2.y - a1*p2.x

    a2 = (p3.y - p4.y)/(p3.x - p4.x)
    b2 = p4.y - a2*p4.x

    if a1 == a2: return None

    x_inter = (b2 - b1)/(a1 - a2)
    y_inter = a1*x_inter + b1 
    # if y_inter  - a2*x_inter + b2 > 0.00001:
    #     print("oh no...")
    
    if isBetween(x_inter, y_inter, p3, p4):
        return Vector(x_inter, y_inter)

    # print(f"intersection ({x_inter}, {y_inter}) outside " + p3.__str__() + "  " + p4.__str__())
    return None

class Polygone():
    def __init__(self, lst_points) -> None:
        self.lst = []
        for i in range (len(lst_points)):
            self.lst.append(Vector(lst_points[i][0], lst_points[i][1]))
    
    def from_vectors(lst_vectors):
        p = Polygone([])
        p.lst = lst_vectors
        return p

    def add(self, vector:Vector):
        self.lst.append(vector)

    def get_points(self):
        lst = []
        for i in range(len(self.lst)):
            lst.append((self.lst[i].x, self.lst[i].y))
        return lst

class Steiner_Symetrisation():
    def __init__(self, lst_points, base_norme = 0.5) -> None:
        self.poly = Polygone(lst_points)
        self.base_norme = base_norme

        self.max_x = 50
        self.min_x = -50
        self.max_y = 50
        self.min_y = -50

    def get_points(self):
        return self.poly.get_points()

    def inside_plot(self, vector):
        return self.min_x <= vector.x <= self.max_x and self.min_y <= vector.y <= self.max_x

    def get_inside_volume(self, u):
        direct = u.copy().add(self.vector)
        lst_inter = []
        
        for i in range(len(self.poly.lst)):
            tmp = instersection(u, direct, self.poly.lst[i], self.poly.lst[(i+1)%len(self.poly.lst)])
            if tmp is not None:
                # print(f"intersection ", u,  direct, self.poly.lst[i], self.poly.lst[(i+1)%len(self.poly.lst)], " -> ",  tmp)
                lst_inter.append(tmp)
        if len(lst_inter) > 2:
            print("more than 2... ", len(lst_inter))
            return 20
        if(len(lst_inter) == 1):
            print("1 seul...")
        if len(lst_inter) < 2:
            return 0
        # if len(lst_inter) == 2
        return lst_inter[0].dist(lst_inter[1])

    def add_end_points(self, u:Vector, volume):
        # print("volume = ", volume)
        tmp1 = self.vector.copy()
        tmp1.normalize(volume/2)
        tmp1.add(u)
        self.new_poly_pos.append(tmp1)

        tmp2 = self.vector.copy()
        tmp2.normalize(volume/2)
        
        tmp2.inverse()
        tmp2.add(u)
        self.new_poly_neg.append(tmp2)

    """ apply a symmetrization througt the perpendicular of "vector" """
    def symmetrization(self, x, y):
        self.vector = Vector(x, y)
        self.vector.normalize()
        self.perp = self.vector.get_perp().normalize(self.base_norme)
        i = 0
        # positive part
        self.new_poly_pos = []
        self.new_poly_neg = []
        u = self.perp.copy()
        while self.inside_plot(u):
            volume = self.get_inside_volume(u)
            if volume > EPSILON:
                self.add_end_points(u, volume)
            u.add(self.perp)

        self.new_poly_neg.reverse()
        self.new_poly_pos.extend(self.new_poly_neg)
        tmp = self.new_poly_pos # we store all the point found on the positive part


        # negative part
        self.new_poly_pos = []
        self.new_poly_neg = []
        
        u = self.perp.copy()
        u.sub(self.perp)
        while self.inside_plot(u):
            volume = self.get_inside_volume(u)
            if volume > EPSILON:
                self.add_end_points(u, volume)
            u.sub(self.perp)

        tmp.extend(self.new_poly_neg)
        self.new_poly_pos.reverse()
        tmp.extend(self.new_poly_pos)

        self.poly = Polygone.from_vectors(tmp)
        

