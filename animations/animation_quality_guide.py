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
SURFACE_SOFT = P.BG_3
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_MUTED
BLUE = P.BLUE
CYAN = P.CYAN
GREEN = P.GREEN
AMBER = P.AMBER
RED = P.ORANGE
PINK = P.PINK
VIOLET = P.PURPLE


class AnimationQualityGuide(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        header = self.header("Improving Animation Quality", "Visual ways to make educational scenes feel more intentional")
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=1.0)

        intro = self.intro_row()
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in intro], lag_ratio=0.12), run_time=1.4)
        self.wait(0.6)
        self.play(FadeOut(intro, shift=DOWN * 0.15), run_time=0.6)

        self.continuity_demo(header)
        self.animate_the_idea_demo(header)
        self.visual_hierarchy_demo(header)
        self.pacing_demo(header)
        self.style_system_demo(header)

        final_note = self.summary_panel()
        self.play(FadeIn(final_note, shift=UP * 0.2), run_time=0.9)
        self.wait(1.8)

    def header(self, title_text, subtitle_text):
        title = Text(title_text, font_size=34, color=TEXT, weight=BOLD)
        subtitle = Text(subtitle_text, font_size=22, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.16)
        line = Line(LEFT * 5.2, RIGHT * 5.2, color=BLUE, stroke_opacity=0.7).next_to(subtitle, DOWN, buff=0.22)
        group = VGroup(title, subtitle, line)
        group.to_edge(UP, buff=0.35)
        return group

    def intro_row(self):
        labels = [
            ("Continuity", BLUE),
            ("Animate the idea", GREEN),
            ("Hierarchy", AMBER),
            ("Pacing", PINK),
            ("Style system", VIOLET),
            ("Check overlaps locally", CYAN),
            ("Clear old content", RED),
        ]
        cards = VGroup(*[self.pill(text, color) for text, color in labels]).scale(0.88)
        first_row = VGroup(*cards[:4]).arrange(RIGHT, buff=0.18)
        second_row = VGroup(*cards[4:]).arrange(RIGHT, buff=0.18)
        group = VGroup(first_row, second_row).arrange(DOWN, buff=0.22)
        group.shift(UP * 0.15)
        return group

    def continuity_demo(self, header):
        section = self.section_label("1. Keep continuity instead of hard resets", BLUE)
        left_frame = self.demo_frame("Before", RED).shift(LEFT * 3.35 + DOWN * 0.2)
        right_frame = self.demo_frame("After", GREEN).shift(RIGHT * 3.35 + DOWN * 0.2)

        old_a = self.topic_card("Problem", "Scene A", RED).move_to(left_frame[0].get_center() + DOWN * 0.1)
        old_b = self.topic_card("Problem", "Scene B", RED).move_to(left_frame[0].get_center() + DOWN * 0.1)

        stable_title = Text("Binary Number", font_size=24, color=TEXT, weight=BOLD)
        stable_title.move_to(right_frame[0].get_top() + DOWN * 0.65)
        state_a = MathTex("110.0", font_size=54, color=TEXT).move_to(right_frame[0].get_center() + UP * 0.15)
        state_b = MathTex("1.10 \\times 2^2", font_size=50, color=GREEN).move_to(state_a)
        anchor = self.small_caption("Anchor objects stay alive across sections.", GREEN)
        anchor.next_to(right_frame[0], DOWN, buff=0.2)

        self.play(FadeIn(section, shift=UP * 0.15), FadeIn(left_frame), FadeIn(right_frame), run_time=0.8)
        self.play(FadeIn(old_a, shift=UP * 0.15), FadeIn(stable_title), FadeIn(state_a), run_time=0.9)
        self.play(FadeOut(old_a, scale=0.9), run_time=0.35)
        self.play(FadeIn(old_b, shift=UP * 0.15), run_time=0.5)
        self.play(
            TransformMatchingTex(state_a, state_b),
            stable_title.animate.set_color(GREEN),
            FadeIn(anchor, shift=UP * 0.1),
            run_time=1.1,
        )
        self.wait(0.5)
        self.play(FadeOut(VGroup(section, left_frame, right_frame, old_b, stable_title, state_a, anchor)), run_time=0.65)

    def animate_the_idea_demo(self, header):
        section = self.section_label("2. Animate the concept, not just the labels", GREEN)
        left_frame = self.demo_frame("Static labels", RED).shift(LEFT * 3.35 + DOWN * 0.2)
        right_frame = self.demo_frame("Concept motion", GREEN).shift(RIGHT * 3.35 + DOWN * 0.2)

        left_number = MathTex("110.0", font_size=58, color=TEXT).move_to(left_frame[0].get_center() + UP * 0.28)
        mantissa_label = self.side_tag("Mantissa", GREEN).move_to(left_frame[0].get_center() + DOWN * 0.25 + LEFT * 1.05)
        exponent_label = self.side_tag("Exponent", AMBER).move_to(left_frame[0].get_center() + DOWN * 0.25 + RIGHT * 1.05)

        stage_0 = MathTex("110.0", font_size=58, color=TEXT)
        stage_1 = MathTex("11.0", font_size=58, color=TEXT)
        stage_2 = MathTex("1.10", font_size=58, color=GREEN)
        for mob in (stage_0, stage_1, stage_2):
            mob.move_to(right_frame[0].get_center() + UP * 0.18)

        exponent_box = RoundedRectangle(width=1.7, height=1.15, corner_radius=0.18, color=AMBER, stroke_width=2)
        exponent_box.set_fill(SURFACE_ALT, opacity=1)
        exponent_box.move_to(right_frame[0].get_center() + DOWN * 0.9)
        exponent_title = Text("Exponent", font_size=22, color=AMBER).move_to(exponent_box.get_top() + DOWN * 0.25)
        exponent_value = Integer(0, font_size=34, color=TEXT).move_to(exponent_box.get_bottom() + UP * 0.3)
        rule = self.small_caption("Show the decimal shift and update the exponent with it.", GREEN)
        rule.next_to(right_frame[0], DOWN, buff=0.2)

        self.play(FadeIn(section, shift=UP * 0.15), FadeIn(left_frame), FadeIn(right_frame), run_time=0.8)
        self.play(FadeIn(left_number), FadeIn(mantissa_label), FadeIn(exponent_label), run_time=0.8)
        self.play(FadeIn(stage_0), FadeIn(exponent_box), FadeIn(exponent_title), FadeIn(exponent_value), run_time=0.8)

        exp_one = Integer(1, font_size=34, color=TEXT).move_to(exponent_value)
        exp_two = Integer(2, font_size=34, color=TEXT).move_to(exponent_value)
        self.play(
            TransformMatchingTex(stage_0, stage_1),
            Transform(exponent_value, exp_one),
            run_time=0.9,
        )
        self.play(
            TransformMatchingTex(stage_1, stage_2),
            Transform(exponent_value, exp_two),
            FadeIn(rule, shift=UP * 0.1),
            run_time=0.9,
        )
        self.wait(0.45)
        self.play(
            FadeOut(
                VGroup(
                    section,
                    left_frame,
                    right_frame,
                    left_number,
                    mantissa_label,
                    exponent_label,
                    stage_0,
                    exponent_box,
                    exponent_title,
                    exponent_value,
                    rule,
                )
            ),
            run_time=0.65,
        )

    def visual_hierarchy_demo(self, header):
        section = self.section_label("3. Reduce clutter and guide the eye", AMBER)
        left_frame = self.demo_frame("Too many active labels", RED).shift(LEFT * 3.35 + DOWN * 0.2)
        right_frame = self.demo_frame("One focus at a time", GREEN).shift(RIGHT * 3.35 + DOWN * 0.2)

        left_cards = VGroup(
            self.busy_card("User", BLUE),
            self.busy_card("Toaster", GREEN),
            self.busy_card("Output", AMBER),
        ).arrange(RIGHT, buff=0.16).scale(0.75)
        left_cards.move_to(left_frame[0].get_center() + UP * 0.15)
        left_arrows = VGroup(
            Arrow(left_cards[0].get_right(), left_cards[1].get_left(), buff=0.08, color=BLUE),
            Arrow(left_cards[1].get_right(), left_cards[2].get_left(), buff=0.08, color=AMBER),
        )
        left_tags = VGroup(
            self.micro_label("movement", BLUE).move_to(left_arrows[0].get_center() + UP * 0.26),
            self.micro_label("heat", RED).move_to(left_cards[1].get_center() + DOWN * 0.58),
            self.micro_label("stored setting", VIOLET).move_to(left_cards[1].get_top() + DOWN * 0.15),
            self.micro_label("return", AMBER).move_to(left_arrows[1].get_center() + UP * 0.26),
        )

        right_cards = VGroup(
            self.busy_card("User", BLUE),
            self.busy_card("Toaster", GREEN),
            self.busy_card("Toast", AMBER),
        ).arrange(RIGHT, buff=0.18).scale(0.78)
        right_cards.move_to(right_frame[0].get_center() + UP * 0.15)
        right_cards[0].set_opacity(0.35)
        right_cards[2].set_opacity(0.35)
        focus_arrow = Arrow(right_cards[0].get_right(), right_cards[1].get_left(), buff=0.08, color=GREEN, stroke_width=6)
        focus_label = self.side_tag("Current focus", GREEN).move_to(focus_arrow.get_center() + UP * 0.34)
        focus_note = self.small_caption("Mute supporting elements so the active step reads instantly.", GREEN)
        focus_note.next_to(right_frame[0], DOWN, buff=0.2)

        self.play(FadeIn(section, shift=UP * 0.15), FadeIn(left_frame), FadeIn(right_frame), run_time=0.8)
        self.play(FadeIn(left_cards), Create(left_arrows), FadeIn(left_tags), run_time=1.0)
        self.play(FadeIn(right_cards), GrowArrow(focus_arrow), FadeIn(focus_label), FadeIn(focus_note, shift=UP * 0.1), run_time=1.0)
        self.play(
            right_cards[0].animate.set_opacity(1),
            right_cards[1].animate.set_opacity(0.35),
            focus_arrow.animate.put_start_and_end_on(right_cards[1].get_right(), right_cards[2].get_left()),
            focus_label.animate.move_to(right_frame[0].get_center() + UP * 0.85),
            run_time=0.8,
        )
        self.wait(0.4)
        self.play(
            FadeOut(
                VGroup(
                    section,
                    left_frame,
                    right_frame,
                    left_cards,
                    left_arrows,
                    left_tags,
                    right_cards,
                    focus_arrow,
                    focus_label,
                    focus_note,
                )
            ),
            run_time=0.65,
        )

    def pacing_demo(self, header):
        section = self.section_label("4. Give setup, impact, and pause different timing", PINK)
        baseline = NumberLine(x_range=[0, 4, 1], length=7.0, include_ticks=False, include_numbers=False, color=SURFACE_SOFT)
        baseline.shift(DOWN * 0.25)
        beats = VGroup(
            self.beat_node("Setup", BLUE),
            self.beat_node("Reveal", GREEN),
            self.beat_node("Aha", AMBER),
            self.beat_node("Pause", VIOLET),
        ).arrange(RIGHT, buff=0.7)
        beats.move_to(baseline)
        tempo_note = self.small_caption("Uniform timing feels flat. Varied pacing creates shape.", PINK)
        tempo_note.next_to(baseline, DOWN, buff=0.55)
        cursor = Dot(radius=0.09, color=TEXT).move_to(beats[0].get_top() + UP * 0.35)

        self.play(FadeIn(section, shift=UP * 0.15), Create(baseline), FadeIn(beats, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(cursor), run_time=0.2)
        self.play(cursor.animate.move_to(beats[1].get_top() + UP * 0.35), beats[0].animate.scale(1.04), run_time=0.45)
        self.play(cursor.animate.move_to(beats[2].get_top() + UP * 0.35), beats[1].animate.scale(1.08), run_time=0.7)
        self.play(
            Flash(beats[2].get_center(), color=AMBER, flash_radius=0.45),
            beats[2].animate.scale(1.14).set_color(AMBER),
            run_time=1.2,
        )
        self.play(FadeIn(tempo_note, shift=UP * 0.1), cursor.animate.move_to(beats[3].get_top() + UP * 0.35), run_time=0.9)
        self.wait(0.6)
        self.play(FadeOut(VGroup(section, baseline, beats, cursor, tempo_note)), run_time=0.65)

    def style_system_demo(self, header):
        section = self.section_label("5. Use one visual system across the whole series", VIOLET)
        left_frame = self.demo_frame("Mixed styles", RED).shift(LEFT * 3.35 + DOWN * 0.2)
        right_frame = self.demo_frame("Shared system", GREEN).shift(RIGHT * 3.35 + DOWN * 0.2)

        mixed = VGroup(
            Rectangle(width=1.55, height=0.85, color=BLUE, stroke_width=1.5),
            Circle(radius=0.45, color=AMBER, stroke_width=5),
            RoundedRectangle(width=1.8, height=0.92, corner_radius=0.24, color=PINK, stroke_width=2.5),
        ).arrange(DOWN, buff=0.25)
        mixed.move_to(left_frame[0].get_center())

        system_cards = VGroup(
            self.system_card("Entity", BLUE),
            self.system_card("Process", GREEN),
            self.system_card("Output", VIOLET),
        ).arrange(DOWN, buff=0.22)
        system_cards.move_to(right_frame[0].get_center())
        system_arrow = Arrow(system_cards[0].get_bottom(), system_cards[1].get_top(), buff=0.1, color=CYAN)
        system_note = self.small_caption("Shared spacing, shapes, strokes, and color roles build trust.", VIOLET)
        system_note.next_to(right_frame[0], DOWN, buff=0.2)

        self.play(FadeIn(section, shift=UP * 0.15), FadeIn(left_frame), FadeIn(right_frame), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(mob, shift=UP * 0.1) for mob in mixed], lag_ratio=0.12), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.1) for card in system_cards], lag_ratio=0.12), GrowArrow(system_arrow), run_time=1.0)
        self.play(FadeIn(system_note, shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(VGroup(section, left_frame, right_frame, mixed, system_cards, system_arrow, system_note)), run_time=0.65)

    def summary_panel(self):
        title = Text("Quality improves when motion carries meaning.", font_size=30, color=TEXT, weight=BOLD)
        chips = VGroup(
            self.pill("Keep anchors alive", BLUE),
            self.pill("Show state change", GREEN),
            self.pill("Reduce clutter", AMBER),
            self.pill("Vary timing", PINK),
            self.pill("Reuse style rules", VIOLET),
            self.pill("Check overlaps locally", CYAN),
            self.pill("Clear old content", RED),
        ).scale(0.82)
        chip_row_1 = VGroup(*chips[:4]).arrange(RIGHT, buff=0.14)
        chip_row_2 = VGroup(*chips[4:]).arrange(RIGHT, buff=0.14)
        chip_rows = VGroup(chip_row_1, chip_row_2).arrange(DOWN, buff=0.18)
        chip_rows.next_to(title, DOWN, buff=0.32)
        box = RoundedRectangle(width=11.6, height=2.75, corner_radius=0.22, color=CYAN, stroke_width=2)
        box.set_fill(SURFACE, opacity=0.95)
        group = VGroup(box, title, chip_rows)
        title.move_to(box.get_center() + UP * 0.62)
        chip_rows.move_to(box.get_center() + DOWN * 0.28)
        group.move_to(DOWN * 0.35)
        return group

    def section_label(self, text, color):
        label = Text(text, font_size=26, color=color, weight=BOLD)
        label.next_to(ORIGIN, UP, buff=0)
        label.shift(UP * 2.15)
        return label

    def demo_frame(self, text, color):
        frame = RoundedRectangle(width=5.55, height=3.6, corner_radius=0.2, color=color, stroke_width=2)
        frame.set_fill(SURFACE, opacity=0.92)
        chip = self.pill(text, color).scale(0.72)
        chip.move_to(frame.get_top() + DOWN * 0.3)
        return VGroup(frame, chip)

    def topic_card(self, eyebrow, label_text, color):
        card = RoundedRectangle(width=2.5, height=1.45, corner_radius=0.18, color=color, stroke_width=2.5)
        card.set_fill(SURFACE_ALT, opacity=1)
        eyebrow_text = Text(eyebrow, font_size=18, color=MUTED)
        label = Text(label_text, font_size=28, color=TEXT, weight=BOLD)
        eyebrow_text.move_to(card.get_center() + UP * 0.3)
        label.move_to(card.get_center() + DOWN * 0.18)
        return VGroup(card, eyebrow_text, label)

    def pill(self, text, color):
        label = Text(text, font_size=20, color=color, weight=BOLD)
        bg = RoundedRectangle(
            width=label.width + 0.45,
            height=0.52,
            corner_radius=0.22,
            color=color,
            stroke_width=1.6,
        )
        bg.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def side_tag(self, text, color):
        label = Text(text, font_size=20, color=color, weight=BOLD)
        bg = RoundedRectangle(width=label.width + 0.38, height=0.46, corner_radius=0.16, color=color, stroke_width=1.6)
        bg.set_fill(BACKGROUND, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def small_caption(self, text, color):
        label = Text(text, font_size=20, color=TEXT)
        bg = RoundedRectangle(width=min(max(label.width + 0.45, 3.2), 5.3), height=0.62, corner_radius=0.14, color=color, stroke_width=1.6)
        bg.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def busy_card(self, text, color):
        box = RoundedRectangle(width=1.45, height=0.82, corner_radius=0.15, color=color, stroke_width=2)
        box.set_fill(SURFACE_ALT, opacity=1)
        label = Text(text, font_size=20, color=TEXT)
        label.move_to(box)
        return VGroup(box, label)

    def micro_label(self, text, color):
        label = Text(text, font_size=15, color=color)
        bg = SurroundingRectangle(label, color=color, buff=0.08, corner_radius=0.08)
        bg.set_fill(BACKGROUND, opacity=0.95)
        return VGroup(bg, label)

    def beat_node(self, text, color):
        circle = Circle(radius=0.38, color=color, stroke_width=3)
        circle.set_fill(SURFACE, opacity=1)
        label = Text(text, font_size=18, color=TEXT)
        label.next_to(circle, DOWN, buff=0.18)
        return VGroup(circle, label)

    def system_card(self, text, color):
        box = RoundedRectangle(width=2.35, height=0.82, corner_radius=0.18, color=color, stroke_width=2.5)
        box.set_fill(SURFACE_ALT, opacity=1)
        label = Text(text, font_size=22, color=TEXT, weight=BOLD)
        label.move_to(box)
        return VGroup(box, label)


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "AnimationQualityGuide",
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
