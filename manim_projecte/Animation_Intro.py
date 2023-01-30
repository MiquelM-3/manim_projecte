from manim import *
from colour import Color

class BasicAnimations(Scene):
    def construct(self):
        polys=VGroup(*[RegularPolygon(5,radius=1,fill_opacity=0.5,
                color=Color(hue=i/5,saturation=1, luminance=0.5) ) for i in range(5)])
        polys.arrange(RIGHT)
        self.play(DrawBorderThenFill(polys),run_time=2)
        self.play(
            Rotate(polys[0],PI,rate_func= lambda t:t), #també: rate_func=linear
            Rotate(polys[1],PI,rate_func= smooth), #també: rate_func=linear
            Rotate(polys[2],PI,rate_func= lambda t:np.sin(t*PI)), #també: rate_func=linear
            Rotate(polys[3],PI,rate_func= there_and_back), #també: rate_func=linear
            Rotate(polys[4],PI,rate_func= lambda t: 1-abs(1-2*t)), #també: rate_func=linear
            run_time=2
        )
        self.wait()


