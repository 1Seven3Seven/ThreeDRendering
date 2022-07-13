from ThreeDRenderer.Camera import Camera
from ThreeDRenderer.Cuboid import Cuboid
from ThreeDRenderer.Vector_Math import Ray, get_vector_from_to
import pygame


def cuboid(camera: Camera, surface: pygame.Surface, cuboid_: Cuboid):
    # For each corner, get the corresponding position on the camera
    points_on_view_plane = []
    for corner in cuboid_.corners:
        # Get the ray to the corner
        ray = Ray(get_vector_from_to(camera.position, corner), camera.position)
        # Position with respect to the camera
        point = [
            a - camera.view_plane.point[i] for i, a in enumerate(camera.view_plane.get_intersect_with_ray(ray))
        ]
        # Save it
        points_on_view_plane.append(point)

    # Convert the points to what will be drawn on the screen
    window_x_size, window_y_size = surface.get_size()
    x_scale = window_x_size / (2 * camera.x_limit)
    y_scale = window_y_size / (2 * camera.y_limit)
    draw_points = []
    for point in points_on_view_plane:
        draw_points.append(
            [
                point[0] * x_scale + window_x_size / 2,
                point[1] * y_scale + window_y_size / 2
            ]
        )

    # Numbering the corners, for debugging purposes
    # font = pygame.font.Font(None, 32)
    # for i, point in enumerate(draw_points):
    #     pygame.draw.circle(surface, (255, 255, 255), point, 5, 1)
    #     surface.blit(font.render(f"{i}", False, (255, 255, 255)), [a + 5 for a in point])

    # Draw the connections
    for i, j, in cuboid_.corner_connections:
        """
        # Check if both points are on the screen
        if (
            0 < draw_points[i][0] < window_x_size and 0 < draw_points[i][1] < window_y_size
        ) or (
            0 < draw_points[j][0] < window_x_size and 0 < draw_points[j][1] < window_y_size
        ):
            # If they are then draw them
            pygame.draw.line(surface, (255, 255, 255), draw_points[i], draw_points[j], 1)
        """
        pygame.draw.line(surface, (255, 255, 255), draw_points[i], draw_points[j], 1)
