from moviepy.editor import VideoFileClip
import os

def compress_video(input_video, output_video, codec=''):
    clip = VideoFileClip(input_video)
    compressed_clip = clip.write_videofile(output_video, codec=codec)
    return compressed_clip

def get_file_size(file_path):
    return os.path.getsize(file_path)


if __name__ == "__main__":
    input_video_path = input("Enter the path of the input video file: ")
    output_dir = input("Enter the path of the output directory for compressed videos: ")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    output_video_h264_path = "compressed_h264.mp4"
    output_video_vp9_path = "compressed_vp9.mp4"
    h264_video_path = os.path.join(output_dir, output_video_h264_path)
    vp9_video_path = os.path.join(output_dir, output_video_vp9_path)
    #H.264
    compress_video(input_video_path,  h264_video_path, codec='libx264')
    print("H.264 Compression completed.")

    # VP9
    compress_video(input_video_path, vp9_video_path, codec='libvpx-vp9')
    print("VP9 Compression completed.")

    print("Compression process finished. Compressed videos saved in:", output_dir)

    # Comparaison des tailles
    h264_file_size = get_file_size(h264_video_path)
    vp9_file_size = get_file_size(vp9_video_path)

    print("\nFile sizes:")
    print("H.264:", h264_file_size, "bytes")
    print("VP9:", vp9_file_size, "bytes")

    # compression percentages
    original_file_size = get_file_size(input_video_path)
    h264_compression_percentage = (1 - (h264_file_size / original_file_size)) * 100
    vp9_compression_percentage = (1 - (vp9_file_size / original_file_size)) * 100

    print("\nCompression percentages compared to the original video:")
    print("H.264:", h264_compression_percentage, "%")
    print("VP9:", vp9_compression_percentage, "%")