# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from dronekit import connect
import numpy as np
import math
import time

plt.ion()
fig, ax = plt.subplots(figsize=(10, 15))
fig.patch.set_alpha(0.0)
ax.set_facecolor((0, 0, 0, 0.5))
ax.set_xlim(-6, 6)
ax.set_ylim(-8, 8)
ax.axis('off')

# ================= ELEMENTOS GRAFICOS ======================
pitch_lines = []
for pitch in range(-20, 25, 5):
    y = pitch * 0.1
    if pitch == 0:
        x1, x2 = -2, 2
        lw = 2
    elif pitch % 10 == 0:
        x1, x2 = -1.2, 1.2
        lw = 1
    else:
        x1, x2 = -0.7, 0.7
        lw = 1
    line, = ax.plot([x1, x2], [y, y], color='lime', lw=lw)
    pitch_lines.append(line)

# Indicador de velocidade
speed_ticks = np.arange(0, 51, 5)
for spd in speed_ticks:
    y = spd * 0.2 - 6
    if spd % 10 == 0:
        x1, x2 = -5.3, -4.7
        ax.text(-5.4, y, str(spd), color='lime', ha='right', va='center', fontsize=8)
    else:
        x1, x2 = -5.2, -4.8
    ax.plot([x1, x2], [y, y], color='lime')
speed_pointer, = ax.plot([-5], [-6], marker='>', color='lime', markersize=10)

# Indicador de altitude
alt_ticks = np.arange(0, 60, 5)
for alt in alt_ticks:
    y = alt * 0.2 - 6
    if alt % 20 == 0:
        x1, x2 = 4.7, 5.3
        ax.text(5.35, y, str(alt), color='lime', ha='left', va='center', fontsize=8)
    elif alt % 10 == 0:
        x1, x2 = 4.75, 5.25
        ax.text(5.3, y, str(alt), color='lime', ha='left', va='center', fontsize=6)
    else:
        x1, x2 = 4.8, 5.2
    ax.plot([x1, x2], [y, y], color='lime')
alt_pointer, = ax.plot([5], [-6], marker='<', color='lime', markersize=10)

# Bússola
for hdg in range(0, 360, 30):
    x = (hdg - 180) * 0.03
    ax.text(x, 7.5, str(hdg), color='lime', ha='center', fontsize=8)
heading_pointer = ax.plot([0], [7.2], marker='v', color='lime', markersize=8)[0]

# Indicador de atitude (roll)
roll_arc = np.linspace(-math.pi/3, math.pi/3, 100)
roll_circle, = ax.plot(np.sin(roll_arc)*4.0, np.cos(roll_arc)*4.0 + 0.5, color='lime', lw=1)

for angle_deg in range(-60, 61, 5):
    angle_rad = math.radians(angle_deg)
    sin_a = math.sin(angle_rad)
    cos_a = math.cos(angle_rad)
    
    # Ajuste do comprimento das linhas
    if angle_deg % 10 == 0:
        x_start = sin_a * 4.5
        y_start = cos_a * 4.5 + 0.5
        x_end = sin_a * 4.0  # Linhas mais longas
        y_end = cos_a * 4.0 + 0.5
    else:
        x_start = sin_a * 4.5
        y_start = cos_a * 4.5 + 0.5
        x_end = sin_a * 4.3  # Linhas mais curtas
        y_end = cos_a * 4.3 + 0.5

    ax.plot([x_start, x_end], [y_start, y_end], color='lime', lw=1)  # Espessura fixa

roll_marker = ax.plot([0], [3], marker='^', color='lime', markersize=10)[0]

# Indicador central
ax.plot([0], [0], marker='o', color='lime', markersize=6)
ax.plot([-3.0, 3.0], [0, 0], color='red', lw=1.5)
ax.plot([0, 0], [-0.3, 0.3], color='lime', lw=1)

print("Conectando ao veiculo...")
vehicle = connect('udp:192.168.12.113:14550', wait_ready=True)
print("Conexao estabelecida!")

try:
    while True:
        att = vehicle.attitude
        vel = vehicle.velocity
        alt = vehicle.location.global_relative_frame.alt
        heading = vehicle.heading

        pitch_deg = math.degrees(att.pitch)
        roll_deg = math.degrees(att.roll)

        for i, pitch in enumerate(range(-20, 25, 5)):
            y = (pitch - pitch_deg) * 0.1
            x_offset = math.tan(math.radians(roll_deg)) * y
            if pitch == 0:
                pitch_lines[i].set_data([-2 + x_offset, 2 + x_offset], [y, y])
            elif pitch % 10 == 0:
                pitch_lines[i].set_data([-1.2 + x_offset, 1.2 + x_offset], [y, y])
            else:
                pitch_lines[i].set_data([-0.7 + x_offset, 0.7 + x_offset], [y, y])

        groundspeed = math.sqrt(vel[0]**2 + vel[1]**2)
        speed_pointer.set_ydata([groundspeed * 0.2 - 6])
        alt_pointer.set_ydata([alt * 0.2 - 6])

        hdg_offset = (heading - 180) * 0.03
        heading_pointer.set_xdata([hdg_offset])

        x = math.sin(math.radians(roll_deg)) * 4.0
        y = math.cos(math.radians(roll_deg)) * 4.0 + 0.5
        roll_marker.set_data([x], [y])

        plt.pause(0.02)

except KeyboardInterrupt:
    print("Encerrando...")
finally:
    vehicle.close()
    plt.close()
