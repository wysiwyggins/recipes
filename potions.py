import random
import markovify
import spacy
import string
import tracery
from tracery.modifiers import base_english

def latex_escape(text):
    special_chars = {
        '&':  r'\&',
        '%':  r'\%',
        '$':  r'\$',
        '#':  r'\#',
        '_':  r'\_',
        '{':  r'\{',
        '}':  r'\}',
        '~':  r'\textasciitilde{}',
        '^':  r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for char, escaped_char in special_chars.items():
        text = text.replace(char, escaped_char)
    return text

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Installing...")
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["{}::{}".format(word.text, word.pos_) for word in nlp(sentence)]
    
    def word_join(self, words):
        tokens = [word_pos.split("::")[0] for word_pos in words]
        sentence = ""
        for i, token in enumerate(tokens):
            if i == 0:
                sentence += token
            else:
                prev_token = tokens[i - 1]
                if token in string.punctuation:
                    sentence += token
                elif prev_token in string.punctuation:
                    sentence += " " + token
                else:
                    sentence += " " + token
        return sentence

# Function to generate random measurements
def generate_measurement():
    measurement_units = {
        'cup': {'min': 0.25, 'max': 4, 'step': 0.25, 'fractional': True},
        'tablespoon': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'ampoule': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'syringe': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'drop': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'shake': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'handful': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'mouthful': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'teaspoon': {'min': 1, 'max': 20, 'step': 1, 'fractional': False},
        'gram': {'min': 10, 'max': 1000, 'step': 10, 'fractional': False},
        'ml': {'min': 5, 'max': 500, 'step': 5, 'fractional': False},
        'portion': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
        'piece': {'min': 1, 'max': 10, 'step': 1, 'fractional': False},
    }
    special_measurements = ['a pinch of', 'half a']
    measurement_choice = random.choice(['quantity'] * 4 + ['special'])  # Increase the chance of 'quantity'

    if measurement_choice == 'special':
        special = random.choice(special_measurements)
        if special == 'half a':
            unit = random.choice(['cup', 'tablespoon', 'teaspoon', 'portion', 'piece'])
            return f"Half a {unit}"
        else:
            return special
    else:
        unit = random.choice(list(measurement_units.keys()))
        unit_info = measurement_units[unit]
        min_val = unit_info['min']
        max_val = unit_info['max']
        step = unit_info['step']
        fractional = unit_info['fractional']
        num_steps = int((max_val - min_val) / step) + 1
        step_choice = random.randint(0, num_steps - 1)
        quantity = min_val + step_choice * step

        # Format quantity
        if fractional and quantity % 1 != 0:
            fraction_map = {0.25: '1/4', 0.5: '1/2', 0.75: '3/4'}
            whole_part = int(quantity)
            fractional_part = quantity - whole_part
            if fractional_part in fraction_map:
                fraction_str = fraction_map[fractional_part]
                if whole_part == 0:
                    quantity_str = fraction_str
                else:
                    quantity_str = f"{whole_part} {fraction_str}"
            else:
                quantity_str = str(quantity)
        else:
            quantity_str = str(int(quantity)) if quantity % 1 == 0 else str(quantity)

        # Pluralize unit if necessary
        if unit in ['cup', 'tablespoon', 'teaspoon', 'slice', 'piece', 'ampoule', 'syringe', 'drop', 'shake', 'handful', 'mouthful', 'portion']:
            if quantity == 1:
                unit_str = unit
            else:
                unit_str = unit + 's'
        else:
            unit_str = unit

        return f"{quantity_str} {unit_str}"

with open('ingredients/colors.txt', 'r') as f:
    colors = [line.strip() for line in f if line.strip()]

with open('ingredients/reagents.txt', 'r') as f:
#    raw_reagents = [line.strip() for line in f if line.strip()]
    reagents = [line.strip() for line in f if line.strip()]

# Process reagents to normalize capitalization, NOT WORKING!
""" def process_reagents(reagents_list):
    processed_reagents = []
    for reagent in reagents_list:
        # Create a context sentence
        sentence = f"I need {reagent}."
        # Parse the sentence with SpaCy
        doc = nlp(sentence)
        # Extract the tokens corresponding to the reagent
        # Tokens after 'need' and before the period
        reagent_tokens = [token for token in doc if token.i > 1 and token.i < len(doc) - 1]
        # Process the reagent tokens
        processed_tokens = []
        for token in reagent_tokens:
            if token.pos_ != 'PROPN':
                # If not a proper noun, lowercase the word
                processed_tokens.append(token.text.lower())
            else:
                # Keep the original casing for proper nouns
                processed_tokens.append(token.text)
        # Reconstruct the reagent name
        processed_reagent = ' '.join(processed_tokens)
        processed_reagents.append(processed_reagent)
    return processed_reagents

reagents = process_reagents(raw_reagents) """

with open('ingredients/effects.txt', 'r') as f:
    effects_text = f.read()

with open('ingredients/skills.txt', 'r') as f:
    skills = [line.strip() for line in f if line.strip()]

with open('ingredients/adjectives.txt', 'r') as f:
    adjectives = [line.strip() for line in f if line.strip()]

with open('ingredients/steps.txt', 'r') as f:
    step_templates = [line.strip() for line in f if line.strip()]

with open('ingredients/color_potion_origins.txt', 'r') as f:
    color_potion_origins = [line.strip() for line in f if line.strip()]

with open('ingredients/skill_potion_origins.txt', 'r') as f:
    skill_potion_origins = [line.strip() for line in f if line.strip()]

text_model = POSifiedText(effects_text, state_size=2)

num_pages = 100 

base_grammar_rules = {
    'adjective': adjectives,
    'time_phrase': [
        'until it is quite soft', 'overnight', 'an hour', 'for two days', 'until dawn', 'during the witching hour'
    ],
    'action_verb': [
        'soak', 'pour', 'place', 'feed', 'clean', 'add', 'combine', 'toast', 'freeze', 'grind', 'chant over',
        'expose', 'mix', 'infuse', 'steep', 'engrave', 'whisper to', 'distill', 'submerge', 'freeze', 'suspend',
        'ferment', 'immerse', 'boil', 'tie', 'paint', 'write on', 'dip', 'sing to', 'bathe'
    ],
    'container': [
        'bowl', 'flask', 'cauldron', 'pot', 'vessel', 'chalice', 'urn', 'crucible', 'goblet'
    ],
    'location': [
        'in the sun', 'under the moonlight', 'in a deep, glacial cave', 'near a roaring fire',
        'at the top of a mountain', 'beside a tranquil lake', 'within a stone circle', 'under the stars'
    ],
    'adverb': [
        'quickly', 'slowly', 'carefully', 'gently', 'thoroughly', 'delicately', 'boldly', 'secretly'
    ],
    'smell_adjective': [
        'pungent', 'fragrant', 'aromatic', 'odorous', 'malodorous', 'musky', 'sweet', 'acrid'
    ],
    'random_element': [
        'fire', 'water', 'earth', 'air', 'spirit', 'lightning', 'shadow'
    ],
    'color': colors,
    'animal': [
        'wolf', 'eagle', 'serpent', 'stag', 'phoenix', 'pangolin', 'unicorn', 'raven', 'armadillo', 'kiwi'
    ],
    'celestial_event': [
        'a solar eclipse', 'a meteor shower', 'the comet’s passing', 'the alignment of the planets', 'true night'
    ],
}

with open('recipe_book.tex', 'w') as f:
    f.write('\\documentclass{article}\n')
    f.write('\\usepackage[margin=1in]{geometry}\n')
    f.write('\\title{The Grand Grimoire of Potions}\n')
    f.write('\\author{Wiley Wiggins, Generated for NaNoGenMo 2024}\n')
    f.write('\\date{}\n')

    f.write('\\begin{document}\n\n')
    f.write('\\maketitle\n\n')
    
    generated_sentences = set()
    recipe_names = []

    for page_num in range(1, num_pages+1):
        name_choice = random.choice(['color'] * 7 + ['skill'] * 3)  # 70% color, 30% skill
        if name_choice == 'color':
            recipe_word = random.choice(colors)
            recipe_name = recipe_word.title() + ' Potion'
            word_type = 'color'
        else:
            recipe_word = random.choice(skills)
            recipe_name = 'Potion of ' + recipe_word.title()
            word_type = 'skill'
        recipe_name = latex_escape(recipe_name)

        if recipe_name in recipe_names:
            continue
        recipe_names.append(recipe_name)

        num_ingredients = random.randint(3, 8)
        ingredients_list = []
        ingredient_details = []
        for _ in range(num_ingredients):
            measurement = generate_measurement()
            ingredient = random.choice(reagents)
            ingredients_list.append(latex_escape(f"{measurement} {ingredient}"))
            ingredient_details.append({'measurement': measurement, 'ingredient': ingredient})

        num_sentences = random.randint(2, 3)
        sentences = []

        grammar_rules = base_grammar_rules.copy()
        grammar_rules.update({
            'origin': color_potion_origins if word_type == 'color' else skill_potion_origins,
            'word': recipe_word.lower(),
        })

        grammar = tracery.Grammar(grammar_rules)
        grammar.add_modifiers(base_english)

        tracery_sentence = grammar.flatten('#origin#')
        sentences.append(tracery_sentence)

        for _ in range(num_sentences - 1):
            sentence = None
            tries = 0
            while sentence is None and tries < 100:
                sentence = text_model.make_sentence(tries=100, test_output=True)
                if sentence and sentence in generated_sentences:
                    sentence = None
                tries += 1
            if sentence:
                sentence = sentence.capitalize()
                sentences.append(sentence)
                generated_sentences.add(sentence)

        effects_paragraph = latex_escape(' '.join(sentences))
        steps = []
        for i, ingredient_detail in enumerate(ingredient_details):
            if i < len(ingredient_details) - 1:
                next_ingredient_detail = ingredient_details[i + 1]
                next_measurement = next_ingredient_detail['measurement']
                next_ingredient = next_ingredient_detail['ingredient']
            else:
                next_measurement = ''
                next_ingredient = 'the mixture' 

            current_step_grammar_rules = grammar_rules.copy()
            current_step_grammar_rules['measurement'] = [ingredient_detail['measurement']]
            current_step_grammar_rules['ingredient'] = [ingredient_detail['ingredient']]
            current_step_grammar_rules['next_measurement'] = [next_measurement]
            current_step_grammar_rules['next_ingredient'] = [next_ingredient]
            current_step_grammar_rules['origin'] = step_templates  # Add the step templates to the grammar

            step_grammar = tracery.Grammar(current_step_grammar_rules)
            step_grammar.add_modifiers(base_english)

            step = step_grammar.flatten('#origin#')
            steps.append(step)

        f.write('\\newpage\n')
        f.write(f'\\section*{{{recipe_name}}}\n\n')
        f.write('\\addcontentsline{toc}{section}{' + recipe_name + '}\n')
        f.write('\\textbf{Ingredients:}\n\n')
        f.write('\\begin{itemize}\n')
        for ingredient in ingredients_list:
            f.write(f'  \\item {ingredient}\n')
        f.write('\\end{itemize}\n\n')

        f.write('\\textbf{Instructions:}\n\n')
        f.write('\\begin{enumerate}\n')
        for step in steps:
            f.write(f'  \\item {latex_escape(step)}\n')
        f.write('\\end{enumerate}\n\n')

        f.write('\\textbf{Effects:}\n\n')
        f.write(f'{effects_paragraph}\n\n')

    f.write('\\end{document}\n')
