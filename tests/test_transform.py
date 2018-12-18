import unittest
import functools

from .fixtures import make_comparable

from cnftools import transform

class PackTests(unittest.TestCase):
	def test_success(self):
		input = [[2, 3], [-2, 5]]
		expected_remapped = {
			2: 1, 3: 2, 5: 3
		}

		remapped = transform.pack(input)

		self.assertDictEqual(
			remapped,
			expected_remapped
		)

	def test_zero(self):
		input = [[0]]

		self.assertRaises(ValueError, functools.partial(transform.pack, input))

class RemapTests(unittest.TestCase):
	def test_success(self):
		input = [[2, 3], [-2, 5]]
		expected = [[1, 2], [-1, 3]]
		remapping = {
			2: 1, 3: 2, 5: 3
		}

		remapped = transform.remap(input, remapping)

		self.assertSetEqual(
			make_comparable(remapped),
			make_comparable(expected)
		)

	def test_missing(self):
		input = [[1]]
		remapping = {}

		remapped = transform.remap(input, remapping)

		self.assertRaises(KeyError, functools.partial(list, remapped))

	def test_zero(self):
		input = [[0]]
		remapping = {}

		remapped = transform.remap(input, remapping)

		self.assertRaises(ValueError, functools.partial(list, remapped))
