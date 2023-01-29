from manim import *

class Positioning(Scene):
    def construct(self):
        #8 units en height; 14+2/9 units en width 
        plane= NumberPlane()
        self.add(plane)

        #next_to

        red_dot= Dot(color=RED)
        green_dot= Dot(color=GREEN)
        green_dot.next_to(red_dot,UP*3+RIGHT*3)

        self.add(red_dot,green_dot)

        #Shift (pren com a referència la posició actual)
        sq= Square(color=ORANGE)
        sq.shift(2*UP+RIGHT*4)
        self.add(sq)

        #move_to (pren com a referència l'origin, i el canvia)
        c=Circle(color=PURPLE)
        c.move_to([-3,-2,-0])
        self.add(c)


        #align_to
        c2= Circle(radius=0.5,color=RED,fill_opacity=0.5)
        c3= c2.copy().set_color(YELLOW)
        c4= c2.copy().set_color(ORANGE)

        c2.align_to(sq,UP)
        c3.align_to(sq,RIGHT)
        c4.align_to(sq,UP+RIGHT)
        self.add(c2,c3,c4)

class CriticalPoints(Scene):
    def construct(self):
        c=Circle(color=GREEN,fill_opacity=0.5)
        creu=Cross(scale_factor=0.2)
        self.add(c)

        #Si dibuixem un quadrat al cercle, veurem que les Cross estan ubicades a totes les directions del quadrat!
        for directions in [ORIGIN,UP,UR,RIGHT,DR,DOWN,DL,LEFT,UL]:
            self.add(Cross(scale_factor=0.2).move_to(c.get_critical_point(directions)))

        #En aquest cas, només hi hauria una creu que l'estariem movent!
        for directions in [ORIGIN,UP,UR,RIGHT,DR,DOWN,DL,LEFT,UL]:
            self.add(creu.move_to(c.get_critical_point(directions)))
             
        sq=Square()
        sq.move_to([1,0,0],aligned_edge=LEFT)
        self.add(sq)

from manim.utils.unit import Percent, Pixels

class UsefulUnits(Scene):
    def construct(self):
        for perc in range(5,51,5):
            #Tenir en comte que X_AXIS i Y_AXIS no tenen ben bé el mateix tamany, per tant
            #depenen de la referència el dibuix serà diferent!
            self.add(Circle(radius=perc*Percent(Y_AXIS)))
            self.add(Square(side_length=2*perc*Percent(Y_AXIS),color=ORANGE))
        #Els pixels depenen de quality settings    
        d=Dot()
        d.shift(100*Pixels*RIGHT)
        self.add(d)

class MobjectsGrups(Scene):
    def construct(self):
        red_dot=Dot(color=RED)
        green_dot=Dot(color=GREEN).next_to(red_dot,RIGHT)
        blue_dot=Dot(color=BLUE).next_to(red_dot,UP)

        dot_grup= VGroup(red_dot,green_dot,blue_dot)
        dot_grup.to_edge(RIGHT)

        self.add(dot_grup)

        #L'estrella serveix per escriureles sense llista, sinó una després una altra
        circles=VGroup(*[Circle(radius=0.2) for i in range(20)])
        circles.arrange(UP,buff=0.5)
        self.add(circles)

        stars= VGroup(*[Star(color=YELLOW,fill_opacity=1).scale(0.5) for i in range(20)])
        stars.arrange_in_grid(4,5,buff=0.5)




