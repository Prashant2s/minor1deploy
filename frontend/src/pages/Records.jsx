import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios.js";

export default function Records() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleDownloadFile = async (certId, filename) => {
    try {
      const response = await api.get(`/certificates/${certId}/download`, {
        responseType: "blob",
      });

      // Get filename from Content-Disposition header or use fallback
      const contentDisposition = response.headers['content-disposition'];
      let downloadFilename = filename || `certificate_${certId}.png`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          downloadFilename = filenameMatch[1];
        }
      }

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", downloadFilename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
      const errorMsg = err?.response?.data?.error || err.message || "Download failed";
      alert(`Download failed: ${errorMsg}. Please try again.`);
    }
  };


  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/certificates");
        setRecords(res.data?.certificates || []);
      } catch (err) {
        setError(err?.response?.data?.error || "Failed to load records");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <p style={{ padding: 16 }}>Loading...</p>;
  if (error) return <p style={{ padding: 16, color: "red" }}>{error}</p>;

  return (
    <div
      style={{
        padding: "24px 32px",
        fontFamily: "Arial, sans-serif",
        maxWidth: "100%",
        margin: "0 auto",
        backgroundColor: "#ffffff",
        height: "calc(100vh - 80px)",
        overflow: "auto",
        boxSizing: "border-box",
      }}
    >
      <h2
        style={{
          color: "#333",
          marginBottom: 24,
          fontSize: "32px",
          fontWeight: "600",
        }}
      >
        AI-Processed Certificate Records
      </h2>
      <p
        style={{
          color: "#666",
          fontSize: "18px",
          marginBottom: "32px",
          lineHeight: "1.6",
        }}
      >
        View all certificates processed by our AI system with extracted tabular
        data
      </p>
      {records.length === 0 ? (
        <div
          style={{
            padding: 24,
            backgroundColor: "#f8f9fa",
            border: "1px solid #dee2e6",
            borderRadius: 8,
            textAlign: "center",
            color: "#6c757d",
          }}
        >
          <h3 style={{ marginTop: 0 }}>No records found</h3>
          <p>Upload a certificate to see it listed here.</p>
        </div>
      ) : (
        <div
          style={{
            backgroundColor: "#1f1f1f",
            border: "1px solid #333",
            borderRadius: 8,
            overflow: "hidden",
            boxShadow: "0 2px 8px rgba(0,0,0,0.3)",
          }}
        >
          <table
            style={{
              borderCollapse: "collapse",
              width: "100%",
            }}
          >
            <thead>
              <tr style={{ backgroundColor: "#262626" }}>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Name</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Degree</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Branch</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>University</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Enrollment No</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>SGPA</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>CGPA</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Semester</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Academic Year</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "left", fontWeight: "bold", color: "#eaeaea" }}>Created</th>
                <th style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "center", fontWeight: "bold", color: "#eaeaea" }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {records.map((record, index) => {
                const t = record.tabular_data || {};
                return (
                  <tr
                    key={record.id}
                    style={{
                      borderBottom: "1px solid #2e2e2e",
                      backgroundColor: index % 2 === 0 ? "#1f1f1f" : "#262626",
                    }}
                  >
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.student_name || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.degree || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.branch || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.university_name || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.enrollment_number || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.sgpa || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.cgpa || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.semester || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#eaeaea" }}>{t.academic_year || "-"}</td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", color: "#a0a0a0", fontSize: "13px" }}>
                      {new Date(record.created_at).toLocaleDateString()} {new Date(record.created_at).toLocaleTimeString()}
                    </td>
                    <td style={{ border: "1px solid #3a3a3a", padding: "10px", textAlign: "center" }}>
                      <div style={{ display: "flex", gap: "8px", justifyContent: "center", flexWrap: "wrap" }}>
                        <Link
                          to={`/records/${record.id}`}
                          style={{
                            backgroundColor: "#2962ff",
                            color: "white",
                            padding: "4px 8px",
                            textDecoration: "none",
                            borderRadius: 4,
                            fontSize: "11px",
                            fontWeight: "bold",
                          }}
                        >
                          View
                        </Link>
                        <button
                          onClick={() => handleDownloadFile(record.id, record.original_filename)}
                          style={{ backgroundColor: "#28a745", color: "white", padding: "4px 8px", border: "none", borderRadius: 4, fontSize: "11px", fontWeight: "bold", cursor: "pointer" }}
                        >
                          Download
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
