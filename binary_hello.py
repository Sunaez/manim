from manim import *

class BinaryToText(Scene):
    def construct(self):
        # Binary representation of "Hello"
        # H=01001000, e=01100101, l=01101100, l=01101100, o=01101111
        binary_string = "01001000 01100101 01101100 01101100 01101111"

        # Create title
        title = Text("Binary to Text Decoder", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create the binary text
        binary_text = Text(binary_string, font_size=32, font="Courier New")
        binary_text.move_to(ORIGIN + RIGHT * 8)  # Start off-screen to the right

        # Create the read header (a rectangular frame)
        read_header = Rectangle(
            height=1.2,
            width=3,
            color=YELLOW,
            stroke_width=4
        )
        read_header.move_to(ORIGIN)

        # Add label for read header
        header_label = Text("Read Header", font_size=24, color=YELLOW)
        header_label.next_to(read_header, UP, buff=0.3)

        # Create output area
        output_label = Text("Output: ", font_size=28)
        output_label.move_to(DOWN * 2 + LEFT * 2)

        output_text = Text("", font_size=32, color=GREEN)
        output_text.next_to(output_label, RIGHT)

        # Display read header and output area
        self.play(
            Create(read_header),
            Write(header_label),
            Write(output_label)
        )
        self.wait(0.5)

        # Display the binary text
        self.play(FadeIn(binary_text))
        self.wait(0.5)

        # Split binary into individual characters for letter-by-letter decoding
        letters = ["H", "e", "l", "l", "o"]
        binary_groups = binary_string.split()

        # Animate binary moving from right to left through the read header
        # and decode each byte as it passes through
        animation_duration = 8

        # Move binary through the read header
        for i, (binary_byte, letter) in enumerate(zip(binary_groups, letters)):
            # Calculate position where this byte should be centered in the read header
            # We need to move the entire binary text so the current byte aligns with the header
            byte_position_in_text = binary_text.get_left()[0] + (i * 2.3)  # Approximate spacing
            target_x = read_header.get_center()[0] - byte_position_in_text

            # Animate movement
            self.play(
                binary_text.animate.shift(LEFT * abs(target_x - binary_text.get_center()[0])),
                run_time=1.5,
                rate_func=linear
            )

            # Flash the read header to show it's reading
            self.play(
                read_header.animate.set_color(RED),
                run_time=0.2
            )
            self.play(
                read_header.animate.set_color(YELLOW),
                run_time=0.2
            )

            # Add the decoded letter to output
            new_output = Text(letter, font_size=32, color=GREEN)
            if i == 0:
                new_output.next_to(output_label, RIGHT)
            else:
                new_output.next_to(output_text, RIGHT, buff=0.1)

            self.play(FadeIn(new_output), run_time=0.3)

            # Update output_text to include the new letter
            if i == 0:
                output_text = new_output
            else:
                output_group = VGroup(output_text, new_output)
                output_text = output_group

            self.wait(0.3)

        # Final wait to show complete result
        self.wait(2)

        # Highlight the final output
        self.play(
            output_text.animate.scale(1.3).set_color(BLUE),
            run_time=0.5
        )
        self.wait(2)
