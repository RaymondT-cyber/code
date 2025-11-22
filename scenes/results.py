import math
import pygame
from core.state_manager import State
from config import COLOR_BLUE, COLOR_GOLD, COLOR_TEXT, COLOR_BG
from ui.enhanced_retro_button import EnhancedRetroButton


class ResultsScene(State):
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.font = pygame.font.SysFont('arial', 24)
        self.font_large = pygame.font.SysFont('arial', 36, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
        
        # Results data
        self.scores = {}
        self.total_score = 0
        self.performance_time = 0
        self.moves_completed = 0
        self.sync_rate = 0
        
        # Color scheme with retro bowl colors
        self.colors = {
            'background': COLOR_BG,
            'text': COLOR_TEXT,
            'gold': COLOR_GOLD,
            'blue': COLOR_BLUE,
            'success': (0, 255, 127),       # Neon green
            'creativity': (0, 255, 255),    # Neon cyan
            'performance': (255, 0, 255),   # Neon magenta
            'field_green': (34, 139, 34),   # Field green
            'stadium_gray': (80, 80, 90)    # Stadium gray
        }
        
        # UI elements
        self.buttons = []
        
        # Animation
        self.animation_time = 0.0
        
    def enter(self, **params):
        """Called when entering this state."""
        # Get results data
        self.scores = params.get('scores', {})
        self.total_score = params.get('total_score', 0)
        self.performance_time = params.get('performance_time', 0)
        self.moves_completed = params.get('moves_completed', 0)
        self.sync_rate = params.get('sync_rate', 0)
        
        # Create UI elements
        self._create_buttons()
        
    def _create_buttons(self):
        """Create navigation buttons."""
        button_width = 200
        button_height = 50
        button_x = pygame.display.get_surface().get_width() // 2 - button_width // 2
        start_y = 500
        spacing = 70
        
        self.buttons = [
            EnhancedRetroButton(
                button_x, start_y, button_width, button_height,
                "NEXT WEEK",
                color=self.colors['blue'],
                on_click=lambda: self._next_week()
            ),
            EnhancedRetroButton(
                button_x, start_y + spacing, button_width, button_height,
                "RETRY",
                color=(100, 100, 100),
                on_click=lambda: self._retry()
            ),
            EnhancedRetroButton(
                button_x, start_y + spacing * 2, button_width, button_height,
                "MAIN MENU",
                color=(120, 40, 40),
                on_click=lambda: self._main_menu()
            )
        ]
        
    def _next_week(self):
        """Go to the next week."""
        # For now, just go back to level select
        self.manager.switch('level_select')
        
    def _retry(self):
        """Retry the current performance."""
        self.manager.switch('competition')
        
    def _main_menu(self):
        """Return to main menu."""
        self.manager.switch('menu')
        
    def handle_event(self, ev):
        """Handle input events."""
        for button in self.buttons:
            if button.handle_event(ev):
                return
                
        # Handle keyboard shortcuts
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self._main_menu()
            elif ev.key == pygame.K_RETURN:
                self._next_week()
            elif ev.key == pygame.K_r:
                self._retry()
                
    def update(self, dt):
        """Update animations."""
        self.animation_time += dt
        
        for button in self.buttons:
            button.update(dt)
            
    def draw(self, surface):
        """Draw the results screen."""
        surface.fill(self.colors['background'])
        
        # Draw stadium decorations
        self._draw_stadium_decorations(surface)
        
        # Draw title
        title = self.font_large.render("PERFORMANCE RESULTS", True, self.colors['gold'])
        title_rect = title.get_rect(center=(surface.get_width() // 2, 60))
        surface.blit(title, title_rect)
        
        # Draw score summary with animation
        score_text = f"TOTAL SCORE: {self.total_score:.1f}%"
        score_surf = self.font_large.render(score_text, True, self.colors['text'])
        score_rect = score_surf.get_rect(center=(surface.get_width() // 2, 120))
        surface.blit(score_surf, score_rect)
        
        # Draw animated score meter
        self._draw_score_meter(surface)
        
        # Draw individual scores
        if self.scores:
            y_pos = 180
            score_items = [
                ('Correctness', self.scores.get('correctness', 0), self.colors['success']),
                ('Creativity', self.scores.get('creativity', 0), self.colors['creativity']),
                ('Performance', self.scores.get('performance', 0), self.colors['performance'])
            ]
            
            for label, score, color in score_items:
                # Draw label
                label_surf = self.font.render(f"{label}:", True, self.colors['text'])
                surface.blit(label_surf, (100, y_pos))
                
                # Draw score
                score_surf = self.font.render(f"{score:.1f}%", True, color)
                surface.blit(score_surf, (300, y_pos))
                
                # Draw progress bar
                bar_width = 400
                bar_height = 20
                bar_x = 400
                pygame.draw.rect(surface, (40, 40, 50), (bar_x, y_pos, bar_width, bar_height))
                fill_width = int((score / 100.0) * bar_width)
                pygame.draw.rect(surface, color, (bar_x, y_pos, fill_width, bar_height))
                pygame.draw.rect(surface, self.colors['text'], (bar_x, y_pos, bar_width, bar_height), 2)
                
                # Draw animated particles for high scores
                if score > 80:
                    self._draw_score_particles(surface, bar_x + fill_width, y_pos + bar_height//2, color)
                
                y_pos += 40
                
        # Draw additional stats
        stats_y = 350
        stats = [
            f"Performance Time: {self.performance_time:.1f}s",
            f"Moves Completed: {self.moves_completed}",
            f"Sync Rate: {self.sync_rate:.1f}%"
        ]
        
        for i, stat in enumerate(stats):
            stat_surf = self.font_small.render(stat, True, (180, 180, 180))
            surface.blit(stat_surf, (100, stats_y + i * 30))
            
        # Draw performance rating
        rating_y = 450
        if self.total_score >= 90:
            rating = "OUTSTANDING!"
            rating_color = self.colors['gold']  # Gold
        elif self.total_score >= 80:
            rating = "EXCELLENT!"
            rating_color = (144, 238, 144)  # Light green
        elif self.total_score >= 70:
            rating = "GOOD!"
            rating_color = (100, 149, 237)  # Cornflower blue
        elif self.total_score >= 60:
            rating = "FAIR"
            rating_color = (255, 140, 0)  # Dark orange
        else:
            rating = "NEEDS IMPROVEMENT"
            rating_color = (220, 20, 60)  # Crimson
            
        rating_surf = self.font_large.render(rating, True, rating_color)
        rating_rect = rating_surf.get_rect(center=(surface.get_width() // 2, rating_y))
        surface.blit(rating_surf, rating_rect)
        
        # Draw animated trophy for high scores
        if self.total_score >= 80:
            self._draw_trophy(surface, surface.get_width() // 2 + 200, rating_y)
            
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Draw instructions
        instructions = self.font_small.render("ENTER: Next Week | R: Retry | ESC: Main Menu", True, (100, 100, 100))
        instructions_rect = instructions.get_rect(center=(surface.get_width() // 2, surface.get_height() - 30))
        surface.blit(instructions, instructions_rect)
        
    def _draw_stadium_decorations(self, surface):
        """Draw stadium decorations in the background."""
        # Draw field lines
        for y in range(100, 600, 40):
            pygame.draw.line(surface, self.colors['field_green'], (0, y), (surface.get_width(), y), 1)
            
        # Draw stadium tiers
        for i in range(5):
            tier_width = 300 - i * 40
            pygame.draw.rect(surface, self.colors['stadium_gray'], 
                           (surface.get_width() // 2 - tier_width // 2, 30 + i * 10, tier_width, 8))
            
    def _draw_score_meter(self, surface):
        """Draw an animated score meter."""
        center_x = surface.get_width() // 2
        center_y = 220
        radius = 80
        
        # Draw meter background
        pygame.draw.circle(surface, (40, 40, 50), (center_x, center_y), radius)
        pygame.draw.circle(surface, self.colors['text'], (center_x, center_y), radius, 3)
        
        # Draw score arc
        if self.total_score > 0:
            angle = (self.total_score / 100.0) * 360
            for i in range(int(angle)):
                rad = math.radians(i - 90)
                x1 = center_x + (radius - 10) * math.cos(rad)
                y1 = center_y + (radius - 10) * math.sin(rad)
                x2 = center_x + radius * math.cos(rad)
                y2 = center_y + radius * math.sin(rad)
                color = self._get_score_color(i / 360.0 * 100)
                pygame.draw.line(surface, color, (x1, y1), (x2, y2), 3)
                
        # Draw center circle
        pygame.draw.circle(surface, self.colors['background'], (center_x, center_y), radius - 20)
        
        # Draw score in center
        score_text = f"{self.total_score:.0f}"
        score_surf = self.font_large.render(score_text, True, self.colors['text'])
        score_rect = score_surf.get_rect(center=(center_x, center_y))
        surface.blit(score_surf, score_rect)
        
        # Draw percentage sign
        percent_surf = self.font.render("%", True, self.colors['text'])
        surface.blit(percent_surf, (center_x + 30, center_y - 10))
        
    def _get_score_color(self, score):
        """Get color based on score."""
        if score >= 90:
            return self.colors['gold']
        elif score >= 80:
            return self.colors['success']
        elif score >= 70:
            return self.colors['creativity']
        elif score >= 60:
            return (255, 140, 0)
        else:
            return (220, 20, 60)
            
    def _draw_score_particles(self, surface, x, y, color):
        """Draw animated particles for high scores."""
        for i in range(5):
            angle = self.animation_time * 2 + i * (2 * math.pi / 5)
            distance = 5 + abs(math.sin(self.animation_time * 3 + i)) * 10
            px = x + int(distance * math.cos(angle))
            py = y + int(distance * math.sin(angle))
            
            # Pulsing particle
            pulse = abs(math.sin(self.animation_time * 5 + i))
            size = int(2 + pulse * 3)
            
            pygame.draw.circle(surface, color, (px, py), size)
            
    def _draw_trophy(self, surface, x, y):
        """Draw an animated trophy."""
        # Trophy base
        pygame.draw.rect(surface, self.colors['gold'], (x - 15, y + 10, 30, 15))
        
        # Trophy cup
        pygame.draw.rect(surface, self.colors['gold'], (x - 10, y - 20, 20, 30))
        pygame.draw.rect(surface, (255, 255, 255), (x - 10, y - 20, 20, 30), 2)
        
        # Trophy handle
        pygame.draw.rect(surface, self.colors['gold'], (x - 25, y - 10, 10, 5))
        pygame.draw.rect(surface, self.colors['gold'], (x + 15, y - 10, 10, 5))
        
        # Animated sparkle
        sparkle_size = int(3 + abs(math.sin(self.animation_time * 4)) * 2)
        pygame.draw.circle(surface, (255, 255, 255), (x, y - 30), sparkle_size)
