from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import json
import os
import random
import requests
from datetime import datetime, timedelta
import hashlib

# ==================== CONFIGURATION & SECURITY ====================

# For demo purposes - in production, use environment variables
OPENAI_API_KEY = "your-openai-api-key-here"  # Replace with actual key
API_TIMEOUT = 30

# User session management
USER_SESSIONS = JsonStore('user_sessions.json')
CURRENT_SESSION_KEY = 'current_session'

# ==================== COMPREHENSIVE DATASETS ====================

YOGA_POSES_DATABASE = {
    "back_pain": {
        "beginner": [
            "Cat-Cow Pose (Marjaryasana-Bitilasana) - 10 reps",
            "Child's Pose (Balasana) - hold 30 seconds",
            "Downward-Facing Dog (Adho Mukha Svanasana) - hold 20 seconds",
            "Bridge Pose (Setu Bandhasana) - hold 15 seconds, 3 reps",
            "Knee-to-Chest Pose (Apanasana) - 10 reps each side"
        ],
        "benefits": "Improves spinal flexibility, strengthens back muscles, relieves tension"
    },
    "stress": {
        "beginner": [
            "Legs-Up-the-Wall Pose (Viparita Karani) - 5 minutes",
            "Corpse Pose (Savasana) - 10 minutes",
            "Easy Pose (Sukhasana) with meditation - 15 minutes",
            "Alternate Nostril Breathing (Nadi Shodhana) - 5 minutes"
        ],
        "benefits": "Reduces cortisol levels, calms nervous system, improves mental clarity"
    },
    "weight_loss": {
        "beginner": [
            "Sun Salutations (Surya Namaskar) - 5 rounds",
            "Warrior II (Virabhadrasana II) - hold 30 seconds each side",
            "Chair Pose (Utkatasana) - hold 20 seconds, 3 reps",
            "Boat Pose (Navasana) - hold 15 seconds, 3 reps"
        ],
        "benefits": "Boosts metabolism, builds lean muscle, improves circulation"
    }
}

EMERGENCY_DATABASE = {
    "heart_attack": {
        "symptoms": ["Chest pain", "Shortness of breath", "Nausea", "Cold sweat", "Pain in arms/jaw"],
        "actions": [
            "Call emergency services immediately (911/112)",
            "Have person sit down and rest",
            "Loosen tight clothing",
            "Give aspirin if available and no allergies",
            "Monitor breathing and consciousness"
        ]
    },
    "stroke": {
        "symptoms": ["Face drooping", "Arm weakness", "Speech difficulty", "Vision problems"],
        "actions": [
            "Call emergency services immediately",
            "Note time when symptoms started",
            "Have person lie down with head elevated",
            "Do not give food or drink"
        ]
    },
    "choking": {
        "symptoms": ["Unable to speak", "Difficulty breathing", "Clutching throat", "Blue lips"],
        "actions": [
            "Perform Heimlich maneuver",
            "Call emergency services",
            "Encourage coughing if possible",
            "Back blows between shoulder blades"
        ]
    }
}

DIET_PLANS = {
    "weight_loss": {
        "breakfast": "Oatmeal with berries and nuts (300 cal)",
        "lunch": "Grilled chicken salad with olive oil (400 cal)",
        "dinner": "Baked fish with steamed vegetables (450 cal)",
        "snacks": "Greek yogurt, apple (200 cal)"
    },
    "muscle_gain": {
        "breakfast": "Protein pancakes with banana (500 cal)",
        "lunch": "Chicken breast with brown rice (600 cal)",
        "dinner": "Salmon with sweet potato (550 cal)",
        "snacks": "Cottage cheese, nuts (300 cal)"
    },
    "diabetes": {
        "breakfast": "Scrambled eggs with spinach (250 cal)",
        "lunch": "Quinoa salad with lean protein (350 cal)",
        "dinner": "Grilled fish with non-starchy vegetables (400 cal)",
        "snacks": "Handful of nuts, cucumber slices (150 cal)"
    }
}

# ==================== AYURVEDIC DATABASE ====================

