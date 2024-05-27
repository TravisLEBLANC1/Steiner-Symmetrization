import math

EPSILON = 0.000001
def print_perso_tmp(lst):
    for i in range(len(lst)):
        print(lst[i][0], lst[i][1])

def print_poly(poly):
    for v in poly.lst:
        print(v, end=" ")
    print()

class Vector():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({round(self.x, 1)}, {round(self.y, 1)})"

    def __eq__(self, value: object) -> bool:
        return abs(value.x - self.x) <= EPSILON and abs(value.y - self.y) <= EPSILON

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

    def add(self, v, coef=1):
        self.x += coef*v.x
        self.y += coef*v.y
        return self

    def sub(self, v, coef=1):
        self.x -= coef*v.x
        self.y -= coef*v.y
        return self

    def dist(v1, v2):
        return math.sqrt((v2.y - v1.y)**2 + (v2.x - v1.x)**2)

    def norm(self):
        return math.sqrt(self.y**2 + self.x**2)

    def prod_scalaire(v1, v2):
        return v1.x*v2.x + v1.y*v2.y

    def projection(self, proj):
        scalaire = self.prod_scalaire(proj)
        norme = proj.norm()
        self.x = proj.x*scalaire/norme
        self.y = proj.y*scalaire/norme
        return self

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
    
    if isBetween(x_inter, y_inter, p3, p4):
        # print(f"intersection ({x_inter}, {y_inter}) inside " + p3.__str__() + "  " + p4.__str__())
        return Vector(x_inter, y_inter)

    # print(f"intersection ({x_inter}, {y_inter}) outside " + p3.__str__() + "  " + p4.__str__())
    return None

class Polygon():
    def __init__(self, lst_points) -> None:
        self.lst = []
        for i in range (len(lst_points)):
            self.lst.append(Vector(lst_points[i][0], lst_points[i][1]))
    
    def __str__(self) -> str:
        return print_poly(self)

    def from_vectors(lst_vectors):
        p = Polygon([])
        p.lst = lst_vectors
        return p

    def add(self, vector:Vector):
        self.lst.append(vector)

    def insert(self, index, vector):
        self.lst.insert(index, vector)

    def __lower_x_point(self):
        if len(self.lst) == 0:
            raise ValueError("impossible to make a min of an empty list")
        index_min = 0
        for i in range(1, len(self.lst)):
            if self.lst[index_min].x > self.lst[i].x:
                index_min = i
        return self.lst[index_min]

    """ return True if p3 is on the left of the segment [p1, p2]"""
    def is_on_left(p1, p2, p3):
        return (p3.y - p1.y)*(p2.x - p1.x) - (p2.y - p1.y)*(p3.x - p1.x) < 0

    """ change the list of points to be the convexHull of the points"""
    def convexHull(self):
        convex = []
        pointHull = self.__lower_x_point()
        i = 0
        while True:
            convex.append(pointHull)
            endPoint = self.lst[0]
            for j in range(1, len(self.lst)):
                if (endPoint == pointHull) or (Polygon.is_on_left(self.lst[j], convex[i], endPoint)):
                    endPoint = self.lst[j]

            i = i+1
            pointHull = endPoint

            if endPoint == convex[0]:
                break
        
        self.lst = convex

    def get_points(self):
        lst = []
        for i in range(len(self.lst)):
            lst.append((self.lst[i].x, self.lst[i].y))
        return lst
    
    def get_perimeter(self):
        p = 0
        for i in range(len(self.lst)):
            p += self.lst[i].dist(self.lst[(i+1)%len(self.lst)])
        return p

    def get_area_convexe(self):
        if len(self.lst) == 0: return 0
        area = 0
        p0 = self.lst[0]

        for i in range(1, len(self.lst)-1):
            p1 = self.lst[i]
            p2 = self.lst[(i+1)]
            a = p0.dist(p1)
            b = p0.dist(p2)
            c = p1.dist(p2)
            s = (a+b+c)/2
            area += math.sqrt(abs(s*(s-a)*(s-b)*(s-c)))

        return area


