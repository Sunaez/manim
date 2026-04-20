from pathlib import Path
import subprocess
import sys

from manim import *

from palette import apply_palette

FRAME_RATE = 30
RENDER_QUALITY = "medium"
# low: preview quality.
# medium: standard render quality.
# high: final render quality.
COLOR_SCHEME = "Dark"

config.frame_rate = FRAME_RATE

P = apply_palette(COLOR_SCHEME)
BACKGROUND = P.BG_0
SURFACE = P.BG_1
SURFACE_ALT = P.BG_2
TEXT = P.TEXT_PRIMARY
MUTED = P.TEXT_SECONDARY
FAINT = P.TEXT_FAINT
BORDER = P.BORDER
ACTIVE = P.CYAN
ACTIVE_SOFT = P.CYAN_SOFT
SWAP = P.AMBER
SWAP_SOFT = P.AMBER_SOFT
SUCCESS = P.GREEN
SUCCESS_SOFT = P.GREEN_SOFT


class BubbleSortWorks(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        values = [5, 3, 8, 4, 2]
        tiles, current_values, positions = self.build_row(values)

        self.title_sequence()
        self.show_unsorted_list(tiles)
        self.rule_sequence(tiles)
        self.first_comparison_sequence(tiles, current_values, positions)
        self.first_pass_sequence(tiles, current_values, positions)
        self.end_of_first_pass_sequence(tiles)
        self.pass_label_sequence()
        self.second_pass_sequence(tiles, current_values, positions)
        self.remaining_passes_sequence(tiles, current_values, positions)
        self.final_sorted_sequence(tiles)
        self.summary_sequence()
        self.wait(1.2)

    def title_sequence(self):
        title = Text("How Bubble Sort Works", font_size=38, color=TEXT, weight=BOLD)
        subtitle = Text("Compare neighbours, swap if needed, repeat", font_size=22, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.18)
        line = Line(LEFT * 4.8, RIGHT * 4.8, color=ACTIVE, stroke_width=3)
        line.next_to(subtitle, DOWN, buff=0.18)
        group = VGroup(title, subtitle, line)
        group.move_to(UP * 1.2)

        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(subtitle, shift=UP * 0.08), Create(line), run_time=0.85)
        self.wait(0.7)
        self.play(FadeOut(group, shift=UP * 0.25), run_time=0.85)

    def show_unsorted_list(self, tiles):
        label = self.section_chip("Unsorted list", ACTIVE)
        label.to_edge(UP, buff=0.42).shift(DOWN * 0.1)

        self.play(FadeIn(label, shift=UP * 0.06), run_time=0.45)
        self.play(
            LaggedStart(
                *[FadeIn(tile, shift=UP * 0.12) for tile in tiles],
                lag_ratio=0.14,
            ),
            run_time=1.0,
        )
        self.wait(1.0)
        self.play(FadeOut(label, shift=UP * 0.05), run_time=0.45)

    def rule_sequence(self, tiles):
        caption = self.statement("Bubble Sort compares neighbouring values.")
        caption.to_edge(UP, buff=0.38).shift(DOWN * 0.05)
        focus = self.pair_focus(tiles[0], tiles[1], ACTIVE)

        self.play(FadeIn(caption, shift=UP * 0.06), FadeIn(focus, scale=0.96), run_time=0.55)
        self.play(*self.tile_state_anims(tiles[0], "active"), *self.tile_state_anims(tiles[1], "active"), run_time=0.35)
        self.wait(0.8)

        next_caption = self.statement("If the left value is bigger, they swap.")
        next_caption.move_to(caption)
        compare_chip = self.section_chip("5 > 3", SWAP)
        compare_chip.next_to(focus, UP, buff=0.18)
        self.play(Transform(caption, next_caption), FadeIn(compare_chip, shift=UP * 0.04), run_time=0.6)
        self.play(Indicate(tiles[0], color=SWAP, scale_factor=1.04), run_time=0.65)
        self.wait(0.7)
        self.play(FadeOut(compare_chip, shift=UP * 0.04), run_time=0.35)

        final_caption = self.statement("This continues across the list.")
        final_caption.move_to(caption)
        self.play(Transform(caption, final_caption), run_time=0.55)
        self.wait(0.7)

        self.play(
            FadeOut(caption, shift=UP * 0.06),
            FadeOut(focus),
            *self.tile_state_anims(tiles[0], "unsorted"),
            *self.tile_state_anims(tiles[1], "unsorted"),
            run_time=0.6,
        )

    def first_comparison_sequence(self, tiles, values, positions):
        caption = self.statement("First comparison in detail.")
        caption.to_edge(UP, buff=0.38).shift(DOWN * 0.05)
        focus = self.pair_focus(tiles[0], tiles[1], ACTIVE)
        compare_chip = self.section_chip("5 > 3", SWAP)
        compare_chip.next_to(focus, UP, buff=0.18)
        prompt = self.statement("Left is bigger, so swap them.")
        prompt.move_to(caption)

        self.play(FadeIn(caption, shift=UP * 0.06), FadeIn(focus, scale=0.96), run_time=0.5)
        self.play(*self.tile_state_anims(tiles[0], "active"), *self.tile_state_anims(tiles[1], "active"), run_time=0.35)
        self.play(FadeIn(compare_chip, shift=UP * 0.04), run_time=0.3)
        self.wait(0.6)
        self.play(Transform(caption, prompt), run_time=0.45)
        self.play(
            tiles[0].box.animate.set_fill(SWAP_SOFT, opacity=1),
            tiles[0].box.animate.set_stroke(SWAP, width=2.8),
            tiles[1].box.animate.set_fill(SWAP_SOFT, opacity=1),
            tiles[1].box.animate.set_stroke(SWAP, width=2.8),
            run_time=0.35,
        )

        left = tiles[0]
        right = tiles[1]
        left_path = ArcBetweenPoints(left.get_center(), positions[1], angle=PI / 2)
        right_path = ArcBetweenPoints(right.get_center(), positions[0], angle=-PI / 2)
        self.play(
            MoveAlongPath(left, left_path),
            MoveAlongPath(right, right_path),
            run_time=0.95,
        )
        tiles[0], tiles[1] = right, left
        values[0], values[1] = values[1], values[0]

        self.play(
            *self.tile_state_anims(tiles[0], "unsorted"),
            *self.tile_state_anims(tiles[1], "unsorted"),
            FadeOut(compare_chip, shift=UP * 0.04),
            run_time=0.45,
        )
        next_focus = self.pair_focus(tiles[1], tiles[2], ACTIVE)
        self.play(Transform(focus, next_focus), run_time=0.55)
        self.play(Transform(caption, self.statement("Now the next pair can be checked.")), run_time=0.45)
        self.wait(0.5)
        self.play(FadeOut(caption, shift=UP * 0.06), FadeOut(focus), run_time=0.55)

    def first_pass_sequence(self, tiles, values, positions):
        # The list is now [3, 5, 8, 4, 2].
        self.compare_step(tiles, values, positions, 1, "5 and 8", swap=False, run_time=0.75)
        self.compare_step(tiles, values, positions, 2, "8 and 4", swap=True, run_time=0.9)
        self.compare_step(tiles, values, positions, 3, "8 and 2", swap=True, run_time=0.9)

    def end_of_first_pass_sequence(self, tiles):
        label = self.statement("Largest value is now in the correct position.")
        label.to_edge(UP, buff=0.38).shift(DOWN * 0.05)
        self.play(FadeIn(label, shift=UP * 0.06), run_time=0.55)
        self.mark_sorted(tiles[4], pulse=True)
        self.wait(0.9)
        self.play(FadeOut(label, shift=UP * 0.05), run_time=0.45)

    def pass_label_sequence(self):
        self.pass_chip = self.section_chip("Pass 1 complete", ACTIVE)
        self.pass_chip.to_corner(UR, buff=0.35)
        self.play(FadeIn(self.pass_chip, shift=UP * 0.05), run_time=0.45)
        self.wait(0.35)

        next_chip = self.section_chip("Pass 2", ACTIVE)
        next_chip.move_to(self.pass_chip)
        self.play(Transform(self.pass_chip, next_chip), run_time=0.55)
        self.wait(0.35)

    def second_pass_sequence(self, tiles, values, positions):
        # The sorted tile at the end remains locked in place.
        self.compare_step(tiles, values, positions, 0, "3 and 5", swap=False, run_time=0.7)
        self.compare_step(tiles, values, positions, 1, "5 and 4", swap=True, run_time=0.85)
        self.compare_step(tiles, values, positions, 2, "5 and 2", swap=True, run_time=0.85)
        self.mark_sorted(tiles[3], pulse=True)
        complete_chip = self.section_chip("Pass 2 complete", ACTIVE)
        complete_chip.move_to(self.pass_chip)
        self.play(Transform(self.pass_chip, complete_chip), run_time=0.55)
        self.wait(0.3)
        next_chip = self.section_chip("Pass 3", ACTIVE)
        next_chip.move_to(self.pass_chip)
        self.play(Transform(self.pass_chip, next_chip), run_time=0.5)

    def remaining_passes_sequence(self, tiles, values, positions):
        self.compare_step(tiles, values, positions, 0, "3 and 4", swap=False, run_time=0.65)
        self.compare_step(tiles, values, positions, 1, "4 and 2", swap=True, run_time=0.8)
        self.mark_sorted(tiles[2], pulse=True)

        complete_chip = self.section_chip("Pass 3 complete", ACTIVE)
        complete_chip.move_to(self.pass_chip)
        self.play(Transform(self.pass_chip, complete_chip), run_time=0.5)
        self.wait(0.25)

        next_chip = self.section_chip("Pass 4", ACTIVE)
        next_chip.move_to(self.pass_chip)
        self.play(Transform(self.pass_chip, next_chip), run_time=0.45)

        self.compare_step(tiles, values, positions, 0, "3 and 2", swap=True, run_time=0.75)
        self.mark_sorted(tiles[1], pulse=True)
        self.mark_sorted(tiles[0], pulse=True)
        complete_chip = self.section_chip("Pass 4 complete", ACTIVE)
        complete_chip.move_to(self.pass_chip)
        self.play(Transform(self.pass_chip, complete_chip), run_time=0.5)

    def final_sorted_sequence(self, tiles):
        highlight = SurroundingRectangle(VGroup(*tiles), color=SUCCESS, buff=0.2, corner_radius=0.18, stroke_width=4)
        highlight.set_fill(SUCCESS, opacity=0.06)
        self.play(Create(highlight), run_time=0.55)
        self.play(Indicate(VGroup(*tiles), color=SUCCESS, scale_factor=1.02), run_time=0.9)
        self.play(FadeOut(highlight), run_time=0.35)

    def summary_sequence(self):
        if hasattr(self, "pass_chip"):
            self.play(FadeOut(self.pass_chip, shift=UP * 0.05), run_time=0.4)

        panel = RoundedRectangle(width=11.0, height=2.2, corner_radius=0.22, color=ACTIVE, stroke_width=2)
        panel.set_fill(SURFACE, opacity=0.96)
        panel.move_to(DOWN * 2.35)

        summary_title = Text("Bubble Sort in four simple ideas", font_size=28, color=TEXT, weight=BOLD)
        summary_title.move_to(panel.get_top() + DOWN * 0.42 + LEFT * 0.9)

        lines = VGroup(
            Text("- compares neighbouring values", font_size=22, color=MUTED),
            Text("- swaps only when the order is wrong", font_size=22, color=MUTED),
            Text("- after each pass, one more value is finished", font_size=22, color=MUTED),
            Text("- easy to follow, but slow on large lists", font_size=22, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lines.move_to(panel.get_center() + LEFT * 1.8 + DOWN * 0.08)

        note = Text("Worst-case time complexity: O(n^2)", font_size=19, color=FAINT)
        note.next_to(panel, DOWN, buff=0.18)
        note.align_to(panel, LEFT)

        self.play(FadeIn(panel), FadeIn(summary_title, shift=UP * 0.06), run_time=0.8)
        self.play(FadeIn(lines[0], shift=UP * 0.04), run_time=0.45)
        self.wait(0.2)
        self.play(FadeIn(lines[1], shift=UP * 0.04), run_time=0.45)
        self.wait(0.2)
        self.play(FadeIn(lines[2], shift=UP * 0.04), run_time=0.45)
        self.wait(0.2)
        self.play(FadeIn(lines[3], shift=UP * 0.04), run_time=0.45)
        self.play(FadeIn(note, shift=UP * 0.04), run_time=0.4)
        self.wait(1.3)

    def compare_step(self, tiles, values, positions, index, label_text, swap, run_time=0.8):
        focus = self.pair_focus(tiles[index], tiles[index + 1], ACTIVE)
        label = self.section_chip(label_text, ACTIVE)
        label.next_to(focus, UP, buff=0.18)

        self.play(FadeIn(focus, scale=0.96), FadeIn(label, shift=UP * 0.05), run_time=0.45)
        self.play(*self.tile_state_anims(tiles[index], "active"), *self.tile_state_anims(tiles[index + 1], "active"), run_time=0.3)
        self.wait(0.45 if swap else 0.25)

        if swap:
            result = self.section_chip("Swap", SWAP)
            result.next_to(focus, DOWN, buff=0.18)
            self.play(FadeIn(result, shift=UP * 0.03), run_time=0.25)

            left = tiles[index]
            right = tiles[index + 1]
            self.play(
                left.box.animate.set_fill(SWAP_SOFT, opacity=1),
                left.box.animate.set_stroke(SWAP, width=2.8),
                right.box.animate.set_fill(SWAP_SOFT, opacity=1),
                right.box.animate.set_stroke(SWAP, width=2.8),
                run_time=0.25,
            )

            left_path = ArcBetweenPoints(left.get_center(), positions[index + 1], angle=PI / 2)
            right_path = ArcBetweenPoints(right.get_center(), positions[index], angle=-PI / 2)
            self.play(
                MoveAlongPath(left, left_path),
                MoveAlongPath(right, right_path),
                run_time=run_time,
            )
            tiles[index], tiles[index + 1] = right, left
            values[index], values[index + 1] = values[index + 1], values[index]

            self.play(FadeOut(result, shift=UP * 0.03), run_time=0.25)
        else:
            result = self.section_chip("Already in order", SUCCESS)
            result.next_to(focus, DOWN, buff=0.18)
            self.play(FadeIn(result, shift=UP * 0.03), run_time=0.25)
            self.play(Indicate(VGroup(tiles[index], tiles[index + 1]), color=SUCCESS, scale_factor=1.03), run_time=0.55)
            self.play(FadeOut(result, shift=UP * 0.03), run_time=0.25)

        self.play(
            *self.tile_state_anims(tiles[index], "unsorted"),
            *self.tile_state_anims(tiles[index + 1], "unsorted"),
            run_time=0.3,
        )

        self.play(FadeOut(label, shift=UP * 0.04), FadeOut(focus), run_time=0.45)

    def pair_focus(self, left_tile, right_tile, color):
        pair = VGroup(left_tile, right_tile)
        focus = RoundedRectangle(
            width=pair.width + 0.22,
            height=pair.height + 0.22,
            corner_radius=0.18,
            color=color,
            stroke_width=4,
        )
        focus.set_fill(color, opacity=0.08)
        focus.move_to(pair)
        focus.set_z_index(0)
        return focus

    def build_row(self, values):
        tiles = VGroup(*[self.make_tile(value) for value in values])
        tiles.arrange(RIGHT, buff=0.34)
        tiles.move_to(DOWN * 0.15)
        positions = [tile.get_center().copy() for tile in tiles]
        return list(tiles), list(values), positions

    def make_tile(self, value):
        box = RoundedRectangle(
            width=1.18,
            height=0.82,
            corner_radius=0.18,
            color=BORDER,
            stroke_width=2.6,
        )
        box.set_fill(SURFACE_ALT, opacity=1)
        number = Text(str(value), font_size=34, color=TEXT, weight=BOLD)
        number.move_to(box.get_center())

        tile = VGroup(box, number)
        tile.box = box
        tile.number = number
        tile.value = value
        tile.set_z_index(2)
        return tile

    def tile_state_anims(self, tile, state):
        fill_map = {
            "unsorted": (SURFACE_ALT, BORDER),
            "active": (ACTIVE_SOFT, ACTIVE),
            "swap": (SWAP_SOFT, SWAP),
            "sorted": (SUCCESS_SOFT, SUCCESS),
        }
        fill_color, stroke_color = fill_map[state]
        return [
            tile.box.animate.set_fill(fill_color, opacity=1),
            tile.box.animate.set_stroke(stroke_color, width=2.6),
        ]

    def mark_sorted(self, tile, pulse=False):
        self.play(*self.tile_state_anims(tile, "sorted"), run_time=0.45)
        if pulse:
            self.play(Indicate(tile, color=SUCCESS, scale_factor=1.06), run_time=0.6)

    def section_chip(self, text, color):
        label = Text(text, font_size=20, color=TEXT, weight=BOLD)
        box = RoundedRectangle(
            width=label.width + 0.42,
            height=0.52,
            corner_radius=0.18,
            color=color,
            stroke_width=1.6,
        )
        box.set_fill(color, opacity=0.18)
        label.move_to(box)
        return VGroup(box, label)

    def statement(self, text):
        return Text(text, font_size=25, color=TEXT, weight=BOLD)


def render_scene():
    script_path = Path(__file__).resolve()
    command = [
        sys.executable,
        "-m",
        "manim",
        *quality_args(RENDER_QUALITY),
        str(script_path),
        "BubbleSortWorks",
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
