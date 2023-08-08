
# Sliedshow Creator

An API that can create video from image URLs.




## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`CLOUDINARY_CLOUD_NAME`

`CLOUDINARY_API_KEY`

`CLOUDINARY_API_SECRET`


## Run Locally

Clone the project

```bash
  git clone https://github.com/Mohit-Thapliyal/Slideshow-Creator.git
```

Go to the project directory

```bash
  cd Slideshow-Creator
```

Create and activate a virtual environment (For Mac)

```bash
  python3 -m venv venv
  source venv/bin/activate
```

Install dependencies

```bash
  pip install cloudinary flask opencv-python pillow requests python-dotenv
```

Start the server

```bash
  python app.py
```


## Usage/Examples

API endpoint (Post API)
```json
http://localhost:3000/create_video
```

Body JSON
```json
{
  "image_urls": [
    "https://mohitthapliyal.in/static/media/bloggy.79dda9c2b006dfe70112.png",
    "https://mohitthapliyal.in/static/media/formGenerator.0c9d15b1397af26ffc42.jpeg",
    "https://mohitthapliyal.in/static/media/reunion.2d59b952b6aae8231f05.jpeg",
    "https://mohitthapliyal.in/static/media/project6.456c944cb03cb40bed61.jpg",
    "https://mohitthapliyal.in/static/media/AirBnb.a7053457e6ecb1ad2268.jpeg"
  ],
  "time_in_between": 3
}
```
Api Response

```json
{
  "message": "Video generated successfully",
  "video_url": "https://res.cloudinary.com/dcrevsijx/video/upload/v1691522416/lvgvfnvs4uukz6iijk4a.mp4"
}
```
