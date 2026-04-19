from pathlib import Path
import subprocess
import sys

import numpy as np

from manim import *

FRAME_RATE = 30
RENDER_QUALITY = "high"
# low: 480p, 30fps preview render.
# medium: 720p, 30fps default render.
# high: 1920x1080, 60fps final render.

config.frame_rate = FRAME_RATE

BACKGROUND = "#0f172a"
SURFACE = "#1e293b"
SURFACE_ALT = "#334155"
PRIMARY_BLUE = "#3b82f6"
TEAL = "#14b8a6"
GREEN = "#22c55e"
ORANGE = "#f59e0b"
RED = "#ef4444"
GOLD = "#eab308"
TEXT = "#f8fafc"
MUTED = "#cbd5e1"


class ToasterBlackBox(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.overview_section()
        self.clear_stage()

        self.input_section()
        self.clear_stage()

        self.stored_setting_section()
        self.clear_stage()

        self.output_section()
        self.clear_stage()

        self.summary_section()
        self.wait(1.5)

    def overview_section(self):
        header = self.section_header("Toaster Black Box Model", "Focus on the flow into the toaster, the stored setting, and the flow out.")
        caption = self.caption_card("A black box model shows the external interaction without exposing full internal detail.", PRIMARY_BLUE)
        user, toaster, slot = self.base_stage()

        boundary = SurroundingRectangle(toaster, color=PRIMARY_BLUE, buff=0.24, corner_radius=0.18)
        boundary.set_stroke(width=2.2, opacity=0.8)
        badge = self.tag("Black Box", PRIMARY_BLUE)
        badge.next_to(boundary, UP, buff=0.16)

        self.play(FadeIn(header, shift=DOWN * 0.15), FadeIn(caption, shift=UP * 0.1), run_time=1.0)
        self.play(
            LaggedStart(
                FadeIn(user, shift=RIGHT * 0.2),
                FadeIn(toaster, shift=LEFT * 0.2),
                Create(slot),
                lag_ratio=0.12,
            ),
            run_time=1.1,
        )
        self.play(Create(boundary), FadeIn(badge, shift=UP * 0.08), run_time=0.8)
        self.play(
            user.animate.set_opacity(0.75),
            toaster.animate.set_opacity(1),
            run_time=0.45,
        )
        self.wait(0.8)

    def input_section(self):
        header = self.section_header("1. Input Flow", "Animate the idea: bread travels from the user into the toaster.")
        caption = self.caption_card("Only the current input is highlighted so the viewer tracks one action at a time.", GREEN)
        user, toaster, slot = self.base_stage()

        bread = self.food_token("Bread", GOLD)
        bread.move_to(user.get_right() + RIGHT * 0.58 + UP * 0.42)

        arrow = Arrow(
            user.get_right() + UP * 0.28,
            toaster.get_left() + UP * 0.45,
            buff=0.18,
            color=GREEN,
            stroke_width=5,
        )
        label = self.flow_label("Input: insert bread", arrow, GREEN, above=True)
        trail = Line(bread.get_center(), toaster.get_center() + UP * 0.32, color=GREEN, stroke_opacity=0.25)

        self.play(FadeIn(header, shift=DOWN * 0.15), FadeIn(caption, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(user), FadeIn(toaster), Create(slot), run_time=0.9)
        self.play(FadeIn(bread, scale=0.9), GrowArrow(arrow), FadeIn(label, shift=UP * 0.08), run_time=0.9)
        self.play(MoveAlongPath(bread, trail), run_time=1.2, rate_func=smooth)
        self.play(
            bread.animate.move_to(toaster.get_center() + UP * 0.28).scale(0.94),
            Flash(slot.get_center(), color=GREEN, flash_radius=0.38),
            toaster[0].animate.set_stroke(GREEN, width=3.4),
            run_time=0.8,
        )
        self.wait(0.65)

    def stored_setting_section(self):
        header = self.section_header("2. Stored Setting", "Clear the previous flow and focus on the setting the toaster keeps internally.")
        caption = self.caption_card("The heat level is a stored state inside the toaster, not another moving object.", TEAL)

        toaster = self.toaster_entity(width=4.7, height=3.0, title_size=30, detail_text="Stored heat setting", detail_size=24)
        toaster.move_to(DOWN * 0.2)
        slot = self.toaster_slot(toaster[0], offset=RIGHT * 0.14 + UP * 0.5, height=0.95)

        dots = self.heat_setting_dots(toaster[0], count=4, active_index=2)
        dots.move_to(toaster[0].get_center() + DOWN * 0.86 + RIGHT * 1.02)

        pointer = Triangle(color=TEAL, fill_opacity=1, stroke_width=0).scale(0.12).rotate(-PI / 2)
        pointer.next_to(dots[2], LEFT, buff=0.1)
        label = self.tag("Stored level", TEAL)
        label.next_to(toaster, RIGHT, buff=0.45).shift(UP * 0.15)
        connector = Arrow(label.get_left(), dots[2].get_right(), buff=0.14, color=TEAL, stroke_width=4)

        glow = self.inner_glow(toaster[0])
        waves = self.heat_waves(toaster[0])

        self.play(FadeIn(header, shift=DOWN * 0.15), FadeIn(caption, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(toaster, shift=UP * 0.1), Create(slot), run_time=0.9)
        self.play(FadeIn(dots, shift=UP * 0.08), FadeIn(pointer, shift=RIGHT * 0.08), run_time=0.6)
        self.play(FadeIn(label, shift=LEFT * 0.08), GrowArrow(connector), run_time=0.7)
        self.play(
            dots[2].animate.scale(1.15).set_fill(GOLD, opacity=1),
            FadeIn(glow),
            run_time=0.7,
        )
        self.play(LaggedStart(*[Create(wave) for wave in waves], lag_ratio=0.08), run_time=0.9)
        self.wait(0.7)

    def output_section(self):
        header = self.section_header("3. Output Flow", "Show the state change: the toaster returns toast to the user.")
        caption = self.caption_card("The moving output is toast. Earlier helper labels are gone so the result reads clearly.", ORANGE)
        user, toaster, slot = self.base_stage()

        glow = self.inner_glow(toaster[0])
        toast = self.food_token("Toast", ORANGE)
        toast.move_to(toaster.get_center() + UP * 0.15)

        arrow = Arrow(
            toaster.get_left() + DOWN * 0.42,
            user.get_right() + DOWN * 0.28,
            buff=0.18,
            color=ORANGE,
            stroke_width=5,
        )
        label = self.flow_label("Output: eject toast", arrow, ORANGE, above=False)
        path = Line(toast.get_center(), user.get_right() + RIGHT * 0.56 + DOWN * 0.42, color=ORANGE, stroke_opacity=0.25)

        self.play(FadeIn(header, shift=DOWN * 0.15), FadeIn(caption, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(user), FadeIn(toaster), Create(slot), FadeIn(glow), run_time=0.9)
        self.play(FadeIn(toast, scale=0.9), toaster[0].animate.set_stroke(ORANGE, width=3.4), run_time=0.7)
        self.play(GrowArrow(arrow), FadeIn(label, shift=DOWN * 0.08), run_time=0.8)
        self.play(MoveAlongPath(toast, path), run_time=1.25, rate_func=smooth)
        self.play(
            Flash(user.get_right() + DOWN * 0.05, color=ORANGE, flash_radius=0.42),
            user[0].animate.set_stroke(TEAL, width=3.2),
            run_time=0.75,
        )
        self.wait(0.65)

    def summary_section(self):
        header = self.section_header("4. Summary", "End with a clean recap rather than leaving old diagram parts on screen.")
        caption = self.caption_card("A stronger animation keeps one clear idea active in each section.", PRIMARY_BLUE)

        cards = VGroup(
            self.summary_card("Input", "Bread moves in", GREEN),
            self.summary_card("Stored State", "Heat level stays inside", TEAL),
            self.summary_card("Output", "Toast moves out", ORANGE),
        ).arrange(RIGHT, buff=0.42)
        cards.move_to(DOWN * 0.1)

        self.play(FadeIn(header, shift=DOWN * 0.15), FadeIn(caption, shift=UP * 0.1), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.15), run_time=1.1)
        self.play(
            cards[0][0].animate.set_stroke(GREEN, width=3.5),
            cards[1][0].animate.set_stroke(TEAL, width=3.5),
            cards[2][0].animate.set_stroke(ORANGE, width=3.5),
            run_time=0.7,
        )

    def clear_stage(self):
        if not self.mobjects:
            return
        mobs = list(self.mobjects)
        self.play(*[FadeOut(mob, shift=DOWN * 0.12) for mob in mobs], run_time=0.55)
        self.clear()

    def base_stage(self):
        user = self.user_entity()
        toaster = self.toaster_entity()
        user.move_to(LEFT * 4.0 + DOWN * 0.15)
        toaster.move_to(RIGHT * 2.1 + DOWN * 0.1)
        slot = self.toaster_slot(toaster[0])
        return user, toaster, slot

    def section_header(self, title_text, subtitle_text):
        title = Text(title_text, font_size=34, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.34)
        line = Line(LEFT * 5.2, RIGHT * 5.2, color=PRIMARY_BLUE, stroke_opacity=0.75).next_to(title, DOWN, buff=0.18)
        subtitle = Text(subtitle_text, font_size=22, color=MUTED)
        subtitle.next_to(line, DOWN, buff=0.2)
        return VGroup(title, line, subtitle)

    def caption_card(self, text, color):
        label = Text(text, font_size=20, color=TEXT)
        card = RoundedRectangle(width=11.0, height=0.78, corner_radius=0.16, color=color, stroke_width=2)
        card.set_fill(SURFACE, opacity=0.98)
        label.move_to(card)
        group = VGroup(card, label)
        group.to_edge(DOWN, buff=0.35)
        return group

    def tag(self, text, color):
        label = Text(text, font_size=18, color=color, weight=BOLD)
        bg = RoundedRectangle(width=label.width + 0.36, height=0.42, corner_radius=0.16, color=color, stroke_width=1.6)
        bg.set_fill(BACKGROUND, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def user_entity(self):
        body = RoundedRectangle(width=2.4, height=1.25, corner_radius=0.22, color=TEAL, stroke_width=3)
        body.set_fill(SURFACE, opacity=1)
        label = Text("User", font_size=26, color=TEXT, weight=BOLD)
        label.move_to(body)
        return VGroup(body, label)

    def toaster_entity(self, width=4.3, height=2.6, title_size=28, detail_text="Black box", detail_size=22):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.22, color=PRIMARY_BLUE, stroke_width=3)
        box.set_fill(SURFACE, opacity=1)
        title = Text("Toaster", font_size=title_size, color=TEXT, weight=BOLD)
        title.move_to(box.get_center() + UP * 0.5)
        detail = Text(detail_text, font_size=detail_size, color=MUTED)
        detail.move_to(box.get_center() + DOWN * 0.35)
        return VGroup(box, title, detail)

    def toaster_slot(self, box, offset=RIGHT * 0.13 + UP * 0.42, height=0.82):
        slot = RoundedRectangle(width=0.22, height=height, corner_radius=0.06, color=TEXT, stroke_width=2)
        slot.set_fill(BACKGROUND, opacity=1)
        slot.move_to(box.get_left() + offset)
        return slot

    def heat_setting_dots(self, box, count=3, active_index=1):
        dots = VGroup(
            *[
                Circle(radius=0.09, color=GOLD, stroke_width=1.8).set_fill(MUTED, opacity=0.2)
                for _ in range(count)
            ]
        ).arrange(RIGHT, buff=0.13)
        if 0 <= active_index < len(dots):
            dots[active_index].set_fill(GOLD, opacity=1)
        dots.move_to(box.get_center() + DOWN * 0.76 + RIGHT * 0.84)
        return dots

    def inner_glow(self, box):
        glow = RoundedRectangle(width=3.35, height=1.5, corner_radius=0.22, color=ORANGE, stroke_width=0)
        glow.set_fill(ORANGE, opacity=0.12)
        glow.move_to(box.get_center() + DOWN * 0.02)
        return glow

    def heat_waves(self, box):
        waves = VGroup()
        for x in np.linspace(-0.58, 0.58, 5):
            wave = VMobject(color=ORANGE, stroke_width=3)
            wave.set_points_smoothly(
                [
                    np.array([x, -0.56, 0]),
                    np.array([x - 0.12, -0.2, 0]),
                    np.array([x + 0.12, 0.18, 0]),
                    np.array([x, 0.54, 0]),
                ]
            )
            waves.add(wave)
        waves.scale(0.95)
        waves.move_to(box.get_center())
        return waves

    def food_token(self, text, color):
        token = RoundedRectangle(width=1.45, height=0.8, corner_radius=0.18, color=color, stroke_width=2.4)
        token.set_fill(color, opacity=0.18)
        label = Text(text, font_size=22, color=TEXT, weight=BOLD)
        label.move_to(token)
        return VGroup(token, label)

    def flow_label(self, text, arrow, color, above=True):
        label = Text(text, font_size=20, color=color, weight=BOLD)
        offset = UP * 0.28 if above else DOWN * 0.28
        label.move_to(arrow.get_center() + offset)
        bg = SurroundingRectangle(label, color=color, buff=0.11, corner_radius=0.08)
        bg.set_fill(BACKGROUND, opacity=1)
        bg.set_stroke(width=1.6)
        return VGroup(bg, label)

    def summary_card(self, title_text, detail_text, color):
        card = RoundedRectangle(width=3.2, height=1.7, corner_radius=0.2, color=color, stroke_width=2.4)
        card.set_fill(SURFACE, opacity=1)
        title = Text(title_text, font_size=24, color=color, weight=BOLD)
        detail = Text(detail_text, font_size=20, color=TEXT)
        title.move_to(card.get_center() + UP * 0.32)
        detail.move_to(card.get_center() + DOWN * 0.28)
        return VGroup(card, title, detail)


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "ToasterBlackBox",
    ]
    raise SystemExit(subprocess.call(command))


def quality_args(name):
    quality_map = {
        "low": ["-p", "--fps", "30", "-r", "854,480"],
        "medium": ["-pqm"],
        "high": ["-p", "--fps", "60", "-r", "1920,1080"],
    }
    if name not in quality_map:
        raise ValueError(f"Unsupported RENDER_QUALITY: {name!r}")
    return quality_map[name]


if __name__ == "__main__":
    render_scene()
