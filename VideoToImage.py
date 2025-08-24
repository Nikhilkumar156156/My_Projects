import cv2
import os

# ✅ Safe path: use raw string with r''
video_path = r'D:\Nikhil Kumar\New Project.mp4'

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Failed to open video.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
interval_sec = 60
interval_frames = int(fps * interval_sec)

# ✅ Save to the right folder
output_folder = 'frames5'
os.makedirs(output_folder, exist_ok=True)

frame_num = 0
saved = 0

while frame_num < total_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        print(f"⚠️ Failed to read frame at {frame_num}")
        break
    cv2.imwrite(f'{output_folder}/frame_{saved:04d}.jpg', frame)
    saved += 1
    frame_num += interval_frames

cap.release()
print(f"✅ Saved {saved} frames to '{output_folder}' every {interval_sec} seconds.")
