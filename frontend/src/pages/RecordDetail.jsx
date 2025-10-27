import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios.js";
import Button from "../components/Button.jsx";

function formatValue(key, value) {
  const s = String(value ?? "");
  if (key === "student_name") {
    const m = s.match(/^(.*?)(Enrollment\s*No\s*:\s*.+)$/i);
    if (m) {
      const before = m[1].trim();
      const enroll = m[2]
        .trim()
        .replace(/^\(+|\)+$/g, "")
        .trim();
      return `${before} (${enroll})`;
    }
  }
  return s;
}

function formatFieldName(key) {
  return key
    .replaceAll("_", " ")
    .replace(/\b\w/g, (l) => l.toUpperCase())
    .replace("Dob", "Date of Birth");
}

function getConfidenceColor(confidence) {
  if (confidence >= 0.8) return "#4CAF50"; // Green
  if (confidence >= 0.6) return "#FF9800"; // Orange
  return "#F44336"; // Red
}

export default function RecordDetail() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reverifying, setReverifying] = useState(false);

  const handleReverify = async () => {
    if (!confirm('Re-verify this certificate against the university database?')) {
      return;
    }
    
    setReverifying(true);
    try {
      const response = await api.post(`/certificates/${id}/reverify`);
      
      if (response.data.success) {
        alert('Certificate re-verified successfully!');
        // Reload the certificate data
        const res = await api.get(`/certificates/${id}`);
        setData(res.data);
      } else {
        alert('Re-verification failed: ' + (response.data.error || 'Unknown error'));
      }
    } catch (err) {
      console.error('Re-verification failed:', err);
      alert('Re-verification failed: ' + (err.response?.data?.error || err.message));
    } finally {
      setReverifying(false);
    }
  };

  const handleDownloadFile = async () => {
    try {
      const response = await api.get(`/certificates/${id}/download`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        data.original_filename || `certificate_${id}.png`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
      alert("Download failed. Please try again.");
    }
  };


  useEffect(() => {
    (async () => {
      try {
        const res = await api.get(`/certificates/${id}`);
        setData(res.data);
      } catch (err) {
        setError(err?.response?.data?.error || "Failed to load record");
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <p style={{ padding: 16 }}>Loading...</p>;
  if (error) return <p style={{ padding: 16, color: "red" }}>{error}</p>;
  if (!data) return <p style={{ padding: 16 }}>No data.</p>;

  // Use the new tabular_data structure
  const tabularData = data.tabular_data || {};

  // Build keyword chips from tabular data
  const keywords = [
    tabularData.student_name,
    tabularData.degree,
    tabularData.branch,
    tabularData.certificate_type,
    tabularData.university_name,
    tabularData.enrollment_number,
    tabularData.graduation_date,
    tabularData.date_of_birth,
    tabularData.grade,
    tabularData.sgpa,
    tabularData.cgpa,
    tabularData.semester,
    tabularData.academic_year,
  ]
    .filter(Boolean)
    .filter((v) => v !== "-")
    .map((v) => String(v).trim())
    .filter((v, i, arr) => v && arr.indexOf(v) === i)
    .slice(0, 12);

  // Build comprehensive display rows from tabular data (AI-extracted structured information only)
  const displayRows = [
    {
      label: "STUDENT NAME",
      value: tabularData.student_name || "-",
    },
    {
      label: "ENROLLMENT NO",
      value: tabularData.enrollment_number || "-",
    },
    {
      label: "DEGREE",
      value: tabularData.degree || "-",
    },
    {
      label: "BRANCH",
      value: tabularData.branch || "-",
    },
    {
      label: "UNIVERSITY NAME",
      value: tabularData.university_name || "-",
    },
    {
      label: "GRADUATION DATE",
      value: tabularData.graduation_date || "-",
    },
    {
      label: "DATE OF BIRTH",
      value: tabularData.date_of_birth || "-",
    },
    {
      label: "OVERALL GRADE",
      value: tabularData.grade || "-",
    },
    {
      label: "CERTIFICATE TYPE",
      value: tabularData.certificate_type || "-",
    },
    {
      label: "SEMESTER",
      value: tabularData.semester || "-",
    },
    {
      label: "ACADEMIC YEAR",
      value: tabularData.academic_year || "-",
    },
    {
      label: "SGPA",
      value: tabularData.sgpa || "-",
    },
    {
      label: "CGPA",
      value: tabularData.cgpa || "-",
    },
    {
      label: "TOTAL CREDITS",
      value: tabularData.total_credits || "-",
    },
    {
      label: "EARNED CREDITS",
      value: tabularData.earned_credits || "-",
    },
  ];

  // Parse subjects data
  const subjects = Array.isArray(tabularData.subjects)
    ? tabularData.subjects
    : [];

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
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "24px",
        }}
      >
        <h2
          style={{
            color: "#333",
            margin: 0,
            fontSize: "32px",
            fontWeight: "600",
          }}
        >
          Certificate Details - #{data.id}
        </h2>
        <div style={{ display: "flex", gap: "12px" }}>
          <Button 
            variant="warning" 
            onClick={handleReverify}
            disabled={reverifying}
          >
            {reverifying ? 'Re-verifying...' : 'Re-verify Certificate'}
          </Button>
          <Button variant="success" onClick={handleDownloadFile}>
            Download File
          </Button>
        </div>
      </div>

      <div>
        {/* Extracted Data Table (Two-column dark table) */}
        <div style={{ width: "100%" }}>
          <div
            style={{
              padding: "20px",
              backgroundColor: "#1f1f1f",
              border: "1px solid #333",
              borderRadius: "8px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.3)",
            }}
          >

            {/* Keyword chips */}
            {keywords.length > 0 && (
              <div style={{ marginBottom: 18 }}>
                <div
                  style={{ color: "#cfd8dc", fontSize: 12, marginBottom: 8 }}
                >
                  Keywords
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                  {keywords.map((k) => (
                    <span
                      key={k}
                      style={{
                        background: "#263238",
                        color: "#e0f2f1",
                        border: "1px solid #37474f",
                        padding: "6px 10px",
                        borderRadius: 999,
                        fontSize: 12,
                        lineHeight: 1,
                        whiteSpace: "nowrap",
                      }}
                    >
                      {k}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <h3
              style={{
                marginTop: 0,
                marginBottom: "20px",
                color: "#f0f0f0",
                borderBottom: "1px solid #333",
                paddingBottom: "10px",
              }}
            >
              AI-Extracted Information
            </h3>

            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
              }}
            >
              <tbody>
                {displayRows.map((row, idx) => (
                  <tr
                    key={row.label}
                    style={{
                      backgroundColor: idx % 2 === 0 ? "#262626" : "#1f1f1f",
                    }}
                  >
                    <td
                      style={{
                        border: "1px solid #3a3a3a",
                        padding: "12px",
                        color: "#eaeaea",
                        fontWeight: 700,
                        width: "35%",
                        textTransform: "uppercase",
                        letterSpacing: "0.3px",
                      }}
                    >
                      {row.label}
                    </td>
                    <td
                      style={{
                        border: "1px solid #3a3a3a",
                        padding: "12px",
                        color: "#f5f5f5",
                        fontWeight: 500,
                      }}
                    >
                      {formatValue(row.label, row.value)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Subjects Table */}
            {subjects.length > 0 && (
              <div style={{ marginTop: "24px" }}>
                <h4
                  style={{
                    color: "#f0f0f0",
                    marginBottom: "16px",
                    borderBottom: "1px solid #333",
                    paddingBottom: "8px",
                  }}
                >
                  Subject-wise Performance
                </h4>
                <table
                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    backgroundColor: "#1f1f1f",
                  }}
                >
                  <thead>
                    <tr style={{ backgroundColor: "#2a2a2a" }}>
                      <th
                        style={{
                          border: "1px solid #3a3a3a",
                          padding: "10px",
                          color: "#eaeaea",
                          fontWeight: "bold",
                          textAlign: "left",
                        }}
                      >
                        Subject Code
                      </th>
                      <th
                        style={{
                          border: "1px solid #3a3a3a",
                          padding: "10px",
                          color: "#eaeaea",
                          fontWeight: "bold",
                          textAlign: "left",
                        }}
                      >
                        Subject Name
                      </th>
                      <th
                        style={{
                          border: "1px solid #3a3a3a",
                          padding: "10px",
                          color: "#eaeaea",
                          fontWeight: "bold",
                          textAlign: "center",
                        }}
                      >
                        Grade
                      </th>
                      <th
                        style={{
                          border: "1px solid #3a3a3a",
                          padding: "10px",
                          color: "#eaeaea",
                          fontWeight: "bold",
                          textAlign: "center",
                        }}
                      >
                        Credits
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {subjects.map((subject, idx) => (
                      <tr
                        key={idx}
                        style={{
                          backgroundColor:
                            idx % 2 === 0 ? "#262626" : "#1f1f1f",
                        }}
                      >
                        <td
                          style={{
                            border: "1px solid #3a3a3a",
                            padding: "10px",
                            color: "#eaeaea",
                            fontWeight: "600",
                          }}
                        >
                          {subject.subject_code || "-"}
                        </td>
                        <td
                          style={{
                            border: "1px solid #3a3a3a",
                            padding: "10px",
                            color: "#f5f5f5",
                          }}
                        >
                          {subject.subject_name || "-"}
                        </td>
                        <td
                          style={{
                            border: "1px solid #3a3a3a",
                            padding: "10px",
                            color: "#f5f5f5",
                            textAlign: "center",
                            fontWeight: "600",
                          }}
                        >
                          {subject.grade || "-"}
                        </td>
                        <td
                          style={{
                            border: "1px solid #3a3a3a",
                            padding: "10px",
                            color: "#f5f5f5",
                            textAlign: "center",
                          }}
                        >
                          {subject.credits || "-"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Verification Results */}
            {data.verification && (
              <div
                style={{
                  marginTop: "24px",
                  padding: "16px",
                  backgroundColor: data.verification.student_verified
                    ? "#113d26"
                    : "#401f23",
                  border:
                    "1px solid " +
                    (data.verification.student_verified
                      ? "#205e3b"
                      : "#6a2731"),
                  borderRadius: "4px",
                  color: "#e9f5ee",
                }}
              >
                <h4
                  style={{
                    marginTop: 0,
                    color: data.verification.student_verified
                      ? "#a8f0c4"
                      : "#f3b2bc",
                  }}
                >
                  University Verification
                </h4>
                <p style={{ margin: "8px 0" }}>
                  <strong>Student Verified:</strong>{" "}
                  <span
                    style={{
                      color: data.verification.student_verified
                        ? "#a8f0c4"
                        : "#f3b2bc",
                      fontWeight: "bold",
                    }}
                  >
                    {data.verification.student_verified ? "YES" : "NO"}
                  </span>
                </p>
                <p style={{ margin: "8px 0" }}>
                  <strong>Enrollment Number:</strong>{" "}
                  <span
                    style={{
                      color: "#a8f0c4",
                      fontWeight: "bold",
                    }}
                  >
                    {tabularData.enrollment_number || "-"}
                  </span>
                </p>
                <p style={{ margin: "8px 0" }}>
                  <strong>Certificate Match:</strong>{" "}
                  <span
                    style={{
                      color: data.verification.student_verified
                        ? "#a8f0c4"
                        : "#f3b2bc",
                      fontWeight: "bold",
                    }}
                  >
                    {data.verification.student_verified ? "YES" : "NO"}
                  </span>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
