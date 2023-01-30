from manim import *
from colour import Color

class BasicAnimations(Scene):
    def construct(self):
        polys=VGroup(*[RegularPolygon(5,radius=1,fill_opacity=0.5,
                color=Color(hue=i/5,saturation=1, luminance=0.5) ) for i in range(5)])
        polys.arrange(RIGHT)
        self.play(DrawBorderThenFill(polys),run_time=2)

        #Mirar a la guia de referencies per veure com funciona rate_func (n'hi ha moltes predeterminades)
        self.play(
            Rotate(polys[0],PI,rate_func= lambda t:t), #també: rate_func=linear
            Rotate(polys[1],PI,rate_func= smooth), 
            Rotate(polys[2],PI,rate_func= lambda t:np.sin(t*PI)),
            Rotate(polys[3],PI,rate_func= there_and_back), 
            Rotate(polys[4],PI,rate_func= lambda t: 1-abs(1-2*t)), 
            run_time=2
        )
        self.wait()

        
#Si hi ha conflicting animations, no donarà error! 
class ConflictingAnimations(Scene):
    def construct(self):
        s=Square()
        self.add(s)
        self.play(Rotate(s,PI),Rotate(s,-PI),run_time=3)
        #Veiem que en aquest cas fa la última primer

#Per fer overlapping d'animacions:
class OverlappingAnimations(Scene):
    def construct(self):
        squares= VGroup(*[Square(color=Color(hue=i/20,
            saturation=1, luminance=0.5, fill_opacity=0.5)) for i in range (20)])
        squares.arrange_in_grid(4,5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(k) for k in squares], lag_ratio=0.15))

#mobj.metodh() retorna normalment un mobj, i per tant no el podem posar a play()
#Per tant, haurem de fer servir .animate:
class AnimateEx(Scene):
    def construct(self):
        s=Square()
        self.play(s.animate.shift(RIGHT)) 
        self.play(s.animate(run_time=2).scale(3)) #Suports animation keywords
        self.play(s.animate.scale(1/2).shift(2*LEFT)) #Suports chaining

        #Note: .animate is not aware of how your mobjects change, knows only start & end and interpolates linearly between them
class AnimateEx2(Scene):
    def construct(self):
        s=Square(color=RED,fill_opacity=0.5)
        c=Circle(color=PURPLE,fill_opacity=0.5)
        self.add(s,c)
        self.play(s.animate.shift(UP), c.animate.shift(DOWN))
        self.play(VGroup(s,c).animate.arrange(RIGHT,buff=1))
        self.play(c.animate(rate_func=linear).shift(RIGHT).scale(2))

class AnimateEx3(Scene):
    def construct(self):
        s=Square(color=RED,fill_opacity=0.5)
        s2=Square(color=YELLOW,fill_opacity=0.5)
        VGroup(s,s2).arrange(RIGHT,buff=1)
        self.add(s,s2)
        self.play(s.animate.rotate(PI), Rotate(s2,PI))
        #Fixem-nos que en el primera animació, l'animate esta "interpolant" entre el final i el desti, i per tant el resultat és "extrany"

'''
MoveToTarget i Restore
Filosofia:  crear una còpia d'un mobject, modificar-lo, i després transformar-lo entre l'original i la còpia

MoveToTarget: call mob.generate_target(), després modificar mob.target -> animate amb MoveToTarget(mob)
Restore: call mob.save_state(), després modificar mob, i després animate return amb el saved state
'''
class AnimationMechanisms(Scene):
    def construct(self):
        s=Square(color=RED,fill_opacity=0.5)
        s2=Square(color=YELLOW,fill_opacity=0.5)

        s.generate_target()

        s.target.set_fill(color=GREEN,opacity=0.5)
        s.target.shift(2*RIGHT+UP).scale(0.5)

        self.add(s)
        self.wait()
        self.play(MoveToTarget(s))

        s2.save_state()
        self.play(FadeIn(s2))
        self.play(s2.animate.set_color(PURPLE).set_opcacity(0.5))
        self.play(s2.animate.shift(5*DOWN).rotate(PI/4))
        self.wait()
        self.play(Restore(s2),run_time=2)
'''
Animacions personalitzades a través de funcions
    L'objectiu és que una funció sigui un mapping de un (mobject,constant)->mobject2
    Per exemple:
    def move_somewhere(mobj,alpha):
        #mobj.move_to(alpha*RIGHT + alpha*2*UP)
    
    Podem utilitzar "UpdateFromAlphaFunc", que ens construeix l'animació

    consell: guardem l'estat inicial en un mobject atribute per més flexibilitat
        p.ex: mobj.initial_position=mobj.get_center()
                ... mobj.initial_position està en la animation function
        (o fer la teva pròpia animació)
''' 
class CustomAnimation(Scene):
    def construct(self):
        def spiral_out(mobject,t):
            radius=4*t
            angle= 2*t * 2*PI
            mobject.move_to(radius*(np.cos(angle)*RIGHT+ np.sin(angle)*UP))
            mobject.set_color(Color(hue=t,saturation=0.8,luminance=0.7))
            mobject.set_opacity(1-t)

        d=Dot(color=WHITE)
        self.add(d)
        self.play(UpdateFromAlphaFunc(d, spiral_out,run_time=3))

'''
Anatomia d'una animacio

Mètodes que es criden en l'animació
    -begin() -> preparar el primer frame;
                guarda còpies dels mobjects en self.starting_mobject
    -interpolate_mobject(alpha) ->
                porta el self.mobject a l'state de alpha% de l'animació
                default: delega a submobjects
    -interpolate_submobject(sub,sub_start,alpha)
                igual que a dalt, prò per un submobject específic (en l'argument)
    -finish() -> acaba l'animació i fa last_frame

    - clean_up_from_scene(scene) ->
                 all remaining mobject and scene cleanup (p.ex: removing mobjects)
'''

class DisperseA(Animation):

    def __init__(self,mobject,dot_radius=0.05,dot_number=100, **kwargs):
        super().__init__(mobject,**kwargs)
        self.dot_radius=dot_radius
        self.dot_number=dot_number
    
    def begin(self):
        dots = VGroup(
                *[Dot(radius=self.dot_radius).move_to(self.mobject.point_from_proportion(p)) for p in np.linspace(0, 1, self.dot_number)]
        )
        for dot in dots:
            dot.initial_position=dot.get_center()
            dot.shift_vector=(dot.get_center()-self.mobject.get_center())

        dots.set_opacity(0)
        self.mobject.add(dots)
        self.dots=dots
        super().begin()

    def clean_up_from_scene(self, scene: "Scene") -> None:
        super().clean_up_from_scene(scene)
        scene.remove(self.dots)

    def interpolate_mobject(self, alpha):
        alpha= self.rate_func(alpha)
        if alpha <=0.5:
            self.mobject.set_opacity(1-2*alpha,family=False)
            self.dots.set_opacity(2*alpha)
        else:
            self.mobject.set_opacity(0)
            self.dots.set_opacity(2*(1-alpha))
            for dot in self.dots:
                dot.move_to(dot.initial_position+ 2*(alpha - 0.5)*dot.shift_vector)

class CustomAnimationExample(Scene):
    def construct(self):
        st=Star(color=YELLOW,fill_opacity=1).scale(3)
        self.add(st)
        self.wait()
        self.play(DisperseA(st,dot_number=200))







