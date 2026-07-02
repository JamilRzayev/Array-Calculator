import os
import random
import math
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (245, 245, 220)  # Cream Beige
PALETTE = {
    "cream": (245, 245, 220),
    "ochre": (204, 119, 34),
    "olive": (128, 128, 0),
    "blue": (102, 153, 204),
    "violet": (145, 95, 109),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "red": (255, 0, 0),
    "brown": (139, 69, 19),
    "green": (34, 139, 34),
}

class DoodleDrawer:
    def __init__(self, draw):
        self.draw = draw

    def shaky_line(self, xy, fill=PALETTE["black"], width=5, complexity=2):
        """Draws a shaky line between points."""
        if len(xy) < 2: return
        all_points = []
        for i in range(len(xy) - 1):
            x1, y1 = xy[i]
            x2, y2 = xy[i+1]
            dist = math.hypot(x2 - x1, y2 - y1)
            steps = max(int(dist / 10), 1)
            for j in range(steps):
                t = j / steps
                px = x1 + (x2 - x1) * t + random.uniform(-complexity, complexity)
                py = y1 + (y2 - y1) * t + random.uniform(-complexity, complexity)
                all_points.append((px, py))
        all_points.append(xy[-1])
        self.draw.line(all_points, fill=fill, width=width, joint="round")

    def shaky_circle(self, center, radius, fill=None, outline=PALETTE["black"], width=5):
        """Draws a shaky circle."""
        cx, cy = center
        points = []
        steps = 40
        for i in range(steps + 1):
            angle = 2 * math.pi * i / steps
            r = radius + random.uniform(-2, 2)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))

        if fill:
            self.draw.polygon(points, fill=fill)
        if outline:
            self.draw.line(points, fill=outline, width=width, joint="round")

    def stick_man(self, pos, scale=1.0, hair=True, gender="man", pose="neutral", age="young"):
        cx, cy = pos
        # Head
        head_radius = 40 * scale
        self.shaky_circle((cx, cy - 100 * scale), head_radius, fill=PALETTE["white"])

        # Hair
        if hair:
            if gender == "man":
                for _ in range(15):
                    angle = random.uniform(math.pi*1.1, math.pi*1.9)
                    h_start = (cx + head_radius*0.8 * math.cos(angle), cy - 100 * scale + head_radius*0.8 * math.sin(angle))
                    h_end = (cx + head_radius*1.2 * math.cos(angle), cy - 100 * scale + head_radius*1.2 * math.sin(angle))
                    self.shaky_line([h_start, h_end], width=int(3*scale))
            elif gender == "woman":
                # Long hair
                self.shaky_line([(cx-head_radius, cy-100*scale), (cx-head_radius-10*scale, cy-20*scale)], width=int(4*scale))
                self.shaky_line([(cx+head_radius, cy-100*scale), (cx+head_radius+10*scale, cy-20*scale)], width=int(4*scale))
                # Braid
                bx, by = cx + head_radius*0.7, cy-100*scale
                self.shaky_line([(bx, by), (bx+20*scale, cy+20*scale)], width=int(6*scale))
                # Beads
                for i in range(3):
                    color = [PALETTE["orange"], PALETTE["red"], PALETTE["white"]][i]
                    self.shaky_circle((bx+15*scale, cy - 60*scale + i*25*scale), 5*scale, fill=color)

        # Eyes
        eye_y = cy - 110*scale
        self.draw.ellipse([cx - 15*scale, eye_y, cx - 10*scale, eye_y + 5*scale], fill=PALETTE["black"])
        self.draw.ellipse([cx + 10*scale, eye_y, cx + 15*scale, eye_y + 5*scale], fill=PALETTE["black"])

        # Eyebrows
        self.shaky_line([(cx - 20*scale, cy - 120*scale), (cx - 5*scale, cy - 120*scale)], width=2)
        self.shaky_line([(cx + 5*scale, cy - 120*scale), (cx + 20*scale, cy - 120*scale)], width=2)

        # Mouth
        if pose == "confused":
             self.shaky_line([(cx - 15*scale, cy - 85*scale), (cx + 15*scale, cy - 85*scale)], width=2)
        elif pose == "open":
             self.shaky_circle((cx, cy - 85*scale), 8*scale, outline=PALETTE["black"])
        else: # neutral
             self.shaky_line([(cx - 10*scale, cy - 85*scale), (cx + 10*scale, cy - 85*scale)], width=2)

        # Body
        body_top = (cx, cy - 60 * scale)
        if age == "old":
            # Hunched
            body_mid = (cx + 20*scale, cy)
            body_bottom = (cx, cy + 60 * scale)
            self.shaky_line([body_top, body_mid, body_bottom], width=5)
        else:
            body_bottom = (cx, cy + 60 * scale)
            self.shaky_line([body_top, body_bottom], width=5)

        # Arms
        if pose == "shrug":
            self.shaky_line([body_top, (cx - 70*scale, cy - 40*scale), (cx - 100*scale, cy - 80*scale)], width=4)
            self.shaky_line([body_top, (cx + 70*scale, cy - 40*scale), (cx + 100*scale, cy - 80*scale)], width=4)
        elif pose == "holding_baby":
            self.shaky_line([body_top, (cx - 40*scale, cy), (cx, cy)], width=4)
            self.shaky_line([body_top, (cx + 40*scale, cy), (cx, cy)], width=4)
            # Baby
            self.shaky_circle((cx, cy), 20*scale, fill=PALETTE["white"])
            self.shaky_line([(cx, cy+15*scale), (cx, cy+35*scale)], width=3)
        elif pose == "pointing":
            self.shaky_line([body_top, (cx - 80*scale, cy + 20*scale)], width=4)
            self.shaky_line([body_top, (cx + 120*scale, cy - 20*scale)], width=4) # pointing arm
        elif pose == "pointing_both":
            self.shaky_line([body_top, (cx - 120*scale, cy - 20*scale)], width=4)
            self.shaky_line([body_top, (cx + 120*scale, cy - 20*scale)], width=4)
        elif pose == "arms_wide":
            self.shaky_line([body_top, (cx - 100*scale, cy - 20*scale)], width=4)
            self.shaky_line([body_top, (cx + 100*scale, cy - 20*scale)], width=4)
        else: # neutral
            self.shaky_line([body_top, (cx - 40*scale, cy + 20*scale)], width=4)
            self.shaky_line([body_top, (cx + 40*scale, cy + 20*scale)], width=4)

        # Legs
        if pose == "sitting":
            self.shaky_line([body_bottom, (cx - 50*scale, cy + 100*scale), (cx - 10*scale, cy + 100*scale)], width=4)
            self.shaky_line([body_bottom, (cx + 50*scale, cy + 100*scale), (cx + 10*scale, cy + 100*scale)], width=4)
        else:
            self.shaky_line([body_bottom, (cx - 30*scale, cy + 140*scale)], width=4)
            self.shaky_line([body_bottom, (cx + 30*scale, cy + 140*scale)], width=4)

    def season_wheel(self, center, radius):
        cx, cy = center
        self.shaky_circle(center, radius, fill=PALETTE["white"])
        # Divide into 4
        self.shaky_line([(cx - radius, cy), (cx + radius, cy)], width=3)
        self.shaky_line([(cx, cy - radius), (cx, cy + radius)], width=3)

        # Sun (Top Right)
        scx, scy = cx + radius/2, cy - radius/2
        self.shaky_circle((scx, scy), 20, fill=PALETTE["ochre"])
        for i in range(8):
            a = i * math.pi/4
            self.shaky_line([(scx+25*math.cos(a), scy+25*math.sin(a)), (scx+35*math.cos(a), scy+35*math.sin(a))], width=2)

        # Rain (Top Left)
        rcx, rcy = cx - radius/2, cy - radius/2
        for _ in range(5):
            rx, ry = rcx + random.uniform(-30, 30), rcy + random.uniform(-30, 30)
            self.shaky_line([(rx, ry), (rx-5, ry+10)], fill=PALETTE["blue"], width=2)

        # Snow (Bottom Left)
        ncx, ncy = cx - radius/2, cy + radius/2
        for _ in range(5):
            nx, ny = ncx + random.uniform(-30, 30), ncy + random.uniform(-30, 30)
            self.shaky_circle((nx, ny), 3, fill=PALETTE["blue"], outline=None)

        # Harvest (Bottom Right)
        hcx, hcy = cx + radius/2, cy + radius/2
        self.shaky_line([(hcx-20, hcy+20), (hcx+20, hcy-20)], fill=PALETTE["ochre"], width=5)
        self.shaky_line([(hcx-10, hcy+20), (hcx+30, hcy-10)], fill=PALETTE["ochre"], width=3)

    def researcher(self, pos, scale=1.0):
        cx, cy = pos
        # Silhouette
        body_points = [(cx-20*scale, cy+100*scale), (cx+20*scale, cy+100*scale), (cx+20*scale, cy-20*scale), (cx, cy-40*scale), (cx-20*scale, cy-20*scale)]
        self.draw.polygon(body_points, fill=PALETTE["olive"])
        self.shaky_circle((cx, cy-60*scale), 20*scale, fill=PALETTE["olive"])
        # Notepad
        self.draw.rectangle([cx+10*scale, cy, cx+40*scale, cy+40*scale], fill=PALETTE["white"], outline=PALETTE["black"])

    def tree(self, pos, stage="full", scale=1.0):
        cx, cy = pos
        if stage == "sapling":
            self.shaky_line([(cx, cy), (cx, cy-40*scale)], fill=PALETTE["brown"], width=3)
            self.shaky_circle((cx+5*scale, cy-40*scale), 10*scale, fill=PALETTE["green"])
        else:
            self.shaky_line([(cx, cy), (cx, cy-150*scale)], fill=PALETTE["brown"], width=15)
            self.shaky_circle((cx, cy-180*scale), 80*scale, fill=PALETTE["green"])

    def deer(self, pos, scale=0.5):
        cx, cy = pos
        # Body
        self.draw.ellipse([cx-40*scale, cy-20*scale, cx+40*scale, cy+20*scale], fill=PALETTE["brown"])
        # Neck & Head
        self.shaky_line([(cx+30*scale, cy), (cx+50*scale, cy-40*scale)], fill=PALETTE["brown"], width=int(8*scale))
        self.shaky_circle((cx+55*scale, cy-45*scale), 10*scale, fill=PALETTE["brown"])
        # Legs
        for i in [-30, -10, 10, 30]:
            self.shaky_line([(cx+i*scale, cy+10*scale), (cx+i*scale, cy+40*scale)], fill=PALETTE["brown"], width=int(3*scale))

