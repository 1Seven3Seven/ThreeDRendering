from math import cos, sin, pi
from typing import Union

from ThreeDRenderer.Vector_Math import Vector, Ray, Plane


class Camera:
    def __init__(
            self,
            window_size: Union[list[int, int], tuple[int, int]],
            x_fov: float = pi/3,
            start_position: list[float, float, float] = None,
    ):
        # The size of the surface things will be drawn to, is used to scale things appropriately
        self.window_size = window_size

        # Some ratios to more easily do math
        self.x_to_y_ratio = window_size[1] / window_size[0]
        self.y_to_x_ratio = window_size[0] / window_size[1]

        # The current position of the camera
        self.position: list[float, float, float] = [0, 0, 0] if start_position is None else start_position.copy()

        # The direction the camera is looking in, not the most necessary as it is also stored in the view_plane
        self.looking_vector: Vector = Vector(0, 0, 1)  # Should be a unit vector

        # The plane used to project 3D images to a 2D form, sits a distance of 10 from the view point
        self.view_plane: Plane = Plane(
            self.looking_vector,
            [a * 10 + b for a, b in zip(self.looking_vector.vector, self.position)]
        )

        # Field of view
        self.x_fov: float = x_fov

        # Calculate the x limit using the x_fov, use the ratio to then find the y limit
        # then use trig to find y fov, maybe, if i am not lazy

        # Finding the x limit
        temp_ray = Ray(
            Vector(sin(x_fov / 2), 0, cos(x_fov / 2)),
            self.position
        )
        temp_point = self.view_plane.get_intersect_with_ray(temp_ray)
        self.x_limit = temp_point[0]

        # Finding the y limit
        self.y_limit = self.x_limit * self.x_to_y_ratio

        print(f"X limit: {self.x_limit}")
        print(f"Y limit: {self.y_limit}")
        print(f"Ratio:   {self.x_limit / self.y_limit}")

    def move_to(self, new_pos: Union[list[float, float, float], tuple[float, float, float]]):
        self.position = list(new_pos)
        self.view_plane.change_point([a + b * 10 for a, b in zip(new_pos, self.looking_vector.vector)])

    def move(self, pos_change):
        new_pos = [a + b for a, b in zip(pos_change, self.position)]
        self.move_to(new_pos)

    def change_x_fov_to(self, angle: float):
        """
Changes the x fov of the camera to the given angle.
Clamps the angle to between pi/100 and 99/100 pi.
        :param angle: Angle to set the x fov to.
        """
        # Clamping the angle
        if angle < pi/100:
            angle = pi/100
        elif angle > 99/100*pi:
            angle = 99/100*pi
        # Set the angle
        self.x_fov = angle
        # Calculate the x limit
        temp_ray = Ray(
            Vector(sin(self.x_fov / 2), 0, cos(self.x_fov / 2)),
            self.position
        )
        temp_point = self.view_plane.get_intersect_with_ray(temp_ray)
        # Make with respect to the center
        temp_point[0] -= self.view_plane.point[0]
        # Get the x limit
        self.x_limit = temp_point[0]
        # Calculate the y limit
        self.y_limit = self.x_limit * self.x_to_y_ratio

    def change_x_fov_by(self, angle: float):
        self.change_x_fov_to(self.x_fov + angle)
