"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from spring.force import SpringBox

class SpringTestNoGraphics(TestCase):
    class Holder():
        def __init__(self, name):
            self.name = name

    @staticmethod
    def connect_all(ndict, objects, w):
        for i in xrange(len(objects)):
            for j in xrange(i+1, len(objects)):
                vn = objects[i].name
                un = objects[j].name
                
                if vn not in ndict:
                    ndict[vn] = dict()
                ndict[vn][un] = w

                if un not in ndict:
                    ndict[un] = dict()
                ndict[un][vn] = w


    @staticmethod
    def kfn(ndict, u, v):
        if u.name not in ndict or v.name not in ndict[u.name]:
            return None
        return ndict[u.name][v.name]

    @staticmethod
    def test_draw_sb(sb):
        pass

    def test_spring(self):
        #self.assertEqual(1 + 1, 2)
        AB = 'abcdefghijklmnopqrstuvwxyz'.upper()
        objects = []
        for c in AB:
            objects.append(self.Holder(c))

        ndict = dict()
        SpringTestNoGraphics.connect_all(ndict, objects[:10],   1)
        SpringTestNoGraphics.connect_all(ndict, objects[10:20], 2)
        SpringTestNoGraphics.connect_all(ndict, objects[20:],   3)
        
        sb = SpringBox(objects=objects, width=150, height=400, 
                       charge=1, mass=1, time_step=0.05, 
                       kfn=lambda x, y: SpringTestNoGraphics.kfn(ndict, x, y))

        sb.move_to_equillibrium(1000)
        SpringTestNoGraphics.test_draw_sb(sb)
        
        
