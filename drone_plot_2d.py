# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')  # Backend gráfico
import matplotlib.pyplot as plt
from dronekit import connect
import numpy as np
import math
import time

# Configuração do display
plt.ion()
fig, ax = plt.subplots(figsize=(5, 5))
ax_main = fig.add_subplot(111, aspect='equal')
ax_speed = fig.add_subplot(111, aspect='equal')
ax_atitude = fig.add_subplot(111, aspect='equal')
ax_bkAngle = fig.add_subplot(111, aspect='equal')
ax_direction = fig.add_subplot(111, aspect='equal')
ax.set_aspect('equal')

#indicador de atitude
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis('off')
ax.grid(color='gray', linestyle='--', linewidth=0.5)
ax.set_xticks(np.arange(-1, 1.1, 0.2))
ax.set_yticks(np.arange(-1, 1.1, 0.2))
ax.set_xlabel('Eixo X', fontsize=10)
ax.set_ylabel('Eixo Y', fontsize=10)
ax.set_title('Indicador de Atitude', fontsize=10)
plt.title('Indicador de Atitude', fontsize=10)

#indicador de velocidade
ax_speed.set_xlim(-1, 1)
ax_speed.set_ylim(-1, 1)
ax_speed.axis('off')
ax_speed.grid(color='gray', linestyle='--', linewidth=0.5)
ax_speed.set_xticks(np.arange(-1, 1.1, 0.2))
ax_speed.set_yticks(np.arange(-1, 1.1, 0.2))
ax_speed.set_xlabel('Eixo X', fontsize=10)
ax_speed.set_ylabel('Eixo Y', fontsize=10)
ax_speed.set_title('Indicador de Velocidade', fontsize=10)

#indicador de atitude
ax_atitude.set_xlim(-1, 1)
ax_atitude.set_ylim(-1, 1)
ax_atitude.axis('off')
ax_atitude.grid(color='gray', linestyle='--', linewidth=0.5)
ax_atitude.set_xticks(np.arange(-1, 1.1, 0.2))
ax_atitude.set_yticks(np.arange(-1, 1.1, 0.2))
ax_atitude.set_xlabel('Eixo X', fontsize=10)
ax_atitude.set_ylabel('Eixo Y', fontsize=10)
ax_atitude.set_title('Indicador de Atitude', fontsize=10)

#configuração de bkAngle
ax_bkAngle.set_xlim(-1, 1)
ax_bkAngle.set_ylim(-1, 1)
ax_bkAngle.axis('off')
ax_bkAngle.grid(color='gray', linestyle='--', linewidth=0.5)
ax_bkAngle.set_xticks(np.arange(-1, 1.1, 0.2))
ax_bkAngle.set_yticks(np.arange(-1, 1.1, 0.2))
ax_bkAngle.set_xlabel('Eixo X', fontsize=10)
ax_bkAngle.set_ylabel('Eixo Y', fontsize=10)
ax_bkAngle.set_title('Indicador de Atitude', fontsize=10)

#confguração de direction
ax_direction.set_xlim(-1, 1)
ax_direction.set_ylim(-1, 1)
ax_direction.axis('off')
ax_direction.grid(color='gray', linestyle='--', linewidth=0.5)
ax_direction.set_xticks(np.arange(-1, 1.1, 0.2))
ax_direction.set_yticks(np.arange(-1, 1.1, 0.2))
ax_direction.set_xlabel('Eixo X', fontsize=10)
ax_direction.set_ylabel('Eixo Y', fontsize=10)
ax_direction.set_title('Indicador de Atitude', fontsize=10)

# Configuração do gráfico
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis('off')
ax.grid(color='gray', linestyle='--', linewidth=0.5)
ax.set_xticks(np.arange(-1, 1.1, 0.2))
ax.set_yticks(np.arange(-1, 1.1, 0.2))
ax.set_xlabel('Eixo X', fontsize=10)
ax.set_ylabel('Eixo Y', fontsize=10)
ax.set_title('Indicador de Atitude', fontsize=10)



# Elementos gráficos
horizon, = ax.plot([], [], 'b-', linewidth=2)  # Linha do horizonte
drone_body = ax.plot([-0.1, 0.1], [0, 0], 'r-', linewidth=3)[0]  # Drone (central)

# Conexão com o simulador
print("Conectando ao simulador...")
vehicle = connect('udp:192.168.12.113:14550', wait_ready=True)
print("Conexao estabelecida!")

def update_display(pitch, roll):
    """Atualiza o indicador de atitude"""
    roll_rad = math.radians(roll)
    x = np.linspace(-1, 1, 50)
    y = x * math.tan(roll_rad) - math.radians(pitch) * 0.5
    horizon.set_data(x, y)
    plt.draw()

try:
    print("Monitoramento ativo. Ctrl+C para sair.")
    while True:
        try:
            att = vehicle.attitude
            update_display(math.degrees(att.pitch), math.degrees(att.roll))
            plt.pause(0.02)  # ~50Hz
        except:
            time.sleep(0.1)
            continue

except KeyboardInterrupt:
    print("Encerrando...")
finally:
    vehicle.close()
    plt.close()
