from pathlib import Path
import subprocess
import sys

from manim import *
from palette import apply_palette

RENDER_QUALITY = "medium"
# Choose one of: Dark, Light, Sepia.
# low: 480p preview render.
# medium: 720p default render.
# high: 1080p final render.

P = apply_palette("Dark")
BACKGROUND = P.BG_0
SURFACE = P.BG_1
SURFACE_ALT = P.BG_2
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY
BLUE = P.BLUE
TEAL = P.TEAL
GREEN = P.GREEN
AMBER = P.AMBER


class FloatingPointStory(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.introduction()
        self.clear()

        self.mantissa_exponent()
        self.clear()

        self.normalised_vs_unnormalised()
        self.clear()

        self.storage_concept()

    def section_title(self, text, color=BLUE_B):
        title = Text(text, font_size=34, color=color)
        title.to_edge(UP)
        line = Line(LEFT * 3, RIGHT * 3, color=color).next_to(title, DOWN, buff=0.15)
        return VGroup(title, line)

    def introduction(self):
        title = self.section_title("1. Introduction", BLUE_B)
        number = DecimalNumber(6.5, num_decimal_places=1, font_size=72, color=WHITE)
        note = Text("Computers store numbers using mantissa and exponent.", font_size=28, color=GREY_A)
        note.next_to(number, DOWN, buff=0.6)

        glow = Circle(radius=1.1, color=BLUE_E, fill_opacity=0.15, stroke_width=0)
        glow.move_to(number)

        self.play(FadeIn(title, shift=DOWN), FadeIn(glow), Write(number), run_time=1.8)
        self.play(Indicate(number, color=YELLOW), run_time=1.0)
        self.play(FadeIn(note, shift=UP), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, number, note, glow)), run_time=1.0)

    def mantissa_exponent(self):
        title = self.section_title("2. Mantissa and Exponent", TEAL_B)

        value = MathTex("6", ".", "5", font_size=72, color=WHITE)
        mantissa_label = Text("Mantissa = digits", font_size=28, color=GREEN_C)
        exponent_label = Text("Exponent = scale", font_size=28, color=ORANGE)

        mantissa_group = VGroup(value[0], value[2])
        mantissa_box = SurroundingRectangle(mantissa_group, color=GREEN_C, buff=0.18, corner_radius=0.1)
        exponent_box = SurroundingRectangle(value[1], color=ORANGE, buff=0.18, corner_radius=0.1)

        labels = VGroup(mantissa_label, exponent_label).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        labels.next_to(value, DOWN, buff=0.8)

        arrow1 = Arrow(mantissa_label.get_top(), mantissa_box.get_bottom(), buff=0.1, color=GREEN_C)
        arrow2 = Arrow(exponent_label.get_top(), exponent_box.get_bottom(), buff=0.1, color=ORANGE)

        self.play(FadeIn(title, shift=DOWN), Write(value), run_time=1.5)
        self.play(Create(mantissa_box), Create(exponent_box), run_time=1.0)
        self.play(FadeIn(labels, shift=UP), GrowArrow(arrow1), GrowArrow(arrow2), run_time=1.2)

        move_left = MathTex("65 \\times 10^{-1}", font_size=52, color=YELLOW)
        move_left.next_to(value, RIGHT, buff=1.2)
        left_arrow = Arrow(value.get_right(), move_left.get_left(), color=BLUE_B, buff=0.15)
        self.play(FadeIn(move_left, shift=RIGHT), GrowArrow(left_arrow), run_time=1.3)

        move_right = MathTex("6.5 \\times 10^{0}", font_size=52, color=YELLOW)
        move_right.next_to(move_left, DOWN, buff=0.5)
        right_arrow = Arrow(move_left.get_left(), move_right.get_left(), color=BLUE_B, buff=0.15)
        self.play(FadeIn(move_right, shift=RIGHT), GrowArrow(right_arrow), run_time=1.1)

        self.play(Indicate(exponent_box, color=ORANGE), Indicate(mantissa_box, color=GREEN_C), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, value, mantissa_box, exponent_box, labels, arrow1, arrow2, move_left, move_right, left_arrow, right_arrow)), run_time=1.0)

    def normalised_vs_unnormalised(self):
        title = self.section_title("3. Normalised vs Unnormalised", PURPLE_B)
        intro = Text("Same number, different forms", font_size=28, color=GREY_A).next_to(title, DOWN, buff=0.35)

        examples = VGroup(
            MathTex("110", font_size=52, color=WHITE),
            MathTex("11.0 \\times 2^1", font_size=52, color=RED_C),
            MathTex("1.10 \\times 2^2", font_size=52, color=GREEN_C),
        ).arrange(DOWN, buff=0.55)
        examples.move_to(ORIGIN)

        labels = VGroup(
            Text("Unnormalised", font_size=24, color=RED_C),
            Text("Still unnormalised", font_size=24, color=RED_C),
            Text("Normalised form", font_size=24, color=GREEN_C),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        labels.next_to(examples, RIGHT, buff=0.7)

        arrows = VGroup(
            Arrow(labels[0].get_left(), examples[0].get_right(), buff=0.15, color=RED_C),
            Arrow(labels[1].get_left(), examples[1].get_right(), buff=0.15, color=RED_C),
            Arrow(labels[2].get_left(), examples[2].get_right(), buff=0.15, color=GREEN_C),
        )

        binary_shift = VGroup(
            MathTex("110", font_size=52, color=WHITE),
            MathTex("11.0", font_size=52, color=WHITE),
            MathTex("1.10", font_size=52, color=WHITE),
        ).arrange(RIGHT, buff=1.1)
        binary_shift.to_edge(DOWN).shift(UP * 0.7)

        shift_text = Text("Move the point left until the first 1 is in front", font_size=24, color=BLUE_A)
        shift_text.next_to(binary_shift, DOWN, buff=0.35)

        self.play(FadeIn(title, shift=DOWN), FadeIn(intro, shift=DOWN), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(mob, shift=UP) for mob in examples], lag_ratio=0.18), run_time=1.8)
        self.play(FadeIn(labels, shift=LEFT), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.4)
        self.wait(0.8)
        self.play(FadeIn(binary_shift[0], shift=UP), run_time=0.5)
        self.play(TransformFromCopy(binary_shift[0], binary_shift[1]), run_time=1.0)
        self.play(TransformFromCopy(binary_shift[1], binary_shift[2]), run_time=1.0)
        self.play(FadeIn(shift_text, shift=UP), run_time=0.8)
        self.play(Indicate(binary_shift[2], color=GREEN_C), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, intro, examples, labels, arrows, binary_shift, shift_text)), run_time=1.0)

    def storage_concept(self):
        title = self.section_title("4. Storage Concept", GOLD_B)
        intro = Text("A floating-point number is split into three parts", font_size=26, color=GREY_A).next_to(title, DOWN, buff=0.35)

        slots = VGroup(
            Rectangle(width=2.0, height=0.9, color=RED_C, stroke_width=3),
            Rectangle(width=3.2, height=0.9, color=ORANGE, stroke_width=3),
            Rectangle(width=4.0, height=0.9, color=GREEN_C, stroke_width=3),
        ).arrange(RIGHT, buff=0.08)
        slots.move_to(ORIGIN)

        slot_labels = VGroup(
            Text("Sign", font_size=28, color=RED_C),
            Text("Exponent", font_size=28, color=ORANGE),
            Text("Mantissa", font_size=28, color=GREEN_C),
        )
        for label, box in zip(slot_labels, slots):
            label.move_to(box)

        bit_labels = VGroup(
            Text("-", font_size=34, color=RED_C),
            Text("2^2", font_size=30, color=ORANGE),
            Text("1.10", font_size=30, color=GREEN_C),
        )
        bit_labels[0].move_to(slots[0])
        bit_labels[1].move_to(slots[1])
        bit_labels[2].move_to(slots[2])

        connector = MathTex("1.10 \\times 2^2", font_size=50, color=WHITE)
        connector.next_to(slots, DOWN, buff=0.8)
        arrow = Arrow(connector.get_top(), slots[1].get_bottom(), color=ORANGE, buff=0.15)

        self.play(FadeIn(title, shift=DOWN), FadeIn(intro, shift=DOWN), run_time=1.2)
        self.play(LaggedStart(*[Create(box) for box in slots], lag_ratio=0.15), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(lbl, scale=0.85) for lbl in slot_labels], lag_ratio=0.15), run_time=1.2)
        self.play(TransformFromCopy(slot_labels[0], bit_labels[0]), TransformFromCopy(slot_labels[1], bit_labels[1]), TransformFromCopy(slot_labels[2], bit_labels[2]), run_time=1.3)
        self.play(FadeIn(connector, shift=UP), GrowArrow(arrow), run_time=1.0)
        self.play(Indicate(slot_labels[0], color=RED_C), Indicate(slot_labels[1], color=ORANGE), Indicate(slot_labels[2], color=GREEN_C), run_time=1.1)
        self.wait(1.8)


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        "-p",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "FloatingPointStory",
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
