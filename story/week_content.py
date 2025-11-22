"""
Week Content System for Pride of Code Story Implementation.
Contains all 16 weeks of story content, character development, Python lessons,
and branching dialogue paths for competition outcomes.
"""

from typing import List, Dict, Optional, Tuple
import json


class WeekContent:
    """Comprehensive week content system for the 16-week Pride of Code campaign."""
    
    def __init__(self):
        self.weeks = self._create_all_weeks_content()
        
    def _create_all_weeks_content(self) -> Dict[int, Dict]:
        """Create content for all 16 weeks."""
        return {
            1: self._create_week_1(),
            2: self._create_week_2(),
            3: self._create_week_3(),
            4: self._create_week_4(),
            5: self._create_week_5(),
            6: self._create_week_6(),
            7: self._create_week_7(),
            8: self._create_week_8(),
            9: self._create_week_9(),
            10: self._create_week_10(),
            11: self._create_week_11(),
            12: self._create_week_12(),
            13: self._create_week_13(),
            14: self._create_week_14(),
            15: self._create_week_15(),
            16: self._create_week_16()
        }
        
    def get_week_content(self, week_number: int) -> Optional[Dict]:
        """Get content for a specific week."""
        return self.weeks.get(week_number)
        
    def get_story_dialogue(self, week_number: int, outcome: str = None) -> List[Dict]:
        """Get story dialogue for a specific week with outcome branching."""
        week_content = self.get_week_content(week_number)
        if not week_content:
            return []
            
        dialogue = week_content.get('story_dialogue', [])
        
        # Apply outcome branching if this is a competition week
        if week_content.get('is_competition') and outcome:
            outcome_dialogue = week_content.get('outcome_dialogue', {}).get(outcome, [])
            dialogue.extend(outcome_dialogue)
            
        return dialogue
        
    def get_python_lesson(self, week_number: int) -> Dict:
        """Get Python lesson content for a specific week."""
        week_content = self.get_week_content(week_number)
        return week_content.get('python_lesson', {})
        
    # Week 1: "Fresh Beats, Fresh Start" (Variables)
    def _create_week_1(self) -> Dict:
        return {
            'title': "Fresh Beats, Fresh Start",
            'theme': "New Beginnings",
            'python_concept': "Variables",
            'is_competition': False,
            'location': 'band_room',
            
            'story_dialogue': [
                {
                    'character': 'coach_hodge',
                    'text': "Welcome to Pride of Code! I'm Assistant Coach Hodge, and this is going to be an amazing season.",
                    'emotion': 'welcoming',
                    'scene': 'band_room_entrance'
                },
                {
                    'character': 'leah',
                    'text': "The band room is buzzing today! Let me give you a quick tour of our rehearsal halls.",
                    'emotion': 'proud',
                    'scene': 'band_room_tour'
                },
                {
                    'character': 'leah',
                    'text': "I'm Leah, the drum major. I'll be helping you lead the band through our routines.",
                    'emotion': 'disciplined',
                    'scene': 'introduction'
                },
                {
                    'character': 'elijah',
                    'text': "Hey Captain! Can we code our way to the trophy? I've got a good feeling about this season!",
                    'emotion': 'joking',
                    'scene': 'meet_percussion'
                },
                {
                    'character': 'anna',
                    'text': "Um... hi everyone. I'm Anna, I play flute. It's nice to meet you all.",
                    'emotion': 'shy',
                    'scene': 'meet_woodwind'
                },
                {
                    'character': 'alex',
                    'text': "I noticed your laptop! I've been working on a band.api interface to sync music and lights with code!",
                    'emotion': 'excited',
                    'scene': 'meet_tech'
                },
                {
                    'character': 'leah',
                    'text': "Today we'll learn about variables - they're like labeled containers for values in our band routines.",
                    'emotion': 'teaching',
                    'scene': 'lesson_introduction'
                },
                {
                    'character': 'alex',
                    'text': "For example: tempo = 120 sets our marching speed, uniform_color = 'blue' picks our outfit theme!",
                    'emotion': 'technical',
                    'scene': 'code_demonstration'
                },
                {
                    'character': 'coach_hodge',
                    'text': "Great news everyone! We've signed up for a local competition in two weeks. Let's make this count!",
                    'emotion': 'excited',
                    'scene': 'competition_announcement'
                },
                {
                    'character': 'elijah',
                    'text': "Two weeks? That's plenty of time to code our way to victory! Let's get started!",
                    'emotion': 'enthusiastic',
                    'scene': 'team_motivation'
                }
            ],
            
            'python_lesson': {
                'concept': 'Variables',
                'description': 'Learn to use variables to control band settings like tempo, uniform color, and volume.',
                'examples': [
                    'tempo = 120  # Set marching speed in BPM',
                    'uniform_color = "blue"  # Choose uniform theme',
                    'volume = 7  # Set music loudness (1-10)',
                    'formation_style = "line"  # Set formation pattern'
                ],
                'exercise': {
                    'title': 'Your First Variables',
                    'instructions': [
                        'Set the tempo to 120 BPM for a moderate marching pace',
                        'Choose blue as the uniform color',
                        'Set the volume to 7 for balanced sound',
                        'Run your code to see the band respond!'
                    ],
                    'starter_code': [
                        '# Welcome to Pride of Code!',
                        '# Set your variables below:',
                        '',
                        'tempo =',
                        'uniform_color =',
                        'volume =',
                        '',
                        '# Test your settings with:',
                        'print(f"Tempo: {tempo} BPM")',
                        'print(f"Uniform: {uniform_color}")',
                        'print(f"Volume: {volume}/10")'
                    ],
                    'expected_output': 'Band should march at 120 BPM with blue uniforms and moderate volume.'
                },
                'learning_objectives': [
                    'Understand what variables are and how to create them',
                    'Learn variable naming conventions',
                    'Practice assigning different types of values',
                    'See how variables affect the band performance'
                ]
            },
            
            'character_development': {
                'leah': {
                    'arc_point': 'Introduction as disciplined leader',
                    'growth': 'Shows her pride in the band and willingness to teach',
                    'relationships': 'Establishes herself as a mentor figure'
                },
                'elijah': {
                    'arc_point': 'Immediate energetic personality',
                    'growth': 'Shows his joking nature and instant rapport',
                    'relationships': 'Bonds immediately with the player, calls them "Captain"'
                },
                'anna': {
                    'arc_point': 'Initial shyness and quiet observation',
                    'growth': 'Takes small steps to participate in group',
                    'relationships': 'Observes from sidelines, blushes when complimented'
                },
                'alex': {
                    'arc_point': 'Tech enthusiasm and expertise',
                    'growth': 'Shows passion for combining music and code',
                    'relationships': 'Excited to share band.api project with player'
                },
                'coach_hodge': {
                    'arc_point': 'Supportive authority figure',
                    'growth': 'Shows confidence in new approach',
                    'relationships': 'Provides encouragement and sets positive tone'
                }
            },
            
            'next_week_setup': {
                'summary': 'The band prepares for their first local competition in two weeks',
                'character_actions': {
                    'leah': 'Assigns sections to practice with new variable settings',
                    'alex': 'Promises to prepare basic band.api script for experimentation',
                    'elijah': 'Leads the team in brainstorming creative ideas',
                    'anna': 'Quietly observes and begins to feel more included'
                },
                'transition_line': "The episode closes with the team walking out together, animatedly brainstorming creative ideas for their upcoming competition."
            }
        }
        
    # Week 2: "First Competition Frenzy" (Conditionals)
    def _create_week_2(self) -> Dict:
        return {
            'title': "First Competition Frenzy",
            'theme': "Facing Challenges",
            'python_concept': "Conditionals",
            'is_competition': True,
            'location': 'local_competition',
            
            'story_dialogue': [
                {
                    'character': 'leah',
                    'text': "Competition day is here! Everyone remember the variable settings we practiced last week.",
                    'emotion': 'focused',
                    'scene': 'backstage_prep'
                },
                {
                    'character': 'elijah',
                    'text': "I've got my drumsticks polished and ready! Let's show them what Pride of Code can do!",
                    'emotion': 'excited',
                    'scene': 'percussion_ready'
                },
                {
                    'character': 'alex',
                    'text': "I set up conditional code to handle weather changes. If it rains, we'll automatically switch to indoor formation!",
                    'emotion': 'technical',
                    'scene': 'tech_preparation'
                },
                {
                    'character': 'anna',
                    'text': "I practiced the flute part all week. I hope I don't get too nervous and mess up.",
                    'emotion': 'nervous',
                    'scene': 'personal_doubt'
                },
                {
                    'character': 'leah',
                    'text': "You'll do great, Anna. We've all practiced hard. Now let's show them what we've learned!",
                    'emotion': 'encouraging',
                    'scene': 'team_pep_talk'
                }
            ],
            
            'outcome_dialogue': {
                'win': [
                    {
                        'character': 'leah',
                        'text': "We won! Thank you so much for helping us create such a perfect routine with conditional code!",
                        'emotion': 'celebrating',
                        'scene': 'victory_celebration'
                    },
                    {
                        'character': 'elijah',
                        'text': "Victory march time! I'm officially declaring myself 'Chief Dance Officer' of Pride of Code!",
                        'emotion': 'triumph',
                        'scene': 'elijah_celebration'
                    },
                    {
                        'character': 'riley',  # Rival drum major
                        'text': "Great job out there! Your coding approach really gave you an edge. See you at the next round!",
                        'emotion': 'respectful',
                        'scene': 'rival_interaction'
                    }
                ],
                'loss': [
                    {
                        'character': 'leah',
                        'text': "We didn't win, but I'm proud of how we handled the unexpected rain. Our conditional code saved the performance!",
                        'emotion': 'determined',
                        'scene': 'gracious_defeat'
                    },
                    {
                        'character': 'elijah',
                        'text': "Next time, more cowbell! And maybe fewer rain clouds. But seriously, we were awesome!",
                        'emotion': 'optimistic',
                        'scene': 'morale_boost'
                    },
                    {
                        'character': 'riley',
                        'text': "You guys handled that weather situation perfectly. Here are some tips for performing in tough conditions.",
                        'emotion': 'helpful',
                        'scene': 'friendly_advice'
                    }
                ]
            },
            
            'python_lesson': {
                'concept': 'Conditionals (Decision Making)',
                'description': 'Learn to use if/else statements to make your band routines adapt to different situations.',
                'examples': [
                    'if weather == "rain":',
                    '    use_indoor_formation()',
                    'else:',
                    '    use_outdoor_show()',
                    '',
                    'if crowd_cheers > 3:',
                    '    emphasize_drums()',
                    'elif energy_low:',
                    '    play_upbeat_song()'
                ],
                'exercise': {
                    'title': 'Adaptive Performance',
                    'instructions': [
                        'Write conditional code to handle weather changes',
                        'Add crowd reaction based adjustments',
                        'Test your logic with different scenarios',
                        'See how your band adapts automatically!'
                    ],
                    'starter_code': [
                        '# Competition Day - Handle the Unexpected!',
                        'weather = "rain"  # Try: "rain", "sunny", "cloudy"',
                        'crowd_level = 4   # Try: 1-5',
                        '',
                        'if weather == "rain":',
                        '    # What should the band do in rain?',
                        '    formation =',
                        '',
                        'elif weather == "sunny":',
                        '    # What formation for sunny weather?',
                        '    formation =',
                        '',
                        'else:',
                        '    # Default formation',
                        '    formation =',
                        '',
                        'if crowd_level > 3:',
                        '    # How to respond to excited crowd?',
                        '    special_move =',
                        'else:',
                        '    special_move = "standard_performance"'
                    ],
                    'expected_output': 'Band should automatically adapt formation and performance based on weather and crowd reaction.'
                },
                'learning_objectives': [
                    'Understand if/elif/else conditional structure',
                    'Learn to write logical conditions',
                    'Practice nesting conditionals for complex decisions',
                    'Apply conditionals to real-world band scenarios'
                ]
            }
        }
        
    # Week 3: "Loops of Rehearsal" (Loops)
    def _create_week_3(self) -> Dict:
        return {
            'title': "Loops of Rehearsal",
            'theme': "Practice and Persistence",
            'python_concept': "Loops",
            'is_competition': False,
            'location': 'practice_field',
            
            'story_dialogue': [
                {
                    'character': 'coach_hodge',
                    'text': "Back from competition, and it's time for some serious practice. The regional competition is just one week away!",
                    'emotion': 'motivated',
                    'scene': 'practice_announcement'
                },
                {
                    'character': 'leah',
                    'text': "We need to practice this tricky drill sequence over and over. But everyone's getting tired of counting manually.",
                    'emotion': 'concerned',
                    'scene': 'rehearsal_challenge'
                },
                {
                    'character': 'elijah',
                    'text': "I swear I've done this march a hundred times! My arms are getting tired just holding these drumsticks!",
                    'emotion': 'exhausted_joking',
                    'scene': 'practice_fatigue'
                },
                {
                    'character': 'player',
                    'text': "I have an idea! Instead of manually counting, let's use loops in our code to handle the repetition automatically.",
                    'emotion': 'problem_solving',
                    'scene': 'solution_proposal'
                },
                {
                    'character': 'alex',
                    'text': "Perfect! I can write a loop that plays the drum cadence 8 times: for i in range(8): play_cadence()",
                    'emotion': 'technical',
                    'scene': 'code_implementation'
                },
                {
                    'character': 'anna',
                    'text': "Wow, that's so much easier! The code does the counting for us. I can focus on playing my flute perfectly.",
                    'emotion': 'relieved',
                    'scene': 'practice_improvement'
                },
                {
                    'character': 'leah',
                    'text': "This is exactly what we needed. Everyone, let's try it with the automated counting!",
                    'emotion': 'impressed',
                    'scene': 'team_success'
                }
            ],
            
            'python_lesson': {
                'concept': 'Loops (Repetition)',
                'description': 'Learn to use loops to automate repetitive tasks and create consistent drill patterns.',
                'examples': [
                    'for i in range(8):',
                    '    band.play_cadence()',
                    '',
                    'for step in formation_steps:',
                    '    move(step)',
                    '',
                    'while practice_time > 0:',
                    '    run_drill()',
                    '    practice_time -= 1'
                ],
                'exercise': {
                    'title': 'Automated Drill Practice',
                    'instructions': [
                        'Create a loop to repeat a drill sequence',
                        'Use different loop types for various patterns',
                        'Combine loops with variables for dynamic practice',
                        'Watch the band practice automatically!'
                    ],
                    'starter_code': [
                        '# Practice Loop Exercise',
                        'drill_repeats = 8  # How many times to repeat?',
                        '',
                        '# Use a for loop to repeat the drill',
                        'for i in range(drill_repeats):',
                        '    print(f"Drill repetition {i + 1}")',
                        '    # Add your drill commands here:',
                        '    ',
                        '',
                        '# Practice different formations with a while loop',
                        'practice_count = 0',
                        'while practice_count < 3:',
                        '    print("Practicing formation...")',
                        '    # Add formation practice here:',
                        '    ',
                        '    practice_count += 1'
                    ],
                    'expected_output': 'Band should automatically repeat drills and formations without manual counting.'
                },
                'learning_objectives': [
                    'Master for loops with range()',
                    'Learn while loops for conditional repetition',
                    'Understand loop control with break and continue',
                    'Apply loops to automate band practice routines'
                ]
            }
        }
        
    # Week 4: "Functions and Formations" (Functions)
    def _create_week_4(self) -> Dict:
        return {
            'title': "Functions and Formations",
            'theme': "Teamwork and Precision",
            'python_concept': "Functions",
            'is_competition': True,
            'location': 'regional_competition',
            
            'story_dialogue': [
                {
                    'character': 'coach_hodge',
                    'text': "The regional marching challenge is here! This is a bigger contest with several schools competing.",
                    'emotion': 'excited',
                    'scene': 'competition_arrival'
                },
                {
                    'character': 'leah',
                    'text': "Our routine is getting complex. I think we need to break it into manageable sections.",
                    'emotion': 'strategic',
                    'scene': 'strategy_meeting'
                },
                {
                    'character': 'player',
                    'text': "Perfect timing to learn about functions! We can divide our performance into distinct sections like opening_fanfare(), drill_section(), and closing_flourish().",
                    'emotion': 'teaching',
                    'scene': 'lesson_introduction'
                },
                {
                    'character': 'alex',
                    'text': "I see! So we can call opening_fanfare(), then drill_section(), then closing_flourish() in order. Each section has its own code!",
                    'emotion': 'understanding',
                    'scene': 'code_comprehension'
                },
                {
                    'character': 'elijah',
                    'text': "Does this mean I get my own special percussion solo function? I've been working on this amazing drum routine!",
                    'emotion': 'excited',
                    'scene': 'solo_opportunity'
                },
                {
                    'character': 'anna',
                    'text': "I can help organize the woodwind sections into functions too. Maybe I can write one for our harmony parts.",
                    'emotion': 'confident',
                    'scene': 'taking_initiative'
                }
            ],
            
            'outcome_dialogue': {
                'win': [
                    {
                        'character': 'leah',
                        'text': "Second place at regionals! Our function-based organization gave us the edge we needed!",
                        'emotion': 'proud',
                        'scene': 'achievement_celebration'
                    },
                    {
                        'character': 'elijah',
                        'text': "Did you see my solo? The percussion function was epic! Code should totally get a trophy!",
                        'emotion': 'jubilant',
                        'scene': 'solo_triumph'
                    },
                    {
                        'character': 'riley',
                        'text': "Your organization is impressive. How do you keep everything so synchronized?",
                        'emotion': 'curious',
                        'scene': 'technical_exchange'
                    }
                ],
                'loss': [
                    {
                        'character': 'leah',
                        'text': "We didn't get first place, but the judges gave us special mention for creativity!",
                        'emotion': 'proud_despite_loss',
                        'scene': 'silver_linings'
                    },
                    {
                        'character': 'anna',
                        'text': "I noticed a timing issue in the woodwind function. Next time we'll be even better!",
                        'emotion': 'analytical',
                        'scene': 'learning_from_loss'
                    },
                    {
                        'character': 'riley',
                        'text': "Your approach is innovative. Would you be interested in sharing some techniques sometime?",
                        'emotion': 'friendly',
                        'scene': 'building_relationships'
                    }
                ]
            },
            
            'python_lesson': {
                'concept': 'Functions (Modularity)',
                'description': 'Learn to create functions to organize your code into reusable, manageable sections.',
                'examples': [
                    'def opening_fanfare():',
                    '    play_trumpets()',
                    '    play_drums()',
                    '',
                    'def drill_section():',
                    '    execute_formation_steps()',
                    '',
                    'def closing_flourish():',
                    '    emphasize_percussion()',
                    '',
                    '# Run the show',
                    'opening_fanfare()',
                    'drill_section()',
                    'closing_flourish()'
                ],
                'exercise': {
                    'title': 'Modular Performance',
                    'instructions': [
                        'Create functions for different performance sections',
                        'Organize your routine with clear function names',
                        'Pass parameters to customize performance elements',
                        'Build a complete show using multiple functions!'
                    ],
                    'starter_code': [
                        '# Function-Based Performance',
                        '',
                        'def opening_section():',
                        '    # Write your opening routine here',
                        '    print("🎺 Opening fanfare begins!")',
                        '    ',
                        '',
                        'def main_performance():',
                        '    # Write your main drill here',
                        '    print("👯 Main drill sequence!")',
                        '    ',
                        '',
                        'def finale_section():',
                        '    # Write your finale here',
                        '    print("🎆 Grand finale!")',
                        '    ',
                        '',
                        '# Run your complete show:',
                        'opening_section()',
                        'main_performance()',
                        'finale_section()'
                    ],
                    'expected_output': 'Band should perform a complete show organized into clear, reusable function sections.'
                }
            }
        }
        
    # Include additional weeks 5-16 with similar comprehensive structure...
    def _create_week_5(self) -> Dict:
        """Week 5: "Harmony and Discord" (Lists) - Conflict and Resolution"""
        return {
            'title': "Harmony and Discord",
            'theme': "Conflict and Resolution",
            'python_concept': "Lists",
            'is_competition': False,
            'story_summary': "Creative tensions emerge between Leah and Elijah over routine direction, teaching the team to blend structure with spontaneity.",
            'python_lesson': {
                'concept': 'Lists (Organization)',
                'examples': [
                    'sections = ["brass", "woodwind", "percussion", "guard"]',
                    'routine_steps = ["march_forward", "left_turn", "right_turn", "jazz_riff"]',
                    'for section in sections:',
                    '    section.play_note()'
                ]
            }
        }
        
    def _create_week_6(self) -> Dict:
        """Week 6: "Midseason Mayhem" (Dictionaries)"""
        return {
            'title': "Midseason Mayhem", 
            'theme': "Unexpected Challenges",
            'python_concept': "Dictionaries",
            'is_competition': True,
            'story_summary': "A sudden rainstorm during competition tests the band's adaptability and their coded contingency plans.",
            'python_lesson': {
                'concept': 'Dictionaries (Mappings)',
                'examples': [
                    'instrument_to_sound = {"snare": "crack", "flute": "whistle"}',
                    'leaders = {"brass": "Leah", "percussion": "Elijah"}'
                ]
            }
        }
        
    def _create_week_7(self) -> Dict:
        """Week 7: "Blueprints and Bonds" (Classes)"""
        return {
            'title': "Blueprints and Bonds",
            'theme': "Creative Planning", 
            'python_concept': "Classes and Objects",
            'is_competition': False,
            'story_summary': "The team uses object-oriented programming to model band sections as classes with their own behaviors.",
            'python_lesson': {
                'concept': 'Classes (Organization and Abstraction)',
                'examples': [
                    'class InstrumentSection:',
                    '    def __init__(self, name, members):',
                    '        self.name = name',
                    '    def play(self):',
                    '        # Play music for this section'
                ]
            }
        }
        
    def _create_week_8(self) -> Dict:
        """Week 8: "Autumn Showdown" (Modules)"""
        return {
            'title': "Autumn Showdown",
            'theme': "Rising Stakes",
            'python_concept': "Modules",
            'is_competition': True,
            'story_summary': "At the state stadium, Pride of Code uses modular code to maintain complex routines with reusable components.",
            'python_lesson': {
                'concept': 'Modules (Reusing Code)',
                'examples': [
                    'from formations import *',
                    'from sections import *',
                    '# Reuse routines across different scripts'
                ]
            }
        }
        
    # Continue with weeks 9-16 following the same comprehensive pattern...
    def _create_week_9(self) -> Dict:
        """Week 9: "Calibration and Code" (Debugging & File I/O)"""
        return {
            'title': "Calibration and Code",
            'theme': "Fine-Tuning",
            'python_concept': "Debugging and File I/O",
            'is_competition': False,
            'python_lesson': {
                'concept': 'Debugging and File I/O',
                'examples': [
                    'try:',
                    '    volume_settings = open("volumes.txt").readlines()',
                    'except FileNotFoundError:',
                    '    print("Using default volume settings")'
                ]
            }
        }
        
    def _create_week_10(self) -> Dict:
        """Week 10: "Blackout Performance" (Exception Handling)"""
        return {
            'title': "Blackout Performance",
            'theme': "Overcoming Adversity",
            'python_concept': "Exception Handling",
            'is_competition': True,
            'python_lesson': {
                'concept': 'Exception Handling (Robustness)',
                'examples': [
                    'try:',
                    '    lights_on = True',
                    'except:',
                    '    lights_on = False',
                    '    band.play_backup()'
                ]
            }
        }
        
    def _create_week_11(self) -> Dict:
        """Week 11: "Symphony of Synergy" (Advanced Loops & Functions)"""
        return {
            'title': "Symphony of Synergy", 
            'theme': "Unity and Integration",
            'python_concept': "Advanced Loops and Functions",
            'is_competition': False,
            'python_lesson': {
                'concept': 'Advanced Loops and Functions',
                'examples': [
                    'for section in band.sections:',
                    '    for beat in range(16):',
                    '        section.play_note(beat)'
                ]
            }
        }
        
    def _create_week_12(self) -> Dict:
        """Week 12: "The City Parade" (APIs & Integration)"""
        return {
            'title': "The City Parade",
            'theme': "Community and Celebration", 
            'python_concept': "APIs and Integration",
            'is_competition': False,
            'python_lesson': {
                'concept': 'APIs and Integration',
                'examples': [
                    'while time < "12:00":',
                    '    play_routine()',
                    'schedule_effect("snowstorm", parade_start_time)'
                ]
            }
        }
        
    def _create_week_13(self) -> Dict:
        """Week 13: "Cutting Edge Code" (Advanced Algorithms)"""
        return {
            'title': "Cutting Edge Code",
            'theme': "Innovation and Identity",
            'python_concept': "Advanced Algorithms",
            'is_competition': False,
            'python_lesson': {
                'concept': 'Advanced Algorithms (Synchronization)',
                'examples': [
                    'while performance_running:',
                    '    play_music_beat()',
                    '    if beat % 4 == 0:',
                    '        trigger_baton_flash()'
                ]
            }
        }
        
    def _create_week_14(self) -> Dict:
        """Week 14: "Road to Championship" (Review & Integration)"""
        return {
            'title': "Road to Championship",
            'theme': "Final Preparations",
            'python_concept': "Review of All Concepts",
            'is_competition': True,
            'python_lesson': {
                'concept': 'Combined Project (Integration)',
                'examples': [
                    '# Combine all concepts: variables, loops, functions, classes, modules, exception handling'
                ]
            }
        }
        
    def _create_week_15(self) -> Dict:
        """Week 15: "The Night Before" (Final Preparations)"""
        return {
            'title': "The Night Before",
            'theme': "Reflection and Rejuvenation",
            'python_concept': "Final Preparations",
            'is_competition': False,
            'story_summary': "The team bonds one last time before the championship, sharing memories and encouragement.",
            'python_lesson': {
                'concept': 'Review and Confidence Building',
                'focus': 'No new concepts - reinforce all previous learning'
            }
        }
        
    def _create_week_16(self) -> Dict:
        """Week 16: "Championship Finale" (Triumph & Reflection)"""
        return {
            'title': "Championship Finale",
            'theme': "Triumph and Reflection", 
            'python_concept': "Culmination of All Skills",
            'is_competition': True,
            'story_summary': "The ultimate competition where every skill is tested and the season's journey culminates.",
            'python_lesson': {
                'concept': 'Grand Finale Performance',
                'focus': 'Apply all Python concepts in a championship performance'
            },
            'outcome_dialogue': {
                'win': [
                    {
                        'character': 'leah',
                        'text': "CHAMPIONS! We did it! All our hard work, all those coding lessons - they paid off!",
                        'emotion': 'triumphant',
                        'scene': 'championship_victory'
                    },
                    {
                        'character': 'elijah', 
                        'text': "CHAMPIONS! I'm starting an Ode to Joy remix on my snare drums right now!",
                        'emotion': 'ecstatic',
                        'scene': 'celebration_drumming'
                    },
                    {
                        'character': 'coach_hodge',
                        'text': "I couldn't be prouder of every single one of you. You've become true musicians and programmers!",
                        'emotion': 'proud',
                        'scene': 'coach_speech'
                    }
                ],
                'loss': [
                    {
                        'character': 'leah',
                        'text': "Runner-up... but we gave it everything we had. I'm proud of how far we've come.",
                        'emotion': 'gracious',
                        'scene': 'honorable_defeat'
                    },
                    {
                        'character': 'alex',
                        'text': "We may not have the trophy, but we gained something more valuable - unbreakable bonds and incredible skills.",
                        'emotion': 'reflective',
                        'scene': 'wisdom'
                    }
                ]
            }
        }
        
    def get_all_weeks_summary(self) -> List[Dict]:
        """Get a summary of all weeks for overview displays."""
        summary = []
        for week_num in range(1, 17):
            week_content = self.weeks.get(week_num, {})
            summary.append({
                'week': week_num,
                'title': week_content.get('title', f'Week {week_num}'),
                'theme': week_content.get('theme', ''),
                'concept': week_content.get('python_concept', ''),
                'is_competition': week_content.get('is_competition', False)
            })
        return summary
        
    def get_competition_weeks(self) -> List[int]:
        """Get list of all competition week numbers."""
        return [week_num for week_num, content in self.weeks.items() 
                if content.get('is_competition', False)]
                
    def get_lesson_progression(self) -> List[str]:
        """Get the progression of Python concepts through the 16 weeks."""
        return [content.get('python_concept', '') for content in self.weeks.values()]
        
    def save_to_file(self, filename: str):
        """Save the complete week content to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.weeks, f, indent=2)
            
    def load_from_file(self, filename: str):
        """Load week content from a JSON file."""
        with open(filename, 'r') as f:
            self.weeks = json.load(f)


# Utility function to create the week content system
def create_week_content_system() -> WeekContent:
    """Create and return a fully initialized week content system."""
    return WeekContent()