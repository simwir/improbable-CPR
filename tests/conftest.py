"""
Conftest module.
"""

import random

import pytest


@pytest.fixture
def seed_random(request):
    seed = request.node.name
    print(f"seed: {seed}")
    random.seed(seed)