def get_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def save(img, name):
    img.save(os.path.join("generated_images", name))

# --- Frame Generators ---

def gen_frame_1():
    img, draw, d = create_image(1)
    d.stick_man((WIDTH//2, HEIGHT//2 + 100), scale=2.0, pose="confused")
    for _ in range(20):
        x, y = random.randint(WIDTH//2 - 300, WIDTH//2 + 300), random.randint(HEIGHT//2 - 400, HEIGHT//2)
        draw.text((x, y), str(random.randint(0, 9)), fill=PALETTE["black"], font=get_font(40))
    save(img, "frame_01.png")

def gen_frame_2():
    img, draw, d = create_image(2)
    d.stick_man((WIDTH//2, HEIGHT//2 + 100), scale=2.0, pose="shrug")
    for _ in range(10):
        x, y = random.randint(WIDTH//2 - 300, WIDTH//2 + 300), random.randint(HEIGHT//2 - 400, HEIGHT//2)
        draw.text((x, y), str(random.randint(0, 9)), fill=(150, 150, 150), font=get_font(30)) # Faint
    save(img, "frame_02.png")

def gen_frame_3():
    img, draw, d = create_image(3)
    d.shaky_line([(0, HEIGHT*0.8), (WIDTH, HEIGHT*0.8)], width=2) # Horizon
    # Campfire
    cx, cy = WIDTH//2, HEIGHT*0.75
    for _ in range(5):
        d.shaky_line([(cx-20, cy), (cx+20, cy-40)], fill=PALETTE["ochre"], width=5)
    # People
    for i in range(5):
        angle = i * (2*math.pi / 5)
        px, py = cx + 200*math.cos(angle), cy + 100*math.sin(angle)
        d.stick_man((px, py), scale=0.8, pose="sitting")
    save(img, "frame_03.png")

def gen_frame_4():
    img, draw, d = create_image(4)
    d.stick_man((WIDTH//2 - 100, HEIGHT//2 + 100), scale=2.0, gender="woman", pose="holding_baby")
    # Stone tablet
    draw.polygon([(WIDTH//2 + 200, HEIGHT//2), (WIDTH//2 + 400, HEIGHT//2), (WIDTH//2 + 400, HEIGHT//2 + 300), (WIDTH//2 + 200, HEIGHT//2 + 300)], fill=(200, 200, 200), outline=PALETTE["black"])
    save(img, "frame_04.png")

def gen_frame_5():
    img, draw, d = create_image(5)
    y = HEIGHT//2
    d.shaky_line([(WIDTH//4, y), (3*WIDTH//4, y)], width=5)
    for i in range(10):
        x = WIDTH//4 + i * (WIDTH//2 / 9)
        d.shaky_line([(x, y-20), (x, y+20)], width=3)
    # Scribble
    for _ in range(50):
        x1, y1 = random.randint(WIDTH//4, 3*WIDTH//4), random.randint(y-50, y+50)
        x2, y2 = x1 + random.randint(-50, 50), y1 + random.randint(-50, 50)
        d.shaky_line([(x1, y1), (x2, y2)], width=10)
    save(img, "frame_05.png")

def gen_frame_6():
    img, draw, d = create_image(6)
    d.season_wheel((WIDTH//2, HEIGHT//2), 300)
    save(img, "frame_06.png")

def gen_frame_7():
    img, draw, d = create_image(7)
    d.shaky_line([(0, HEIGHT*0.8), (WIDTH, HEIGHT*0.8)], width=2)
    for i in range(4):
        d.deer((400 + i*300, HEIGHT*0.75))
    # Rain
    for _ in range(100):
        rx, ry = random.randint(0, WIDTH), random.randint(0, HEIGHT//2)
        d.shaky_line([(rx, ry), (rx-10, ry+20)], fill=PALETTE["blue"], width=1)
    save(img, "frame_07.png")

def gen_frame_8():
    img, draw, d = create_image(8)
    d.stick_man((WIDTH//3, HEIGHT//2 + 100), scale=2.0)
    d.season_wheel((2*WIDTH//3, HEIGHT//2), 200)
    save(img, "frame_08.png")

def gen_frame_9():
    img, draw, d = create_image(9)
    d.shaky_line([(0, HEIGHT*0.8), (WIDTH, HEIGHT*0.8)], width=2)
    d.tree((WIDTH//3, HEIGHT*0.8), stage="sapling", scale=2.0)
    d.tree((2*WIDTH//3, HEIGHT*0.8), stage="full", scale=2.0)
    save(img, "frame_09.png")

def gen_frame_10():
    img, draw, d = create_image(10)
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(1, 11):
        d.shaky_circle((cx, cy), i * 30, outline=PALETTE["black"], width=2)
    save(img, "frame_10.png")

def gen_frame_11():
    img, draw, d = create_image(11)
    d.stick_man((WIDTH//2, HEIGHT//2 + 100), scale=2.0, pose="shrug")
    draw.text((WIDTH//2 - 20, HEIGHT//2 - 250), "?", fill=PALETTE["black"], font=get_font(100))
    draw.text((WIDTH//2 + 200, HEIGHT//2), "HADZA", fill=PALETTE["black"], font=get_font(80))
    save(img, "frame_11.png")

def gen_frame_12():
    img, draw, d = create_image(12)
    # Close-up
    d.stick_man((WIDTH//2, HEIGHT + 400), scale=5.0)
    save(img, "frame_12.png")

def gen_frame_13():
    img, draw, d = create_image(13)
    d.researcher((WIDTH//3, HEIGHT//2 + 100), scale=2.0)
    d.stick_man((2*WIDTH//3, HEIGHT//2 + 100), scale=2.0, gender="woman")
    draw.text((WIDTH//2, HEIGHT//2 + 300), "JU'/HOANSI", fill=PALETTE["black"], font=get_font(80))
    save(img, "frame_13.png")

def gen_frame_14():
    img, draw, d = create_image(14)
    d.stick_man((WIDTH//3, HEIGHT//2 + 100), scale=2.0, age="old", pose="sitting")
    d.researcher((2*WIDTH//3, HEIGHT//2 + 100), scale=2.0)
    save(img, "frame_14.png")

def gen_frame_15():
    img, draw, d = create_image(15)
    # Split scene
    d.shaky_line([(WIDTH//2, 0), (WIDTH//2, HEIGHT)], width=5)
    # Flood
    for y in range(0, HEIGHT, 40):
        d.shaky_line([(0, y), (WIDTH//2, y + 20)], fill=PALETTE["blue"], width=2)
    # Cracked earth
    for _ in range(20):
        x1, y1 = random.randint(WIDTH//2, WIDTH), random.randint(0, HEIGHT)
        x2, y2 = x1 + random.randint(-50, 50), y1 + random.randint(-50, 50)
        d.shaky_line([(x1, y1), (x2, y2)], fill=PALETTE["ochre"], width=3)
    save(img, "frame_15.png")

def gen_frame_16():
    img, draw, d = create_image(16)
    d.stick_man((WIDTH//2, HEIGHT//2 + 100), scale=2.0, age="old", pose="pointing_both")
    # Left flood
    d.shaky_line([(100, HEIGHT//2), (400, HEIGHT//2 + 50)], fill=PALETTE["blue"], width=10)
    # Right crack
    d.shaky_line([(WIDTH-400, HEIGHT//2), (WIDTH-100, HEIGHT//2 + 50)], fill=PALETTE["ochre"], width=10)
    save(img, "frame_16.png")

def gen_frame_17():
    img, draw, d = create_image(17)
    # Jungle
    for _ in range(30):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        d.shaky_circle((x, y), random.randint(50, 150), fill=PALETTE["olive"], outline=None)
    # Silhouettes
    for i in range(3):
        d.stick_man((400 + i*500, HEIGHT//2 + 200), scale=1.5, hair=False)
    draw.text((WIDTH//2, HEIGHT//2), "PIRAHÃ", fill=PALETTE["black"], font=get_font(100))
    save(img, "frame_17.png")

def gen_frame_18():
    img, draw, d = create_image(18)
    d.stick_man((WIDTH//2, HEIGHT//2 + 100), scale=2.0, pose="open")
    # Speech bubble
    d.shaky_circle((WIDTH//2 + 150, HEIGHT//2 - 150), 100, fill=PALETTE["white"])
    d.shaky_line([(WIDTH//2 + 50, HEIGHT//2 - 80), (WIDTH//2 + 70, HEIGHT//2 - 100)], width=3)
    save(img, "frame_18.png")

def gen_frame_19():
    img, draw, d = create_image(19)
    # Few
    d.shaky_circle((WIDTH//3, HEIGHT//2), 20, fill=PALETTE["ochre"])
    d.shaky_circle((WIDTH//3 + 50, HEIGHT//2 + 20), 20, fill=PALETTE["ochre"])
    draw.text((WIDTH//3, HEIGHT//2 + 100), "FEW", fill=PALETTE["black"], font=get_font(60))
    # Many
    for _ in range(15):
        x, y = random.randint(2*WIDTH//3, 2*WIDTH//3 + 100), random.randint(HEIGHT//2 - 50, HEIGHT//2 + 50)
        d.shaky_circle((x, y), 20, fill=PALETTE["ochre"])
    draw.text((2*WIDTH//3, HEIGHT//2 + 100), "MANY", fill=PALETTE["black"], font=get_font(60))
    save(img, "frame_19.png")

def gen_frame_20():
    img, draw, d = create_image(20)
    # Jungle bg
    for _ in range(20):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        d.shaky_circle((x, y), random.randint(50, 150), fill=PALETTE["olive"], outline=None)
    # 1, 2, 3
    draw.text((WIDTH//2 - 200, HEIGHT//2), "1, 2, 3", fill=PALETTE["black"], font=get_font(150))
    # Scribble over it
    for _ in range(40):
        x1, y1 = random.randint(WIDTH//2 - 300, WIDTH//2 + 300), random.randint(HEIGHT//2, HEIGHT//2 + 150)
        x2, y2 = x1 + random.randint(-100, 100), y1 + random.randint(-50, 50)
        d.shaky_line([(x1, y1), (x2, y2)], width=15)
    save(img, "frame_20.png")

def create_image(frame_num):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    d = DoodleDrawer(draw)
    return img, draw, d

if __name__ == "__main__":
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")

    generators = [
        gen_frame_1, gen_frame_2, gen_frame_3, gen_frame_4, gen_frame_5,
        gen_frame_6, gen_frame_7, gen_frame_8, gen_frame_9, gen_frame_10,
        gen_frame_11, gen_frame_12, gen_frame_13, gen_frame_14, gen_frame_15,
        gen_frame_16, gen_frame_17, gen_frame_18, gen_frame_19, gen_frame_20
    ]

    for i, gen in enumerate(generators):
        gen()
        print(f"Frame {i+1} generated.")
