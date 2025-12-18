// src/Editor.js
import React, { useRef, useState, useEffect } from "react";
import { Stage, Layer, Image as KonvaImage, Text, Transformer } from "react-konva";
import useImage from "use-image";
import "./Editor.css";
import ColorPalette from "./components/ColorPalette";

const URLImage = ({ src, shapeProps, isSelected, onSelect, onChange }) => {
  const [image] = useImage(src, "anonymous");
  const shapeRef = useRef();
  const trRef = useRef();

  useEffect(() => {
    if (isSelected && trRef.current && shapeRef.current) {
      trRef.current.nodes([shapeRef.current]);
      trRef.current.getLayer().batchDraw();
    }
  }, [isSelected]);

  return (
    <>
      <KonvaImage
        image={image}
        ref={shapeRef}
        {...shapeProps}
        draggable
        onClick={onSelect}
        onTap={onSelect}
        onDragEnd={(e) => {
          onChange({
            ...shapeProps,
            x: e.target.x(),
            y: e.target.y()
          });
        }}
        onTransformEnd={() => {
          const node = shapeRef.current;

          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          node.scaleX(1);
          node.scaleY(1);

          onChange({
            ...shapeProps,
            x: node.x(),
            y: node.y(),
            rotation: node.rotation(),
            width: Math.max(30, node.width() * scaleX),
            height: Math.max(30, node.height() * scaleY)
          });
        }}
      />

      {isSelected && (
        <Transformer
          ref={trRef}
          rotateEnabled={true}
          anchorSize={10}
          rotateAnchorOffset={40}
          enabledAnchors={["top-left", "top-right", "bottom-left", "bottom-right"]}
        />
      )}
    </>
  );
};

