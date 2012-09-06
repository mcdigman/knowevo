'''
By Sasho

Implements a force based algorithm outlined here:
http://www.cs.brown.edu/~rt/gdhandbook/chapters/force-directed.pdf
'''
import math
from chartit import DataPool, Chart

Kc = 8.9875*10**9

class SpringBox:
    def __init__(self, objects, width, height, charge, mass, time_step, kfn):
        self.objects   = objects 
        self.width     = width
        self.height    = height
        self.charge    = charge
        self.mass      = mass
        self.time_step = time_step
        self.kfn       = kfn
        
        self.init_positions()


    def init_positions(self):
        '''
        sets the initial positions for the objects for the given width and height
        of the canvas
        sets the force, acceleration, velocity, distance, charge and mass fields
        '''
        
        A = self.width * self.height      #total area
        N = len(self.objects)             #number of squares
        S = A / N                         #square area
        R = S ** 0.5                      #object radius
        
        curr_x = 0
        curr_y = R
        for o in self.objects:
            o.pos    = [0.0, 0.0]
            o.force  = [0.0, 0.0]
            o.acc    = [0.0, 0.0]
            o.vel    = [0.0, 0.0]
            o.mass   = self.mass+0.0
            o.charge = self.charge+0.0

            o.pos[0] = curr_x + R
            o.pos[1] = curr_y
            
            curr_x += R                   #center square
            
            if curr_x + R > self.width:   #wrap to next line
                curr_x = 0
                curr_y += 2 * R
                
        
    def clear_forces(self):
        '''
        clears force vector for each object. needed to reset at each iteration
        '''
        for o in self.objects:
            o.force = [0.0, 0.0]
                

    def compute_repulsive_force(self):
        '''
        computes a repulsive force for all pairs with provided charge
        uses Coloumbic force to update the force vector
        '''
        for i in xrange(len(self.objects)):
            for j in xrange(i+1, len(self.objects)):
                
                v = self.objects[i]
                u = self.objects[j]
                
                dx = v.pos[0] - u.pos[0]
                if dx != 0:
                    sign        = dx / math.fabs(dx)
                    v.force[0] += sign * Kc * v.charge * u.charge / dx**2
                    u.force[0] += (-1) * sign * Kc * v.charge * u.charge / dx**2

                dy = v.pos[1] - u.pos[1]                
                if dy != 0:
                    sign        = dy / math.fabs(dy)
                    v.force[1] += sign * Kc * v.charge * u.charge / dy**2
                    u.force[1] += (-1) * sign * Kc * v.charge * u.charge / dy**2
                

    def compute_attractive_force(self):
        '''
        computes the spring force for all neighbors of each object
        using Hooke's Law: F = -k*d
        kfn returns the spring constant for a pair of objects.
        if the pair is not neighbors then kfn returns None
        '''
        for i in xrange(len(self.objects)):
            for j in xrange(i+1, len(self.objects)):
                
                v = self.objects[i]
                u = self.objects[j]
                
                k = self.kfn(v, u)
                if k == None:
                    continue
                
                dx = v.pos[0] - u.pos[0]
                if dx != 0:
                    v.force[0] += (-1) * dx * k
                    u.force[0] += dx * k
                
                dy = v.pos[1] - u.pos[1]
                if dy != 0:
                    v.force[1] += (-1) * dy * k
                    u.force[1] += dy * k
                
    def move(self):
        '''
        moves according ot acceleration for given time stamp
        keeps track of momentum
        
        S = Vo*t + 1/2*a*t^2
        V = Vo + a*t
        '''
        for o in self.objects:
            o.acc = map(lambda x: x / o.mass, o.force)
            o.pos = map(lambda x, y: 
                        x * self.time_step + y / 2 * self.time_step ** 2,
                        o.vel, o.acc)
            
            o.vel = map(lambda x, y: x + y * self.time_step, o.vel, o.acc)

    def scale_to_map(self):
        minx, miny = self.objects[0].pos
        maxx, maxy = self.objects[0].pos

        for o in self.objects:
            if o.pos[0] < minx:  minx = o.pos[0]
            if o.pos[0] > maxx:  maxx = o.pos[0]
            if o.pos[1] < miny:  miny = o.pos[1]
            if o.pos[1] > maxy:  maxy = o.pos[1]
            
        lenx = maxx-minx+1
        leny = maxy-miny+1
        
        scalex = self.width / lenx
        scaley = self.height / leny

        for o in self.objects:
            o.pos[0] = (o.pos[0]-minx) * scalex
            o.pos[1] = (o.pos[1]-miny) * scaley

            o.xpos, o.ypos = o.pos
            

    def move_to_equillibrium(self, R):
        '''
        sets forces and moves for a time_stamp R times. then assumes equillibirum
        has been reached
        '''
        for x in xrange(R):
            self.clear_forces()
            self.compute_repulsive_force()
            self.compute_attractive_force()
            self.move()

        self.scale_to_map()

        
    def print_objects(self):
        for o in self.objects:
            x, y = int(o.pos[0]), int(o.pos[1])
            print x,y,o.name
            
    @staticmethod
    def get_chart(models):
        objdata = DataPool(
            series = [
                {'options': { 'source': models },
                 'terms': ['xpos', 'ypos', 'name'] }])
        
        chart = Chart(
            datasource = objdata,
            series_options = [
                {'options': {
                        'type': 'scatter',

                        },
                 
                 'terms': {
                        'xpos': [
                            'ypos'],
                        },

                 }],

            chart_options = {
                'title': {
                    'text': 'Spring Box on links of depth 1 or less'
                    },
                'tooltip': {
                    'enabled':'true',
                    'useHTML':'true',
                    'pointFormat':'<b>dadwadawda</b>'
                    }
                })

        return chart
            

    @staticmethod
    def kfn(ndict, u, v):
        if u.name not in ndict or v.name not in ndict[u.name]:
            return None
        return ndict[u.name][v.name]

    @staticmethod
    def update_ndict(ndict, u, v, w):
        vn = v.name
        un = u.name
        if vn not in ndict:
            ndict[vn] = dict()
        ndict[vn][un] = w
            
        if un not in ndict:
            ndict[un] = dict()
        ndict[un][vn] = w

                
