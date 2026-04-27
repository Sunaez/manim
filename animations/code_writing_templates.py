from pathlib import Path
import subprocess
import sys

from manim import *

from palette import apply_palette

RENDER_QUALITY = "low"
# low: preview quality
# medium: standard render quality
# high: final render quality
COLOR_SCHEME = "Sepia"

P = apply_palette(COLOR_SCHEME)
BACKGROUND = P.BG_0
SURFACE = P.BG_1
SURFACE_ALT = P.BG_2
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY
FAINT = P.TEXT_FAINT
BLUE = P.BLUE
CYAN = P.CYAN
TEAL = P.TEAL
GREEN = P.GREEN
YELLOW = P.YELLOW
AMBER = P.AMBER
ORANGE = P.ORANGE
RED = P.RED
PINK = P.PINK
PURPLE = P.PURPLE
VIOLET = P.VIOLET

CODE_FONT = "Consolas"


class CodeWritingTemplates(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.show_title()
        self.clear_stage()
        self.show_templates()
        self.clear_stage()
        self.show_summary()
        self.wait(1.2)

    def show_title(self):
        title = Text("Different ways to write the same code", font_size=38, color=TEXT, weight=BOLD)
        subtitle = Text("Four styles for the same snippet.", font_size=22, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.18)
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=BLUE, stroke_width=3).next_to(subtitle, DOWN, buff=0.18)

        glow = Circle(radius=1.35, color=BLUE, stroke_width=0)
        glow.set_fill(BLUE, opacity=0.08)
        glow.move_to(title)

        title_group = VGroup(glow, title, subtitle, line)
        title_group.to_edge(UP, buff=0.35)
        self.title_group = VGroup(title, subtitle, line)

        self.play(FadeIn(glow), FadeIn(title, shift=UP * 0.08), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.05), Create(line), run_time=0.75)
        self.wait(0.4)

    def show_templates(self):
        self.show_clean_block()
        self.clear_stage()
        self.show_reveal_block()
        self.clear_stage()
        self.show_annotated_block()
        self.clear_stage()
        self.show_split_block()

    def show_clean_block(self):
        self.cards = {}
        card = self.clean_block_card()

        self.play(FadeIn(card, shift=UP * 0.08), run_time=0.9)
        self.play(Indicate(self.cards["clean"]["title"], color=BLUE), run_time=0.35)
        self.play(self.cards["clean"]["highlight"].animate.set_opacity(1.0), run_time=0.2)
        self.play(Indicate(self.cards["clean"]["output"], color=GREEN), run_time=0.45)
        self.wait(0.45)

    def show_reveal_block(self):
        self.cards = {}
        card = self.reveal_card()

        self.play(FadeIn(card, shift=UP * 0.08), run_time=0.9)
        self.play(Indicate(self.cards["reveal"]["title"], color=GREEN), run_time=0.35)

        for row in self.cards["reveal"]["rows"]:
            self.play(row.animate.set_opacity(1.0), run_time=0.28)
            self.play(
                self.cards["reveal"]["focus"].animate.set_opacity(1.0),
                Transform(self.cards["reveal"]["focus"], self.highlight_line(row[1], GREEN)),
                run_time=0.22,
            )
            self.play(Indicate(row[1], color=GREEN), run_time=0.2)
        self.wait(0.45)

    def show_annotated_block(self):
        self.cards = {}
        card = self.annotated_card()
        self.position_extras()

        self.play(FadeIn(card, shift=UP * 0.08), run_time=0.9)
        self.play(Indicate(self.cards["annotated"]["title"], color=AMBER), run_time=0.35)
        self.play(
            LaggedStart(
                *[mob.animate.set_opacity(1.0) for mob in self.cards["annotated"]["callouts"]],
                lag_ratio=0.12,
            ),
            run_time=0.85,
        )
        self.play(Indicate(self.cards["annotated"]["loop_brace"], color=AMBER), run_time=0.45)
        self.wait(0.45)

    def show_split_block(self):
        self.cards = {}
        card = self.split_result_card()
        self.position_extras()

        self.play(FadeIn(card, shift=UP * 0.08), run_time=0.9)
        self.play(Indicate(self.cards["split"]["title"], color=PURPLE), run_time=0.35)
        self.play(
            self.cards["split"]["output_box"].animate.set_opacity(1.0),
            self.cards["split"]["console_label"].animate.set_opacity(1.0),
            self.cards["split"]["output_value"].animate.set_opacity(1.0),
            self.cards["split"]["arrow"].animate.set_opacity(1.0),
            self.cards["split"]["caption"].animate.set_opacity(1.0),
            run_time=0.6,
        )
        self.play(Indicate(self.cards["split"]["output_value"], color=YELLOW), run_time=0.45)
        self.wait(0.45)

    def clear_stage(self):
        if not self.mobjects:
            return
        mobs = list(self.mobjects)
        self.play(*[FadeOut(mob, shift=DOWN * 0.08) for mob in mobs], run_time=0.65)
        self.clear()

    def show_summary(self):
        summary = RoundedRectangle(width=12.1, height=1.05, corner_radius=0.18, color=CYAN, stroke_width=2.2)
        summary.set_fill(SURFACE, opacity=0.96)
        summary.to_edge(DOWN, buff=0.28)

        headline = Text("Pick the template that matches the job.", font_size=24, color=TEXT, weight=BOLD)
        headline.move_to(summary.get_center() + UP * 0.13)

        chips = VGroup(
            self.chip("Reference", BLUE),
            self.chip("Teaching", GREEN),
            self.chip("Explanation", AMBER),
            self.chip("Demo", PURPLE),
        ).arrange(RIGHT, buff=0.16)
        chips.scale(0.8)
        chips.next_to(headline, DOWN, buff=0.16)

        self.play(FadeIn(summary, shift=UP * 0.08), Write(headline), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(chip, shift=UP * 0.05) for chip in chips], lag_ratio=0.12), run_time=0.7)

    def clean_block_card(self):
        frame, title, subtitle = self.card_shell(
            "Clean block",
            "Quick to scan.",
            BLUE,
        )

        code_specs = [
            ("items = [2, 4, 6]", {"items": CYAN, "2": YELLOW, "4": YELLOW, "6": YELLOW}, "items"),
            ("total = 0", {"total": TEAL, "0": YELLOW}, "total"),
            ("for value in items:", {"for": BLUE, "value": GREEN, "items": CYAN}, "loop"),
            ("    total += value", {"total": TEAL, "+=": YELLOW, "value": GREEN}, "update"),
            ("print(total)", {"print": GREEN, "total": TEAL}, "output"),
        ]
        code, refs = self.code_block(code_specs, font_size=16.5, numbered=True, line_gap=0.18)
        code.move_to(frame.get_center() + DOWN * 0.05).shift(DOWN * 0.08 + RIGHT * 0.05)
        code.scale(0.94)

        highlight = self.highlight_line(refs["output"], GREEN)
        highlight.set_opacity(0.0)

        group = VGroup(frame, title, subtitle, code, highlight)
        self.cards["clean"] = {
            "frame": frame,
            "title": title,
            "subtitle": subtitle,
            "code": code,
            "lines": list(refs.values()),
            "highlight": highlight,
            "output": refs["output"],
        }
        return group

    def reveal_card(self):
        frame, title, subtitle = self.card_shell(
            "Type-in reveal",
            "Teach one step at a time.",
            GREEN,
        )

        code_specs = [
            ("items = [2, 4, 6]", {"items": CYAN, "2": YELLOW, "4": YELLOW, "6": YELLOW}, "items"),
            ("total = 0", {"total": TEAL, "0": YELLOW}, "total"),
            ("for value in items:", {"for": BLUE, "value": GREEN, "items": CYAN}, "loop"),
            ("    total += value", {"total": TEAL, "+=": YELLOW, "value": GREEN}, "update"),
            ("print(total)", {"print": GREEN, "total": TEAL}, "output"),
        ]
        code, refs = self.code_block(code_specs, font_size=16.0, numbered=True, line_gap=0.16)
        code.move_to(frame.get_center() + DOWN * 0.03).shift(DOWN * 0.08 + RIGHT * 0.03)
        code.scale(0.94)

        for row in code:
            row[0].set_opacity(0.0)
            row[1].set_opacity(0.0)
        focus = self.highlight_line(code[0][1], GREEN)
        focus.set_opacity(0.0)

        group = VGroup(frame, title, subtitle, code, focus)
        self.cards["reveal"] = {
            "frame": frame,
            "title": title,
            "subtitle": subtitle,
            "rows": code,
            "lines": [row[1] for row in code],
            "focus": focus,
        }
        return group

    def annotated_card(self):
        frame, title, subtitle = self.card_shell(
            "Annotated walkthrough",
            "Add labels and meaning.",
            AMBER,
        )

        code_specs = [
            ("items = [2, 4, 6]", {"items": CYAN, "2": YELLOW, "4": YELLOW, "6": YELLOW}, "items"),
            ("total = 0", {"total": TEAL, "0": YELLOW}, "total"),
            ("for value in items:", {"for": BLUE, "value": GREEN, "items": CYAN}, "loop"),
            ("    total += value", {"total": TEAL, "+=": YELLOW, "value": GREEN}, "update"),
            ("print(total)", {"print": GREEN, "total": TEAL}, "output"),
        ]
        code, refs = self.code_block(code_specs, font_size=15.8, numbered=False, line_gap=0.16)
        code.move_to(frame.get_center() + DOWN * 0.03).shift(DOWN * 0.03 + LEFT * 0.08)

        brace = Brace(VGroup(refs["loop"], refs["update"]), RIGHT, color=AMBER, buff=0.1)
        brace_label = Text("repeat for each value", font_size=15, color=AMBER, weight=BOLD)
        brace_label.next_to(brace, RIGHT, buff=0.12)

        input_tag = self.callout("input list", BLUE)
        input_tag.next_to(refs["items"], LEFT, buff=0.28)
        input_arrow = Arrow(input_tag.get_right(), refs["items"].get_left(), buff=0.08, color=BLUE, stroke_width=3)

        start_tag = self.callout("start here", TEAL)
        start_tag.next_to(refs["total"], RIGHT, buff=0.25)
        start_arrow = Arrow(start_tag.get_left(), refs["total"].get_right(), buff=0.08, color=TEAL, stroke_width=3)

        output_tag = self.callout("show result", GREEN)
        output_tag.next_to(refs["output"], RIGHT, buff=0.3)
        output_arrow = Arrow(output_tag.get_left(), refs["output"].get_right(), buff=0.08, color=GREEN, stroke_width=3)

        callouts = VGroup(input_tag, input_arrow, start_tag, start_arrow, output_tag, output_arrow, brace, brace_label)
        callouts.set_opacity(0.0)

        group = VGroup(frame, title, subtitle, code)
        self.cards["annotated"] = {
            "frame": frame,
            "title": title,
            "subtitle": subtitle,
            "code": code,
            "callouts": [input_tag, input_arrow, start_tag, start_arrow, output_tag, output_arrow, brace, brace_label],
            "loop_brace": brace,
        }
        return group

    def split_result_card(self):
        frame, title, subtitle = self.card_shell(
            "Code + result",
            "Show code and output together.",
            PURPLE,
        )

        left_block = self.code_block(
            [
                ("items = [2, 4, 6]", {"items": CYAN, "2": YELLOW, "4": YELLOW, "6": YELLOW}, "items"),
                ("total = 0", {"total": TEAL, "0": YELLOW}, "total"),
                ("for value in items:", {"for": BLUE, "value": GREEN, "items": CYAN}, "loop"),
                ("    total += value", {"total": TEAL, "+=": YELLOW, "value": GREEN}, "update"),
                ("print(total)", {"print": GREEN, "total": TEAL}, "output"),
            ],
            font_size=14.8,
            numbered=False,
            line_gap=0.14,
        )[0]
        left_block.scale(0.86)
        left_block.move_to(frame.get_left() + RIGHT * 1.55 + DOWN * 0.08)

        output_box = RoundedRectangle(width=1.7, height=1.15, corner_radius=0.18, color=PURPLE, stroke_width=2)
        output_box.set_fill(SURFACE_ALT, opacity=0.98)
        output_box.move_to(frame.get_right() + LEFT * 1.55 + DOWN * 0.02)
        output_box.set_opacity(0.0)
        output_value = Integer(12, font_size=32, color=TEXT)
        output_value.move_to(output_box)
        output_value.set_opacity(0.0)

        arrow = Arrow(
            left_block[-1].get_right() + RIGHT * 0.12,
            output_box.get_left() + LEFT * 0.1,
            buff=0.08,
            color=PURPLE,
            stroke_width=4,
        )
        arrow.set_opacity(0.0)

        caption = self.chip("print(total) -> 12", PURPLE)
        caption.scale(0.68)
        caption.next_to(output_box, DOWN, buff=0.12)
        caption.set_opacity(0.0)

        group = VGroup(frame, title, subtitle, left_block)
        self.cards["split"] = {
            "frame": frame,
            "title": title,
            "subtitle": subtitle,
            "code": left_block,
            "output_box": output_box,
            "caption": caption,
            "output_value": output_value,
            "arrow": arrow,
        }
        return group

    def position_extras(self):
        annotated = self.cards.get("annotated")
        if annotated is not None:
            code = annotated["code"]
            refs = {
                "items": code[0],
                "total": code[1],
                "loop": code[2],
                "update": code[3],
                "output": code[4],
            }

            input_tag, input_arrow, start_tag, start_arrow, output_tag, output_arrow, brace, brace_label = annotated["callouts"]
            input_tag.next_to(refs["items"], LEFT, buff=0.2)
            input_arrow.put_start_and_end_on(input_tag.get_right(), refs["items"].get_left())
            start_tag.next_to(refs["total"], RIGHT, buff=0.18)
            start_arrow.put_start_and_end_on(start_tag.get_left(), refs["total"].get_right())
            output_tag.next_to(refs["output"], RIGHT, buff=0.22)
            output_arrow.put_start_and_end_on(output_tag.get_left(), refs["output"].get_right())
            brace.next_to(VGroup(refs["loop"], refs["update"]), RIGHT, buff=0.1)
            brace_label.next_to(brace, RIGHT, buff=0.12)
            self.add(input_tag, input_arrow, start_tag, start_arrow, output_tag, output_arrow, brace, brace_label)

        split = self.cards.get("split")
        if split is not None:
            code = split["code"]
            frame = split["frame"]
            output_box = split["output_box"]
            console_label = Text("output", font_size=15, color=PURPLE, weight=BOLD)
            console_label.set_opacity(0.0)
            output_value = split["output_value"]
            arrow = split["arrow"]
            caption = split["caption"]

            output_box.move_to(frame.get_right() + LEFT * 1.45 + DOWN * 0.02)
            console_label.next_to(output_box, UP, buff=0.12)
            output_value.move_to(output_box)
            arrow.put_start_and_end_on(code[-1].get_right() + RIGHT * 0.12, output_box.get_left() + LEFT * 0.1)
            caption.next_to(output_box, DOWN, buff=0.12)
            split["console_label"] = console_label
            self.add(output_box, console_label, output_value, arrow, caption)

    def card_shell(self, title_text, subtitle_text, accent):
        frame = RoundedRectangle(width=5.95, height=3.0, corner_radius=0.18, color=P.BORDER, stroke_width=2.2)
        frame.set_fill(SURFACE, opacity=0.97)

        title = self.pill(title_text, accent)
        title.scale(0.72)
        title.move_to(frame.get_top() + DOWN * 0.34).align_to(frame, LEFT).shift(RIGHT * 0.24)

        subtitle = Text(subtitle_text, font_size=15, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.1)
        subtitle.align_to(title, LEFT)

        return frame, title, subtitle

    def code_block(self, specs, font_size=16, numbered=False, line_gap=0.16):
        rows = VGroup()
        refs = {}

        for i, (text, color_map, key) in enumerate(specs, start=1):
            line = Text(text, font=CODE_FONT, font_size=font_size, color=TEXT, t2c=color_map)
            line.set_z_index(2)
            if key is not None:
                refs[key] = line

            if numbered:
                number = Text(str(i), font=CODE_FONT, font_size=12, color=FAINT)
                row = VGroup(number, line).arrange(RIGHT, buff=0.14)
            else:
                row = line
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=line_gap)
        return rows, refs

    def callout(self, text, color):
        label = Text(text, font_size=14.5, color=color, weight=BOLD)
        box = RoundedRectangle(width=label.width + 0.34, height=0.42, corner_radius=0.12, color=color, stroke_width=1.6)
        box.set_fill(BACKGROUND, opacity=1)
        label.move_to(box)
        return VGroup(box, label)

    def chip(self, text, color):
        label = Text(text, font_size=18, color=color, weight=BOLD)
        bg = RoundedRectangle(width=label.width + 0.42, height=0.5, corner_radius=0.18, color=color, stroke_width=1.5)
        bg.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def pill(self, text, color):
        label = Text(text, font_size=18, color=color, weight=BOLD)
        bg = RoundedRectangle(width=label.width + 0.5, height=0.54, corner_radius=0.2, color=color, stroke_width=1.6)
        bg.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def highlight_line(self, line, color):
        box = SurroundingRectangle(line, color=color, buff=0.08, corner_radius=0.08, stroke_width=3)
        box.set_fill(color, opacity=0.12)
        return box

    def preflight_layout_check(self):
        self.assert_separated("top left card", self.cards["clean"]["frame"], "top right card", self.cards["reveal"]["frame"], padding=0.1)
        self.assert_separated("bottom left card", self.cards["annotated"]["frame"], "bottom right card", self.cards["split"]["frame"], padding=0.1)
        self.assert_separated("top row", VGroup(self.cards["clean"]["frame"], self.cards["reveal"]["frame"]), "bottom row", VGroup(self.cards["annotated"]["frame"], self.cards["split"]["frame"]), padding=0.18)

    def assert_separated(self, left_name, left_mob, right_name, right_mob, padding=0.0):
        left = self.bounds(left_mob)
        right = self.bounds(right_mob)

        x_overlap = left["left"] - padding <= right["right"] and right["left"] - padding <= left["right"]
        y_overlap = left["bottom"] - padding <= right["top"] and right["bottom"] - padding <= left["top"]
        if x_overlap and y_overlap:
            raise ValueError(f"Layout overlap detected between {left_name!r} and {right_name!r}.")

    def bounds(self, mob):
        points = mob.get_all_points()
        if len(points) == 0:
            center = mob.get_center()
            return {"left": center[0], "right": center[0], "top": center[1], "bottom": center[1]}

        xs = points[:, 0]
        ys = points[:, 1]
        return {"left": float(xs.min()), "right": float(xs.max()), "top": float(ys.max()), "bottom": float(ys.min())}


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        "-p",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "CodeWritingTemplates",
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
