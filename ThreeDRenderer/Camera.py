from math import cos, sin, pi
from typing import Union

from ThreeDRenderer.Vector_Math import Vector, Ray, Plane


class Camera:
    # Information for calculating the fov, decoupled from the main camera to make things more simple
    __fov_point = [0, 0, 0]
    __fov_plane = Plane(
        Vector(0, 0, 1),
        [0, 0, 10]
    )

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

        # Rotational information
        self.yaw = 0  # Looking left and right

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
        """
Moves the camera to the given position.
        :param new_pos: The position to move the camera to.
        """
        self.position = list(new_pos)
        self.view_plane.change_point(
            [
                new_pos[0] + self.looking_vector.x * 10,
                new_pos[1] + self.looking_vector.y * 10,
                new_pos[2] + self.looking_vector.z * 10,
            ]
        )

    def move(self, pos_change: Union[list[float, float, float], tuple[float, float, float]]):
        """
Moves the camera's position by the given values in pos_change.
        :param pos_change: The movement to be performed by the camera.
        """
        self.move_to(
            [
                pos_change[0] + self.position[0],
                pos_change[1] + self.position[1],
                pos_change[2] + self.position[2],
            ]
        )

    def change_x_fov_to(self, angle: float):
        """
Changes the x fov of the camera to the given angle.
Clamps the angle to between pi/100 and 99/100 pi.
        :param angle: Angle (in radians) to set the x fov to.
        """
        # Clamping the angle
        if angle < pi / 100:
            angle = pi / 100
        elif angle > 99 / 100 * pi:
            angle = 99 / 100 * pi
        # Set the angle
        self.x_fov = angle
        # Calculate the x limit
        temp_ray = Ray(
            Vector(sin(self.x_fov / 2), 0, cos(self.x_fov / 2)),
            self.__fov_point
        )
        temp_point = self.__fov_plane.get_intersect_with_ray(temp_ray)
        # Get the x limit
        self.x_limit = temp_point[0]
        # Calculate the y limit
        self.y_limit = self.x_limit * self.x_to_y_ratio

    def change_x_fov_by(self, angle: float):
        """
Adds the given angle to the current fov of the camera.
        :param angle: Angle (in radians) to adjust fov by.
        """
        self.change_x_fov_to(self.x_fov + angle)

    def rotate_to(self, angle: float):
        """
Rotates the camera to the given angle.
        :param angle: Angle (in radians) to rotate the camera to.
        """
        # Get the new looking vector and create the view plane from that
        # I don't think there is anymore to do with the camera
        self.looking_vector.x = sin(angle)
        self.looking_vector.y = 0
        self.looking_vector.z = cos(angle)
        # The view plane contains a reference to the looking vector so there is no need to redefine the vector inside
        # the plane
        self.view_plane.update_constant()
        # Save the angle
        self.yaw = angle

    def rotate(self, angle_change: float):
        """
Adds the given angle to the current rotation of the camera.
        :param angle_change: Angle (in radians) to rotate the camera by.
        """
        self.rotate_to(
            self.yaw + angle_change
        )
