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
PRIMARY_BLUE = P.BLUE
TEAL = P.TEAL
GREEN = P.GREEN
ORANGE = P.AMBER
RED = P.RED
GOLD = P.YELLOW
PURPLE = P.PURPLE
BLUE = P.BLUE
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY


class VendingMachineDFD(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.show_intro()
        self.clear()

        self.show_entities_and_boundary()
        self.clear()

        self.show_internal_processes()
        self.clear()

        self.show_purchase_flow()

    def section_title(self, text, color=BLUE_B):
        title = Text(text, font_size=34, color=color)
        title.to_edge(UP)
        line = Line(LEFT * 3, RIGHT * 3, color=color).next_to(title, DOWN, buff=0.15)
        return VGroup(title, line)

    def show_intro(self):
        title = self.section_title("Vending Machine DFD", BLUE_B)
        subtitle = Text("A diagram of the data moving into, through, and out of the system", font_size=25, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.35)
        chip = RoundedRectangle(width=4.9, height=1.0, corner_radius=0.18, color=SURFACE, stroke_width=2)
        chip.set_fill(SURFACE, opacity=1)
        chip.shift(DOWN * 0.25)
        label = Text("Each chunk is shown, then cleared before the next one.", font_size=24, color=TEXT)
        label.move_to(chip)
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), FadeIn(chip), Write(label), run_time=1.5)
        self.wait(0.8)

    def show_entities_and_boundary(self):
        title = self.section_title("1. External Entities", BLUE_B)
        subtitle = Text("People and services outside the machine", font_size=25, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.35)

        boundary = RoundedRectangle(width=8.6, height=4.5, corner_radius=0.2, color=PRIMARY_BLUE, stroke_width=3)
        boundary.set_fill(SURFACE, opacity=0.2)
        boundary.shift(DOWN * 0.1)
        boundary_label = Text("Vending Machine System", font_size=26, color=PRIMARY_BLUE)
        boundary_label.next_to(boundary, UP, buff=0.15)

        customer = self.external_entity("Customer", GREEN)
        payment = self.external_entity("Payment Service", ORANGE)
        technician = self.external_entity("Technician", PURPLE)
        customer.to_edge(LEFT, buff=0.6).shift(UP * 0.7)
        payment.to_edge(RIGHT, buff=0.6).shift(UP * 1.0)
        technician.to_edge(DOWN, buff=0.6).shift(RIGHT * 2.4)

        arrow1 = Arrow(customer.get_right(), boundary.get_left(), buff=0.2, color=GREEN)
        arrow2 = Arrow(boundary.get_right(), payment.get_left(), buff=0.2, color=ORANGE)
        arrow3 = Arrow(boundary.get_bottom(), technician.get_top(), buff=0.2, color=PURPLE)

        label1 = self.flow_label("choice / payment", arrow1, GREEN, above=True)
        label2 = self.flow_label("approval request", arrow2, ORANGE, above=True)
        label3 = self.flow_label("restock alert", arrow3, PURPLE, above=False)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=1.0)
        self.play(Create(boundary), FadeIn(boundary_label, shift=UP), run_time=1.0)
        self.play(LaggedStart(Create(customer), Create(payment), Create(technician), lag_ratio=0.18), run_time=1.2)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3), run_time=1.0)
        self.play(FadeIn(label1, shift=UP * 0.1), FadeIn(label2, shift=UP * 0.1), FadeIn(label3, shift=DOWN * 0.1), run_time=1.0)
        self.wait(1.0)

    def show_internal_processes(self):
        title = self.section_title("2. Internal Processes", TEAL)
        subtitle = Text("What the vending machine does with the data", font_size=25, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.35)

        blocks = VGroup(
            self.block("User Interface", GREEN),
            self.block("Payment Check", ORANGE),
            self.block("Inventory", TEAL),
            self.block("Dispense", BLUE),
        ).arrange_in_grid(rows=2, cols=2, buff=0.8)
        blocks.shift(DOWN * 0.05)

        labels = VGroup(
            Text("Choose item", font_size=22, color=GREEN),
            Text("Validate funds", font_size=22, color=ORANGE),
            Text("Check stock", font_size=22, color=TEAL),
            Text("Release snack", font_size=22, color=BLUE),
        )
        for label, box in zip(labels, blocks):
            label.move_to(box)

        connector1 = Arrow(blocks[0].get_right(), blocks[1].get_left(), buff=0.16, color=BLUE)
        connector2 = Arrow(blocks[1].get_bottom(), blocks[2].get_top(), buff=0.16, color=TEAL)
        connector3 = Arrow(blocks[2].get_right(), blocks[3].get_left(), buff=0.16, color=GREEN)
        loop_start = blocks[3].get_top() + UP * 0.05
        loop_end = blocks[0].get_bottom() + DOWN * 0.05
        loop = CurvedArrow(loop_start, loop_end, angle=-PI / 2, color=GOLD)

        label1 = self.flow_label("selection", connector1, BLUE, above=True)
        label2 = self.flow_label("auth status", connector2, TEAL, above=False)
        label3 = self.flow_label("item signal", connector3, GREEN, above=True)
        label4 = self.flow_label("complete", loop, GOLD, above=True)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=1.0)
        self.play(LaggedStart(*[Create(box) for box in blocks], lag_ratio=0.12), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(lbl, scale=0.9) for lbl in labels], lag_ratio=0.08), run_time=0.9)
        self.play(GrowArrow(connector1), GrowArrow(connector2), GrowArrow(connector3), Create(loop), run_time=1.2)
        self.play(FadeIn(label1, shift=UP * 0.1), FadeIn(label2, shift=DOWN * 0.1), FadeIn(label3, shift=UP * 0.1), FadeIn(label4, shift=UP * 0.1), run_time=1.0)
        self.wait(1.0)

    def show_purchase_flow(self):
        title = self.section_title("3. Purchase Flow", GOLD)
        subtitle = Text("One typical path through the DFD", font_size=25, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.35)

        steps = VGroup(
            self.step_card("1", "Select item", GREEN),
            self.step_card("2", "Pay", ORANGE),
            self.step_card("3", "Check stock", TEAL),
            self.step_card("4", "Dispense", BLUE),
        ).arrange(RIGHT, buff=0.55)
        steps.shift(DOWN * 0.2)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.15) for step in steps], lag_ratio=0.12), run_time=1.2)

        packet = Dot(radius=0.08, color=TEXT)
        packet.move_to(steps[0].get_right() + RIGHT * 0.25)
        self.play(FadeIn(packet), run_time=0.3)

        flow_specs = [
            (steps[0], steps[1], "selection", BLUE),
            (steps[1], steps[2], "payment", ORANGE),
            (steps[2], steps[3], "authorise and dispatch", TEAL),
        ]

        for source, target, label_text, color in flow_specs:
            arrow = Arrow(source.get_right(), target.get_left(), buff=0.14, color=color)
            label = self.flow_label(label_text, arrow, color, above=True)
            self.play(
                Indicate(source, color=color),
                Create(arrow),
                FadeIn(label, shift=UP * 0.12),
                run_time=0.8,
            )
            self.play(packet.animate.move_to(target.get_left() + LEFT * 0.25), run_time=0.6)
            self.play(FadeOut(arrow), FadeOut(label), run_time=0.25)
            self.play(Indicate(target, color=color), run_time=0.35)

        result = Text("Data moves forward, one step at a time.", font_size=26, color=TEXT)
        result.next_to(steps, DOWN, buff=0.55)
        self.play(FadeOut(packet), Write(result), run_time=0.9)
        self.wait(1.5)

    def external_entity(self, text, color):
        box = RoundedRectangle(width=2.4, height=0.85, corner_radius=0.15, color=color, stroke_width=3)
        box.set_fill(SURFACE, opacity=0.85)
        label = Text(text, font_size=24, color=color)
        label.move_to(box)
        return VGroup(box, label)

    def block(self, text, color):
        box = RoundedRectangle(width=2.35, height=1.05, corner_radius=0.16, color=color, stroke_width=3)
        box.set_fill(SURFACE, opacity=0.95)
        label = Text(text, font_size=22, color=TEXT)
        label.move_to(box)
        return VGroup(box, label)

    def flow_label(self, text, arrow, color, above=True):
        label = Text(text, font_size=20, color=color)
        offset = UP * 0.25 if above else DOWN * 0.25
        label.move_to(arrow.get_center() + offset)
        bg = SurroundingRectangle(label, color=color, buff=0.12, corner_radius=0.08)
        bg.set_fill(BACKGROUND, opacity=0.85)
        bg.set_stroke(color=color, width=1.5)
        return VGroup(bg, label)

    def step_card(self, number, text, color):
        card = RoundedRectangle(width=2.1, height=1.25, corner_radius=0.16, color=color, stroke_width=3)
        card.set_fill(SURFACE, opacity=0.95)
        num = Circle(radius=0.24, color=color, stroke_width=2)
        num.set_fill(color, opacity=0.95)
        num.move_to(card.get_left() + RIGHT * 0.45)
        number_text = Text(number, font_size=20, color=BACKGROUND)
        number_text.move_to(num)
        label = Text(text, font_size=24, color=TEXT)
        label.next_to(num, RIGHT, buff=0.25)
        group = VGroup(card, num, number_text, label)
        return group


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "VendingMachineDFD",
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
