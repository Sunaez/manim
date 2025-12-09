from manim import *

config.frame_rate = 30  # Ensure 30fps minimum


class RobotDoorFlowchart(Scene):
    """
    Flow diagram animation showing how to program a robot to open a door.
    Uses standard flowchart symbols:
    - Oval: start/end
    - Rectangle: process
    - Parallelogram: input/output
    - Diamond: decision
    - Arrow: flow direction
    """

    # Color scheme matching the reference image
    SHAPE_COLOR = "#7FCFEA"  # Light blue for shapes
    SHAPE_FILL = "#E8F6FB"   # Very light blue fill

    def construct(self):
        # Title scene
        self.title_scene()
        self.wait(0.5)
        self.clear()

        # Legend/key explanation
        self.legend_scene()
        self.wait(0.5)
        self.clear()

        # Main flowchart
        self.flowchart_scene()
        self.wait(1)

    def create_oval(self, text, width=2.2, height=0.7):
        """Create an oval (start/end) with text"""
        oval = Ellipse(width=width, height=height, color=self.SHAPE_COLOR,
                       fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=18, color=BLACK)
        label.move_to(oval.get_center())
        return VGroup(oval, label)

    def create_rectangle(self, text, width=2.4, height=0.7):
        """Create a rectangle (process) with text"""
        rect = Rectangle(width=width, height=height, color=self.SHAPE_COLOR,
                        fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=16, color=BLACK)
        label.move_to(rect.get_center())
        if label.width > width - 0.2:
            label.scale((width - 0.2) / label.width)
        return VGroup(rect, label)

    def create_parallelogram(self, text, width=2.4, height=0.7):
        """Create a parallelogram (input/output) with text"""
        skew = 0.35
        points = [
            [-width/2 + skew, height/2, 0],
            [width/2 + skew, height/2, 0],
            [width/2 - skew, -height/2, 0],
            [-width/2 - skew, -height/2, 0],
        ]
        para = Polygon(*points, color=self.SHAPE_COLOR,
                       fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=16, color=BLACK)
        label.move_to(para.get_center())
        if label.width > width - 0.4:
            label.scale((width - 0.4) / label.width)
        return VGroup(para, label)

    def create_diamond(self, text, width=2.2, height=1.2):
        """Create a diamond (decision) with text"""
        points = [
            [0, height/2, 0],
            [width/2, 0, 0],
            [0, -height/2, 0],
            [-width/2, 0, 0],
        ]
        diamond = Polygon(*points, color=self.SHAPE_COLOR,
                         fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=14, color=BLACK)
        label.move_to(diamond.get_center())
        if label.width > width - 0.5:
            label.scale((width - 0.5) / label.width)
        return VGroup(diamond, label)

    def create_arrow(self, start, end):
        """Create a flow arrow between two points"""
        return Arrow(start, end, color=self.SHAPE_COLOR, stroke_width=3,
                    buff=0, max_tip_length_to_length_ratio=0.15)

    def title_scene(self):
        """Opening title"""
        title = Text("Flow Diagram", font_size=56, color=BLUE)
        subtitle = Text("How to Program a Robot to Open a Door",
                       font_size=32, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title, run_time=1))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def legend_scene(self):
        """Show the flowchart symbol legend"""
        header = Text("Flowchart Symbols", font_size=40, color=BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header))

        # Create legend items
        oval = self.create_oval("Start/End", width=1.8, height=0.55)
        oval_desc = Text("Oval = Start or End point", font_size=18, color=WHITE)

        arrow = Arrow(LEFT * 0.7, RIGHT * 0.7, color=self.SHAPE_COLOR, stroke_width=3)
        arrow_desc = Text("Arrow = Flow direction", font_size=18, color=WHITE)

        para = self.create_parallelogram("Input", width=1.8, height=0.55)
        para_desc = Text("Parallelogram = Input/Output", font_size=18, color=WHITE)

        rect = self.create_rectangle("Process", width=1.8, height=0.55)
        rect_desc = Text("Rectangle = Process step", font_size=18, color=WHITE)

        diamond = self.create_diamond("Decision?", width=1.6, height=0.9)
        diamond_desc = Text("Diamond = Decision point", font_size=18, color=WHITE)

        items = [
            (oval, oval_desc),
            (arrow, arrow_desc),
            (para, para_desc),
            (rect, rect_desc),
            (diamond, diamond_desc),
        ]

        y_positions = [2, 1, 0, -1, -2.1]

        for i, (shape, desc) in enumerate(items):
            shape.move_to(LEFT * 3 + UP * y_positions[i])
            desc.next_to(shape, RIGHT, buff=0.7)

        for shape, desc in items:
            self.play(
                FadeIn(shape, scale=0.8),
                FadeIn(desc, shift=RIGHT * 0.3),
                run_time=0.5
            )

        self.wait(1.5)

        all_items = VGroup(header, *[item for pair in items for item in pair])
        self.play(FadeOut(all_items))

    def flowchart_scene(self):
        """Main flowchart animation - simplified vertical layout"""
        header = Text("Robot Door Opening Algorithm", font_size=32, color=BLUE)
        header.to_edge(UP, buff=0.2)
        self.play(Write(header))

        # Vertical spacing
        v_gap = 0.35
        scale = 0.8

        # Column positions
        left_col = LEFT * 3.5
        center_col = ORIGIN
        right_col = RIGHT * 3.5

        # START
        start = self.create_oval("START")
        start.scale(scale).move_to(UP * 3 + left_col)

        # Process 1: Approach door
        approach = self.create_rectangle("Approach door")
        approach.scale(scale).next_to(start, DOWN, buff=v_gap)

        # Input: Detect handle (sensor input)
        detect = self.create_parallelogram("Detect handle")
        detect.scale(scale).next_to(approach, DOWN, buff=v_gap)

        # Decision 1: Is door locked?
        locked_q = self.create_diamond("Locked?")
        locked_q.scale(scale).next_to(detect, DOWN, buff=v_gap)

        # Branch: Unlock door (Yes path)
        unlock = self.create_rectangle("Unlock door")
        unlock.scale(scale).next_to(locked_q, RIGHT, buff=0.7)

        # Process: Grip handle
        grip = self.create_rectangle("Grip handle")
        grip.scale(scale).next_to(locked_q, DOWN, buff=0.5)

        # Process: Turn handle
        turn = self.create_rectangle("Turn handle")
        turn.scale(scale).move_to(center_col + UP * 1.5)

        # Decision 2: Push or Pull?
        push_pull_q = self.create_diamond("Push or Pull?")
        push_pull_q.scale(scale).next_to(turn, DOWN, buff=v_gap)

        # Process: Push door
        push_door = self.create_rectangle("Push door")
        push_door.scale(scale).next_to(push_pull_q, LEFT, buff=0.6)

        # Process: Pull door
        pull_door = self.create_rectangle("Pull door")
        pull_door.scale(scale).next_to(push_pull_q, RIGHT, buff=0.6)

        # Decision 3: Door open?
        open_q = self.create_diamond("Door open?")
        open_q.scale(scale).next_to(push_pull_q, DOWN, buff=0.5)

        # Process: Move through
        move = self.create_rectangle("Move through")
        move.scale(scale).next_to(open_q, DOWN, buff=0.5)

        # END
        end = self.create_oval("END")
        end.scale(scale).next_to(move, DOWN, buff=v_gap)

        # Create all arrows
        def arrow(s, e):
            return Arrow(s, e, color=self.SHAPE_COLOR, stroke_width=2.5, buff=0,
                        max_tip_length_to_length_ratio=0.12)

        def label_text(txt, color=WHITE):
            return Text(txt, font_size=12, color=color)

        # Main flow arrows
        arr_start_approach = arrow(start.get_bottom(), approach.get_top())
        arr_approach_detect = arrow(approach.get_bottom(), detect.get_top())
        arr_detect_locked = arrow(detect.get_bottom(), locked_q.get_top())

        # Locked? -> Yes -> Unlock
        arr_locked_unlock = arrow(locked_q.get_right(), unlock.get_left())
        yes1 = label_text("Yes", GREEN).next_to(arr_locked_unlock, UP, buff=0.02)

        # Locked? -> No -> Grip
        arr_locked_grip = arrow(locked_q.get_bottom(), grip.get_top())
        no1 = label_text("No", RED).next_to(arr_locked_grip, LEFT, buff=0.02)

        # Unlock rejoins to Grip (line down then left)
        unlock_join = VGroup(
            Line(unlock.get_bottom(), unlock.get_bottom() + DOWN * 0.25,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Arrow(unlock.get_bottom() + DOWN * 0.25, grip.get_right(),
                  color=self.SHAPE_COLOR, stroke_width=2.5, buff=0)
        )

        # Grip -> Turn
        arr_grip_turn = arrow(grip.get_bottom(),
                              grip.get_bottom() + DOWN * 0.3)
        arr_grip_turn2 = arrow(grip.get_bottom() + DOWN * 0.3 + RIGHT * (turn.get_center()[0] - grip.get_center()[0]),
                               turn.get_top())
        grip_turn_line = Line(grip.get_bottom() + DOWN * 0.3,
                              grip.get_bottom() + DOWN * 0.3 + RIGHT * (turn.get_center()[0] - grip.get_center()[0]),
                              color=self.SHAPE_COLOR, stroke_width=2.5)
        grip_to_turn = VGroup(arr_grip_turn, grip_turn_line, arr_grip_turn2)

        # Turn -> Push/Pull?
        arr_turn_pp = arrow(turn.get_bottom(), push_pull_q.get_top())

        # Push/Pull? -> Push
        arr_pp_push = arrow(push_pull_q.get_left(), push_door.get_right())
        push_lbl = label_text("Push", BLUE).next_to(arr_pp_push, UP, buff=0.02)

        # Push/Pull? -> Pull
        arr_pp_pull = arrow(push_pull_q.get_right(), pull_door.get_left())
        pull_lbl = label_text("Pull", BLUE).next_to(arr_pp_pull, UP, buff=0.02)

        # Push/Pull -> Door open? (both converge)
        push_to_open = VGroup(
            Line(push_door.get_bottom(), push_door.get_bottom() + DOWN * 0.3,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Line(push_door.get_bottom() + DOWN * 0.3, open_q.get_left() + LEFT * 0.1 + UP * 0.1,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Arrow(open_q.get_left() + LEFT * 0.1 + UP * 0.1, open_q.get_left(),
                  color=self.SHAPE_COLOR, stroke_width=2.5, buff=0)
        )

        pull_to_open = VGroup(
            Line(pull_door.get_bottom(), pull_door.get_bottom() + DOWN * 0.3,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Line(pull_door.get_bottom() + DOWN * 0.3, open_q.get_right() + RIGHT * 0.1 + UP * 0.1,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Arrow(open_q.get_right() + RIGHT * 0.1 + UP * 0.1, open_q.get_right(),
                  color=self.SHAPE_COLOR, stroke_width=2.5, buff=0)
        )

        # Door open? -> Yes -> Move
        arr_open_move = arrow(open_q.get_bottom(), move.get_top())
        yes2 = label_text("Yes", GREEN).next_to(arr_open_move, LEFT, buff=0.02)

        # Door open? -> No (loop back to Push/Pull?)
        no_loop = VGroup(
            Line(open_q.get_right() + DOWN * 0.15, open_q.get_right() + RIGHT * 1.2 + DOWN * 0.15,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Line(open_q.get_right() + RIGHT * 1.2 + DOWN * 0.15,
                 push_pull_q.get_right() + RIGHT * 1.2,
                 color=self.SHAPE_COLOR, stroke_width=2.5),
            Arrow(push_pull_q.get_right() + RIGHT * 1.2,
                  push_pull_q.get_right() + RIGHT * 0.05,
                  color=self.SHAPE_COLOR, stroke_width=2.5, buff=0)
        )
        no2 = label_text("No", RED).move_to(open_q.get_right() + RIGHT * 0.7)

        # Move -> END
        arr_move_end = arrow(move.get_bottom(), end.get_top())

        # Animate the flowchart
        # Section 1: Start to first decision
        self.play(FadeIn(start, scale=0.8), run_time=0.4)
        self.play(Create(arr_start_approach), run_time=0.25)
        self.play(FadeIn(approach, scale=0.8), run_time=0.4)
        self.play(Create(arr_approach_detect), run_time=0.25)
        self.play(FadeIn(detect, scale=0.8), run_time=0.4)
        self.play(Create(arr_detect_locked), run_time=0.25)
        self.play(FadeIn(locked_q, scale=0.8), run_time=0.4)

        # Section 2: Locked decision branches
        self.play(Create(arr_locked_unlock), FadeIn(yes1), run_time=0.3)
        self.play(FadeIn(unlock, scale=0.8), run_time=0.4)
        self.play(Create(unlock_join), run_time=0.3)

        self.play(Create(arr_locked_grip), FadeIn(no1), run_time=0.3)
        self.play(FadeIn(grip, scale=0.8), run_time=0.4)

        # Section 3: Grip to Push/Pull decision
        self.play(Create(grip_to_turn), run_time=0.4)
        self.play(FadeIn(turn, scale=0.8), run_time=0.4)
        self.play(Create(arr_turn_pp), run_time=0.25)
        self.play(FadeIn(push_pull_q, scale=0.8), run_time=0.4)

        # Section 4: Push/Pull branches
        self.play(
            Create(arr_pp_push), FadeIn(push_lbl),
            Create(arr_pp_pull), FadeIn(pull_lbl),
            run_time=0.4
        )
        self.play(
            FadeIn(push_door, scale=0.8),
            FadeIn(pull_door, scale=0.8),
            run_time=0.4
        )

        # Section 5: Converge to Door open?
        self.play(Create(push_to_open), Create(pull_to_open), run_time=0.4)
        self.play(FadeIn(open_q, scale=0.8), run_time=0.4)

        # Section 6: Door open decision
        self.play(Create(no_loop), FadeIn(no2), run_time=0.4)
        self.play(Create(arr_open_move), FadeIn(yes2), run_time=0.3)
        self.play(FadeIn(move, scale=0.8), run_time=0.4)
        self.play(Create(arr_move_end), run_time=0.25)
        self.play(FadeIn(end, scale=0.8), run_time=0.4)

        self.wait(1.5)

        # Success message
        success_msg = Text("Robot successfully opens the door!", font_size=26, color=GREEN)
        success_msg.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(success_msg, shift=UP))

        self.wait(2)
