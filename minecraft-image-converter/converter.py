from PIL import Image
import math
import os

blocks = [
    "blackstone","deepslate","blue_terracotta","blue_concrete_powder",
    "cyan_terracotta","cyan_concrete_powder","warped_nylium","prismarine",
    "green_terracotta","green_concrete_powder","moss_block","lime_terracotta",
    "lime_concrete_powder","oxidized_copper","packed_ice","ice",

    "red_terracotta","brown_terracotta","purple_terracotta","magenta_terracotta",
    "pink_terracotta","granite","diorite","andesite",
    "tuff","calcite","dripstone_block","smooth_basalt",
    "clay","light_blue_terracotta","light_blue_concrete_powder","cyan_wool",

    "red_concrete_powder","red_wool","nether_bricks","crimson_nylium",
    "magenta_concrete_powder","purple_wool","pink_concrete_powder","pink_wool",
    "orange_terracotta","orange_concrete_powder","honeycomb_block","cut_copper",
    "yellow_terracotta","yellow_concrete_powder","sponge","end_stone",

    "sandstone","sandstone_top","birch_planks","end_stone_bricks",
    "white_terracotta","light_gray_terracotta","gray_terracotta","cobblestone",
    "stone","smooth_stone","polished_andesite","polished_diorite",
    "calcite","quartz_block_bottom","quartz_bricks","white_concrete_powder"
]

block_data = []

for name in blocks:
    img = Image.open("block/" + name + ".png").convert("RGB")

    sum_r = sum_g = sum_b = 0

    for y in range(16):
        for x in range(16):
            r, g, b = img.getpixel((x, y))
            sum_r += r
            sum_g += g
            sum_b += b

    average = (sum_r // 256, sum_g // 256, sum_b // 256)
    block_data.append((img, average))

read_size = 4
scale = 16

os.makedirs("result", exist_ok=True)

for file in os.listdir("read"):

    if not file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    print(f"Processing: {file}")

    path = os.path.join("read", file)
    image = Image.open(path).convert("RGB")

    width, height = image.size

    new_width = math.ceil(width / read_size) * scale
    new_height = math.ceil(height / read_size) * scale

    result = Image.new("RGB", (new_width, new_height))

    for by in range(0, height, read_size):
        for bx in range(0, width, read_size):

            sum_r = sum_g = sum_b = 0
            count = 0

            for y in range(by, min(by + read_size, height)):
                for x in range(bx, min(bx + read_size, width)):
                    r, g, b = image.getpixel((x, y))
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1

            avg_r = sum_r // count
            avg_g = sum_g // count
            avg_b = sum_b // count

            best = None
            min_dist = float("inf")

            for img, (br, bg, bb) in block_data:
                dist = (avg_r - br)**2 + (avg_g - bg)**2 + (avg_b - bb)**2

                if dist < min_dist:
                    min_dist = dist
                    best = img

            nx = (bx // read_size) * scale
            ny = (by // read_size) * scale

            result.paste(best, (nx, ny))

    name = os.path.splitext(file)[0] + "_minecraft.png"
    result.save(os.path.join("result", name))

    print(f"✔ Saved: {name}")

print("Done!")