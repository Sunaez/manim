from pathlib import Path
import subprocess
import sys

from manim import *

from palette import apply_palette

RENDER_QUALITY = "medium"
# low: preview quality
# medium: standard render quality
# high: final render quality
COLOR_SCHEME = "Dark"

P = apply_palette(COLOR_SCHEME)
BACKGROUND = P.BG_0
SURFACE = P.BG_1
SURFACE_ALT = P.BG_2
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY
FAINT = P.TEXT_FAINT
BORDER = P.BORDER
AXIS = P.AXIS
GRID = P.GRID
CURVE = P.BLUE
TANGENT = P.GREEN
SECANT = P.AMBER
POINT = P.YELLOW
X_COLOR = P.CYAN
XH_COLOR = P.AMBER
H_COLOR = P.YELLOW
FX_COLOR = P.TEAL
FPH_COLOR = P.PINK
DERIVATIVE = P.GREEN


class FirstPrinciplesGradient(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        self.camera.frame.save_state()

        self.x_value = 1.35
        self.h_tracker = ValueTracker(0.95)

        self.setup_graph()
        self.scene_1_intro_curve()
        self.scene_2_secant_triangle()
        self.scene_3_label_what_we_know()
        self.scene_4_substitute_gradient_formula()
        self.scene_5_apply_x_squared()
        self.scene_6_let_h_approach_zero()
        self.scene_7_apply_at_x_equals_two()
        self.scene_8_final_summary()
        self.wait(1.0)

    def setup_graph(self):
        self.axes = Axes(
            x_range=[0, 4.4, 1],
            y_range=[0, 10, 2],
            x_length=6.8,
            y_length=5.2,
            tips=False,
            axis_config={"color": AXIS, "stroke_width": 3, "include_numbers": True, "font_size": 26},
            x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
            y_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        )
        self.axes.shift(LEFT * 1.15 + DOWN * 0.4)

        self.axis_labels = self.axes.get_axis_labels(
            MathTex("x", font_size=32, color=X_COLOR),
            MathTex("y", font_size=32, color=FX_COLOR),
        )
        self.graph = self.axes.plot(lambda x: x**2, x_range=[0, 3.2], color=CURVE, stroke_width=5)

        self.curve_label = MathTex("y", "=", "x^2", font_size=34, color=TEXT)
        self.curve_label[2].set_color(CURVE)
        self.curve_label.move_to(self.axes.c2p(2.65, 8.5) + RIGHT * 0.9 + UP * 0.15)

        self.graph_base = VGroup(self.axes, self.axis_labels, self.graph, self.curve_label)
        self.graph_base.save_state()

    def scene_1_intro_curve(self):
        self.title = Text(
            "Differentiation from First Principles",
            font_size=36,
            color=TEXT,
            weight=BOLD,
        )
        self.title.to_edge(UP, buff=0.28)

        self.title_line = Line(LEFT * 5.7, RIGHT * 5.7, color=CURVE, stroke_width=3)
        self.title_line.next_to(self.title, DOWN, buff=0.18)

        self.point_at_two = Dot(self.axes.c2p(2, 4), radius=0.085, color=POINT)
        self.point_label = self.bubble_math(r"(2,4)", self.axes.c2p(2, 4), UR, font_size=28)
        self.tangent_line = self.make_tangent_line(2, span=1.0, color=TANGENT)
        self.derivative_note = self.caption_box(
            "Derivative = gradient of the tangent at a point",
            TANGENT,
            width=7.0,
        )
        self.derivative_note.to_edge(DOWN, buff=0.32)

        self.play(FadeIn(self.title, shift=UP * 0.08), Create(self.title_line), run_time=0.9)
        self.play(Create(self.axes), FadeIn(self.axis_labels), run_time=1.0)
        self.play(Create(self.graph), FadeIn(self.curve_label, shift=UP * 0.05), run_time=1.0)
        self.play(FadeIn(self.point_at_two, scale=0.7), FadeIn(self.point_label, shift=UP * 0.05), run_time=0.7)
        self.play(Create(self.tangent_line), run_time=0.75)
        self.play(FadeIn(self.derivative_note, shift=UP * 0.05), run_time=0.6)
        self.play(
            Indicate(self.tangent_line, color=TANGENT, scale_factor=1.02),
            Indicate(self.point_at_two, color=POINT, scale_factor=1.2),
            run_time=0.8,
        )
        self.wait(0.8)

        self.play(
            FadeOut(self.point_label, shift=UP * 0.04),
            FadeOut(self.derivative_note, shift=DOWN * 0.04),
            FadeOut(self.title, shift=UP * 0.04),
            FadeOut(self.title_line, shift=UP * 0.04),
            FadeOut(self.point_at_two),
            run_time=0.65,
        )

    def scene_2_secant_triangle(self):
        self.point_a = always_redraw(
            lambda: Dot(self.axes.c2p(self.x_value, self.f(self.x_value)), radius=0.075, color=X_COLOR)
        )
        self.point_b = always_redraw(
            lambda: Dot(
                self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value + self.h_tracker.get_value())),
                radius=0.075,
                color=FPH_COLOR,
            )
        )
        self.point_c = always_redraw(
            lambda: Dot(
                self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
                radius=0.07,
                color=H_COLOR,
            )
        )

        self.secant_line = always_redraw(
            lambda: self.make_secant_line(self.x_value, self.h_tracker.get_value(), span=1.0, color=SECANT)
        )
        self.horizontal_side = always_redraw(
            lambda: Line(
                self.axes.c2p(self.x_value, self.f(self.x_value)),
                self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
                color=H_COLOR,
                stroke_width=5,
            )
        )
        self.vertical_side = always_redraw(
            lambda: Line(
                self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
                self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value + self.h_tracker.get_value())),
                color=FPH_COLOR,
                stroke_width=5,
            )
        )

        self.add(self.point_a, self.point_b, self.point_c, self.horizontal_side, self.vertical_side)
        self.play(
            ReplacementTransform(
                self.tangent_line,
                self.make_secant_line(self.x_value, self.h_tracker.get_value(), span=1.0, color=SECANT),
            ),
            FadeIn(self.point_a, scale=0.7),
            FadeIn(self.point_b, scale=0.7),
            FadeIn(self.point_c, scale=0.7),
            run_time=0.9,
        )
        self.remove(self.tangent_line)
        self.add(self.secant_line)

        self.point_a_label, self.point_a_tex = self.coordinate_label(
            "x",
            "f(x)",
            self.axes.c2p(self.x_value, self.f(self.x_value)),
            LEFT + DOWN,
        )
        self.point_b_label, self.point_b_tex = self.coordinate_label(
            "x+h",
            "f(x+h)",
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value + self.h_tracker.get_value())),
            UP + RIGHT,
        )
        self.point_c_label, self.point_c_tex = self.coordinate_label(
            "x+h",
            "f(x)",
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
            DOWN + RIGHT,
        )

        self.h_brace = BraceBetweenPoints(
            self.axes.c2p(self.x_value, self.f(self.x_value)),
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
            direction=DOWN,
            color=H_COLOR,
        )
        self.h_brace_label = MathTex("h", font_size=28, color=H_COLOR)
        self.h_brace_label.next_to(self.h_brace, DOWN, buff=0.1)

        self.vertical_brace = BraceBetweenPoints(
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value + self.h_tracker.get_value())),
            direction=RIGHT,
            color=FPH_COLOR,
        )
        self.vertical_brace_label = self.colored_math(
            r"f(x+h)-f(x)",
            font_size=26,
        )
        self.vertical_brace_label.next_to(self.vertical_brace, RIGHT, buff=0.12)

        horizontal_snapshot = Line(
            self.axes.c2p(self.x_value, self.f(self.x_value)),
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
        )
        vertical_snapshot = Line(
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value)),
            self.axes.c2p(self.x_value + self.h_tracker.get_value(), self.f(self.x_value + self.h_tracker.get_value())),
        )
        self.right_angle = RightAngle(horizontal_snapshot, vertical_snapshot, length=0.14, color=FAINT)

        self.annotation_group = VGroup(
            self.point_a_label,
            self.point_b_label,
            self.point_c_label,
            self.h_brace,
            self.h_brace_label,
            self.vertical_brace,
            self.vertical_brace_label,
            self.right_angle,
        )

        self.play(
            FadeIn(self.point_a_label, shift=LEFT * 0.05),
            FadeIn(self.point_b_label, shift=UP * 0.05),
            FadeIn(self.point_c_label, shift=DOWN * 0.05),
            run_time=0.8,
        )
        self.play(
            GrowFromCenter(self.h_brace),
            FadeIn(self.h_brace_label, shift=DOWN * 0.04),
            GrowFromCenter(self.vertical_brace),
            FadeIn(self.vertical_brace_label, shift=RIGHT * 0.04),
            FadeIn(self.right_angle),
            run_time=0.9,
        )

        focus_group = VGroup(
            self.point_a_label,
            self.point_b_label,
            self.point_c_label,
            self.h_brace,
            self.vertical_brace,
            self.h_brace_label,
            self.vertical_brace_label,
        )
        self.play(
            self.camera.frame.animate.set(width=7.0).move_to(focus_group.get_center() + RIGHT * 0.2 + UP * 0.2),
            run_time=1.2,
        )
        self.wait(0.7)

    def scene_3_label_what_we_know(self):
        self.formula_panel = RoundedRectangle(width=5.8, height=5.8, corner_radius=0.2, color=BORDER, stroke_width=2)
        self.formula_panel.set_fill(SURFACE, opacity=0.97)
        self.formula_panel.to_edge(RIGHT, buff=0.35).shift(DOWN * 0.15)

        self.left_layout = VGroup(self.graph_base, self.annotation_group)
        self.play(
            Restore(self.camera.frame),
            self.left_layout.animate.scale(1.05).move_to(LEFT * 3.2 + DOWN * 0.35),
            run_time=1.15,
        )

        self.general_formula = self.colored_math(
            r"m=\frac{y_2-y_1}{x_2-x_1}",
            font_size=38,
        )
        self.general_formula.move_to(self.formula_panel.get_top() + DOWN * 0.82)

        known_values = VGroup(
            self.colored_math(r"x_1=x", font_size=30),
            self.colored_math(r"x_2=x+h", font_size=30),
            self.colored_math(r"y_1=f(x)", font_size=30),
            self.colored_math(r"y_2=f(x+h)", font_size=30),
        )
        known_values.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        known_values.move_to(self.formula_panel.get_center() + DOWN * 0.55)
        known_values.align_to(self.formula_panel.get_left() + RIGHT * 0.48, LEFT)
        self.known_values = known_values

        self.play(FadeIn(self.formula_panel), FadeIn(self.general_formula, shift=UP * 0.05), run_time=0.8)

        highlights = [
            (known_values[0], self.point_a_tex.get_part_by_tex("x"), self.point_a, X_COLOR),
            (known_values[1], self.point_b_tex.get_part_by_tex("x+h"), self.point_b, XH_COLOR),
            (known_values[2], self.point_a_tex.get_part_by_tex("f(x)"), self.point_a, FX_COLOR),
            (known_values[3], self.point_b_tex.get_part_by_tex("f(x+h)"), self.point_b, FPH_COLOR),
        ]
        for line, label_part, point, color in highlights:
            self.play(FadeIn(line, shift=RIGHT * 0.05), run_time=0.35)
            self.play(
                Indicate(label_part, color=color, scale_factor=1.06),
                Indicate(point, color=color, scale_factor=1.2),
                run_time=0.45,
            )
        self.wait(0.6)

    def scene_4_substitute_gradient_formula(self):
        substituted = self.colored_math(
            r"m=\frac{f(x+h)-f(x)}{(x+h)-x}",
            font_size=36,
        )
        substituted.move_to(self.general_formula)
        simplified = self.colored_math(
            r"m=\frac{f(x+h)-f(x)}{h}",
            font_size=38,
        )
        simplified.move_to(self.general_formula)

        self.play(FadeOut(self.known_values, shift=DOWN * 0.05), run_time=0.45)
        self.play(TransformMatchingTex(self.general_formula, substituted), run_time=0.95)
        self.general_formula = substituted
        self.wait(0.3)
        self.play(TransformMatchingTex(self.general_formula, simplified), run_time=0.85)
        self.general_formula = simplified

        self.secant_note = self.caption_box("Gradient of the secant line", SECANT, width=4.6)
        self.secant_note.scale(0.9)
        self.secant_note.move_to(self.formula_panel.get_bottom() + UP * 0.55)
        self.play(FadeIn(self.secant_note, shift=UP * 0.04), run_time=0.45)
        self.play(Indicate(self.secant_line, color=SECANT, scale_factor=1.02), run_time=0.55)
        self.wait(0.6)

    def scene_5_apply_x_squared(self):
        self.play(FadeOut(self.secant_note, shift=DOWN * 0.04), run_time=0.35)

        self.fx_line = self.colored_math(r"f(x)=x^2", font_size=30)
        self.fxh_line = self.colored_math(r"f(x+h)=(x+h)^2", font_size=30)
        context = VGroup(self.fx_line, self.fxh_line).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        context.move_to(self.formula_panel.get_top() + DOWN * 1.0)
        context.align_to(self.formula_panel.get_left() + RIGHT * 0.42, LEFT)

        step_1 = self.colored_math(r"m=\frac{(x+h)^2-x^2}{h}", font_size=32)
        step_2 = self.colored_math(r"m=\frac{x^2+2xh+h^2-x^2}{h}", font_size=30)
        step_3 = self.colored_math(r"m=\frac{2xh+h^2}{h}", font_size=34)
        step_4 = self.colored_math(r"m=\frac{h(2x+h)}{h}", font_size=34)
        step_5 = self.colored_math(r"m=2x+h", font_size=38)

        for formula in [step_1, step_2, step_3, step_4, step_5]:
            formula.scale_to_fit_width(self.formula_panel.width - 0.7)
            formula.move_to(self.formula_panel.get_center() + DOWN * 0.55)

        self.play(FadeIn(self.fx_line, shift=RIGHT * 0.05), run_time=0.35)
        self.play(FadeIn(self.fxh_line, shift=RIGHT * 0.05), run_time=0.35)
        self.wait(0.2)

        self.play(TransformMatchingTex(self.general_formula, step_1), run_time=0.9)
        self.general_formula = step_1
        self.play(TransformMatchingTex(self.general_formula, step_2), run_time=0.9)
        self.general_formula = step_2
        self.play(TransformMatchingTex(self.general_formula, step_3), run_time=0.8)
        self.general_formula = step_3
        self.play(TransformMatchingTex(self.general_formula, step_4), run_time=0.8)
        self.general_formula = step_4
        self.play(TransformMatchingTex(self.general_formula, step_5), run_time=0.75)
        self.general_formula = step_5
        self.wait(0.7)

    def scene_6_let_h_approach_zero(self):
        self.play(FadeOut(self.annotation_group), run_time=0.4)

        limit_prefix = Text("as", font_size=24, color=MUTED, weight=BOLD)
        limit_symbol = self.colored_math(r"h\to 0", font_size=30)
        limit_note = VGroup(limit_prefix, limit_symbol).arrange(RIGHT, buff=0.14)
        limit_note.move_to(self.formula_panel.get_center() + UP * 1.45)

        limit_formula = self.colored_math(r"m=2x", font_size=38)
        limit_formula.move_to(self.general_formula)
        derivative_formula = self.colored_math(r"\frac{dy}{dx}=2x", font_size=38)
        derivative_formula.move_to(self.general_formula)

        self.play(FadeIn(limit_note, shift=UP * 0.05), run_time=0.45)
        self.play(self.h_tracker.animate.set_value(0.12), run_time=2.2, rate_func=smooth)

        self.generic_tangent = self.make_tangent_line(self.x_value, span=0.9, color=TANGENT)
        self.play(FadeIn(self.generic_tangent), run_time=0.45)
        self.play(TransformMatchingTex(self.general_formula, limit_formula), run_time=0.8)
        self.general_formula = limit_formula
        self.play(TransformMatchingTex(self.general_formula, derivative_formula), run_time=0.8)
        self.general_formula = derivative_formula
        self.wait(0.7)

        self.limit_note = limit_note

    def scene_7_apply_at_x_equals_two(self):
        generic_objects = VGroup(
            self.point_a,
            self.point_b,
            self.point_c,
            self.horizontal_side,
            self.vertical_side,
            self.secant_line,
            self.generic_tangent,
            self.formula_panel,
            self.fx_line,
            self.fxh_line,
            self.general_formula,
            self.limit_note,
        )
        self.play(
            FadeOut(generic_objects, shift=DOWN * 0.05),
            Restore(self.graph_base),
            run_time=0.95,
        )

        point = Dot(self.axes.c2p(2, 4), radius=0.085, color=POINT)
        point_label = self.bubble_math(r"(2,4)", self.axes.c2p(2, 4), UR, font_size=28)
        tangent = self.make_tangent_line(2, span=1.0, color=TANGENT)
        gradient_label = self.bubble_text("Gradient = 4", tangent.get_end() + LEFT * 0.7 + DOWN * 0.2, TANGENT, 22)

        calc_1 = self.colored_math(r"\frac{dy}{dx}=2x", font_size=36)
        calc_2 = self.colored_math(r"\frac{dy}{dx}=2(2)", font_size=36)
        calc_3 = self.colored_math(r"\frac{dy}{dx}=4", font_size=36)
        calc_anchor = RIGHT * 3.55 + UP * 1.35
        for mob in (calc_1, calc_2, calc_3):
            mob.move_to(calc_anchor)

        self.play(FadeIn(point, scale=0.7), FadeIn(point_label, shift=UP * 0.04), run_time=0.55)
        self.play(Create(tangent), run_time=0.7)
        self.play(FadeIn(calc_1, shift=UP * 0.05), run_time=0.45)
        self.play(TransformMatchingTex(calc_1, calc_2), run_time=0.65)
        calc_1 = calc_2
        self.play(TransformMatchingTex(calc_1, calc_3), run_time=0.65)
        calc_1 = calc_3
        self.play(FadeIn(gradient_label, shift=UP * 0.04), run_time=0.45)
        self.play(
            Indicate(point, color=POINT, scale_factor=1.2),
            Indicate(tangent, color=TANGENT, scale_factor=1.02),
            run_time=0.75,
        )
        self.wait(0.8)

        self.final_graph_group = VGroup(point, point_label, tangent, calc_1, gradient_label)

    def scene_8_final_summary(self):
        self.play(FadeOut(self.final_graph_group), FadeOut(self.graph_base), run_time=0.75)

        summary_box = RoundedRectangle(width=11.3, height=4.9, corner_radius=0.22, color=CURVE, stroke_width=2)
        summary_box.set_fill(SURFACE, opacity=0.97)

        title = Text("First principles summary", font_size=32, color=TEXT, weight=BOLD)
        title.move_to(summary_box.get_top() + DOWN * 0.45)

        steps = VGroup(
            Text("1. Choose two points on the curve", font_size=24, color=TEXT),
            Text("2. Find the gradient between them", font_size=24, color=TEXT),
            Text("3. Move the second point closer", font_size=24, color=TEXT),
            Text("4. Let h approach 0", font_size=24, color=TEXT),
            Text("5. The secant becomes a tangent", font_size=24, color=TEXT),
            Text("6. The gradient becomes the derivative", font_size=24, color=TEXT),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        steps.move_to(summary_box.get_center() + LEFT * 1.4 + DOWN * 0.05)

        final_prefix = Text("For y = x^2, the derivative is", font_size=26, color=MUTED)
        final_formula = self.colored_math(r"\frac{dy}{dx}=2x", font_size=34)
        final_line = VGroup(final_prefix, final_formula).arrange(RIGHT, buff=0.18)
        final_line.move_to(summary_box.get_bottom() + UP * 0.55)

        self.play(FadeIn(summary_box, shift=UP * 0.08), FadeIn(title, shift=UP * 0.05), run_time=0.85)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.04) for line in steps], lag_ratio=0.12), run_time=1.25)
        self.play(FadeIn(final_line, shift=UP * 0.05), run_time=0.6)
        self.wait(1.2)

    def f(self, x_value):
        return x_value**2

    def make_tangent_line(self, x_value, span=1.0, color=TANGENT):
        slope = 2 * x_value
        y_value = self.f(x_value)
        left_x = max(0, x_value - span)
        right_x = min(3.35, x_value + span)
        left_y = y_value + slope * (left_x - x_value)
        right_y = y_value + slope * (right_x - x_value)
        return Line(
            self.axes.c2p(left_x, left_y),
            self.axes.c2p(right_x, right_y),
            color=color,
            stroke_width=4,
        )

    def make_secant_line(self, x_value, h_value, span=1.0, color=SECANT):
        slope = (self.f(x_value + h_value) - self.f(x_value)) / h_value
        center_x = x_value + h_value / 2
        left_x = max(0, center_x - span)
        right_x = min(3.35, center_x + span)
        base_y = self.f(x_value)
        left_y = base_y + slope * (left_x - x_value)
        right_y = base_y + slope * (right_x - x_value)
        return Line(
            self.axes.c2p(left_x, left_y),
            self.axes.c2p(right_x, right_y),
            color=color,
            stroke_width=4,
        )

    def coordinate_label(self, x_text, y_text, point, direction, font_size=26):
        tex = MathTex("(", x_text, ",", y_text, ")", font_size=font_size, color=TEXT)
        tex[1].set_color(XH_COLOR if x_text == "x+h" else X_COLOR)
        tex[3].set_color(FPH_COLOR if y_text == "f(x+h)" else FX_COLOR)
        bg = BackgroundRectangle(tex, color=BACKGROUND, fill_opacity=0.92, buff=0.06)
        group = VGroup(bg, tex)
        group.next_to(point, direction, buff=0.14)
        return group, tex

    def bubble_math(self, tex_text, point, direction, font_size=28):
        tex = MathTex(tex_text, font_size=font_size, color=TEXT)
        bg = BackgroundRectangle(tex, color=BACKGROUND, fill_opacity=0.92, buff=0.08)
        group = VGroup(bg, tex)
        group.next_to(point, direction, buff=0.14)
        return group

    def bubble_text(self, text, point, color, font_size):
        label = Text(text, font_size=font_size, color=color, weight=BOLD)
        bg = BackgroundRectangle(label, color=BACKGROUND, fill_opacity=0.94, buff=0.08)
        group = VGroup(bg, label)
        group.move_to(point)
        return group

    def caption_box(self, text, color, width=5.0):
        box = RoundedRectangle(width=width, height=0.75, corner_radius=0.16, color=color, stroke_width=1.8)
        box.set_fill(SURFACE_ALT, opacity=0.98)
        label = Text(text, font_size=22, color=TEXT)
        label.move_to(box)
        return VGroup(box, label)

    def colored_math(self, tex_text, font_size=34):
        keys = [
            "f(x+h)",
            "f(x)",
            "x+h",
            r"\frac{dy}{dx}",
            "y_2",
            "y_1",
            "x_2",
            "x_1",
            "2x",
            "x",
            "h",
            "m",
            "y",
        ]
        mob = MathTex(
            tex_text,
            font_size=font_size,
            color=TEXT,
            substrings_to_isolate=keys,
        )
        color_map = {
            "f(x)": FX_COLOR,
            "f(x+h)": FPH_COLOR,
            "x+h": XH_COLOR,
            "x_1": X_COLOR,
            "x_2": XH_COLOR,
            "y_1": FX_COLOR,
            "y_2": FPH_COLOR,
            r"\frac{dy}{dx}": DERIVATIVE,
            "2x": DERIVATIVE,
            "h": H_COLOR,
            "x": X_COLOR,
            "m": DERIVATIVE,
            "y": FX_COLOR,
        }
        for key in sorted(color_map, key=len):
            mob.set_color_by_tex(key, color_map[key])
        return mob


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        "-p",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "FirstPrinciplesGradient",
    ]
    raise SystemExit(subprocess.call(command))


def quality_args(name):
    quality_map = {
        "low": ["-ql"],
        "medium": ["-qm"],
        "high": ["-qh"],
    }
    if name not in quality_map:
        raise ValueError(f"Unsupported RENDER_QUALITY: {name!r}")
    return quality_map[name]


if __name__ == "__main__":
    render_scene()
