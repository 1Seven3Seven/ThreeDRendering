from math import cos, sin, radians, pi
from typing import Union

from ThreeDRenderer.Vector_Math import Vector, Ray, Plane, get_vector_from_to


class Camera:
    def __init__(
            self,
            window_size: Union[list[int, int], tuple[int, int]],
            y_fov: float
    ):
        # Positional information
        self.position: list[float, float, float] = [0, 0, 0]

        # Directional information
        self.looking_vector: Vector = Vector(0, 0, 1)
        self.yaw: float = 0
        self.pitch: float = 0

        # Viewing information
        self.view_plane: Plane = Plane(self.looking_vector, [a * 10 for a in self.looking_vector.vector])

        self.y_fov: float = radians(y_fov)
        self.x_fov: float = self.y_fov * (window_size[1] / window_size[0])

        # Finding the unknown viewing information
        temp_ray = Ray(get_vector_from_to(self.position, (cos(self.x_fov), 0, 1)), self.position)
        temp_point = self.view_plane.get_intersect_with_ray(temp_ray)
        self.x_limit: float = temp_point[0]

        temp_ray = Ray(get_vector_from_to(self.position, (0, cos(self.y_fov), 1)), self.position)
        temp_point = self.view_plane.get_intersect_with_ray(temp_ray)
        self.y_limit: float = temp_point[1]

    def move_to(self, new_pos: Union[list[float, float, float], tuple[float, float, float]]):
        self.position = list(new_pos)
        self.view_plane.change_point([a + b * 10 for a, b in zip(new_pos, self.looking_vector.vector)])

    def move(self, pos_change):
        new_pos = [a + b for a, b in zip(pos_change, self.position)]
        self.move_to(new_pos)


class Camera2:
    def __init__(
            self,
            window_size: Union[list[int, int], tuple[int, int]],
            x_fov: float = pi/3,
            start_position: list[float, float, float] = None,
    ):
        # The size of the surface things will be drawn to, is used to scale things appropriately
        self.window_size = window_size

        # The current position of the camera
        self.position: list[float, float, float] = [0, 0, 0] if start_position is None else start_position.copy()

        # The direction the camera is looking in, not the most necessary as it is also stored in the view_plane
        self.looking_vector: Vector = Vector(0, 0, 1)  # Should be a unit vector

        # The plane used to project 3D images to a 2D form
        self.view_plane: Plane = Plane(
            self.looking_vector,
            [a * 10 + b for a, b in zip(self.looking_vector.vector, self.position)]
        )

        # Field of view
        self.x_fov: float = x_fov
        self.y_fov: float = x_fov * window_size[1] / window_size[0]

        # Limits of the points that can be seen on the view plane
        temp_ray = Ray(
            Vector(sin(x_fov), 0, cos(x_fov)),
            self.position
        )
        print(temp_ray)
        temp_point = self.view_plane.get_intersect_with_ray(temp_ray)
        self.x_limit = temp_point[0]

        temp_ray = Ray(
            Vector(0, sin(self.y_fov), cos(self.y_fov)),
            self.position
        )
        print(temp_ray)
        temp_point = self.view_plane.get_intersect_with_ray(temp_ray)
        self.y_limit = temp_point[1]

        print(f"X limit: {self.x_limit}")
        print(f"Y limit: {self.y_limit}")
        print(f"Ratio:   {self.x_limit / self.y_limit}")

    def move_to(self, new_pos: Union[list[float, float, float], tuple[float, float, float]]):
        self.position = list(new_pos)
        self.view_plane.change_point([a + b * 10 for a, b in zip(new_pos, self.looking_vector.vector)])

    def move(self, pos_change):
        new_pos = [a + b for a, b in zip(pos_change, self.position)]
        self.move_to(new_pos)
