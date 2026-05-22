# MIT license; Copyright (c) 2024, Planet Innovation
# SPDX-License-Identifier: MIT
# 436 Elgar Road, Box Hill, 3128, VIC, Australia
# Phone: +61 3 9945 7510

# cairo is only needed for rendering, not parsing. Mock it so tests that only
# exercise parsing logic can run without the system cairo library installed.
from unittest.mock import MagicMock
import sys

sys.modules["cairo"] = MagicMock()
