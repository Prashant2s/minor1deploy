import { useState } from "react";
import api from "../api/axios.js";
import Button from "../components/Button.jsx";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await api.post("/certificates/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      const errorMessage = err?.response?.data?.error || "Upload failed";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: "32px 48px",
        maxWidth: "1400px",
        margin: "0 auto",
        height: "calc(100vh - 80px)",
        backgroundColor: "#ffffff",
        overflow: "hidden",
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ flex: "0 0 auto", marginBottom: "24px" }}>
        <h2
          style={{
            fontSize: "28px",
            marginBottom: "16px",
            color: "#333",
            fontWeight: "600",
          }}
        >
          AI Certificate Upload & Analysis
        </h2>
        <p
          style={{
            color: "#666",
            fontSize: "16px",
            marginBottom: "0",
            lineHeight: "1.5",
          }}
        >
          Upload your academic certificate (PDF, JPG, PNG) for AI-powered
          extraction and verification
        </p>
      </div>
      <div style={{ flex: "0 0 auto", marginBottom: "24px" }}>
        <form onSubmit={onSubmit}>
          <div
            style={{
              display: "flex",
              gap: "20px",
              alignItems: "center",
              flexWrap: "nowrap",
            }}
          >
            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png,.tiff,.bmp"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              style={{
                padding: "14px 16px",
                border: "2px dashed #ddd",
                borderRadius: "8px",
                backgroundColor: "#fafafa",
                fontSize: "16px",
                minWidth: "400px",
                cursor: "pointer",
                flex: "1",
              }}
            />
            <Button
              type="submit"
              variant="primary"
              disabled={!file || loading}
              style={{
                padding: "14px 28px",
                fontSize: "16px",
                fontWeight: "600",
                whiteSpace: "nowrap",
              }}
            >
              {loading ? "Uploading..." : "Upload Certificate"}
            </Button>
          </div>
        </form>
        {error && (
          <p
            style={{
              color: "#dc3545",
              fontSize: "14px",
              marginTop: "12px",
              padding: "8px 12px",
              backgroundColor: "#f8d7da",
              border: "1px solid #f5c6cb",
              borderRadius: "4px",
            }}
          >
            {error}
          </p>
        )}
      </div>
      {result && (
        <div
          style={{
            flex: "1 1 auto",
            padding: "20px",
            background: "#f8f9fa",
            border: "1px solid #dee2e6",
            borderRadius: "8px",
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
          }}
        >

          {/* Verification Status */}
          {result.verification && (
            <div style={{ flex: "0 0 auto", marginBottom: "16px" }}>
              <div
                style={{
                  fontSize: "14px",
                  color: "#6c757d",
                  marginBottom: "8px",
                  fontWeight: "500",
                }}
              >
                🎯 University Verification Status
              </div>
              {(() => {
                const status = (result.simple_status || '').toLowerCase();
                const colors = status === 'verified'
                  ? { bg: '#d4edda', border: '#c3e6cb', text: '#155724', label: '✅ VERIFIED' }
                  : status === 'mismatch'
                  ? { bg: '#fff3cd', border: '#ffeeba', text: '#856404', label: '⚠️ MISMATCH' }
                  : { bg: '#f8d7da', border: '#f5c6cb', text: '#721c24', label: '❌ NOT VERIFIED' };
                return (
                  <div
                    style={{
                      padding: "12px 16px",
                      borderRadius: "6px",
                      backgroundColor: colors.bg,
                      border: `1px solid ${colors.border}`,
                      color: colors.text,
                    }}
                  >
                    <div style={{ fontWeight: "600", fontSize: "16px" }}>
                      Status: {colors.label}
                    </div>
                    <div style={{ fontSize: "14px", marginTop: "4px" }}>
                      Confidence Score:{" "}
                      {Math.round(
                        (result.verification.confidence_score || 0) * 100
                      )}
                      %
                    </div>
                    {result.verification.matched_student && (
                      <div style={{ fontSize: "14px", marginTop: "8px" }}>
                        <strong>Matched University Record:</strong>{" "}
                        {(result.verification.matched_student.name || result.verification.matched_student.student_name) || '-'} (Enroll:{" "}
                        {(result.verification.matched_student.reg_no || result.verification.matched_student.enrollment_number) || '-'})
                      </div>
                    )}
                  </div>
                );
              })()}
            </div>
          )}

          <div
            style={{ flex: "0 0 auto", marginTop: "16px", textAlign: "right" }}
          >
            <a
              href={`#/records/${result.id}`}
              style={{
                display: "inline-block",
                background: "#2962ff",
                color: "white",
                padding: "10px 16px",
                borderRadius: "6px",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: "600",
                transition: "all 0.2s ease",
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = "#1e53e5";
                e.target.style.transform = "translateY(-1px)";
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = "#2962ff";
                e.target.style.transform = "translateY(0)";
              }}
            >
              View Full Record #{result.id}
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
