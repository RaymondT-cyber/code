"""
Enhanced Story & Dialogue Scene for Pride of Code.
Features character portraits, semi-transparent overlays, pixel text ≥18px,
keyboard/mouse navigation, skippable dialogue with subtitles, and alternate dialogue paths.
"""

import pygame
import math
from typing import List, Dict, Optional, Tuple
from core.state_manager import State
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLUE, COLOR_GOLD, 
                   COLOR_TEXT, COLOR_BG)
from ui.enhanced_retro_button import EnhancedRetroButton


class EnhancedStoryScene(State):
    """Enhanced story scene with comprehensive dialogue system and character portraits."""
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        
        # Color scheme
        self.colors = {
            'background_overlay': (20, 20, 30, 220),  # Semi-transparent dark
            'dialogue_box': (30, 30, 40, 240),       # Dialogue background
            'border': COLOR_BLUE,                     # Accent border
            'text': COLOR_TEXT,                       # Main text
            'name_text': COLOR_GOLD,                  # Character names
            'subtitle': (180, 180, 180),              # Subtitles
            'choices': COLOR_BLUE,                    # Choice buttons
            'progress': (150, 150, 150)               # Progress indicator
        }
        
        # Fonts - ensure ≥18px for readability
        try:
            self.font_dialogue = pygame.font.Font(None, 24)      # 24px for main dialogue
            self.font_name = pygame.font.Font(None, 28, bold=True)  # 28px for character names
            self.font_subtitle = pygame.font.Font(None, 18)     # 18px for subtitles
            self.font_choice = pygame.font.Font(None, 20)       # 20px for choices
            self.font_small = pygame.font.Font(None, 16)        # 16px for UI elements
        except:
            self.font_dialogue = pygame.font.SysFont('arial', 24)
            self.font_name = pygame.font.SysFont('arial', 28, bold=True)
            self.font_subtitle = pygame.font.SysFont('arial', 18)
            self.font_choice = pygame.font.SysFont('arial', 20)
            self.font_small = pygame.font.SysFont('arial', 16)
        
        # Character portraits and data
        self.characters = self._create_character_data()
        
        # Dialogue system
        self.current_dialogue = None
        self.dialogue_sequence = []
        self.dialogue_index = 0
        self.dialogue_complete = False
        self.text_animation_progress = 0.0
        self.text_speed = 0.02  # Characters per frame
        self.auto_advance = False
        self.auto_advance_timer = 0.0
        
        # Story context
        self.current_week = 1
        self.story_context = {}
        self.competition_outcome = None  # 'win' or 'loss'
        
        # UI state
        self.show_subtitles = True
        self.skippable = True
        self.choices_available = []
        self.selected_choice = 0
        
        # Animation
        self.portrait_animation = 0.0
        self.fade_alpha = 0.0
        self.scene_transition = False
        
        # Background
        self.background_surface = None
        
    def _create_character_data(self) -> Dict:
        """Create character data with portraits and dialogue variants."""
        return {
            'leah': {
                'name': 'Leah',
                'role': 'Drum Major',
                'portrait_colors': {
                    'skin': (220, 200, 180),
                    'hair': (139, 69, 19),
                    'uniform': COLOR_BLUE,
                    'accent': COLOR_GOLD
                },
                'personality': 'disciplined_caring',
                'dialogue_variants': {
                    'normal': [
                        "Alright team, let's focus on today's lesson.",
                        "I expect everyone to give their best effort.",
                        "Precision is everything in marching band.",
                        "Let me show you how this is supposed to work."
                    ],
                    'encouraging': [
                        "Great work everyone! You're really improving.",
                        "I knew you could do it! Keep up the excellent work.",
                        "That's exactly what I was looking for. Well done!",
                        "Perfect! You're all becoming true musicians."
                    ],
                    'stressed': [
                        "We need to work harder if we want to win.",
                        "Focus, team! We can't afford mistakes.",
                        "This isn't good enough. Let's run it again.",
                        "I need your full attention on this."
                    ]
                }
            },
            'elijah': {
                'name': 'Elijah',
                'role': 'Percussionist',
                'portrait_colors': {
                    'skin': (180, 140, 100),
                    'hair': (40, 40, 40),
                    'uniform': COLOR_BLUE,
                    'accent': (220, 20, 60)  # Red for percussion
                },
                'personality': 'energetic_joking',
                'dialogue_variants': {
                    'normal': [
                        "Can we code our way to the trophy? Let's find out!",
                        "Alright team, time to make some noise!",
                        "I've got a rhythm for this... and it's not just in the drums!",
                        "Let's beat this challenge into submission!"
                    ],
                    'joking': [
                        "Next time, more cowbell! That always fixes everything.",
                        "Can we add a drum solo to this code? I think it needs more percussion!",
                        "I call myself 'Chief Dance Officer' now. What do you think, Captain?",
                        "My drumsticks are ready for action! Let's code something epic!"
                    ],
                    'serious': [
                        "Okay, this is serious. We need to nail this formation.",
                        "Sometimes jokes have to wait. This is important.",
                        "Let me handle the rhythm section. I'll make sure we're perfect.",
                        "I'll do whatever it takes to help us win."
                    ]
                }
            },
            'anna': {
                'name': 'Anna',
                'role': 'Flute Player',
                'portrait_colors': {
                    'skin': (240, 220, 200),
                    'hair': (200, 100, 50),
                    'uniform': COLOR_BLUE,
                    'accent': (144, 238, 144)  # Light green for woodwinds
                },
                'personality': 'shy_talented',
                'dialogue_variants': {
                    'normal': [
                        "Um... I think I understand this part.",
                        "If I may suggest something...",
                        "This reminds me of a flute piece I know.",
                        "I'll try my best to help."
                    ],
                    'confident': [
                        "I know exactly what we need to do here.",
                        "Let me show you how this melody should work.",
                        "I've been practicing this technique. Let me help.",
                        "I have an idea that might improve our performance."
                    ],
                    'supportive': [
                        "We can do this together, everyone.",
                        "Don't worry, I'll help you with that part.",
                        "Your code sounds beautiful. Keep going!",
                        "We make a great team when we work together."
                    ]
                }
            },
            'alex': {
                'name': 'Alex',
                'role': 'Saxophonist/Tech Expert',
                'portrait_colors': {
                    'skin': (200, 180, 160),
                    'hair': (255, 184, 28),  # Golden blonde
                    'uniform': COLOR_BLUE,
                    'accent': (255, 215, 0)  # Gold for brass
                },
                'personality': 'tech_savvy_enthusiastic',
                'dialogue_variants': {
                    'normal': [
                        "I can code this! Let me show you how.",
                        "The band.api can handle this. Let me write the function.",
                        "I've been working on a solution for exactly this problem.",
                        "Let me sync the music and lights with this code."
                    ],
                    'technical': [
                        "I'll create a class to manage this section efficiently.",
                        "We need to optimize this algorithm for better performance.",
                        "Let me implement a better data structure for this.",
                        "I can write a module that will handle all of this automatically."
                    ],
                    'excited': [
                        "This is amazing! I never thought we could do this with code!",
                        "I have so many ideas for making our show even better!",
                        "Wait until you see what I've programmed for the finale!",
                        "The possibilities are endless when you combine music and code!"
                    ]
                }
            },
            'coach_hodge': {
                'name': 'Coach Hodge',
                'role': 'Assistant Coach',
                'portrait_colors': {
                    'skin': (180, 160, 140),
                    'hair': (100, 100, 100),
                    'uniform': (60, 60, 60),
                    'accent': COLOR_GOLD
                },
                'personality': 'wise_encouraging',
                'dialogue_variants': {
                    'normal': [
                        "I'm proud of the progress you're all making.",
                        "Remember the fundamentals, and you'll succeed.",
                        "Great work today, team. Keep it up.",
                        "I have confidence in every one of you."
                    ],
                    'advice': [
                        "In both music and code, attention to detail matters.",
                        "Practice makes perfect, whether you're playing an instrument or debugging code.",
                        "Teamwork is everything. Support each other.",
                        "The best performances come from the heart, and the best code comes from careful thought."
                    ],
                    'proud': [
                        "You've all exceeded my expectations. Bravo!",
                        "This is exactly the kind of performance I knew you were capable of.",
                        "I couldn't be prouder to be your coach.",
                        "You've become not just better musicians, but better problem solvers too."
                    ]
                }
            }
        }
        
    def start_story_sequence(self, week: int, context: Dict = None):
        """Start a story sequence for a specific week."""
        self.current_week = week
        self.story_context = context or {}
        self.dialogue_complete = False
        self.text_animation_progress = 0.0
        
        # Get dialogue sequence for this week
        self.dialogue_sequence = self._get_week_dialogue(week)
        self.dialogue_index = 0
        
        # Load appropriate background
        self._load_background(week)
        
        # Start fade-in
        self.fade_alpha = 255
        self.scene_transition = True
        
    def _get_week_dialogue(self, week: int) -> List[Dict]:
        """Get dialogue sequence for a specific week."""
        if week == 1:
            return [
                {
                    'character': 'coach_hodge',
                    'text': "Welcome to Pride of Code! I'm Coach Hodge, and this is going to be an amazing season.",
                    'emotion': 'normal',
                    'portrait_pose': 'welcoming'
                },
                {
                    'character': 'leah',
                    'text': "This is the band room where all the magic happens. It's buzzing with excitement today!",
                    'emotion': 'normal',
                    'portrait_pose': 'proud'
                },
                {
                    'character': 'elijah',
                    'text': "Hey Captain! Can we code our way to the trophy? I've got a good feeling about this!",
                    'emotion': 'joking',
                    'portrait_pose': 'excited'
                },
                {
                    'character': 'anna',
                    'text': "Um... hi. I'll be helping with the woodwind sections. Your flute playing is beautiful.",
                    'emotion': 'normal',
                    'portrait_pose': 'shy'
                },
                {
                    'character': 'alex',
                    'text': "I noticed you have a laptop! I've been working on a band.api interface to sync music and lights!",
                    'emotion': 'excited',
                    'portrait_pose': 'enthusiastic'
                },
                {
                    'character': 'leah',
                    'text': "Today, we'll learn about variables - like tempo, uniform colors, and volume settings.",
                    'emotion': 'normal',
                    'portrait_pose': 'teaching'
                },
                {
                    'character': 'alex',
                    'text': "Variables are like labeled containers. For example: tempo = 120 sets our marching speed!",
                    'emotion': 'technical',
                    'portrait_pose': 'explaining'
                },
                {
                    'character': 'coach_hodge',
                    'text': "We've signed up for a local competition in two weeks. Let's make this count!",
                    'emotion': 'proud',
                    'portrait_pose': 'announcing'
                }
            ]
        elif week == 2:
            base_dialogue = [
                {
                    'character': 'leah',
                    'text': "It's competition day! Remember the variable settings we practiced.",
                    'emotion': 'normal',
                    'portrait_pose': 'focused'
                },
                {
                    'character': 'elijah',
                    'text': "I've got my drumsticks ready! Let's show them what Pride of Code can do!",
                    'emotion': 'excited',
                    'portrait_pose': 'ready'
                },
                {
                    'character': 'alex',
                    'text': "I've set up conditional code: if weather == 'rain', we'll use indoor formation!",
                    'emotion': 'technical',
                    'portrait_pose': 'prepared'
                }
            ]
            
            # Different dialogue based on competition outcome
            if self.competition_outcome == 'win':
                base_dialogue.extend([
                    {
                        'character': 'leah',
                        'text': "We won! Thank you for helping us create such a perfect routine!",
                        'emotion': 'encouraging',
                        'portrait_pose': 'celebrating'
                    },
                    {
                        'character': 'elijah',
                        'text': "Victory march time! I call myself 'Chief Dance Officer' now!",
                        'emotion': 'joking',
                        'portrait_pose': 'victory'
                    }
                ])
            else:
                base_dialogue.extend([
                    {
                        'character': 'leah',
                        'text': "We didn't win, but we gave it our all. Next time, we'll be even better.",
                        'emotion': 'stressed',
                        'portrait_pose': 'determined'
                    },
                    {
                        'character': 'elijah',
                        'text': "Next time, more cowbell! And maybe fewer rainy day performances!",
                        'emotion': 'joking',
                        'portrait_pose': 'optimistic'
                    }
                ])
                
            return base_dialogue
            
        # Default dialogue for other weeks
        return [
            {
                'character': 'coach_hodge',
                'text': "Let's continue working on our Python skills and marching routines!",
                'emotion': 'normal',
                'portrait_pose': 'encouraging'
            }
        ]
        
    def _load_background(self, week: int):
        """Load appropriate background for the story scene."""
        # Create different backgrounds based on location
        if week == 1:
            # Band room background
            self.background_surface = self._create_band_room_background()
        elif week % 2 == 0:
            # Competition stadium background
            self.background_surface = self._create_stadium_background()
        else:
            # Practice field background
            self.background_surface = self._create_practice_field_background()
            
    def _create_band_room_background(self) -> pygame.Surface:
        """Create band room background."""
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Band room colors
        floor_color = (139, 90, 43)  # Wood floor
        wall_color = (100, 80, 60)    # Wood walls
        
        # Fill walls
        surface.fill(wall_color)
        
        # Draw floorboards
        for y in range(WINDOW_HEIGHT // 2, WINDOW_HEIGHT, 20):
            pygame.draw.line(surface, floor_color, (0, y), (WINDOW_WIDTH, y), 3)
            
        # Draw music stands
        stand_color = (60, 60, 60)
        for x in range(100, WINDOW_WIDTH - 100, 200):
            # Stand pole
            pygame.draw.rect(surface, stand_color, (x, WINDOW_HEIGHT - 200, 4, 120))
            # Stand top
            pygame.draw.rect(surface, stand_color, (x - 30, WINDOW_HEIGHT - 210, 60, 15))
            
        # Draw instruments on walls
        self._draw_wall_instruments(surface)
        
        return surface
        
    def _create_stadium_background(self) -> pygame.Surface:
        """Create competition stadium background."""
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Sky gradient
        for y in range(WINDOW_HEIGHT // 2):
            color = (135 - y // 4, 206 - y // 4, 235 - y // 4)
            pygame.draw.line(surface, color, (0, y), (WINDOW_WIDTH, y))
            
        # Field
        field_color = (34, 139, 34)
        pygame.draw.rect(surface, field_color, (0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
        
        # Field lines
        for x in range(0, WINDOW_WIDTH, 100):
            pygame.draw.line(surface, (255, 255, 255), (x, WINDOW_HEIGHT // 2), (x, WINDOW_HEIGHT), 3)
            
        # Stadium stands
        stand_color = (80, 80, 80)
        pygame.draw.rect(surface, stand_color, (0, 0, WINDOW_WIDTH, 50))
        pygame.draw.rect(surface, stand_color, (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50))
        
        return surface
        
    def _create_practice_field_background(self) -> pygame.Surface:
        """Create practice field background."""
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Sky
        for y in range(WINDOW_HEIGHT // 2):
            color = (135 - y // 6, 206 - y // 6, 250 - y // 6)
            pygame.draw.line(surface, color, (0, y), (WINDOW_WIDTH, y))
            
        # Practice field
        field_color = (40, 120, 40)
        surface.fill(field_color, (0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
        
        # Practice cones
        cone_color = (255, 140, 0)
        for x in range(150, WINDOW_WIDTH - 150, 200):
            for y in range(WINDOW_HEIGHT // 2 + 100, WINDOW_HEIGHT - 100, 150):
                pygame.draw.polygon(surface, cone_color, [
                    (x - 10, y), (x + 10, y), (x, y - 20)
                ])
                
        return surface
        
    def _draw_wall_instruments(self, surface: pygame.Surface):
        """Draw instrument silhouettes on walls."""
        instrument_color = (60, 40, 20)
        
        # Trumpets
        for x in range(200, WINDOW_WIDTH - 200, 300):
            pygame.draw.rect(surface, instrument_color, (x, 100, 8, 40))
            pygame.draw.rect(surface, instrument_color, (x + 8, 90, 20, 4))
            pygame.draw.circle(surface, instrument_color, (x + 32, 92), 8)
            
        # Drum sets
        for x in range(350, WINDOW_WIDTH - 350, 400):
            pygame.draw.rect(surface, instrument_color, (x, 120, 6, 30))
            pygame.draw.circle(surface, instrument_color, (x + 3, 140), 10)
            pygame.draw.circle(surface, instrument_color, (x + 3, 155), 8)
            
    def handle_event(self, ev):
        """Handle input events for dialogue system."""
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE or ev.key == pygame.K_RETURN:
                self._advance_dialogue()
            elif ev.key == pygame.K_ESCAPE:
                if self.skippable:
                    self._skip_dialogue()
            elif ev.key == pygame.K_s:
                self.show_subtitles = not self.show_subtitles
                
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:  # Left click
                self._advance_dialogue()
                
        # Handle choice selection
        if self.choices_available:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    self.selected_choice = (self.selected_choice - 1) % len(self.choices_available)
                elif ev.key == pygame.K_DOWN:
                    self.selected_choice = (self.selected_choice + 1) % len(self.choices_available)
                elif ev.key == pygame.K_RETURN:
                    self._make_choice()
                    
    def _advance_dialogue(self):
        """Advance to the next dialogue or choice."""
        if self.text_animation_progress < 1.0:
            # Skip text animation
            self.text_animation_progress = 1.0
        else:
            # Move to next dialogue
            self.dialogue_index += 1
            
            if self.dialogue_index >= len(self.dialogue_sequence):
                self.dialogue_complete = True
                self._end_story_sequence()
            else:
                self.text_animation_progress = 0.0
                
    def _skip_dialogue(self):
        """Skip the entire dialogue sequence."""
        self.dialogue_complete = True
        self._end_story_sequence()
        
    def _make_choice(self):
        """Process the selected dialogue choice."""
        if self.choices_available and self.selected_choice < len(self.choices_available):
            choice = self.choices_available[self.selected_choice]
            # Process choice outcome
            self.choices_available = []
            self._advance_dialogue()
            
    def _end_story_sequence(self):
        """End the story sequence and return to appropriate scene."""
        # Fade out
        self.fade_alpha = 0
        self.scene_transition = True
        
        # Return to appropriate scene based on context
        if 'competition' in self.story_context:
            self.manager.switch('results')
        else:
            self.manager.switch('enhanced_editor', level_id=f"week{self.current_week}")
            
    def update(self, dt):
        """Update animations and dialogue system."""
        # Update portrait animations
        self.portrait_animation += dt * 2
        
        # Update text animation
        if self.text_animation_progress < 1.0:
            self.text_animation_progress = min(1.0, self.text_animation_progress + self.text_speed)
            
        # Update auto-advance timer
        if self.auto_advance:
            self.auto_advance_timer -= dt
            if self.auto_advance_timer <= 0:
                self._advance_dialogue()
                self.auto_advance_timer = 3.0  # Reset timer
                
        # Update fade transition
        if self.scene_transition:
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + 300 * dt)
                
    def draw(self, surface):
        """Render the enhanced story scene."""
        # Draw background
        if self.background_surface:
            surface.blit(self.background_surface, (0, 0))
        else:
            surface.fill(COLOR_BG)
            
        # Apply fade overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            fade_surf.fill((0, 0, 0, self.fade_alpha))
            surface.blit(fade_surf, (0, 0))
            
        # Draw dialogue system
        if not self.dialogue_complete and self.dialogue_sequence:
            self._draw_dialogue_system(surface)
            
    def _draw_dialogue_system(self, surface):
        """Draw the complete dialogue system."""
        if self.dialogue_index >= len(self.dialogue_sequence):
            return
            
        current = self.dialogue_sequence[self.dialogue_index]
        character_data = self.characters.get(current['character'], {})
        
        # Draw character portrait
        self._draw_character_portrait(surface, current['character'], current.get('emotion', 'normal'))
        
        # Draw dialogue box
        self._draw_dialogue_box(surface, current, character_data)
        
        # Draw subtitles if enabled
        if self.show_subtitles:
            self._draw_subtitles(surface, current)
            
        # Draw choices if available
        if self.choices_available:
            self._draw_choices(surface)
            
        # Draw progress indicator
        self._draw_progress(surface)
        
    def _draw_character_portrait(self, surface, character: str, emotion: str):
        """Draw character portrait with animations."""
        character_data = self.characters.get(character, {})
        colors = character_data.get('portrait_colors', {})
        
        # Portrait position
        portrait_x = 100
        portrait_y = WINDOW_HEIGHT // 2 - 100
        portrait_size = 150
        
        # Draw portrait background circle
        pygame.draw.circle(surface, (40, 40, 50), (portrait_x + portrait_size // 2, portrait_y + portrait_size // 2), 
                         portrait_size // 2 + 10)
        pygame.draw.circle(surface, COLOR_BLUE, (portrait_x + portrait_size // 2, portrait_y + portrait_size // 2), 
                         portrait_size // 2 + 10, 3)
        
        # Draw character (simplified pixel art style)
        self._draw_character_sprite(surface, portrait_x, portrait_y, portrait_size, colors, emotion)
        
        # Draw character name
        name = character_data.get('name', character)
        role = character_data.get('role', '')
        
        name_surf = self.font_name.render(name, True, self.colors['name_text'])
        surface.blit(name_surf, (portrait_x - 20, portrait_y + portrait_size + 20))
        
        role_surf = self.font_small.render(role, True, self.colors['subtitle'])
        surface.blit(role_surf, (portrait_x - 20, portrait_y + portrait_size + 50))
        
    def _draw_character_sprite(self, surface, x, y, size, colors, emotion):
        """Draw simplified character sprite."""
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Head
        head_size = size // 4
        head_color = colors.get('skin', (220, 200, 180))
        pygame.draw.circle(surface, head_color, (center_x, center_y - size // 4), head_size)
        
        # Hair (based on character)
        hair_color = colors.get('hair', (100, 100, 100))
        if emotion == 'excited':
            # Hair bouncing
            bounce = int(math.sin(self.portrait_animation * 4) * 3)
            pygame.draw.ellipse(surface, hair_color, 
                              (center_x - head_size, center_y - size // 4 - bounce - head_size // 2, 
                               head_size * 2, head_size))
        else:
            pygame.draw.ellipse(surface, hair_color, 
                              (center_x - head_size, center_y - size // 4 - head_size // 2, 
                               head_size * 2, head_size))
        
        # Body
        body_height = size // 2
        body_color = colors.get('uniform', COLOR_BLUE)
        pygame.draw.rect(surface, body_color, 
                        (center_x - size // 3, center_y - size // 6, size // 3 * 2, body_height))
        
        # Accent/insignia
        accent_color = colors.get('accent', COLOR_GOLD)
        pygame.draw.rect(surface, accent_color, 
                        (center_x - size // 4, center_y - size // 8, size // 2, 10))
        
        # Eyes (animated)
        eye_color = (60, 60, 80)
        if emotion == 'excited':
            # Sparkling eyes
            pygame.draw.circle(surface, eye_color, (center_x - 8, center_y - size // 4), 3)
            pygame.draw.circle(surface, eye_color, (center_x + 8, center_y - size // 4), 3)
            pygame.draw.circle(surface, (255, 255, 255), (center_x - 6, center_y - size // 4 - 2), 1)
            pygame.draw.circle(surface, (255, 255, 255), (center_x + 10, center_y - size // 4 - 2), 1)
        else:
            pygame.draw.circle(surface, eye_color, (center_x - 8, center_y - size // 4), 2)
            pygame.draw.circle(surface, eye_color, (center_x + 8, center_y - size // 4), 2)
            
        # Mouth (based on emotion)
        if emotion in ['joking', 'excited']:
            # Smiling
            pygame.draw.arc(surface, (200, 100, 100), 
                           (center_x - 10, center_y - size // 4 + 5, 20, 15), 
                           0, math.pi, 2)
        elif emotion == 'stressed':
            # Frowning
            pygame.draw.arc(surface, (200, 100, 100), 
                           (center_x - 10, center_y - size // 4 + 10, 20, 10), 
                           math.pi, 0, 2)
        else:
            # Neutral
            pygame.draw.line(surface, (150, 100, 100), 
                           (center_x - 5, center_y - size // 4 + 10), 
                           (center_x + 5, center_y - size // 4 + 10), 2)
                           
    def _draw_dialogue_box(self, surface, dialogue_data, character_data):
        """Draw the dialogue box with animated text."""
        # Dialogue box dimensions
        box_x = 300
        box_y = WINDOW_HEIGHT // 2 - 80
        box_width = WINDOW_WIDTH - 350
        box_height = 200
        
        # Create semi-transparent surface
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surf.fill(self.colors['dialogue_box'])
        surface.blit(box_surf, (box_x, box_y))
        
        # Draw border
        pygame.draw.rect(surface, self.colors['border'], (box_x, box_y, box_width, box_height), 3)
        
        # Get text with animation
        full_text = dialogue_data['text']
        if self.text_animation_progress < 1.0:
            # Animate text appearance
            text_length = int(len(full_text) * self.text_animation_progress)
            display_text = full_text[:text_length]
        else:
            display_text = full_text
            
        # Word wrap text
        words = display_text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surf = self.font_dialogue.render(test_line, True, self.colors['text'])
            if text_surf.get_width() > box_width - 40:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)
                
        if current_line:
            lines.append(' '.join(current_line))
            
        # Draw text lines
        for i, line in enumerate(lines):
            if i < 6:  # Maximum 6 lines
                text_surf = self.font_dialogue.render(line, True, self.colors['text'])
                surface.blit(text_surf, (box_x + 20, box_y + 20 + i * 30))
                
        # Draw continue prompt if text is fully displayed
        if self.text_animation_progress >= 1.0:
            prompt_alpha = int(abs(math.sin(self.portrait_animation * 2)) * 255)
            prompt_surf = self.font_small.render("Press SPACE or click to continue...", True, 
                                                (*self.colors['subtitle'], prompt_alpha))
            surface.blit(prompt_surf, (box_x + 20, box_y + box_height - 30))
            
    def _draw_subtitles(self, surface, dialogue_data):
        """Draw subtitles at the bottom of the screen."""
        subtitle_text = dialogue_data['text']
        
        # Word wrap for subtitles
        words = subtitle_text.split(' ')
        lines = []
        current_line = []
        
        max_width = WINDOW_WIDTH - 100
        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surf = self.font_subtitle.render(test_line, True, (0, 0, 0))
            if text_surf.get_width() > max_width:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)
                
        if current_line:
            lines.append(' '.join(current_line))
            
        # Draw subtitle background
        subtitle_height = len(lines) * 20 + 20
        subtitle_y = WINDOW_HEIGHT - subtitle_height - 20
        
        bg_surf = pygame.Surface((WINDOW_WIDTH - 40, subtitle_height), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        surface.blit(bg_surf, (20, subtitle_y))
        
        # Draw subtitle text
        for i, line in enumerate(lines):
            text_surf = self.font_subtitle.render(line, True, self.colors['text'])
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, subtitle_y + 15 + i * 20))
            surface.blit(text_surf, text_rect)
            
    def _draw_choices(self, surface):
        """Draw dialogue choice buttons."""
        choice_y = WINDOW_HEIGHT - 200
        
        for i, choice in enumerate(self.choices_available):
            # Create choice button
            choice_button = EnhancedRetroButton(
                WINDOW_WIDTH // 2 - 150, choice_y + i * 40, 300, 35,
                choice,
                color=self.colors['choices'] if i == self.selected_choice else (60, 60, 60)
            )
            choice_button.draw(surface)
            
    def _draw_progress(self, surface):
        """Draw dialogue progress indicator."""
        progress_text = f"{self.dialogue_index + 1}/{len(self.dialogue_sequence)}"
        progress_surf = self.font_small.render(progress_text, True, self.colors['progress'])
        surface.blit(progress_surf, (WINDOW_WIDTH - 80, 50))
        
        # Draw progress bar
        bar_width = 100
        bar_height = 6
        bar_x = WINDOW_WIDTH - 120
        bar_y = 70
        
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        progress = (self.dialogue_index + 1) / len(self.dialogue_sequence)
        fill_width = int(bar_width * progress)
        pygame.draw.rect(surface, COLOR_GOLD, (bar_x, bar_y, fill_width, bar_height))