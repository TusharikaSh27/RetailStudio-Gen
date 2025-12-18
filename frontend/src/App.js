import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import Editor from "./Editor"; // ⭐ NEW

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingStep, setLoadingStep] = useState("");
  const [creatives, setCreatives] = useState([]);
  const [processedImg, setProcessedImg] = useState("");
  const [tagline, setTagline] = useState("");
  const [offer, setOffer] = useState("");
  const [dark, setDark] = useState(false);
  const [fullscreenImg, setFullscreenImg] = useState(null);
  const [carousel, setCarousel] = useState(false);

  // ⭐ EDITOR STATE
  const [editorOpen, setEditorOpen] = useState(false);
  const [editorSrc, setEditorSrc] = useState(null);

  const handleUpload = async () => {
    if (!selectedFile) return alert("Please upload an image.");
    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      setCreatives([]);

      setLoadingStep("📤 Uploading image…");

      const res = await axios.post(
        "http://127.0.0.1:5000/generate-creatives",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setLoadingStep("🪄 Removing background…");
      await new Promise((r) => setTimeout(r, 400));

      setLoadingStep("🎨 Extracting dominant colors…");
      await new Promise((r) => setTimeout(r, 400));

      setLoadingStep("✍️ Generating AI text…");
      await new Promise((r) => setTimeout(r, 400));

      setLoadingStep("🧩 Creating templates…");
      await new Promise((r) => setTimeout(r, 400));

      setLoadingStep("");

      // Store data
      setProcessedImg(res.data.processed_image_url);
      setCreatives(res.data.creatives);
      setTagline(res.data.tagline);
      setOffer(res.data.offer);

    } catch (err) {
      alert("Error generating creatives.");
      setLoadingStep("");
    }
  };

  // PNG download
  const downloadImage = async (url, filename) => {
    const response = await fetch(url);
    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  };

  // ⭐ OPEN EDITOR
  const openEditorFor = (url) => {
    setEditorSrc(url);
    setEditorOpen(true);
  };

  // ⭐ HANDLE EXPORT FROM EDITOR
  const handleEditorExport = (dataUrl) => {
    console.log("exported dataUrl length:", dataUrl.length);
    setEditorOpen(false);
  };

  return (
    <div className={dark ? "app dark" : "app"}>
      {/* Fullscreen preview modal */}
      {fullscreenImg && (
        <div className="fullscreen-modal" onClick={() => setFullscreenImg(null)}>
          <img src={fullscreenImg} className="fullscreen-img" alt="preview" />
        </div>
      )}

      {/* Top Bar */}
      <div className="top-bar">
        <h1 className="title">AI Creative Generator</h1>

        <div className="toggle-group">
          <button onClick={() => setDark(!dark)} className="toggle-btn">
            {dark ? "🌙 Dark" : "☀ Light"}
          </button>

          <button onClick={() => setCarousel(!carousel)} className="toggle-btn">
            {carousel ? "📚 Grid Mode" : "🎠 Carousel Mode"}
          </button>
        </div>
      </div>

      {/* Upload Panel */}
      <div className="glass-panel">
        <input
          type="file"
          onChange={(e) => setSelectedFile(e.target.files[0])}
          className="file-input"
        />

        <div className="input-row">
          <input
            type="text"
            value={tagline}
            onChange={(e) => setTagline(e.target.value)}
            placeholder="Tagline…"
            className="text-input"
          />

          <input
            type="text"
            value={offer}
            onChange={(e) => setOffer(e.target.value)}
            placeholder="Offer text…"
            className="text-input"
          />
        </div>

        <button className="generate-btn" onClick={handleUpload}>
          Generate Creatives
        </button>
      </div>

      {/* Loading UI */}
      {loadingStep && (
        <div className="loading-box glass-panel">
          <div className="loader"></div>
          <p>{loadingStep}</p>
        </div>
      )}

      {/* Processed image */}
      {processedImg && (
        <div className="section">
          <h2>Background Removed</h2>
          <img src={processedImg} className="processed-img" alt="processed" />
        </div>
      )}

      {/* TEMPLATES */}
      {creatives.length > 0 && (
        <div className="section">
          <h2>Your Creatives</h2>

          {/* Carousel Mode */}
          {carousel ? (
            <div className="carousel">
              {creatives.map((item, idx) =>
                ["clean_url", "split_url", "hero_url", "gradient_url", "neon_url", "diagonal_url"]
                  .map((key) => (
                    <img
                      key={idx + key}
                      src={item[key]}
                      onClick={() => setFullscreenImg(item[key])}
                      className="carousel-img"
                      alt="creative"
                    />
                  ))
              )}
            </div>
          ) : (
            // Grid Mode
            <div className="creative-grid">
              {creatives.map((item, idx) => (
                <React.Fragment key={idx}>
                  {[
                    ["Clean", "clean_url", "clean_template"],
                    ["Split", "split_url", "split_template"],
                    ["Hero", "hero_url", "hero_template"],
                    ["Gradient", "gradient_url", "gradient_template"],
                    ["Neon", "neon_url", "neon_template"],
                    ["Diagonal", "diagonal_url", "diagonal_template"],
                  ].map(([label, urlKey, nameKey]) => (
                    <div className="creative-card glass-card" key={label}>
                      <h3>{item.size.toUpperCase()} — {label}</h3>

                      <img
                        src={item[urlKey]}
                        className="creative-img"
                        onClick={() => setFullscreenImg(item[urlKey])}
                        alt={label}
                      />

                      <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                        <button
                          className="download-btn"
                          onClick={() => downloadImage(item[urlKey], item[nameKey])}
                        >
                          ⬇ Download PNG
                        </button>

                        <button
                          className="edit-btn"
                          onClick={() => openEditorFor(item[urlKey])}
                        >
                          ✏️ Edit
                        </button>
                      </div>
                    </div>
                  ))}
                </React.Fragment>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ⭐ EDITOR POPUP */}
      {editorOpen && editorSrc && (
        <Editor
          src={editorSrc}
          initialTagline={tagline}
          initialOffer={offer}
          onExport={handleEditorExport}
          onClose={() => setEditorOpen(false)}
          canvasSize={{ width: 1080, height: 1080 }}
        />
      )}
    </div>
  );
}

export default App;
