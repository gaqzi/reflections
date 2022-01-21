import unittest


def is_power_of_two(number: int) -> bool:
    return number > 0 and number.bit_count() == 1


class IsPowerofTwoTest(unittest.TestCase):
    def setUp(self):
        self.power_of_twos = [2 ** x for x in range(2, 25_000)]
        self.not_power_of_twos = [3 ** x for x in range(2, 25_000)]

    def test_is_power_of_two(self):
        for x, y in zip(self.power_of_twos, self.not_power_of_twos):
            self.assertIs(is_power_of_two(x), True)
            self.assertIs(is_power_of_two(y), False)


if __name__ == "__main__":
    unittest.main()