export default function Editor({
  src,
  initialTagline = "Your Tagline Here",
  initialOffer = "Special Offer",
  onExport,
  onClose,
  canvasSize = { width: 1080, height: 1080 }
}) {
  const stageRef = useRef();

  const extractedColors = ["#ff9900", "#111111", "#ffffff"];
  const [bgColor, setBgColor] = useState("#ffffff");

  const [imgProps, setImgProps] = useState({
    x: canvasSize.width * 0.1,
    y: canvasSize.height * 0.12,
    width: canvasSize.width * 0.8,
    height: canvasSize.height * 0.6,
    rotation: 0
  });

  const [tagline, setTagline] = useState(initialTagline);
  const [offer, setOffer] = useState(initialOffer);
  const [tagFontSize, setTagFontSize] = useState(48);
  const [offerFontSize, setOfferFontSize] = useState(36);
  const [tagColor, setTagColor] = useState("#000000");
  const [offerColor, setOfferColor] = useState("#ffffff");
  const [offerBg, setOfferBg] = useState("#ff3b30");

  const [selectedId, setSelectedId] = useState("img");

  const [aiLayout, setAiLayout] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  // ⭐ FIX HOOK DEPENDENCY WARNING
  useEffect(() => {
    setImgProps((prev) => ({
      ...prev,
      x: canvasSize.width / 2,
      y: canvasSize.height / 2
    }));
  }, [canvasSize.width, canvasSize.height]);

  // Reset when src changes
  useEffect(() => {
    setImgProps({
      x: canvasSize.width * 0.1,
      y: canvasSize.height * 0.12,
      width: canvasSize.width * 0.8,
      height: canvasSize.height * 0.6,
      rotation: 0
    });
  }, [src]);

  // EXPORT
  const handleExport = (type = "download") => {
    const uri = stageRef.current.toDataURL({ pixelRatio: 2 });

    if (type === "download") {
      const link = document.createElement("a");
      link.download = `creative_${Date.now()}.png`;
      link.href = uri;
      link.click();
    }

    if (onExport) onExport(uri);
  };

  const resetCanvas = () => {
    setTagline(initialTagline);
    setOffer(initialOffer);
    setTagFontSize(48);
    setOfferFontSize(36);
    setTagColor("#000000");
    setOfferColor("#ffffff");
    setOfferBg("#ff3b30");
    setBgColor("#ffffff");

    setImgProps({
      x: canvasSize.width * 0.1,
      y: canvasSize.height * 0.12,
      width: canvasSize.width * 0.8,
      height: canvasSize.height * 0.6,
      rotation: 0
    });

    setSelectedId("img");
  };

  // ⭐ AI API CALL
  const getLayoutSuggestions = async (file) => {
    try {
      const formData = new FormData();
      formData.append("image", file);

      const res = await fetch("http://localhost:5000/api/layout-suggestions", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      console.log("AI Layout Suggestions:", data);

      setAiLayout(data.layout_suggestions);
    } catch (error) {
      console.error("AI Layout Error:", error);
    }
  };

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setSelectedImage(file);
    getLayoutSuggestions(file);
  };

  return (
    <div className="editor-modal">
      <div className="editor-panel">

        {/* IMAGE UPLOAD */}
        <div style={{ marginBottom: 10 }}>
          <input type="file" accept="image/*" onChange={handleUpload} />
        </div>

        {/* CANVAS */}
        <div className="editor-canvas">
          <Stage
            width={canvasSize.width}
            height={canvasSize.height}
            ref={stageRef}
            style={{ background: bgColor, borderRadius: 8 }}
            onMouseDown={(e) => {
              if (e.target === e.target.getStage()) setSelectedId(null);
            }}
          >
            <Layer>
              <URLImage
                src={src}
                shapeProps={imgProps}
                isSelected={selectedId === "img"}
                onSelect={() => setSelectedId("img")}
                onChange={(newProps) => setImgProps(newProps)}
              />

              <Text
                x={40}
                y={20}
                text={tagline}
                fontSize={tagFontSize}
                fill={tagColor}
                width={canvasSize.width - 80}
                draggable
                onClick={() => setSelectedId("tag")}
              />

              <Text
                text={offer}
                fontSize={offerFontSize}
                fill={offerColor}
                padding={10}
                x={canvasSize.width / 2 - 200}
                y={canvasSize.height - 140}
                width={400}
                align="center"
                draggable
                onClick={() => setSelectedId("offer")}
              />
            </Layer>
          </Stage>
        </div>

        {/* CONTROL PANEL */}
        <div className="editor-controls">
          <h3>Controls</h3>
          <label>Selected: {selectedId || "None"}</label>

          <div className="control-row">
            <button onClick={() => setSelectedId("img")}>Select Image</button>
            <button onClick={() => setSelectedId("tag")}>Select Tagline</button>
            <button onClick={() => setSelectedId("offer")}>Select Offer</button>
          </div>

          <hr />

          <h4>Tagline</h4>
          <input value={tagline} onChange={(e) => setTagline(e.target.value)} />
          <label>Font Size</label>
          <input
            type="range"
            min="16"
            max="120"
            value={tagFontSize}
            onChange={(e) => setTagFontSize(Number(e.target.value))}
          />
          <label>Color</label>
          <input
            type="color"
            value={tagColor}
            onChange={(e) => setTagColor(e.target.value)}
          />

          <hr />

          <h4>Offer</h4>
          <input value={offer} onChange={(e) => setOffer(e.target.value)} />
          <label>Font Size</label>
          <input
            type="range"
            min="12"
            max="80"
            value={offerFontSize}
            onChange={(e) => setOfferFontSize(Number(e.target.value))}
          />
          <label>Text Color</label>
          <input
            type="color"
            value={offerColor}
            onChange={(e) => setOfferColor(e.target.value)}
          />

          <label>Badge Color</label>
          <input
            type="color"
            value={offerBg}
            onChange={(e) => setOfferBg(e.target.value)}
          />

          <hr />

          <h4>Brand Colors</h4>
          <ColorPalette
            colors={extractedColors}
            onColorSelect={(color) => setBgColor(color)}
          />

          <hr />

          <div className="control-row">
            <button className="primary" onClick={() => handleExport("download")}>
              Download PNG
            </button>
            <button className="secondary" onClick={() => handleExport("base64")}>
              Export Base64
            </button>
          </div>

          <div className="control-row">
            <button onClick={resetCanvas}>Reset</button>
            <button onClick={onClose}>Close</button>
          </div>

          {aiLayout && (
            <div style={{ marginTop: 20, padding: 10, background: "#f3f3f3" }}>
              <h4>AI Layout Suggestions</h4>
              <pre>{JSON.stringify(aiLayout, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
