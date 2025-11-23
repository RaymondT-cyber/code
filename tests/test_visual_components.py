"""
Test file to verify visual components are working correctly.
"""

import sys
import os
import pygame

# Add the code directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def _check_color_imports():
    """Test that color imports work correctly."""
    try:
        from core.colors import (
            DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
            SILVER_STEEL, NEON_COMPETENCE_CYAN, GOLD_EXCELLENCE,
            PRECISION_MAGENTA, STADIUM_TURF_GREEN
        )
        print("✓ Color imports successful")
        return True
    except Exception as e:
        print(f"✗ Color imports failed: {e}")
        return False


def test_color_imports():
    assert _check_color_imports()


def _check_component_imports():
    """Test that component imports work correctly."""
    try:
        from ui.components import RetroButton, RetroPanel, ScoreBar, TextRenderer
        print("✓ Component imports successful")
        return True
    except Exception as e:
        print(f"✗ Component imports failed: {e}")
        return False


def test_component_imports():
    assert _check_component_imports()


def _check_animation_imports():
    """Test that animation imports work correctly."""
    try:
        from core.animations import AnimationManager, SparkleEffect
        print("✓ Animation imports successful")
        return True
    except Exception as e:
        print(f"✗ Animation imports failed: {e}")
        return False


def test_animation_imports():
    assert _check_animation_imports()


def _check_scene_imports():
    """Test that scene imports work correctly."""
    try:
        from scenes.main_menu import MainMenuScene
        from scenes.code_editor import CodeEditorScene
        from scenes.level_select import LevelSelectScene
        print("✓ Scene imports successful")
        return True
    except Exception as e:
        print(f"✗ Scene imports failed: {e}")
        return False


def test_scene_imports():
    assert _check_scene_imports()


def _check_color_values():
    """Test that color values match the style guide."""
    try:
        from core.colors import (
            DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
            SILVER_STEEL, NEON_COMPETENCE_CYAN, GOLD_EXCELLENCE
        )

        # Test specific color values
        assert DARK_GRAPHITE_BLACK.r == 26 and DARK_GRAPHITE_BLACK.g == 28 and DARK_GRAPHITE_BLACK.b == 30
        assert RETRO_PIXEL_AMBER.r == 242 and RETRO_PIXEL_AMBER.g == 169 and RETRO_PIXEL_AMBER.b == 0
        assert DEEP_SIGNAL_BLUE.r == 33 and DEEP_SIGNAL_BLUE.g == 70 and DEEP_SIGNAL_BLUE.b == 199
        assert SILVER_STEEL.r == 197 and SILVER_STEEL.g == 202 and SILVER_STEEL.b == 211
        assert NEON_COMPETENCE_CYAN.r == 67 and NEON_COMPETENCE_CYAN.g == 224 and NEON_COMPETENCE_CYAN.b == 236
        assert GOLD_EXCELLENCE.r == 255 and GOLD_EXCELLENCE.g == 201 and GOLD_EXCELLENCE.b == 71

        print("✓ Color values match style guide")
        return True
    except Exception as e:
        print(f"✗ Color values test failed: {e}")
        return False


def test_color_values():
    assert _check_color_values()


def _check_component_creation():
    """Test that components can be created successfully."""
    try:
        pygame.init()

        from ui.components import RetroButton, RetroPanel, ScoreBar

        # Test button creation
        button = RetroButton(0, 0, 100, 50, "Test")

        # Test panel creation
        panel = RetroPanel(0, 0, 100, 100)

        # Test score bar creation
        from core.colors import STADIUM_TURF_GREEN
        bar = ScoreBar(0, 0, 100, 20, STADIUM_TURF_GREEN, "Test")

        print("✓ Component creation successful")
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Component creation failed: {e}")
        try:
            pygame.quit()
        except Exception:
            pass
        return False


def test_component_creation():
    assert _check_component_creation()


def run_all_tests():
    """Run all tests and report results."""
    print("Running Pride of Code Visual Components Tests")
    print("=" * 50)

    tests = [
        _check_color_imports,
        _check_component_imports,
        _check_animation_imports,
        _check_scene_imports,
        _check_color_values,
        _check_component_creation
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("All tests passed! Visual components are ready to use.")
        return True
    else:
        print("Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
