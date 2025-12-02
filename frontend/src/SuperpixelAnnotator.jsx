import React, { useRef, useState, useEffect } from "react";
import axios from "axios";

/*
 Props:
  - imageUrl: "http://127.0.0.1:5000/uploads/<filename>"
  - segmentsMeta: object returned by /segment (polygons, features, image_shape)
*/

const LABEL_COLORS = {
  good: "rgba(120, 255, 154, 0.45)",
  moderate: "rgba(255, 179, 71, 0.45)",
  bad: "rgba(255, 99, 99, 0.45)"
};

export default function SuperpixelAnnotator({ imageUrl, segmentsMeta }) {
  const svgRef = useRef(null);
  const imgRef = useRef(null);

  const [labels, setLabels] = useState({});
  const [hoverId, setHoverId] = useState(null);
  const [imageSize, setImageSize] = useState([0, 0]);

  // NEW: Selected label mode (default good)
  const [currentLabel, setCurrentLabel] = useState("good");

  useEffect(() => {
    async function loadLabels() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/labels/${segmentsMeta.image_id}`
        );
        setLabels(res.data || {});
      } catch (e) {}
    }
    loadLabels();
  }, [segmentsMeta.image_id]);

  useEffect(() => {
    setHoverId(null);
  }, [segmentsMeta]);

  function onImgLoad(e) {
    setImageSize([e.target.naturalWidth, e.target.naturalHeight]);
  }

  function applyLabel(id, label) {
    const newLabels = { ...labels };
    newLabels[id] = { label, ts: Date.now() };
    setLabels(newLabels);

    axios
      .post("http://127.0.0.1:5000/save_label", {
        image_id: segmentsMeta.image_id,
        superpixel_id: id,
        label: label,
        user: "web_user"
      })
      .catch((err) => console.error("label save failed", err));
  }

  function polygonPoints(polygon) {
    return polygon.map((p) => p.join(",")).join(" ");
  }

  return (
    <div
      style={{
        position: "relative",
        maxWidth: "100%",
        overflow: "auto",
        border: "1px solid #222",
        padding: 8,
        background: "#000"
      }}
    >
      {/* LABEL BUTTONS */}
      <div style={{ marginBottom: 12 }}>
        <button
          className={currentLabel === "good" ? "selected" : ""}
          onClick={() => setCurrentLabel("good")}
          style={{
            padding: "6px 12px",
            borderRadius: "6px",
            marginRight: 6,
            background: currentLabel === "good" ? "#78ff9a" : "#222",
            color: currentLabel === "good" ? "#000" : "#ddd",
            border: "1px solid #444",
            cursor: "pointer"
          }}
        >
          Good
        </button>

        <button
          className={currentLabel === "moderate" ? "selected" : ""}
          onClick={() => setCurrentLabel("moderate")}
          style={{
            padding: "6px 12px",
            borderRadius: "6px",
            marginRight: 6,
            background: currentLabel === "moderate" ? "#ffb347" : "#222",
            color: currentLabel === "moderate" ? "#000" : "#ddd",
            border: "1px solid #444",
            cursor: "pointer"
          }}
        >
          Moderate
        </button>

        <button
          className={currentLabel === "bad" ? "selected" : ""}
          onClick={() => setCurrentLabel("bad")}
          style={{
            padding: "6px 12px",
            borderRadius: "6px",
            background: currentLabel === "bad" ? "#ff6363" : "#222",
            color: currentLabel === "bad" ? "#000" : "#ddd",
            border: "1px solid #444",
            cursor: "pointer"
          }}
        >
          Bad
        </button>

        <span style={{ marginLeft: 12, color: "#b388ff" }}>
          Selected: <strong>{currentLabel.toUpperCase()}</strong>
        </span>
      </div>

      {/* IMAGE + POLYGONS */}
      <div style={{ position: "relative", display: "inline-block" }}>
        <img
          ref={imgRef}
          src={imageUrl}
          alt="orthomosaic"
          onLoad={onImgLoad}
          style={{ display: "block", maxWidth: "100%", height: "auto" }}
        />

        <svg
          ref={svgRef}
          viewBox={`0 0 ${segmentsMeta.image_shape[1]} ${segmentsMeta.image_shape[0]}`}
          preserveAspectRatio="xMinYMin meet"
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: "100%",
            height: "100%",
            pointerEvents: "none"
          }}
        >
          {segmentsMeta.polygons.map((s) => {
            const id = s.id;
            const labelObj = labels[id];
            const fill = labelObj
              ? LABEL_COLORS[labelObj.label]
              : "rgba(0,0,0,0)";
            const stroke =
              hoverId === id
                ? "rgba(255,255,255,0.6)"
                : "rgba(0,0,0,0.25)";

            return (
              <polygon
                key={id}
                points={polygonPoints(s.polygon)}
                fill={fill}
                stroke={stroke}
                strokeWidth={0.7}
                style={{ cursor: "pointer", pointerEvents: "all" }}
                onClick={(e) => {
                  e.stopPropagation();
                  applyLabel(id, currentLabel);
                }}
                onMouseEnter={() => setHoverId(id)}
                onMouseLeave={() => setHoverId(null)}
              />
            );
          })}
        </svg>
      </div>

      {/* LABEL MANAGEMENT BUTTONS */}
      <div style={{ marginTop: 12 }}>
        <button
          onClick={async () => {
            const payload = { image_id: segmentsMeta.image_id, labels };
            const blob = new Blob([JSON.stringify(payload, null, 2)], {
              type: "application/json"
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${segmentsMeta.image_id}_labels.json`;
            a.click();
            URL.revokeObjectURL(url);
          }}
        >
          Download labels JSON
        </button>

        <button
          style={{ marginLeft: 8 }}
          onClick={async () => {
            const res = await axios.get(
              `http://127.0.0.1:5000/labels/${segmentsMeta.image_id}`
            );
            setLabels(res.data || {});
          }}
        >
          Reload labels
        </button>
      </div>
    </div>
  );
}
