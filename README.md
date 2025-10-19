# IoT-Based-ArecaNut-Disease-Diagnosis-and-Segregation-System

![Project Banner](./banner.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)]()
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)]()
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3B%2B-green)]()
[![Status](https://img.shields.io/badge/Status-Prototype-red)]()

---

## 🚀 Project Overview

**IoT-Based Areca Nut Disease Diagnosis and Segregation System** is an integrated hardware + software solution that automatically detects diseases on areca nuts using computer vision (CNN), classifies them, and actuates a conveyor-driven segregation system — all monitored remotely via IoT.

This repo contains: dataset preparation scripts, model training code, Raspberry Pi inference scripts, and microcontroller (relay/motor) control logic.

---

## ✨ Key Features

- Real-time disease detection using a CNN model (TensorFlow / Keras).
- Automated conveyor segmentation with relay control.
- Remote monitoring and alerts via IoT dashboard (Blynk or similar).
- Lightweight inference optimized for Raspberry Pi 3B+ (or similar).
- Modular: swap model, dataset, or hardware easily.

---

## 🧩 System Architecture

```mermaid
flowchart LR
  Camera[USB Camera] --> RP(Raspberry Pi 3B+)
  RP -->|Image Preproc| Model[Inference: CNN Model]
  Model -->|Class Label| Decision[Segregation Logic]
  Decision --> Relay[Relay Module]
  Relay --> Motor[Conveyor Motor]
  RP --> IoT[IoT Dashboard (Blynk/MQTT)]
  IoT --> User[User Mobile/Web App]


