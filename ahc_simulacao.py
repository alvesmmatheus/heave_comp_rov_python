
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parâmetros do sistema (modelo simplificado)
D = 50e-6        # Deslocamento volumétrico [m^3/rad]
K_valve = 1e7    # Ganho hidráulico simplificado (u -> torque)
J = 5.0          # Inércia [kg.m²]
b = 2.0          # Atrito viscoso [N.m.s/rad]
deadzone = 0.1   # Zona morta
dt = 0.01
t_final = 20.0
t = np.arange(0, t_final, dt)
y0 = [0.0, 0.0]  # posição, velocidade

def gerar_heave(t, tipo="calmo", seed=42):
    rng = np.random.default_rng(seed)
    if tipo == "calmo":
        return 1.0 * np.sin(2 * np.pi * 0.1 * t) + 0.02 * rng.standard_normal(len(t))
    elif tipo == "medio":
        return 1.5 * np.sin(2 * np.pi * 0.2 * t) + 0.05 * rng.standard_normal(len(t))
    elif tipo == "agitado":
        swell = 2.0 * np.sin(2 * np.pi * 0.25 * t)
        ruido = 0.2 * rng.standard_normal(len(t))
        rajada = 0.5 * np.sin(2 * np.pi * 1.5 * t)
        return swell + ruido + rajada
    else:
        raise ValueError("tipo de mar inválido")

class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.int_error = 0.0
        self.prev_error = 0.0

    def compute(self, error, dt):
        self.int_error += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.kp*error + self.ki*self.int_error + self.kd*derivative

pid = PID(kp=5e4, ki=2e3, kd=1e4)

def modelo_ahc(t_now, y, ref_signal):
    theta, omega = y
    idx = min(int(t_now / dt), len(ref_signal) - 1)
    error = ref_signal[idx] - theta
    u = pid.compute(error, dt)
    if abs(u) < deadzone:
        torque = 0.0
    else:
        torque = D * K_valve * (u - np.sign(u)*deadzone)
        torque = np.clip(torque, -100.0, 100.0)  # saturação
    domega = (torque - b * omega) / J
    dtheta = omega
    return [dtheta, domega]

# --------- Escolha do cenário ---------
cenario = "calmo"  # "calmo", "medio" ou "agitado"

heave = gerar_heave(t, cenario)
sol = solve_ivp(modelo_ahc, [0, t_final], y0, t_eval=t, args=(heave,), method='RK45')
theta = sol.y[0]

# --------- Plot ---------
plt.figure(figsize=(10, 6))
plt.plot(t, heave, label="MRU (referência)")
plt.plot(t, theta, label="Posição da TMS")
plt.title(f"Simulação AHC – Mar {cenario.capitalize()}")
plt.xlabel("Tempo [s]")
plt.ylabel("Deslocamento [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
