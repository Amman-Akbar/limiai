import React, { useCallback, useState } from 'react';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

const ImageUpload = ({ onImageSelect, selectedImage }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      processFile(file);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
      onImageSelect(file, reader.result);
    };
    reader.readAsDataURL(file);
  };

  const clearImage = (e) => {
    e.stopPropagation();
    setPreview(null);
    onImageSelect(null, null);
  };

  return (
    <div className="input-group">
      <label className="input-label">Image Upload</label>
      <div
        className={`upload-zone glass ${isDragging ? 'dragging' : ''} ${preview ? 'has-preview' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !preview && document.getElementById('file-input').click()}
      >
        <input
          id="file-input"
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        
        {!preview ? (
          <div className="upload-placeholder">
            <Upload size={40} className="upload-icon" />
            <p>Drag & drop or <span>browse</span></p>
            <p className="upload-hint">Supports: JPG, PNG, WEBP</p>
          </div>
        ) : (
          <div className="preview-container">
            <img src={preview} alt="Upload preview" className="image-preview" />
            <button className="clear-btn glass" onClick={clearImage}>
              <X size={16} />
            </button>
          </div>
        )}
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .upload-zone {
          height: 200px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-direction: column;
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          overflow: hidden;
          margin-bottom: 1rem;
        }
        .upload-zone:hover {
          border-color: var(--primary);
          background: rgba(255, 255, 255, 0.05);
        }
        .upload-zone.dragging {
          border-color: var(--primary);
          background: rgba(139, 92, 246, 0.1);
          transform: scale(1.02);
        }
        .upload-placeholder {
          text-align: center;
          color: var(--text-secondary);
        }
        .upload-icon {
          margin-bottom: 1rem;
          color: var(--primary);
        }
        .upload-placeholder span {
          color: var(--primary);
          font-weight: 600;
        }
        .upload-hint {
          font-size: 0.75rem;
          margin-top: 0.5rem;
        }
        .preview-container {
          width: 100%;
          height: 100%;
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .image-preview {
          max-width: 100%;
          max-height: 100%;
          object-fit: contain;
          border-radius: 0.5rem;
        }
        .clear-btn {
          position: absolute;
          top: 0.5rem;
          right: 0.5rem;
          width: 2rem;
          height: 2rem;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          background: rgba(239, 68, 68, 0.8);
          border: none;
          cursor: pointer;
          transition: background 0.2s;
        }
        .clear-btn:hover {
          background: var(--danger);
        }
      `}} />
    </div>
  );
};

export default ImageUpload;
