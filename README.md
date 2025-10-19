# IoT-Based Areca Nut Disease Diagnosis and Segregation System

<img width="1184" height="864" alt="Gemini_Generated_Image_otfoo5otfoo5otfo" src="https://github.com/user-attachments/assets/6990d117-4ac6-4ca4-be08-12db7c10c24a" />

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)]()
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Detection-green)]()
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3B%2B-red)]()
[![Status](https://img.shields.io/badge/Status-Prototype-yellow)]()

---

## 🚀 Project Overview

This project presents a **low-cost, IoT-enabled vision system** that automatically detects and classifies areca nuts as **healthy** or **diseased** using **YOLOv8**.  
It replaces manual sorting with an automated conveyor-based segregation setup and enables **remote operation via Ethernet communication** using **VNC Viewer** and **PuTTY**.

---

## 🎯 Objectives

- Detect and classify areca nuts using **real-time image processing**.  
- Automate sorting through a **conveyor mechanism** controlled by relays.  
- Enable **remote communication and monitoring** via **Ethernet (VNC Viewer + PuTTY)**.

---

## ⚙️ Problem Identification & Solution

| Problem | Proposed Solution |
|----------|------------------|
| Manual sorting is slow, inconsistent, and error-prone. | Introduce **automated vision-based classification** using CNN / YOLOv8. |
| Missed detection of subtle symptoms (Koleroga, nut borer, fungal issues). | Use **trained YOLOv8 model** on diverse dataset for reliable detection. |
| No affordable automation for small farmers. | Build **low-cost Raspberry Pi system** integrated with relay-based conveyor. |

---

## 🧩 System Architecture

flowchart LR
  Camera[USB Camera] --> Pi[Raspberry Pi 3B+]
  Pi --> YOLO[YOLOv8 Model Inference]
  YOLO --> Decision[Classification Logic]
  Decision --> Relay[Relay Module]
  Relay --> Motor[Conveyor Motor]
  Pi -->|Ethernet| VNC[VNC Viewer (Remote Desktop)]
  Pi -->|Ethernet| PuTTY[PuTTY (SSH Control)]

---

💡 YOLOv8 Architecture (Simplified)
<img width="1472" height="704" alt="Gemini_Generated_Image_n2pkfkn2pkfkn2pk" src="https://github.com/user-attachments/assets/d3ab6179-b566-458f-b26c-00b9a937837c" />
flowchart TD
  A[Input Image 640×640] --> B[Backbone (CSPDarknet)]
  B --> C[Neck (PAN-FPN)]
  C --> D[Head (Detection Layers)]
  D --> E[Bounding Boxes + Class Probabilities]
  subgraph Details
    B -->|C2f + Conv Layers| F[Feature Extraction]
    C -->|Multi-scale Fusion| G[Feature Pyramid]
    D -->|3 Scales| H[Small / Medium / Large Object Detection]
  end

---

