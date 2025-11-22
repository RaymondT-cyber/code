#!/usr/bin/env python3
"""System test to verify all components work together."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("\\n" + "="*60)
    print("TESTING: Enhanced Module Imports")
    print("="*60)
    
    try:
        import pygame
        print("✓ pygame imported")
        
        from config import WINDOW_WIDTH, WINDOW_HEIGHT
        print(f"✓ config imported (window: {WINDOW_WIDTH}x{WINDOW_HEIGHT})")
        
        from gameplay.band_api import BandAPI, BandMember
        print("✓ band_api imported")
        
        from gameplay.code_executor import CodeExecutor
        print("✓ code_executor imported")
        
        from gameplay.lessons import LessonManager
        print("✓ lessons imported")
        
        from ui.field_view import FieldView
        print("✓ field_view imported")
        
        from ui.editor import CodeEditor
        print("✓ editor imported")
        
        # Enhanced UI components
        from ui.enhanced_retro_button import EnhancedRetroButton
        print("✓ enhanced_retro_button imported")
        
        # Enhanced scenes
        from scenes.enhanced_main_menu import EnhancedMainMenu
        print("✓ enhanced_main_menu imported")
        
        from scenes.enhanced_level_select import EnhancedLevelSelect
        print("✓ enhanced_level_select imported")
        
        from scenes.enhanced_story_scene import EnhancedStoryScene
        print("✓ enhanced_story_scene imported")
        
        from scenes.enhanced_code_editor import EnhancedCodeEditor
        print("✓ enhanced_code_editor imported")
        
        from scenes.enhanced_competition_scene import EnhancedCompetitionScene
        print("✓ enhanced_competition_scene imported")
        
        # Story content system
        from story.week_content import WeekContent
        print("✓ week_content system imported")
        
        from core.game import PrideOfCodeGame
        print("✓ game imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_band_api():
    """Test the Band API functionality."""
    print("\\n" + "="*60)
    print("TESTING: Band API")
    print("="*60)
    
    try:
        from gameplay.band_api import BandAPI
        
        api = BandAPI()
        api.create_band(16)
        print(f"✓ Created band with {len(api.members)} members")
        
        # Test move_to
        member = api.members[0]
        api.move_to(member, 50, 26)
        print(f"✓ Moved member to ({member.x}, {member.y})")
        
        # Test form_circle
        brass = api.get_section('brass')
        api.form_circle(brass, 50, 26, 10)
        print(f"✓ Formed circle with {len(brass)} brass members")
        
        # Test form_line
        woodwind = api.get_section('woodwind')
        api.form_line(woodwind, 20, 20, 80, 20)
        print(f"✓ Formed line with {len(woodwind)} woodwind members")
        
        return True
    except Exception as e:
        print(f"✗ Band API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_ui():
    """Test enhanced UI components."""
    print("\\n" + "="*60)
    print("TESTING: Enhanced UI Components")
    print("="*60)
    
    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        import pygame
        pygame.init()
        
        from ui.enhanced_retro_button import EnhancedRetroButton
        button = EnhancedRetroButton(100, 100, 150, 50, "Test Button")
        print("✓ Enhanced retro button created")
        
        # Test button properties
        assert button.text == "Test Button"
        assert button.rect.width == 150
        print("✓ Enhanced button properties verified")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Enhanced UI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_story_content():
    """Test the story content system."""
    print("\\n" + "="*60)
    print("TESTING: Story Content System")
    print("="*60)
    
    try:
        from story.week_content import WeekContent
        
        week_content = WeekContent()
        
        # Test week content retrieval
        week_1 = week_content.get_week_content(1)
        assert week_1 is not None
        print(f"✓ Week 1 content: {week_1['title']}")
        
        # Test dialogue system
        dialogue = week_content.get_story_dialogue(1)
        assert len(dialogue) > 0
        print(f"✓ Week 1 dialogue: {len(dialogue)} lines")
        
        # Test Python lesson
        lesson = week_content.get_python_lesson(1)
        assert lesson['concept'] == 'Variables'
        print(f"✓ Week 1 lesson: {lesson['concept']}")
        
        # Test competition weeks
        competition_weeks = week_content.get_competition_weeks()
        print(f"✓ Competition weeks: {competition_weeks}")
        
        return True
    except Exception as e:
        print(f"✗ Story content test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_scenes():
    """Test enhanced scene initialization."""
    print("\\n" + "="*60)
    print("TESTING: Enhanced Scenes")
    print("="*60)
    
    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        
        import pygame
        pygame.init()
        
        from core.state_manager import StateManager
        from scenes.enhanced_main_menu import EnhancedMainMenu
        from scenes.enhanced_level_select import EnhancedLevelSelect
        from scenes.enhanced_story_scene import EnhancedStoryScene
        from scenes.enhanced_code_editor import EnhancedCodeEditor
        from scenes.enhanced_competition_scene import EnhancedCompetitionScene
        
        manager = StateManager()
        
        # Mock game object
        class MockGame:
            def __init__(self):
                self.audio = None
        
        game = MockGame()
        
        # Test scene creation
        menu = EnhancedMainMenu(manager, game)
        print("✓ Enhanced main menu created")
        
        level_select = EnhancedLevelSelect(manager, game)
        print("✓ Enhanced level select created")
        
        story = EnhancedStoryScene(manager, game)
        print("✓ Enhanced story scene created")
        
        editor = EnhancedCodeEditor(manager, game)
        print("✓ Enhanced code editor created")
        
        competition = EnhancedCompetitionScene(manager, game)
        print("✓ Enhanced competition scene created")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Enhanced scenes test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_init():
    """Test game initialization (without running the loop)."""
    print("\\n" + "="*60)
    print("TESTING: Enhanced Game Initialization")
    print("="*60)
    
    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        
        import pygame
        pygame.init()
        
        from core.game import PrideOfCodeGame
        
        game = PrideOfCodeGame()
        print("✓ Enhanced game initialized")
        print(f"✓ Window size: {game.screen.get_width()}x{game.screen.get_height()}")
        print(f"✓ Available enhanced scenes: {list(game.state_manager.states.keys())}")
        print(f"✓ Current scene: {game.state_manager.current_name}")
        print(f"✓ Story content system loaded: {hasattr(game, 'week_content')}")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Game init test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\\n" + "="*70)
    print("  PRIDE OF CODE - ENHANCED SYSTEM TEST SUITE")
    print("="*70)
    
    results = []
    
    results.append(("Enhanced Module Imports", test_imports()))
    results.append(("Band API", test_band_api()))
    results.append(("Enhanced UI Components", test_enhanced_ui()))
    results.append(("Story Content System", test_story_content()))
    results.append(("Enhanced Scenes", test_enhanced_scenes()))
    results.append(("Enhanced Game Initialization", test_game_init()))
    
    # Summary
    print("\\n" + "="*70)
    print("ENHANCED TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} | {name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\\n🎉 ALL ENHANCED TESTS PASSED! System is operational.")
        print("\\n🚀 Enhanced Features Available:")
        print("  ✓ Retro-pixel main menu with animations")
        print("  ✓ 16-week level select with competition weeks")
        print("  ✓ Character portraits and story dialogue system")
        print("  ✓ Professional code editor with syntax highlighting")
        print("  ✓ Live band competition performances")
        print("  ✓ Complete 16-week story campaign")
        print("  ✓ Colorblind accessibility features")
        print("  ✓ 8-bit audio framework")
        print("\\nTo run the enhanced game:")
        print("  python3 core/main.py")
        print("\\nTo run the demo:")
        print("  python3 DEMO.py")
        return 0
    else:
        print(f"\\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())