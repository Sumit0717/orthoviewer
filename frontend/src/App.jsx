import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    if (file) setPreview(URL.createObjectURL(file));
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert("Select an image!");

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setUploadedFilename(res.data.filename);  // FIXED
    } catch (err) {
      console.error("Upload error:", err);
    }
  };

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>Orthoviewer</h2>
        <ul>
          <li className="active">Upload</li>
          <li>Annotate</li>
          <li>Superpixels</li>
          <li>Model</li>
          <li>Settings</li>
        </ul>
      </aside>

      <main className="main">
        <header className="topbar">
          <h1>Orthomosaic Annotation Platform</h1>
        </header>

        <section className="content">
          {/* Upload Card */}
          <div className="upload-card">
            <h3>Upload Orthomosaic Image</h3>

            <div className="upload-box">
              <input
                type="file"
                accept="image/*"
                id="file-input"
                onChange={handleFileChange}
              />
              <label htmlFor="file-input">Click or Drop Image Here</label>
            </div>

            {preview && (
              <div className="preview-box">
                <h4>Preview</h4>
                <img src={preview} alt="Preview" />
              </div>
            )}

            <button className="btn" onClick={handleUpload}>
              Upload
            </button>
          </div>

          {/* Show Uploaded File */}
          {uploadedFilename && (
            <div className="uploaded-card">
              <h3>Uploaded Image</h3>
              <img
                src={`http://127.0.0.1:5000/uploads/${uploadedFilename}`}
                alt="Uploaded"
              />
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
