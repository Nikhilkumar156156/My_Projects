import cv2
import imageio
import os

# === CONFIGURATION ===
video_path = r"D:\Nikhil Kumar\Weapons _ Official Trailer.mp4"  # 🔁 Change this
output_folder = "gifs"
gif_duration = 3      # seconds
interval = 20         # seconds
gif_fps = 10          # frames per second

# === SETUP ===
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
video_duration = total_frames / fps

print(f"Video FPS: {fps}, Total Duration: {video_duration:.2f} seconds")

# === EXTRACT GIFS ===
start_time = 0
gif_num = 1

while start_time + gif_duration < video_duration:
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)  # go to start time

    frames = []
    for _ in range(int(gif_duration * gif_fps)):
        ret, frame = cap.read()
        if not ret:
            break
        # Resize for smaller GIFs (optional)
        frame = cv2.resize(frame, (480, 270))  # Adjust size if needed
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)

    gif_path = os.path.join(output_folder, f"gif_{start_time}s.gif")
    imageio.mimsave(gif_path, frames, duration=1/gif_fps)
    print(f"✅ Saved {gif_path}")

    start_time += interval
    gif_num += 1

cap.release()
print("✅ All GIFs created successfully.")
