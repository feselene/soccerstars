import os
import cv2
from pytube import YouTube
from PIL import Image

def download_youtube_video(video_url, output_path="downloaded_video.mp4"):
    """Downloads a YouTube video to the specified path."""
    print(f"Downloading video from {video_url}...")
    yt = YouTube(video_url)
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
    video_path = os.path.join(os.getcwd(), output_path)
    video_stream.download(filename=video_path)
    print(f"Video downloaded successfully at {video_path}")
    return video_path

def extract_frames_evenly(video_path, output_dir="frames", frame_count=100):
    """Extracts frames evenly spaced from the video."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Extracting {frame_count} frames evenly from video {video_path}...")
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, total_frames // frame_count)  # Calculate frame interval to get 100 frames
    
    print(f"Video has {total_frames} total frames. Extracting 1 frame every {frame_interval} frames.")
    
    frame_number = 0
    extracted_frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret or extracted_frame_count >= frame_count:
            break
        
        if frame_number % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{extracted_frame_count:03d}.png")
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image)
            img.save(frame_filename)
            print(f"Saved frame {extracted_frame_count + 1}/{frame_count} at {frame_filename}")
            extracted_frame_count += 1
        
        frame_number += 1
    
    cap.release()
    print(f"Successfully extracted {extracted_frame_count} frames to {output_dir}.")

def main():
    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE"
    video_path = download_youtube_video(video_url)
    extract_frames_evenly(video_path, output_dir="frames", frame_count=100)

if __name__ == "__main__":
    main()
