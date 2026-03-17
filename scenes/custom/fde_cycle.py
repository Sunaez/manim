from manim import *

config.frame_rate = 30


class FDECycleExplainer(MovingCameraScene):
    BG = "#07111F"
    PANEL = "#0F1C2E"
    PANEL_ALT = "#12263D"
    FETCH = "#2EC4B6"
    DECODE = "#FF9F1C"
    EXECUTE = "#E71D36"
    ACCENT = "#7FDBFF"
    SOFT = "#D9F0FF"
    MEMORY = "#8ECAE6"
    CPU = "#1D3557"

    def construct(self):
        self.camera.background_color = self.BG
        backdrop = self.build_backdrop()
        self.add(backdrop)

        title_block = self.build_title_block()
        self.play(FadeIn(title_block, shift=0.3 * UP), run_time=1.2)
        self.wait(0.5)

        architecture, parts = self.build_architecture_diagram()
        title_block.generate_target()
        title_block.target.scale(0.74).to_edge(UP, buff=0.25)

        self.play(
            MoveToTarget(title_block),
            LaggedStart(*[FadeIn(mob, shift=0.25 * UP) for mob in architecture], lag_ratio=0.05),
            run_time=1.5,
        )
        self.wait(0.4)

        overview = self.build_overview_card()
        self.play(FadeIn(overview, shift=0.2 * LEFT), run_time=0.8)
        self.wait(1.2)

        self.play(FadeOut(overview), run_time=0.5)

        step_panel = self.build_step_panel()
        self.play(
            architecture.animate.scale(0.8).to_edge(LEFT, buff=0.2).shift(DOWN * 0.18),
            FadeIn(step_panel, shift=0.25 * LEFT),
            run_time=0.9,
        )

        self.animate_fetch(parts, step_panel)
        self.animate_decode(parts, step_panel)
        self.animate_execute(parts, step_panel)

        self.wait(0.5)
        self.animate_holistic_zoom(title_block, architecture, parts, step_panel)
        self.wait(1.2)

    def build_backdrop(self):
        base = FullScreenRectangle(fill_color=self.BG, fill_opacity=1, stroke_width=0)

        rings = VGroup()
        for radius, opacity in [(3.9, 0.08), (2.8, 0.06), (1.7, 0.05)]:
            ring = Circle(radius=radius, stroke_color=self.ACCENT, stroke_opacity=opacity, stroke_width=2)
            ring.shift(4.7 * LEFT + 2.1 * UP)
            rings.add(ring)

        glow = VGroup(
            Circle(radius=1.4, fill_color=self.FETCH, fill_opacity=0.05, stroke_width=0).shift(5.5 * RIGHT + 2.8 * DOWN),
            Circle(radius=1.1, fill_color=self.DECODE, fill_opacity=0.04, stroke_width=0).shift(5.9 * RIGHT + 2.3 * UP),
        )
        return VGroup(base, rings, glow)

    def build_title_block(self):
        eyebrow = Text("OCR A Level Computer Science", font_size=20, color=self.ACCENT)
        title = Text("The Fetch-Decode-Execute Cycle", font_size=38, weight=BOLD, color=WHITE)
        subtitle = Text(
            "How the control unit, registers and buses work together to run each instruction",
            font_size=21,
            color=self.SOFT,
        )
        subtitle.scale_to_fit_width(10.4)
        block = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.16)
        block.to_edge(UP, buff=0.45)
        return block

    def build_architecture_diagram(self):
        cpu_outer = RoundedRectangle(
            corner_radius=0.18,
            width=5.9,
            height=5.4,
            fill_color=self.CPU,
            fill_opacity=0.7,
            stroke_color=self.ACCENT,
            stroke_width=2.4,
        )
        cpu_outer.shift(2.9 * LEFT + 0.15 * DOWN)

        cpu_title = Text("Processor", font_size=28, weight=BOLD, color=WHITE)
        cpu_title.move_to(cpu_outer.get_top() + DOWN * 0.42)

        cu = self.labelled_box("Control Unit", 2.2, 0.95, self.FETCH, font_size=24)
        cu.move_to(cpu_outer.get_center() + UP * 1.38)

        alu = self.labelled_box("ALU", 1.65, 0.95, self.EXECUTE, font_size=24)
        alu.move_to(cpu_outer.get_center() + LEFT * 1.35 + DOWN * 1.15)

        register_bank = RoundedRectangle(
            corner_radius=0.14,
            width=2.9,
            height=2.55,
            fill_color=self.PANEL,
            fill_opacity=0.82,
            stroke_color=self.DECODE,
            stroke_width=1.8,
        )
        register_bank.move_to(cpu_outer.get_center() + RIGHT * 1.15 + DOWN * 0.95)

        reg_title = Text("Registers", font_size=22, weight=BOLD, color=self.SOFT)
        reg_title.move_to(register_bank.get_top() + DOWN * 0.22)

        pc = self.register_box("PC", "Next instruction address", self.FETCH)
        mar = self.register_box("MAR", "Address in memory", self.FETCH)
        mdr = self.register_box("MDR", "Instruction/data value", self.DECODE)
        cir = self.register_box("CIR", "Current instruction", self.DECODE)
        acc = self.register_box("ACC", "Result of calculation", self.EXECUTE)

        top_row = VGroup(pc, mar).arrange(RIGHT, buff=0.12)
        mid_row = VGroup(mdr, cir).arrange(RIGHT, buff=0.12)
        reg_grid = VGroup(top_row, mid_row, acc).arrange(DOWN, buff=0.13)
        reg_grid.scale(0.92)
        reg_grid.move_to(register_bank.get_center() + DOWN * 0.18)

        memory = RoundedRectangle(
            corner_radius=0.18,
            width=3.2,
            height=5.0,
            fill_color=self.PANEL_ALT,
            fill_opacity=0.82,
            stroke_color=self.MEMORY,
            stroke_width=2.1,
        )
        memory.shift(4.65 * RIGHT + 0.1 * DOWN)
        memory_title = Text("Main Memory", font_size=28, weight=BOLD, color=WHITE)
        memory_title.move_to(memory.get_top() + DOWN * 0.42)

        mem_cells = VGroup()
        for i, txt in enumerate(["204: ADD 301", "205: LDA 205", "206: OUT", "207: HLT"]):
            cell = RoundedRectangle(
                corner_radius=0.08,
                width=2.45,
                height=0.6,
                fill_color="#17314F",
                fill_opacity=0.95,
                stroke_color=self.MEMORY,
                stroke_width=1.2,
            )
            label = Text(txt, font_size=18, color=self.SOFT)
            label.scale_to_fit_width(2.05)
            label.move_to(cell.get_center())
            entry = VGroup(cell, label)
            entry.move_to(memory.get_top() + DOWN * (1.22 + i * 0.84))
            mem_cells.add(entry)

        bus_group = self.build_bus_group(cpu_outer, memory)

        diagram = VGroup(
            cpu_outer, cpu_title, cu, alu, register_bank, reg_title, reg_grid,
            memory, memory_title, mem_cells, bus_group
        )
        diagram.move_to(ORIGIN + DOWN * 0.25)

        parts = {
            "cpu_outer": cpu_outer,
            "cu": cu,
            "alu": alu,
            "register_bank": register_bank,
            "pc": pc,
            "mar": mar,
            "mdr": mdr,
            "cir": cir,
            "acc": acc,
            "memory": memory,
            "mem_cells": mem_cells,
            "bus_group": bus_group,
            "data_bus": bus_group[0],
            "address_bus": bus_group[1],
            "control_bus": bus_group[2],
        }
        return diagram, parts

    def build_bus_group(self, cpu_outer, memory):
        start_x = cpu_outer.get_right()[0] + 0.15
        end_x = memory.get_left()[0] - 0.15
        y_positions = [0.9, 0.1, -0.7]
        labels = [
            ("Data bus", self.DECODE, True),
            ("Address bus", self.FETCH, False),
            ("Control bus", self.ACCENT, True),
        ]
        buses = VGroup()

        for y, (name, color, double_head) in zip(y_positions, labels):
            line = Line(
                [start_x, y, 0],
                [end_x, y, 0],
                color=color,
                stroke_width=5,
            )
            line.add_tip(tip_length=0.18, tip_width=0.14)
            if double_head:
                reverse_tip = ArrowTriangleFilledTip(color=color).scale(0.7)
                reverse_tip.rotate(PI)
                reverse_tip.move_to(line.get_start())
                bus = VGroup(line, reverse_tip)
            else:
                bus = VGroup(line)

            tag = RoundedRectangle(
                corner_radius=0.08,
                width=1.5,
                height=0.42,
                fill_color=self.BG,
                fill_opacity=0.92,
                stroke_color=color,
                stroke_width=1.2,
            )
            text = Text(name, font_size=17, color=WHITE)
            text.scale_to_fit_width(1.18)
            text.move_to(tag.get_center())
            label = VGroup(tag, text).move_to(line.get_center())
            buses.add(VGroup(bus, label))

        buses.shift(DOWN * 0.15)
        return buses

    def build_overview_card(self):
        card = RoundedRectangle(
            corner_radius=0.18,
            width=4.0,
            height=2.35,
            fill_color=self.PANEL,
            fill_opacity=0.92,
            stroke_color=self.ACCENT,
            stroke_width=1.8,
        )
        card.to_corner(DL, buff=0.45)

        heading = Text("Cycle summary", font_size=25, weight=BOLD, color=WHITE)
        heading.move_to(card.get_top() + DOWN * 0.33)

        lines = self.bullet_lines(
            [
                "Fetch: get the next instruction from memory.",
                "Decode: split it into opcode and operand.",
                "Execute: carry out the instruction.",
            ],
            font_size=20,
            width=3.45,
        )
        lines.move_to(card.get_center() + DOWN * 0.2)
        return VGroup(card, heading, lines)

    def build_step_panel(self):
        panel = RoundedRectangle(
            corner_radius=0.18,
            width=3.65,
            height=5.15,
            fill_color=self.PANEL,
            fill_opacity=0.95,
            stroke_color=self.ACCENT,
            stroke_width=1.8,
        )
        panel.to_edge(RIGHT, buff=0.38).shift(DOWN * 0.22)

        phase = Text("Fetch", font_size=30, weight=BOLD, color=self.FETCH)
        phase.move_to(panel.get_top() + DOWN * 0.38)

        sub = Text("Register changes and purpose", font_size=18, color=self.SOFT)
        sub.next_to(phase, DOWN, buff=0.1)

        rule = Line(panel.get_left() + RIGHT * 0.32 + DOWN * 0.95, panel.get_right() + LEFT * 0.32 + DOWN * 0.95, color=GREY_B, stroke_opacity=0.6)

        bullets = self.bullet_lines([""], font_size=18, width=3.0)
        bullets.move_to(panel.get_center() + DOWN * 0.2)

        holder = VGroup(panel, phase, sub, rule, bullets)
        holder.phase = phase
        holder.sub = sub
        holder.rule = rule
        holder.bullets = bullets
        return holder

    def update_step_panel(self, panel, title, color, lines):
        new_phase = Text(title, font_size=30, weight=BOLD, color=color).move_to(panel.phase)
        new_bullets = self.bullet_lines(lines, font_size=18, width=3.0).move_to(panel.bullets)
        self.play(
            Transform(panel.phase, new_phase),
            Transform(panel.bullets, new_bullets),
            run_time=0.6,
        )

    def animate_fetch(self, parts, panel):
        self.update_step_panel(
            panel,
            "Fetch",
            self.FETCH,
            [
                "PC holds the address of the next instruction.",
                "MAR receives that address.",
                "Memory sends the instruction to MDR over the data bus.",
                "PC increases by 1 ready for the next fetch.",
                "MDR copies the instruction into CIR.",
            ],
        )

        highlight = self.soft_highlight(parts["pc"], self.FETCH)
        self.play(FadeIn(highlight), Indicate(parts["pc"], color=self.FETCH), run_time=0.7)

        pc_to_mar = self.flow_arrow(parts["pc"], parts["mar"], self.FETCH)
        self.play(GrowArrow(pc_to_mar), run_time=0.6)
        self.play(Indicate(parts["mar"], color=self.FETCH), run_time=0.5)

        mar_to_memory = self.flow_arrow(parts["mar"], parts["mem_cells"][1], self.FETCH)
        address_glow = self.soft_highlight(parts["data_bus"], self.DECODE, opacity=0.1)
        self.play(GrowArrow(mar_to_memory), FadeIn(self.soft_highlight(parts["address_bus"], self.FETCH, opacity=0.13)), run_time=0.7)
        self.play(Indicate(parts["mem_cells"][1], color=self.FETCH), run_time=0.5)

        memory_to_mdr = self.flow_arrow(parts["mem_cells"][1], parts["mdr"], self.DECODE)
        self.play(GrowArrow(memory_to_mdr), FadeIn(address_glow), Indicate(parts["mdr"], color=self.DECODE), run_time=0.8)

        pc_plus = Text("PC + 1", font_size=22, color=self.SOFT)
        pc_plus.next_to(parts["pc"], UP, buff=0.08)
        self.play(FadeIn(pc_plus, shift=0.1 * UP), run_time=0.4)
        self.play(Flash(parts["pc"].get_center(), color=self.FETCH, flash_radius=0.45), run_time=0.5)

        mdr_to_cir = self.flow_arrow(parts["mdr"], parts["cir"], self.DECODE)
        self.play(GrowArrow(mdr_to_cir), Indicate(parts["cir"], color=self.DECODE), run_time=0.8)
        self.wait(0.4)

        self.play(
            FadeOut(VGroup(highlight, pc_to_mar, mar_to_memory, memory_to_mdr, mdr_to_cir, address_glow, pc_plus)),
            run_time=0.5,
        )

    def animate_decode(self, parts, panel):
        self.update_step_panel(
            panel,
            "Decode",
            self.DECODE,
            [
                "The control unit reads the instruction in CIR.",
                "It splits the instruction into opcode and operand.",
                "Opcode tells the CPU what action to perform.",
                "Operand tells it which address or value to use.",
            ],
        )

        self.play(Indicate(parts["cu"], color=self.DECODE), Indicate(parts["cir"], color=self.DECODE), run_time=0.8)

        instruction_card = RoundedRectangle(
            corner_radius=0.12,
            width=2.95,
            height=1.2,
            fill_color="#17314F",
            fill_opacity=0.95,
            stroke_color=self.DECODE,
            stroke_width=1.6,
        )
        instruction_card.move_to(panel[0].get_bottom() + UP * 0.85)

        instruction = Text("LDA 205", font_size=24, weight=BOLD, color=WHITE)
        instruction.move_to(instruction_card.get_center() + UP * 0.12)

        divider = Line(instruction_card.get_center() + LEFT * 0.18 + DOWN * 0.23, instruction_card.get_center() + LEFT * 0.18 + UP * 0.3, color=GREY_B)
        opcode = Text("Opcode", font_size=16, color=self.DECODE).next_to(divider, LEFT, buff=0.23).shift(DOWN * 0.28)
        operand = Text("Operand", font_size=16, color=self.ACCENT).next_to(divider, RIGHT, buff=0.26).shift(DOWN * 0.28)

        cu_to_cir = self.flow_arrow(parts["cu"], parts["cir"], self.DECODE)
        self.play(FadeIn(instruction_card), GrowArrow(cu_to_cir), run_time=0.7)
        self.play(Write(instruction), Create(divider), FadeIn(opcode), FadeIn(operand), run_time=0.8)
        self.wait(0.8)
        self.play(FadeOut(VGroup(instruction_card, instruction, divider, opcode, operand, cu_to_cir)), run_time=0.5)

    def animate_execute(self, parts, panel):
        self.update_step_panel(
            panel,
            "Execute",
            self.EXECUTE,
            [
                "The control unit sends signals on the control bus.",
                "The ALU or another unit carries out the opcode.",
                "If needed, data is read from memory.",
                "Results can be stored in ACC or written back to memory.",
            ],
        )

        control_glow = self.soft_highlight(parts["control_bus"], self.ACCENT, opacity=0.15)
        self.play(FadeIn(control_glow), Indicate(parts["cu"], color=self.ACCENT), run_time=0.7)

        cir_to_alu = self.flow_arrow(parts["cir"], parts["alu"], self.EXECUTE)
        self.play(GrowArrow(cir_to_alu), Indicate(parts["alu"], color=self.EXECUTE), run_time=0.7)

        alu_to_acc = self.flow_arrow(parts["alu"], parts["acc"], self.EXECUTE)
        result = Text("Result", font_size=20, color=self.SOFT).next_to(alu_to_acc, DOWN, buff=0.05)
        self.play(GrowArrow(alu_to_acc), FadeIn(result, shift=0.08 * DOWN), Indicate(parts["acc"], color=self.EXECUTE), run_time=0.8)

        write_back = self.flow_arrow(parts["acc"], parts["mem_cells"][0], self.EXECUTE)
        self.play(GrowArrow(write_back), Indicate(parts["mem_cells"][0], color=self.EXECUTE), run_time=0.7)
        self.wait(0.4)

        self.play(FadeOut(VGroup(control_glow, cir_to_alu, alu_to_acc, result, write_back)), run_time=0.5)

    def animate_holistic_zoom(self, title_block, architecture, parts, step_panel):
        focus_group = VGroup(title_block, architecture, step_panel)
        self.play(self.camera.frame.animate.scale(1.18).move_to(focus_group), run_time=1.0)

        self.play(
            architecture.animate.scale(0.58).move_to(4.15 * LEFT + 0.05 * DOWN),
            FadeOut(step_panel, shift=0.25 * RIGHT),
            run_time=1.1,
        )

        cycle = self.build_cycle_view()
        cycle.shift(2.15 * RIGHT + 0.18 * UP)
        cycle.scale(0.92)

        connector = Arrow(
            start=parts["cpu_outer"].get_right() + RIGHT * 0.3,
            end=cycle.get_left() + LEFT * 0.18,
            buff=0.1,
            stroke_width=4,
            color=self.ACCENT,
            max_tip_length_to_length_ratio=0.08,
        )

        summary = self.build_summary_strip()
        summary.to_edge(DOWN, buff=0.2)

        self.play(
            LaggedStart(*[FadeIn(mob, shift=0.15 * UP) for mob in cycle], lag_ratio=0.07),
            GrowArrow(connector),
            FadeIn(summary, shift=0.2 * UP),
            run_time=1.4,
        )
        self.wait(1.8)

    def build_cycle_view(self):
        fetch = self.phase_node("1", "Fetch", "PC -> MAR\nMemory -> MDR -> CIR", self.FETCH)
        decode = self.phase_node("2", "Decode", "Control unit splits\nopcode and operand", self.DECODE)
        execute = self.phase_node("3", "Execute", "ALU acts, ACC stores\nor memory is updated", self.EXECUTE)

        fetch.move_to(LEFT * 1.75 + UP * 0.9)
        decode.move_to(RIGHT * 1.75 + UP * 0.9)
        execute.move_to(DOWN * 0.82)

        arrow_a = CurvedArrow(fetch.get_right() + RIGHT * 0.1, decode.get_left() + LEFT * 0.1, angle=-PI / 3.8, color=self.ACCENT, stroke_width=4)
        arrow_b = CurvedArrow(decode.get_bottom() + DOWN * 0.1, execute.get_right() + RIGHT * 0.2, angle=-PI / 3.7, color=self.ACCENT, stroke_width=4)
        arrow_c = CurvedArrow(execute.get_left() + LEFT * 0.2, fetch.get_bottom() + DOWN * 0.1, angle=-PI / 3.7, color=self.ACCENT, stroke_width=4)

        title = Text("Holistic view of one CPU cycle", font_size=24, weight=BOLD, color=WHITE)
        title.move_to(UP * 2.15)

        return VGroup(title, fetch, decode, execute, arrow_a, arrow_b, arrow_c)

    def build_summary_strip(self):
        strip = RoundedRectangle(
            corner_radius=0.16,
            width=11.7,
            height=0.95,
            fill_color=self.PANEL_ALT,
            fill_opacity=0.94,
            stroke_color=self.ACCENT,
            stroke_width=1.4,
        )
        left = Text("Every clock cycle moves the instruction one stage further.", font_size=20, color=WHITE)
        left.scale_to_fit_width(5.2)
        left.move_to(strip.get_center() + LEFT * 2.8)

        right = Text("Then the processor repeats the loop for the next instruction.", font_size=20, color=self.SOFT)
        right.scale_to_fit_width(5.2)
        right.move_to(strip.get_center() + RIGHT * 2.8)

        divider = Line(strip.get_center() + UP * 0.36, strip.get_center() + DOWN * 0.36, color=GREY_B, stroke_opacity=0.7)
        return VGroup(strip, left, right, divider)

    def labelled_box(self, label, width, height, color, font_size=24):
        box = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            fill_color=self.PANEL,
            fill_opacity=0.92,
            stroke_color=color,
            stroke_width=1.8,
        )
        text = Text(label, font_size=font_size, weight=BOLD, color=WHITE)
        text.scale_to_fit_width(width - 0.3)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def register_box(self, short, desc, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=1.28,
            height=0.6,
            fill_color="#18314D",
            fill_opacity=0.98,
            stroke_color=color,
            stroke_width=1.3,
        )
        name = Text(short, font_size=18, weight=BOLD, color=WHITE)
        name.move_to(box.get_center() + UP * 0.1)
        detail = Text(desc, font_size=10, color=self.SOFT)
        detail.scale_to_fit_width(1.0)
        detail.move_to(box.get_center() + DOWN * 0.16)
        return VGroup(box, name, detail)

    def bullet_lines(self, lines, font_size, width):
        items = VGroup()
        for line in lines:
            bullet = Dot(radius=0.045, color=self.ACCENT)
            text = Text(line, font_size=font_size, color=self.SOFT)
            text.scale_to_fit_width(width - 0.3)
            row = VGroup(bullet, text).arrange(RIGHT, buff=0.14, aligned_edge=UP)
            items.add(row)
        items.arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        return items

    def phase_node(self, number, title, description, color):
        circle = Circle(radius=0.72, fill_color=color, fill_opacity=0.2, stroke_color=color, stroke_width=3)
        inner = Circle(radius=0.48, fill_color=self.BG, fill_opacity=1, stroke_color=color, stroke_width=2)
        num = Text(number, font_size=26, weight=BOLD, color=WHITE).move_to(inner)
        badge = VGroup(circle, inner, num)

        heading = Text(title, font_size=25, weight=BOLD, color=color)
        body = Text(description, font_size=18, color=self.SOFT, line_spacing=0.84)
        body.scale_to_fit_width(2.7)
        content = VGroup(heading, body).arrange(DOWN, buff=0.14)

        panel = RoundedRectangle(
            corner_radius=0.16,
            width=3.15,
            height=2.35,
            fill_color=self.PANEL,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.8,
        )
        badge.move_to(panel.get_top() + DOWN * 0.66)
        content.move_to(panel.get_center() + DOWN * 0.42)
        return VGroup(panel, badge, content)

    def flow_arrow(self, source, target, color):
        return Arrow(
            start=source.get_center(),
            end=target.get_center(),
            buff=0.25,
            stroke_width=4,
            color=color,
            max_tip_length_to_length_ratio=0.09,
        )

    def soft_highlight(self, mob, color, opacity=0.12):
        glow = SurroundingRectangle(
            mob,
            buff=0.08,
            corner_radius=0.12,
            stroke_width=0,
            fill_color=color,
            fill_opacity=opacity,
        )
        return glow