"""
Store a Polygon and allow to symetrize it through a hyperplan (1-dimensionnal) with the symmetrization method

"""
class Steiner_Symetrisation():
    def __init__(self, lst_points, base_norme = 0.5) -> None:
        self.poly = Polygon(lst_points)
        self.base_norme = base_norme

        self.max_x = 50
        self.min_x = -50
        self.max_y = 50
        self.min_y = -50

    """ return the list of points of the curent polygon"""
    def get_points(self):
        return self.poly.get_points()

    def get_perimeter(self):
        return self.poly.get_perimeter()

    def get_volume(self):
        return self.poly.get_area_convexe()

    """ return true if the vectore is inside the plot (the initial max and min values)"""
    def __inside_plot(self, vector):
        return self.min_x <= vector.x <= self.max_x and self.min_y <= vector.y <= self.max_x

# approximate version
    """return the 1-dimensionnal volume of the section through u"""
    def __get_inside_volume(self, u):
        direct = u.copy().add(self.vector)
        lst_inter = []
        
        for i in range(len(self.poly.lst)):
            tmp = instersection(u, direct, self.poly.lst[i], self.poly.lst[(i+1)%len(self.poly.lst)])
            if tmp is not None:
                # print(f"intersection ", u,  direct, self.poly.lst[i], self.poly.lst[(i+1)%len(self.poly.lst)], " -> ",  tmp)
                lst_inter.append(tmp)
        if len(lst_inter) > 2:
            print("more than 2... ", len(lst_inter))
            return -1
        if(len(lst_inter) == 1):
            print("1 seul...")
        if len(lst_inter) < 2:
            return 0
        # if len(lst_inter) == 2
        return lst_inter[0].dist(lst_inter[1])

    """ add the end points above an under the vector, at volume/2 distance, and shift by u"""
    def __add_end_points(self, u:Vector, volume):
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
    def symmetrization_approximated(self, x, y):
        self.vector = Vector(x, y)
        self.vector.normalize()
        self.perp = self.vector.get_perp().normalize(self.base_norme)
        i = 0
        # positive part
        self.new_poly_pos = []
        self.new_poly_neg = []
        u = self.perp.copy()
        while self.__inside_plot(u):
            volume = self.__get_inside_volume(u)
            if volume > EPSILON:
                self.__add_end_points(u, volume)
            u.add(self.perp)

        self.new_poly_neg.reverse()
        self.new_poly_pos.extend(self.new_poly_neg)
        tmp = self.new_poly_pos # we store all the point found on the positive part


        # negative part
        self.new_poly_pos = []
        self.new_poly_neg = []
        
        u = self.perp.copy()
        u.sub(self.perp)
        while self.__inside_plot(u):
            volume = self.__get_inside_volume(u)
            if volume > EPSILON:
                self.__add_end_points(u, volume)
            u.sub(self.perp)

        tmp.extend(self.new_poly_neg)
        self.new_poly_pos.reverse()
        tmp.extend(self.new_poly_pos)  # we then add all the points found to one polygon

        self.poly = Polygon.from_vectors(tmp)
    
# correct version

    def get_intersection(self, index):
        direct = self.poly.lst[index].copy().add(self.vector)
        for i in range(len(self.poly.lst)):
            if i == index or (i+1)%len(self.poly.lst) == index: continue
            tmp = instersection(self.poly.lst[index], direct, self.poly.lst[i], self.poly.lst[(i+1)%len(self.poly.lst)])

            if tmp is None: continue
            return tmp, i+1
        return None, None

    def symmetrization_correct(self, x, y):
        self.new_poly = Polygon([]) 

        self.vector = Vector(x, y).normalize()
        self.perp = self.vector.get_perp()

        for i in range(len(self.poly.lst)):
            v = self.poly.lst[i]
            inter, index = self.get_intersection(i)
            projection = v.copy().projection(self.perp)
            if inter is None:
                self.new_poly.add(projection)
            else:
                dist = inter.dist(v)
                tmp_pos = projection.copy().add(self.vector, coef=dist/2)
                tmp_neg = projection.sub(self.vector, coef=dist/2)
                self.new_poly.add(tmp_neg)
                self.new_poly.add(tmp_pos)

        self.new_poly.convexHull()
        self.poly = self.new_poly
