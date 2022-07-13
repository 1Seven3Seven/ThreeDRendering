import math
import sys

import pygame
from pygame.locals import *

import ThreeDRenderer
from ThreeDRenderer.Camera import Camera2


def upon_exit():
    """
Function to be called upon wanting the pygame screen to close.
    """

    pygame.display.quit()
    sys.exit("Pygame screen close")


def main():
    # region - Initializing pygame
    pygame.init()
    pygame.display.set_caption("Title")
    window_size = (1280, 720)
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    mouse_diff = (0, 0)
    mouse_pos = (0, 0)
    # endregion - Initializing pygame

    font = pygame.font.Font(None, 32)

    my_cuboids = [
        ThreeDRenderer.Cuboid(-5, -5, 15, 10, 10, 10),
        ThreeDRenderer.Cuboid(-5, -5, 50, 10, 10, 10),
        ThreeDRenderer.Cuboid(-25, -5, 50, 10, 10, 10),
        ThreeDRenderer.Cuboid(-5, -25, 50, 10, 10, 10),
        ThreeDRenderer.Cuboid(-5, -5, 250, 10, 10, 10),
    ]

    my_camera = ThreeDRenderer.Camera(window_size, 60)
    temp_camera = Camera2(
        window_size
    )

    use_camera = my_camera

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                upon_exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    upon_exit()

                if event.key == K_SPACE:
                    use_camera.move_to((0, 0, 0))

            if event.type == MOUSEMOTION:
                mouse_diff = (event.pos[0] - mouse_pos[0], event.pos[1] - mouse_pos[1])
                mouse_pos = event.pos

        screen.fill((0, 0, 0))

        """BELOW"""
        movement = [0, 0, 0]
        pressed = pygame.key.get_pressed()
        if pressed[K_d]:
            movement[0] += 0.5
        if pressed[K_a]:
            movement[0] -= 0.5
        if pressed[K_w]:
            movement[2] += 0.5
        if pressed[K_s]:
            movement[2] -= 0.5
        if pressed[K_q]:
            movement[1] -= 0.5
        if pressed[K_e]:
            movement[1] += 0.5

        use_camera.move(movement)

        use_camera.position = [round(a, 2) for a in use_camera.position]

        for my_cuboid in my_cuboids:
            ThreeDRenderer.renderer.cuboid(use_camera, screen, my_cuboid)

        screen.blit(font.render(f"View from: {use_camera.position}", False, (125, 125, 125)), (0, 0))
        screen.blit(font.render(f"View {use_camera.view_plane}", False, (125, 125, 125)), (0, 25))
        screen.blit(font.render(f"Plane center {use_camera.view_plane.point}", False, (125, 125, 125)), (0, 50))
        screen.blit(font.render(f"{my_cuboids[0].corners[0]}", False, (125, 125, 125)), (0, 75))

        """ABOVE"""

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
