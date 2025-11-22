"""
Pride of Code Animation System
==============================

Framework for micro-animations described in the visual identity style guide.

Style Guide Reference:
Section 6. Animation Guidelines
Section 4. Micro-Detail Visual Rules
"""

import pygame
import random
import math


class AnimationManager:
    """Central manager for all animations in the game."""
    
    def __init__(self):
        self.animations = []
    
    def add_animation(self, animation):
        """Add an animation to be managed."""
        self.animations.append(animation)
    
    def remove_animation(self, animation):
        """Remove an animation from management."""
        if animation in self.animations:
            self.animations.remove(animation)
    
    def update(self, dt):
        """Update all managed animations."""
        for animation in self.animations[:]:  # Copy list to allow removal during iteration
            animation.update(dt)
            if animation.is_finished():
                self.animations.remove(animation)
    
    def draw(self, surface):
        """Draw all managed animations."""
        for animation in self.animations:
            animation.draw(surface)


class Animation:
    """Base class for all animations."""
    
    def __init__(self, duration):
        self.duration = duration
        self.time_elapsed = 0
        self.finished = False
    
    def update(self, dt):
        """Update animation state."""
        self.time_elapsed += dt
        if self.time_elapsed >= self.duration:
            self.finished = True
            self.on_finish()
    
    def is_finished(self):
        """Check if animation has finished."""
        return self.finished
    
    def draw(self, surface):
        """Draw the animation."""
        pass
    
    def on_finish(self):
        """Called when animation finishes."""
        pass


class ButtonHoverGlow(Animation):
    """
    Button hover shimmer effect.
    
    Style Guide Reference:
    Section 6. Micro-Animations - Button hover shimmer
    """
    
    def __init__(self, button_rect, duration=0.5):
        super().__init__(duration)
        self.button_rect = button_rect
        self.max_alpha = 38  # 15% of 255
    
    def update(self, dt):
        super().update(dt)
    
    def draw(self, surface):
        if not self.is_finished():
            # Calculate current alpha (pulse effect)
            progress = self.time_elapsed / self.duration
            alpha = self.max_alpha * (0.5 + 0.5 * math.sin(progress * math.pi * 4))
            
            # Create glow surface
            glow_surf = pygame.Surface((self.button_rect.width, self.button_rect.height), pygame.SRCALPHA)
            glow_color = (67, 224, 236, int(alpha))  # NEON_COMPETENCE_CYAN with alpha
            pygame.draw.rect(glow_surf, glow_color, 
                           pygame.Rect(0, 0, self.button_rect.width, self.button_rect.height), 
                           border_radius=4)
            surface.blit(glow_surf, self.button_rect)


class ScoreBarFill(Animation):
    """
    Score bar fill increment animation.
    
    Style Guide Reference:
    Section 6. Micro-Animations - Score bar fill increments with 1px steps
    """
    
    def __init__(self, bar_rect, start_value, end_value, duration=0.3):
        super().__init__(duration)
        self.bar_rect = bar_rect
        self.start_value = start_value
        self.end_value = end_value
        self.current_value = start_value
    
    def update(self, dt):
        super().update(dt)
        if not self.is_finished():
            progress = self.time_elapsed / self.duration
            self.current_value = self.start_value + (self.end_value - self.start_value) * progress
    
    def draw(self, surface):
        # This animation doesn't draw directly, it updates the bar value
        pass
    
    def get_current_value(self):
        return self.current_value


class SparkleEffect(Animation):
    """
    Tiny pixel sparkles around high scores.
    
    Style Guide Reference:
    Section 6. Micro-Animations - Tiny pixel sparkles around high scores
    """
    
    def __init__(self, x, y, duration=1.0, count=5):
        super().__init__(duration)
        self.x = x
        self.y = y
        self.particles = []
        
        # Create particles
        for _ in range(count):
            particle = {
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-10, 10),
                'size': random.randint(1, 2),
                'speed_x': random.uniform(-20, 20),
                'speed_y': random.uniform(-20, 20),
                'alpha': 255
            }
            self.particles.append(particle)
    
    def update(self, dt):
        super().update(dt)
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['speed_x'] * dt
            particle['y'] += particle['speed_y'] * dt
            particle['alpha'] = max(0, particle['alpha'] - 200 * dt)
    
    def draw(self, surface):
        if not self.is_finished():
            for particle in self.particles:
                if particle['alpha'] > 0:
                    color = (255, 255, 255, int(particle['alpha']))
                    s = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
                    s.fill(color)
                    surface.blit(s, (particle['x'], particle['y']))


class PixelDissolve(Animation):
    """
    Pixel dissolve transition effect.
    
    Style Guide Reference:
    Section 6. Global Animation Rules - Transitions are slide, fade, or pixel dissolve (3–5 frames)
    """
    
    def __init__(self, surface, rect, duration=0.5):
        super().__init__(duration)
        self.surface = surface
        self.rect = rect
        self.pixel_size = 3  # Size of dissolve blocks
    
    def draw(self, surface):
        if not self.is_finished():
            # Create a copy of the surface
            temp_surface = self.surface.copy()
            
            # Calculate dissolve progress
            progress = self.time_elapsed / self.duration
            
            # Draw grid of pixels that disappear over time
            for y in range(0, self.rect.height, self.pixel_size):
                for x in range(0, self.rect.width, self.pixel_size):
                    # Random threshold determines when this pixel disappears
                    threshold = random.random() * 1.2
                    if progress > threshold:
                        pygame.draw.rect(temp_surface, (0, 0, 0), 
                                       pygame.Rect(self.rect.x + x, self.rect.y + y, 
                                                 self.pixel_size, self.pixel_size))
            
            surface.blit(temp_surface, self.rect)