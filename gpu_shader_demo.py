from manimlib import *
import numpy as np

class GPUShaderDemo(Scene):
    def construct(self):
        # Title
        title = Tex(r"\textbf{CPU vs GPU Performance Comparison}", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Subtitle explaining shader usage
        subtitle = Text("Using GPU Shaders for Complex Graphics", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        # Create two comparison boxes
        cpu_label = Text("CPU Rendering", font_size=32, color=RED, weight=BOLD)
        cpu_label.move_to(LEFT * 3.5 + UP * 2)

        gpu_label = Text("GPU Rendering", font_size=32, color=GREEN, weight=BOLD)
        gpu_label.move_to(RIGHT * 3.5 + UP * 2)

        self.play(
            Write(cpu_label),
            Write(gpu_label)
        )
        self.wait(0.3)

        # Create boxes for visual comparison
        cpu_box = Rectangle(height=4, width=3, color=RED, stroke_width=3)
        cpu_box.move_to(LEFT * 3.5 + DOWN * 0.5)

        gpu_box = Rectangle(height=4, width=3, color=GREEN, stroke_width=3)
        gpu_box.move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(Create(cpu_box), Create(gpu_box))
        self.wait(0.3)

        # Performance metrics
        cpu_info = VGroup(
            Text("Single Core", font_size=20),
            Text("Sequential", font_size=20),
            Text("~100 ops/frame", font_size=20, color=ORANGE)
        ).arrange(DOWN, buff=0.2)
        cpu_info.move_to(cpu_box.get_center())

        gpu_info = VGroup(
            Text("Thousands of Cores", font_size=20),
            Text("Parallel Processing", font_size=20),
            Text("~10,000+ ops/frame", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        gpu_info.move_to(gpu_box.get_center())

        self.play(
            FadeIn(cpu_info),
            FadeIn(gpu_info)
        )
        self.wait(1)

        # Clear for particle demo
        self.play(
            FadeOut(cpu_info),
            FadeOut(gpu_info)
        )

        # Create particle system - CPU side (fewer particles)
        cpu_particles = VGroup()
        num_cpu_particles = 20
        for i in range(num_cpu_particles):
            dot = Dot(radius=0.05, color=interpolate_color(RED, ORANGE, i/num_cpu_particles))
            angle = i * TAU / num_cpu_particles
            dot.move_to(cpu_box.get_center() + np.array([
                0.5 * np.cos(angle),
                0.5 * np.sin(angle),
                0
            ]))
            cpu_particles.add(dot)

        # Create particle system - GPU side (many more particles)
        gpu_particles = VGroup()
        num_gpu_particles = 100
        for i in range(num_gpu_particles):
            dot = Dot(radius=0.03, color=interpolate_color(GREEN, BLUE, i/num_gpu_particles))
            angle = i * TAU / num_gpu_particles
            dot.move_to(gpu_box.get_center() + np.array([
                0.5 * np.cos(angle),
                0.5 * np.sin(angle),
                0
            ]))
            gpu_particles.add(dot)

        self.play(
            FadeIn(cpu_particles),
            FadeIn(gpu_particles)
        )
        self.wait(0.5)

        # Animate particles in spiral pattern
        # CPU - slower, fewer particles
        cpu_animations = []
        for i, particle in enumerate(cpu_particles):
            angle_offset = i * TAU / num_cpu_particles
            path = ParametricFunction(
                lambda t: cpu_box.get_center() + np.array([
                    (0.5 + 0.8 * t) * np.cos(angle_offset + 2 * TAU * t),
                    (0.5 + 0.8 * t) * np.sin(angle_offset + 2 * TAU * t),
                    0
                ]),
                t_range=[0, 1]
            )
            cpu_animations.append(MoveAlongPath(particle, path))

        # GPU - faster, more particles
        gpu_animations = []
        for i, particle in enumerate(gpu_particles):
            angle_offset = i * TAU / num_gpu_particles
            path = ParametricFunction(
                lambda t: gpu_box.get_center() + np.array([
                    (0.5 + 0.8 * t) * np.cos(angle_offset + 2 * TAU * t),
                    (0.5 + 0.8 * t) * np.sin(angle_offset + 2 * TAU * t),
                    0
                ]),
                t_range=[0, 1]
            )
            gpu_animations.append(MoveAlongPath(particle, path))

        # Run animations - GPU finishes faster
        self.play(
            AnimationGroup(*gpu_animations, lag_ratio=0),
            run_time=2
        )

        # GPU done marker
        gpu_done = MathTex(r"\checkmark", font_size=60, color=GREEN)
        gpu_done.move_to(gpu_box.get_center())
        self.play(FadeIn(gpu_done, scale=2))

        # CPU still running
        self.play(
            AnimationGroup(*cpu_animations, lag_ratio=0),
            run_time=4
        )

        cpu_done = MathTex(r"\checkmark", font_size=60, color=RED)
        cpu_done.move_to(cpu_box.get_center())
        self.play(FadeIn(cpu_done, scale=2))

        self.wait(0.5)

        # Show timing comparison
        timing_text = VGroup(
            Text("GPU: 2 seconds", font_size=28, color=GREEN, weight=BOLD),
            Text("CPU: 6 seconds", font_size=28, color=RED, weight=BOLD),
            Tex(r"\textbf{Speedup: 3x}", font_size=32, color=YELLOW)
        ).arrange(DOWN, buff=0.3)
        timing_text.move_to(DOWN * 3)

        self.play(Write(timing_text))
        self.wait(1)

        # Clear for shader demo
        self.play(
            FadeOut(cpu_particles),
            FadeOut(gpu_particles),
            FadeOut(cpu_done),
            FadeOut(gpu_done),
            FadeOut(cpu_box),
            FadeOut(gpu_box),
            FadeOut(cpu_label),
            FadeOut(gpu_label),
            FadeOut(timing_text)
        )

        # Shader-based effects demonstration
        shader_title = Tex(r"\textbf{GPU Shader Effects}", font_size=40, color=BLUE)
        shader_title.move_to(ORIGIN)
        self.play(Transform(subtitle, shader_title))
        self.wait(0.5)

        # Create complex gradient mesh using shaders
        resolution = 30
        grid = VGroup()

        for i in range(resolution):
            for j in range(resolution):
                x = -3 + 6 * i / (resolution - 1)
                y = -2 + 4 * j / (resolution - 1)

                # Calculate color based on position (simulating shader)
                r = (np.sin(i * 0.5) + 1) / 2
                g = (np.cos(j * 0.5) + 1) / 2
                b = (np.sin(i * 0.3 + j * 0.3) + 1) / 2
                color = rgb_to_color([r, g, b])

                dot = Dot(point=[x, y, 0], radius=0.08, color=color)
                grid.add(dot)

        self.play(FadeIn(grid, lag_ratio=0.01), run_time=2)

        # Animate the shader effect
        def update_shader(mob, alpha):
            for k, dot in enumerate(mob):
                i = k // resolution
                j = k % resolution

                # Time-varying shader effect
                r = (np.sin(i * 0.5 + alpha * TAU) + 1) / 2
                g = (np.cos(j * 0.5 + alpha * TAU) + 1) / 2
                b = (np.sin(i * 0.3 + j * 0.3 + alpha * TAU) + 1) / 2
                color = rgb_to_color([r, g, b])
                dot.set_color(color)

        self.play(
            UpdateFromAlphaFunc(grid, update_shader),
            run_time=4,
            rate_func=linear
        )

        self.wait(0.5)

        # Final message
        final_message = VGroup(
            Tex(r"\textbf{GPU Benefits:}", font_size=36, color=YELLOW),
            Text("• Parallel Processing", font_size=24),
            Text("• Real-time Shader Effects", font_size=24),
            Text("• Complex Particle Systems", font_size=24),
            Text("• Faster Rendering", font_size=24),
            Tex(r"\textbf{Use: }", font_size=28, color=GREEN).next_to(ORIGIN, RIGHT * 0),
            Text("--renderer=opengl", font_size=24, font="Monospace", color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Adjust positioning for the last item
        final_message[-1].next_to(final_message[-2], RIGHT, buff=0.2)

        final_message.move_to(ORIGIN)

        self.play(
            FadeOut(grid),
            FadeOut(subtitle)
        )
        self.play(FadeIn(final_message, shift=UP))

        self.wait(2)

        # Ending
        self.play(
            final_message.animate.scale(1.2).set_color(BLUE),
            run_time=0.5
        )
        self.wait(2)
