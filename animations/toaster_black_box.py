from pathlib import Path
import subprocess
import sys
import numpy as np

from manim import *

FRAME_RATE = 60
RENDER_QUALITY = "high"
# low: 480p, 30fps preview render.
# medium: 720p, 30fps default render.
# high: 1080p, 60fps final render.

config.frame_rate = FRAME_RATE


class ToasterBlackBox(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        title = self.section_title("Toaster Black Box Model", BLUE_B)
        subtitle = self.subtitle_text("A simple black box view of the toaster system", title)
        caption = self.caption_card("The model shows the user, the toaster, and the movement between them.")

        user = self.user_entity()
        toaster = self.toaster_entity()
        slot = self.toaster_slot(toaster[0])
        heat_dots = self.heat_setting_dots(toaster[0])
        glow = self.inner_glow(toaster[0])
        heat_waves = self.heat_waves(toaster[0])
        user.shift(LEFT * 3.6 + DOWN * 0.2)
        toaster.shift(RIGHT * 2.2 + DOWN * 0.2)
        slot.shift(RIGHT * 2.2 + DOWN * 0.2)
        heat_dots.shift(RIGHT * 2.2 + DOWN * 0.2)
        glow.shift(RIGHT * 2.2 + DOWN * 0.2)
        heat_waves.shift(RIGHT * 2.2 + DOWN * 0.2)

        input_start = user.get_right() + UP * 0.28
        input_end = toaster.get_left() + UP * 0.45
        output_start = toaster.get_left() + DOWN * 0.45
        output_end = user.get_right() + DOWN * 0.28

        input_arrow = Arrow(
            input_start,
            input_end,
            buff=0.16,
            color=GREEN,
            stroke_width=5,
        )
        input_label = self.flow_label("Movement - Inserting Bread", input_arrow, GREEN, above=True)

        output_arrow = Arrow(
            output_start,
            output_end,
            buff=0.16,
            color=ORANGE,
            stroke_width=5,
        )
        output_label = self.flow_label("Movement - Eject toast", output_arrow, ORANGE, above=False)

        bread = self.food_token("Bread", GOLD)
        bread.move_to(user.get_right() + RIGHT * 0.55 + UP * 0.45)
        toast = self.food_token("Toast", ORANGE)
        toast.move_to(toaster.get_center() + DOWN * 0.15)

        self.play(Write(title[0]), Create(title[1]), run_time=1.2)
        self.reveal_text(subtitle, run_time=0.8)
        self.reveal_caption(caption)

        self.play(Create(user[0]), FadeIn(user[1], shift=UP * 0.12), run_time=0.9)
        self.play(Create(toaster[0]), FadeIn(toaster[1], shift=UP * 0.12), Create(slot), run_time=0.9)
        self.reveal_text(toaster[2], shift=UP * 0.08, run_time=0.8)
        self.play(Circumscribe(toaster[0], color=PRIMARY_BLUE), run_time=1.0)

        subtitle = self.swap_text(subtitle, "First, the user sends bread into the toaster.")
        caption = self.swap_caption(caption, "The input is a movement flow from the user to the toaster.")
        self.play(GrowArrow(input_arrow), run_time=0.8)
        self.reveal_flow_label(input_label, shift=UP * 0.08)
        self.play(FadeIn(bread, scale=0.85), run_time=0.4)
        self.play(MoveAlongPath(bread, Line(bread.get_center(), input_end + RIGHT * 0.35)), run_time=1.3)
        self.play(
            bread.animate.move_to(toaster.get_center() + UP * 0.28).scale(0.92),
            Flash(slot.get_center(), color=GREEN, flash_radius=0.4),
            run_time=0.8,
        )

        subtitle = self.swap_text(subtitle, "Inside the toaster, the heat setting is stored on site.")
        caption = self.swap_caption(caption, "")
        self.play(FadeIn(heat_dots, shift=UP * 0.08), run_time=0.5)
        self.play(
            Indicate(toaster[2], color=TEAL),
            heat_dots[0].animate.set_fill(MUTED, opacity=0.45),
            heat_dots[1].animate.set_fill(MUTED, opacity=0.45),
            heat_dots[2].animate.set_fill(GOLD, opacity=1),
            run_time=1.0,
        )
        self.play(Circumscribe(toaster[2], color=TEAL), run_time=0.9)

        subtitle = self.swap_text(subtitle, "The toaster applies heat before anything comes back out.")
        caption = self.swap_caption(caption, "The Heat is not part of the diagram, it is just a visual representation !!")
        self.play(FadeIn(glow), run_time=0.5)
        self.play(LaggedStart(*[Create(wave) for wave in heat_waves], lag_ratio=0.12), run_time=1.0)
        self.play(
            toaster[0].animate.set_stroke(ORANGE, width=3.5),
            glow.animate.set_fill(ORANGE, opacity=0.2),
            run_time=0.8,
        )
        self.play(Transform(bread, toast), run_time=0.9)
        self.play(Indicate(bread, color=ORANGE), run_time=0.7)

        subtitle = self.swap_text(subtitle, "Finally, the toaster returns toast to the user. This is a movement output.")
        caption = self.swap_caption(caption, "The output is another movement flow, this time from toaster to user.")
        self.play(GrowArrow(output_arrow), run_time=0.8)
        self.reveal_flow_label(output_label, shift=DOWN * 0.08)
        self.play(
            MoveAlongPath(bread, Line(bread.get_center(), user.get_right() + RIGHT * 0.55 + DOWN * 0.45)),
            run_time=1.4,
        )
        self.play(
            Flash(user.get_right() + DOWN * 0.1, color=ORANGE, flash_radius=0.45),
            Indicate(user[0], color=TEAL),
            run_time=0.9,
        )

        subtitle = self.swap_text(subtitle, "Input, stored setting, and output are all visible in one black box model.")
        caption = self.swap_caption(caption, "")
        self.play(FadeOut(heat_waves), glow.animate.set_fill(ORANGE, opacity=0.08), run_time=0.6)
        self.wait(2.0)

    def section_title(self, text, color=BLUE_B):
        title = Text(text, font_size=34, color=color)
        title.to_edge(UP)
        line = Line(LEFT * 3, RIGHT * 3, color=color).next_to(title, DOWN, buff=0.15)
        return VGroup(title, line)

    def subtitle_text(self, text, title_group):
        subtitle = Text(text, font_size=24, color=MUTED)
        subtitle.next_to(title_group, DOWN, buff=0.35)
        return subtitle

    def caption_card(self, text, color=None):
        color = color or PRIMARY_BLUE
        label = Text(text, font_size=22, color=TEXT)
        card = RoundedRectangle(width=10.7, height=0.95, corner_radius=0.16, color=color, stroke_width=2)
        card.set_fill(SURFACE, opacity=0.88)
        label.move_to(card)
        group = VGroup(card, label)
        group.to_edge(DOWN, buff=0.45)
        return group

    def user_entity(self):
        shape = Ellipse(width=2.6, height=1.5, color=TEAL, stroke_width=3)
        shape.set_fill(SURFACE, opacity=0.9)
        label = Text("User", font_size=28, color=TEXT)
        label.move_to(shape)
        return VGroup(shape, label)

    def toaster_entity(self):
        box = Rectangle(width=4.4, height=2.6, color=PRIMARY_BLUE, stroke_width=3)
        box.set_fill(SURFACE, opacity=0.92)
        title = Text("Toaster", font_size=28, color=TEXT)
        title.move_to(box.get_center() + UP * 0.52)
        detail = Text("On site - Store heat setting", font_size=23, color=MUTED)
        detail.move_to(box.get_center() + DOWN * 0.28)
        return VGroup(box, title, detail)

    def flow_label(self, text, arrow, color, above=True):
        label = Text(text, font_size=22, color=color)
        offset = UP * 0.3 if above else DOWN * 0.3
        label.move_to(arrow.get_center() + offset)
        bg = SurroundingRectangle(label, color=color, buff=0.12, corner_radius=0.08)
        bg.set_fill(BACKGROUND, opacity=0.88)
        bg.set_stroke(color=color, width=1.5)
        return VGroup(bg, label)

    def toaster_slot(self, box):
        slot = RoundedRectangle(width=0.22, height=0.85, corner_radius=0.06, color=TEXT, stroke_width=2)
        slot.set_fill(BACKGROUND, opacity=1)
        slot.move_to(box.get_left() + RIGHT * 0.13 + UP * 0.42)
        return slot

    def heat_setting_dots(self, box):
        dots = VGroup(
            *[
                Circle(radius=0.08, color=GOLD, stroke_width=1.5).set_fill(MUTED, opacity=0.25)
                for _ in range(3)
            ]
        ).arrange(RIGHT, buff=0.12)
        dots.move_to(box.get_center() + DOWN * 0.8 + RIGHT * 0.95)
        return dots

    def inner_glow(self, box):
        glow = RoundedRectangle(
            width=3.45,
            height=1.65,
            corner_radius=0.2,
            color=ORANGE,
            stroke_width=0,
        )
        glow.set_fill(ORANGE, opacity=0.08)
        glow.move_to(box.get_center() + DOWN * 0.02)
        return glow

    def heat_waves(self, box):
        waves = VGroup()
        x_values = np.linspace(-0.58, 0.58, 6)
        for x in x_values:
            wave = VMobject(color=ORANGE, stroke_width=3)
            wave.set_points_smoothly(
                [
                    np.array([x, -0.62, 0]),
                    np.array([x - 0.11, -0.25, 0]),
                    np.array([x + 0.11, 0.15, 0]),
                    np.array([x, 0.58, 0]),
                ]
            )
            waves.add(wave)
        waves.scale(0.82)
        waves.move_to(box.get_center() + DOWN * 0.04)
        return waves

    def food_token(self, text, color):
        token = RoundedRectangle(width=1.35, height=0.78, corner_radius=0.18, color=color, stroke_width=2.5)
        token.set_fill(color, opacity=0.18)
        label = Text(text, font_size=24, color=TEXT)
        label.move_to(token)
        return VGroup(token, label)

    def reveal_text(self, text_mobject, shift=UP * 0.12, run_time=0.8):
        self.play(Write(text_mobject), run_time=run_time * 0.7)
        self.play(text_mobject.animate.shift(shift * 0.15).shift(-shift * 0.15), run_time=run_time * 0.3)

    def reveal_caption(self, caption):
        self.play(FadeIn(caption[0], scale=0.96), run_time=0.35)
        self.play(Write(caption[1]), run_time=0.8)

    def reveal_flow_label(self, flow_label, shift):
        self.play(FadeIn(flow_label[0], scale=0.92), run_time=0.25)
        self.play(Write(flow_label[1]), run_time=0.75)
        self.play(flow_label[1].animate.shift(shift * 0.2).shift(-shift * 0.2), run_time=0.25)

    def swap_text(self, old_text, new_text):
        updated = Text(new_text, font_size=old_text.font_size, color=old_text.color)
        updated.move_to(old_text)
        self.play(TransformMatchingShapes(old_text, updated), run_time=0.8)
        return updated

    def swap_caption(self, old_caption, new_text, color=None):
        card_color = color or old_caption[0].get_stroke_color()
        updated = self.caption_card(new_text, card_color)
        self.play(TransformMatchingShapes(old_caption, updated), run_time=0.9)
        return updated


BACKGROUND = "#f8fafc"
SURFACE = "#ffffff"
PRIMARY_BLUE = "#2563eb"
TEAL = "#0d9488"
GREEN = "#16a34a"
ORANGE = "#ea580c"
GOLD = "#ca8a04"
TEXT = "#0f172a"
MUTED = "#64748b"


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
