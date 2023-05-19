# README

## Video Anonymizer - Face Blur

### Dependencies

Before running the project, make sure to install the following dependencies:

#### Python Dependencies

Run the following command to install the required Python packages:

```
pip install -r requirements.txt
```

#### Node.js and React

Make sure you have Node.js installed. You can download it from [here](https://nodejs.org/en/download/).

Next, navigate to the `client` folder and install the required packages:

``` 
cd client
npm install
```

### Running the Web App

To run the web app, you will need to start both the frontend and backend servers.

#### Backend Server

Navigate to the `server` folder and run the following command to start the Flask API server:
```
cd server
python api.py
```

The Flask API server will start on `http://localhost:5000`.

#### Frontend Server

Create a new command prompt or terminal window. Navigate to the `client` folder and run the following command to start the React app:

```
cd client
npm start
```

The React app will start on `http://localhost:3000`. Open this URL in your browser to use the Video Anonymizer web app.

### Running Face Blur Standalone

To run the face blur script without the web app, simply execute the `face_blur.py` script:
```
python face_blur.py
```

When prompted, enter the path to the input video file. The output video will be saved in the `output_videos` folder as `output_video.mp4`.

## File Structure
```
CS-445-Final-Project/
├── client/ # React app
│ ├── ...
│ └── src/
│ └── App.js
└── server/ # Flask API
├── input_videos/
├── output_videos/
├── api.py
└── face_blur.py
```

## Usage

For the web app, upload an input video file and provide an output filename. Click on the "Anonymize Video" button to process the video. After processing, the output video will download automatically.

For the standalone `face_blur.py`, provide the input video file path when prompted. The output video will be saved in the `output_videos` folder as `output_video.mp4`.
