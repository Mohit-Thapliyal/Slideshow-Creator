from flask import Flask, request, jsonify
import os
import requests
from PIL import Image
import cv2
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

#download
def download_image_from_url(url, folder_path):
        # Send a GET request to the provided URL
        response = requests.get(url)
        
        # Check if the response is successful
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            
            # Verify if the response contains image data
            if 'image' in content_type:
                image_data = response.content
                image_extension = os.path.splitext(url)[1]
                
                # Generate a unique image filename and save it in the specified folder
                image_filename = os.path.join(folder_path, f'image_{os.urandom(4).hex()}{image_extension}')
                with open(image_filename, 'wb') as f:
                    f.write(image_data)
                print("Image downloaded successfully.")
                return image_filename

def download_images_from_url(downloaded_images, image_urls, folder_path):
    # Create the download folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Loop through each image URL and download the images
    for url in image_urls:
        image_filename = download_image_from_url(url, folder_path)
        
        if image_filename:
            downloaded_images.append(image_filename)
        
#resize
def resize_image(input_path, output_path, new_width, new_height):
    try:
        # Open the image
        img = Image.open(input_path)

        # Convert to RGB mode
        img = img.convert("RGB")
        
        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.BILINEAR)
        # resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Save the resized image
        # resized_img.save(output_path)
        resized_img.save(output_path, format="JPEG", quality=90)
        # resized_img.save(output_path, format="PNG")
        
        print("Image resized successfully.")
    except Exception as e:
        print("Error resizing image:", e)

def resize_images_in_folder(input_folder, output_folder, new_width, new_height):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Loop through images in the input folder
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)
                resize_image(input_path, output_path, new_width, new_height)
    except Exception as e:
        print("Error processing images:", e)

#convert
def convert_images_to_jpeg(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.png')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpeg')

            img = Image.open(input_path)
            img.save(output_path, 'JPEG')
            print("Image converted successfully.")

#create video
def create_video_from_images(image_folder, video_name, time_in_between):
    # Frames per second for the output video
    fps = 1

    # Duration (in seconds) for each image in the video
    image_duration = time_in_between  # Change this value as needed

    # Get a list of image filenames in the specified folder
    images = [img for img in os.listdir(image_folder) if img.endswith('.jpeg')]

    # Read the first image to get dimensions
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the video codec (change it based on your requirements)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create a VideoWriter object to write the video
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Loop through the list of image filenames and add them to the video
    for image in images:
        # img_path = os.path.join(image_folder, image)
        # video.write(cv2.imread(img_path))  # Add the current image to the video
        # # Calculate the number of frames needed for the desired duration
        # num_frames = int(fps * image_duration)
        img_path = os.path.join(image_folder, image)
        img = cv2.imread(img_path)
        
        # Calculate the number of frames needed for the desired duration
        num_frames = int(fps * image_duration)
        
        # Add the same image multiple times to represent the desired duration
        for _ in range(num_frames):
            video.write(img)
    print("Video created successfully.")

    # Release the VideoWriter and close any OpenCV windows
    video.release()
    cv2.destroyAllWindows()

#upload video
def upload_video_to_cloudinary():
    # Configure Cloudinary (replace 'cloud_name', 'api_key', and 'api_secret' with your Cloudinary credentials)
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    # Upload the video
    video_file_path = 'video.mp4'
    upload_result = cloudinary.uploader.upload(video_file_path, resource_type='video')

    # Display the URL of the uploaded video
    video_url = upload_result['secure_url']
    print("Video uploaded to cloudinary successfully.")
    print("Uploaded Video URL:", video_url)
    return video_url

#empty file=
def delete_all_files_in_folder(folder_paths):
    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        print("Folder emptied successfully.")
    os.remove("video.mp4")
    print("Video delted successfully.")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>You can create video from image urls</p>"

@app.route('/create_video', methods=['POST'])
def create_video():
    try:
        data = request.get_json()
        
        if 'image_urls' in data:
            image_urls = data['image_urls']
            time_in_between = 2
            if 'time_in_between' in data:
                time_in_between = data['time_in_between']
            downloaded_images = []
            
            # Download images from url
            download_images_from_url(downloaded_images, image_urls, './downloaded_photos')

            # Resize downloaded images
            resize_images_in_folder('downloaded_photos', 'resized_photos', 2800, 1600)

            # Convert images to JPEG format
            convert_images_to_jpeg('resized_photos', 'converted_photos')

            # Create a video from the converted images
            create_video_from_images('converted_photos', 'video.mp4', time_in_between)

            # Upload Video to cloudinary
            video_url = "dummy_url"
            video_url = upload_video_to_cloudinary()
            # upload_video_to_cloudinary()

            # Empty folders
            delete_all_files_in_folder(["downloaded_photos",'resized_photos','converted_photos'])

            # Return success response with downloaded image filenames
            return jsonify({"message": "Video generated successfully", "video_url": video_url})
        else:
            return jsonify({"error": "Missing 'image_urls' in the request data"}), 400

    except Exception as e:
        # Handle any exceptions that might occur during image download or processing
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
