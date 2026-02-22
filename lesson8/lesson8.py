import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# שאלה 1 – פונקציות טריגונומטריות
# ============================================================

# א. פונקציה שממירה ממעלות לרדיאנים
def degrees_to_radians(degrees):
    return degrees * math.pi / 180

# ב + ג. חישוב והדפסה בפורמט CSV
degrees_list = [0, 1, 5, 10, 30, 45, 90, 180]

print("degrees,radians,sin,cos")
for deg in degrees_list:
    rad = degrees_to_radians(deg)
    s = math.sin(rad)
    c = math.cos(rad)
    print(f"{deg},{rad:.6f},{s:.6f},{c:.6f}")

print()

# ============================================================
# שאלה 3 – מטריצות סיבוב, scaling וציור מלבנים
# ============================================================

# א. מטריצת סיבוב 30 מעלות
theta = np.radians(30)
r_30 = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])
print("מטריצת סיבוב 30 מעלות (r_30):")
print(r_30)

# ב. מטריצת scale פי 2 בציר x
sx_2 = np.array([
    [2, 0],
    [0, 1]
])
print("\nמטריצת scale פי 2 בציר x (sx_2):")
print(sx_2)

# ג. rs = r_30 @ sx_2  (קודם scale, אחר כך סיבוב)
rs = r_30 @ sx_2
print("\nrs = r_30 @ sx_2:")
print(rs)

# ד. sr = sx_2 @ r_30  (קודם סיבוב, אחר כך scale)
sr = sx_2 @ r_30
print("\nsr = sx_2 @ r_30:")
print(sr)

# ה. מלבן מקורי: רוחב 2, גובה 1, מרכז בראשית
rect = np.array([
    [-1,  1,  1, -1, -1],         # קואורדינטות x
    [-0.5, -0.5, 0.5, 0.5, -0.5]  # קואורדינטות y
])

# ו. סיבוב 30 מעלות
rotated = r_30 @ rect

# ז. מתיחה פי 2 בציר x
scaled = sx_2 @ rect

# ח. הפעלת sr ו-rs על המלבן
sr_rect = sr @ rect
rs_rect = rs @ rect

# ט. ציור כל חמשת המלבנים
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(rect[0],     rect[1],     'b-o', linewidth=2, label='מלבן מקורי')
ax.plot(rotated[0],  rotated[1],  'r-o', linewidth=2, label='סיבוב 30° (r_30)')
ax.plot(scaled[0],   scaled[1],   'g-o', linewidth=2, label='scale פי 2 בציר x (sx_2)')
ax.plot(sr_rect[0],  sr_rect[1],  'm-o', linewidth=2, label='sr = קודם סיבוב, אחר כך scale')
ax.plot(rs_rect[0],  rs_rect[1],  'c-o', linewidth=2, label='rs = קודם scale, אחר כך סיבוב')

ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_aspect('equal')
ax.legend(loc='upper left')
ax.set_title('חמישה מלבנים – סיבוב ו-Scaling')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()