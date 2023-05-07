import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [inputFile, setInputFile] = useState(null);
  const [outputFilename, setOutputFilename] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [outputVideoUrl, setOutputVideoUrl] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!inputFile || !outputFilename) {
      alert("Please select a video file and provide an output filename.");
      return;
    }
  
    let finalOutputFilename = outputFilename.endsWith(".mp4") ? outputFilename : outputFilename + ".mp4";
  
    setIsProcessing(true);
  
    const formData = new FormData();
    formData.append("inputVideo", inputFile);
    formData.append("outputFilename", finalOutputFilename);
  
    try {
      await axios.post("http://localhost:5000/anonymize", formData);
      const response = await axios.get(`http://localhost:5000/output_videos/${finalOutputFilename}`, {
        responseType: "blob",
      });
  
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", finalOutputFilename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };  

  const downloadVideo = () => {
    if (outputVideoUrl) {
      const link = document.createElement('a');
      link.href = outputVideoUrl;
      link.download = outputFilename;
      link.click();
    }
  };

  return (
    <div className="App">
      <div className="box"></div>
      <div className="inner-box">
        <h1 className="mb-4">AnoniMe</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="inputVideo" className="form-label">
              Input video
            </label>
            <input
              type="file"
              className="form-control custom-file-input"
              id="inputVideo"
              onChange={(e) => setInputFile(e.target.files[0])}
            />
          </div>
          <div className="mb-3">
          <label htmlFor="outputFilename" className="form-label">
              Output filename
            </label>
            <input
              type="text"
              className="form-control"
              id="outputFilename"
              value={outputFilename}
              onChange={(e) => setOutputFilename(e.target.value)}
            />
          </div>
          <div className="enter">
            <button type="submit" className="btn btn-primary" disabled={isProcessing}>
              {isProcessing ? "Processing..." : "Anonymize Video"}
            </button>
          </div>
        </form>

        {outputVideoUrl && (
          <div className="mt-4">
            <a href={outputVideoUrl} download className="btn btn-success">
              Download Output Video
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
