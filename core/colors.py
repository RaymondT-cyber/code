"""
Pride of Code Color System
==========================

This module implements the color palette specified in the visual identity style guide.
All colors are defined with their hex codes, RGB values, and intended usage.

Style Guide Reference:
Section 2. Color System Specification
"""

import pygame


class ColorPalette:
    """Complete color palette implementation for Pride of Code."""
    
    # Primary Colors
    DARK_GRAPHITE_BLACK = pygame.Color(26, 28, 30)  # #1A1C1E
    RETRO_PIXEL_AMBER = pygame.Color(242, 169, 0)    # #F2A900
    DEEP_SIGNAL_BLUE = pygame.Color(33, 70, 199)     # #2146C7
    
    # Secondary Colors
    SILVER_STEEL = pygame.Color(197, 202, 211)       # #C5CAD3
    STADIUM_TURF_GREEN = pygame.Color(59, 142, 46)   # #3B8E2E
    ERROR_RED = pygame.Color(194, 55, 55)            # #C23737
    
    # Highlight Colors
    NEON_COMPETENCE_CYAN = pygame.Color(67, 224, 236)  # #43E0EC
    PRECISION_MAGENTA = pygame.Color(235, 63, 190)     # #EB3FBE
    GOLD_EXCELLENCE = pygame.Color(255, 201, 71)       # #FFC947
    
    # Additional UI Colors
    TRANSPARENT = pygame.Color(0, 0, 0, 0)
    SEMI_TRANSPARENT_BLACK = pygame.Color(0, 0, 0, 178)  # 70% opacity
    DARKER_GRAPHITE = pygame.Color(15, 16, 17)           # #0F1011
    
    # Color name to value mapping for easy access
    COLOR_MAP = {
        'dark_graphite_black': DARK_GRAPHITE_BLACK,
        'retro_pixel_amber': RETRO_PIXEL_AMBER,
        'deep_signal_blue': DEEP_SIGNAL_BLUE,
        'silver_steel': SILVER_STEEL,
        'stadium_turf_green': STADIUM_TURF_GREEN,
        'error_red': ERROR_RED,
        'neon_competence_cyan': NEON_COMPETENCE_CYAN,
        'precision_magenta': PRECISION_MAGENTA,
        'gold_excellence': GOLD_EXCELLENCE,
        'transparent': TRANSPARENT,
        'semi_transparent_black': SEMI_TRANSPARENT_BLACK,
        'darker_graphite': DARKER_GRAPHITE
    }
    
    @classmethod
    def get_color(cls, name):
        """Get a color by its name."""
        return cls.COLOR_MAP.get(name.lower(), cls.DARK_GRAPHITE_BLACK)
    
    @classmethod
    def adjust_brightness(cls, color, factor):
        """
        Adjust the brightness of a color.
        
        Args:
            color: pygame.Color to adjust
            factor: float between 0.0 (black) and 2.0 (double brightness)
            
        Returns:
            pygame.Color with adjusted brightness
        """
        r = min(255, max(0, int(color.r * factor)))
        g = min(255, max(0, int(color.g * factor)))
        b = min(255, max(0, int(color.b * factor)))
        return pygame.Color(r, g, b, color.a)
    
    @classmethod
    def with_alpha(cls, color, alpha):
        """
        Create a copy of a color with specified alpha.
        
        Args:
            color: pygame.Color to modify
            alpha: int between 0 (transparent) and 255 (opaque)
            
        Returns:
            pygame.Color with specified alpha
        """
        return pygame.Color(color.r, color.g, color.b, alpha)


# Convenience constants for direct access
DARK_GRAPHITE_BLACK = ColorPalette.DARK_GRAPHITE_BLACK
RETRO_PIXEL_AMBER = ColorPalette.RETRO_PIXEL_AMBER
DEEP_SIGNAL_BLUE = ColorPalette.DEEP_SIGNAL_BLUE
SILVER_STEEL = ColorPalette.SILVER_STEEL
STADIUM_TURF_GREEN = ColorPalette.STADIUM_TURF_GREEN
ERROR_RED = ColorPalette.ERROR_RED
NEON_COMPETENCE_CYAN = ColorPalette.NEON_COMPETENCE_CYAN
PRECISION_MAGENTA = ColorPalette.PRECISION_MAGENTA
GOLD_EXCELLENCE = ColorPalette.GOLD_EXCELLENCE
TRANSPARENT = ColorPalette.TRANSPARENT
SEMI_TRANSPARENT_BLACK = ColorPalette.SEMI_TRANSPARENT_BLACK
DARKER_GRAPHITE = ColorPalette.DARKER_GRAPHITE