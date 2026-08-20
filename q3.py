#Step 1: Draw a square.
#Step 2: Attach a right triangle to one of its sides along its hy-
#pothenuse (here with two equal sides).
#Step 3: Attach two squares along the free sides of the triangle.
#Step 4: Attach two right triangles.
#Step 5: Attach four squares.
#Step 6: Attach four right triangles.
#Step 7: Attach eight squares.
import math
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_rotation_matrix(deg):
    angle_rad = deg/180.0 * math.pi
    c = torch.cos(angle_rad)
    s = torch.sin(angle_rad)
    return torch.stack([torch.stack([c, -s]), torch.stack([s, c])])

def generate_square_corners(p1, p2):
    # p1, p2 are bottom-left and bottom-right corners (shape: [2])
    v = p2 - p1
    perp = torch.stack([-v[1], v[0]])
    p3 = p1 + perp
    p4 = p2 + perp
    return torch.stack([p1, p2, p4, p3])

def tri_eq(tl, tr):
    peak = (tr + tl) / 2.0
    v = peak - tl
    perp = torch.stack([-v[1], v[0]])
    peak = peak + perp 
    return peak

def tri_isoc(tl, tr):
    v = tr - tl
    theta = torch.tensor(50.0)
    peak = torch.matmul(get_rotation_matrix(theta), v)
    return peak + tl

def build_pythagoras_tree(p1, p2, depth): # alpha = 45 deg
        #step 1: draw a square
    corners = generate_square_corners(p1,p2)
    tl = corners[3]
    tr = corners[2]

    if depth == 0:
        return [corners]

    #tri_point = tri_eq(tl,tr)
    tri_point = tri_isoc(tl, tr)

    left = build_pythagoras_tree(tl, tri_point, depth - 1)
    right = build_pythagoras_tree(tri_point, tr, depth - 1)
    triangle = torch.stack([tl, tri_point, tr])

    return [corners] + [triangle] + left + right

p1 = torch.tensor([0.0, 0.0], dtype=torch.float32)
p2 = torch.tensor([1.0, 0.0], dtype=torch.float32)
squares = build_pythagoras_tree(p1, p2, depth=5)

fig, ax = plt.subplots(figsize=(10, 10))
for sq in squares:
    sq_np = sq.detach().numpy()
    polygon = patches.Polygon(sq_np, closed=True, edgecolor='black', facecolor='forestgreen', alpha=0.6)
    ax.add_patch(polygon)
ax.set_xlim(-2, 3)
ax.set_ylim(0, 5)
ax.set_aspect('equal')
plt.axis('off')
plt.show()