# This file is part of PxPayPy.
#
# PxPayPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# PxPayPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with PxPayPy. If not, see
# <http://www.gnu.org/licenses/>.

import unittest
import pycodestyle


class TestCodeStyle(unittest.TestCase):
    """Check if all python files follow PEP8 style guide."""

    def test_pep8_conformance(self):
        """Test if files follow PEP8 style guide."""

        paths = ['./setup.py', './pxpaypy/', './tests/']

        styleguide = pycodestyle.StyleGuide()
        self.assertEqual(styleguide.check_files(paths).total_errors, 0)
