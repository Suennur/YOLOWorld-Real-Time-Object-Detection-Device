# 🎯 YOLOWorld Real-Time Object Detection Device on Raspberry Pi

This project implements a **real-time object detection system on a Raspberry Pi 5**, using a YOLOWorld model integrated with a camera and display. The device allows the user to enter custom text, performs object detection on the live camera feed, and displays the detection results instantly on a connected screen.

---

## 🚀 Key Features

- Real-time object detection using **YOLOWorld** at 30 FPS on Raspberry Pi 5.
- Integrated user interface built with **Tkinter** for easy text input and result display.
- High detection accuracy with minimal latency.
- Fully portable, low-power device suitable for in-vehicle, drone, or mobile applications.
- Easy to use with a simple and intuitive GUI.

---

## 🛠️ Hardware and Software

- **Hardware:**
  - Raspberry Pi 5
  - Raspberry Pi Infrared Camera Module V2.1
  - Waveshare 7” HDMI Display

- **Software:**
  - Raspberry Pi OS
  - Python 3
  - YOLOWorld model (yoloworld.pt)

- **Python Libraries:**
  - tkinter
  - PIL & ImageTk
  - picamera2
  - numpy
  - threading
  - opencv-python
  - ultralytics

---

## 📸 How It Works
The user enters a custom text prompt through the Tkinter GUI.

The Raspberry Pi camera captures the live video feed.

YOLOWorld model detects objects matching the user’s prompt in real-time.

Detection results are overlaid on the video and displayed on the connected HDMI screen.

![image](https://github.com/user-attachments/assets/f297038d-d252-4fd2-8997-9971253ab821)

![image](https://github.com/user-attachments/assets/99d05d40-296c-45e4-a903-f2a8f2c61cac)

![image](https://github.com/user-attachments/assets/eb4d70b3-a6af-4a42-a669-372327cd89e8)



---

🤝 Contact

Developed by Suennur Altaş

📫 Email: suennur.altas@gmail.com

🔗 [LinkedIn](https://www.linkedin.com/in/suennur-altas000/) | [GitHub](https://github.com/Suennur)
