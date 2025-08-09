
# Active Heave Compensation (AHC) para ROV – Simulação em Python

📄 [Baixar o estudo completo em PDF](Estudo_AHC_Python.pdf)

## 1. Introdução
Em operações offshore com ROVs (*Remotely Operated Vehicles*), o movimento vertical da embarcação causado por ondas — *heave* — é transmitido à **TMS** (*Tether Management System*) pelo umbilical. Esse movimento pode gerar variações bruscas de tensão no cabo, afetar manobras de acoplamento/desacoplamento do ROV e aumentar o desgaste do sistema.

O **Active Heave Compensation (AHC)** é um sistema de controle que atua no **guincho do LARS** para comandar o *payout* do cabo de forma a compensar o *heave* do navio, mantendo a **TMS praticamente estacionária** na coluna d’água em relação ao fundo. Embora o AHC não estabilize o ROV diretamente, ele reduz picos de tração e deslocamentos indesejados, contribuindo para operações mais seguras e eficientes.

Este estudo apresenta um **modelo simplificado** de AHC implementado em **Python**, com foco na modelagem da malha de controle e na análise de desempenho em diferentes condições de mar.

---

## 2. Arquitetura do Sistema
O modelo representa a malha de controle de forma simplificada:

- **MRU**: Mede o deslocamento vertical do navio. No modelo, é o sinal sintético de *heave*. Na prática, MRUs usam IMUs (acelerômetros/giroscópios) com filtragem e algoritmos de fusão sensorial.
- **Controlador PID**: Calcula o comando de torque para compensar o *heave*, com ganhos \(K_p\), \(K_i\) e \(K_d\).
- **Válvula proporcional**: Converte o comando elétrico em torque hidráulico, considerando zona morta e saturação.
- **Guincho**: Modelado como um sistema de 2ª ordem com inércia \(J\) e atrito viscoso \(b\).
- **Encoder**: Mede a posição da TMS (ponto de *payout* do cabo) para fechar a malha de controle.

Diagrama de Blocos do sistema:

![Diagrama de Blocos](Diagrama_Simplificado.png)


---

## 3. Resultados
**Gráficos** (exemplos gerados):
- `plot_ahc_calmo_anotado.png`
- `plot_ahc_medio_anotado.png`
- `plot_ahc_agitado_anotado.png`

![Mar calmo](plot_ahc_calmo_anotado.png)
![Mar médio](plot_ahc_medio_anotado.png)
![Mar agitado](plot_ahc_agitado_anotado.png)

**Resumo qualitativo:**
- Mar calmo: rastreamento quase perfeito.
- Mar médio: pequeno atraso, sistema estável.
- Mar agitado: limitação de torque + zona morta → desempenho reduzido.

> *Nota:* Caso queira computar RMS no próprio script, calcule `rms = np.sqrt(np.mean((heave - theta)**2))` após a integração.

---

## 4. Como rodar
```bash
# criar venv (opcional)
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate

# instalar deps
pip install -r requirements.txt

# escolher cenário no código (calmo | medio | agitado)
python ahc_simulacao.py
```

---

## 5. Estrutura do Projeto
```text
ahc-rov-sim/
├── ahc_simulacao.py
├── Diagrama_Simplificado.png
├── plot_ahc_calmo_anotado.png
├── plot_ahc_medio_anotado.png
├── plot_ahc_agitado_anotado.png
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 6. Licença
Livre para uso educacional e demonstração de portfólio.
