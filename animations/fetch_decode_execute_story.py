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

P = apply_palette("Sepia")
BACKGROUND = P.BG_0
SURFACE = P.BG_1
SURFACE_ALT = P.BG_2
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY
FAINT = P.TEXT_FAINT
FETCH = P.BLUE
DECODE = P.AMBER
EXECUTE = P.GREEN
MEMORY = P.PURPLE
CPU = P.CYAN
TEA = P.TEAL
WARN = P.YELLOW

CODE_FONT = "Consolas"


class FetchDecodeExecuteStory(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.title_section()
        self.clear_stage()

        self.stage_intro()
        self.clear_stage()

        self.tea_analogy()
        self.clear_stage()

        self.cpu_link()
        self.clear_stage()

        self.fetch_section()
        self.clear_stage()

        self.decode_section()
        self.clear_stage()

        self.execute_section()
        self.clear_stage()

        self.cycle_repeat_section()
        self.clear_stage()

        self.summary_section()
        self.wait(1.4)

    def title_section(self):
        title = Text("The Fetch-Decode-Execute Cycle", font_size=40, color=TEXT, weight=BOLD)
        subtitle = Text("How the CPU runs instructions", font_size=24, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.2)

        question = self.caption_card("How does a computer know what to do next?", FETCH, width=8.8)
        question.to_edge(DOWN, buff=0.45)

        glow = Circle(radius=1.25, color=FETCH, stroke_width=0)
        glow.set_fill(FETCH, opacity=0.1)
        glow.move_to(title)

        self.play(FadeIn(glow), FadeIn(title, shift=UP * 0.08), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.06), run_time=0.6)
        self.play(FadeIn(question, shift=UP * 0.05), run_time=0.65)
        self.wait(1.1)

    def stage_intro(self):
        header = self.section_header("1. Three simple stages", "The CPU follows the same pattern again and again.", FETCH)

        columns = self.stage_triplet()
        columns.scale(0.98)
        columns.move_to(ORIGIN + DOWN * 0.1)

        loop = CurvedArrow(
            columns[2][0].get_top() + UP * 0.12,
            columns[0][0].get_top() + UP * 0.12,
            angle=PI / 1.55,
            color=EXECUTE,
            stroke_width=4,
        )

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        for idx, color in enumerate([FETCH, DECODE, EXECUTE]):
            self.play(FadeIn(columns[idx], shift=UP * 0.06), run_time=0.55)
            self.play(Indicate(columns[idx][0], color=color), run_time=0.35)
        self.play(Create(loop), run_time=0.65)

        recap = self.caption_card("Fetch, Decode, Execute. Then it starts again.", EXECUTE, width=8.9)
        recap.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(recap, shift=UP * 0.05), run_time=0.55)
        self.wait(0.9)

    def tea_analogy(self):
        header = self.section_header("2. A real-world example", "Think about making a cup of tea.", TEA)
        chips = self.stage_triplet()
        chips.scale(0.82)
        chips.to_edge(UP, buff=1.05)

        robot = self.robot_icon()
        robot.scale(0.85)
        robot.move_to(LEFT * 4.55 + DOWN * 0.55)

        list_panel, rows = self.tea_list_panel()
        list_panel.scale(0.94)
        list_panel.move_to(RIGHT * 2.8 + UP * 0.15)

        kettle = self.prop_box("Kettle", FETCH, width=1.55, height=0.84)
        kettle.move_to(LEFT * 2.2 + DOWN * 2.25)
        mug = self.prop_box("Mug", EXECUTE, width=1.55, height=0.84)
        mug.move_to(LEFT * 0.15 + DOWN * 2.25)
        tea_bag = self.prop_box("Tea bag", DECODE, width=1.4, height=0.72)
        tea_bag.move_to(RIGHT * 1.95 + DOWN * 2.25)

        steam = self.steam_lines(kettle)
        steam.set_opacity(0.0)

        fetch_caption = self.caption_card("Fetch: get the next instruction.", FETCH, width=7.8)
        fetch_caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(
            LaggedStart(
                FadeIn(chips[0], shift=UP * 0.05),
                FadeIn(chips[1], shift=UP * 0.05),
                FadeIn(chips[2], shift=UP * 0.05),
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )
        self.play(FadeIn(robot, shift=LEFT * 0.08), FadeIn(list_panel, shift=RIGHT * 0.08), run_time=0.9)
        self.play(FadeIn(kettle, shift=UP * 0.05), FadeIn(mug, shift=UP * 0.05), FadeIn(tea_bag, shift=UP * 0.05), run_time=0.7)
        self.play(FadeIn(fetch_caption, shift=UP * 0.05), run_time=0.55)

        first_row = rows[0]
        first_highlight = self.highlight_box(first_row, FETCH)
        fetch_arrow = Arrow(first_row.get_left(), robot.get_right(), buff=0.12, color=FETCH, stroke_width=4)
        fetch_arrow.shift(UP * 0.14)

        self.play(Create(first_highlight), GrowArrow(fetch_arrow), run_time=0.7)
        self.play(Indicate(chips[0][0], color=FETCH), run_time=0.35)
        self.wait(0.45)

        self.play(FadeOut(VGroup(first_highlight, fetch_arrow)), run_time=0.35)
        decode_caption = self.caption_card("Decode: work out what it means.", DECODE, width=7.9)
        decode_caption.move_to(fetch_caption)
        self.play(Transform(fetch_caption, decode_caption), run_time=0.45)
        self.play(Indicate(chips[1][0], color=DECODE), run_time=0.35)
        self.play(Indicate(first_row, color=FETCH), run_time=0.35)
        self.wait(0.35)

        execute_caption = self.caption_card("Execute: do the action.", EXECUTE, width=7.3)
        execute_caption.move_to(fetch_caption)
        self.play(Transform(fetch_caption, execute_caption), run_time=0.45)
        self.play(Indicate(chips[2][0], color=EXECUTE), run_time=0.35)
        self.play(Indicate(kettle, color=FETCH), run_time=0.45)
        self.play(
            steam.animate.set_opacity(1.0),
            kettle[0].animate.set_fill(FETCH, opacity=0.22),
            run_time=0.55,
        )
        self.play(LaggedStart(*[Create(line) for line in steam], lag_ratio=0.08), run_time=0.65)
        self.wait(0.5)

        second_highlight = self.highlight_box(rows[1], DECODE)
        tea_arrow = Arrow(rows[1].get_left(), tea_bag.get_top(), buff=0.12, color=DECODE, stroke_width=4)
        tea_arrow.shift(LEFT * 0.15)
        self.play(Transform(first_highlight, second_highlight), Transform(fetch_arrow, tea_arrow), run_time=0.6)
        self.play(Indicate(rows[1], color=DECODE), run_time=0.4)
        self.play(tea_bag.animate.move_to(mug.get_center() + UP * 0.45), run_time=0.75)
        self.play(Indicate(mug, color=EXECUTE), run_time=0.45)
        self.play(FadeOut(VGroup(first_highlight, fetch_arrow, steam)), run_time=0.35)

        repeat = self.caption_card("Then the same steps happen again for the next instruction.", TEA, width=10.2)
        repeat.to_edge(DOWN, buff=0.42)
        self.play(Transform(fetch_caption, repeat), run_time=0.5)
        self.wait(1.0)

    def cpu_link(self):
        header = self.section_header("3. Now link it to the CPU", "A program is a list of instructions stored in memory.", CPU)

        memory_panel, memory_rows, pc_chip = self.memory_panel(
            ["LOAD 3", "ADD 5", "STORE 8"],
            pc_index=0,
        )
        memory_panel.to_edge(LEFT, buff=0.55).shift(DOWN * 0.2)

        cpu_panel, ir_box, value_box = self.cpu_panel("...", 0)
        cpu_panel.to_edge(RIGHT, buff=0.55).shift(DOWN * 0.2)

        arrow = Arrow(memory_rows[0].get_right(), ir_box.get_left(), buff=0.12, color=FETCH, stroke_width=4)
        arrow.shift(UP * 0.05)
        caption = self.caption_card("The CPU goes through them one at a time.", FETCH, width=8.8)
        caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(FadeIn(memory_panel, shift=LEFT * 0.08), FadeIn(cpu_panel, shift=RIGHT * 0.08), run_time=0.9)
        self.play(GrowArrow(arrow), run_time=0.55)
        self.play(FadeIn(pc_chip, shift=UP * 0.05), run_time=0.5)
        self.play(Indicate(memory_rows[0], color=FETCH), run_time=0.4)
        self.play(FadeIn(caption, shift=UP * 0.05), run_time=0.55)
        self.wait(0.9)

    def fetch_section(self):
        header = self.section_header("4. Fetch", "Fetch means get the next instruction.", FETCH)

        memory_panel, memory_rows, pc_chip = self.memory_panel(
            ["LOAD 3", "ADD 5", "STORE 8"],
            pc_index=0,
        )
        memory_panel.to_edge(LEFT, buff=0.55).shift(DOWN * 0.16)

        cpu_panel, ir_box, value_box = self.cpu_panel("...", 0)
        cpu_panel.to_edge(RIGHT, buff=0.55).shift(DOWN * 0.16)

        arrow = Arrow(memory_rows[0].get_right(), ir_box.get_left(), buff=0.12, color=FETCH, stroke_width=4)
        arrow.shift(UP * 0.05)

        caption = self.caption_card("The CPU looks in memory, then copies the instruction into the CPU.", FETCH, width=10.2)
        caption.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(FadeIn(memory_panel, shift=LEFT * 0.08), FadeIn(cpu_panel, shift=RIGHT * 0.08), run_time=0.9)
        self.play(FadeIn(pc_chip, shift=UP * 0.05), run_time=0.45)
        self.play(Create(self.highlight_box(memory_rows[0], FETCH)), run_time=0.45)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeOut(ir_box[1]), run_time=0.2)
        fetched = Text("LOAD 3", font=CODE_FONT, font_size=20, color=TEXT, t2c=self.instruction_colors("LOAD 3"))
        fetched.move_to(ir_box[0].get_center())
        self.play(TransformFromCopy(memory_rows[0], fetched), run_time=0.75)
        self.play(Transform(pc_chip, self.pc_chip("PC = 2", FETCH)), run_time=0.55)
        self.play(FadeIn(caption, shift=UP * 0.05), run_time=0.55)
        self.wait(0.9)

    def decode_section(self):
        header = self.section_header("5. Decode", "Decode means understand the instruction.", DECODE)

        cpu_panel, ir_box, value_box = self.cpu_panel("ADD 5", 3, stage_color=DECODE)
        cpu_panel.scale(1.02)
        cpu_panel.move_to(ORIGIN + DOWN * 0.05)

        meaning = self.meaning_box("Add 5 to the current value.", DECODE, width=5.7)
        meaning.next_to(cpu_panel, DOWN, buff=0.35)

        arrow = Arrow(ir_box.get_bottom(), meaning.get_top(), buff=0.12, color=DECODE, stroke_width=4)

        caption = self.caption_card("The CPU works out what the words mean.", DECODE, width=8.8)
        caption.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(FadeIn(cpu_panel, shift=UP * 0.08), run_time=0.85)
        self.play(Indicate(ir_box, color=DECODE), run_time=0.45)
        self.play(GrowArrow(arrow), FadeIn(meaning, shift=UP * 0.05), run_time=0.8)
        self.play(Transform(caption, self.caption_card("Decode means understand the instruction.", DECODE, width=8.8)), run_time=0.45)
        self.play(Indicate(meaning[1], color=DECODE), run_time=0.45)
        self.wait(0.9)

    def execute_section(self):
        header = self.section_header("6. Execute", "Execute means do the job.", EXECUTE)

        cpu_panel, ir_box, value_box = self.cpu_panel("ADD 5", 3, stage_color=EXECUTE)
        cpu_panel.scale(1.02)
        cpu_panel.move_to(ORIGIN + DOWN * 0.05)

        eq_left = self.value_equation("3", "5", "8", EXECUTE)
        eq_left.next_to(cpu_panel, DOWN, buff=0.35)

        caption = self.caption_card("The CPU carries out the instruction and the value changes.", EXECUTE, width=10.2)
        caption.to_edge(DOWN, buff=0.38)
        arrow = Arrow(eq_left.get_left(), eq_left.get_right(), buff=0.12, color=EXECUTE, stroke_width=4)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(FadeIn(cpu_panel, shift=UP * 0.08), run_time=0.85)
        self.play(Indicate(value_box, color=EXECUTE), run_time=0.4)
        self.play(FadeIn(eq_left, shift=UP * 0.05), GrowArrow(arrow), run_time=0.8)
        self.play(Transform(value_box[1], Integer(8, font_size=24, color=EXECUTE)), run_time=0.7)
        self.play(Indicate(value_box[1], color=EXECUTE), run_time=0.45)
        self.play(FadeIn(caption, shift=UP * 0.05), run_time=0.55)
        self.wait(0.9)

    def cycle_repeat_section(self):
        header = self.section_header("7. The cycle repeats", "Fetch -> Decode -> Execute -> Repeat.", FETCH)

        stage_boxes = self.cycle_boxes()
        stage_boxes.to_edge(UP, buff=1.25)

        loop = CurvedArrow(
            stage_boxes[2].get_top() + UP * 0.1,
            stage_boxes[0].get_top() + UP * 0.1,
            angle=PI / 1.45,
            color=EXECUTE,
            stroke_width=4,
        )

        value_box = self.value_readout(0)
        value_box.next_to(stage_boxes, RIGHT, buff=0.6).shift(DOWN * 0.15)

        memory_box = self.memory_write_box("Memory", 0)
        memory_box.next_to(value_box, DOWN, buff=0.45)

        caption = self.caption_card("The CPU can do this millions or billions of times every second.", TEA, width=10.6)
        caption.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(FadeIn(stage_boxes, shift=UP * 0.05), Create(loop), run_time=0.85)
        self.play(FadeIn(value_box), FadeIn(memory_box), run_time=0.65)

        first = self.instruction_token("LOAD 3", FETCH)
        first.move_to(DOWN * 2.1 + LEFT * 0.2)
        self.play(FadeIn(first, shift=UP * 0.05), run_time=0.45)
        self.play(first.animate.move_to(stage_boxes[0].get_center()), Indicate(stage_boxes[0], color=FETCH), run_time=0.55)
        self.play(first.animate.move_to(stage_boxes[1].get_center()), Indicate(stage_boxes[1], color=DECODE), run_time=0.55)
        self.play(
            first.animate.move_to(stage_boxes[2].get_center()),
            Indicate(stage_boxes[2], color=EXECUTE),
            Transform(value_box[1], Integer(3, font_size=24, color=EXECUTE)),
            run_time=0.65,
        )
        self.play(FadeOut(first), run_time=0.25)

        second = self.instruction_token("ADD 5", DECODE)
        second.move_to(DOWN * 2.1 + LEFT * 0.2)
        self.play(FadeIn(second, shift=UP * 0.05), run_time=0.45)
        self.play(second.animate.move_to(stage_boxes[0].get_center()), Indicate(stage_boxes[0], color=FETCH), run_time=0.55)
        self.play(second.animate.move_to(stage_boxes[1].get_center()), Indicate(stage_boxes[1], color=DECODE), run_time=0.55)
        self.play(
            second.animate.move_to(stage_boxes[2].get_center()),
            Indicate(stage_boxes[2], color=EXECUTE),
            Transform(value_box[1], Integer(8, font_size=24, color=EXECUTE)),
            run_time=0.65,
        )
        self.play(FadeOut(second), run_time=0.25)

        third = self.instruction_token("STORE 8", EXECUTE)
        third.move_to(DOWN * 2.1 + LEFT * 0.2)
        self.play(FadeIn(third, shift=UP * 0.05), run_time=0.45)
        self.play(third.animate.move_to(stage_boxes[0].get_center()), Indicate(stage_boxes[0], color=FETCH), run_time=0.55)
        self.play(third.animate.move_to(stage_boxes[1].get_center()), Indicate(stage_boxes[1], color=DECODE), run_time=0.55)
        self.play(
            third.animate.move_to(stage_boxes[2].get_center()),
            Indicate(stage_boxes[2], color=EXECUTE),
            GrowArrow(Arrow(value_box.get_bottom(), memory_box.get_top(), buff=0.12, color=EXECUTE, stroke_width=4)),
            run_time=0.7,
        )
        self.play(FadeOut(third), run_time=0.25)

        self.play(FadeIn(caption, shift=UP * 0.05), run_time=0.55)
        self.wait(1.1)

    def summary_section(self):
        header = self.section_header("8. Quick recap", "Keep the three words in order.", FETCH)

        cards = VGroup(
            self.summary_card("Fetch", "Get the instruction from memory.", FETCH),
            self.summary_card("Decode", "Understand what it means.", DECODE),
            self.summary_card("Execute", "Do the job.", EXECUTE),
        ).arrange(RIGHT, buff=0.35)
        cards.move_to(ORIGIN + UP * 0.1)

        takeaway = self.caption_card("The CPU repeats this cycle over and over to run programs.", TEA, width=10.8)
        takeaway.to_edge(DOWN, buff=0.4)

        ending = Text("Without the FDE cycle, a computer would not know what to do next.", font_size=22, color=MUTED)
        ending.next_to(takeaway, UP, buff=0.18)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.06) for card in cards], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(takeaway, shift=UP * 0.05), run_time=0.55)
        self.play(FadeIn(ending, shift=UP * 0.05), run_time=0.45)
        self.play(
            Indicate(cards[0][0], color=FETCH),
            Indicate(cards[1][0], color=DECODE),
            Indicate(cards[2][0], color=EXECUTE),
            run_time=0.85,
        )
        self.wait(1.0)

    def clear_stage(self):
        if not self.mobjects:
            return
        mobs = list(self.mobjects)
        self.play(*[FadeOut(mob, shift=DOWN * 0.08) for mob in mobs], run_time=0.55)
        self.clear()

    def section_header(self, title_text, subtitle_text, accent):
        title = Text(title_text, font_size=32, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=accent, stroke_width=3).next_to(title, DOWN, buff=0.15)
        subtitle = Text(subtitle_text, font_size=20, color=MUTED)
        subtitle.next_to(line, DOWN, buff=0.13)
        return VGroup(title, line, subtitle)

    def caption_card(self, text, accent, width=10.0):
        card = RoundedRectangle(width=width, height=0.78, corner_radius=0.16, color=accent, stroke_width=2)
        card.set_fill(SURFACE, opacity=0.97)
        label = Text(text, font_size=21, color=TEXT)
        label.move_to(card)
        return VGroup(card, label)

    def stage_triplet(self):
        return VGroup(
            self.stage_column("Fetch", "Get the next instruction.", FETCH),
            self.stage_column("Decode", "Work out what it means.", DECODE),
            self.stage_column("Execute", "Do the job.", EXECUTE),
        ).arrange(RIGHT, buff=0.5)

    def stage_column(self, title_text, subtitle_text, color):
        chip = self.stage_chip(title_text, color)
        subtitle = Text(subtitle_text, font_size=17, color=MUTED)
        subtitle.next_to(chip, DOWN, buff=0.18)
        return VGroup(chip, subtitle)

    def stage_chip(self, text, color):
        label = Text(text, font_size=18, color=color, weight=BOLD)
        bg = RoundedRectangle(width=label.width + 0.5, height=0.5, corner_radius=0.16, color=color, stroke_width=1.8)
        bg.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def prop_box(self, text, color, width=1.5, height=0.82):
        label = Text(text, font_size=18, color=TEXT, weight=BOLD)
        box = RoundedRectangle(width=width, height=height, corner_radius=0.16, color=color, stroke_width=2)
        box.set_fill(color, opacity=0.18)
        label.move_to(box)
        return VGroup(box, label)

    def robot_icon(self):
        head = RoundedRectangle(width=1.15, height=0.9, corner_radius=0.12, color=FETCH, stroke_width=2.2)
        head.set_fill(SURFACE_ALT, opacity=1)
        head.shift(UP * 0.72)

        eye_left = Circle(radius=0.06, color=TEXT, stroke_width=0).move_to(head.get_center() + LEFT * 0.22 + UP * 0.06)
        eye_right = Circle(radius=0.06, color=TEXT, stroke_width=0).move_to(head.get_center() + RIGHT * 0.22 + UP * 0.06)
        mouth = Line(head.get_center() + LEFT * 0.18 + DOWN * 0.2, head.get_center() + RIGHT * 0.18 + DOWN * 0.2, color=TEXT, stroke_width=2)
        antenna = Line(head.get_top() + UP * 0.06, head.get_top() + UP * 0.32, color=FETCH, stroke_width=2.2)
        antenna_tip = Dot(head.get_top() + UP * 0.35, radius=0.05, color=FETCH)

        body = RoundedRectangle(width=1.45, height=1.0, corner_radius=0.15, color=CPU, stroke_width=2.2)
        body.set_fill(SURFACE_ALT, opacity=1)
        body.shift(DOWN * 0.32)

        arm_left = Line(body.get_left() + LEFT * 0.02 + UP * 0.12, body.get_left() + LEFT * 0.42 + UP * 0.38, color=CPU, stroke_width=2.2)
        arm_right = Line(body.get_right() + RIGHT * 0.02 + UP * 0.12, body.get_right() + RIGHT * 0.42 + UP * 0.38, color=CPU, stroke_width=2.2)
        leg_left = Line(body.get_bottom() + LEFT * 0.26, body.get_bottom() + LEFT * 0.38 + DOWN * 0.34, color=CPU, stroke_width=2.2)
        leg_right = Line(body.get_bottom() + RIGHT * 0.26, body.get_bottom() + RIGHT * 0.38 + DOWN * 0.34, color=CPU, stroke_width=2.2)

        label = Text("Robot", font_size=18, color=MUTED)
        label.next_to(body, DOWN, buff=0.12)

        return VGroup(head, eye_left, eye_right, mouth, antenna, antenna_tip, body, arm_left, arm_right, leg_left, leg_right, label)

    def tea_list_panel(self):
        panel = RoundedRectangle(width=5.0, height=3.6, corner_radius=0.18, color=MEMORY, stroke_width=2.2)
        panel.set_fill(SURFACE, opacity=0.98)

        title = Text("Tea instructions", font_size=20, color=MEMORY, weight=BOLD)
        title.to_edge(UP, buff=0.16).move_to(panel.get_top() + DOWN * 0.26 + LEFT * 1.5)

        texts = ["Boil water", "Put tea bag in mug", "Pour water", "Remove tea bag", "Add milk"]
        rows = VGroup()
        row_refs = []
        for i, text in enumerate(texts, start=1):
            num = Text(str(i), font=CODE_FONT, font_size=16, color=FAINT)
            label = Text(text, font_size=18, color=TEXT)
            row = VGroup(num, label).arrange(RIGHT, buff=0.18)
            bg = RoundedRectangle(width=4.2, height=0.42, corner_radius=0.1, color=P.BORDER_SUBTLE, stroke_width=1.2)
            bg.set_fill(BACKGROUND, opacity=0.2)
            row_group = VGroup(bg, row)
            row.move_to(bg)
            rows.add(row_group)
            row_refs.append(row_group)

        rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.2).align_to(panel, LEFT).shift(RIGHT * 0.35)

        panel_group = VGroup(panel, title, rows)
        return panel_group, row_refs

    def memory_panel(self, instructions, pc_index=0):
        panel = RoundedRectangle(width=5.55, height=4.35, corner_radius=0.18, color=MEMORY, stroke_width=2.2)
        panel.set_fill(SURFACE, opacity=0.98)

        title = Text("Main Memory (RAM)", font_size=20, color=MEMORY, weight=BOLD)
        title.move_to(panel.get_top() + DOWN * 0.28 + LEFT * 1.5)

        pc_chip = self.pc_chip(f"PC = {pc_index + 1}", FETCH)
        pc_chip.next_to(title, DOWN, buff=0.14).align_to(panel, LEFT).shift(RIGHT * 0.28)

        rows = VGroup()
        row_refs = []
        for i, instr in enumerate(instructions, start=1):
            num = Text(str(i), font=CODE_FONT, font_size=16, color=FAINT)
            label = Text(instr, font=CODE_FONT, font_size=19, color=TEXT, t2c=self.instruction_colors(instr))
            row = VGroup(num, label).arrange(RIGHT, buff=0.18)
            bg = RoundedRectangle(width=4.2, height=0.44, corner_radius=0.1, color=P.BORDER_SUBTLE, stroke_width=1.2)
            bg.set_fill(BACKGROUND, opacity=0.2)
            row_group = VGroup(bg, row)
            row.move_to(bg)
            rows.add(row_group)
            row_refs.append(row_group)

        rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        rows.next_to(pc_chip, DOWN, buff=0.18).align_to(panel, LEFT).shift(RIGHT * 0.35)

        if 0 <= pc_index < len(row_refs):
            current = self.highlight_box(row_refs[pc_index], FETCH)
        else:
            current = VGroup()

        group = VGroup(panel, title, pc_chip, rows, current)
        return group, row_refs, pc_chip

    def cpu_panel(self, instruction_text, value, stage_color=CPU):
        panel = RoundedRectangle(width=5.55, height=4.35, corner_radius=0.18, color=CPU, stroke_width=2.2)
        panel.set_fill(SURFACE, opacity=0.98)

        title = Text("CPU", font_size=22, color=CPU, weight=BOLD)
        title.move_to(panel.get_top() + DOWN * 0.28 + LEFT * 0.5)

        instruction_box = RoundedRectangle(width=4.3, height=0.92, corner_radius=0.14, color=stage_color, stroke_width=2)
        instruction_box.set_fill(stage_color, opacity=0.12)
        instruction_box.move_to(panel.get_center() + UP * 0.92)

        ir_label = Text("Instruction register", font_size=16, color=MUTED)
        ir_label.next_to(instruction_box, UP, buff=0.1)

        ir_text = Text(instruction_text, font=CODE_FONT, font_size=20, color=TEXT, t2c=self.instruction_colors(instruction_text))
        ir_text.move_to(instruction_box)

        value_box = RoundedRectangle(width=2.25, height=0.88, corner_radius=0.14, color=EXECUTE, stroke_width=2)
        value_box.set_fill(EXECUTE, opacity=0.12)
        value_box.move_to(panel.get_center() + DOWN * 0.5)

        value_label = Text("Current value", font_size=16, color=MUTED)
        value_label.next_to(value_box, UP, buff=0.1)
        value_text = Integer(value, font_size=24, color=EXECUTE if value != 0 else MUTED)
        value_text.move_to(value_box)

        note = Text("The CPU reads, understands, and carries out instructions.", font_size=15, color=FAINT)
        note.next_to(value_box, DOWN, buff=0.22)
        note.move_to(panel.get_bottom() + UP * 0.28)

        group = VGroup(panel, title, ir_label, instruction_box, ir_text, value_label, value_box, value_text, note)
        return group, VGroup(instruction_box, ir_text), VGroup(value_box, value_text)

    def pc_chip(self, text, color):
        label = Text(text, font_size=17, color=color, weight=BOLD)
        bg = RoundedRectangle(width=label.width + 0.48, height=0.48, corner_radius=0.14, color=color, stroke_width=1.8)
        bg.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(bg)
        return VGroup(bg, label)

    def highlight_box(self, mob, color):
        box = SurroundingRectangle(mob, color=color, buff=0.08, corner_radius=0.08, stroke_width=3)
        box.set_fill(color, opacity=0.12)
        return box

    def meaning_box(self, text, color, width=5.4):
        label = Text(text, font_size=20, color=TEXT)
        box = RoundedRectangle(width=width, height=0.78, corner_radius=0.14, color=color, stroke_width=2)
        box.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(box)
        return VGroup(box, label)

    def value_equation(self, left_value, add_value, result_value, color):
        left = Integer(int(left_value), font_size=26, color=TEXT)
        plus = Text("+", font_size=26, color=color, weight=BOLD)
        add = Integer(int(add_value), font_size=26, color=color)
        equal = Text("=", font_size=26, color=color, weight=BOLD)
        result = Integer(int(result_value), font_size=28, color=EXECUTE)
        eq = VGroup(left, plus, add, equal, result).arrange(RIGHT, buff=0.24)
        return eq

    def cycle_boxes(self):
        return VGroup(
            self.cycle_box("Fetch", FETCH),
            self.cycle_box("Decode", DECODE),
            self.cycle_box("Execute", EXECUTE),
        ).arrange(RIGHT, buff=0.4)

    def cycle_box(self, text, color):
        label = Text(text, font_size=20, color=color, weight=BOLD)
        box = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.16, color=color, stroke_width=2.2)
        box.set_fill(color, opacity=0.12)
        label.move_to(box)
        return VGroup(box, label)

    def instruction_token(self, text, color):
        label = Text(text, font=CODE_FONT, font_size=18, color=TEXT, t2c=self.instruction_colors(text))
        box = RoundedRectangle(width=label.width + 0.42, height=0.52, corner_radius=0.12, color=color, stroke_width=1.8)
        box.set_fill(SURFACE_ALT, opacity=1)
        label.move_to(box)
        return VGroup(box, label)

    def value_readout(self, value):
        box = RoundedRectangle(width=1.55, height=0.72, corner_radius=0.14, color=EXECUTE, stroke_width=2)
        box.set_fill(EXECUTE, opacity=0.12)
        label = Integer(value, font_size=26, color=EXECUTE)
        label.move_to(box)
        return VGroup(box, label)

    def memory_write_box(self, title_text, value):
        box = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.16, color=MEMORY, stroke_width=2.2)
        box.set_fill(MEMORY, opacity=0.1)
        title = Text(title_text, font_size=18, color=MEMORY, weight=BOLD)
        value_text = Integer(value, font_size=24, color=MEMORY)
        title.move_to(box.get_center() + UP * 0.17)
        value_text.move_to(box.get_center() + DOWN * 0.16)
        return VGroup(box, title, value_text)

    def steam_lines(self, kettle):
        top = kettle.get_top() + UP * 0.1
        lines = VGroup()
        for offset in [-0.22, 0.0, 0.22]:
            line = Arc(
                radius=0.2,
                start_angle=PI / 2,
                angle=PI * 0.9,
                color=FETCH,
                stroke_width=2,
            )
            line.shift(top + RIGHT * offset)
            lines.add(line)
        return lines

    def instruction_colors(self, text):
        upper = text.upper()
        colors = {}
        for token in ["LOAD", "ADD", "STORE"]:
            if token in upper:
                colors[token] = FETCH if token == "LOAD" else DECODE if token == "ADD" else EXECUTE
        for token in ["3", "5", "8"]:
            if token in upper:
                colors[token] = WARN
        return colors

    def summary_card(self, title_text, detail_text, color):
        card = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.2, color=color, stroke_width=2.2)
        card.set_fill(SURFACE, opacity=0.98)
        title = Text(title_text, font_size=24, color=color, weight=BOLD)
        detail = Text(detail_text, font_size=19, color=TEXT)
        title.move_to(card.get_center() + UP * 0.28)
        detail.move_to(card.get_center() + DOWN * 0.22)
        return VGroup(card, title, detail)

def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        "-p",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "FetchDecodeExecuteStory",
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
