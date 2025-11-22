
"""Enhanced Competition Scene for Pride of Code.
Features live "show" scene with pixel-art band animations, scoreboard/HUD with three score bars,
contrasting colors (neon green, cyan, magenta), consistent pixel-icon style, minimal overlay HUD,
non-intrusive pop-up tips, volume/mute controls, and colorblind mode toggle.
"""

import pygame
import math
import random
from typing import List, Dict, Optional, Tuple
from core.state_manager import State
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLUE, COLOR_GOLD, 
                   COLOR_TEXT, COLOR_BG, SECTION_COLORS)
from ui.enhanced_retro_button import EnhancedRetroButton


class EnhancedCompetitionScene(State):
    """Enhanced competition scene with live band performance and comprehensive HUD."""
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        
        # Color scheme with neon colors for scores
        self.colors = {
            'field': (34, 139, 34),             # Field green
            'field_lines': (255, 255, 255),     # White lines
            'hud_bg': (20, 20, 30, 180),        # Semi-transparent HUD
            'correctness': (0, 255, 127),       # Neon green
            'creativity': (0, 255, 255),        # Neon cyan
            'performance': (255, 0, 255),       # Neon magenta
            'gold': COLOR_GOLD,                 # Gold for achievements
            'silver': (192, 192, 192),          # Silver
            'bronze': (205, 127, 50),           # Bronze
            'crowd': (100, 100, 120),           # Crowd background
            'stadium': (60, 60, 80),            # Stadium structure
            'text': COLOR_TEXT,
            'shadow': (0, 0, 0),
            'endzone_red': (220, 20, 60),       # End zone red
            'endzone_blue': (30, 144, 255),     # End zone blue
            'yard_line': (255, 255, 0)          # Yellow yard lines
        }
        
        # Fonts
        try:
            self.font_score = pygame.font.Font(None, 36)       # Large for scores
            self.font_hud = pygame.font.Font(None, 24)         # HUD text
            self.font_small = pygame.font.Font(None, 18)       # Small text
            self.font_tiny = pygame.font.Font(None, 14)        # Tiny text
        except:
            self.font_score = pygame.font.SysFont('arial', 36, bold=True)
            self.font_hud = pygame.font.SysFont('arial', 24)
            self.font_small = pygame.font.SysFont('arial', 18)
            self.font_tiny = pygame.font.SysFont('arial', 14)
        
        # Performance state
        self.performance_active = False
        self.performance_time = 0.0
        self.performance_duration = 30.0  # 30 seconds per performance
        
        # Scores (0-100 scale)
        self.scores = {
            'correctness': 0.0,
            'creativity': 0.0,
            'performance': 0.0
        }
        self.target_scores = {
            'correctness': 85.0,
            'creativity': 90.0,
            'performance': 88.0
        }
        
        # Band members
        self.band_members = []
        self._create_band_formation()
        
        # Animation state
        self.animation_time = 0.0
        self.beat_timer = 0.0
        self.current_beat = 0
        self.tempo = 120  # BPM
        
        # Visual effects
        self.particles = []
        self.field_effects = []
        self.spotlight_positions = []
        
        # UI elements
        self._create_ui_elements()
        
        # Settings
        self.volume_level = 0.7
        self.muted = False
        self.colorblind_mode = False
        self.show_tips = True
        self.current_tip_index = 0
        self.tip_timer = 0.0
        
        # Crowd simulation
        self.crowd_intensity = 0.0
        self.crowd_members = []
        self._create_crowd()
        
        # Performance metrics
        self.moves_completed = 0
        self.total_moves = 50
        self.sync_rate = 100.0
        self.creativity_bonus = 0.0
        
        # Retro bowl elements
        self._create_stadium_elements()
        
    def enter(self, **params):
        """Called when entering this state."""
        # Start performance automatically when entering
        self.start_performance()
        
    def _create_band_formation(self):
        """Create initial band formation."""
        sections = ['brass', 'woodwind', 'percussion', 'guard']
        section_sizes = [8, 6, 4, 6]  # Number of members per section
        
        start_x = 200
        start_y = WINDOW_HEIGHT // 2
        
        member_id = 0
        for section_idx, section in enumerate(sections):
            color = SECTION_COLORS[section]
            size = section_sizes[section_idx]
            
            for i in range(size):
                # Create formation pattern
                if section == 'brass':
                    # Brass in front lines
                    x = start_x + (i % 4) * 40
                    y = start_y + (i // 4) * 60 - 60
                elif section == 'woodwind':
                    # Woodwind in middle
                    x = start_x + (i % 3) * 40 + 40
                    y = start_y + (i // 3) * 60
                elif section == 'percussion':
                    # Percussion in back center
                    x = start_x + 80 + i * 30
                    y = start_y - 30
                else:  # guard
                    # Guard on sides
                    if i < 3:
                        x = start_x - 60
                        y = start_y + i * 40 - 40
                    else:
                        x = start_x + 200
                        y = start_y + (i - 3) * 40 - 40
                        
                member = {
                    'id': member_id,
                    'section': section,
                    'x': x,
                    'y': y,
                    'target_x': x,
                    'target_y': y,
                    'color': color,
                    'instrument': self._get_instrument_for_section(section),
                    'move_timer': random.random() * 2,
                    'performance_level': random.uniform(0.8, 1.0),
                    'facing_forward': True,
                    'step_height': 0.0,
                    'animation_offset': random.random() * math.pi * 2,
                    'size': 8 + random.randint(0, 4)  # Variable size for retro effect
                }
                self.band_members.append(member)
                member_id += 1
                
    def _get_instrument_for_section(self, section: str) -> str:
        """Get instrument type for a section."""
        instruments = {
            'brass': 'trumpet',
            'woodwind': 'flute',
            'percussion': 'drum',
            'guard': 'flag'
        }
        return instruments.get(section, 'trumpet')
        
    def _create_crowd(self):
        """Create crowd members in stadium stands."""
        # Create simplified crowd representation
        for i in range(150):
            crowd_member = {
                'x': random.randint(50, WINDOW_WIDTH - 50),
                'y': random.randint(50, 200),  # Top area of screen
                'excitement': random.uniform(0.3, 0.8),
                'color': random.choice([(80, 80, 100), (100, 80, 80), (80, 100, 80)]),
                'animation_offset': random.random() * math.pi * 2,
                'size': 4 + random.randint(0, 3)
            }
            self.crowd_members.append(crowd_member)
            
    def _create_stadium_elements(self):
        """Create stadium elements for retro bowl theme."""
        self.stadium_tiers = []
        
        # Create stadium tiers
        for i in range(8):
            tier = {
                'y': 30 + i * 15,
                'width': 300 - i * 25,
                'color': (50 + i * 2, 50 + i * 2, 60 + i * 2)
            }
            self.stadium_tiers.append(tier)
            
    def _create_ui_elements(self):
        """Create UI elements for the competition scene."""
        # Volume control button
        self.volume_button = EnhancedRetroButton(
            WINDOW_WIDTH - 150, 20, 60, 30,
            "VOL",
            color=(100, 100, 100),
            on_click=lambda: self._toggle_mute()
        )
        
        # Colorblind mode button
        self.colorblind_button = EnhancedRetroButton(
            WINDOW_WIDTH - 220, 20, 60, 30,
            "CB",
            color=(150, 100, 100),
            on_click=lambda: self._toggle_colorblind_mode()
        )
        
        # Tips for performance
        self.performance_tips = [
            "Clean code increases endurance!",
            "Synchronized formations boost score!",
            "Creativity points for unique moves!",
            "Watch the beat markers for timing!",
            "Perfect synchronization = max points!",
            "Use functions for complex formations!",
            "Variables control tempo and volume!",
            "Lists organize your band sections!"
        ]
        
    def start_performance(self, tempo: int = 120, difficulty: str = 'medium'):
        """Start a band performance."""
        self.performance_active = True
        self.performance_time = 0.0
        self.tempo = tempo
        self.beat_timer = 0.0
        self.current_beat = 0
        
        # Reset scores
        self.scores = {
            'correctness': 0.0,
            'creativity': 0.0,
            'performance': 0.0
        }
        
        # Set target scores based on difficulty
        difficulty_multipliers = {
            'easy': 0.7,
            'medium': 1.0,
            'hard': 1.3
        }
        mult = difficulty_multipliers.get(difficulty, 1.0)
        
        self.target_scores = {
            'correctness': 75.0 * mult,
            'creativity': 85.0 * mult,
            'performance': 80.0 * mult
        }
        
        # Generate performance sequence
        self._generate_performance_sequence()
        
        # Create initial particles for excitement
        for _ in range(20):
            self._create_beat_particle()
            
    def _generate_performance_sequence(self):
        """Generate a sequence of formations for the performance."""
        # Create series of target positions for band members
        formations = [
            self._create_line_formation,
            self._create_circle_formation,
            self._create_v_formation,
            self._create_spike_formation,
            self._create_grid_formation
        ]
        
        self.formation_sequence = []
        for i in range(5):  # 5 formations in performance
            formation_func = formations[i % len(formations)]
            targets = formation_func()
            self.formation_sequence.append(targets)
            
    def _create_line_formation(self) -> Dict:
        """Create line formation targets."""
        targets = {}
        for i, member in enumerate(self.band_members):
            targets[member['id']] = {
                'x': 200 + i * 15,
                'y': WINDOW_HEIGHT // 2
            }
        return targets
        
    def _create_circle_formation(self) -> Dict:
        """Create circle formation targets."""
        targets = {}
        center_x = WINDOW_WIDTH // 2 - 200
        center_y = WINDOW_HEIGHT // 2
        radius = 100
        
        for i, member in enumerate(self.band_members):
            angle = (i / len(self.band_members)) * math.pi * 2
            targets[member['id']] = {
                'x': center_x + int(radius * math.cos(angle)),
                'y': center_y + int(radius * math.sin(angle))
            }
        return targets
        
    def _create_v_formation(self) -> Dict:
        """Create V formation targets."""
        targets = {}
        center_x = WINDOW_WIDTH // 2 - 200
        center_y = WINDOW_HEIGHT // 2
        
        for i, member in enumerate(self.band_members):
            if i < len(self.band_members) // 2:
                # Left side of V
                offset = i * 8
                targets[member['id']] = {
                    'x': center_x - offset,
                    'y': center_y - offset
                }
            else:
                # Right side of V
                offset = (i - len(self.band_members) // 2) * 8
                targets[member['id']] = {
                    'x': center_x + offset,
                    'y': center_y - offset
                }
        return targets
        
    def _create_spike_formation(self) -> Dict:
        """Create spike formation targets."""
        targets = {}
        center_x = WINDOW_WIDTH // 2 - 200
        center_y = WINDOW_HEIGHT // 2
        
        for i, member in enumerate(self.band_members):
            if i == 0:
                # Point of spike
                targets[member['id']] = {
                    'x': center_x,
                    'y': center_y - 120
                }
            else:
                # Base of spike
                angle = ((i - 1) / (len(self.band_members) - 1)) * math.pi * 0.6 - math.pi * 0.3
                radius = 80
                targets[member['id']] = {
                    'x': center_x + int(radius * math.sin(angle)),
                    'y': center_y + int(radius * math.cos(angle))
                }
        return targets
        
    def _create_grid_formation(self) -> Dict:
        """Create grid formation targets."""
        targets = {}
        start_x = 150
        start_y = WINDOW_HEIGHT // 2 - 60
        
        for i, member in enumerate(self.band_members):
            row = i // 8
            col = i % 8
            targets[member['id']] = {
                'x': start_x + col * 30,
                'y': start_y + row * 40
            }
        return targets
        
    def handle_event(self, ev):
        """Handle input events."""
        # Handle UI button events
        self.volume_button.handle_event(ev)
        self.colorblind_button.handle_event(ev)
        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                if not self.performance_active:
                    self.start_performance()
            elif ev.key == pygame.K_ESCAPE:
                self._end_performance()
            elif ev.key == pygame.K_m:
                self._toggle_mute()
            elif ev.key == pygame.K_c:
                self._toggle_colorblind_mode()
            elif ev.key == pygame.K_t:
                self.show_tips = not self.show_tips
                
    def update(self, dt):
        """Update the competition scene."""
        self.animation_time += dt
        
        # Update performance
        if self.performance_active:
            self._update_performance(dt)
            
        # Update band members
        self._update_band_members(dt)
        
        # Update visual effects
        self._update_particles(dt)
        self._update_field_effects(dt)
        
        # Update crowd
        self._update_crowd(dt)
        
        # Update UI elements
        self.volume_button.update(dt)
        self.colorblind_button.update(dt)
        
        # Update tips
        if self.show_tips:
            self.tip_timer += dt
            if self.tip_timer > 5.0:  # Change tip every 5 seconds
                self.tip_timer = 0.0
                self.current_tip_index = (self.current_tip_index + 1) % len(self.performance_tips)
                
        # Update stadium elements
        self._update_stadium_elements(dt)
                
    def _update_performance(self, dt):
        """Update the active performance."""
        self.performance_time += dt
        
        # Update beat timer
        beat_interval = 60.0 / self.tempo  # Seconds per beat
        self.beat_timer += dt
        
        if self.beat_timer >= beat_interval:
            self.beat_timer = 0.0
            self.current_beat += 1
            self._on_beat()
            
        # Update formation progress
        formation_index = min(int(self.performance_time / 6.0), len(self.formation_sequence) - 1)
        if formation_index >= 0 and self.formation_sequence:
            current_targets = self.formation_sequence[formation_index]
            self._update_formation_targets(current_targets)
            
        # Update scores based on performance
        self._update_scores(dt)
        
        # Check if performance is complete
        if self.performance_time >= self.performance_duration:
            self._end_performance()
            
    def _on_beat(self):
        """Called on each beat of the music."""
        # Create beat effect
        for member in self.band_members:
            member['step_height'] = 8.0
            
        # Add beat particles
        for _ in range(8):
            self._create_beat_particle()
            
        # Update crowd excitement
        self.crowd_intensity = min(1.0, self.crowd_intensity + 0.05)
        
        # Create ripple effect on field
        self._create_field_effect('ripple', 
                                (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2),
                                (0, 255, 255),  # Cyan ripple
                                20, 100, 2.0)
        
    def _update_formation_targets(self, targets: Dict):
        """Update band member target positions."""
        for member in self.band_members:
            if member['id'] in targets:
                member['target_x'] = targets[member['id']]['x']
                member['target_y'] = targets[member['id']]['y']
                
    def _update_scores(self, dt):
        """Update performance scores."""
        # Gradually increase scores based on performance
        score_rate = dt * 2.0  # Score increase rate
        
        # Correctness based on formation accuracy
        formation_accuracy = self._calculate_formation_accuracy()
        self.scores['correctness'] = min(self.target_scores['correctness'], 
                                        self.scores['correctness'] + formation_accuracy * score_rate)
        
        # Creativity based on variety and complexity
        self.scores['creativity'] = min(self.target_scores['creativity'], 
                                       self.scores['creativity'] + score_rate * 1.2)
        
        # Performance based on synchronization and crowd response
        sync_bonus = self.sync_rate / 100.0
        crowd_bonus = self.crowd_intensity
        self.scores['performance'] = min(self.target_scores['performance'], 
                                        self.scores['performance'] + sync_bonus * crowd_bonus * score_rate)
        
    def _calculate_formation_accuracy(self) -> float:
        """Calculate how accurately band members are in formation."""
        total_distance = 0
        for member in self.band_members:
            dx = member['x'] - member['target_x']
            dy = member['y'] - member['target_y']
            distance = math.sqrt(dx * dx + dy * dy)
            total_distance += distance
            
        average_distance = total_distance / len(self.band_members)
        # Convert distance to accuracy (closer = higher accuracy)
        accuracy = max(0.0, 1.0 - average_distance / 100.0)
        return accuracy
        
    def _update_band_members(self, dt):
        """Update band member positions and animations."""
        for member in self.band_members:
            # Move towards target
            dx = member['target_x'] - member['x']
            dy = member['target_y'] - member['y']
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > 2:
                move_speed = 80.0 * dt * member['performance_level']
                member['x'] += (dx / distance) * move_speed
                member['y'] += (dy / distance) * move_speed
                
            # Update animation
            member['move_timer'] += dt
            if member['step_height'] > 0:
                member['step_height'] = max(0, member['step_height'] - dt * 20.0)
                
            # Add subtle movement
            wobble = math.sin(self.animation_time * 3 + member['animation_offset']) * 2
            member['x'] += wobble * dt
            
    def _update_particles(self, dt):
        """Update particle effects."""
        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        # Update existing particles
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += particle['gravity'] * dt
            particle['life'] -= dt
            particle['rotation'] += particle['rotation_speed'] * dt
            
    def _update_field_effects(self, dt):
        """Update field-based visual effects."""
        # Remove dead effects
        self.field_effects = [e for e in self.field_effects if e['duration'] > 0]
        
        # Update existing effects
        for effect in self.field_effects:
            effect['duration'] -= dt
            effect['radius'] += effect['expansion_rate'] * dt
            
    def _update_crowd(self, dt):
        """Update crowd animation and excitement."""
        self.crowd_intensity = max(0.0, self.crowd_intensity - dt * 0.1)
        
        for crowd_member in self.crowd_members:
            # Animate crowd members
            excitement = crowd_member['excitement'] + self.crowd_intensity
            if excitement > 0.7:
                # Jumping animation
                jump = abs(math.sin(self.animation_time * 5 + crowd_member['animation_offset'])) * 10
                crowd_member['current_y'] = crowd_member['y'] - jump
            else:
                crowd_member['current_y'] = crowd_member['y']
                
    def _update_stadium_elements(self, dt):
        """Update stadium background elements."""
        # Animate stadium tiers
        for tier in self.stadium_tiers:
            tier['width'] += math.sin(self.animation_time * 0.5 + tier['y'] * 0.01) * 0.3
                
    def _create_beat_particle(self):
        """Create a particle effect for beat emphasis."""
        particle = {
            'x': random.randint(100, WINDOW_WIDTH - 100),
            'y': random.randint(200, WINDOW_HEIGHT - 200),
            'vx': random.uniform(-50, 50),
            'vy': random.uniform(-100, -50),
            'gravity': 200,
            'life': random.uniform(0.5, 1.5),
            'color': random.choice([self.colors['correctness'], self.colors['creativity'], self.colors['performance']]),
            'size': random.randint(2, 6),
            'rotation': 0,
            'rotation_speed': random.uniform(-180, 180)
        }
        self.particles.append(particle)
        
    def _create_field_effect(self, effect_type: str, center: Tuple[int, int], 
                           color: Tuple[int, int, int], initial_radius: int,
                           max_radius: int, duration: float):
        """Create a field-based visual effect."""
        effect = {
            'type': effect_type,
            'center': center,
            'color': color,
            'radius': initial_radius,
            'max_radius': max_radius,
            'duration': duration,
            'max_duration': duration,
            'expansion_rate': (max_radius - initial_radius) / duration
        }
        self.field_effects.append(effect)
        
    def _toggle_mute(self):
        """Toggle audio mute."""
        self.muted = not self.muted
        volume_text = "MUTED" if self.muted else f"{int(self.volume_level * 100)}%"
        self.volume_button.set_text(volume_text)
        
    def _toggle_colorblind_mode(self):
        """Toggle colorblind mode."""
        self.colorblind_mode = not self.colorblind_mode
        cb_text = "CB ON" if self.colorblind_mode else "CB"
        self.colorblind_button.set_text(cb_text)
        
    def _end_performance(self):
        """End the current performance and show results."""
        self.performance_active = False
        
        # Calculate final score
        total_score = (self.scores['correctness'] + self.scores['creativity'] + self.scores['performance']) / 3.0
        
        # Pass results to results screen
        self.manager.switch('results', {
            'scores': self.scores.copy(),
            'total_score': total_score,
            'performance_time': self.performance_time,
            'moves_completed': self.moves_completed,
            'sync_rate': self.sync_rate
        })
        
    def draw(self, surface):
        """Render the enhanced competition scene."""
        # Draw stadium background
        self._draw_stadium(surface)
        
        # Draw field
        self._draw_field(surface)
        
        # Draw crowd
        self._draw_crowd(surface)
        
        # Draw band members
        self._draw_band_members(surface)
        
        # Draw visual effects
        self._draw_particles(surface)
        self._draw_field_effects(surface)
        
        # Draw HUD
        self._draw_hud(surface)
        
        # Draw UI elements
        self._draw_ui(surface)
        
        # Draw tips if enabled
        if self.show_tips and not self.performance_active:
            self._draw_tips(surface)
            
    def _draw_stadium(self, surface):
        """Draw stadium background elements."""
        # Sky gradient
        for y in range(WINDOW_HEIGHT // 3):
            color = (135 - y // 6, 206 - y // 6, 235 - y // 6)
            pygame.draw.line(surface, color, (0, y), (WINDOW_WIDTH, y))
            
        # Draw stadium tiers
        for tier in self.stadium_tiers:
            tier_rect = pygame.Rect(
                WINDOW_WIDTH // 2 - tier['width'] // 2,
                tier['y'],
                tier['width'],
                12
            )
            pygame.draw.rect(surface, tier['color'], tier_rect)
            
        # Stadium stands
        pygame.draw.rect(surface, self.colors['stadium'], (0, 50, WINDOW_WIDTH, 150))
        
        # Stadium details
        for x in range(0, WINDOW_WIDTH, 80):
            pygame.draw.rect(surface, (40, 40, 50), (x, 60, 60, 120))
            
    def _draw_field(self, surface):
        """Draw the marching field with retro bowl styling."""
        # Main field
        field_rect = pygame.Rect(50, 200, WINDOW_WIDTH - 100, WINDOW_HEIGHT - 250)
        pygame.draw.rect(surface, self.colors['field'], field_rect)
        
        # End zones
        left_endzone = pygame.Rect(50, 200, 30, WINDOW_HEIGHT - 250)
        right_endzone = pygame.Rect(WINDOW_WIDTH - 80, 200, 30, WINDOW_HEIGHT - 250)
        pygame.draw.rect(surface, self.colors['endzone_red'], left_endzone)
        pygame.draw.rect(surface, self.colors['endzone_blue'], right_endzone)
        
        # Yard lines (white)
        for x in range(80, WINDOW_WIDTH - 50, 40):
            pygame.draw.line(surface, self.colors['field_lines'], 
                           (x, 200), (x, WINDOW_HEIGHT - 50), 2)
            
        # Hash marks
        for y in range(250, WINDOW_HEIGHT - 50, 80):
            for x in range(100, WINDOW_WIDTH - 75, 80):
                pygame.draw.line(surface, self.colors['field_lines'],
                               (x, y), (x, y + 15), 2)
                               
        # Center line
        pygame.draw.line(surface, self.colors['yard_line'],
                        (WINDOW_WIDTH // 2 - 200, 200), (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 50), 4)
                        
        # Yard numbers
        yard_numbers = ['10', '20', '30', '40', '50', '40', '30', '20', '10']
        for i, num in enumerate(yard_numbers):
            x_pos = 120 + i * 60
            if x_pos < WINDOW_WIDTH - 100:
                num_surf = self.font_small.render(num, True, self.colors['yard_line'])
                surface.blit(num_surf, (x_pos - 10, 210))
                surface.blit(num_surf, (x_pos - 10, WINDOW_HEIGHT - 70))
                
    def _draw_crowd(self, surface):
        """Draw animated crowd."""
        for crowd_member in self.crowd_members:
            y = getattr(crowd_member, 'current_y', crowd_member['y'])
            
            # Draw simplified crowd member
            size = crowd_member['size']
            pygame.draw.circle(surface, crowd_member['color'], 
                             (crowd_member['x'], y), size)
            
            # Add excitement effects
            if crowd_member['excitement'] + self.crowd_intensity > 0.8:
                # Draw arms up
                pygame.draw.line(surface, crowd_member['color'],
                               (crowd_member['x'] - size//2, y), 
                               (crowd_member['x'] - size, y - size), 2)
                pygame.draw.line(surface, crowd_member['color'],
                               (crowd_member['x'] + size//2, y), 
                               (crowd_member['x'] + size, y - size), 2)
                               
    def _draw_band_members(self, surface):
        """Draw all band members with instruments."""
        for member in self.band_members:
            self._draw_band_member(surface, member)
            
    def _draw_band_member(self, surface, member):
        """Draw a single band member."""
        x = int(member['x'])
        y = int(member['y'] - member['step_height'])
        size = member['size']
        
        # Draw shadow
        shadow_offset = 2
        pygame.draw.ellipse(surface, (0, 0, 0, 100),
                          (x - size//3 + shadow_offset, y + shadow_offset, size//1.5, size//3))
        
        # Draw body
        pygame.draw.circle(surface, member['color'], (x, y), size//2)
        
        # Draw instrument
        self._draw_instrument(surface, x, y, member['instrument'], member['color'], size)
        
        # Draw performance indicator
        if member['performance_level'] > 0.9:
            # Star for high performance
            self._draw_star(surface, x + size, y - size//2, size//3, self.colors['gold'])
            
    def _draw_instrument(self, surface, x, y, instrument, color, size):
        """Draw instrument for band member."""
        if instrument == 'trumpet':
            # Trumpet
            pygame.draw.rect(surface, color, (x + size//2, y - size//4, size, size//4))
            pygame.draw.circle(surface, color, (x + size, y - size//8), size//3)
        elif instrument == 'flute':
            # Flute
            pygame.draw.rect(surface, color, (x + size//2, y - size//6, size, size//6))
        elif instrument == 'drum':
            # Drum
            pygame.draw.rect(surface, (139, 69, 19), (x - size//2, y - size//3, size//1.5, size//1.5))
            pygame.draw.rect(surface, (255, 255, 255), (x - size//2, y - size//3, size//1.5, size//6))
        elif instrument == 'flag':
            # Flag
            pole_color = (100, 100, 100)
            flag_color = color
            
            # Pole
            pygame.draw.rect(surface, pole_color, (x + size//2, y - size, size//8, size))
            # Flag
            points = [(x + size//2 + size//8, y - size), 
                     (x + size//2 + size//8 + size//2, y - size + size//4), 
                     (x + size//2 + size//8, y - size + size//2)]
            pygame.draw.polygon(surface, flag_color, points)
            
    def _draw_star(self, surface, x, y, size, color):
        """Draw a small star."""
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
        
    def _draw_particles(self, surface):
        """Draw particle effects."""
        for particle in self.particles:
            alpha = particle['life'] / 1.5
            size = int(particle['size'] * alpha)
            if size > 0:
                # Create a surface for the particle with alpha
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = (*particle['color'], int(255 * alpha))
                pygame.draw.rect(particle_surf, color, (0, 0, size * 2, size * 2))
                surface.blit(particle_surf, (particle['x'] - size, particle['y'] - size))
                
    def _draw_field_effects(self, surface):
        """Draw field-based visual effects."""
        for effect in self.field_effects:
            if effect['type'] == 'ripple':
                alpha = 1.0 - (effect['duration'] / effect['max_duration'])
                color = (*effect['color'], int(alpha * 200))
                pygame.draw.circle(surface, color, effect['center'], 
                                 int(effect['radius']), 3)
                                
    def _draw_hud(self, surface):
        """Draw the heads-up display."""
        # HUD background
        hud_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 80)
        hud_surf = pygame.Surface((WINDOW_WIDTH, 80), pygame.SRCALPHA)
        hud_surf.fill(self.colors['hud_bg'])
        surface.blit(hud_surf, (0, 0))
        
        # Score bars
        self._draw_score_bars(surface)
        
        # Performance timer
        if self.performance_active:
            time_text = f"Time: {self.performance_time:.1f}s / {self.performance_duration:.1f}s"
            time_surf = self.font_hud.render(time_text, True, self.colors['text'])
            surface.blit(time_surf, (WINDOW_WIDTH // 2 - 80, 40))
            
        # Beat indicator
        if self.performance_active:
            beat_size = int(5 + self.beat_timer * 10)
            pygame.draw.circle(surface, self.colors['gold'], (50, 40), beat_size)
            beat_text = self.font_tiny.render(f"Beat: {self.current_beat}", True, self.colors['text'])
            surface.blit(beat_text, (20, 55))
            
        # Tempo indicator
        tempo_text = f"Tempo: {self.tempo} BPM"
        tempo_surf = self.font_tiny.render(tempo_text, True, self.colors['text'])
        surface.blit(tempo_surf, (WINDOW_WIDTH - 150, 55))
            
    def _draw_score_bars(self, surface):
        """Draw the three score bars."""
        bar_width = 200
        bar_height = 20
        bar_y = 15
        bar_spacing = 250
        
        scores = [
            ('Correctness', self.scores['correctness'], self.colors['correctness']),
            ('Creativity', self.scores['creativity'], self.colors['creativity']),
            ('Performance', self.scores['performance'], self.colors['performance'])
        ]
        
        for i, (label, score, color) in enumerate(scores):
            x = 150 + i * bar_spacing
            
            # Draw background bar
            pygame.draw.rect(surface, (40, 40, 50), (x, bar_y, bar_width, bar_height))
            
            # Draw filled bar
            fill_width = int((score / 100.0) * bar_width)
            pygame.draw.rect(surface, color, (x, bar_y, fill_width, bar_height))
            
            # Draw bar border
            pygame.draw.rect(surface, self.colors['text'], (x, bar_y, bar_width, bar_height), 2)
            
            # Draw label and score
            label_text = f"{label}: {int(score)}%"
            label_surf = self.font_small.render(label_text, True, self.colors['text'])
            surface.blit(label_surf, (x, bar_y + 25))
            
            # Use colorblind-friendly patterns if needed
            if self.colorblind_mode:
                patterns = ['===', '///', "\\\\\\"]
                pattern_surf = self.font_tiny.render(patterns[i], True, self.colors['text'])
                surface.blit(pattern_surf, (x + bar_width + 5, bar_y + 5))
                
    def _draw_ui(self, surface):
        """Draw UI elements."""
        self.volume_button.draw(surface)
        self.colorblind_button.draw(surface)
        
        # Draw performance status
        if self.performance_active:
            status_text = "PERFORMANCE ACTIVE"
            status_color = self.colors['correctness']
        else:
            status_text = "Press SPACE to Start"
            status_color = self.colors['text']
            
        status_surf = self.font_hud.render(status_text, True, status_color)
        status_rect = status_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        surface.blit(status_surf, status_rect)
        
    def _draw_tips(self, surface):
        """Draw performance tips."""
        if self.current_tip_index < len(self.performance_tips):
            tip_text = self.performance_tips[self.current_tip_index]
            
            # Create semi-transparent background for tip
            tip_surf = self.font_small.render(tip_text, True, self.colors['text'])
            tip_rect = tip_surf.get_rect(center=(WINDOW_WIDTH // 2, 120))
            
            # Draw tip background
            bg_rect = tip_rect.inflate(20, 10)
            bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surf.fill((30, 30, 40, 200))
            surface.blit(bg_surf, bg_rect)
            
            # Draw tip text
            surface.blit(tip_surf, tip_rect)
