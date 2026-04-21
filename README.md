<p align="center">
  <img src="docs/images/cover.png" width="740"/>
</p>

# Access Control System — RFID Anomaly Detection

---

## The problem

Standard RFID access control grants entry to anyone who holds the correct card — a stolen or cloned card is indistinguishable from the legitimate owner. Physical security systems need a second layer that doesn't require a PIN or biometric scanner.

---

## The approach

Every legitimate cardholder has a unique behavioural pattern: they tap at roughly the same times of day, hold the card the same way, and approach the reader at a characteristic speed. A system that has learned this pattern can flag entries that look out of place — without ever needing labelled attacker data.

This project pairs an RFID reader with a **Time-of-Flight distance sensor** to capture the full approach profile of each tap, then trains unsupervised anomaly detection models on the owner's data alone.

---

## Data

Two datasets were collected:

**Phase 1 — Synthetic** — generated from real dormitory access statistics to validate the approach before hardware measurements were available.

**Phase 2 — Real captures** — 20 taps each from two real individuals. Training uses one person's taps; the other person's taps act as the attack set.

Each dataset is split 70 / 30 into training (owner only) and test sets.

---

## Features

Each tap produces:

| Feature | What it captures |
|---|---|
| `time_of_day` | Time encoded cyclically (23:59 → 00:00 is continuous) |
| `day_of_week` | Day encoded cyclically |
| `rfid_hold_duration_ms` | How long the card was held against the reader |
| `tof_*` | Approach speed, min/max/mean/std distance, approach distance |

<img src="docs/images/tap_distribution.png" width="740"/>

The owner taps consistently around **08:00** and **18:00** — a clear daily rhythm the models can learn.

---

## Models

All models train exclusively on legitimate owner data.

<img src="docs/images/isolation_forest_owner.png" width="740"/>

The red-shaded region is learned as anomalous — entries outside the owner's normal time windows are flagged regardless of day.

<img src="docs/images/isolation_forest_attack.png" width="740"/>

On the attack dataset the same boundary catches the majority of intruder taps.

---

## Results

| Method | FRR | FAR | Notes |
|---|---|---|---|
| Threshold ±1 h (baseline) | 28.95 % | 26.67 % | Median tap time + fixed window |
| Isolation Forest | 13.16 % | 26.67 % | Time features only |
| One-Class SVM | 23.68 % | 2.22 % | |
| Local Outlier Factor | 10.53 % | 13.33 % | |
| **Neural Network (autoencoder)** | **2.63 %** | **4.44 %** | Time + ToF features, fused branches |

The autoencoder reconstructs normal entry sequences; inputs with reconstruction error above the 95th-percentile training threshold are flagged as anomalies.

---

## Notebooks

| File | Language | Description |
|---|---|---|
| `01_synthetic_data.ipynb` | Slovak | Phase 1 — synthetic data |
| `01_synthetic_data_en.ipynb` | English | Phase 1 — synthetic data |
| `02_real_data.ipynb` | Slovak | Phase 2 — real captures |
| `02_real_data_en.ipynb` | English | Phase 2 — real captures |

Full written report: [`docs/`](docs/)

---

## Stack

Python · scikit-learn · pandas · NumPy · Matplotlib · Jupyter
