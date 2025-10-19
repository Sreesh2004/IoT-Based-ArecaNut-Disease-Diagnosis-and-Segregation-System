# IoT-Based Areca Nut Disease Diagnosis and Segregation System

<img width="1184" height="864" alt="Gemini_Generated_Image_otfoo5otfoo5otfo" src="https://github.com/user-attachments/assets/6990d117-4ac6-4ca4-be08-12db7c10c24a" />

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)]()
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Detection-green)]()
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3B%2B-red)]()
[![Status](https://img.shields.io/badge/Status-Prototype-yellow)]()



## 🚀 Project Overview

This project presents a **low-cost, IoT-enabled vision system** that automatically detects and classifies areca nuts as **healthy** or **diseased** using **YOLOv8**.  

It replaces manual sorting with an automated conveyor-based segregation setup and enables **remote operation via Ethernet communication** using **VNC Viewer** and **PuTTY**.



## 🎯 Objectives

- Detect and classify areca nuts using **real-time image processing**.  
- Automate sorting through a **conveyor mechanism** controlled by relays.  
- Enable **remote communication and monitoring** via **Ethernet (VNC Viewer + PuTTY)**.



## ⚙️ Problem Identification & Solution

| Problem | Proposed Solution |
|----------|------------------|
| Manual sorting is slow, inconsistent, and error-prone. | Introduce **automated vision-based classification** using CNN / YOLOv8. |
| Missed detection of subtle symptoms (Koleroga, nut borer, fungal issues). | Use **trained YOLOv8 model** on diverse dataset for reliable detection. |
| No affordable automation for small farmers. | Build **low-cost Raspberry Pi system** integrated with relay-based conveyor. |



## 🧩 System Architecture

  - Camera [USB Camera] --> Pi [Raspberry Pi 3B+]
  
  - Pi --> YOLO [YOLOv8 Model Inference]
  
  - YOLO --> Decision [Classification Logic]
  
  - Decision --> Relay [Relay Module]
  
  - Relay --> Motor [Conveyor Motor]
  
  - Pi --> |Ethernet| VNC [VNC Viewer (Remote Desktop)]
  
  - Pi --> |Ethernet| PuTTY [PuTTY (SSH Control)]



## 💡 YOLOv8 Architecture (Simplified)

<img width="1400" height="650" alt="Gemini_Generated_Image_n2pkfkn2pkfkn2pk" src="https://github.com/user-attachments/assets/d3ab6179-b566-458f-b26c-00b9a937837c" />

  - A [Input Image 640×640] --> B [Backbone (CSPDarknet)]
  
  - B --> C [Neck (PAN-FPN)]
  
  - C --> D [Head (Detection Layers)]
  
  - D --> E [Bounding Boxes + Class Probabilities]

 **Subgraph Details**
 
    B --> | C2f + Conv Layers | F[Feature Extraction]
    
    C --> | Multi-scale Fusion | G[Feature Pyramid]
    
    D --> | 3 Scales | H[Small / Medium / Large Object Detection]



## 🔌 IoT Communication (Ethernet)

- VNC Viewer → remote GUI access to Raspberry Pi desktop.

- PuTTY (SSH) → terminal-based control, monitoring, and file transfer.

- Ethernet ensures reliable connectivity and low latency compared to Wi-Fi.



## 🧠 Hardware Setup

- Raspberry Pi 3 Model B+

- USB Camera (≥ 640x480 p)

- Conveyor mechanism

- Relay module

- Gear motor (DC)

- Power supply (12 V)

- Ethernet cable for communication



## 💻 Software Stack

- Python 3.11 +

- YOLOv8 (Ultralytics)

- TensorFlow / OpenCV

- Raspberry Pi OS 64 Bit 

- Google Colab (for training) --> https://colab.research.google.com/drive/1y_Pll2h5nWtQkqxRwwx6mqZJzxmFDZtM?usp=drive_link

- VNC Viewer and PuTTY (for Ethernet control)



## 📊 Dataset & Performance

Dataset Size: ~2700 areca nut images
Classes: Healthy / Unhealthy

| Class          | Precision(%) | Recall(%) | F1-Score(%) |
| -------------- | --------- | ------ | -------- |
| Healthy Nuts   | 0.90      | 0.95   | 0.92     |
| Unhealthy Nuts | 0.93      | 0.91   | 0.92     |
| Accuracy       | —         | —      | 0.93     |
| Macro Avg      | 0.92      | 0.93   | 0.92     |
| Weighted Avg   | 0.92      | 0.93   | 0.93     |



## 🎯 Accuracy & Confusion Matrix

<img width="618" height="550" alt="image" src="https://github.com/user-attachments/assets/cb112047-be81-4db2-8308-a06261d170dd" />            <img width="661" height="547" alt="image" src="https://github.com/user-attachments/assets/a41856c4-0b31-44b3-9687-8d37c679994c" />

<img width="618" height="550" alt="image" src="https://github.com/user-attachments/assets/d429bd03-f0f2-412e-a0f9-4b6b5382b7db" />



## 🔄 Workflow Summary

<img width="666" height="818" alt="image" src="https://github.com/user-attachments/assets/8ab450e8-0733-4c16-b300-eb2c55f548cf" />

- Image captured by USB Camera.

- YOLOv8 performs detection & classification.

- Decision logic triggers corresponding relay output.

- Motor drives conveyor to segregate nuts.

- System accessible remotely via Ethernet (VNC Viewer + PuTTY).



## 🧩 Block Diagram

<img width="1000" height="678" alt="image" src="https://github.com/user-attachments/assets/3062de8e-ab0e-423a-8fa9-a1d0bad664d2" />

  - A[Camera] --> B[Raspberry Pi 3B+]
  
  - B --> C[YOLOv8 Detection]
  
  - C --> D[Classification Output]
  
  - D --> E[Relay Control]
  
  - E --> F[Motor/Conveyor]
  
  - B -->|Ethernet| G[VNC Viewer + PuTTY]



## 🌱 Sustainable Development Goals

**SDG	Target	Relevance**

<img width="175" height="166" alt="image" src="https://github.com/user-attachments/assets/eef56d01-ba67-40f5-876a-124ac93c2319" />


**SDG 9	Upgrade infrastructure & retrofit industries for sustainability.	Integrates IoT + AI in rural agro-processing.**

<img width="175" height="166" alt="image" src="https://github.com/user-attachments/assets/70c7cab2-2016-4bb7-95b8-6af05244de7d" />


**SDG 12	Halve global food waste by 2030.	Reduces post-harvest losses via automated disease removal.**



## ⚙️ System Status & Conveyor Setup

<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/e8e4deee-a966-424e-b7ff-b89ee1f6fa7b" />      <img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/36ed4aa1-5d2e-425b-9b46-ea881d0c553f" />

<img width="738" height="526" alt="image" src="https://github.com/user-attachments/assets/b506af88-721b-456e-89ad-39e0aadc39d7" />



## 🧭 Scope & Innovation

Combines camera-based detection, YOLOv8 inference, and IoT Ethernet connectivity.

Affordable and scalable for small to mid-sized areca nut processors.

Promotes sustainable rural automation and improved product quality.



## 📚 References

Rajendra A. B. et al., Areca Nut Disease Detection Using Image Processing, Soft Computing Applications (2020).

Anilkumar M G et al., Detection of Diseases in Arecanut Using CNN, IRJET (2021).

Mitra S. K. & Devi H., Arecanut in India – Present Situation and Prospects, ISTTH (2016).

Kanan L. V. et al., Arecanut Yield Disease Forecast Using IoT and ML, IJSRET (2021).

Zeng G., Fruit and Vegetables Classification Using CNN, IEEE ITOEC (2017).



## ✉️ Contact

Created by SREESH T N 

For queries: sreesh2004@gmail.com