AYURVEDIC_DATABASE = {
    "doshas": {
        "vata": {
            "name": "Vata Dosha",
            "elements": ["Air", "Ether"],
            "qualities": ["Dry", "Light", "Cold", "Rough", "Subtle", "Mobile", "Clear"],
            "characteristics": [
                "Creative and energetic",
                "Quick learning but quick forgetting",
                "Irregular appetite and digestion",
                "Light sleeper, tendency to insomnia",
                "Enthusiasm, imagination, flexibility"
            ],
            "imbalance_symptoms": [
                "Anxiety, worry, nervousness",
                "Dry skin and hair",
                "Constipation, gas, bloating",
                "Fatigue, weakness",
                "Joint pain, cracking joints"
            ],
            "balancing_foods": [
                "Warm, cooked foods",
                "Sweet, sour, and salty tastes",
                "Nuts, seeds, avocados",
                "Root vegetables",
                "Whole grains like oats and rice"
            ],
            "avoid_foods": [
                "Cold foods and drinks",
                "Raw vegetables",
                "Beans, cabbage, broccoli",
                "Dry, light foods like popcorn"
            ],
            "lifestyle_tips": [
                "Maintain regular routine",
                "Stay warm and moist",
                "Gentle, grounding exercise",
                "Adequate rest and sleep",
                "Oil massage (abhyanga)"
            ],
            "herbs": ["Ashwagandha", "Brahmi", "Shatavari", "Ginger", "Cinnamon"]
        },
        "pitta": {
            "name": "Pitta Dosha",
            "elements": ["Fire", "Water"],
            "qualities": ["Hot", "Sharp", "Light", "Liquid", "Oily", "Spreading"],
            "characteristics": [
                "Intelligent and focused",
                "Strong digestion and appetite",
                "Medium build and strength",
                "Leadership qualities",
                "Competitive nature"
            ],
            "imbalance_symptoms": [
                "Irritability, anger",
                "Skin rashes, acne",
                "Acid reflux, heartburn",
                "Inflammation, fever",
                "Excessive criticism"
            ],
            "balancing_foods": [
                "Cool, refreshing foods",
                "Sweet, bitter, astringent tastes",
                "Cucumber, melons, coconut",
                "Leafy greens",
                "Dairy products (in moderation)"
            ],
            "avoid_foods": [
                "Spicy, oily, fried foods",
                "Sour fruits",
                "Alcohol, caffeine",
                "Red meat",
                "Hot beverages"
            ],
            "lifestyle_tips": [
                "Stay cool, avoid excessive heat",
                "Moderate exercise",
                "Practice patience and compassion",
                "Regular meal times",
                "Moonlight walks"
            ],
            "herbs": ["Amalaki", "Neem", "Brahmi", "Coriander", "Fennel"]
        },
        "kapha": {
            "name": "Kapha Dosha",
            "elements": ["Earth", "Water"],
            "qualities": ["Heavy", "Slow", "Cool", "Oily", "Smooth", "Dense", "Soft"],
            "characteristics": [
                "Strong, sturdy build",
                "Calm, loving nature",
                "Excellent endurance",
                "Slow, methodical learning",
                "Good long-term memory"
            ],
            "imbalance_symptoms": [
                "Weight gain, fluid retention",
                "Lethargy, depression",
                "Congestion, sinus issues",
                "Slow digestion",
                "Attachment, possessiveness"
            ],
            "balancing_foods": [
                "Light, dry, warm foods",
                "Pungent, bitter, astringent tastes",
                "Apples, pears, pomegranates",
                "Legumes, beans",
                "Spices like ginger, pepper"
            ],
            "avoid_foods": [
                "Heavy, oily foods",
                "Dairy, wheat",
                "Sweet, salty, sour tastes",
                "Cold foods and drinks",
                "Bananas, avocados"
            ],
            "lifestyle_tips": [
                "Regular vigorous exercise",
                "Wake up early",
                "Try new experiences",
                "Light, dry massage",
                "Stimulating environment"
            ],
            "herbs": ["Triphala", "Guggul", "Ginger", "Turmeric", "Pippali"]
        }
    },
    "herbal_remedies": {
        "digestive_issues": {
            "ginger_tea": {
                "name": "Ginger Tea",
                "ingredients": ["Fresh ginger", "Water", "Honey (optional)", "Lemon (optional)"],
                "preparation": "Boil sliced ginger in water for 10 minutes. Strain and add honey/lemon.",
                "benefits": "Improves digestion, reduces nausea, boosts immunity",
                "dosha_balance": "Balances Kapha and Vata"
            },
            "triphala": {
                "name": "Triphala Powder",
                "ingredients": ["Amla", "Bibhitaki", "Haritaki"],
                "preparation": "Mix 1 tsp in warm water before bedtime",
                "benefits": "Gentle detoxification, improves digestion, antioxidant",
                "dosha_balance": "Tridoshic - balances all three doshas"
            }
        },
        "stress_relief": {
            "ashwagandha_milk": {
                "name": "Ashwagandha Milk",
                "ingredients": ["Ashwagandha powder", "Milk", "Honey", "Cardamom"],
                "preparation": "Mix 1 tsp ashwagandha in warm milk. Add honey and cardamom.",
                "benefits": "Reduces stress, improves sleep, strengthens nervous system",
                "dosha_balance": "Balances Vata and Kapha"
            },
            "brahmi_tea": {
                "name": "Brahmi Tea",
                "ingredients": ["Brahmi leaves/powder", "Water", "Honey"],
                "preparation": "Steep brahmi in hot water for 5-7 minutes. Strain and add honey.",
                "benefits": "Calms mind, improves memory, reduces anxiety",
                "dosha_balance": "Balances all three doshas"
            }
        },
        "immunity_boost": {
            "turmeric_golden_milk": {
                "name": "Golden Milk",
                "ingredients": ["Turmeric", "Milk", "Honey", "Black pepper", "Ghee"],
                "preparation": "Mix turmeric and black pepper in warm milk. Add ghee and honey.",
                "benefits": "Anti-inflammatory, boosts immunity, improves joint health",
                "dosha_balance": "Balances Kapha and Vata"
            },
            "tulsi_tea": {
                "name": "Holy Basil Tea",
                "ingredients": ["Fresh tulsi leaves", "Water", "Honey", "Ginger"],
                "preparation": "Boil tulsi leaves and ginger in water for 10 minutes. Strain and add honey.",
                "benefits": "Powerful antioxidant, respiratory health, stress relief",
                "dosha_balance": "Balances all three doshas"
            }
        }
    },
    "daily_routines": {
        "morning": [
            "Wake up before sunrise",
            "Drink warm water with lemon",
            "Oil pulling with sesame oil",
            "Nasya (nasal oil drops)",
            "Abhyanga (self-massage)",
            "Yoga and meditation",
            "Light breakfast"
        ],
        "afternoon": [
            "Main meal at noon when digestion is strongest",
            "Short walk after eating",
            "Stay hydrated with room temperature water",
            "Avoid napping during the day"
        ],
        "evening": [
            "Light, early dinner",
            "Gentle walk after dinner",
            "Digital detox 1 hour before bed",
            "Warm oil foot massage",
            "Meditation or reading",
            "Early to bed (by 10 PM)"
        ]
    }
}


# ==================== API SERVICES ====================

