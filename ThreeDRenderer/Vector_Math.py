import math
from typing import Union


class ParallelError(Exception):
    pass


class Vector:
    __slots__ = "x", "y", "z"

    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __str__(self):
        return f"Vector: {self.x} x, {self.y} y, {self.z} y"

    def __mul__(self, constant: float) -> 'Vector':
        new_vector = Vector.from_instance(self)
        new_vector.x *= constant
        new_vector.y *= constant
        new_vector.z *= constant
        return new_vector

    def __truediv__(self, constant: float) -> 'Vector':
        new_vector = Vector.from_instance(self)
        new_vector.x /= constant
        new_vector.y /= constant
        new_vector.z /= constant
        return new_vector

    def __eq__(self, other_vector: 'Vector') -> bool:
        if isinstance(other_vector, Vector):
            return self.vector == other_vector.vector
        return False

    @property
    def vector(self) -> list[float, float, float]:
        return [self.x, self.y, self.z]

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    @classmethod
    def from_instance(cls, other_instance: 'Vector') -> 'Vector':
        return cls(
            other_instance.x,
            other_instance.y,
            other_instance.z
        )

    @classmethod
    def from_iterable(cls, iterable: Union[list[float, float, float], tuple[float, float, float]]) -> 'Vector':
        return cls(
            iterable[0],
            iterable[1],
            iterable[2]
        )

    def dot(self, other_vector: 'Vector') -> float:
        return self.x * other_vector.x + self.y * other_vector.y + self.z * other_vector.z

    def dot_product(self, other_vector: 'Vector') -> float:
        dot_number = self.dot(other_vector)

        if dot_number == 0:
            return 90

        return math.acos(dot_number / (self.magnitude * other_vector.magnitude))

    def cross(self, other_vector: 'Vector') -> 'Vector':
        return Vector(
            (self.y * other_vector.z - self.z * other_vector.y),
            -(self.x * other_vector.z - self.z * other_vector.x),
            (self.x * other_vector.y - self.y * other_vector.x)
        )

    def reverse(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def get_reverse(self) -> 'Vector':
        return Vector(
            -self.x,
            -self.y,
            -self.z
        )

    def change_to_yaw_pitch(self, yaw: float, pitch: float, magnitude: float = 1):
        """
        Currently incorrectly implemented
        """
        self.x = math.sin(yaw) * math.cos(pitch) * magnitude
        self.y = math.sin(pitch) * magnitude
        self.z = math.cos(yaw) * math.cos(pitch) * magnitude


class Ray:
    __slots__ = "vector", "start"

    def __init__(self, vector: Vector, start: [float, float, float]):
        self.vector: Vector = vector
        self.start: list[float, float, float] = start

    def __str__(self):
        return f"Ray: (x, y, z) = {self.start} + t{self.vector.vector}"


class Plane:
    __slots__ = "normal", "point", "constant"

    def __init__(self, normal: 'Vector', point: Union[list[float, float, float], tuple[float, float, float]]):
        self.normal: Vector = normal
        self.point = point
        self.constant: float = -sum([a * b for a, b in zip(normal.vector, point)])

    def __str__(self):
        return f"Plane: {self.normal.x}x + {self.normal.y}y + {self.normal.z}z = {-self.constant}"

    def update_constant(self):
        self.constant = -sum([a * b for a, b in zip(self.normal.vector, self.point)])

    def change_normal(self, new_normal: Vector):
        self.normal = new_normal
        self.update_constant()

    def change_point(self, new_point: Union[list[float, float, float], tuple[float, float, float]]):
        self.point = new_point
        self.update_constant()

    def change_normal_and_point(self,
                                new_normal: Vector,
                                new_point: Union[list[float, float, float], tuple[float, float, float]]):
        self.normal = new_normal
        self.point = new_point
        self.update_constant()

    def get_intersect_with_ray(self, ray: Ray) -> list[float, float, float]:
        if self.normal.dot(ray.vector) == 0:
            raise ParallelError(f"{self} and {ray} are parallel")

        numerator = self.constant + sum([a * b for a, b in zip(self.normal.vector, ray.start)])
        denominator = sum([a * b for a, b in zip(self.normal.vector, ray.vector.vector)])
        t = - numerator / denominator

        return [a + b * t for a, b in zip(ray.start, ray.vector.vector)]

    def get_shortest_distance_to_point(self, point: Union[list[float, float, float], tuple[float, float, float]]):
        numerator = abs(self.normal.x * point[0] + self.normal.y * point[1] + self.normal.z * point[2] + self.constant)
        denominator = math.sqrt(
            self.normal.x * self.normal.x + self.normal.y * self.normal.y + self.normal.z * self.normal.z
        )
        return numerator / denominator


def get_vector_from_to(point1: Union[list[float, float, float], tuple[float, float, float]],
                       point2: Union[list[float, float, float], tuple[float, float, float]]):
    return Vector(
        point2[0] - point1[0],
        point2[1] - point1[1],
        point2[2] - point1[2],
    )


def get_vector_from_yaw_pitch(yaw: float, pitch: float) -> Vector:
    """
    :param yaw: Yaw angle in radians
    :param pitch: Pitch angle in radians
    """
    return Vector(
        math.sin(yaw) * math.cos(pitch),
        math.sin(pitch),
        math.cos(yaw) * math.cos(pitch)
    )


def main():
    tests = {
        "Dot": True,
        "Dot Product": True,
        "Cross Product": True,
        "Ray Intersection With Plane": True,
        "Shortest Distance From Plane To Point": True,
    }

    detailed_printing = 0

    passed_all = True

    print("Detailed Prints (y/n) anything but 'y' is considered n")
    answer = input(": ")
    if answer == "y":
        detailed_printing = 1

    def disp(*args, **kwargs):
        if detailed_printing:
            print(*args, **kwargs)

    if tests["Dot"]:
        print("\n", " Dot Tests" .center(50, '-'))

        print("Test 1")
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(0, 1, 0)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = 0
        disp(f"Expected result = {expected_result}")
        result = vector1.dot(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 2")
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(1, 1, 0)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = 1
        disp(f"Expected result = {expected_result}")
        result = vector1.dot(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 3")
        vector1 = Vector(10, 5, 2)
        vector2 = Vector(7, 6, 9)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = 118
        disp(f"Expected result = {expected_result}")
        result = vector1.dot(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

    if tests["Dot Product"]:
        print("\n", " Dot Product Tests ".center(50, '-'))

        print("Test 1")
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(0, 1, 0)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = 90
        disp(f"Expected result = {expected_result}")
        result = vector1.dot_product(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 2")
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(1, 1, 0)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = round(math.pi / 4, 10)
        disp(f"Expected result = {expected_result}")
        result = round(vector1.dot_product(vector2), 10)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 3")
        vector1 = Vector(10, 5, 2)
        vector2 = Vector(7, 6, 9)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = 0.6328119474
        disp(f"Expected result = {expected_result} (10 dp)")
        result = round(vector1.dot_product(vector2), 10)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

    if tests["Cross Product"]:
        print("\n", " Cross Product Tests ".center(50, '-'))

        print("Test 1")
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(0, 1, 0)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = Vector(0, 0, 1)
        disp(f"Expected result = {expected_result}")
        result = vector1.cross(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 2")
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(1, 1, 0)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = Vector(0, 0, 1)
        disp(f"Expected result = {expected_result}")
        result = vector1.cross(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 3")
        vector1 = Vector(10, 5, 2)
        vector2 = Vector(7, 6, 9)
        disp(f"Vector 1 = {vector1}")
        disp(f"Vector 2 = {vector2}")
        expected_result = Vector(33, -76, 25)
        disp(f"Expected result = {expected_result}")
        result = vector1.cross(vector2)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

    if tests["Ray Intersection With Plane"]:
        print("\n", " Ray Intersection With Plane ".center(50, '-'))

        print("Test 1")
        plane = Plane(Vector(0, 0, 1), [0, 0, 0])
        ray = Ray(Vector(0, 0, 15), [17, 22, -16])
        disp(f"Plane = {plane}")
        disp(f"Ray = {ray}")
        expected_result = [17.0, 22.0, 0.0]
        disp(f"Expected result = {expected_result}")
        result = plane.get_intersect_with_ray(ray)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 2")
        plane = Plane(Vector(2, 1, -4), [0, 0, -1])
        ray = Ray(Vector(1, 3, 1), [0, 2, 0])
        disp(f"Plane = {plane}")
        disp(f"Ray = {ray}")
        expected_result = [2.0, 8.0, 2.0]
        disp(f"Expected result = {expected_result}")
        result = plane.get_intersect_with_ray(ray)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 3")
        plane = Plane(Vector(4, 5, -2), [4, 0, -1])
        ray = Ray(Vector(3, -4, 1), [2, 0, 5])
        disp(f"Plane = {plane}")
        disp(f"Ray = {ray}")
        expected_result = [-4.0, 8.0, 3.0]
        disp(f"Expected result = {expected_result}")
        result = plane.get_intersect_with_ray(ray)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

    if tests["Shortest Distance From Plane To Point"]:
        print("\n", " Shortest Distance From Plane To Point ".center(50, '-'))

        print("Test 1")
        plane = Plane(Vector(0, 0, 1), [0, 0, 0])
        point = (0, 0, 10)
        disp(f"Plane = {plane}")
        disp(f"Point = {point}")
        expected_result = 10
        disp(f"Expected result = {expected_result}")
        result = plane.get_shortest_distance_to_point(point)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 2")
        plane = Plane(Vector(2, 1, -4), [0, 0, -1])
        point = (17, 22, 19)
        disp(f"Plane = {plane}")
        disp(f"Ray = {point}")
        expected_result = 5.237229366
        disp(f"Expected result = {expected_result} (9 dp)")
        result = round(plane.get_shortest_distance_to_point(point), 9)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

        print("Test 2")
        plane = Plane(Vector(4, 5, -2), [4, 0, -1])
        point = (-52, 2, 17)
        disp(f"Plane = {plane}")
        disp(f"Ray = {point}")
        expected_result = 37.26779962
        disp(f"Expected result = {expected_result} (8 dp)")
        result = round(plane.get_shortest_distance_to_point(point), 8)
        disp(f"Result          = {result}")
        pass_fail = "Passed" if result == expected_result else "Failed"
        print(f"\t{pass_fail}")
        if pass_fail == "Failed":
            passed_all = False
            if detailed_printing:
                input("Press enter to continue")

    print("\n")
    print("=" * 50)
    if passed_all:
        print(" All Passed ".center(50, ' '))
    else:
        print(" Some Failed ".center(50, '='))
    print("=" * 50)


if __name__ == '__main__':
    main()
