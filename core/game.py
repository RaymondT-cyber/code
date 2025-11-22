import pygame
import time

from config import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE, EDITOR_X, EDITOR_Y, EDITOR_WIDTH, EDITOR_HEIGHT

from core.state_manager import StateManager
from core.audio_manager import AudioManager
from core.save_system import SaveSystem

from gameplay.level_manager import LevelManager
from gameplay.lessons import LessonManager
from ui.editor import CodeEditor

# Import all enhanced scenes
from scenes.enhanced_main_menu import EnhancedMainMenu
from scenes.enhanced_level_select import EnhancedLevelSelect
from scenes.enhanced_story_scene import EnhancedStoryScene
from scenes.enhanced_code_editor import EnhancedCodeEditor
from scenes.enhanced_competition_scene import EnhancedCompetitionScene

# Legacy scenes (kept for compatibility during transition)
from scenes.results import ResultsScene


class PrideOfCodeGame:
    def __init__(self):
        # -------------------------------
        # Window
        # -------------------------------
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # -------------------------------
        # Time management
        # -------------------------------
        self.clock = pygame.time.Clock()
        self.last_time = time.time()

        # -------------------------------
        # Systems
        # -------------------------------
        self.audio = AudioManager()
        self.save = SaveSystem()
        self.level_manager = LevelManager()
        self.lesson_manager = LessonManager()

        # -------------------------------
        # Story content system
        # -------------------------------
        from story.week_content import WeekContent
        self.week_content = WeekContent()

        # -------------------------------
        # Editor (global instance)
        # -------------------------------
        self.editor = CodeEditor(
            rect=pygame.Rect(EDITOR_X, EDITOR_Y, EDITOR_WIDTH, EDITOR_HEIGHT)
        )

        # -------------------------------
        # State Manager + Scene Registration
        # -------------------------------
        self.state_manager = StateManager()

        # Enhanced Main Menu - Complete retro-pixel design
        self.state_manager.register(
            "menu", 
            EnhancedMainMenu(self.state_manager, self))

        # Enhanced Level Select - 16-week calendar/locker room style
        self.state_manager.register("level_select",
            EnhancedLevelSelect(self.state_manager, self))

        # Enhanced Story Scene - Character portraits and dialogue system
        self.state_manager.register("story",
            EnhancedStoryScene(self.state_manager, self))

        # Enhanced Code Editor - Professional development environment
        self.state_manager.register("enhanced_editor",
            EnhancedCodeEditor(self.state_manager, self))

        # Enhanced Competition Scene - Live band performance
        self.state_manager.register("competition",
            EnhancedCompetitionScene(self.state_manager, self))

        # Results Scene (kept for now, will be enhanced later)
        self.state_manager.register("results",
            ResultsScene(self.state_manager, self))

        # Begin in main menu
        self.state_manager.switch("menu")

    # -------------------------------------------------
    # Main Game Loop
    # -------------------------------------------------
    def run(self):
        running = True

        while running:
            # --------------------------
            # Delta-time calculation
            # --------------------------
            now = time.time()
            dt = now - self.last_time
            self.last_time = now

            # --------------------------
            # Event Handling
            # --------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    # Enhanced editor handles its own events
                    if self.state_manager.current_name == "enhanced_editor":
                        # The enhanced editor handles events internally
                        pass
                    
                    self.state_manager.handle_event(event)

            # --------------------------
            # Update
            # --------------------------
            self.state_manager.update(dt)

            # --------------------------
            # Draw
            # --------------------------
            self.screen.fill((20, 20, 30))    # global background
            self.state_manager.draw(self.screen)
            pygame.display.flip()

            # --------------------------
            # Framerate cap
            # --------------------------
            self.clock.tick(60)