class OpenAIService:
    """Service for OpenAI API integration"""

    @staticmethod
    def get_yoga_advice(question, user_context=""):
        """
        Get AI-powered yoga advice using OpenAI API
        """
        try:
            # For demo purposes - simulate API response
            prompt = f"""
            As a certified yoga instructor, provide personalized yoga advice.

            User Context: {user_context}
            Question: {question}

            Please provide:
            1. Specific yoga poses recommended
            2. Duration and frequency
            3. Precautions based on user context
            4. Expected benefits

            Format the response in a clear, structured way.
            """

            # Simulated API response
            responses = {
                "back pain": f"""🧘 Yoga for Back Pain Relief 🧘

Based on your profile {user_context}, here's my recommendation:

Recommended Poses:
1. Cat-Cow Pose - 10 repetitions daily
2. Child's Pose - Hold for 30 seconds, 3 times
3. Downward Dog - Hold for 20 seconds, 3 times
4. Bridge Pose - Hold for 15 seconds, 5 repetitions

Frequency: Practice daily in the morning
Precautions: Avoid forward bends if acute pain
Benefits: Improved spinal flexibility, reduced tension

💡 Tip: Combine with proper posture throughout the day.""",

                "stress": f"""😌 Yoga for Stress Relief 😌

Based on your profile {user_context}, here's my recommendation:

Recommended Practices:
1. Legs-Up-The-Wall Pose - 5-10 minutes daily
2. Alternate Nostril Breathing - 5 minutes
3. Corpse Pose with deep breathing - 10 minutes
4. Gentle forward bends

Frequency: Practice twice daily
Precautions: Focus on breath awareness
Benefits: Reduced anxiety, better sleep, mental clarity

💡 Tip: Practice before bed for better sleep.""",

                "default": f"""🌟 Personalized Yoga Advice 🌟

Based on your query about "{question}" and your profile {user_context}:

General Recommendation:
1. Start with basic breathing exercises
2. Incorporate gentle stretching
3. Practice consistently for best results
4. Listen to your body's limits

Suggested Poses:
• Mountain Pose for grounding
• Easy Pose for meditation
• Gentle twists for mobility

Frequency: 15-20 minutes daily
Precautions: Consult doctor if you have health concerns

💡 Remember: Consistency is key in yoga practice."""
            }

            # Find the most relevant response
            question_lower = question.lower()
            for key in responses:
                if key in question_lower:
                    return {
                        "success": True,
                        "advice": responses[key],
                        "sources": ["AI Yoga Analysis", "Medical Research"]
                    }

            return {
                "success": True,
                "advice": responses["default"],
                "sources": ["AI Yoga Analysis"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "advice": "Unable to fetch AI advice at the moment. Please try basic yoga poses and consult a professional."
            }

    @staticmethod
    def get_diet_plan(goal, user_context="", disease=""):
        """
        Get AI-powered diet plan using OpenAI API
        """
        try:
            # Simulated API response
            prompt = f"""
            Create a personalized diet plan for:
            Goal: {goal}
            Disease Considerations: {disease}
            User Context: {user_context}

            Provide:
            1. Daily meal plan with calories
            2. Specific food recommendations
            3. Foods to avoid
            4. Nutritional tips
            """

            # Simulated responses
            diet_responses = {
                "weight_loss": f"""🍽️ Weight Loss Diet Plan 🍽️

Based on your profile {user_context}:

Daily Plan (≈1500 calories):
• Breakfast: Oatmeal with berries (300 cal)
• Lunch: Grilled chicken salad (400 cal)
• Dinner: Baked fish with veggies (450 cal)
• Snacks: Greek yogurt, apple (200 cal)

Foods to Include:
- Lean proteins (chicken, fish, tofu)
- Fresh vegetables
- Whole grains
- Healthy fats

Foods to Avoid:
- Processed foods
- Sugary drinks
- White bread/pasta
- High-calorie snacks

💡 Tips: Drink plenty of water, eat slowly, and combine with exercise.""",

                "muscle_gain": f"""💪 Muscle Gain Diet Plan 💪

Based on your profile {user_context}:

Daily Plan (≈2500 calories):
• Breakfast: Protein pancakes (500 cal)
• Lunch: Chicken with brown rice (600 cal)
• Dinner: Salmon with sweet potato (550 cal)
• Snacks: Cottage cheese, nuts (300 cal)

Key Nutrients:
- Protein: 1.6-2.2g per kg body weight
- Complex carbs for energy
- Healthy fats for hormone production

Meal Timing:
- Eat every 3-4 hours
- Protein within 30 mins after workout
- Stay hydrated

💡 Tips: Focus on progressive overload in training."""
            }

            response_key = goal.lower().replace(" ", "_")
            if response_key in diet_responses:
                advice = diet_responses[response_key]
            else:
                advice = diet_responses["weight_loss"]

            if disease:
                advice += f"\n\n🏥 Special Considerations for {disease}:\n- Consult with healthcare provider\n- Monitor specific nutrient needs\n- Adjust based on medical advice"

            return {
                "success": True,
                "advice": advice,
                "sources": ["AI Nutrition Analysis"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "advice": "Unable to generate diet plan at the moment. Please try basic dietary guidelines."
            }


class EmergencyAPIService:
    """Service for emergency information"""

    @staticmethod
    def search_emergency_info(query):
        """
        Search emergency database for information
        """
        try:
            query_lower = query.lower()
            results = []

            for condition, data in EMERGENCY_DATABASE.items():
                if (query_lower in condition.lower() or
                        any(query_lower in symptom.lower() for symptom in data["symptoms"])):
                    results.append({
                        "condition": condition.replace("_", " ").title(),
                        "symptoms": data["symptoms"],
                        "actions": data["actions"]
                    })

            if results:
                return {
                    "success": True,
                    "results": results,
                    "count": len(results)
                }
            else:
                return {
                    "success": True,
                    "results": [{
                        "condition": "General Emergency Advice",
                        "symptoms": ["Multiple possible symptoms"],
                        "actions": [
                            "Call emergency services immediately",
                            "Stay calm and assess the situation",
                            "Provide first aid if trained",
                            "Monitor vital signs",
                            "Do not move injured person unnecessarily"
                        ]
                    }],
                    "count": 1
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class AyurvedicService:
    """Service for Ayurvedic calculations and recommendations"""

    @staticmethod
    def calculate_dosha_quiz(answers):
        """
        Calculate dosha predominance based on quiz answers
        """
        scores = {"vata": 0, "pitta": 0, "kapha": 0}

        # Scoring logic based on answers
        for answer in answers:
            if answer in ["a", "1"]:  # Vata characteristics
                scores["vata"] += 1
            elif answer in ["b", "2"]:  # Pitta characteristics
                scores["pitta"] += 1
            elif answer in ["c", "3"]:  # Kapha characteristics
                scores["kapha"] += 1

        # Determine primary dosha
        max_score = max(scores.values())
        primary_dosha = [dosha for dosha, score in scores.items() if score == max_score][0]

        return {
            "primary_dosha": primary_dosha,
            "scores": scores,
            "description": AYURVEDIC_DATABASE["doshas"][primary_dosha]
        }

    @staticmethod
    def get_dosha_recommendations(dosha_type, concern=""):
        """
        Get personalized recommendations based on dosha type
        """
        dosha_data = AYURVEDIC_DATABASE["doshas"][dosha_type]

        recommendations = {
            "diet": dosha_data["balancing_foods"],
            "lifestyle": dosha_data["lifestyle_tips"],
            "herbs": dosha_data["herbs"],
            "avoid": dosha_data["avoid_foods"]
        }

        if concern and concern in AYURVEDIC_DATABASE["herbal_remedies"]:
            recommendations["remedies"] = AYURVEDIC_DATABASE["herbal_remedies"][concern]

        return recommendations

    @staticmethod
    def get_daily_routine():
        """Get Ayurvedic daily routine (Dinacharya)"""
        return AYURVEDIC_DATABASE["daily_routines"]


# ==================== ANIMATED WIDGETS ====================

class AnimatedButton(Button):
    """Custom button with animation effects"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.6, 0.8, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = '16sp'
        self.bold = True

    def on_press(self):
        # Color animation on press instead of scale
        original_color = self.background_color
        anim = Animation(background_color=(0.9, 0.9, 0.9, 1), duration=0.1) + \
               Animation(background_color=original_color, duration=0.1)
        anim.start(self)
        super().on_press()


# ==================== SCREENS ====================

class LoginScreen(Screen):
    """Login screen with user authentication"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Main layout with gradient background
        main_layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))

        with main_layout.canvas.before:
            Color(0.1, 0.3, 0.5, 1)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self.update_bg, size=self.update_bg)

        # App logo/title
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        title_label = Label(
            text='Health & Wellness\nAssistant',
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='center'
        )
        title_layout.add_widget(title_label)
        main_layout.add_widget(title_layout)

        # Login form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, 0.7))

        # Gender selection
        gender_label = Label(text='Gender:', font_size='18sp', color=(1, 1, 1, 1))
        form_layout.add_widget(gender_label)

        gender_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, None), height=dp(50))
        self.gender_btns = {}

        for gender in ['Male', 'Female']:
            btn = ToggleButton(
                text=gender,
                group='gender',
                background_normal='',
                background_color=(0.3, 0.5, 0.7, 0.7)
            )
            self.gender_btns[gender] = btn
            gender_layout.add_widget(btn)
        form_layout.add_widget(gender_layout)

        # Age input
        age_label = Label(text='Age:', font_size='18sp', color=(1, 1, 1, 1))
        form_layout.add_widget(age_label)
        self.age_input = TextInput(
            hint_text='Enter your age',
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            font_size='18sp',
            input_type='number'
        )
        form_layout.add_widget(self.age_input)

        # Weight input
        weight_label = Label(text='Weight (kg):', font_size='18sp', color=(1, 1, 1, 1))
        form_layout.add_widget(weight_label)
        self.weight_input = TextInput(
            hint_text='Enter your weight in kg',
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            font_size='18sp',
            input_type='number'
        )
        form_layout.add_widget(self.weight_input)

        # Login button
        login_btn = AnimatedButton(
            text='Start Health Journey',
            size_hint=(1, None),
            height=dp(60),
            background_color=(0.2, 0.8, 0.4, 1)
        )
        login_btn.bind(on_press=self.login)
        form_layout.add_widget(login_btn)

        main_layout.add_widget(form_layout)
        self.add_widget(main_layout)

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def login(self, instance):
        # Get user data
        gender = next((g for g, btn in self.gender_btns.items() if btn.state == 'down'), None)
        age = self.age_input.text.strip()
        weight = self.weight_input.text.strip()

        # Validate inputs
        if not all([gender, age, weight]):
            self.show_error("Please fill all fields")
            return

        if not age.isdigit() or not weight.replace('.', '').isdigit():
            self.show_error("Please enter valid numbers for age and weight")
            return

        # Create user session
        user_data = {
            'gender': gender,
            'age': age,
            'weight': weight,
            'login_time': datetime.now().isoformat(),
            'session_id': hashlib.sha256(f"{gender}{age}{weight}{datetime.now()}".encode()).hexdigest()[:16]
        }

        # Store session
        USER_SESSIONS.put(CURRENT_SESSION_KEY, **user_data)

        # Set current user in app
        app = App.get_running_app()
        app.current_user = user_data

        # Navigate to home with animation
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'home'

    def show_error(self, message):
        # Remove any existing error labels
        for child in self.children[:]:
            if isinstance(child, Label) and child.color == [1, 0.3, 0.3, 1]:
                self.remove_widget(child)

        error_label = Label(
            text=message,
            color=(1, 0.3, 0.3, 1),
            font_size='16sp',
            size_hint=(1, None),
            height=dp(40)
        )
        self.add_widget(error_label)

        # Remove error message after 3 seconds
        Clock.schedule_once(lambda dt: self.remove_widget(error_label), 3)


