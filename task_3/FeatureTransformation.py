import numpy as np
import unittest


def convert_time_to_cyclic(hour):
    angle = hour * (2 * np.pi / 24)
    return np.sin(angle), np.cos(angle)


class CyclicTimeFeaturesTest(unittest.TestCase):

    def test_midnight(self):
        sine, cosine = convert_time_to_cyclic(0)
        self.assertAlmostEqual(sine, 0.0, places=5)
        self.assertAlmostEqual(cosine, 1.0, places=5)

    def test_noon(self):
        sine, cosine = convert_time_to_cyclic(12)
        self.assertAlmostEqual(sine, 0.0, places=5)
        self.assertAlmostEqual(cosine, -1.0, places=5)

    def test_evening(self):
        sine, cosine = convert_time_to_cyclic(18)
        self.assertAlmostEqual(sine, -1.0, places=5)
        self.assertAlmostEqual(cosine, 0.0, places=5)

    def test_morning(self):
        sine, cosine = convert_time_to_cyclic(6)
        self.assertAlmostEqual(sine, 1.0, places=5)
        self.assertAlmostEqual(cosine, 0.0, places=5)

    def test_crossing_day_boundary(self):
        sine1, cosine1 = convert_time_to_cyclic(23)
        sine2, cosine2 = convert_time_to_cyclic(1)
        dot_product = np.dot([sine1, cosine1], [sine2, cosine2])
        hour_difference = np.arccos(dot_product) * 24 / (2 * np.pi)
        self.assertAlmostEqual(hour_difference, 2.0, places=1)


if __name__ == "__main__":
    unittest.main()
