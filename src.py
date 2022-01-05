# import time
# from functools import lru_cache


# @lru_cache
# def slow_add(*args, delay=1):
#     time.sleep(delay)
#     return sum(args)


# s1 = time.perf_counter()

# for i in range(5):
#     print(f"Result of run {i} is: {slow_add(1,2,3)}")

# s2 = time.perf_counter()
# print(f"Total runtime: {s2-s1} seconds.")


# import timeit

# # Implicitly interned dict creation and access.
# implicitly_interned = """
# d = {"#"*4096 : "Interned"}
# d["#"*4096]
# """

# # Explicitly interned dict creation and access.
# explicitly_interned = """
# k = sys.intern("#"*4097)
# d = { k : "Explicitly-interned"}
# d[k]
# """

# # print(f"Interned dict creation & access: {timeit.timeit(interned)} seconds")
# # print(f"Non-interned dict creation & access: {timeit.timeit(non_interned)} seconds")

# print(timeit.timeit(explicitly_interned)/timeit.timeit(implicitly_interned))

# src.py
import textwrap
import unittest


def crop(text: str, limit: int) -> str:
    cropped_text = textwrap.shorten(
        text,
        width=limit,
        initial_indent="",
        subsequent_indent="",
        break_long_words=False,
        break_on_hyphens=False,
        placeholder="",
    )
    return cropped_text


class TestCrop(unittest.TestCase):
    def setUp(self):
        self.text = "This is an example of speech synthesis in English."
        self.text_complex = """
        wrap(), fill() and shorten() work by creating a TextWrapper instance
        and calling a single method on it.
        """

    def test_ok(self):
        cropped_text = crop(self.text, limit=10)
        self.assertEqual(cropped_text, "This is an")

    def test_ok_complex(self):
        cropped_text = crop(self.text_complex, limit=15)
        self.assertEqual(cropped_text, "wrap(), fill()")

    def test_no_word_break(self):
        cropped_text = crop(self.text, limit=9)
        self.assertNotEqual(cropped_text, "This is a")

    def test_no_trailing_space(self):
        cropped_text = crop(self.text, limit=8)
        self.assertNotEqual(cropped_text, "This is ")


if __name__ == "__main__":
    unittest.main()