class HomeScreen(Screen):
    """Main home screen with feature buttons"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Header with user info and logout
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))

        self.user_info = Label(
            text='Health Assistant',
            font_size='20sp',
            color=(0.2, 0.4, 0.6, 1),
            bold=True,
            size_hint=(0.7, 1)
        )

        logout_btn = AnimatedButton(
            text='Logout',
            size_hint=(0.3, 0.8),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        logout_btn.bind(on_press=self.logout)

        header_layout.add_widget(self.user_info)
        header_layout.add_widget(logout_btn)
        main_layout.add_widget(header_layout)

        # Feature buttons grid
        grid_layout = GridLayout(cols=2, spacing=dp(15), size_hint=(1, 0.8))

        features = [
            ('Emergency\nHelp', (1, 0.3, 0.3, 1), 'emergency'),
            ('Ayurvedic', (0.8, 0.6, 0.2, 1), 'ayurvedic'),
            ('Homeopathy', (0.6, 0.8, 0.4, 1), 'homeopathy'),
            ('AI Assistant', (0.3, 0.5, 0.8, 1), 'ai'),
            ('Yoga', (0.3, 0.7, 0.3, 1), 'yoga'),
            ('Diet Plan', (0.4, 0.3, 0.8, 1), 'diet')
        ]

        for text, color, screen in features:
            btn = AnimatedButton(
                text=text,
                background_color=color
            )
            btn.screen_name = screen
            btn.bind(on_press=self.navigate_to_feature)
            grid_layout.add_widget(btn)

        main_layout.add_widget(grid_layout)
        self.add_widget(main_layout)

    def on_enter(self):
        # Update user info when screen enters
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            user = app.current_user
            self.user_info.text = f"Welcome!\n{user['gender']}, {user['age']} years"

    def navigate_to_feature(self, instance):
        screen_name = instance.screen_name
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = screen_name

    def logout(self, instance):
        # Clear user session
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            if USER_SESSIONS.exists(CURRENT_SESSION_KEY):
                USER_SESSIONS.delete(CURRENT_SESSION_KEY)
            app.current_user = None

        # Navigate back to login
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


class AyurvedicScreen(Screen):
    """Comprehensive Ayurvedic screen matching the SVG design"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quiz_answers = []
        self.current_question = 0
        self.setup_ui()

    def setup_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = self.create_header('Ayurvedic Wellness', 'home')
        main_layout.add_widget(header)

        # Tab buttons
        tab_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        self.dosha_tab = ToggleButton(text='Dosha Quiz', group='ayurvedic_tabs', state='down')
        self.herbs_tab = ToggleButton(text='Herbal Remedies', group='ayurvedic_tabs')
        self.routine_tab = ToggleButton(text='Daily Routine', group='ayurvedic_tabs')
        self.analysis_tab = ToggleButton(text='Dosha Analysis', group='ayurvedic_tabs')

        self.dosha_tab.bind(on_press=self.show_dosha_quiz)
        self.herbs_tab.bind(on_press=self.show_herbal_remedies)
        self.routine_tab.bind(on_press=self.show_daily_routine)
        self.analysis_tab.bind(on_press=self.show_dosha_analysis)

        tab_layout.add_widget(self.dosha_tab)
        tab_layout.add_widget(self.herbs_tab)
        tab_layout.add_widget(self.routine_tab)
        tab_layout.add_widget(self.analysis_tab)
        main_layout.add_widget(tab_layout)

        # Content area
        self.content_scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.content_scroll.add_widget(self.content_layout)
        main_layout.add_widget(self.content_scroll)

        self.add_widget(main_layout)
        self.show_dosha_quiz()

    def create_header(self, title, back_screen):
        """Create standardized header with back button"""
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        back_btn = AnimatedButton(
            text='← Back',
            size_hint=(0.2, 0.8),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', back_screen))

        title_label = Label(
            text=title,
            font_size='20sp',
            bold=True,
            color=(0.2, 0.4, 0.6, 1),
            size_hint=(0.8, 1)
        )

        header.add_widget(back_btn)
        header.add_widget(title_label)
        return header

    def show_dosha_quiz(self, instance=None):
        """Show dosha quiz section"""
        self.content_layout.clear_widgets()

        welcome_label = Label(
            text='🌿 Discover Your Ayurvedic Constitution 🌿',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=(0.1, 0.5, 0.2, 1)
        )
        self.content_layout.add_widget(welcome_label)

        description = Label(
            text='Take this quiz to discover your dominant dosha and receive personalized Ayurvedic recommendations for optimal health and balance.',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(80),
            text_size=(None, None),
            valign='top'
        )
        self.content_layout.add_widget(description)

        # Start quiz button
        start_btn = AnimatedButton(
            text='Start Dosha Quiz',
            size_hint=(1, None),
            height=dp(60),
            background_color=(0.2, 0.6, 0.3, 1)
        )
        start_btn.bind(on_press=self.start_quiz)
        self.content_layout.add_widget(start_btn)

        # Quiz explanation
        explanation = Label(
            text='\nWhat are Doshas?\n\n• Vata (Air+Ether): Creativity, movement\n• Pitta (Fire+Water): Transformation, metabolism\n• Kapha (Earth+Water): Structure, stability\n\nUnderstanding your dosha helps you make lifestyle choices that maintain balance and prevent disease.',
            font_size='13sp',
            size_hint=(1, None),
            height=dp(200),
            text_size=(None, None),
            valign='top'
        )
        self.content_layout.add_widget(explanation)

    def start_quiz(self, instance):
        """Start the dosha quiz"""
        self.quiz_answers = []
        self.current_question = 0
        self.show_quiz_question()

    def show_quiz_question(self):
        """Display current quiz question"""
        self.content_layout.clear_widgets()

        questions = [
            {
                "question": "1. What best describes your body frame?",
                "options": {
                    "a": "Light, thin, prominent bones",
                    "b": "Medium, muscular, well-proportioned",
                    "c": "Large, solid, well-padded"
                }
            },
            {
                "question": "2. How is your skin typically?",
                "options": {
                    "a": "Dry, thin, cool, rough",
                    "b": "Warm, oily, sensitive, reddish",
                    "c": "Thick, oily, cool, soft"
                }
            },
            {
                "question": "3. What describes your hair?",
                "options": {
                    "a": "Dry, thin, brittle, dark",
                    "b": "Fine, oily, early graying",
                    "c": "Thick, oily, wavy, lustrous"
                }
            },
            {
                "question": "4. How is your appetite?",
                "options": {
                    "a": "Irregular, often forget to eat",
                    "b": "Strong, get irritable if hungry",
                    "c": "Steady, can skip meals easily"
                }
            },
            {
                "question": "5. What describes your sleep pattern?",
                "options": {
                    "a": "Light sleeper, easily disturbed",
                    "b": "Moderate, wake up hot",
                    "c": "Deep, heavy, long hours needed"
                }
            },
            {
                "question": "6. How do you handle stress?",
                "options": {
                    "a": "Worry, anxiety, nervousness",
                    "b": "Irritability, anger, frustration",
                    "c": "Avoidance, withdrawal, inaction"
                }
            },
            {
                "question": "7. What's your typical energy level?",
                "options": {
                    "a": "Bursts of energy, then fatigue",
                    "b": "Sustained, moderate energy",
                    "c": "Slow starter, steady endurance"
                }
            },
            {
                "question": "8. How is your memory?",
                "options": {
                    "a": "Quick to learn, quick to forget",
                    "b": "Sharp, focused, good retention",
                    "c": "Slow to learn, never forgets"
                }
            }
        ]

        if self.current_question < len(questions):
            question_data = questions[self.current_question]

            # Question label
            question_label = Label(
                text=question_data["question"],
                font_size='16sp',
                bold=True,
                size_hint=(1, None),
                height=dp(60),
                color=(0.2, 0.4, 0.6, 1)
            )
            self.content_layout.add_widget(question_label)

            # Progress
            progress_label = Label(
                text=f'Question {self.current_question + 1} of {len(questions)}',
                font_size='12sp',
                size_hint=(1, None),
                height=dp(30),
                color=(0.4, 0.4, 0.4, 1)
            )
            self.content_layout.add_widget(progress_label)

            # Options
            for key, option_text in question_data["options"].items():
                option_btn = AnimatedButton(
                    text=option_text,
                    size_hint=(1, None),
                    height=dp(70),
                    background_color=(0.8, 0.9, 0.8, 1)
                )
                option_btn.answer = key
                option_btn.bind(on_press=self.record_answer)
                self.content_layout.add_widget(option_btn)
        else:
            self.show_quiz_results()

    def record_answer(self, instance):
        """Record answer and move to next question"""
        self.quiz_answers.append(instance.answer)
        self.current_question += 1
        self.show_quiz_question()

    def show_quiz_results(self):
        """Calculate and display quiz results"""
        self.content_layout.clear_widgets()

        result = AyurvedicService.calculate_dosha_quiz(self.quiz_answers)
        primary_dosha = result["primary_dosha"]
        dosha_data = result["description"]

        # Result header
        result_label = Label(
            text=f'🎉 Your Ayurvedic Constitution: {dosha_data["name"]} 🎉',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=self.get_dosha_color(primary_dosha)
        )
        self.content_layout.add_widget(result_label)

        # Scores
        scores_text = f"Scores:\nVata: {result['scores']['vata']} | Pitta: {result['scores']['pitta']} | Kapha: {result['scores']['kapha']}"
        scores_label = Label(
            text=scores_text,
            font_size='14sp',
            size_hint=(1, None),
            height=dp(50)
        )
        self.content_layout.add_widget(scores_label)

        # Dosha information
        info_sections = [
            ("Elements", dosha_data["elements"]),
            ("Key Qualities", dosha_data["qualities"]),
            ("Characteristics", dosha_data["characteristics"]),
            ("Imbalance Signs", dosha_data["imbalance_symptoms"])
        ]

        for section_title, items in info_sections:
            section_label = Label(
                text=f"\n{section_title}:\n• " + "\n• ".join(items),
                font_size='13sp',
                size_hint=(1, None),
                height=len(items) * dp(20) + dp(40),
                text_size=(None, None),
                valign='top'
            )
            self.content_layout.add_widget(section_label)

        # Recommendations button
        rec_btn = AnimatedButton(
            text='Get Personalized Recommendations',
            size_hint=(1, None),
            height=dp(60),
            background_color=self.get_dosha_color(primary_dosha)
        )
        rec_btn.dosha_type = primary_dosha
        rec_btn.bind(on_press=self.show_recommendations)
        self.content_layout.add_widget(rec_btn)

        # Retake quiz button
        retake_btn = AnimatedButton(
            text='Retake Quiz',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        retake_btn.bind(on_press=lambda x: self.show_dosha_quiz())
        self.content_layout.add_widget(retake_btn)

    def get_dosha_color(self, dosha_type):
        """Get color associated with each dosha"""
        colors = {
            "vata": (0.6, 0.8, 1.0, 1),  # Light blue
            "pitta": (1.0, 0.6, 0.4, 1),  # Orange/red
            "kapha": (0.4, 0.8, 0.4, 1)  # Green
        }
        return colors.get(dosha_type, (0.5, 0.5, 0.5, 1))

    def show_recommendations(self, instance):
        """Show personalized recommendations for the dosha"""
        dosha_type = instance.dosha_type
        recommendations = AyurvedicService.get_dosha_recommendations(dosha_type)

        self.content_layout.clear_widgets()

        header = Label(
            text=f'🌿 Personalized {dosha_type.title()} Recommendations 🌿',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=self.get_dosha_color(dosha_type)
        )
        self.content_layout.add_widget(header)

        # Diet recommendations
        diet_section = self.create_recommendation_section(
            "🍽️ Balancing Diet",
            recommendations["diet"],
            "Include these foods in your diet:"
        )
        self.content_layout.add_widget(diet_section)

        # Lifestyle recommendations
        lifestyle_section = self.create_recommendation_section(
            "🌅 Daily Lifestyle",
            recommendations["lifestyle"],
            "Incorporate these practices:"
        )
        self.content_layout.add_widget(lifestyle_section)

        # Herbs recommendations
        herbs_section = self.create_recommendation_section(
            "🌿 Beneficial Herbs",
            recommendations["herbs"],
            "Consider these Ayurvedic herbs:"
        )
        self.content_layout.add_widget(herbs_section)

        # Foods to avoid
        avoid_section = self.create_recommendation_section(
            "🚫 Foods to Minimize",
            recommendations["avoid"],
            "Reduce or avoid these foods:"
        )
        self.content_layout.add_widget(avoid_section)

        # Back button
        back_btn = AnimatedButton(
            text='← Back to Results',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: self.show_quiz_results())
        self.content_layout.add_widget(back_btn)

    def create_recommendation_section(self, title, items, subtitle):
        """Create a recommendation section with title and items"""
        section = BoxLayout(orientation='vertical', size_hint=(1, None), height=len(items) * dp(25) + dp(80))

        with section.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            RoundedRectangle(pos=section.pos, size=section.size, radius=[10])

        title_label = Label(
            text=title,
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.3),
            color=(0.2, 0.4, 0.6, 1)
        )

        subtitle_label = Label(
            text=subtitle,
            font_size='12sp',
            size_hint=(1, 0.2),
            color=(0.4, 0.4, 0.4, 1)
        )

        items_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        for item in items:
            item_label = Label(
                text=f"• {item}",
                font_size='12sp',
                size_hint=(1, None),
                height=dp(25)
            )
            items_layout.add_widget(item_label)

        section.add_widget(title_label)
        section.add_widget(subtitle_label)
        section.add_widget(items_layout)

        return section

    def show_herbal_remedies(self, instance=None):
        """Show herbal remedies section"""
        self.content_layout.clear_widgets()

        header = Label(
            text='🌿 Ayurvedic Herbal Remedies 🌿',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=(0.1, 0.5, 0.2, 1)
        )
        self.content_layout.add_widget(header)

        description = Label(
            text='Traditional Ayurvedic herbal preparations for common health concerns',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(50)
        )
        self.content_layout.add_widget(description)

        # Remedy categories
        categories = [
            ("Digestive Health", "digestive_issues", "Improve digestion and gut health"),
            ("Stress Relief", "stress_relief", "Calm mind and nervous system"),
            ("Immunity Boost", "immunity_boost", "Strengthen immune function")
        ]

        for category_name, category_key, category_desc in categories:
            category_card = self.create_remedy_category_card(category_name, category_desc, category_key)
            self.content_layout.add_widget(category_card)

    def create_remedy_category_card(self, name, description, category_key):
        """Create a card for remedy category"""
        card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(120))

        with card.canvas.before:
            Color(0.9, 0.95, 0.9, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            Color(0.1, 0.5, 0.2, 0.3)
            Rectangle(pos=(card.pos[0], card.pos[1]), size=(card.size[0], dp(3)))

        name_label = Label(
            text=name,
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.4),
            color=(0.1, 0.5, 0.2, 1)
        )

        desc_label = Label(
            text=description,
            font_size='12sp',
            size_hint=(1, 0.3),
            color=(0.4, 0.4, 0.4, 1)
        )

        view_btn = AnimatedButton(
            text='View Remedies',
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 0.3, 1)
        )
        view_btn.category = category_key
        view_btn.bind(on_press=self.show_remedy_details)

        card.add_widget(name_label)
        card.add_widget(desc_label)
        card.add_widget(view_btn)

        return card

    def show_remedy_details(self, instance):
        """Show detailed information about remedies in a category"""
        category_key = instance.category
        remedies = AYURVEDIC_DATABASE["herbal_remedies"][category_key]

        self.content_layout.clear_widgets()

        back_btn = AnimatedButton(
            text='← Back to Remedies',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: self.show_herbal_remedies())
        self.content_layout.add_widget(back_btn)

        category_label = Label(
            text=f'🌿 {category_key.replace("_", " ").title()} Remedies 🌿',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=(0.1, 0.5, 0.2, 1)
        )
        self.content_layout.add_widget(category_label)

        for remedy_key, remedy_data in remedies.items():
            remedy_card = self.create_remedy_card(remedy_data)
            self.content_layout.add_widget(remedy_card)

    def create_remedy_card(self, remedy_data):
        """Create a detailed card for a herbal remedy"""
        card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(300))

        with card.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[10])

        # Name
        name_label = Label(
            text=remedy_data["name"],
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.15),
            color=(0.1, 0.5, 0.2, 1)
        )

        # Benefits
        benefits_label = Label(
            text=f"Benefits: {remedy_data['benefits']}",
            font_size='12sp',
            size_hint=(1, 0.15),
            color=(0.3, 0.5, 0.3, 1)
        )

        # Ingredients
        ingredients_label = Label(
            text="Ingredients:\n• " + "\n• ".join(remedy_data["ingredients"]),
            font_size='11sp',
            size_hint=(1, 0.25),
            text_size=(None, None),
            valign='top'
        )

        # Preparation
        prep_label = Label(
            text=f"Preparation:\n{remedy_data['preparation']}",
            font_size='11sp',
            size_hint=(1, 0.3),
            text_size=(None, None),
            valign='top'
        )

        # Dosha balance
        dosha_label = Label(
            text=f"Dosha Balance: {remedy_data['dosha_balance']}",
            font_size='11sp',
            size_hint=(1, 0.15),
            color=(0.4, 0.4, 0.4, 1)
        )

        card.add_widget(name_label)
        card.add_widget(benefits_label)
        card.add_widget(ingredients_label)
        card.add_widget(prep_label)
        card.add_widget(dosha_label)

        return card

    def show_daily_routine(self, instance=None):
        """Show Ayurvedic daily routine (Dinacharya)"""
        self.content_layout.clear_widgets()

        header = Label(
            text='🌅 Ayurvedic Daily Routine (Dinacharya) 🌅',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=(0.1, 0.5, 0.2, 1)
        )
        self.content_layout.add_widget(header)

        description = Label(
            text='A balanced daily routine is fundamental to Ayurvedic health. Follow these practices to maintain dosha balance and promote wellbeing.',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(60),
            text_size=(None, None),
            valign='top'
        )
        self.content_layout.add_widget(description)

        routine_data = AyurvedicService.get_daily_routine()

        time_sections = [
            ("🌞 Morning Routine (6AM - 12PM)", routine_data["morning"]),
            ("☀️ Afternoon Routine (12PM - 6PM)", routine_data["afternoon"]),
            ("🌙 Evening Routine (6PM - 10PM)", routine_data["evening"])
        ]

        for section_title, practices in time_sections:
            section_card = self.create_routine_section(section_title, practices)
            self.content_layout.add_widget(section_card)

    def create_routine_section(self, title, practices):
        """Create a section for daily routine practices"""
        section = BoxLayout(orientation='vertical', size_hint=(1, None), height=len(practices) * dp(30) + dp(60))

        with section.canvas.before:
            Color(0.9, 0.95, 0.9, 1)
            RoundedRectangle(pos=section.pos, size=section.size, radius=[10])

        title_label = Label(
            text=title,
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.3),
            color=(0.1, 0.5, 0.2, 1)
        )

        practices_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.7))
        for i, practice in enumerate(practices):
            practice_label = Label(
                text=f"{i + 1}. {practice}",
                font_size='12sp',
                size_hint=(1, None),
                height=dp(30)
            )
            practices_layout.add_widget(practice_label)

        section.add_widget(title_label)
        section.add_widget(practices_layout)

        return section

    def show_dosha_analysis(self, instance=None):
        """Show comprehensive dosha analysis"""
        self.content_layout.clear_widgets()

        header = Label(
            text='📊 Comprehensive Dosha Analysis 📊',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=(0.1, 0.5, 0.2, 1)
        )
        self.content_layout.add_widget(header)

        description = Label(
            text='Detailed analysis of all three doshas and their characteristics',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(50)
        )
        self.content_layout.add_widget(description)

        # Create analysis for each dosha
        for dosha_key, dosha_data in AYURVEDIC_DATABASE["doshas"].items():
            dosha_card = self.create_dosha_analysis_card(dosha_key, dosha_data)
            self.content_layout.add_widget(dosha_card)

    def create_dosha_analysis_card(self, dosha_key, dosha_data):
        """Create a comprehensive analysis card for a dosha"""
        card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(400))

        with card.canvas.before:
            Color(*self.get_dosha_color(dosha_key))
            RoundedRectangle(pos=card.pos, size=(card.size[0], dp(40)), radius=[10, 10, 0, 0])
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=(card.pos[0], card.pos[1] + dp(40)), size=(card.size[0], card.size[1] - dp(40)))

        # Header
        header_label = Label(
            text=dosha_data["name"],
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )

        # Content area
        content_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=dp(10))

        # Elements
        elements_label = Label(
            text=f"Elements: {', '.join(dosha_data['elements'])}",
            font_size='12sp',
            size_hint=(1, 0.08),
            color=(0.3, 0.3, 0.3, 1)
        )

        # Qualities
        qualities_text = "Qualities: " + ", ".join(dosha_data["qualities"])
        qualities_label = Label(
            text=qualities_text,
            font_size='11sp',
            size_hint=(1, 0.12),
            text_size=(None, None),
            valign='top'
        )

        # Characteristics
        chars_text = "Characteristics:\n• " + "\n• ".join(dosha_data["characteristics"][:3])
        chars_label = Label(
            text=chars_text,
            font_size='11sp',
            size_hint=(1, 0.25),
            text_size=(None, None),
            valign='top'
        )

        # Imbalance symptoms
        imbalance_text = "Imbalance:\n• " + "\n• ".join(dosha_data["imbalance_symptoms"][:3])
        imbalance_label = Label(
            text=imbalance_text,
            font_size='11sp',
            size_hint=(1, 0.25),
            text_size=(None, None),
            valign='top'
        )

        # Key herbs
        herbs_text = "Key Herbs:\n" + ", ".join(dosha_data["herbs"][:3])
        herbs_label = Label(
            text=herbs_text,
            font_size='11sp',
            size_hint=(1, 0.1),
            color=(0.1, 0.5, 0.2, 1)
        )

        content_layout.add_widget(elements_label)
        content_layout.add_widget(qualities_label)
        content_layout.add_widget(chars_label)
        content_layout.add_widget(imbalance_label)
        content_layout.add_widget(herbs_label)

        card.add_widget(header_label)
        card.add_widget(content_layout)

        return card


