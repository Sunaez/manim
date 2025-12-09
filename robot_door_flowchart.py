from manim import *

config.frame_rate = 30  # Ensure 30fps minimum
config.background_color = "#fff4ed"  # Light cream background


class RobotDoorFlowchart(MovingCameraScene):
    """
    Flow diagram animation showing how to program a robot to open a door.
    Uses standard flowchart symbols:
    - Oval: start/end
    - Rectangle: process
    - Parallelogram: input/output
    - Diamond: decision
    - Arrow: flow direction

    Light theme with scrolling vertical layout.
    """

    # Light mode color scheme
    SHAPE_STROKE = "#2B7A9E"    # Darker blue for borders
    SHAPE_FILL = "#B8E0F0"      # Light blue fill
    ARROW_COLOR = "#2B7A9E"     # Darker blue for arrows
    TEXT_COLOR = "#1a1a1a"      # Near black for text
    LABEL_YES = "#2E8B57"       # Sea green for Yes
    LABEL_NO = "#C75050"        # Muted red for No
    LABEL_BRANCH = "#5B5EA6"    # Muted purple-blue for branch labels
    HEADER_COLOR = "#2B5F7A"    # Dark blue for headers

    def construct(self):
        # Title scene
        self.title_scene()
        self.wait(1)
        self.clear()

        # Legend/key explanation
        self.legend_scene()
        self.wait(1)
        self.clear()

        # Main flowchart with scrolling
        self.flowchart_scene()
        self.wait(2)

    def create_oval(self, text, width=2.5, height=0.8):
        """Create an oval (start/end) with text"""
        oval = Ellipse(width=width, height=height, color=self.SHAPE_STROKE,
                       fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=22, color=self.TEXT_COLOR, weight=BOLD)
        label.move_to(oval.get_center())
        return VGroup(oval, label)

    def create_rectangle(self, text, width=3.0, height=0.9):
        """Create a rectangle (process) with text"""
        rect = Rectangle(width=width, height=height, color=self.SHAPE_STROKE,
                        fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=20, color=self.TEXT_COLOR)
        label.move_to(rect.get_center())
        if label.width > width - 0.3:
            label.scale((width - 0.3) / label.width)
        return VGroup(rect, label)

    def create_parallelogram(self, text, width=3.0, height=0.9):
        """Create a parallelogram (input/output) with text"""
        skew = 0.4
        points = [
            [-width/2 + skew, height/2, 0],
            [width/2 + skew, height/2, 0],
            [width/2 - skew, -height/2, 0],
            [-width/2 - skew, -height/2, 0],
        ]
        para = Polygon(*points, color=self.SHAPE_STROKE,
                       fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=20, color=self.TEXT_COLOR)
        label.move_to(para.get_center())
        if label.width > width - 0.5:
            label.scale((width - 0.5) / label.width)
        return VGroup(para, label)

    def create_diamond(self, text, width=2.8, height=1.5):
        """Create a diamond (decision) with text"""
        points = [
            [0, height/2, 0],
            [width/2, 0, 0],
            [0, -height/2, 0],
            [-width/2, 0, 0],
        ]
        diamond = Polygon(*points, color=self.SHAPE_STROKE,
                         fill_color=self.SHAPE_FILL, fill_opacity=1, stroke_width=3)
        label = Text(text, font_size=18, color=self.TEXT_COLOR)
        label.move_to(diamond.get_center())
        if label.width > width - 0.6:
            label.scale((width - 0.6) / label.width)
        return VGroup(diamond, label)

    def create_arrow(self, start, end):
        """Create a flow arrow between two points"""
        return Arrow(start, end, color=self.ARROW_COLOR, stroke_width=3,
                    buff=0, max_tip_length_to_length_ratio=0.12)

    def title_scene(self):
        """Opening title"""
        title = Text("Flow Diagram", font_size=60, color=self.HEADER_COLOR, weight=BOLD)
        subtitle = Text("How to Program a Robot to Open a Door",
                       font_size=34, color=self.TEXT_COLOR)
        subtitle.next_to(title, DOWN, buff=0.6)

        self.play(Write(title, run_time=2))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(title, shift=UP), FadeOut(subtitle, shift=UP), run_time=1.5)

    def legend_scene(self):
        """Show the flowchart symbol legend"""
        header = Text("Flowchart Symbols", font_size=44, color=self.HEADER_COLOR, weight=BOLD)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        self.wait(0.5)

        # Create legend items
        oval = self.create_oval("Start/End", width=2.2, height=0.7)
        oval_desc = Text("Oval = Start or End point", font_size=22, color=self.TEXT_COLOR)

        arrow = Arrow(LEFT * 0.9, RIGHT * 0.9, color=self.ARROW_COLOR, stroke_width=3)
        arrow_desc = Text("Arrow = Flow direction", font_size=22, color=self.TEXT_COLOR)

        para = self.create_parallelogram("Input", width=2.2, height=0.7)
        para_desc = Text("Parallelogram = Input/Output", font_size=22, color=self.TEXT_COLOR)

        rect = self.create_rectangle("Process", width=2.2, height=0.7)
        rect_desc = Text("Rectangle = Process step", font_size=22, color=self.TEXT_COLOR)

        diamond = self.create_diamond("Decision?", width=2.0, height=1.1)
        diamond_desc = Text("Diamond = Decision point", font_size=22, color=self.TEXT_COLOR)

        items = [
            (oval, oval_desc),
            (arrow, arrow_desc),
            (para, para_desc),
            (rect, rect_desc),
            (diamond, diamond_desc),
        ]

        y_positions = [2, 0.9, -0.2, -1.3, -2.5]

        for i, (shape, desc) in enumerate(items):
            shape.move_to(LEFT * 3.2 + UP * y_positions[i])
            desc.next_to(shape, RIGHT, buff=0.9)

        for shape, desc in items:
            self.play(
                FadeIn(shape, scale=0.8),
                FadeIn(desc, shift=RIGHT * 0.3),
                run_time=1.0
            )
            self.wait(0.5)

        self.wait(2)

        all_items = VGroup(header, *[item for pair in items for item in pair])
        self.play(FadeOut(all_items), run_time=1.5)

    def flowchart_scene(self):
        """Main flowchart animation - vertical layout with camera scrolling"""
        header = Text("Robot Door Opening Flow Diagram", font_size=36,
                     color=self.HEADER_COLOR, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=1.5)
        self.wait(1)

        # Vertical spacing between elements
        v_gap = 0.6
        h_offset = 3.8  # Horizontal offset for branches (wider to avoid clipping)

        # Build the flowchart - all elements positioned vertically
        # We'll create everything first, then animate with camera movement

        # Starting Y position (top of flowchart)
        current_y = 2.0

        # START
        start = self.create_oval("START")
        start.move_to(UP * current_y)

        current_y -= 1.2

        # Process 1: Approach door
        approach = self.create_rectangle("Approach door")
        approach.move_to(UP * current_y)
        arr_start_approach = self.create_arrow(start.get_bottom(), approach.get_top())

        current_y -= 1.3

        # Input: Detect handle
        detect = self.create_parallelogram("Detect handle")
        detect.move_to(UP * current_y)
        arr_approach_detect = self.create_arrow(approach.get_bottom(), detect.get_top())

        current_y -= 1.4

        # Decision 1: Locked?
        locked_q = self.create_diamond("Locked?")
        locked_q.move_to(UP * current_y)
        arr_detect_locked = self.create_arrow(detect.get_bottom(), locked_q.get_top())

        # Branch: Unlock door (Yes - to the right)
        unlock = self.create_rectangle("Unlock door")
        unlock.move_to(UP * current_y + RIGHT * h_offset)
        arr_locked_unlock = self.create_arrow(locked_q.get_right(), unlock.get_left())
        yes1 = Text("Yes", font_size=16, color=self.LABEL_YES, weight=BOLD)
        yes1.next_to(arr_locked_unlock, UP, buff=0.08)

        current_y -= 1.6

        # Process: Grip handle
        grip = self.create_rectangle("Grip handle")
        grip.move_to(UP * current_y)
        arr_locked_grip = self.create_arrow(locked_q.get_bottom(), grip.get_top())
        no1 = Text("No", font_size=16, color=self.LABEL_NO, weight=BOLD)
        no1.next_to(arr_locked_grip, LEFT, buff=0.08)

        # Unlock rejoins to Grip
        unlock_join = VGroup(
            Line(unlock.get_bottom(), unlock.get_bottom() + DOWN * 0.4,
                 color=self.ARROW_COLOR, stroke_width=3),
            Arrow(unlock.get_bottom() + DOWN * 0.4, grip.get_right(),
                  color=self.ARROW_COLOR, stroke_width=3, buff=0)
        )

        current_y -= 1.3

        # Process: Turn handle
        turn = self.create_rectangle("Turn handle")
        turn.move_to(UP * current_y)
        arr_grip_turn = self.create_arrow(grip.get_bottom(), turn.get_top())

        current_y -= 1.5

        # Decision 2: Push or Pull?
        push_pull_q = self.create_diamond("Push or Pull?")
        push_pull_q.move_to(UP * current_y)
        arr_turn_pp = self.create_arrow(turn.get_bottom(), push_pull_q.get_top())

        # Process: Push door (left branch)
        push_door = self.create_rectangle("Push door")
        push_door.move_to(UP * current_y + LEFT * h_offset)
        arr_pp_push = self.create_arrow(push_pull_q.get_left(), push_door.get_right())
        push_lbl = Text("Push", font_size=16, color=self.LABEL_BRANCH, weight=BOLD)
        push_lbl.next_to(arr_pp_push, UP, buff=0.08)

        # Process: Pull door (right branch)
        pull_door = self.create_rectangle("Pull door")
        pull_door.move_to(UP * current_y + RIGHT * h_offset)
        arr_pp_pull = self.create_arrow(push_pull_q.get_right(), pull_door.get_left())
        pull_lbl = Text("Pull", font_size=16, color=self.LABEL_BRANCH, weight=BOLD)
        pull_lbl.next_to(arr_pp_pull, UP, buff=0.08)

        current_y -= 1.6

        # Decision 3: Door open?
        open_q = self.create_diamond("Door open?")
        open_q.move_to(UP * current_y)

        # Push converges to Door open?
        push_to_open = VGroup(
            Line(push_door.get_bottom(), push_door.get_bottom() + DOWN * 0.5,
                 color=self.ARROW_COLOR, stroke_width=3),
            Line(push_door.get_bottom() + DOWN * 0.5,
                 [open_q.get_left()[0] - 0.2, push_door.get_bottom()[1] - 0.5, 0],
                 color=self.ARROW_COLOR, stroke_width=3),
            Arrow([open_q.get_left()[0] - 0.2, push_door.get_bottom()[1] - 0.5, 0],
                  open_q.get_left(),
                  color=self.ARROW_COLOR, stroke_width=3, buff=0)
        )

        # Pull converges to Door open?
        pull_to_open = VGroup(
            Line(pull_door.get_bottom(), pull_door.get_bottom() + DOWN * 0.5,
                 color=self.ARROW_COLOR, stroke_width=3),
            Line(pull_door.get_bottom() + DOWN * 0.5,
                 [open_q.get_right()[0] + 0.2, pull_door.get_bottom()[1] - 0.5, 0],
                 color=self.ARROW_COLOR, stroke_width=3),
            Arrow([open_q.get_right()[0] + 0.2, pull_door.get_bottom()[1] - 0.5, 0],
                  open_q.get_right(),
                  color=self.ARROW_COLOR, stroke_width=3, buff=0)
        )

        current_y -= 1.5

        # Process: Move through
        move = self.create_rectangle("Move through doorway")
        move.move_to(UP * current_y)
        arr_open_move = self.create_arrow(open_q.get_bottom(), move.get_top())
        yes2 = Text("Yes", font_size=16, color=self.LABEL_YES, weight=BOLD)
        yes2.next_to(arr_open_move, LEFT, buff=0.08)

        current_y -= 1.2

        # END
        end = self.create_oval("END")
        end.move_to(UP * current_y)
        arr_move_end = self.create_arrow(move.get_bottom(), end.get_top())

        # Animate step by step - camera centers on each new element

        # Step 1: START
        self.play(
            self.camera.frame.animate.move_to(start.get_center()),
            run_time=0.5
        )
        self.play(FadeIn(start, scale=0.8), run_time=1.0)
        self.wait(1)

        # Step 2: Approach door
        self.play(Create(arr_start_approach), run_time=0.8)
        self.play(
            FadeIn(approach, scale=0.8),
            self.camera.frame.animate.move_to(approach.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 3: Detect handle
        self.play(Create(arr_approach_detect), run_time=0.8)
        self.play(
            FadeIn(detect, scale=0.8),
            self.camera.frame.animate.move_to(detect.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 4: Locked? decision
        self.play(Create(arr_detect_locked), run_time=0.8)
        self.play(
            FadeIn(locked_q, scale=0.8),
            self.camera.frame.animate.move_to(locked_q.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 5: Yes branch - Unlock door
        self.play(
            Create(arr_locked_unlock),
            FadeIn(yes1),
            run_time=1.0
        )
        self.play(
            FadeIn(unlock, scale=0.8),
            self.camera.frame.animate.move_to(unlock.get_center()),
            run_time=1.0
        )
        self.wait(0.8)
        self.play(Create(unlock_join), run_time=0.8)
        self.wait(0.5)

        # Step 6: No branch - Grip handle
        self.play(
            Create(arr_locked_grip),
            FadeIn(no1),
            run_time=1.0
        )
        self.play(
            FadeIn(grip, scale=0.8),
            self.camera.frame.animate.move_to(grip.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 7: Turn handle
        self.play(Create(arr_grip_turn), run_time=0.8)
        self.play(
            FadeIn(turn, scale=0.8),
            self.camera.frame.animate.move_to(turn.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 8: Push or Pull? decision
        self.play(Create(arr_turn_pp), run_time=0.8)
        self.play(
            FadeIn(push_pull_q, scale=0.8),
            self.camera.frame.animate.move_to(push_pull_q.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 9: Push and Pull branches
        self.play(
            Create(arr_pp_push),
            FadeIn(push_lbl),
            Create(arr_pp_pull),
            FadeIn(pull_lbl),
            run_time=1.2
        )
        self.play(
            FadeIn(push_door, scale=0.8),
            FadeIn(pull_door, scale=0.8),
            run_time=1.0
        )
        self.wait(1)

        # Step 10: Converge to Door open?
        self.play(
            Create(push_to_open),
            Create(pull_to_open),
            run_time=1.2
        )
        self.play(
            FadeIn(open_q, scale=0.8),
            self.camera.frame.animate.move_to(open_q.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 11: Yes path - Move through
        self.play(
            Create(arr_open_move),
            FadeIn(yes2),
            run_time=1.0
        )
        self.play(
            FadeIn(move, scale=0.8),
            self.camera.frame.animate.move_to(move.get_center()),
            run_time=1.0
        )
        self.wait(1)

        # Step 12: END
        self.play(Create(arr_move_end), run_time=0.8)
        self.play(
            FadeIn(end, scale=0.8),
            self.camera.frame.animate.move_to(end.get_center()),
            run_time=1.0
        )
        self.wait(2)

        # Final view: Zoom out to show entire diagram (START at top, END at bottom)
        self.play(
            FadeOut(header),
            run_time=1.0
        )

        # Calculate center and height to fit full diagram
        diagram_center = (start.get_center() + end.get_center()) / 2
        diagram_height = start.get_center()[1] - end.get_center()[1] + 2

        self.play(
            self.camera.frame.animate.move_to(diagram_center).set(height=diagram_height + 1),
            run_time=2.5
        )

        self.wait(3)
