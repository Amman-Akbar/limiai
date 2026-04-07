import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import AnalysisDisplay from './components/AnalysisDisplay';
import { Search, Loader2, Sparkles, BrainCircuit } from 'lucide-react';
import './index.css';

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (file, preview) => {
    setImageFile(file);
    setImagePreview(preview);
    setResult(null); // Reset result when new image is picked
    setError(null);
  };

  const handleAnalyze = async (e) => {
    if (e) e.preventDefault();
    if (!imageFile || !query) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('text', query);

    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9000';
      const response = await fetch(`${baseUrl}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Analysis failed:', err);
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:9000';
      setError(`Failed to analyze image. Please ensure the backend is running at ${baseUrl}.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header fade-in">
        <div className="logo-container">
          <BrainCircuit size={40} className="logo-icon" />
          <h1>Limi<span>AI-Assesment</span></h1>
        </div>
        <p className="subtitle">Advanced Image Analysis & Semantic Intelligence</p>
      </header>

      <main className="main-content">
        <div className="input-section glass fade-in">
          <ImageUpload 
            onImageSelect={handleImageSelect} 
            selectedImage={imagePreview} 
          />
          
          <div className="input-group">
            <label className="input-label">What should I look for?</label>
            <div className="search-box">
              <input
                type="text"
                className="text-input"
                placeholder="e.g., a man holding a gun"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
              />
              <button 
                className="btn btn-primary" 
                onClick={handleAnalyze}
                disabled={loading || !imageFile || !query}
              >
                {loading ? <Loader2 className="animate-spin" size={20} /> : <Search size={20} />}
                {loading ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message glass fade-in">
            <Sparkles size={20} />
            <p>{error}</p>
          </div>
        )}

        {result && (
          <AnalysisDisplay 
            result={result} 
            imagePreview={imagePreview} 
          />
        )}
      </main>

      <style dangerouslySetInnerHTML={{ __html: `
        .header {
          text-align: center;
          margin-bottom: 3rem;
        }
        .logo-container {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1rem;
          margin-bottom: 0.5rem;
        }
        .logo-icon {
          color: var(--primary);
        }
        h1 {
          font-size: 3rem;
          margin: 0;
          letter-spacing: -2px;
          background: linear-gradient(to right, #fff, var(--primary));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        h1 span {
          font-weight: 300;
        }
        .subtitle {
          color: var(--text-secondary);
          font-size: 1.1rem;
        }
        .main-content {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        .input-section {
          padding: 2rem;
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .search-box {
          display: flex;
          gap: 1rem;
        }
        .search-box .text-input {
          flex: 1;
        }
        .animate-spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .error-message {
          padding: 1rem 1.5rem;
          border-left: 4px solid var(--danger);
          display: flex;
          align-items: center;
          gap: 1rem;
          color: #f87171;
          background: rgba(239, 68, 68, 0.05);
        }
        .footer {
          margin-top: auto;
          padding: 3rem 0;
          text-align: center;
          color: var(--text-secondary);
          font-size: 0.9rem;
          border-top: 1px solid var(--glass-border);
        }
      `}} />
    </div>
  );
}

export default App;