# ==================== OTHER SCREENS (Placeholders for brevity) ====================

class YogaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Yoga Features Coming Soon!', font_size='18sp'))
        back_btn = AnimatedButton(text='← Back', size_hint=(1, 0.2))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)


class EmergencyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Emergency Features Coming Soon!', font_size='18sp'))
        back_btn = AnimatedButton(text='← Back', size_hint=(1, 0.2))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)


class DietScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Diet Features Coming Soon!', font_size='18sp'))
        back_btn = AnimatedButton(text='← Back', size_hint=(1, 0.2))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)


class HomeopathyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Homeopathy Features Coming Soon!', font_size='18sp'))
        back_btn = AnimatedButton(text='← Back', size_hint=(1, 0.2))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)


class AIScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='AI Assistant Features Coming Soon!', font_size='18sp'))
        back_btn = AnimatedButton(text='← Back', size_hint=(1, 0.2))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)


# ==================== MAIN APP ====================

class HealthWellnessApp(App):
    """Main application class"""

    def build(self):
        Window.size = (400, 700)
        self.title = "Health & Wellness Assistant"

        # Initialize screen manager
        self.sm = ScreenManager()

        # Add all screens
        screens = [
            ('login', LoginScreen()),
            ('home', HomeScreen()),
            ('emergency', EmergencyScreen()),
            ('yoga', YogaScreen()),
            ('diet', DietScreen()),
            ('ayurvedic', AyurvedicScreen()),
            ('homeopathy', HomeopathyScreen()),
            ('ai', AIScreen())
        ]

        for name, screen in screens:
            screen.name = name
            self.sm.add_widget(screen)

        # Check for existing session
        self.check_existing_session()

        return self.sm

    def check_existing_session(self):
        """Check if user has an active session"""
        if USER_SESSIONS.exists(CURRENT_SESSION_KEY):
            user_data = USER_SESSIONS.get(CURRENT_SESSION_KEY)
            # Check if session is not expired (24 hours)
            login_time = datetime.fromisoformat(user_data['login_time'])
            if datetime.now() - login_time < timedelta(hours=24):
                self.current_user = user_data
                self.sm.current = 'home'
            else:
                # Session expired, delete it
                USER_SESSIONS.delete(CURRENT_SESSION_KEY)

    def on_pause(self):
        """Handle app pausing"""
        return True

    def on_resume(self):
        """Handle app resuming"""
        pass


if __name__ == '__main__':
    HealthWellnessApp().run()
