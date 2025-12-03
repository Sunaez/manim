from manim import *
import random

config.frame_rate = 30  # Ensure 30fps minimum


class ManimFeatureDemo(Scene):
    """
    Comprehensive demonstration of Manim Community Edition features.
    Showcases text, shapes, transformations, animations, and more.
    """

    def construct(self):
        # Scene 1: Title and Introduction
        self.intro_scene()
        self.wait(0.5)
        self.clear()

        # Scene 2: Text and Typography
        self.text_scene()
        self.wait(0.5)
        self.clear()

        # Scene 3: Shapes and Colors
        self.shapes_scene()
        self.wait(0.5)
        self.clear()

        # Scene 4: Transformations
        self.transformation_scene()
        self.wait(0.5)
        self.clear()

        # Scene 5: Mathematical Animations
        self.math_scene()
        self.wait(0.5)
        self.clear()

        # Scene 6: Graph and Functions
        self.graph_scene()
        self.wait(0.5)
        self.clear()

        # Scene 7: Finale
        self.finale_scene()
        self.wait(1)

    def intro_scene(self):
        """Opening title sequence"""
        title = Text("Manim Community Edition", font_size=56, gradient=(BLUE, GREEN))
        subtitle = Text("Feature Demonstration", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title, run_time=1.5))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)

        # Animated underline
        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            color=BLUE
        )
        self.play(Create(underline))
        self.wait(0.5)

        # Fade out everything
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(underline)
        )

    def text_scene(self):
        """Demonstrate text features"""
        header = Text("Text & Typography", font_size=48, color=ORANGE)
        header.to_edge(UP)
        self.play(Write(header))

        # Different text styles
        text_group = VGroup(
            Text("Regular Text", font_size=28),
            Text("Colored Text", font_size=28, color=RED),
            Text("Slanted Text", font_size=28, slant=ITALIC),
            Text("Gradient Text", font_size=28, gradient=(PURPLE, PINK))
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        text_group.move_to(ORIGIN)

        for text in text_group:
            self.play(FadeIn(text, shift=RIGHT), run_time=0.5)

        self.wait(1)
        self.play(FadeOut(header), FadeOut(text_group))

    def shapes_scene(self):
        """Demonstrate basic shapes"""
        header = Text("Shapes & Colors", font_size=48, color=GREEN)
        header.to_edge(UP)
        self.play(Write(header))

        # Create various shapes
        circle = Circle(radius=0.8, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=1.5, color=RED, fill_opacity=0.5)
        triangle = Triangle(color=YELLOW, fill_opacity=0.5)

        shapes = VGroup(circle, square, triangle).arrange(RIGHT, buff=1)
        shapes.move_to(ORIGIN)

        # Animate shapes appearing
        self.play(
            DrawBorderThenFill(circle),
            DrawBorderThenFill(square),
            DrawBorderThenFill(triangle),
            run_time=2
        )
        self.wait(0.5)

        # Rotate all shapes
        self.play(
            Rotate(circle, PI),
            Rotate(square, PI/2),
            Rotate(triangle, PI),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(FadeOut(header), FadeOut(shapes))

    def transformation_scene(self):
        """Demonstrate transformations and morphing"""
        header = Text("Transformations", font_size=48, color=PURPLE)
        header.to_edge(UP)
        self.play(Write(header))

        # Start with a circle
        shape = Circle(radius=1.5, color=BLUE, fill_opacity=0.7)
        self.play(Create(shape))
        self.wait(0.3)

        # Transform to square
        self.play(Transform(shape, Square(side_length=3, color=RED, fill_opacity=0.7)))
        self.wait(0.3)

        # Transform to triangle
        self.play(Transform(shape, Triangle(color=GREEN, fill_opacity=0.7).scale(2)))
        self.wait(0.3)

        # Transform to star
        star = Star(n=5, outer_radius=2, color=YELLOW, fill_opacity=0.7)
        self.play(Transform(shape, star))
        self.wait(0.5)

        # Scale animation
        self.play(shape.animate.scale(0.5), run_time=0.8)
        self.play(shape.animate.scale(2), run_time=0.8)

        self.play(FadeOut(header), FadeOut(shape))

    def math_scene(self):
        """Demonstrate mathematical text and equations"""
        header = Text("Mathematical Expressions", font_size=48, color=TEAL)
        header.to_edge(UP)
        self.play(Write(header))

        # Mathematical equations
        eq1 = MathTex(r"E = mc^2", font_size=60, color=YELLOW)
        eq1.move_to(UP * 1.5)

        eq2 = MathTex(r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}", font_size=50, color=GREEN)
        eq2.move_to(ORIGIN)

        eq3 = MathTex(r"e^{i\pi} + 1 = 0", font_size=60, color=BLUE)
        eq3.move_to(DOWN * 1.5)

        equations = VGroup(eq1, eq2, eq3)

        for eq in equations:
            self.play(Write(eq), run_time=1)
            self.wait(0.3)

        self.wait(0.5)
        self.play(FadeOut(header), FadeOut(equations))

    def graph_scene(self):
        """Demonstrate graphs and plotting"""
        header = Text("Graphs & Functions", font_size=48, color=MAROON)
        header.to_edge(UP)
        self.play(Write(header))

        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN)

        # Create functions
        sine_graph = axes.plot(lambda x: np.sin(2 * x), color=BLUE)
        cosine_graph = axes.plot(lambda x: np.cos(2 * x), color=RED)

        # Labels
        sine_label = MathTex(r"\sin(2x)", color=BLUE, font_size=36)
        sine_label.next_to(axes, RIGHT, buff=0.3).shift(UP * 0.5)

        cosine_label = MathTex(r"\cos(2x)", color=RED, font_size=36)
        cosine_label.next_to(sine_label, DOWN, buff=0.3)

        # Animate
        self.play(Create(axes))
        self.play(Create(sine_graph), Write(sine_label), run_time=1.5)
        self.wait(0.3)
        self.play(Create(cosine_graph), Write(cosine_label), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(header),
            FadeOut(axes),
            FadeOut(sine_graph),
            FadeOut(cosine_graph),
            FadeOut(sine_label),
            FadeOut(cosine_label)
        )

    def finale_scene(self):
        """Final scene with multiple elements"""
        # Create title
        title = Text("Manim CE", font_size=72, gradient=(BLUE, PURPLE))
        subtitle = Text("Create Beautiful Mathematical Animations", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Decorative elements
        circles = VGroup(*[
            Circle(radius=0.2, color=random_bright_color(), fill_opacity=0.6)
            for _ in range(20)
        ])

        for circle in circles:
            angle = random.uniform(0, TAU)
            radius = random.uniform(3, 4)
            circle.move_to([radius * np.cos(angle), radius * np.sin(angle), 0])

        # Animate
        self.play(
            LaggedStart(*[FadeIn(circle, scale=0.5) for circle in circles], lag_ratio=0.1),
            run_time=2
        )

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(0.5)

        # Rotate circles
        self.play(
            Rotate(circles, PI/2, about_point=ORIGIN),
            title.animate.set_color(GREEN),
            run_time=2
        )

        self.wait(0.5)

        # Final message
        thanks = Text("Thank you for watching!", font_size=40, color=WHITE)
        thanks.move_to(DOWN * 2)
        self.play(FadeIn(thanks, shift=UP))

        self.wait(1.5)
