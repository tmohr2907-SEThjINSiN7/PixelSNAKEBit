import turtle
import time
import random

# --- KONFIGURATION ---
DELAY = 0.05
SCORE_IN_BITS = 0
DATA_SIZES = [
    ("1 Bit", 1, "white"),
    ("1 Kilobit", 1000, "yellow"),
    ("1 Megabyte", 1000000, "orange"),
    ("1 Gigabyte", 1000000000, "red"),
    ("1 Terabyte", 1000000000000, "purple")
]

segments = []

# --- SETUP ---
screen = turtle.Screen()
screen.title("Self-Aware Data AI: Evolution Mode")
screen.bgcolor("#0a0a0a")
screen.setup(width=600, height=600)
screen.tracer(0)

# UI
pen = turtle.Turtle()
pen.speed(0); pen.color("cyan"); pen.penup(); pen.hideturtle(); pen.goto(0, 260)

head = turtle.Turtle()
head.shape("square"); head.color("#00ff41"); head.penup()
head.direction = "right"

food = turtle.Turtle()
food.shape("circle"); food.penup()

# --- LOGIK-FUNKTIONEN ---

def format_size(bits):
    if bits < 1000: return f"{bits} Bit"
    elif bits < 1000000: return f"{bits/1000:.1f} KB"
    elif bits < 1000000000: return f"{bits/1000000:.1f} MB"
    elif bits < 1000000000000: return f"{bits/1000000000:.1f} GB"
    else: return f"{bits/1000000000000:.2f} TB"

def spawn_food():
    global current_food_data
    current_food_data = random.choice(DATA_SIZES)
    food.color(current_food_data[2])
    # Raster-Positionen (20er Schritte)
    x = random.randint(-14, 14) * 20
    y = random.randint(-14, 14) * 20
    food.goto(x, y)

spawn_food()

def is_collision(x, y):
    for segment in segments:
        if segment.distance(x, y) < 20:
            return True
    return False

def move():
    if head.direction == "up": head.sety(head.ycor() + 20)
    elif head.direction == "down": head.sety(head.ycor() - 20)
    elif head.direction == "left": head.setx(head.xcor() - 20)
    elif head.direction == "right": head.setx(head.xcor() + 20)

def autopilot():
    # Mögliche Züge prüfen
    directions = {
        "up": (head.xcor(), head.ycor() + 20),
        "down": (head.xcor(), head.ycor() - 20),
        "left": (head.xcor() - 20, head.ycor()),
        "right": (head.xcor() + 20, head.ycor())
    }
    
    best_dir = head.direction
    min_dist = float('inf')
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}

    for direction, (nx, ny) in directions.items():
        if direction == opposites.get(head.direction): continue
        
        # Wand-Teleportation simulieren für Distanzcheck
        tx, ty = nx, ny
        if tx > 280: tx = -280
        elif tx < -280: tx = 280
        if ty > 280: ty = -280
        elif ty < -280: ty = 280

        if not is_collision(tx, ty):
            # Einfache euklidische Distanz zum Futter
            dist = ((tx - food.xcor())**2 + (ty - food.ycor())**2)**0.5
            if dist < min_dist:
                min_dist = dist
                best_dir = direction
    
    head.direction = best_dir

# --- MAIN LOOP ---
while True:
    screen.update()

    # 1. Kollision mit Futter
    if head.distance(food) < 20:
        label, value, color = current_food_data
        SCORE_IN_BITS += value
        
        # Ein Segment hinzufügen
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color(color)
        new_segment.penup()
        segments.append(new_segment)
        
        spawn_food()
        pen.clear()
        pen.write(f"Data Collected: {format_size(SCORE_IN_BITS)}", align="center", font=("Courier", 14, "bold"))

    # 2. Segmente bewegen (von hinten nach vorne)
    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # 3. KI Entscheidung & Bewegung
    autopilot()
    move()

    # 4. Screen Wrap (Teleportation an den Rändern)
    if head.xcor() > 290: head.setx(-290)
    elif head.xcor() < -290: head.setx(290)
    if head.ycor() > 290: head.sety(-290)
    elif head.ycor() < -290: head.sety(290)

    time.sleep(DELAY)

screen.mainloop()
