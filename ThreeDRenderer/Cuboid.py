from ThreeDRenderer.Vector_Math import Vector, Plane
from math import sqrt


class Cuboid:

    # The normals of each surface
    normals: tuple[tuple[int, int, int]] = (
        (0, 0, -1),     # Front
        (-1, 0, 0),     # Left
        (1, 0, 0),      # Right
        (0, 1, 0),      # Top
        (0, -1, 0),     # Bottom
        (0, 0, 1),      # Back
    )

    # The indexes of each corner that connect to one another
    corner_connections: tuple[tuple[int, int]] = (
        (0, 1),  # 0
        (0, 2),  # 1
        (0, 4),  # 2
        (1, 3),  # 3
        (1, 5),  # 4
        (2, 3),  # 5
        (2, 6),  # 6
        (3, 7),  # 7
        (4, 5),  # 8
        (4, 6),  # 9
        (5, 7),  # 10
        (6, 7),  # 11
    )

    # The indexes of the corners for each surface, these are in order from one to another
    surface_corners: tuple[tuple[int, int, int, int]] = (
        (0, 1, 3, 2),  # Front
        (0, 2, 6, 4),  # Left
        (1, 3, 7, 5),  # Right
        (2, 3, 7, 6),  # Top
        (0, 1, 5, 4),  # Bottom
        (4, 5, 7, 6),  # Back
    )

    # The indexes of corner connections for each surface
    surface_corner_connections: tuple[tuple[int, int, int, int]] = (
        (0, 1, 3, 5),    # Front
        (1, 2, 6, 9),    # Left
        (3, 4, 7, 10),   # Right
        (5, 6, 7, 11),   # Top
        (0, 2, 4, 8),    # Bottom
        (8, 9, 10, 11),  # Back
    )

    __slots__ = "x", "y", "z", "width", "height", "length", "center", "radius", "corners", "faces"

    def __init__(self, x: float, y: float, z: float, width: float, height: float, length: float):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.length = length

        # The corners of the cuboid
        self.corners: list[list[float, float, float]] = [
            [x,         y + height, z],           # 0
            [x + width, y + height, z],           # 1
            [x,         y,          z],           # 2
            [x + width, y,          z],           # 3
            [x,         y + height, z + length],  # 4
            [x + width, y + height, z + length],  # 5
            [x,         y,          z + length],  # 6
            [x + width, y,          z + length],  # 7
        ]

        # The faces of the cuboid
        self.faces = [
            Plane(Vector.from_iterable(self.normals[0]), self.corners[0]),  # Front
            Plane(Vector.from_iterable(self.normals[1]), self.corners[0]),  # Left
            Plane(Vector.from_iterable(self.normals[2]), self.corners[7]),  # Right
            Plane(Vector.from_iterable(self.normals[3]), self.corners[7]),  # Top
            Plane(Vector.from_iterable(self.normals[4]), self.corners[0]),  # Bottom
            Plane(Vector.from_iterable(self.normals[5]), self.corners[7]),  # Back
        ]

        # Making the point in each face be the center of the face
        for i in range(6):
            self.faces[i].change_point(
                [(a + b + c + d) / 4 for a, b, c, d in zip(*[self.corners[a] for a in self.surface_corners[i]])]
            )

        # For frustum culling, consider it a sphere
        self.center = (
            x + width / 2,
            y + height / 2,
            z + length / 2
        )
        self.radius = sqrt(sum([(a - b) * (a - b) for a, b in zip(self.center, self.corners[0])]))

    def __str__(self):
        return f"Cuboid: corner1 = {self.corners[0]}, corner2 = {self.corners[7]}"

    def collides_with(self, other_cuboid: 'Cuboid'):
        if self.x < other_cuboid.x + other_cuboid.width and self.x + self.width > other_cuboid.x:
            if self.y < other_cuboid.y + other_cuboid.height and self.y + self.height > other_cuboid.y:
                if self.z < other_cuboid.z + other_cuboid.length and self.z + self.length > other_cuboid.z:
                    return True
        return False
