import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from picamera2 import Picamera2, controls
import cv2
import numpy as np
import threading
from ultralytics import YOLOWorld
import time

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1024x580+350+100")
        
        self.video_label = tk.Label(self.main_window, bg='black')
        self.video_label.place(x=0, y=80, width=640, height=480)

        self.capture_button = tk.Button(self.main_window, text='RESMİ ÇEK', bg='green', width=40, height=5, command=self.capture_image)
        self.capture_button.place(x=650, y=350)

        self.reset_button = tk.Button(self.main_window, width=40, height=5, text='Reset', bg='gray', fg='black', command=self.reset)
        self.reset_button.place(x=650, y=450)

        self.label_id = tk.Label(self.main_window, text='G191210014', fg='white', bg='red', font=('Helvetica', 30))
        self.label_id.place(relx=0.5, rely=0.05, anchor='n')

        self.label_prompt = tk.Label(self.main_window, text='Bir Nesne Giriniz:')
        self.label_prompt.place(x=650, y=230)

        self.entry_object = tk.Entry(self.main_window, width=40)
        self.entry_object.place(x=650, y=250)

        self.label_object_count = tk.Label(self.main_window, font=('Helvetica', 20))
        self.label_object_count.place(x=650, y=200)

        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start()

        self.update_video = True
        self.update_video_feed()

    def update_video_feed(self):
        if self.update_video:
            frame = self.picam2.capture_array()
            frame = self.improve_image_quality(frame)
            image = Image.fromarray(frame)
            self.image_tk = ImageTk.PhotoImage(image)
            self.video_label.imgtk = self.image_tk
            self.video_label.configure(image=self.image_tk)
            self.main_window.after(30, self.update_video_feed)

    def improve_image_quality(self, frame):

        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        frame = cv2.filter2D(frame, -1, kernel)
        return frame

    def capture_image(self):
        print("Fotoğraf çekiliyor...")
        self.update_video = False 
        frame = self.picam2.capture_array()
        frame = self.improve_image_quality(frame)
        cv2.imwrite("/home/ssypi/aa.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        
        self.show_detection_text()

        self.label_prompt.place_forget()
        self.entry_object.place_forget()
        self.capture_button.place_forget()

        threading.Thread(target=self.run_yolo_and_show_results).start()

    def show_detection_text(self):
        self.video_label.config(image='', text='')

        self.detection_frame = tk.Frame(self.video_label, bg='black')
        self.detection_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.detection_text_label = tk.Label(self.detection_frame, text="Nesne tespit ediliyor", font=('Helvetica', 20), fg='white', bg='black')
        self.detection_text_label.pack(side=tk.TOP, pady=10)

        self.loading_gif = Image.open("loading2.gif")
        self.loading_frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(self.loading_gif)]
        self.loading_label = tk.Label(self.detection_frame, bg='black')
        self.loading_label.pack(side=tk.TOP)
        self.animate_loading(0)

    def animate_loading(self, frame):
        self.loading_label.config(image=self.loading_frames[frame])
        frame = (frame + 1) % len(self.loading_frames)
        self.main_window.after(100, self.animate_loading, frame)

    def run_yolo_and_show_results(self):
        model = YOLOWorld("/home/ssypi/yolov8x-world.pt")  

        object_class = self.entry_object.get().strip()
        if object_class:
            model.set_classes([object_class])
        else:
            model.set_classes([])  

        results = model.predict('/home/ssypi/aa.jpg', max_det=100, iou=0.01, conf=0.01)
        self.show_captured_image(results[0], object_class)

    def show_captured_image(self, yolo_result, object_class):

        captured_image = cv2.imread("/home/ssypi/aa.jpg")
        for box in yolo_result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(captured_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(captured_image, object_class, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        image = Image.fromarray(cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB))
        self.image_tk = ImageTk.PhotoImage(image)
        self.video_label.imgtk = self.image_tk
        self.video_label.configure(image=self.image_tk, text='')

        object_count = len(yolo_result.boxes)
        self.label_object_count.config(text=f'Nesne Sayısı = {object_count}')

        self.detection_frame.destroy()

    def reset(self):
        print("Resetting application...")
        self.update_video = False
        self.entry_object.delete(0, tk.END)
        self.label_object_count.config(text=' ') 
        self.picam2.stop()

        time.sleep(1)
        
        self.picam2.start()
        self.update_video = True
        self.update_video_feed()  

        self.label_prompt.place(x=650, y=230)
        self.entry_object.place(x=650, y=250)
        self.capture_button.place(x=650, y=350)

    def save_image_to_database(self):
        print("Fotoğraf veri tabanına kaydediliyor...")
        # vt işlemleri

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
