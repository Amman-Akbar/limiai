import React, { useRef, useEffect, useState } from 'react';
import { Target, Activity, Tag, Layers } from 'lucide-react';

const AnalysisDisplay = ({ result, imagePreview }) => {
  const containerRef = useRef(null);
  const [imgSize, setImgSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (imagePreview) {
      const img = new Image();
      img.onload = () => {
        setImgSize({ width: img.width, height: img.height });
      };
      img.src = imagePreview;
    }
  }, [imagePreview]);

  if (!result) return null;

  const { detected_objects, text_analysis } = result.data;

  return (
    <div className="analysis-root fade-in">
      <div className="main-display glass">
        <div className="image-container" ref={containerRef}>
          <img src={imagePreview} alt="Analyzed" className="analyzed-image" />
          {imgSize.width > 0 && (
            <svg
              className="bounding-boxes"
              viewBox={`0 0 ${imgSize.width} ${imgSize.height}`}
              preserveAspectRatio="xMidYMid meet"
            >
            {detected_objects?.map((obj, i) => {
              // Assuming [x1, y1, x2, y2] based on typical object detection outputs
              // but adding a check to be safe if the format is [y1, x1, y2, x2]
              let [x1, y1, x2, y2] = obj.box;
              
              // If the detect person is wider than tall but coordinates suggest it should be tall,
              // or if y2-y1 is smaller than x2-x1 for a 'person', it might be [y1, x1, y2, x2]
              // However, most industry standards use [x1, y1, x2, y2] for web display.
              
              const width = x2 - x1;
              const height = y2 - y1;

              return (
                <g key={i} className="box-group">
                  <rect
                    x={x1}
                    y={y1}
                    width={width}
                    height={height}
                    className="box-rect"
                  />
                  <g className="label-container">
                    <rect
                      x={x1}
                      y={y1 > 25 ? y1 - 25 : y1}
                      width={obj.label.length * 10 + 60}
                      height={20}
                      className="label-bg"
                    />
                    <text
                      x={x1 + 5}
                      y={y1 > 25 ? y1 - 10 : y1 + 15}
                      className="box-label"
                    >
                      {obj.label} ({(obj.confidence * 100).toFixed(0)}%)
                    </text>
                  </g>
                </g>
              );
            })}
            </svg>
          )}
        </div>
      </div>

      <div className="results-panel">
        <div className="panel-section glass sentiment-section">
          <h3>
            <Activity size={18} /> Text Sentiment
          </h3>
          <div className={`sentiment-badge ${text_analysis?.sentiment}`}>
            {text_analysis?.sentiment}
          </div>
          <p className="query-text">"{text_analysis?.query}"</p>
        </div>

        <div className="panel-grid">
          <div className="panel-section glass">
            <h3>
              <Tag size={18} /> Keywords
            </h3>
            <div className="tag-cloud">
              {text_analysis?.extracted_keywords?.map((kw, i) => (
                <span key={i} className="tag">{kw}</span>
              ))}
            </div>
          </div>

          <div className="panel-section glass">
            <h3>
              <Layers size={18} /> Semantic Mapping
            </h3>
            <div className="tag-cloud">
              {text_analysis?.semantic_mapping?.map((sm, i) => (
                <span key={i} className="tag semantic">{sm}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .analysis-root {
          display: grid;
          grid-template-columns: 1fr 350px;
          gap: 2rem;
          margin-top: 2rem;
          height: 600px;
        }
        @media (max-width: 1024px) {
          .analysis-root {
            grid-template-columns: 1fr;
            height: auto;
          }
        }
        .main-display {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
          overflow: hidden;
          position: relative;
        }
        .image-container {
          position: relative;
          max-width: 100%;
          max-height: 100%;
          display: flex;
        }
        .analyzed-image {
          max-width: 100%;
          max-height: 550px;
          border-radius: 0.5rem;
          display: block;
        }
        .bounding-boxes {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
        }
        .box-rect {
          fill: rgba(139, 92, 246, 0.1);
          stroke: var(--primary);
          stroke-width: 2.5;
          vector-effect: non-scaling-stroke;
          filter: drop-shadow(0 0 4px rgba(139, 92, 246, 0.4));
          transition: all 0.2s;
        }
        .box-group:hover .box-rect {
          fill: rgba(139, 92, 246, 0.2);
          stroke-width: 4;
        }
        .label-bg {
          fill: var(--primary);
          rx: 4;
          ry: 4;
        }
        .box-label {
          fill: white;
          font-size: 13px;
          font-weight: 700;
          font-family: inherit;
          pointer-events: none;
        }
        .results-panel {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
          overflow-y: auto;
        }
        .panel-section {
          padding: 1.5rem;
        }
        .panel-section h3 {
          margin: 0 0 1rem;
          font-size: 1.1rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          color: var(--text-primary);
        }
        .sentiment-badge {
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 2rem;
          font-weight: 700;
          font-size: 1.2rem;
          margin-bottom: 0.5rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .sentiment-badge.NEGATIVE { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #f87171; }
        .sentiment-badge.POSITIVE { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #34d399; }
        .sentiment-badge.NEUTRAL { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #60a5fa; }
        
        .query-text {
          font-style: italic;
          color: var(--text-secondary);
          font-size: 0.9rem;
        }
        .panel-grid {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .tag-cloud {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .tag {
          padding: 0.35rem 0.75rem;
          background: var(--bg-dark);
          border: 1px solid var(--border-color);
          border-radius: 0.5rem;
          font-size: 0.85rem;
          color: var(--text-primary);
        }
        .tag.semantic {
          background: rgba(139, 92, 246, 0.1);
          border-color: rgba(139, 92, 246, 0.3);
          color: var(--primary);
        }
      `}} />
    </div>
  );
};

export default AnalysisDisplay;
