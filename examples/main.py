"""
This module contains examples of Python code.
"""

import improbable_cpr


def main() -> None:
    """Main function."""
    vec1 = improbable_cpr.Vector2D(-1, 1)
    vec2 = improbable_cpr.Vector2D(2.5, -2.5)
    print(vec1 - vec2)


if __name__ == "__main__":
    main()
