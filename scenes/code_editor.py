"""
Pride of Code Code Editor Screen
================================

Implementation of the code editor following the visual identity style guide.

Style Guide Reference:
Section 5.4 Code Editor Screen
"""

import pygame
from core.colors import (
    DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
    SILVER_STEEL, PRECISION_MAGENTA, STADIUM_TURF_GREEN,
    ERROR_RED, DARKER_GRAPHITE
)
from ui.components import RetroPanel, TextRenderer


class CodeEditorScene:
    """
    Code editor screen implementation.
    
    Style Guide Reference:
    Section 5.4 Code Editor Screen
    """
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_renderer = TextRenderer()
        
        # Editor state
        self.code_lines = [
            "def marching_band():",
            "    # Initialize band members",
            "    members = []",
            "    for i in range(8):",
            "        members.append(BandMember(i))",
            "    ",
            "    # Execute formation",
            "    execute_formation(members)",
            "    ",
            "    return 'Performance complete'"
        ]
        self.cursor_line = 0
        self.cursor_pos = 0
        self.scroll_offset = 0
        
        # Console output
        self.console_lines = [
            "Pride of Code v1.0",
            "Ready for performance!",
            ">>> marching_band()",
            "Performance complete"
        ]
        
        # Create UI panels
        self._create_panels()
    
    def _create_panels(self):
        """Create the editor and console panels."""
        # Editor panel (top 70% of screen)
        editor_height = int(self.screen_height * 0.7)
        self.editor_panel = RetroPanel(
            10, 10, 
            self.screen_width - 20, 
            editor_height - 20,
            border_color=SILVER_STEEL,
            background_color=DARK_GRAPHITE_BLACK,
            border_width=1
        )
        
        # Console panel (bottom 30% of screen)
        console_height = int(self.screen_height * 0.3)
        self.console_panel = RetroPanel(
            10, editor_height + 10,
            self.screen_width - 20,
            console_height - 20,
            border_color=SILVER_STEEL,
            background_color=DARKER_GRAPHITE,
            border_width=1
        )
    
    def _draw_editor_background(self, surface):
        """Draw the editor background with vignette and scanlines."""
        panel_rect = self.editor_panel.rect
        
        # Draw vignette effect (subtle darkening at edges)
        vignette_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        for y in range(panel_rect.height):
            for x in range(panel_rect.width):
                # Calculate distance from center
                center_x, center_y = panel_rect.width // 2, panel_rect.height // 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = (center_x ** 2 + center_y ** 2) ** 0.5
                
                # Calculate vignette intensity (8-10%)
                intensity = 1.0 - (distance / max_distance) * 0.09
                vignette_surf.set_at((x, y), (0, 0, 0, int(255 * (1 - intensity))))
        
        surface.blit(vignette_surf, panel_rect)
        
        # Draw subtle scanlines
        for y in range(0, panel_rect.height, 2):
            scanline = pygame.Surface((panel_rect.width, 1), pygame.SRCALPHA)
            scanline.fill((0, 0, 0, int(255 * 0.02)))  # 2% opacity
            surface.blit(scanline, (panel_rect.x, panel_rect.y + y))
    
    def _draw_code(self, surface):
        """Draw the code with syntax highlighting."""
        panel_rect = self.editor_panel.rect
        
        # Font for code
        font = self.text_renderer.fonts['large']
        line_height = font.get_height()
        
        # Draw each line of code
        for i, line in enumerate(self.code_lines):
            y_pos = panel_rect.y + 20 + (i - self.scroll_offset) * line_height
            
            # Skip lines outside the visible area
            if y_pos < panel_rect.y - line_height or y_pos > panel_rect.y + panel_rect.height:
                continue
            
            # Highlight current line
            if i == self.cursor_line:
                highlight_rect = pygame.Rect(
                    panel_rect.x + 5,
                    y_pos,
                    panel_rect.width - 10,
                    line_height
                )
                pygame.draw.rect(surface, (30, 30, 40), highlight_rect)
            
            # Apply syntax highlighting
            self._draw_syntax_highlighted_line(surface, line, panel_rect.x + 10, y_pos)
            
            # Draw line numbers
            line_num = str(i + 1)
            line_num_surf = font.render(line_num, True, SILVER_STEEL)
            line_num_rect = line_num_surf.get_rect()
            line_num_rect.right = panel_rect.x - 5
            line_num_rect.y = y_pos
            surface.blit(line_num_surf, line_num_rect)
    
    def _draw_syntax_highlighted_line(self, surface, line, x, y):
        """Draw a line of code with syntax highlighting."""
        font = self.text_renderer.fonts['large']
        
        # Simple syntax highlighting based on keywords
        keywords = ['def', 'for', 'if', 'else', 'return', 'in', 'range']
        functions = ['marching_band', 'BandMember', 'execute_formation']
        
        # Split line into tokens
        tokens = line.split(' ')
        current_x = x
        
        for token in tokens:
            # Determine token color
            color = SILVER_STEEL  # Default color
            
            # Check for keywords
            clean_token = token.strip('():,')
            if clean_token in keywords:
                color = DEEP_SIGNAL_BLUE
            elif clean_token in functions:
                color = PRECISION_MAGENTA
            elif clean_token.startswith('#'):
                color = pygame.Color(SILVER_STEEL.r, SILVER_STEEL.g, SILVER_STEEL.b, int(255 * 0.6))
            elif clean_token.startswith('"') or clean_token.startswith("'") or \
                 (token.startswith('"') and token.endswith('"')) or \
                 (token.startswith("'") and token.endswith("'")):
                color = RETRO_PIXEL_AMBER
            elif clean_token == 'True' or clean_token == 'False' or clean_token.isdigit():
                color = RETRO_PIXEL_AMBER
            
            # Render token
            token_surf = font.render(token + ' ', True, color)
            surface.blit(token_surf, (current_x, y))
            current_x += token_surf.get_width()
    
    def _draw_console(self, surface):
        """Draw the console output."""
        panel_rect = self.console_panel.rect
        
        # Font for console
        font = self.text_renderer.fonts['medium']
        line_height = font.get_height()
        
        # Draw each line of console output
        for i, line in enumerate(self.console_lines):
            y_pos = panel_rect.y + 10 + i * line_height
            
            # Skip lines outside the visible area
            if y_pos < panel_rect.y or y_pos > panel_rect.y + panel_rect.height - line_height:
                continue
            
            # Determine line color
            color = SILVER_STEEL
            if "Error" in line or "error" in line:
                color = ERROR_RED
            elif "complete" in line.lower():
                color = STADIUM_TURF_GREEN
            
            # Render line
            line_surf = font.render(line, True, color)
            surface.blit(line_surf, (panel_rect.x + 10, y_pos))
    
    def _draw_gutter_markers(self, surface):
        """Draw error markers in the gutter."""
        panel_rect = self.editor_panel.rect
        font = self.text_renderer.fonts['large']
        line_height = font.get_height()
        
        # Draw error marker on line 7 (0-indexed)
        error_line = 7
        y_pos = panel_rect.y + 20 + (error_line - self.scroll_offset) * line_height
        
        if panel_rect.y <= y_pos <= panel_rect.y + panel_rect.height - line_height:
            # Draw error underline in the code
            error_text = self.code_lines[error_line]
            text_width = font.size(error_text)[0]
            pygame.draw.line(
                surface,
                ERROR_RED,
                (panel_rect.x + 10, y_pos + line_height - 2),
                (panel_rect.x + 10 + text_width, y_pos + line_height - 2),
                2
            )
            
            # Draw error icon in gutter
            error_icon = font.render("!", True, RETRO_PIXEL_AMBER)
            surface.blit(error_icon, (panel_rect.x - 15, y_pos))
    
    def handle_event(self, event):
        """Handle pygame events."""
        self.editor_panel.handle_event(event)
        self.console_panel.handle_event(event)
        
        # Handle keyboard input for code editing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.cursor_line = max(0, self.cursor_line - 1)
            elif event.key == pygame.K_DOWN:
                self.cursor_line = min(len(self.code_lines) - 1, self.cursor_line + 1)
            elif event.key == pygame.K_RETURN:
                # Add new line
                self.code_lines.insert(self.cursor_line + 1, "")
                self.cursor_line += 1
                self.cursor_pos = 0
    
    def update(self, dt):
        """Update scene state."""
        self.editor_panel.update(dt)
        self.console_panel.update(dt)
    
    def draw(self, surface):
        """Draw the code editor scene."""
        # Draw panels
        self.editor_panel.draw(surface)
        self.console_panel.draw(surface)
        
        # Draw editor background effects
        self._draw_editor_background(surface)
        
        # Draw code
        self._draw_code(surface)
        
        # Draw console output
        self._draw_console(surface)
        
        # Draw gutter markers
        self._draw_gutter_markers(surface)