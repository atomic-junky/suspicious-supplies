import json
from beet import PngFile, Context, Model

from recipes import generate


def build_recipes(ctx: Context):
    pack = ctx.data
    generate(pack)
    

def build_resource_pack(ctx: Context):
    ctx.assets.icon = PngFile(source_path="suspicious-supplies/pack.png")
    
    # build_item_models(ctx)

def build_item_models(ctx: Context):
    pack = ctx.assets
    for texture in ctx.assets.textures:
        item_name = texture.split("/")[1]
        if pack["tasty_supplies"].models.get(f"item/{item_name}"):
            continue
        
        json_model = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"tasty_supplies:item/{item_name}"
            }
        }
        model = Model(
            json.dumps(json_model),
            f"{item_name}.json"
        )
        pack["tasty_supplies"].models[f"item/{item_name}"] = model