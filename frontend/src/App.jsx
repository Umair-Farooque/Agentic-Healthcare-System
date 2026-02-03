import { useState, useRef } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append('raw_input', input);
    if (file) {
      formData.append('file', file);
    }

    try {
      // Use environment variable or fallback to localhost
      let apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      if (!apiUrl.startsWith('http')) {
        apiUrl = `https://${apiUrl}`;
      }

      const response = await fetch(`${apiUrl}/invoke`, {
        method: 'POST',
        // Content-Type is set automatically for FormData
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="app-container">
      <div className="face-card">
        <header className="header">
          <h1>Agentic Healthcare</h1>
          <p className="subtitle">AI-Powered Patient Intake & Analysis</p>
        </header>

        <form onSubmit={handleSubmit} className="input-section">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe patient symptoms (e.g., 'Patient John Doe, 45, reports severe chest pain...')"
            className="main-input"
            rows="5"
            required
          />

          <div className="file-upload-section">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: 'none' }}
              accept=".pdf,.png,.jpg,.jpeg"
            />
            <button
              type="button"
              className="secondary-btn"
              onClick={() => fileInputRef.current.click()}
            >
              {file ? `📎 ${file.name}` : '📎 Attach Report (PDF/Image)'}
            </button>
            {file && (
              <button
                type="button"
                className="clear-file-btn"
                onClick={() => { setFile(null); fileInputRef.current.value = ''; }}
              >
                ✕
              </button>
            )}
          </div>

          <div className="actions">
            <button type="submit" disabled={loading || (!input && !file)} className="analyze-btn">
              {loading ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                  <span className="loader"></span> Processing...
                </div>
              ) : 'Analyze Case'}
            </button>
            {loading && <div style={{ marginTop: '10px', textAlign: 'center', color: '#94a3b8', fontSize: '0.9rem' }}>Please wait while our agents analyze the data...</div>}
          </div>
        </form>

        {error && <div className="error-message">{error}</div>}

        {result && (
          <div className="results-container">
            <div className="result-card intake">
              <h3>Intake</h3>
              <pre>{JSON.stringify(result.structured_data, null, 2)}</pre>
            </div>

            <div className="result-card validation">
              <h3>Validation</h3>
              <div className={`status-badge ${result.validated ? 'success' : 'warning'}`}>
                {result.validated ? 'Valid' : 'Issues Found'}
              </div>
            </div>

            <div className="result-card reasoning">
              <h3>Reasoning</h3>
              <p>{result.decision}</p>
            </div>

            <div className="result-card action">
              <h3>Action</h3>
              <ul>
                {result.actions?.map((action, idx) => (
                  <li key={idx}>{action}</li>
                ))}
              </ul>
            </div>

            <div className="result-card audit">
              <h3>Latest Audit</h3>
              <pre className="audit-log">{JSON.stringify(result.audit_log?.[result.audit_log.length - 1], null, 2)}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
