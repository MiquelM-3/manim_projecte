from manim import *

class DefaultTemplate(Scene):
    def construct(self):
        #construcció de l'objecte. Veure a cadaobjecte les seves propietats
        box= Rectangle(stroke_color=ORANGE,stroke_opacity=0.7,
                        fill_color=RED_B,fill_opacity=0.5,
                        height=1,width=1)
        self.add(box)
        #objecte.animate serveix per començar l'animació
        self.play(box.animate.shift(RIGHT*2),run_time=2)
        self.play(box.animate.shift(UP*2),run_time=2)
        self.play(box.animate.shift(DOWN*5+LEFT*5),run_time=2)
        self.play(box.animate.shift(UP*1.5+RIGHT*1),run_time=2)

class DiferentsObjectes(Scene):
    def construct(self):
        #Primer num i segon num són les subdivions en x i y, positives i negatives; el tercer num es el "ratio"
        #En x_length i y_length: trivial
        
        #Fixem-nos que va bé per posar gràfiques de diferents tamanys en els dos eixos canviar els números amb les lengths iguals!


        axes= Axes(x_range=[-5,5,1],y_range=[-4,4,1],
        x_length=5,y_length=5)

        #to_edge indica que es posiciona a algun edge de la pantalla, buff la distancia entre l'edge i l'objecte
        axes.to_edge(LEFT,buff=5)

        triangle=Triangle(stroke_color=ORANGE,stroke_width=10,
                fill_color=GREY)

        #shift mou l'objecte en alguna direcció especificada
        triangle.set_height(2).shift(DOWN*3+RIGHT*3)

        circle=Circle(stroke_width=6,stroke_color=YELLOW,
                fill_color=RED_C, fill_opacity= 0.8)

        #Hi ha diferents posicions apart de left, right, up, bottom: UL,UR,DL,DR,CENTER,etc.
        circle.set_width(2).to_edge(DR,buff=0)

        #Dibuixa les axes i després el circle
        self.play(Write(axes))
        self.play(DrawBorderThenFill(circle))
        #Transforma el circle (en una animació) a una width de 1.
        self.play(circle.animate.set_width(1))
        #Transforma el circle en el triangle
        self.play(Transform(circle,triangle),run_time=1)
        #El "triangle" que està en pantalla encara és referit pel circle!
        self.play(FadeOut(circle))

class UpdatersExample(Scene):
    def construct(self):
        rectangle= RoundedRectangle(stroke_width=8,stroke_color=WHITE,
                fill_color=BLUE_B,width=4.5,height=2)
        rectangle.shift(UP*3+LEFT*4)

        textmates= MathTex("\\frac{3}{4}=0.75")
        textmates.set_color_by_gradient(GREEN,PINK).set_height(1.5)
        textmates.move_to(rectangle.get_center())
        
        textmates.add_updater(lambda x: x.move_to(rectangle.get_center()))

        self.play(FadeIn(rectangle))
        self.play(Write(textmates))

        self.play(rectangle.animate.shift(RIGHT*1.5+DOWN*5),run_time=6)
        self.wait()
        textmates.clear_updaters()
        self.play(rectangle.animate.shift(LEFT*2+UP*1),run_time=6)

        
