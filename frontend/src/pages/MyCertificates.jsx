import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios.js";
import Button from "../components/Button.jsx";

export default function MyCertificates() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/certificates/my-certificates");
        setRecords(res.data?.certificates || []);
      } catch (err) {
        setError(err?.response?.data?.error || "Failed to load certificates");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleDownloadFile = async (certId, filename) => {
    try {
      const response = await api.get(`/certificates/${certId}/download`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename || `certificate_${certId}.png`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
      alert("Download failed. Please try again.");
    }
  };

  const handleExportData = async (certId) => {
    try {
      const response = await api.get(`/certificates/${certId}/export`);

      const dataStr = JSON.stringify(response.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: "application/json" });

      const url = window.URL.createObjectURL(dataBlob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `certificate_${certId}_data.json`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export failed:", err);
      alert("Export failed. Please try again.");
    }
  };

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
        My Certificates
      </h2>
      <p
        style={{
          color: "#666",
          fontSize: "18px",
          marginBottom: "32px",
          lineHeight: "1.6",
        }}
      >
        View and download your uploaded certificates
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
          <h3 style={{ marginTop: 0 }}>No certificates found</h3>
          <p>Upload a certificate to see it listed here.</p>
          <Link
            to="/upload"
            style={{
              display: "inline-block",
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              marginTop: "10px",
            }}
          >
            Upload Certificate
          </Link>
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
                <th
                  style={{
                    border: "1px solid #3a3a3a",
                    padding: "10px",
                    textAlign: "left",
                    fontWeight: "bold",
                    color: "#eaeaea",
                  }}
                >
                  ID
                </th>
                <th
                  style={{
                    border: "1px solid #3a3a3a",
                    padding: "10px",
                    textAlign: "left",
                    fontWeight: "bold",
                    color: "#eaeaea",
                  }}
                >
                  FILENAME
                </th>
                <th
                  style={{
                    border: "1px solid #3a3a3a",
                    padding: "10px",
                    textAlign: "left",
                    fontWeight: "bold",
                    color: "#eaeaea",
                  }}
                >
                  STATUS
                </th>
                <th
                  style={{
                    border: "1px solid #3a3a3a",
                    padding: "10px",
                    textAlign: "left",
                    fontWeight: "bold",
                    color: "#eaeaea",
                  }}
                >
                  SUMMARY
                </th>
                <th
                  style={{
                    border: "1px solid #3a3a3a",
                    padding: "10px",
                    textAlign: "left",
                    fontWeight: "bold",
                    color: "#eaeaea",
                  }}
                >
                  CREATED
                </th>
                <th
                  style={{
                    border: "1px solid #3a3a3a",
                    padding: "10px",
                    textAlign: "center",
                    fontWeight: "bold",
                    color: "#eaeaea",
                  }}
                >
                  ACTIONS
                </th>
              </tr>
            </thead>
            <tbody>
              {records.map((record, index) => (
                <tr
                  key={record.id}
                  style={{
                    borderBottom: "1px solid #2e2e2e",
                    backgroundColor: index % 2 === 0 ? "#1f1f1f" : "#262626",
                  }}
                >
                  <td
                    style={{
                      border: "1px solid #3a3a3a",
                      padding: "10px",
                      fontWeight: "bold",
                      color: "#8ab4ff",
                    }}
                  >
                    #{record.id}
                  </td>
                  <td
                    style={{
                      border: "1px solid #3a3a3a",
                      padding: "10px",
                      color: "#dcdcdc",
                      fontSize: "13px",
                    }}
                  >
                    {record.original_filename || `certificate_${record.id}.png`}
                  </td>
                  <td
                    style={{
                      border: "1px solid #3a3a3a",
                      padding: "10px",
                    }}
                  >
                    <span
                      style={{
                        backgroundColor:
                          record.status === "processed" ? "#2e7d32" : "#b26a00",
                        color: "white",
                        padding: "3px 8px",
                        borderRadius: 4,
                        fontSize: "12px",
                        fontWeight: "bold",
                      }}
                    >
                      {record.status.toUpperCase()}
                    </span>
                  </td>
                  <td
                    style={{
                      border: "1px solid #3a3a3a",
                      padding: "10px",
                      color: "#dcdcdc",
                      maxWidth: "300px",
                    }}
                  >
                    {record.summary ? (
                      <div style={{ lineHeight: 1.4 }}>{record.summary}</div>
                    ) : (
                      <span style={{ color: "#9aa0a6", fontStyle: "italic" }}>
                        No summary available
                      </span>
                    )}
                  </td>
                  <td
                    style={{
                      border: "1px solid #3a3a3a",
                      padding: "10px",
                      color: "#a0a0a0",
                      fontSize: "13px",
                    }}
                  >
                    {new Date(record.created_at).toLocaleDateString()}{" "}
                    {new Date(record.created_at).toLocaleTimeString()}
                  </td>
                  <td
                    style={{
                      border: "1px solid #3a3a3a",
                      padding: "10px",
                      textAlign: "center",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        gap: "8px",
                        justifyContent: "center",
                        flexWrap: "wrap",
                      }}
                    >
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
                      <Button
                        variant="success"
                        onClick={() =>
                          handleDownloadFile(
                            record.id,
                            record.original_filename
                          )
                        }
                        style={{ padding: "4px 8px", fontSize: "11px" }}
                      >
                        Download
                      </Button>
                      <Button
                        variant="info"
                        onClick={() => handleExportData(record.id)}
                        style={{ padding: "4px 8px", fontSize: "11px" }}
                      >
                        Export
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
