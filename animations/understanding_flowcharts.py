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
START_END = P.GREEN
PROCESS = P.BLUE
INPUT_OUTPUT = P.PURPLE
DECISION = P.ORANGE
ERROR = P.RED
HIGHLIGHT = P.YELLOW
FLOW = P.TEXT_SECONDARY
CODE_FONT = "Consolas"


class UnderstandingFlowcharts(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        self.scene_intro()
        self.clear_stage()

        self.scene_symbols()
        self.clear_stage()

        flowchart = self.scene_build_flowchart()
        self.scene_trace(flowchart)
        self.scene_pseudocode(flowchart)

        self.clear_stage()
        self.scene_mistakes()
        self.clear_stage()

        self.scene_challenge()
        self.wait(1.4)

    def scene_intro(self):
        title = Text("Understanding Flowcharts", font_size=40, color=TEXT, weight=BOLD)
        definition = Text(
            "A flowchart is a diagram that shows the steps in an algorithm.",
            font_size=24,
            color=MUTED,
        )
        definition.next_to(title, DOWN, buff=0.28)

        note = self.caption_card("Each shape has a different meaning.", INPUT_OUTPUT, width=7.6)
        note.next_to(definition, DOWN, buff=0.45)

        glow = Circle(radius=1.4, color=INPUT_OUTPUT, stroke_width=0)
        glow.set_fill(INPUT_OUTPUT, opacity=0.08)
        glow.move_to(title)

        self.play(FadeIn(glow), FadeIn(title, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(definition, shift=UP * 0.08), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.8)
        self.wait(1.2)
        self.play(
            FadeOut(note, shift=DOWN * 0.1),
            title.animate.scale(0.82).to_edge(UP, buff=0.4),
            definition.animate.scale(0.9).next_to(title, DOWN, buff=0.18),
            run_time=0.8,
        )
        self.wait(0.4)

    def scene_symbols(self):
        header = self.section_header("2. Flowchart symbols", "Each symbol has a specific job.", INPUT_OUTPUT)
        panel = RoundedRectangle(width=3.8, height=6.0, corner_radius=0.18, color=BORDER, stroke_width=2)
        panel.set_fill(SURFACE, opacity=0.98)
        panel.to_edge(RIGHT, buff=0.45).shift(DOWN * 0.2)

        panel_title = Text("Reference", font_size=24, color=TEXT, weight=BOLD)
        panel_title.move_to(panel.get_top() + DOWN * 0.35)

        slots = []
        top_y = panel.get_top()[1] - 1.0
        for index in range(5):
            slot = RoundedRectangle(width=3.1, height=0.8, corner_radius=0.12, color=P.BORDER_SUBTLE, stroke_width=1.2)
            slot.set_fill(SURFACE_ALT, opacity=0.65)
            slot.move_to(panel.get_center() + UP * (top_y - panel.get_center()[1] - index * 0.95))
            slots.append(slot)
        slot_group = VGroup(*slots)

        self.play(FadeIn(header, shift=DOWN * 0.12), FadeIn(panel), FadeIn(panel_title), FadeIn(slot_group), run_time=0.9)

        symbol_specs = [
            {
                "name": "Start / End",
                "color": START_END,
                "builder": lambda: self.terminator_node("Start / End", label_size=26),
                "explanation": "Used to show where an algorithm begins or finishes.",
            },
            {
                "name": "Process",
                "color": PROCESS,
                "builder": lambda: self.process_node("Process", label_size=28),
                "explanation": "Used for an instruction or action.",
            },
            {
                "name": "Input / Output",
                "color": INPUT_OUTPUT,
                "builder": lambda: self.input_output_node("Input / Output", label_size=24),
                "explanation": "Used when data is entered or displayed.",
            },
            {
                "name": "Decision",
                "color": DECISION,
                "builder": self.decision_symbol_demo,
                "explanation": "Used when the algorithm asks a question.",
            },
            {
                "name": "Flow line",
                "color": FLOW,
                "builder": self.flow_line_symbol,
                "explanation": "Shows the direction the algorithm moves in.",
            },
        ]

        entries = VGroup()
        for index, spec in enumerate(symbol_specs):
            demo_shape = spec["builder"]()
            demo_shape.move_to(LEFT * 2.7 + UP * 0.55)

            demo_name = Text(spec["name"], font_size=30, color=spec["color"], weight=BOLD)
            demo_name.next_to(demo_shape, DOWN, buff=0.32)

            explanation = self.caption_card(spec["explanation"], spec["color"], width=6.9)
            explanation.to_edge(DOWN, buff=0.45)

            self.play(FadeIn(demo_shape, shift=UP * 0.08), run_time=0.7)
            self.play(FadeIn(demo_name, shift=UP * 0.06), run_time=0.45)
            self.play(Circumscribe(demo_shape, color=HIGHLIGHT, time_width=0.7), FadeIn(explanation, shift=UP * 0.06), run_time=0.8)
            self.wait(0.5)

            entry = self.reference_entry(spec["name"], demo_shape.copy().scale(0.42), spec["color"])
            entry.move_to(slots[index].get_center())
            self.play(TransformFromCopy(VGroup(demo_shape, demo_name), entry), run_time=0.8)
            entries.add(entry)
            self.play(FadeOut(VGroup(demo_shape, demo_name, explanation), shift=DOWN * 0.08), run_time=0.45)
            self.wait(0.25)

        self.wait(0.9)

    def scene_build_flowchart(self):
        header = self.section_header("3. Build a simple flowchart", 'Algorithm: "Check if a number is positive."', START_END)
        flowchart = self.build_positive_flowchart(scale=0.94, center=ORIGIN + DOWN * 0.2)
        caption = self.caption_card("Every flowchart begins with Start.", START_END, width=7.8)
        caption.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(header, shift=DOWN * 0.12), run_time=0.75)
        self.play(FadeIn(caption, shift=UP * 0.08), run_time=0.45)

        self.play(Create(flowchart["start"][0]), FadeIn(flowchart["start"][1]), run_time=0.8)
        self.play(Circumscribe(flowchart["start"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.8)
        self.wait(0.7)

        caption = self.swap_caption(caption, "Input is shown using a parallelogram.", INPUT_OUTPUT, width=7.1)
        self.play(GrowArrow(flowchart["start_to_input"]), Create(flowchart["input"][0]), FadeIn(flowchart["input"][1]), run_time=1.0)
        self.play(Circumscribe(flowchart["input"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.8)
        self.wait(0.7)

        caption = self.swap_caption(caption, "A decision uses a question and must have branches.", DECISION, width=8.8)
        self.play(GrowArrow(flowchart["input_to_decision"]), Create(flowchart["decision"][0]), FadeIn(flowchart["decision"][1]), run_time=1.0)
        self.play(Circumscribe(flowchart["decision"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.8)
        self.wait(0.7)

        caption = self.swap_caption(caption, "This path is used when the condition is true.", INPUT_OUTPUT, width=7.8)
        self.play(
            GrowArrow(flowchart["yes_arrow"]),
            FadeIn(flowchart["yes_label"], shift=UP * 0.05),
            Create(flowchart["yes_output"][0]),
            FadeIn(flowchart["yes_output"][1]),
            run_time=1.0,
        )
        self.play(Circumscribe(flowchart["yes_output"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.8)
        self.wait(0.7)

        caption = self.swap_caption(caption, "This path is used when the condition is false.", INPUT_OUTPUT, width=8.0)
        self.play(
            GrowArrow(flowchart["no_arrow"]),
            FadeIn(flowchart["no_label"], shift=UP * 0.05),
            Create(flowchart["no_output"][0]),
            FadeIn(flowchart["no_output"][1]),
            run_time=1.0,
        )
        self.play(Circumscribe(flowchart["no_output"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.8)
        self.wait(0.7)

        caption = self.swap_caption(caption, "Both paths eventually finish the algorithm.", START_END, width=7.7)
        self.play(Create(flowchart["end"][0]), FadeIn(flowchart["end"][1]), run_time=0.7)
        self.play(GrowArrow(flowchart["yes_to_end"]), GrowArrow(flowchart["no_to_end"]), run_time=1.0)
        self.play(Circumscribe(flowchart["end"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.8)
        self.wait(1.1)

        flowchart["header"] = header
        flowchart["caption"] = caption
        return flowchart

    def scene_trace(self, flowchart):
        new_header = self.section_header("4. Trace the flowchart", "Follow the path step by step.", HIGHLIGHT)
        self.play(Transform(flowchart["header"], new_header), flowchart["caption"].animate.set_opacity(0.0), run_time=0.7)

        example = Text("Example: number = 5", font_size=26, color=INPUT_OUTPUT, weight=BOLD)
        example.to_edge(UP, buff=1.05).shift(RIGHT * 3.2)
        check_card = self.caption_card("5 > 0 is True", DECISION, width=4.4)
        check_card.to_edge(DOWN, buff=1.2)
        output_card = self.caption_card("Final output: Positive", INPUT_OUTPUT, width=5.3)
        output_card.to_edge(DOWN, buff=0.32)
        tracer = Dot(radius=0.1, color=HIGHLIGHT).move_to(flowchart["start"][0].get_center())

        self.play(FadeIn(example, shift=UP * 0.06), FadeIn(tracer), run_time=0.6)
        self.play(Circumscribe(flowchart["start"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.6)
        self.travel(tracer, flowchart["start_to_input"], flowchart["input"])
        self.play(Circumscribe(flowchart["input"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.6)
        self.travel(tracer, flowchart["input_to_decision"], flowchart["decision"])
        self.play(Circumscribe(flowchart["decision"][0], color=HIGHLIGHT, time_width=0.7), FadeIn(check_card, shift=UP * 0.06), run_time=0.7)
        self.travel(tracer, flowchart["yes_arrow"], flowchart["yes_output"])
        self.play(Circumscribe(flowchart["yes_output"][0], color=HIGHLIGHT, time_width=0.7), FadeIn(output_card, shift=UP * 0.06), run_time=0.7)
        self.travel(tracer, flowchart["yes_to_end"], flowchart["end"])
        self.play(Circumscribe(flowchart["end"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.6)
        self.wait(1.0)

        next_example = Text("Example: number = -3", font_size=26, color=INPUT_OUTPUT, weight=BOLD)
        next_example.move_to(example)
        next_check = self.caption_card("-3 > 0 is False", DECISION, width=4.8)
        next_check.move_to(check_card)
        next_output = self.caption_card("Final output: Not positive", INPUT_OUTPUT, width=6.0)
        next_output.move_to(output_card)

        self.play(
            Transform(example, next_example),
            Transform(check_card, next_check),
            Transform(output_card, next_output),
            tracer.animate.move_to(flowchart["start"][0].get_center()),
            run_time=0.9,
        )
        self.play(Circumscribe(flowchart["start"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.6)
        self.travel(tracer, flowchart["start_to_input"], flowchart["input"])
        self.play(Circumscribe(flowchart["input"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.6)
        self.travel(tracer, flowchart["input_to_decision"], flowchart["decision"])
        self.play(Circumscribe(flowchart["decision"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.7)
        self.travel(tracer, flowchart["no_arrow"], flowchart["no_output"])
        self.play(Circumscribe(flowchart["no_output"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.7)
        self.travel(tracer, flowchart["no_to_end"], flowchart["end"])
        self.play(Circumscribe(flowchart["end"][0], color=HIGHLIGHT, time_width=0.7), run_time=0.6)
        self.wait(1.0)

        self.play(FadeOut(example), FadeOut(check_card), FadeOut(output_card), FadeOut(tracer), run_time=0.45)

    def scene_pseudocode(self, flowchart):
        new_header = self.section_header("5. Connect flowcharts to pseudocode", "The same algorithm can be shown in different ways.", INPUT_OUTPUT)
        self.play(
            Transform(flowchart["header"], new_header),
            flowchart["caption"].animate.set_opacity(0.0),
            flowchart["group"].animate.scale(0.74).move_to(LEFT * 3.45 + DOWN * 0.25),
            run_time=1.0,
        )

        panel = RoundedRectangle(width=5.4, height=5.2, corner_radius=0.18, color=INPUT_OUTPUT, stroke_width=2)
        panel.set_fill(SURFACE, opacity=0.98)
        panel.move_to(RIGHT * 2.85 + DOWN * 0.15)

        title = Text("Pseudocode", font_size=26, color=INPUT_OUTPUT, weight=BOLD)
        title.move_to(panel.get_top() + DOWN * 0.34)

        lines = self.pseudocode_lines()
        lines_group = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lines_group.next_to(title, DOWN, buff=0.28)
        lines_group.align_to(panel, LEFT).shift(RIGHT * 0.55)

        closing = self.caption_card(
            "Flowcharts and pseudocode can show the same algorithm in different ways.",
            INPUT_OUTPUT,
            width=11.0,
        )
        closing.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(panel), FadeIn(title), LaggedStart(*[FadeIn(line, shift=UP * 0.04) for line in lines], lag_ratio=0.06), run_time=1.0)

        link_specs = [
            (lines[1], flowchart["input"][0]),
            (lines[2], flowchart["decision"][0]),
            (lines[3], flowchart["yes_output"][0]),
            (lines[5], flowchart["no_output"][0]),
            (lines[7], flowchart["end"][0]),
        ]
        for line, shape in link_specs:
            line_box = SurroundingRectangle(line, color=HIGHLIGHT, buff=0.08, corner_radius=0.08, stroke_width=3)
            line_box.set_fill(HIGHLIGHT, opacity=0.08)
            link = DashedLine(shape.get_right(), line.get_left(), color=HIGHLIGHT, dash_length=0.09)
            self.play(Create(line_box), Create(link), Circumscribe(shape, color=HIGHLIGHT, time_width=0.7), run_time=0.8)
            self.wait(0.35)
            self.play(FadeOut(line_box), FadeOut(link), run_time=0.3)

        self.play(FadeIn(closing, shift=UP * 0.06), run_time=0.6)
        self.wait(1.0)

    def scene_mistakes(self):
        header = self.section_header("6. Common Flowchart Mistakes", "Notice the problem, then fix it.", ERROR)
        list_panel = RoundedRectangle(width=4.4, height=5.6, corner_radius=0.18, color=BORDER, stroke_width=2)
        list_panel.set_fill(SURFACE, opacity=0.98)
        list_panel.to_edge(LEFT, buff=0.45).shift(DOWN * 0.15)

        list_title = Text("Checklist", font_size=24, color=TEXT, weight=BOLD)
        list_title.move_to(list_panel.get_top() + DOWN * 0.35)

        demo_frame = RoundedRectangle(width=7.1, height=4.9, corner_radius=0.18, color=BORDER, stroke_width=2)
        demo_frame.set_fill(SURFACE, opacity=0.98)
        demo_frame.to_edge(RIGHT, buff=0.45).shift(DOWN * 0.05)

        demo_title = Text("Example", font_size=24, color=TEXT, weight=BOLD)
        demo_title.move_to(demo_frame.get_top() + DOWN * 0.35)

        self.play(FadeIn(header, shift=DOWN * 0.12), FadeIn(list_panel), FadeIn(list_title), FadeIn(demo_frame), FadeIn(demo_title), run_time=0.9)

        rows = []
        items = [
            "1. Forgetting Start or End",
            "2. Using a rectangle\nfor input",
            "3. Decision without\nYes / No labels",
            "4. Arrows not\nshowing direction",
        ]
        for index, text in enumerate(items):
            row = self.checklist_row(text)
            row.move_to(list_panel.get_top() + DOWN * (1.0 + index * 0.95)).align_to(list_panel, LEFT).shift(RIGHT * 0.42)
            rows.append(row)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.05), run_time=0.45)

        demo_center = demo_frame.get_center() + DOWN * 0.2

        rows[0][1].set_color(HIGHLIGHT)
        missing_start = self.missing_start_demo().move_to(demo_center)
        start_fix = self.terminator_node("Start", label_size=24).scale(0.82)
        start_fix.move_to(missing_start[0].get_center() + UP * 1.65)
        fix_arrow = self.flow_arrow(start_fix[0].get_bottom(), missing_start[0][0].get_top())
        cross = Cross(missing_start, stroke_color=ERROR, stroke_width=6)
        self.play(FadeIn(missing_start, shift=UP * 0.05), run_time=0.7)
        self.play(Create(cross), run_time=0.45)
        self.wait(0.4)
        self.play(FadeOut(cross), FadeIn(start_fix), GrowArrow(fix_arrow), run_time=0.8)
        self.play(rows[0][0].animate.set_fill(START_END, opacity=1), rows[0][1].animate.set_color(TEXT), run_time=0.45)
        self.wait(0.5)
        self.play(FadeOut(VGroup(missing_start, start_fix, fix_arrow)), run_time=0.45)

        rows[1][1].set_color(HIGHLIGHT)
        wrong_input = self.process_node("Input\nname", label_size=24).scale(0.9).move_to(demo_center)
        right_input = self.input_output_node("Input\nname", label_size=24).scale(0.9).move_to(demo_center)
        cross = Cross(wrong_input, stroke_color=ERROR, stroke_width=6)
        self.play(FadeIn(wrong_input, shift=UP * 0.05), run_time=0.7)
        self.play(Create(cross), run_time=0.45)
        self.wait(0.4)
        self.play(FadeOut(cross), Transform(wrong_input, right_input), run_time=0.8)
        self.play(rows[1][0].animate.set_fill(START_END, opacity=1), rows[1][1].animate.set_color(TEXT), run_time=0.45)
        self.wait(0.5)
        self.play(FadeOut(wrong_input), run_time=0.45)

        rows[2][1].set_color(HIGHLIGHT)
        unlabeled = self.unlabeled_decision_demo().move_to(demo_center)
        yes_tag = Text("Yes", font_size=22, color=TEXT, weight=BOLD).next_to(unlabeled[1], UP, buff=0.12)
        no_tag = Text("No", font_size=22, color=TEXT, weight=BOLD).next_to(unlabeled[2], UP, buff=0.12)
        cross = Cross(unlabeled, stroke_color=ERROR, stroke_width=6)
        self.play(FadeIn(unlabeled, shift=UP * 0.05), run_time=0.7)
        self.play(Create(cross), run_time=0.45)
        self.wait(0.4)
        self.play(FadeOut(cross), FadeIn(yes_tag), FadeIn(no_tag), run_time=0.8)
        self.play(rows[2][0].animate.set_fill(START_END, opacity=1), rows[2][1].animate.set_color(TEXT), run_time=0.45)
        self.wait(0.5)
        self.play(FadeOut(VGroup(unlabeled, yes_tag, no_tag)), run_time=0.45)

        rows[3][1].set_color(HIGHLIGHT)
        disconnected = self.disconnected_demo().move_to(demo_center)
        arrow_top = self.flow_arrow(disconnected[0][0].get_bottom(), disconnected[1][0].get_top())
        arrow_bottom = self.flow_arrow(disconnected[1][0].get_bottom(), disconnected[2][0].get_top())
        cross = Cross(disconnected, stroke_color=ERROR, stroke_width=6)
        self.play(FadeIn(disconnected, shift=UP * 0.05), run_time=0.7)
        self.play(Create(cross), run_time=0.45)
        self.wait(0.4)
        self.play(FadeOut(cross), GrowArrow(arrow_top), GrowArrow(arrow_bottom), run_time=0.8)
        self.play(rows[3][0].animate.set_fill(START_END, opacity=1), rows[3][1].animate.set_color(TEXT), run_time=0.45)
        self.wait(0.8)

    def scene_challenge(self):
        title = Text("Your Turn", font_size=40, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.35)

        prompt = Text("Create a flowchart for this algorithm:", font_size=25, color=MUTED)
        prompt.next_to(title, DOWN, buff=0.22)

        left_panel = RoundedRectangle(width=5.8, height=4.9, corner_radius=0.18, color=INPUT_OUTPUT, stroke_width=2)
        left_panel.set_fill(SURFACE, opacity=0.98)
        left_panel.move_to(LEFT * 3.15 + DOWN * 0.25)

        right_panel = RoundedRectangle(width=5.8, height=4.9, corner_radius=0.18, color=START_END, stroke_width=2)
        right_panel.set_fill(SURFACE, opacity=0.98)
        right_panel.move_to(RIGHT * 3.15 + DOWN * 0.25)

        algo_title = Text("Algorithm", font_size=24, color=INPUT_OUTPUT, weight=BOLD)
        algo_title.move_to(left_panel.get_top() + DOWN * 0.34)
        criteria_title = Text("Success criteria", font_size=24, color=START_END, weight=BOLD)
        criteria_title.move_to(right_panel.get_top() + DOWN * 0.34)

        algorithm_lines = [
            "1. Start",
            "2. Input age",
            '3. If age >= 18,\n   output "Adult"',
            '4. Otherwise,\n   output "Child"',
            "5. End",
        ]
        criteria_lines = [
            "Use Start and End ovals.",
            "Use a parallelogram\nfor input and output.",
            "Use a diamond for the decision.",
            "Label the branches Yes and No.",
            "Use arrows to show the flow.",
        ]

        algo_group = VGroup(
            *[Text(line, font_size=20, color=TEXT, line_spacing=0.9) for line in algorithm_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        algo_group.next_to(algo_title, DOWN, buff=0.35)
        algo_group.align_to(left_panel, LEFT).shift(RIGHT * 0.45)

        criteria_group = VGroup(
            *[Text(line, font_size=19, color=TEXT, line_spacing=0.9) for line in criteria_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        criteria_group.next_to(criteria_title, DOWN, buff=0.35)
        criteria_group.align_to(right_panel, LEFT).shift(RIGHT * 0.45)

        closing = self.caption_card(
            "Flowcharts help us see how an algorithm works step by step.",
            HIGHLIGHT,
            width=10.4,
        )
        closing.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(title, shift=UP * 0.08), FadeIn(prompt, shift=UP * 0.06), run_time=0.8)
        self.play(FadeIn(left_panel), FadeIn(right_panel), FadeIn(algo_title), FadeIn(criteria_title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.04) for line in algo_group], lag_ratio=0.08), run_time=1.0)
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.04) for line in criteria_group], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(closing, shift=UP * 0.06), run_time=0.6)
        self.wait(1.6)

    def build_positive_flowchart(self, scale=1.0, center=ORIGIN):
        start = self.terminator_node("Start", label_size=26)
        input_node = self.input_output_node("Input\nnumber", label_size=24)
        decision = self.decision_node("number > 0?", label_size=22)
        yes_output = self.input_output_node("Output\nPositive", label_size=22)
        no_output = self.input_output_node("Output\nNot positive", label_size=20)
        end = self.terminator_node("End", label_size=26)

        start.move_to(UP * 2.7)
        input_node.move_to(UP * 1.1)
        decision.move_to(DOWN * 0.55)
        yes_output.move_to(RIGHT * 3.35 + DOWN * 0.55)
        no_output.move_to(LEFT * 3.35 + DOWN * 0.55)
        end.move_to(DOWN * 3.1)

        start_to_input = self.flow_arrow(start[0].get_bottom(), input_node[0].get_top())
        input_to_decision = self.flow_arrow(input_node[0].get_bottom(), decision[0].get_top())
        yes_arrow = self.flow_arrow(decision[0].get_right(), yes_output[0].get_left())
        no_arrow = self.flow_arrow(decision[0].get_left(), no_output[0].get_right())
        yes_to_end = self.flow_arrow(yes_output[0].get_bottom() + DOWN * 0.02, end[0].get_top() + RIGHT * 0.72)
        no_to_end = self.flow_arrow(no_output[0].get_bottom() + DOWN * 0.02, end[0].get_top() + LEFT * 0.72)

        yes_label = Text("Yes", font_size=19, color=TEXT, weight=BOLD).next_to(yes_arrow, UP, buff=0.1)
        no_label = Text("No", font_size=19, color=TEXT, weight=BOLD).next_to(no_arrow, UP, buff=0.1)

        group = VGroup(
            start,
            input_node,
            decision,
            yes_output,
            no_output,
            end,
            start_to_input,
            input_to_decision,
            yes_arrow,
            no_arrow,
            yes_to_end,
            no_to_end,
            yes_label,
            no_label,
        )
        group.scale(scale)
        group.move_to(center)

        return {
            "group": group,
            "start": start,
            "input": input_node,
            "decision": decision,
            "yes_output": yes_output,
            "no_output": no_output,
            "end": end,
            "start_to_input": start_to_input,
            "input_to_decision": input_to_decision,
            "yes_arrow": yes_arrow,
            "no_arrow": no_arrow,
            "yes_to_end": yes_to_end,
            "no_to_end": no_to_end,
            "yes_label": yes_label,
            "no_label": no_label,
        }

    def terminator_node(self, text, label_size=26):
        shape = Ellipse(width=2.7, height=1.15, color=START_END, stroke_width=3)
        shape.set_fill(START_END, opacity=0.16)
        label = Text(text, font_size=label_size, color=TEXT, weight=BOLD)
        label.move_to(shape.get_center())
        return VGroup(shape, label)

    def process_node(self, text, label_size=26):
        shape = RoundedRectangle(width=3.0, height=1.2, corner_radius=0.08, color=PROCESS, stroke_width=3)
        shape.set_fill(PROCESS, opacity=0.16)
        label = Text(text, font_size=label_size, color=TEXT, weight=BOLD)
        label.move_to(shape.get_center())
        return VGroup(shape, label)

    def input_output_node(self, text, label_size=24):
        width = 3.2
        height = 1.25
        slant = 0.35
        points = [
            LEFT * (width / 2 - slant) + UP * (height / 2),
            RIGHT * (width / 2) + UP * (height / 2),
            RIGHT * (width / 2 - slant) + DOWN * (height / 2),
            LEFT * (width / 2) + DOWN * (height / 2),
        ]
        shape = Polygon(*points, color=INPUT_OUTPUT, stroke_width=3)
        shape.set_fill(INPUT_OUTPUT, opacity=0.16)
        label = Text(text, font_size=label_size, color=TEXT, weight=BOLD, line_spacing=0.9)
        label.move_to(shape.get_center())
        return VGroup(shape, label)

    def decision_node(self, text, label_size=22):
        width = 3.2
        height = 1.9
        shape = Polygon(
            UP * (height / 2),
            RIGHT * (width / 2),
            DOWN * (height / 2),
            LEFT * (width / 2),
            color=DECISION,
            stroke_width=3,
        )
        shape.set_fill(DECISION, opacity=0.16)
        label = Text(text, font_size=label_size, color=TEXT, weight=BOLD)
        label.move_to(shape.get_center())
        return VGroup(shape, label)

    def decision_symbol_demo(self):
        decision = self.decision_node("Question?", label_size=22)
        yes_arrow = self.flow_arrow(decision[0].get_right(), decision[0].get_right() + RIGHT * 1.4)
        no_arrow = self.flow_arrow(decision[0].get_bottom() + LEFT * 0.02, decision[0].get_bottom() + DOWN * 1.2)
        yes_label = Text("Yes", font_size=18, color=TEXT, weight=BOLD).next_to(yes_arrow, UP, buff=0.08)
        no_label = Text("No", font_size=18, color=TEXT, weight=BOLD).next_to(no_arrow, LEFT, buff=0.08)
        return VGroup(decision, yes_arrow, no_arrow, yes_label, no_label)

    def flow_line_symbol(self):
        arrow = self.flow_arrow(LEFT * 1.6, RIGHT * 1.6)
        return VGroup(arrow)

    def missing_start_demo(self):
        input_node = self.input_output_node("Input\nnumber", label_size=22).scale(0.82)
        end = self.terminator_node("End", label_size=24).scale(0.82)
        input_node.move_to(UP * 0.95)
        end.move_to(DOWN * 1.05)
        arrow = self.flow_arrow(input_node[0].get_bottom(), end[0].get_top())
        return VGroup(input_node, arrow, end)

    def unlabeled_decision_demo(self):
        decision = self.decision_node("Score >= 50?", label_size=19).scale(0.84)
        left_arrow = self.flow_arrow(decision[0].get_left(), decision[0].get_left() + LEFT * 1.5)
        right_arrow = self.flow_arrow(decision[0].get_right(), decision[0].get_right() + RIGHT * 1.5)
        return VGroup(decision, left_arrow, right_arrow)

    def disconnected_demo(self):
        start = self.terminator_node("Start", label_size=22).scale(0.76)
        process = self.process_node("Process", label_size=22).scale(0.76)
        end = self.terminator_node("End", label_size=22).scale(0.76)
        start.move_to(UP * 1.45)
        process.move_to(ORIGIN)
        end.move_to(DOWN * 1.45)
        return VGroup(start, process, end)

    def pseudocode_lines(self):
        text_specs = [
            "START",
            "INPUT number",
            "IF number > 0 THEN",
            '    OUTPUT "Positive"',
            "ELSE",
            '    OUTPUT "Not positive"',
            "END IF",
            "END",
        ]
        return [
            Text(
                line,
                font=CODE_FONT,
                font_size=22,
                color=TEXT,
                t2c={
                    "START": START_END,
                    "END": START_END,
                    "INPUT": INPUT_OUTPUT,
                    "OUTPUT": INPUT_OUTPUT,
                    "IF": DECISION,
                    "THEN": DECISION,
                    "ELSE": DECISION,
                },
            )
            for line in text_specs
        ]

    def flow_arrow(self, start, end):
        return Arrow(
            start,
            end,
            buff=0.08,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.16,
            color=FLOW,
        )

    def travel(self, tracer, arrow, target):
        flash = arrow.copy().set_color(HIGHLIGHT).set_stroke(width=6)
        self.play(
            ShowPassingFlash(flash, time_width=0.7),
            tracer.animate.move_to(target[0].get_center()),
            run_time=0.8,
        )

    def reference_entry(self, name, symbol, color):
        label = Text(name, font_size=20, color=TEXT, weight=BOLD)
        label.move_to(RIGHT * 0.45)
        symbol.move_to(LEFT * 0.95)
        box = RoundedRectangle(width=3.0, height=0.72, corner_radius=0.1, color=color, stroke_width=1.6)
        box.set_fill(SURFACE_ALT, opacity=0.88)
        return VGroup(box, symbol, label)

    def checklist_row(self, text):
        marker = Square(side_length=0.22, color=START_END, stroke_width=2)
        marker.set_fill(BACKGROUND, opacity=1)
        label = Text(text, font_size=18, color=TEXT, line_spacing=0.9)
        row = VGroup(marker, label).arrange(RIGHT, buff=0.16)
        return row

    def section_header(self, title_text, subtitle_text, accent):
        title = Text(title_text, font_size=31, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.26)
        line = Line(LEFT * 5.9, RIGHT * 5.9, color=accent, stroke_width=3).next_to(title, DOWN, buff=0.14)
        subtitle = Text(subtitle_text, font_size=20, color=MUTED)
        subtitle.next_to(line, DOWN, buff=0.13)
        return VGroup(title, line, subtitle)

    def caption_card(self, text, accent, width=8.2):
        font_size = 22
        if len(text) > 42:
            font_size = 20
        if len(text) > 62:
            font_size = 18
        label = Text(text, font_size=font_size, color=TEXT)
        box = RoundedRectangle(width=width, height=0.85, corner_radius=0.16, color=accent, stroke_width=2)
        box.set_fill(SURFACE, opacity=0.98)
        label.move_to(box)
        return VGroup(box, label)

    def swap_caption(self, current, text, accent, width=8.2):
        new_caption = self.caption_card(text, accent, width=width)
        new_caption.move_to(current)
        self.play(Transform(current, new_caption), run_time=0.45)
        return current

    def clear_stage(self):
        if not self.mobjects:
            return
        mobs = list(self.mobjects)
        self.play(*[FadeOut(mob, shift=DOWN * 0.08) for mob in mobs], run_time=0.55)
        self.clear()


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        "-p",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "UnderstandingFlowcharts",
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
