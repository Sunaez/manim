from manim import *

class BinaryToText(Scene):
    def construct(self):
        # Binary representation of "Hello"
        # H=01001000, e=01100101, l=01101100, l=01101100, o=01101111
        binary_string = "01001000 01100101 01101100 01101100 01101111"

        # Create title using Tex for LaTeX formatting
        title = Tex(r"\textbf{Binary to Text Decoder}", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create the binary text using Tex for monospace formatting
        binary_text = Tex(
            r"\texttt{01001000}", r"\;",
            r"\texttt{01100101}", r"\;",
            r"\texttt{01101100}", r"\;",
            r"\texttt{01101100}", r"\;",
            r"\texttt{01101111}",
            font_size=36
        )
        binary_text.move_to(ORIGIN + RIGHT * 8)  # Start off-screen to the right

        # Create the read header (a rectangular frame)
        read_header = Rectangle(
            height=1.5,
            width=3.5,
            color=YELLOW,
            stroke_width=4
        )
        read_header.move_to(ORIGIN)

        # Add label for read header using Text (normal text)
        header_label = Text("Read Header", font_size=32, color=YELLOW)
        header_label.next_to(read_header, UP, buff=0.3)

        # Create output area using Text (normal text)
        output_label = Text("Output:", font_size=36, weight=BOLD)
        output_label.move_to(DOWN * 2 + LEFT * 2)

        output_text = Text("", font_size=36, color=GREEN)
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

        # Add binary annotations using Text (normal text)
        letter_labels = VGroup(*[
            Text(letter, font_size=24, color=GRAY)
            for letter in letters
        ])
        letter_labels.arrange(RIGHT, buff=0.5)
        letter_labels.move_to(binary_text.get_center() + DOWN * 0.8)
        self.play(FadeIn(letter_labels, shift=UP * 0.2))
        self.wait(0.3)

        # Move binary through the read header
        # Since Tex creates separate submobjects, we get the indices of actual binary bytes (even indices)
        binary_indices = [0, 2, 4, 6, 8]  # Indices of binary bytes in Tex

        for i, (binary_idx, binary_byte, letter) in enumerate(zip(binary_indices, binary_groups, letters)):
            # Get the position of the current binary byte
            current_byte = binary_text[binary_idx]

            # Calculate how much to shift to center this byte in the read header
            byte_center = current_byte.get_center()[0]
            header_center = read_header.get_center()[0]
            shift_amount = header_center - byte_center

            # Animate movement of both binary text and letter labels together
            self.play(
                binary_text.animate.shift(RIGHT * shift_amount),
                letter_labels.animate.shift(RIGHT * shift_amount),
                run_time=1.5,
                rate_func=linear
            )

            # Flash the read header to show it's reading
            self.play(
                read_header.animate.set_color(RED),
                current_byte.animate.set_color(RED),
                run_time=0.2
            )
            self.play(
                read_header.animate.set_color(YELLOW),
                current_byte.animate.set_color(WHITE),
                run_time=0.2
            )

            # Show binary to decimal conversion using MathTex (equation)
            decimal_value = int(binary_byte, 2)
            conversion = MathTex(
                r"\texttt{" + binary_byte + r"}_2",
                r"=",
                str(decimal_value) + r"_{10}",
                r"=",
                r"\text{``" + letter + r"''}",
                font_size=28,
                color=ORANGE
            )
            conversion.next_to(read_header, RIGHT, buff=0.5)
            self.play(FadeIn(conversion, shift=LEFT * 0.3), run_time=0.4)
            self.wait(0.3)

            # Add the decoded letter to output using Text (normal text with font)
            new_output = Text(letter, font_size=40, font="Monospace", color=GREEN, weight=BOLD)
            if i == 0:
                new_output.next_to(output_label, RIGHT, buff=0.2)
            else:
                new_output.next_to(output_text, RIGHT, buff=0.05)

            self.play(
                FadeIn(new_output, scale=1.5),
                FadeOut(conversion),
                run_time=0.4
            )

            # Update output_text to include the new letter
            if i == 0:
                output_text = new_output
            else:
                output_group = VGroup(output_text, new_output)
                output_text = output_group

            self.wait(0.3)

        # Final wait to show complete result
        self.wait(1)

        # Add completion checkmark using MathTex (math symbol/equation)
        checkmark = MathTex(r"\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(output_text, RIGHT, buff=0.3)

        # Highlight the final output with Tex (LaTeX formatting)
        final_text = Tex(
            r"\Large\textbf{Decoded: ``Hello''}",
            font_size=48,
            color=BLUE
        )
        final_text.move_to(DOWN * 3)

        self.play(
            FadeIn(checkmark, scale=2),
            Write(final_text),
            output_text.animate.set_color(BLUE),
            run_time=0.8
        )
        self.wait(2)
