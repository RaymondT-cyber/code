
"""Enhanced Level Select / Week Planner for Pride of Code.
Features calendar/locker room style display, 16 week chapters, competition weeks,
colorblind-safe indicators, and comprehensive navigation.
"""

import pygame
import math
from typing import List, Dict, Optional, Tuple
from core.state_manager import State
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLUE, COLOR_GOLD, 
                   COLOR_TEXT, COLOR_BG, SECTION_COLORS)
from ui.enhanced_retro_button import EnhancedRetroButton


class EnhancedLevelSelect(State):
    """Enhanced level select with calendar/locker room aesthetic and 16-week structure."""
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        
        # Color scheme with colorblind-safe alternatives
        self.colors = {
            'background': COLOR_BG,
            'grid': (40, 40, 50),
            'locked': (80, 80, 90),        # Gray for locked weeks
            'unlocked': COLOR_BLUE,        # Blue for available weeks
            'completed': COLOR_GOLD,       # Gold for completed weeks
            'competition': (220, 20, 60),  # Red for competition weeks
            'text': COLOR_TEXT,
            'subtitle': (180, 180, 180),
            'hover': (100, 150, 200)
        }
        
        # Fonts
        try:
            self.font_title = pygame.font.Font(None, 48)
            self.font_header = pygame.font.Font(None, 32)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
            self.font_tiny = pygame.font.Font(None, 14)
        except:
            self.font_title = pygame.font.SysFont('arial', 48, bold=True)
            self.font_header = pygame.font.SysFont('arial', 32, bold=True)
            self.font_medium = pygame.font.SysFont('arial', 24)
            self.font_small = pygame.font.SysFont('arial', 18)
            self.font_tiny = pygame.font.SysFont('arial', 14)

        # Create font dictionary for buttons
        self.fonts = {
            'font_title': self.font_title,
            'font_header': self.font_header,
            'font_medium': self.font_medium,
            'font_small': self.font_small,
            'font_tiny': self.font_tiny
        }
        
        # Week data structure
        self.weeks = self._create_week_data()
        
        # Calendar grid setup
        self.grid_cols = 4
        self.grid_rows = 4
        self.week_buttons = []
        self._create_week_grid()
        
        # Navigation buttons
        self._create_navigation_buttons()
        
        # UI state
        self.selected_week = 0
        self.animation_time = 0.0
        self.show_details = False
        self.detail_week = None
        
        # Accessibility
        self.colorblind_mode = False
        self.keyboard_nav = True
        
    def _create_week_data(self) -> List[Dict]:
        """Create data for all 16 weeks with competition weeks highlighted."""
        weeks = []
        
        # Import level manager to get actual level data
        from gameplay.level_manager import LevelManager
        level_manager = LevelManager()
        
        # Week titles and themes
        week_data = [
            {"title": "Fresh Beats, Fresh Start", "theme": "Variables", "competition": False, "level_id": "week1"},
            {"title": "First Competition Frenzy", "theme": "Conditionals", "competition": True, "level_id": "competition1"},
            {"title": "Loops of Rehearsal", "theme": "Loops", "competition": False, "level_id": "week2"},
            {"title": "Functions and Formations", "theme": "Functions", "competition": True, "level_id": "competition2"},
            {"title": "Harmony and Discord", "theme": "Lists", "competition": False, "level_id": "week3"},
            {"title": "Midseason Mayhem", "theme": "Dictionaries", "competition": True, "level_id": "competition1"},
            {"title": "Blueprints and Bonds", "theme": "Classes", "competition": False, "level_id": "week4"},
            {"title": "Autumn Showdown", "theme": "Modules", "competition": True, "level_id": "competition2"},
            {"title": "Calibration and Code", "theme": "Debugging & File I/O", "competition": False, "level_id": "week1"},
            {"title": "Blackout Performance", "theme": "Exception Handling", "competition": True, "level_id": "competition1"},
            {"title": "Symphony of Synergy", "theme": "Advanced Loops & Functions", "competition": False, "level_id": "week2"},
            {"title": "The City Parade", "theme": "APIs & Integration", "competition": True, "level_id": "competition2"},
            {"title": "Cutting Edge Code", "theme": "Advanced Algorithms", "competition": False, "level_id": "week3"},
            {"title": "Road to Championship", "theme": "Review & Integration", "competition": True, "level_id": "competition1"},
            {"title": "The Night Before", "theme": "Final Preparations", "competition": False, "level_id": "week4"},
            {"title": "Championship Finale", "theme": "Triumph & Reflection", "competition": True, "level_id": "competition2"},
        ]
        
        for i, data in enumerate(week_data):
            week_num = i + 1
            
            # Determine status (for demo, unlock progressively)
            status = "locked"
            if week_num == 1:
                status = "unlocked"
            elif week_num <= 4:  # Demo unlock first 4 weeks
                status = "unlocked"
            elif week_num <= 2:  # Demo completed
                status = "completed"
                
            # Get level info from level manager
            level_info = level_manager.get_level(data['level_id'])
            
            # Create week data
            week = {
                'number': week_num,
                'title': data['title'],
                'theme': data['theme'],
                'competition': data['competition'],
                'level_id': data['level_id'],
                'status': status,  # locked, unlocked, completed
                'score': None,     # Competition score
                'best_score': None,
                'lessons_completed': 0,
                'total_lessons': 3 if not data['competition'] else 5
            }
            
            # Add demo scores for completed weeks
            if status == "completed" and data['competition']:
                week['score'] = 85 + (week_num * 2)
                week['best_score'] = 90 + week_num
                
            weeks.append(week)
            
        return weeks
        
    def _create_week_grid(self):
        """Create the week selection grid."""
        grid_start_x = 150
        grid_start_y = 180
        cell_width = 180
        cell_height = 120
        spacing_x = 20
        spacing_y = 20
        
        self.week_buttons = []
        
        for i, week in enumerate(self.weeks):
            row = i // self.grid_cols
            col = i % self.grid_cols
            
            x = grid_start_x + col * (cell_width + spacing_x)
            y = grid_start_y + row * (cell_height + spacing_y)
            
            button = WeekButton(
                x, y, cell_width, cell_height,
                week, self.colors, self.fonts
            )
            button.on_click = lambda w=week: self._select_week(w)
            self.week_buttons.append(button)
            
    def _create_navigation_buttons(self):
        """Create navigation and action buttons."""
        button_y = WINDOW_HEIGHT - 80
        
        self.nav_buttons = [
            EnhancedRetroButton(
                50, button_y, 150, 50,
                "BACK TO MENU",
                color=(100, 40, 40),
                on_click=lambda: self._go_to_menu()
            ),
            EnhancedRetroButton(
                WINDOW_WIDTH - 200, button_y, 150, 50,
                "SETTINGS",
                color=(60, 60, 60),
                on_click=lambda: self._toggle_settings()
            ),
            EnhancedRetroButton(
                WINDOW_WIDTH // 2 - 75, button_y, 150, 50,
                "CONTINUE",
                color=self.colors['unlocked'],
                on_click=lambda: self._continue_game()
            )
        ]
        
    def _select_week(self, week: Dict):
        """Handle week selection."""
        if week['status'] == "locked":
            return  # Can't select locked weeks
            
        self.selected_week = week['number'] - 1
        self.detail_week = week
        self.show_details = True
        
        # Play selection sound
        self._play_sound('select')
        
    def _go_to_menu(self):
        """Return to main menu."""
        self._play_sound('back')
        self.manager.switch('menu')
        
    def _toggle_settings(self):
        """Toggle settings panel."""
        self._play_sound('click')
        self.colorblind_mode = not self.colorblind_mode
        # Update all week buttons with new color scheme
        for button in self.week_buttons:
            button.update_color_scheme(self.colorblind_mode)
            
    def _continue_game(self):
        """Continue with selected or next available week."""
        available_weeks = [w for w in self.weeks if w['status'] in ['unlocked', 'completed']]
        if available_weeks:
            target_week = available_weeks[-1]  # Last available
            self._start_week(target_week)
            
    def _start_week(self, week: Dict):
        """Start the selected week."""
        self._play_sound('start')
        level_id = week['level_id']
        self.manager.switch('enhanced_editor', level_id=level_id)
        
    def _play_sound(self, sound_type: str):
        """Play sound effects (placeholder for audio system)."""
        # This would integrate with the actual audio system
        sounds = {
            'select': 523,   # C5
            'click': 440,    # A4
            'back': 349,     # F4
            'start': 659     # E5
        }
        frequency = sounds.get(sound_type, 440)
        print(f"\u266a Sound effect: {sound_type} ({frequency}Hz)")
        
    def handle_event(self, ev):
        """Handle input events."""
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self._go_to_menu()
            elif ev.key == pygame.K_TAB:
                self.show_details = not self.show_details
            elif ev.key == pygame.K_RETURN:
                if self.detail_week:
                    self._start_week(self.detail_week)
                    
        # Handle week button events
        for button in self.week_buttons:
            if button.handle_event(ev):
                return
                
        # Handle navigation button events
        for button in self.nav_buttons:
            button.handle_event(ev)
            
    def update(self, dt):
        """Update animations."""
        self.animation_time += dt
        
        # Update all buttons
        for button in self.week_buttons:
            button.update(dt)
        for button in self.nav_buttons:
            button.update(dt)
            
    def draw(self, surface):
        """Render the enhanced level select screen."""
        # Draw background
        surface.fill(self.colors['background'])
        
        # Draw locker room background elements
        self._draw_locker_room(surface)
        
        # Draw title and headers
        self._draw_title(surface)
        self._draw_legend(surface)
        
        # Draw week grid
        self._draw_week_grid(surface)
        
        # Draw navigation buttons
        self._draw_navigation(surface)
        
        # Draw week details panel if active
        if self.show_details and self.detail_week:
            self._draw_week_details(surface, self.detail_week)
            
    def _draw_locker_room(self, surface):
        """Draw locker room background aesthetic."""
        # Locker silhouettes
        locker_color = (30, 30, 40)
        
        for x in range(0, WINDOW_WIDTH, 80):
            if x % 160 == 0:
                # Tall lockers
                pygame.draw.rect(surface, locker_color, (x, 50, 30, 80))
                pygame.draw.rect(surface, (25, 25, 35), (x + 2, 52, 26, 76))
                pygame.draw.circle(surface, (60, 60, 70), (x + 15, 90), 3)
            else:
                # Short lockers
                pygame.draw.rect(surface, locker_color, (x, 70, 30, 60))
                pygame.draw.rect(surface, (25, 25, 35), (x + 2, 72, 26, 56))
                pygame.draw.circle(surface, (60, 60, 70), (x + 15, 100), 3)
                
        # Bench
        bench_rect = pygame.Rect(50, WINDOW_HEIGHT - 120, WINDOW_WIDTH - 100, 15)
        pygame.draw.rect(surface, (40, 30, 20), bench_rect)
        pygame.draw.rect(surface, (30, 20, 10), bench_rect.inflate(-2, -2))
        
    def _draw_title(self, surface):
        """Draw screen title and subtitle."""
        # Main title
        title = self.font_title.render("SEASON PLANNER", True, self.colors['text'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40))
        
        # Title shadow
        title_shadow = self.font_title.render("SEASON PLANNER", True, (0, 0, 0))
        surface.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        surface.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("16 Weeks to Championship", True, self.colors['subtitle'])
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 80))
        surface.blit(subtitle, subtitle_rect)
        
        # Progress indicator
        completed = len([w for w in self.weeks if w['status'] == 'completed'])
        progress_text = f"Progress: {completed}/16 weeks completed"
        progress_surf = self.font_small.render(progress_text, True, self.colors['subtitle'])
        progress_rect = progress_surf.get_rect(center=(WINDOW_WIDTH // 2, 110))
        surface.blit(progress_surf, progress_rect)
        
    def _draw_legend(self, surface):
        """Draw legend for week status indicators."""
        legend_x = 50
        legend_y = 140
        
        legend_items = [
            ("Available", self.colors['unlocked'], 'square'),
            ("Completed", self.colors['completed'], 'star'),
            ("Competition", self.colors['competition'], 'trophy'),
            ("Locked", self.colors['locked'], 'lock')
        ]
        
        for i, (label, color, icon_type) in enumerate(legend_items):
            x = legend_x + i * 180
            
            # Draw icon
            if icon_type == 'square':
                pygame.draw.rect(surface, color, (x, legend_y, 16, 16))
                pygame.draw.rect(surface, (255, 255, 255), (x, legend_y, 16, 16), 2)
            elif icon_type == 'star':
                self._draw_star(surface, x + 8, legend_y + 8, 8, color)
            elif icon_type == 'trophy':
                self._draw_trophy(surface, x + 8, legend_y + 8, 8, color)
            elif icon_type == 'lock':
                self._draw_lock(surface, x + 8, legend_y + 8, 8, color)
                
            # Draw label
            label_surf = self.font_small.render(label, True, self.colors['subtitle'])
            surface.blit(label_surf, (x + 25, legend_y))
            
    def _draw_star(self, surface, x, y, size, color):
        """Draw a star icon."""
        points = []
        for i in range(10):
            angle = math.pi * i / 5 - math.pi / 2
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.5
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(surface, color, points)
        
    def _draw_trophy(self, surface, x, y, size, color):
        """Draw a trophy icon."""
        # Cup
        pygame.draw.rect(surface, color, (x - size//2, y - size//2, size, size//2))
        pygame.draw.rect(surface, (255, 255, 255), (x - size//2, y - size//2, size, size//2), 1)
        # Base
        pygame.draw.rect(surface, color, (x - size//3, y, size//3 * 2, size//3))
        
    def _draw_lock(self, surface, x, y, size, color):
        """Draw a lock icon."""
        # Lock body
        pygame.draw.rect(surface, color, (x - size//2, y, size, size//2))
        # Lock shackle
        pygame.draw.arc(surface, color, (x - size//2, y - size//2, size, size), 
                       math.pi, 0, 2)
                       
    def _draw_week_grid(self, surface):
        """Draw the week selection grid."""
        # Draw grid lines
        grid_color = self.colors['grid']
        for i in range(self.grid_cols + 1):
            x = 150 + i * 200
            pygame.draw.line(surface, grid_color, (x, 170), (x, 670), 1)
            
        for i in range(self.grid_rows + 1):
            y = 170 + i * 140
            pygame.draw.line(surface, grid_color, (130, y), (WINDOW_WIDTH - 130, y), 1)
            
        # Draw week buttons
        for button in self.week_buttons:
            button.draw(surface)
            
    def _draw_navigation(self, surface):
        """Draw navigation buttons."""
        for button in self.nav_buttons:
            button.draw(surface)
            
    def _draw_week_details(self, surface, week: Dict):
        """Draw detailed information panel for selected week."""
        # Panel background
        panel_width = 400
        panel_height = 300
        panel_x = WINDOW_WIDTH - panel_width - 50
        panel_y = 150
        
        # Create semi-transparent surface
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((20, 20, 30, 240))
        surface.blit(panel_surf, (panel_x, panel_y))
        
        # Panel border
        border_color = self.colors['unlocked'] if week['status'] != 'locked' else self.colors['locked']
        pygame.draw.rect(surface, border_color, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Week title
        title = f"Week {week['number']}: {week['title']}"
        title_surf = self.font_medium.render(title, True, self.colors['text'])
        surface.blit(title_surf, (panel_x + 20, panel_y + 20))
        
        # Theme
        theme_text = f"Python Theme: {week['theme']}"
        theme_surf = self.font_small.render(theme_text, True, self.colors['subtitle'])
        surface.blit(theme_surf, (panel_x + 20, panel_y + 50))
        
        # Competition indicator
        if week['competition']:
            comp_text = "\ud83c\udfc6 COMPETITION WEEK"
            comp_surf = self.font_medium.render(comp_text, True, self.colors['competition'])
            surface.blit(comp_surf, (panel_x + 20, panel_y + 80))
            
        # Status
        status_text = f"Status: {week['status'].upper()}"
        status_color = self.colors[week['status']] if week['status'] in self.colors else self.colors['text']
        status_surf = self.font_small.render(status_text, True, status_color)
        surface.blit(status_surf, (panel_x + 20, panel_y + 110))
        
        # Lessons progress
        if week['total_lessons'] > 0:
            lessons_text = f"Lessons: {week['lessons_completed']}/{week['total_lessons']}"
            lessons_surf = self.font_small.render(lessons_text, True, self.colors['subtitle'])
            surface.blit(lessons_surf, (panel_x + 20, panel_y + 140))
            
            # Progress bar
            bar_width = panel_width - 40
            bar_height = 10
            bar_x = panel_x + 20
            bar_y = panel_y + 165
            
            pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            progress = week['lessons_completed'] / week['total_lessons']
            fill_width = int(bar_width * progress)
            pygame.draw.rect(surface, COLOR_GOLD, (bar_x, bar_y, fill_width, bar_height))
            
        # Score (if competition)
        if week['competition'] and week['score']:
            score_text = f"Last Score: {week['score']}%"
            score_surf = self.font_small.render(score_text, True, self.colors['text'])
            surface.blit(score_surf, (panel_x + 20, panel_y + 185))
            
            if week['best_score']:
                best_text = f"Best Score: {week['best_score']}%"
                best_surf = self.font_small.render(best_text, True, COLOR_GOLD)
                surface.blit(best_surf, (panel_x + 20, panel_y + 205))
                
        # Action buttons
        if week['status'] != 'locked':
            start_button = EnhancedRetroButton(
                panel_x + 20, panel_y + panel_height - 60, 150, 40,
                "START WEEK",
                color=self.colors['unlocked'],
                on_click=lambda: self._start_week(week)
            )
            start_button.draw(surface)
            
        # Close button
        close_button = EnhancedRetroButton(
            panel_x + panel_width - 80, panel_y + 10, 60, 25,
            "X",
            color=(100, 40, 40),
            on_click=lambda: setattr(self, 'show_details', False)
        )
        close_button.draw(surface)


class WeekButton(EnhancedRetroButton):
    """Specialized button for week selection with status indicators."""
    
    def __init__(self, x, y, width, height, week_data, colors, fonts):
        self.week_data = week_data
        self.colors = colors
        self.fonts = fonts
        
        # Determine color based on status
        color_map = {
            'locked': colors['locked'],
            'unlocked': colors['unlocked'],
            'completed': colors['completed']
        }
        color = color_map.get(week_data['status'], colors['locked'])
        
        super().__init__(x, y, width, height, "", color)
        self.on_click = None
        
    def update_color_scheme(self, colorblind_mode: bool):
        """Update colors for colorblind mode."""
        if colorblind_mode:
            # Use patterns and shapes instead of colors
            pass
        else:
            # Use original colors
            pass
            
    def draw(self, surface):
        """Draw the week button with status indicators."""
        # Base button drawing
        super().draw(surface)
        
        # Draw week number
        week_text = f"Week {self.week_data['number']}"
        week_color = self.colors['text'] if self.week_data['status'] != 'locked' else (120, 120, 120)
        week_surf = self.fonts['font_medium'].render(week_text, True, week_color)
        week_rect = week_surf.get_rect(center=(self.rect.centerx, self.rect.y + 25))
        surface.blit(week_surf, week_rect)
        
        # Draw competition icon
        if self.week_data['competition']:
            if self.week_data['status'] == 'completed':
                # Trophy for completed competition
                self._draw_trophy(surface, self.rect.right - 20, self.rect.y + 15, 8, self.colors['completed'])
            elif self.week_data['status'] == 'unlocked':
                # Star for available competition
                self._draw_star(surface, self.rect.right - 20, self.rect.y + 15, 8, self.colors['competition'])
            else:
                # Lock for locked competition
                self._draw_lock(surface, self.rect.right - 20, self.rect.y + 15, 8, self.colors['locked'])
                
        # Draw week title (truncated if needed)
        title = self.week_data['title']
        if len(title) > 20:
            title = title[:17] + "..."
            
        title_color = week_color
        title_surf = self.fonts['font_small'].render(title, True, title_color)
        title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(title_surf, title_rect)
        
        # Draw theme
        theme = self.week_data['theme']
        theme_color = (150, 150, 150) if self.week_data['status'] != 'locked' else (80, 80, 80)
        theme_surf = self.fonts['font_tiny'].render(theme, True, theme_color)
        theme_rect = theme_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
        surface.blit(theme_surf, theme_rect)
        
        # Draw status indicator (colorblind-safe shape)
        if self.week_data['status'] == 'locked':
            # Draw lock pattern
            for i in range(3):
                for j in range(3):
                    if (i + j) % 2 == 0:
                        pygame.draw.rect(surface, (50, 50, 50), 
                                       (self.rect.x + 10 + i * 10, self.rect.y + 10 + j * 10, 8, 8))
                                       
    def _draw_star(self, surface, x, y, size, color):
        """Draw a star icon."""
        points = []
        for i in range(10):
            angle = math.pi * i / 5 - math.pi / 2
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.5
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(surface, color, points)
        
    def _draw_trophy(self, surface, x, y, size, color):
        """Draw a trophy icon."""
        # Cup
        pygame.draw.rect(surface, color, (x - size//2, y - size//2, size, size//2))
        pygame.draw.rect(surface, (255, 255, 255), (x - size//2, y - size//2, size, size//2), 1)
        # Base
        pygame.draw.rect(surface, color, (x - size//3, y, size//3 * 2, size//3))
        
    def _draw_lock(self, surface, x, y, size, color):
        """Draw a lock icon."""
        # Lock body
        pygame.draw.rect(surface, color, (x - size//2, y, size, size//2))
        # Lock shackle
        pygame.draw.arc(surface, color, (x - size//2, y - size//2, size, size), 
                       math.pi, 0, 2)
