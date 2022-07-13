from ThreeDRenderer.Vector_Math import Vector, Plane
from typing import Union


class Frustum:
    def __init__(self,
                 camera_position: Union[list[float, float, float], tuple[float, float, float]],
                 near_plane_point: Union[list[float, float, float], tuple[float, float, float]],
                 far_plane_point: Union[list[float, float, float], tuple[float, float, float]],
                 view_direction: Vector,
                 fov_x: float,
                 fov_y: float
                 ):
        self.near_plane = Plane(view_direction, near_plane_point)
        self.far_plane = Plane(view_direction.get_reverse(), far_plane_point)

        #
        #
        self.right_plane = None
        self.left_plane = None
        self.top_plane = None
        self.bottom_plane = None
