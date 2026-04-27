from pathlib import Path
import subprocess
import sys

from manim import *
from palette import apply_palette

RENDER_QUALITY = "medium"
# Choose one of: low, medium, high.
# low: preview render.
# medium: default render.
# high: final render.

P = apply_palette("Dark")
BACKGROUND = P.BG_0
SURFACE = P.BG_1
SURFACE_ALT = P.BG_2
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY
BLUE = P.BLUE
TEAL = P.TEAL
GREEN = P.GREEN
YELLOW = P.YELLOW
AMBER = P.AMBER
ORANGE = P.ORANGE
RED = P.RED
GOLD = P.YELLOW
PURPLE = P.PURPLE

CODE_FONT = "Consolas"


class WhileLoopStory(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.title_screen()
        self.clear_stage()

        self.repetition_intro()
        self.clear_stage()

        self.show_code_example()
        self.show_loop_parts()
        self.setup_trace_view()
        self.run_trace()
        self.explain_stop()
        self.infinite_loop_warning()
        self.clear_stage()

        self.summary_slide()
        self.wait(1.5)

    def title_screen(self):
        title = Text("How does a while loop work?", font_size=40, color=TEXT, weight=BOLD)
        subtitle = Text("A worked example with step-by-step tracing", font_size=24, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.28)

        loop_icon = self.loop_icon(color=GREEN)
        loop_icon.scale(0.9)
        loop_icon.next_to(title, LEFT, buff=0.45)

        glow = Circle(radius=1.15, color=BLUE, stroke_width=0)
        glow.set_fill(BLUE, opacity=0.12)
        glow.move_to(title)

        self.play(FadeIn(glow), FadeIn(loop_icon, shift=UP * 0.08), FadeIn(title, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.06), run_time=0.75)
        self.wait(1.6)

    def repetition_intro(self):
        header = self.section_header("1. What a while loop does", "A while loop repeats code while a condition is true.")

        loop_icon = self.loop_icon(color=GREEN)
        loop_icon.scale(1.15)
        loop_icon.to_edge(LEFT, buff=0.9).shift(DOWN * 0.25)

        cards = VGroup(
            self.statement_card("A while loop repeats code", BLUE, {"repeats": GREEN}),
            self.statement_card("It keeps going while a condition is true", TEAL, {"while": GREEN, "condition": YELLOW, "true": GREEN}),
            self.statement_card("It stops when the condition becomes false", RED, {"stops": RED, "condition": YELLOW, "false": RED}),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        cards.next_to(header, DOWN, buff=0.55).shift(RIGHT * 0.55)

        loop_arrow = CurvedArrow(
            loop_icon.get_bottom() + DOWN * 0.15 + LEFT * 0.1,
            loop_icon.get_top() + UP * 0.15 + LEFT * 0.1,
            angle=PI / 1.35,
            color=GREEN,
            stroke_width=5,
        )

        self.play(FadeIn(header, shift=DOWN * 0.12), FadeIn(loop_icon, shift=RIGHT * 0.1), Create(loop_arrow), run_time=1.0)
        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.12), run_time=0.7)
            self.play(Indicate(card[1], color=card[0].get_stroke_color()), run_time=0.45)
        self.wait(0.9)

    def show_code_example(self):
        self.header = self.section_header("2. Our worked example", "We will trace this exact program line by line.")
        self.play(FadeIn(self.header, shift=DOWN * 0.12), run_time=0.75)

        self.code_group, self.code_lines = self.build_code_panel(
            width=6.5,
            height=3.9,
            scale=1.0,
        )
        self.code_group.move_to(ORIGIN)

        self.caption = self.caption_card(
            "Starting value first, then the condition is checked before every repeat.",
            BLUE,
            width=10.8,
        )
        self.caption.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(self.code_group, scale=0.96), FadeIn(self.caption, shift=UP * 0.08), run_time=0.9)

        focus = self.highlight_line(self.code_lines["start"], BLUE)
        self.play(Create(focus), run_time=0.5)
        self.play(Indicate(self.code_lines["start"], color=BLUE), run_time=0.5)
        self.update_caption("count = 1 sets the starting value.")

        self.play(Transform(focus, self.highlight_line(self.code_lines["condition"], GREEN)), run_time=0.5)
        self.play(Indicate(self.code_lines["condition"], color=GREEN), run_time=0.5)
        self.update_caption("while count <= 5: asks a question before the loop runs.")

        self.play(Transform(focus, self.highlight_line(self.code_lines["print"], TEAL)), run_time=0.5)
        self.play(Indicate(self.code_lines["print"], color=TEAL), run_time=0.5)
        self.update_caption("print(count) shows the current value.")

        self.play(Transform(focus, self.highlight_line(self.code_lines["update"], YELLOW)), run_time=0.5)
        self.play(Indicate(self.code_lines["update"], color=YELLOW), run_time=0.5)
        self.update_caption("count = count + 1 moves the loop toward stopping.")

        warning = Text("If count never changes, the loop could run forever.", font_size=22, color=RED)
        warning.next_to(self.caption, UP, buff=0.2)
        self.play(FadeIn(warning, shift=UP * 0.08), run_time=0.7)
        self.wait(0.8)

        self.code_focus = focus
        self.warning_note = warning

    def show_loop_parts(self):
        self.play(FadeOut(self.code_focus), run_time=0.25)
        self.play(
            self.code_group.animate.scale(0.92).shift(LEFT * 2.95 + UP * 0.15),
            self.caption.animate.scale(0.95).shift(LEFT * 0.95),
            self.warning_note.animate.scale(0.95).shift(LEFT * 0.95),
            run_time=0.9,
        )

        title = self.section_header("3. Break the loop into parts", "Starting value, condition, repeated code, and update.")
        title.to_edge(UP, buff=0.25)
        self.play(Transform(self.header, title), run_time=0.7)

        start_tag = self.callout_tag("Starting value", BLUE)
        start_tag.next_to(self.code_lines["start"], LEFT, buff=0.32)
        start_arrow = Arrow(start_tag.get_right(), self.code_lines["start"].get_left(), buff=0.08, color=BLUE, stroke_width=4)

        cond_tag = self.callout_tag("Condition", GREEN)
        cond_tag.next_to(self.code_lines["condition"], RIGHT, buff=0.36)
        cond_arrow = Arrow(self.code_lines["condition"].get_right(), cond_tag.get_left(), buff=0.08, color=GREEN, stroke_width=4)

        body_brace = Brace(VGroup(self.code_lines["print"], self.code_lines["update"]), RIGHT, color=TEAL)
        body_label = Text("Repeated code", font_size=20, color=TEAL, weight=BOLD)
        body_label.next_to(body_brace, RIGHT, buff=0.18)

        update_tag = self.callout_tag("Update", YELLOW)
        update_tag.next_to(self.code_lines["update"], LEFT, buff=0.32)
        update_arrow = Arrow(update_tag.get_right(), self.code_lines["update"].get_left(), buff=0.08, color=YELLOW, stroke_width=4)

        down_arrow = CurvedArrow(
            self.code_lines["condition"].get_bottom() + DOWN * 0.05,
            self.code_lines["print"].get_top() + UP * 0.05,
            angle=-PI / 2.3,
            color=GREEN,
            stroke_width=4,
        )
        return_arrow = CurvedArrow(
            self.code_lines["update"].get_right() + RIGHT * 0.1,
            self.code_lines["condition"].get_right() + RIGHT * 0.1,
            angle=PI / 2.1,
            color=YELLOW,
            stroke_width=4,
        )

        self.play(
            FadeIn(start_tag, shift=LEFT * 0.1),
            GrowArrow(start_arrow),
            FadeIn(cond_tag, shift=RIGHT * 0.1),
            GrowArrow(cond_arrow),
            Create(body_brace),
            FadeIn(body_label, shift=RIGHT * 0.08),
            FadeIn(update_tag, shift=LEFT * 0.1),
            GrowArrow(update_arrow),
            Create(down_arrow),
            Create(return_arrow),
            run_time=1.2,
        )
        self.play(Indicate(body_brace, color=TEAL), Indicate(update_tag, color=YELLOW), run_time=0.8)

        self.return_arrow = return_arrow
        self.loop_structure = VGroup(start_tag, start_arrow, cond_tag, cond_arrow, body_brace, body_label, update_tag, update_arrow, down_arrow, return_arrow)
        self.wait(0.8)

    def setup_trace_view(self):
        self.trace_title = self.section_header("4. Trace the program", "Follow the values as the loop repeats.")
        self.trace_title.to_edge(UP, buff=0.23)
        self.play(Transform(self.header, self.trace_title), run_time=0.7)

        self.trace_panel = self.build_trace_panel()
        self.trace_panel["panel"].to_edge(RIGHT, buff=0.45).shift(DOWN * 0.28)
        self.trace_panel["panel"].shift(LEFT * 0.15)

        self.count_chip = self.count_box(1)
        self.count_chip.next_to(self.trace_panel["check"], UP, buff=0.22).align_to(self.trace_panel["check"], LEFT)

        self.play(FadeIn(self.trace_panel["panel"], shift=LEFT * 0.08), FadeIn(self.count_chip, shift=UP * 0.05), run_time=1.0)

        self.check_text = self.trace_panel["check_text"]
        self.check_result = self.trace_panel["check_result"]
        self.console_line = None
        self.trace_rows = []
        self.focus_highlight = self.highlight_line(self.code_lines["condition"], BLUE)
        self.play(Create(self.focus_highlight), run_time=0.45)

    def run_trace(self):
        iterations = [
            (1, True, 1, 2, "1"),
            (2, True, 2, 3, "2"),
            (3, True, 3, 4, "3"),
            (4, True, 4, 5, "4"),
            (5, True, 5, 6, "5"),
            (6, False, 6, 6, "none"),
        ]

        for step, is_true, current_count, next_count, output in iterations:
            count_target = self.count_box(current_count)
            count_target.move_to(self.count_chip)
            self.play(Transform(self.count_chip, count_target), run_time=0.45)

            expr = self.check_expression(current_count)
            expr.move_to(self.check_text)
            self.play(Transform(self.check_text, expr), run_time=0.45)

            badge = self.truth_badge(is_true)
            badge.move_to(self.check_result)
            self.play(Transform(self.check_result, badge), run_time=0.4)

            self.play(Transform(self.focus_highlight, self.highlight_line(self.code_lines["condition"], BLUE)), run_time=0.35)
            self.play(Indicate(self.code_lines["condition"], color=BLUE), run_time=0.45)

            if is_true:
                self.play(Transform(self.focus_highlight, self.highlight_line(self.code_lines["print"], TEAL)), run_time=0.35)
                self.play(Indicate(self.code_lines["print"], color=TEAL), run_time=0.45)

                self.play(Transform(self.focus_highlight, self.highlight_line(self.code_lines["update"], YELLOW)), run_time=0.35)
                self.play(Indicate(self.code_lines["update"], color=YELLOW), run_time=0.45)

                output_line = self.output_line(output)
                if self.console_line is None:
                    output_line.move_to(self.trace_panel["console"].get_center() + LEFT * 1.8)
                    self.console_line = output_line
                    self.play(FadeIn(output_line, shift=RIGHT * 0.08), run_time=0.35)
                else:
                    output_line.move_to(self.console_line)
                    self.play(Transform(self.console_line, output_line), run_time=0.35)

                row = self.trace_row(step, current_count, True, output)
                row.move_to(self.trace_row_position(step))
                self.trace_rows.append(row)
                self.play(FadeIn(row, shift=UP * 0.06), run_time=0.45)

                next_count_target = self.count_box(next_count)
                next_count_target.move_to(self.count_chip)
                self.play(Transform(self.count_chip, next_count_target), run_time=0.4)
                self.play(Indicate(self.return_arrow, color=YELLOW), run_time=0.35)
            else:
                self.play(Indicate(self.code_lines["condition"], color=RED), run_time=0.35)
                row = self.trace_row(step, current_count, False, "none")
                row.move_to(self.trace_row_position(step))
                self.trace_rows.append(row)
                self.play(FadeIn(row, shift=UP * 0.06), run_time=0.45)

    def explain_stop(self):
        stop_box = RoundedRectangle(width=6.2, height=1.45, corner_radius=0.18, color=RED, stroke_width=2.4)
        stop_box.set_fill(SURFACE, opacity=1)
        stop_box.to_edge(LEFT, buff=0.55).shift(DOWN * 0.95)

        line1 = Text("The loop stops because the condition is false.", font_size=24, color=TEXT)
        line2 = Text("count became 6, and 6 is not less than or equal to 5.", font_size=22, color=MUTED)
        VGroup(line1, line2).arrange(DOWN, buff=0.12)
        VGroup(line1, line2).move_to(stop_box)

        false_tag = self.truth_badge(False)
        false_tag.next_to(stop_box, RIGHT, buff=0.35)

        self.play(FadeIn(stop_box, shift=UP * 0.08), FadeIn(false_tag, shift=UP * 0.08), run_time=0.8)
        self.play(Write(line1), run_time=0.9)
        self.play(Write(line2), run_time=0.95)
        self.wait(0.9)

    def infinite_loop_warning(self):
        title = self.section_header("5. What happens if you forget the update?", "The condition never changes, so the loop never reaches false.")
        title.to_edge(UP, buff=0.24)
        self.play(Transform(self.header, title), run_time=0.7)

        wrong_code_group, wrong_lines = self.build_code_panel(
            width=5.2,
            height=2.9,
            scale=0.92,
            wrong_version=True,
        )
        wrong_code_group.to_edge(LEFT, buff=0.8).shift(DOWN * 0.35)

        warning = self.warning_card(
            "count never changes, so the condition stays true forever.",
            RED,
            width=5.45,
        )
        warning.next_to(wrong_code_group, RIGHT, buff=0.55).shift(UP * 0.1)

        loop = self.loop_icon(color=RED)
        loop.scale(1.35)
        loop.next_to(warning, DOWN, buff=0.3)

        self.play(FadeIn(wrong_code_group, shift=RIGHT * 0.08), run_time=0.8)
        self.play(FadeIn(warning, shift=UP * 0.08), run_time=0.8)
        self.play(Create(loop), run_time=0.65)
        self.play(Indicate(wrong_lines["condition"], color=RED), run_time=0.8)
        self.play(Indicate(wrong_lines["print"], color=RED), run_time=0.7)
        self.play(Flash(loop.get_center(), color=RED, flash_radius=0.55), run_time=0.7)
        self.wait(0.8)

    def summary_slide(self):
        title = self.section_header("6. Summary", "Keep asking: should the loop go again?")
        title.to_edge(UP, buff=0.25)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.7)

        cards = VGroup(
            self.summary_card("A while loop repeats while a condition is true", GREEN),
            self.summary_card("The condition is checked before each repeat", BLUE),
            self.summary_card("The variable usually changes inside the loop", YELLOW),
            self.summary_card("The loop stops when the condition becomes false", RED),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        cards.move_to(ORIGIN + DOWN * 0.1)

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.12), run_time=1.2)

        takeaway = RoundedRectangle(width=8.6, height=0.78, corner_radius=0.16, color=PURPLE, stroke_width=2)
        takeaway.set_fill(SURFACE, opacity=1)
        takeaway.to_edge(DOWN, buff=0.35)
        takeaway_text = Text('A while loop keeps asking: "Should I go again?"', font_size=24, color=TEXT)
        takeaway_text.move_to(takeaway)
        self.play(FadeIn(takeaway, shift=UP * 0.08), Write(takeaway_text), run_time=1.0)

        compare = Text("Small condition changes matter: <= 5 runs 5 times, < 5 runs 4 times.", font_size=20, color=MUTED)
        compare.next_to(takeaway, UP, buff=0.18)
        self.play(FadeIn(compare, shift=UP * 0.08), run_time=0.75)

    def clear_stage(self):
        if not self.mobjects:
            return
        mobs = list(self.mobjects)
        self.play(*[FadeOut(mob, shift=DOWN * 0.08) for mob in mobs], run_time=0.6)
        self.clear()

    def update_caption(self, text):
        new_caption = self.caption_card(text, BLUE, width=10.8)
        new_caption.to_edge(DOWN, buff=0.35)
        self.play(Transform(self.caption, new_caption), run_time=0.5)
        self.caption = new_caption

    def section_header(self, title_text, subtitle_text):
        title = Text(title_text, font_size=32, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=BLUE, stroke_width=3).next_to(title, DOWN, buff=0.15)
        subtitle = Text(subtitle_text, font_size=20, color=MUTED)
        subtitle.next_to(line, DOWN, buff=0.15)
        return VGroup(title, line, subtitle)

    def statement_card(self, text, accent, t2c_map):
        card = RoundedRectangle(width=11.0, height=0.72, corner_radius=0.16, color=accent, stroke_width=2)
        card.set_fill(SURFACE, opacity=0.96)
        label = Text(text, font_size=23, color=TEXT, t2c=t2c_map)
        label.move_to(card)
        return VGroup(card, label)

    def caption_card(self, text, accent, width=10.0):
        card = RoundedRectangle(width=width, height=0.78, corner_radius=0.16, color=accent, stroke_width=2)
        card.set_fill(SURFACE, opacity=0.96)
        label = Text(text, font_size=21, color=TEXT)
        label.move_to(card)
        return VGroup(card, label)

    def warning_card(self, text, accent, width=5.8):
        card = RoundedRectangle(width=width, height=1.0, corner_radius=0.16, color=accent, stroke_width=2.2)
        card.set_fill(SURFACE, opacity=0.98)
        label = Text(text, font_size=21, color=TEXT)
        label.move_to(card)
        return VGroup(card, label)

    def callout_tag(self, text, color):
        label = Text(text, font_size=19, color=color, weight=BOLD)
        box = RoundedRectangle(width=label.width + 0.4, height=0.46, corner_radius=0.12, color=color, stroke_width=1.8)
        box.set_fill(BACKGROUND, opacity=1)
        label.move_to(box)
        return VGroup(box, label)

    def loop_icon(self, color):
        arc1 = CurvedArrow(LEFT * 0.35 + DOWN * 0.12, RIGHT * 0.35 + UP * 0.12, angle=TAU / 2.6, color=color, stroke_width=5)
        arc2 = CurvedArrow(RIGHT * 0.35 + UP * 0.12, LEFT * 0.35 + DOWN * 0.12, angle=TAU / 2.6, color=color, stroke_width=5)
        dot = Dot(radius=0.06, color=color)
        return VGroup(arc1, arc2, dot)

    def build_code_panel(self, width, height, scale=1.0, wrong_version=False):
        panel = RoundedRectangle(width=width, height=height, corner_radius=0.18, color=P.BORDER, stroke_width=2.2)
        panel.set_fill(SURFACE, opacity=0.98)

        title = Text("Python", font_size=18, color=MUTED, weight=BOLD)
        title.next_to(panel.get_top(), DOWN, buff=0.16)
        title.align_to(panel, LEFT).shift(RIGHT * 0.28)

        if wrong_version:
            specs = [
                ("count = 1", {"count": TEAL, "1": YELLOW}, "start"),
                ("", {}, "blank"),
                ("while count <= 5:", {"while": BLUE, "count": TEAL, "<=": YELLOW, "5": YELLOW}, "condition"),
                ("    print(count)", {"print": TEAL, "count": TEAL}, "print"),
            ]
        else:
            specs = [
                ("count = 1", {"count": TEAL, "1": YELLOW}, "start"),
                ("", {}, "blank"),
                ("while count <= 5:", {"while": BLUE, "count": TEAL, "<=": YELLOW, "5": YELLOW}, "condition"),
                ("    print(count)", {"print": TEAL, "count": TEAL}, "print"),
                ("    count = count + 1", {"count": TEAL, "+": YELLOW, "1": YELLOW}, "update"),
            ]

        lines = VGroup()
        refs = {}
        for text, t2c_map, key in specs:
            if text == "":
                line = Text(" ", font=CODE_FONT, font_size=28, color=TEXT)
                line.set_opacity(0.0)
            else:
                line = Text(text, font=CODE_FONT, font_size=28, color=TEXT, t2c=t2c_map)
            line.set_z_index(2)
            lines.add(line)
            if key != "blank":
                refs[key] = line

        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lines.next_to(title, DOWN, buff=0.28).align_to(panel, LEFT).shift(RIGHT * 0.34)

        bg = VGroup(panel, title, lines)
        bg.scale(scale)
        return bg, refs

    def highlight_line(self, line, color):
        box = SurroundingRectangle(line, color=color, buff=0.08, corner_radius=0.08, stroke_width=3)
        box.set_fill(color, opacity=0.14)
        return box

    def build_trace_panel(self):
        panel = RoundedRectangle(width=6.1, height=5.55, corner_radius=0.18, color=P.BORDER, stroke_width=2.2)
        panel.set_fill(SURFACE, opacity=0.98)

        title = Text("Trace table", font_size=20, color=TEXT, weight=BOLD)
        title.next_to(panel.get_top(), DOWN, buff=0.12)
        title.align_to(panel, LEFT).shift(RIGHT * 0.24)

        chip = RoundedRectangle(width=2.45, height=0.55, corner_radius=0.14, color=BLUE, stroke_width=1.8)
        chip.set_fill(BLUE, opacity=0.15)
        chip_label = Text("Current count", font_size=18, color=BLUE, weight=BOLD)
        chip_label.move_to(chip)
        chip_group = VGroup(chip, chip_label)
        chip_group.next_to(title, DOWN, buff=0.15).align_to(panel, LEFT).shift(RIGHT * 0.24)

        check_box = RoundedRectangle(width=5.55, height=0.72, corner_radius=0.14, color=GREEN, stroke_width=1.8)
        check_box.set_fill(SURFACE_ALT, opacity=0.95)
        check_label = Text("Check:", font_size=18, color=MUTED, weight=BOLD)
        check_expr = Text("1 <= 5", font=CODE_FONT, font_size=21, color=TEXT, t2c={"1": BLUE, "<=": YELLOW, "5": YELLOW})
        check_result = self.truth_badge(True)
        check_label.move_to(check_box.get_left() + RIGHT * 0.48)
        check_expr.next_to(check_label, RIGHT, buff=0.18)
        check_result.move_to(check_box.get_right() + LEFT * 0.78)
        check_group = VGroup(check_box, check_label, check_expr, check_result)
        check_group.next_to(chip_group, DOWN, buff=0.15).align_to(panel, LEFT).shift(RIGHT * 0.24)

        header_y = check_group.get_bottom()[1] - 0.3
        table_frame = RoundedRectangle(width=5.55, height=2.65, corner_radius=0.12, color=P.BORDER, stroke_width=1.8)
        table_frame.set_fill(BACKGROUND, opacity=0.35)
        table_frame.move_to(np.array([panel.get_center()[0], header_y - 1.02, 0]))

        headers = VGroup(
            Text("Step", font_size=18, color=TEXT, weight=BOLD),
            Text("count", font_size=18, color=TEXT, weight=BOLD),
            Text("Condition", font_size=18, color=TEXT, weight=BOLD),
            Text("Output", font_size=18, color=TEXT, weight=BOLD),
        )
        headers[0].move_to(table_frame.get_top() + DOWN * 0.28 + LEFT * 2.35)
        headers[1].move_to(table_frame.get_top() + DOWN * 0.28 + LEFT * 1.22)
        headers[2].move_to(table_frame.get_top() + DOWN * 0.28 + RIGHT * 0.25)
        headers[3].move_to(table_frame.get_top() + DOWN * 0.28 + RIGHT * 2.0)

        sep1 = Line(table_frame.get_top() + DOWN * 0.08 + LEFT * 1.75, table_frame.get_bottom() + UP * 0.08 + LEFT * 1.75, color=P.BORDER, stroke_opacity=0.55)
        sep2 = Line(table_frame.get_top() + DOWN * 0.08 + LEFT * 0.55, table_frame.get_bottom() + UP * 0.08 + LEFT * 0.55, color=P.BORDER, stroke_opacity=0.55)
        sep3 = Line(table_frame.get_top() + DOWN * 0.08 + RIGHT * 1.25, table_frame.get_bottom() + UP * 0.08 + RIGHT * 1.25, color=P.BORDER, stroke_opacity=0.55)
        separators = VGroup(sep1, sep2, sep3)

        console = RoundedRectangle(width=5.55, height=1.55, corner_radius=0.12, color=TEAL, stroke_width=1.8)
        console.set_fill(SURFACE_ALT, opacity=0.96)
        console.next_to(table_frame, DOWN, buff=0.18)

        console_title = Text("Output", font_size=18, color=TEAL, weight=BOLD)
        console_title.next_to(console.get_top(), DOWN, buff=0.12)
        console_title.align_to(console, LEFT).shift(RIGHT * 0.24)

        panel_group = VGroup(panel, title, chip_group, check_group, table_frame, headers, separators, console, console_title)
        return {
            "panel": panel_group,
            "headers": headers,
            "table_frame": VGroup(table_frame, separators),
            "check": check_group,
            "check_text": check_expr,
            "check_result": check_result,
            "console": console,
            "console_title": console_title,
            "panel_bg": panel,
            "chip": chip_group,
        }

    def trace_row_position(self, step):
        top_y = self.trace_panel["table_frame"][0].get_top()[1] - 0.43
        return np.array([self.trace_panel["table_frame"][0].get_center()[0], top_y - 0.37 * (step - 1), 0])

    def trace_row(self, step, count, condition, output):
        color = GREEN if condition else RED
        row = RoundedRectangle(width=5.42, height=0.35, corner_radius=0.08, color=color, stroke_width=1.3)
        row.set_fill(color, opacity=0.1 if condition else 0.08)

        cells = VGroup(
            Text(str(step), font_size=16, color=TEXT, weight=BOLD),
            Integer(count, font_size=16, color=TEAL if condition else RED),
            Text("True" if condition else "False", font_size=16, color=GREEN if condition else RED, weight=BOLD),
            Text(output, font=CODE_FONT, font_size=16, color=TEXT if output != "none" else MUTED),
        )
        cells[0].move_to(row.get_left() + RIGHT * 0.35)
        cells[1].move_to(row.get_left() + RIGHT * 1.5)
        cells[2].move_to(row.get_left() + RIGHT * 2.95)
        cells[3].move_to(row.get_left() + RIGHT * 4.55)
        return VGroup(row, cells)

    def output_line(self, text):
        line = Text(text, font=CODE_FONT, font_size=18, color=TEXT)
        return line

    def count_box(self, count):
        box = RoundedRectangle(width=2.4, height=0.62, corner_radius=0.14, color=BLUE, stroke_width=1.8)
        box.set_fill(BLUE, opacity=0.14)
        label = Text("count =", font_size=18, color=BLUE, weight=BOLD)
        value = Integer(count, font_size=22, color=YELLOW)
        label.move_to(box.get_left() + RIGHT * 0.65)
        value.move_to(box.get_right() + LEFT * 0.45)
        return VGroup(box, label, value)

    def check_expression(self, count):
        return Text(f"{count} <= 5", font=CODE_FONT, font_size=21, color=TEXT, t2c={str(count): BLUE, "<=": YELLOW, "5": YELLOW})

    def truth_badge(self, truth):
        color = GREEN if truth else RED
        text = "True" if truth else "False"
        box = RoundedRectangle(width=1.0, height=0.42, corner_radius=0.12, color=color, stroke_width=1.6)
        box.set_fill(color, opacity=0.18)
        label = Text(text, font_size=16, color=color, weight=BOLD)
        label.move_to(box)
        return VGroup(box, label)

    def loop_return_arrow(self):
        return CurvedArrow(
            self.code_lines["update"].get_right() + RIGHT * 0.14,
            self.code_lines["condition"].get_right() + RIGHT * 0.14,
            angle=PI / 1.8,
            color=YELLOW,
            stroke_width=4,
        )

    def summary_card(self, text, accent):
        card = RoundedRectangle(width=11.0, height=0.72, corner_radius=0.16, color=accent, stroke_width=2)
        card.set_fill(SURFACE, opacity=0.96)
        label = Text(text, font_size=22, color=TEXT)
        label.move_to(card)
        return VGroup(card, label)


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        "-p",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "WhileLoopStory",
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
