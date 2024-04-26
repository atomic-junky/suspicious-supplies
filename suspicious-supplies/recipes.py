from itertools import combinations, combinations_with_replacement
import json
import math
import os

from beet import DataPack, Recipe


f = open(f"{os.path.dirname(__file__)}/ingredients.json")
_all_ingredients = json.load(f)


def _build_recipe(_raw_ingredients) -> Recipe:
    _ingredients = []
    for ing in _raw_ingredients:
        type = "item"
        if ing.startswith("#"):
            type = "tag"
            
        _ingredients.append({
            type: ing.removeprefix("#")
        })
    
    return Recipe(
        json.dumps(
            {
                "type": "minecraft:crafting_shapeless",
                "ingredients": _ingredients,
                "category": "food",
                "group": "suspicious_food",
                "result": _build_food_result(_raw_ingredients)
            },
            
        )
    )


def _build_food_result(ingredients):
    nutrition_modifier = 0.0
    saturation_modifier = 0.3
    poisonous = 0
    
    for ing in ingredients:
        if ing == "#suspicious_supplies:bowl":
            continue
        
        ing_data = _all_ingredients[ing]
        nutrition_modifier = (nutrition_modifier + ing_data["eatable"])/2
        
        poisonous += ing_data["poisonous"]

    
    nutrition = nutrition_modifier * len(ingredients)
    nausea_duration = int(poisonous*60*20)
    effect_prob = poisonous/6
    
    nausea_minute = math.floor((nausea_duration/20)/60)
    nausea_seconds = round((nausea_duration/20)%60)
    
    rank = ""
    rng_rank = ""
    
    if poisonous <= 0.1:
        rank = "Healthy"
        rng_rank = "Unlikely"
    elif poisonous <= 0.5:
        rank = "Suspicious"
        rng_rank = "Rare"
    elif poisonous <= 1.0:
        rank = "Contaminated"
        rng_rank = "Possible"
    elif poisonous <= 2.0:
        rank = "Toxic"
        rng_rank = "Probable"
    elif poisonous <= 3.0:
        rank = "Poisonous"
        rng_rank = "Certain"
    else:
        rank = "Lethal"
        rng_rank = "Inevitable"
    
    return {
        "id": "minecraft:suspicious_stew",
        "count": 1,
        "components": {
            "custom_name": "{\"text\": \"" + rank + " Food\", \"italic\": false}",
            "lore": [
                "{\"text\": \"Nausea (" + f"{str(nausea_minute)}:{str(nausea_seconds):>02}" + ")\", \"italic\": false, \"color\": \"red\"}",
                "{\"text\": \" \", \"italic\": false, \"color\": \"red\"}",
                "{\"text\": \"When Applied:\", \"italic\": false, \"color\": \"dark_purple\"}",
                "{\"text\": \"" + f"{rng_rank}" + " Side Effects\", \"italic\": false, \"color\": \"red\"}",
            ],
            "custom_model_data": 2760000,
            "food": {
                "nutrition": round(nutrition),
                "saturation": round(nutrition * saturation_modifier * 2),
                "can_always_eat": True,
                "effects": [
                    {
                        "effect": {
                            "id": "minecraft:nausea",
                            "duration": nausea_duration
                        },
                        "probability": 1
                    },
                    {
                        "effect": {
                            "id": "minecraft:mining_fatigue",
                            "duration": 1200
                        },
                        "probability": effect_prob
                    },
                    {
                        "effect": {
                            "id": "minecraft:instant_damage",
                            "amplifier": 1,
                        },
                        "probability": effect_prob*0.75
                    },
                    {
                        "effect": {
                            "id": "minecraft:blindness",
                            "duration": 600
                        },
                        "probability": effect_prob*0.75
                    },
                    {
                        "effect": {
                            "id": "minecraft:hunger",
                            "duration": 900,
                            "amplifier": 3,
                        },
                        "probability": effect_prob
                    },
                    {
                        "effect": {
                            "id": "minecraft:weakness",
                            "duration": 600
                        },
                        "probability": effect_prob
                    },
                    {
                        "effect": {
                            "id": "minecraft:poison",
                            "duration": 300,
                            "amplifier": 2
                        },
                        "probability": effect_prob*0.75
                    },
                    {
                        "effect": {
                            "id": "minecraft:wither",
                            "duration": 300
                        },
                        "probability": effect_prob*0.75
                    },
                    {
                        "effect": {
                            "id": "minecraft:levitation",
                            "duration": 300
                        },
                        "probability": effect_prob*0.75
                    },
                    {
                        "effect": {
                            "id": "minecraft:unluck",
                            "duration": 600
                        },
                        "probability": effect_prob
                    },
                    {
                        "effect": {
                            "id": "minecraft:darkness",
                            "duration": 600
                        },
                        "probability": effect_prob
                    }
                ]
            }
        }
    }


def _get_recipe_name(_ingredients):
    _ingredients = map(lambda i: i.removeprefix("#suspicious_supplies:"), _ingredients)
    _ingredients = map(lambda i: i.removeprefix("minecraft:"), _ingredients)
    _ingredients = map(lambda i: i.split("_")[0], _ingredients)
    return "-".join(_ingredients)

def _get_all_ingredients():
    result = list(_all_ingredients.keys())
        
    return result


def generate(pack: DataPack):    
    for n_ingredients in range(1, 9):
        for ingredients in combinations_with_replacement(_get_all_ingredients(), n_ingredients):
            if "#suspicious_supplies:healthy_food" in ingredients and not len(set(ingredients)) >= 2:
                continue
            
            ingredients += ("#suspicious_supplies:bowl",)
            
            recipe = _build_recipe(list(ingredients))
            recipe_name = _get_recipe_name(list(ingredients))
            
            pack["suspicious_supplies"].recipes[f"{recipe_name}"] = recipe
    
    print(f"Successfully generated {len(pack["suspicious_supplies"].recipes.keys())} recipes!")