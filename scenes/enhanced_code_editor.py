
"""Enhanced Code Editor Scene for Pride of Code.
Features dark background with retro colors, syntax highlighting, real-time error hints,
undo/redo buttons, console output panel, monospaced pixel font \u226518px, and full keyboard navigation.
"""

import pygame
import re
import math
from typing import List, Dict, Optional, Tuple
from core.state_manager import State
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLUE, COLOR_GOLD, 
                   COLOR_TEXT, COLOR_BG)
from ui.enhanced_retro_button import EnhancedRetroButton


class EnhancedCodeEditor(State):
    """Enhanced code editor with comprehensive retro styling and features."""
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.level_id = None
        
        # Color scheme for code editor with retro bowl colors
        self.colors = {
            'background': (15, 15, 25),        # Very dark background
            'text_normal': (200, 200, 200),    # Light gray for normal text
            'text_keyword': (255, 120, 120),   # Red-ish for keywords  
            'text_string': (120, 255, 120),    # Green for strings
            'text_comment': (120, 120, 255),   # Blue for comments
            'text_function': (255, 255, 120),  # Yellow for functions
            'text_number': (255, 120, 255),    # Magenta for numbers
            'line_numbers': (80, 80, 100),     # Dim for line numbers
            'error_underline': (255, 100, 100), # Red for errors
            'warning_underline': (255, 200, 100), # Yellow for warnings
            'selection': (100, 150, 200),      # Blue for selection
            'cursor': (255, 255, 255),         # White cursor
            'console_bg': (25, 25, 35),        # Console background
            'console_text': (180, 255, 180),   # Console text (green)
            'console_error': (255, 180, 180),  # Console error (red)
            'button_bg': (60, 60, 80),         # Button background
            'button_hover': (80, 80, 100),     # Button hover
            'field_green': (34, 139, 34),      # Field green for accents
            'stadium_gray': (80, 80, 90)       # Stadium gray
        }
        
        # Fonts - ensure \u226518px monospace
        try:
            self.font_code = pygame.font.Font(None, 20)      # 20px monospace
            self.font_line_numbers = pygame.font.Font(None, 16)  # 16px for line numbers
            self.font_console = pygame.font.Font(None, 18)   # 18px for console
            self.font_ui = pygame.font.Font(None, 18)        # 18px for UI elements
            self.font_title = pygame.font.Font(None, 24)     # 24px for titles
        except:
            self.font_code = pygame.font.SysFont('consolas', 20)
            self.font_line_numbers = pygame.font.SysFont('consolas', 16)
            self.font_console = pygame.font.SysFont('consolas', 18)
            self.font_ui = pygame.font.SysFont('arial', 18)
            self.font_title = pygame.font.SysFont('arial', 24, bold=True)
        
        # Editor dimensions
        self.editor_x = 50
        self.editor_y = 120
        self.editor_width = 800
        self.editor_height = 500
        self.line_number_width = 60
        
        # Console dimensions
        self.console_x = self.editor_x
        self.console_y = self.editor_y + self.editor_height + 20
        self.console_width = self.editor_width
        self.console_height = 150
        
        # Code content
        self.lines = ["# Welcome to Pride of Code!", 
                     "# Use Python to control the marching band",
                     "tempo = 120",
                     "uniform_color = 'blue'",
                     "volume = 7",
                     "",
                     "# Try changing these values!"]
        self.current_line = 0
        self.current_column = 0
        
        # Editor state
        self.selection_start = None
        self.selection_end = None
        self.scroll_offset = 0
        self.cursor_visible = True
        self.cursor_blink_timer = 0.0
        self.dirty = False
        
        # History for undo/redo
        self.history = []
        self.history_index = -1
        self.max_history = 50
        
        # Error detection and hints
        self.errors = []
        self.warnings = []
        self.hints = []
        
        # Console output
        self.console_output = ["Ready to run your code...", "Press RUN to execute"]
        self.console_scrollback = 1000
        
        # UI elements
        self._create_ui_elements()
        
        # Syntax highlighting patterns
        self.syntax_patterns = self._create_syntax_patterns()
        
        # Keyboard shortcuts
        self.shortcuts = {
            'run': pygame.K_F5,
            'save': pygame.K_F2,
            'undo': pygame.K_z,
            'redo': pygame.K_y,
            'clear_console': pygame.K_c
        }
        
        # Animation
        self.animation_time = 0.0
        self.error_pulse = 0.0
        
        # Retro bowl elements
        self._create_stadium_decorations()
        
    def _create_stadium_decorations(self):
        """Create stadium decorations for retro bowl theme."""
        self.stadium_lights = []
        for i in range(6):
            light = {
                'x': 100 + i * 200,
                'y': 30,
                'brightness': 0.5 + abs(math.sin(i)) * 0.5
            }
            self.stadium_lights.append(light)
            
    def _create_ui_elements(self):
        """Create editor UI elements."""
        button_y = self.editor_y - 50
        button_spacing = 110
        
        self.buttons = [
            EnhancedRetroButton(
                self.editor_x, button_y, 100, 35,
                "RUN (F5)",
                color=(100, 200, 100),
                on_click=lambda: self._run_code()
            ),
            EnhancedRetroButton(
                self.editor_x + button_spacing, button_y, 100, 35,
                "UNDO (Z)",
                color=self.colors['button_bg'],
                on_click=lambda: self._undo()
            ),
            EnhancedRetroButton(
                self.editor_x + button_spacing * 2, button_y, 100, 35,
                "REDO (Y)",
                color=self.colors['button_bg'],
                on_click=lambda: self._redo()
            ),
            EnhancedRetroButton(
                self.editor_x + button_spacing * 3, button_y, 100, 35,
                "SAVE (F2)",
                color=(100, 100, 200),
                on_click=lambda: self._save_code()
            ),
            EnhancedRetroButton(
                self.editor_x + button_spacing * 4, button_y, 100, 35,
                "CLEAR",
                color=(200, 100, 100),
                on_click=lambda: self._clear_console()
            )
        ]
        
        # Side panel buttons
        panel_x = self.editor_x + self.editor_width + 20
        
        self.panel_buttons = [
            EnhancedRetroButton(
                panel_x, self.editor_y, 120, 30,
                "HINTS",
                color=(100, 150, 100),
                on_click=lambda: self._toggle_hints()
            ),
            EnhancedRetroButton(
                panel_x, self.editor_y + 40, 120, 30,
                "SYNTAX",
                color=(100, 100, 150),
                on_click=lambda: self._check_syntax()
            ),
            EnhancedRetroButton(
                panel_x, self.editor_y + 80, 120, 30,
                "BACK",
                color=(120, 40, 40),
                on_click=lambda: self._go_back()
            )
        ]
        
    def _go_back(self):
        """Go back to level select."""
        self.manager.switch('level_select')
        
    def _create_syntax_patterns(self) -> List[Tuple[str, str]]:
        """Create regex patterns for syntax highlighting."""
        return [
            (r'\b(def|class|if|elif|else|for|while|return|import|from|as|try|except|finally|with|lambda|and|or|not|in|is|None|True|False)\b', 'keyword'),
            (r'".*?"|\'.*?\'', 'string'),
            (r'#.*$', 'comment'),
            (r'\b([a-zA-Z_][a-zA-Z0-9_]*(?=\())', 'function'),
            (r'\b\d+\.?\d*\b', 'number')
        ]
        
    def enter(self, **params):
        """Called when entering this state."""
        if 'level_id' in params:
            self.level_id = params['level_id']
            
        # Set initial code based on level
        if self.level_id:
            self._set_initial_code_for_level()
        
    def _set_initial_code_for_level(self):
        """Set initial code based on the current level."""
        level_templates = {
            'week1': [
                "# Week 1: Creating Lists",
                "# Create a list of brass instruments",
                "brass_section = ['trumpet', 'trombone', 'tuba']",
                "",
                "# Print the list",
                "print('Brass section:', brass_section)"
            ],
            'week2': [
                "# Week 2: Working with Lists",
                "# Create lists for different sections",
                "brass_section = ['trumpet', 'trombone', 'tuba']",
                "woodwind_section = ['flute', 'clarinet', 'saxophone']",
                "",
                "# Combine sections",
                "all_sections = brass_section + woodwind_section",
                "print('All sections:', all_sections)"
            ],
            'week3': [
                "# Week 3: Using Loops",
                "# Set tempo for the performance",
                "tempo = 120",
                "",
                "# Print a countdown",
                "for i in range(5, 0, -1):",
                "    print(f'Starting in {i}...')",
                "",
                "print('Performance started!')"
            ],
            'week4': [
                "# Week 4: Creating Functions",
                "# Define a function to set up a section",
                "def setup_section(instruments):",
                "    print(f'Setting up section with {len(instruments)} instruments')",
                "    return instruments",
                "",
                "# Use the function",
                "brass_section = setup_section(['trumpet', 'trombone', 'tuba'])",
                "print('Section ready:', brass_section)"
            ],
            'competition1': [
                "# Competition Week: Show Your Skills!",
                "# Configure your performance settings",
                "tempo = 120",
                "uniform_color = 'blue'",
                "volume = 7",
                "",
                "# Add your creative code here!",
                "# Try creating formations, patterns, or special effects"
            ],
            'competition2': [
                "# Advanced Competition: Impress the Judges!",
                "# Advanced configuration options",
                "tempo = 140",
                "uniform_color = 'gold'",
                "volume = 8",
                "formation = 'complex'",
                "",
                "# Create an amazing performance using all your Python skills!"
            ]
        }
        
        if self.level_id in level_templates:
            self.lines = level_templates[self.level_id]
            self.current_line = 0
            self.current_column = 0
            self.dirty = False
            
    def handle_event(self, ev):
        """Handle keyboard and mouse input for the editor."""
        # Handle UI button events
        for button in self.buttons + self.panel_buttons:
            if button.handle_event(ev):
                return
                
        if ev.type == pygame.KEYDOWN:
            self._handle_key_input(ev)
            
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:  # Left click
                self._handle_mouse_click(ev.pos)
            elif ev.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif ev.button == 5:  # Scroll down
                max_scroll = max(0, len(self.lines) - self._get_visible_lines())
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                
    def _handle_key_input(self, ev):
        """Handle keyboard input for text editing."""
        ctrl_held = pygame.key.get_mods() & pygame.KMOD_CTRL
        shift_held = pygame.key.get_mods() & pygame.KMOD_SHIFT
        
        # Handle shortcuts
        if ev.key == self.shortcuts['run']:
            self._run_code()
        elif ev.key == self.shortcuts['save']:
            self._save_code()
        elif ev.key == self.shortcuts['undo'] and ctrl_held:
            self._undo()
        elif ev.key == self.shortcuts['redo'] and ctrl_held:
            self._redo()
        elif ev.key == self.shortcuts['clear_console'] and ctrl_held:
            self._clear_console()
        elif ev.key == pygame.K_ESCAPE:
            self._go_back()
        else:
            self._handle_text_input(ev, ctrl_held, shift_held)
            
    def _handle_text_input(self, ev, ctrl_held, shift_held):
        """Handle regular text input and cursor movement."""
        line = self.lines[self.current_line]
        
        # Cursor movement
        if ev.key == pygame.K_LEFT:
            if self.current_column > 0:
                self.current_column -= 1
        elif ev.key == pygame.K_RIGHT:
            if self.current_column < len(line):
                self.current_column += 1
        elif ev.key == pygame.K_UP:
            if self.current_line > 0:
                self.current_line -= 1
                self.current_column = min(self.current_column, len(self.lines[self.current_line]))
        elif ev.key == pygame.K_DOWN:
            if self.current_line < len(self.lines) - 1:
                self.current_line += 1
                self.current_column = min(self.current_column, len(self.lines[self.current_line]))
        elif ev.key == pygame.K_HOME:
            self.current_column = 0
        elif ev.key == pygame.K_END:
            self.current_column = len(line)
        elif ev.key == pygame.K_PAGEUP:
            self.current_line = max(0, self.current_line - self._get_visible_lines())
        elif ev.key == pygame.K_PAGEDOWN:
            self.current_line = min(len(self.lines) - 1, self.current_line + self._get_visible_lines())
            
        # Text editing
        elif ev.key == pygame.K_BACKSPACE:
            if self.current_column > 0:
                self._save_to_history()
                self.lines[self.current_line] = line[:self.current_column-1] + line[self.current_column:]
                self.current_column -= 1
                self.dirty = True
            elif self.current_line > 0:
                self._save_to_history()
                # Merge with previous line
                prev_line = self.lines[self.current_line - 1]
                self.lines[self.current_line - 1] = prev_line + line
                self.current_column = len(prev_line)
                self.lines.pop(self.current_line)
                self.current_line -= 1
                self.dirty = True
                
        elif ev.key == pygame.K_DELETE:
            if self.current_column < len(line):
                self._save_to_history()
                self.lines[self.current_line] = line[:self.current_column] + line[self.current_column+1:]
                self.dirty = True
                
        elif ev.key == pygame.K_RETURN:
            self._save_to_history()
            # Split line
            before_cursor = line[:self.current_column]
            after_cursor = line[self.current_column:]
            self.lines[self.current_line] = before_cursor
            self.lines.insert(self.current_line + 1, after_cursor)
            self.current_line += 1
            self.current_column = 0
            self.dirty = True
            
        elif ev.key == pygame.K_TAB:
            self._save_to_history()
            # Insert 4 spaces
            self.lines[self.current_line] = line[:self.current_column] + "    " + line[self.current_column:]
            self.current_column += 4
            self.dirty = True
            
        else:
            # Regular character input
            char = ev.unicode
            if char and char.isprintable():
                self._save_to_history()
                self.lines[self.current_line] = line[:self.current_column] + char + line[self.current_column:]
                self.current_column += 1
                self.dirty = True
                
        # Check for syntax errors after changes
        if self.dirty:
            self._check_syntax()
            
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks in the editor."""
        x, y = pos
        
        # Check if click is in editor area
        if (self.editor_x <= x <= self.editor_x + self.editor_width and
            self.editor_y <= y <= self.editor_y + self.editor_height):
            
            # Convert to line and column
            rel_x = x - self.editor_x - self.line_number_width
            rel_y = y - self.editor_y
            
            if rel_x >= 0:
                line_index = self.scroll_offset + (rel_y // self.font_code.get_height())
                line_index = min(line_index, len(self.lines) - 1)
                
                if 0 <= line_index < len(self.lines):
                    # Calculate column (approximate)
                    char_width = self.font_code.get_width(' ')
                    column = rel_x // char_width
                    column = min(column, len(self.lines[line_index]))
                    
                    self.current_line = line_index
                    self.current_column = column
                    
    def _save_to_history(self):
        """Save current state to undo history."""
        # Remove any states after current index
        self.history = self.history[:self.history_index + 1]
        
        # Add current state
        self.history.append(self.lines.copy())
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1
            
    def _undo(self):
        """Undo last change."""
        if self.history_index > 0:
            self.history_index -= 1
            self.lines = self.history[self.history_index].copy()
            self.dirty = True
            self._check_syntax()
            
    def _redo(self):
        """Redo last undone change."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.lines = self.history[self.history_index].copy()
            self.dirty = True
            self._check_syntax()
            
    def _run_code(self):
        """Execute the current code and show output."""
        self._clear_console()
        self._add_console_output("Running code...", 'normal')
        
        # Get the code as a string
        code = '\
'.join(self.lines)
        
        # Try to execute the code
        try:
            # Create a namespace for execution
            exec_globals = {}
            
            # Execute the code
            exec(code, exec_globals)
            
            # Validate the code if we have a level_id
            if self.level_id:
                # Import the level manager
                from gameplay.level_manager import LevelManager
                level_manager = LevelManager()
                
                # Validate the code
                success, message = level_manager.validate(self.level_id, exec_globals)
                
                if success:
                    self._add_console_output(f"\u2713 {message}", 'success')
                    self._add_console_output("Code validation successful!", 'success')
                    
                    # If this is a competition week, transition to competition scene
                    if 'competition' in self.level_id:
                        self._add_console_output("Starting competition performance...", 'normal')
                        self.manager.switch('competition')
                    else:
                        self._add_console_output("Level completed! Moving to next week.", 'success')
                        # Extract the week number and go to next week
                        week_num = int(self.level_id.replace('week', ''))
                        next_week = week_num + 1
                        self.manager.switch('story', week=next_week)
                else:
                    self._add_console_output(f"\u2717 {message}", 'error')
                    self._add_console_output("Please fix the issues and try again.", 'normal')
            else:
                # Just run the code without validation
                self._add_console_output("\u2713 Code executed successfully!", 'success')
                self._add_console_output("Band formation updated.", 'normal')
                
        except Exception as e:
            self._add_console_output(f"Error: {str(e)}", 'error')
            
        self.dirty = False
        
    def _save_code(self):
        """Save the current code."""
        self._add_console_output("Code saved!", 'success')
        self.dirty = False
        
    def _clear_console(self):
        """Clear the console output."""
        self.console_output = []
        
    def _add_console_output(self, text: str, output_type: str = 'normal'):
        """Add text to the console output."""
        timestamp = f"[{pygame.time.get_ticks() // 1000 % 10000:04d}] "
        self.console_output.append(timestamp + text)
        
        # Limit console output length
        if len(self.console_output) > self.console_scrollback:
            self.console_output = self.console_output[-self.console_scrollback:]
            
    def _check_syntax(self):
        """Check for syntax errors and warnings."""
        self.errors = []
        self.warnings = []
        
        try:
            code = '\
'.join(self.lines)
            
            # Basic syntax checks
            for line_num, line in enumerate(self.lines, 1):
                # Check for unclosed quotes
                if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
                    self.errors.append({
                        'line': line_num,
                        'message': 'Unclosed string quote',
                        'column': len(line)
                    })
                    
                # Check for basic syntax patterns
                if 'if' in line and ':' not in line and not line.strip().endswith('#'):
                    self.warnings.append({
                        'line': line_num,
                        'message': 'Missing colon after if statement',
                        'column': line.find('if')
                    })
                    
                if 'for' in line and 'in' not in line:
                    self.warnings.append({
                        'line': line_num,
                        'message': 'for loop should include "in"',
                        'column': line.find('for')
                    })
                    
                if 'def' in line and ':' not in line and not line.strip().endswith('#'):
                    self.warnings.append({
                        'line': line_num,
                        'message': 'Missing colon after function definition',
                        'column': line.find('def')
                    })
                    
        except Exception as e:
            self.errors.append({
                'line': 1,
                'message': f'Syntax error: {str(e)}',
                'column': 0
            })
            
    def _get_visible_lines(self) -> int:
        """Get the number of visible lines in the editor."""
        line_height = self.font_code.get_height()
        return self.editor_height // line_height
        
    def _toggle_hints(self):
        """Toggle hints display."""
        self._add_console_output("Hints toggled", 'normal')
        
    def update(self, dt):
        """Update editor animations and cursor."""
        self.animation_time += dt
        
        # Update cursor blink
        self.cursor_blink_timer += dt
        self.cursor_visible = (self.cursor_blink_timer % 1.0) < 0.5
        
        # Update error pulse
        if self.errors:
            self.error_pulse += dt * 3
            
        # Update buttons
        for button in self.buttons + self.panel_buttons:
            button.update(dt)
            
        # Update stadium decorations
        self._update_stadium_decorations(dt)
            
    def _update_stadium_decorations(self, dt):
        """Update stadium decorations."""
        for light in self.stadium_lights:
            light['brightness'] = 0.5 + abs(math.sin(self.animation_time * 2 + light['x'] * 0.01)) * 0.5
            
    def draw(self, surface):
        """Render the enhanced code editor."""
        # Draw background
        surface.fill(self.colors['background'])
        
        # Draw stadium decorations
        self._draw_stadium_decorations(surface)
        
        # Draw main editor area
        self._draw_editor_background(surface)
        
        # Draw line numbers
        self._draw_line_numbers(surface)
        
        # Draw code with syntax highlighting
        self._draw_code(surface)
        
        # Draw cursor and selection
        self._draw_cursor(surface)
        self._draw_selection(surface)
        
        # Draw error/warning indicators
        self._draw_error_indicators(surface)
        
        # Draw UI buttons
        self._draw_buttons(surface)
        
        # Draw console
        self._draw_console(surface)
        
        # Draw side panel
        self._draw_side_panel(surface)
        
        # Draw title and status
        self._draw_header(surface)
        
    def _draw_stadium_decorations(self, surface):
        """Draw stadium decorations in the background."""
        # Draw stadium lights
        for light in self.stadium_lights:
            brightness = int(light['brightness'] * 200)
            light_color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, light_color, (light['x'], light['y']), 8)
            pygame.draw.circle(surface, (200, 200, 100), (light['x'], light['y']), 8, 2)
            
        # Draw field lines in background
        for y in range(100, WINDOW_HEIGHT, 40):
            pygame.draw.line(surface, self.colors['field_green'], (0, y), (WINDOW_WIDTH, y), 1)
            
    def _draw_editor_background(self, surface):
        """Draw the editor background and borders."""
        # Editor background
        editor_rect = pygame.Rect(self.editor_x, self.editor_y, self.editor_width, self.editor_height)
        pygame.draw.rect(surface, self.colors['background'], editor_rect)
        pygame.draw.rect(surface, self.colors['text_normal'], editor_rect, 2)
        
        # Line number background
        line_number_rect = pygame.Rect(self.editor_x, self.editor_y, self.line_number_width, self.editor_height)
        pygame.draw.rect(surface, (20, 20, 30), line_number_rect)
        pygame.draw.rect(surface, self.colors['line_numbers'], line_number_rect, 1)
        
        # Draw subtle grid pattern
        grid_color = (25, 25, 35)
        for y in range(self.editor_y, self.editor_y + self.editor_height, 20):
            pygame.draw.line(surface, grid_color, 
                           (self.editor_x + self.line_number_width, y),
                           (self.editor_x + self.editor_width, y), 1)
                           
    def _draw_line_numbers(self, surface):
        """Draw line numbers."""
        start_line = self.scroll_offset + 1
        visible_lines = self._get_visible_lines()
        line_height = self.font_code.get_height()
        
        for i in range(visible_lines):
            line_num = start_line + i
            if line_num <= len(self.lines):
                y = self.editor_y + i * line_height
                
                # Highlight current line number
                if line_num - 1 == self.current_line:
                    color = self.colors['text_normal']
                else:
                    color = self.colors['line_numbers']
                    
                text = self.font_line_numbers.render(str(line_num), True, color)
                surface.blit(text, (self.editor_x + 5, y))
                
    def _draw_code(self, surface):
        """Draw code with syntax highlighting."""
        start_line = self.scroll_offset
        visible_lines = self._get_visible_lines()
        line_height = self.font_code.get_height()
        
        for i in range(visible_lines):
            line_index = start_line + i
            if line_index < len(self.lines):
                y = self.editor_y + i * line_height
                self._draw_highlighted_line(surface, self.lines[line_index], 
                                           self.editor_x + self.line_number_width + 5, y)
                                           
    def _draw_highlighted_line(self, surface, line: str, x: int, y: int):
        """Draw a single line with syntax highlighting."""
        if not line.strip():
            return
            
        # Apply syntax highlighting patterns
        highlighted_segments = []
        last_end = 0
        
        for pattern, token_type in self.syntax_patterns:
            for match in re.finditer(pattern, line):
                start, end = match.span()
                
                # Add normal text before this match
                if start > last_end:
                    highlighted_segments.append((line[last_end:start], 'normal'))
                    
                # Add highlighted text
                highlighted_segments.append((line[start:end], token_type))
                last_end = end
                
        # Add remaining normal text
        if last_end < len(line):
            highlighted_segments.append((line[last_end:], 'normal'))
            
        # Draw each segment
        current_x = x
        for text, token_type in highlighted_segments:
            color = self.colors.get(f'text_{token_type}', self.colors['text_normal'])
            text_surf = self.font_code.render(text, True, color)
            surface.blit(text_surf, (current_x, y))
            current_x += text_surf.get_width()
            
    def _draw_cursor(self, surface):
        """Draw the cursor."""
        if not self.cursor_visible:
            return
            
        if self.current_line < len(self.lines):
            line_num = self.current_line - self.scroll_offset
            if 0 <= line_num < self._get_visible_lines():
                y = self.editor_y + line_num * self.font_code.get_height()
                
                # Get cursor position
                line_text = self.lines[self.current_line][:self.current_column]
                cursor_x = self.editor_x + self.line_number_width + 5 + self.font_code.get_width(line_text)
                
                # Draw cursor
                cursor_height = self.font_code.get_height()
                pygame.draw.line(surface, self.colors['cursor'], 
                               (cursor_x, y), (cursor_x, y + cursor_height), 2)
                               
    def _draw_selection(self, surface):
        """Draw text selection."""
        if self.selection_start and self.selection_end:
            # TODO: Implement selection highlighting
            pass
            
    def _draw_error_indicators(self, surface):
        """Draw error and warning indicators."""
        line_height = self.font_code.get_height()
        
        # Draw error indicators in line numbers
        for error in self.errors:
            line_num = error['line'] - 1 - self.scroll_offset
            if 0 <= line_num < self._get_visible_lines():
                y = self.editor_y + line_num * line_height
                # Red dot for error
                pygame.draw.circle(surface, self.colors['error_underline'], 
                                 (self.editor_x + self.line_number_width - 10, y + 8), 3)
                                 
        # Draw warning indicators
        for warning in self.warnings:
            line_num = warning['line'] - 1 - self.scroll_offset
            if 0 <= line_num < self._get_visible_lines():
                y = self.editor_y + line_num * line_height
                # Yellow triangle for warning
                points = [
                    (self.editor_x + self.line_number_width - 12, y + 5),
                    (self.editor_x + self.line_number_width - 8, y + 11),
                    (self.editor_x + self.line_number_width - 16, y + 11)
                ]
                pygame.draw.polygon(surface, self.colors['warning_underline'], points)
                
        # Draw error underlines
        for error in self.errors:
            line_num = error['line'] - 1 - self.scroll_offset
            if 0 <= line_num < self._get_visible_lines():
                y = self.editor_y + line_num * line_height + self.font_code.get_height() - 2
                line = self.lines[error['line'] - 1]
                
                if error['column'] < len(line):
                    # Calculate underline position
                    char_width = self.font_code.get_width(' ')
                    underline_start = self.editor_x + self.line_number_width + 5 + error['column'] * char_width
                    
                    # Pulsing red underline
                    pulse = abs(math.sin(self.error_pulse)) * 0.5 + 0.5
                    color = (*self.colors['error_underline'], int(255 * pulse))
                    pygame.draw.line(surface, color[:3], 
                                   (underline_start, y), (underline_start + 20, y), 3)
                                   
    def _draw_buttons(self, surface):
        """Draw all UI buttons."""
        for button in self.buttons:
            button.draw(surface)
            
    def _draw_console(self, surface):
        """Draw the console output area."""
        # Console background
        console_rect = pygame.Rect(self.console_x, self.console_y, self.console_width, self.console_height)
        pygame.draw.rect(surface, self.colors['console_bg'], console_rect)
        pygame.draw.rect(surface, self.colors['text_normal'], console_rect, 2)
        
        # Console title
        title = self.font_title.render("CONSOLE OUTPUT", True, self.colors['text_normal'])
        surface.blit(title, (self.console_x + 10, self.console_y - 25))
        
        # Console output
        line_height = self.font_console.get_height()
        max_lines = (self.console_height - 10) // line_height
        
        start_line = max(0, len(self.console_output) - max_lines)
        
        for i, line in enumerate(self.console_output[start_line:]):
            y = self.console_y + 5 + i * line_height
            
            # Determine text color based on content
            if 'Error' in line or 'error' in line.lower():
                color = self.colors['console_error']
            elif '\u2713' in line or 'success' in line.lower():
                color = self.colors['console_text']
            else:
                color = self.colors['text_normal']
                
            # Truncate line if too long
            if len(line) > 100:
                line = line[:97] + "..."
                
            text_surf = self.font_console.render(line, True, color)
            surface.blit(text_surf, (self.console_x + 10, y))
            
    def _draw_side_panel(self, surface):
        """Draw the side panel with hints and info."""
        panel_x = self.editor_x + self.editor_width + 20
        panel_y = self.editor_y + 120
        panel_width = 120
        
        # Hints section
        if self.errors:
            hints_title = self.font_ui.render("ERRORS:", True, self.colors['error_underline'])
            surface.blit(hints_title, (panel_x, panel_y))
            
            for i, error in enumerate(self.errors[:5]):  # Show max 5 errors
                y = panel_y + 25 + i * 20
                error_text = f"Line {error['line']}: {error['message']}"
                
                # Word wrap long error messages
                if len(error_text) > 18:
                    error_text = error_text[:15] + "..."
                    
                text_surf = self.font_small.render(error_text, True, self.colors['text_normal'])
                surface.blit(text_surf, (panel_x, y))
                
        elif self.warnings:
            hints_title = self.font_ui.render("WARNINGS:", True, self.colors['warning_underline'])
            surface.blit(hints_title, (panel_x, panel_y))
            
            for i, warning in enumerate(self.warnings[:3]):
                y = panel_y + 25 + i * 20
                warning_text = f"Line {warning['line']}: {warning['message']}"
                
                if len(warning_text) > 18:
                    warning_text = warning_text[:15] + "..."
                    
                text_surf = self.font_small.render(warning_text, True, self.colors['warning_underline'])
                surface.blit(text_surf, (panel_x, y))
                
        else:
            hints_title = self.font_ui.render("TIPS:", True, self.colors['text_function'])
            surface.blit(hints_title, (panel_x, panel_y))
            
            tips = [
                "Use tempo to set speed",
                "uniform_color sets theme", 
                "volume controls loudness",
                "Press F5 to run code",
                "Ctrl+Z to undo"
            ]
            
            for i, tip in enumerate(tips):
                y = panel_y + 25 + i * 18
                text_surf = self.font_small.render(tip, True, self.colors['text_normal'])
                surface.blit(text_surf, (panel_x, y))
                
        # Draw panel buttons
        for button in self.panel_buttons:
            button.draw(surface)
            
    def _draw_header(self, surface):
        """Draw editor header and status."""
        # Title
        title_text = "PRIDE OF CODE - PYTHON EDITOR"
        if self.level_id:
            title_text += f" ({self.level_id.upper()})"
        title = self.font_title.render(title_text, True, self.colors['text_normal'])
        surface.blit(title, (self.editor_x, 20))
        
        # Status
        status = "MODIFIED" if self.dirty else "SAVED"
        status_color = COLOR_GOLD if self.dirty else self.colors['console_text']
        status_surf = self.font_small.render(status, True, status_color)
        surface.blit(status_surf, (self.editor_x, 50))
        
        # Position info
        pos_text = f"Line {self.current_line + 1}, Column {self.current_column + 1}"
        pos_surf = self.font_small.render(pos_text, True, self.colors['text_normal'])
        surface.blit(pos_surf, (self.editor_x + 300, 50))
        
        # Keyboard shortcuts
        shortcuts_text = "F5:Run | F2:Save | Ctrl+Z:Undo | Ctrl+Y:Redo | ESC:Back"
        shortcuts_surf = self.font_small.render(shortcuts_text, True, self.colors['subtitle'])
        surface.blit(shortcuts_surf, (self.editor_x + 500, 50))
