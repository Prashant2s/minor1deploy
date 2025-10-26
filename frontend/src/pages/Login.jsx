import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [userType, setUserType] = useState("student");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Simple credentials (for demo - use real auth in production)
  const CREDENTIALS = {
    student: { username: "student", password: "student123" },
    admin: { username: "admin", password: "admin123" }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    // Simple login - accept any alphanumeric username
    if (!username || username.trim() === "") {
      setError("Please enter a username");
      return;
    }

    // Accept any alphanumeric username (case-insensitive)
    const alphanumericRegex = /^[a-zA-Z0-9]+$/;
    if (!alphanumericRegex.test(username)) {
      setError("Username must be alphanumeric only");
      return;
    }

    // Store username and login
    sessionStorage.setItem("userLoggedIn", "true");
    sessionStorage.setItem("userType", userType);
    sessionStorage.setItem("username", username);
    navigate("/");
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "20px"
    }}>
      <div style={{
        background: "white",
        borderRadius: "10px",
        padding: "40px",
        maxWidth: "400px",
        width: "100%",
        boxShadow: "0 10px 30px rgba(0,0,0,0.2)"
      }}>
        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <div style={{
            width: "80px",
            height: "80px",
            margin: "0 auto 20px",
            background: "#2E5BBA",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "40px",
            color: "white"
          }}>
            🎓
          </div>
          <h1 style={{
            fontSize: "24px",
            color: "#2E5BBA",
            marginBottom: "10px"
          }}>
            Certificate Verifier
          </h1>
          <p style={{ color: "#666", fontSize: "14px" }}>
            Login to access the system
          </p>
        </div>

        {error && (
          <div style={{
            background: "#f8d7da",
            color: "#721c24",
            padding: "12px",
            borderRadius: "6px",
            marginBottom: "20px",
            fontSize: "14px"
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              marginBottom: "12px",
              color: "#333",
              fontWeight: "500",
              fontSize: "15px"
            }}>
              User Type:
            </label>
            <div style={{ 
              display: "flex", 
              gap: "20px",
              padding: "15px",
              background: "#f8f9fa",
              borderRadius: "6px",
              border: "2px solid #e1e5e9"
            }}>
              <label style={{ 
                flex: 1, 
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                fontSize: "15px",
                fontWeight: "500",
                color: "#333"
              }}>
                <input
                  type="radio"
                  name="userType"
                  value="student"
                  checked={userType === "student"}
                  onChange={(e) => setUserType(e.target.value)}
                  style={{ 
                    marginRight: "8px",
                    width: "18px",
                    height: "18px",
                    cursor: "pointer"
                  }}
                />
                👤 Student
              </label>
              <label style={{ 
                flex: 1, 
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                fontSize: "15px",
                fontWeight: "500",
                color: "#333"
              }}>
                <input
                  type="radio"
                  name="userType"
                  value="admin"
                  checked={userType === "admin"}
                  onChange={(e) => setUserType(e.target.value)}
                  style={{ 
                    marginRight: "8px",
                    width: "18px",
                    height: "18px",
                    cursor: "pointer"
                  }}
                />
                🔐 Admin
              </label>
            </div>
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              marginBottom: "8px",
              color: "#333",
              fontWeight: "500"
            }}>
              Username:
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Enter username"
              style={{
                width: "100%",
                padding: "12px",
                border: "2px solid #e1e5e9",
                borderRadius: "6px",
                fontSize: "15px"
              }}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              marginBottom: "8px",
              color: "#333",
              fontWeight: "500"
            }}>
              Password: <span style={{color: "#999", fontWeight: "normal", fontSize: "13px"}}>(optional)</span>
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password (optional)"
              style={{
                width: "100%",
                padding: "12px",
                border: "2px solid #e1e5e9",
                borderRadius: "6px",
                fontSize: "15px"
              }}
            />
          </div>

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "14px",
              background: "#2E5BBA",
              color: "white",
              border: "none",
              borderRadius: "6px",
              fontSize: "16px",
              fontWeight: "600",
              cursor: "pointer",
              transition: "background 0.3s"
            }}
            onMouseEnter={(e) => e.target.style.background = "#1e3f8a"}
            onMouseLeave={(e) => e.target.style.background = "#2E5BBA"}
          >
            Login
          </button>
        </form>

        <div style={{
          marginTop: "20px",
          padding: "15px",
          background: "#f8f9fa",
          borderRadius: "6px",
          fontSize: "12px",
          color: "#666"
        }}>
          <strong>Quick Login:</strong><br />
          Enter any alphanumeric username<br />
          <span style={{fontSize: "11px", color: "#999"}}>
            Examples: STUDENT, Admin, user123<br />
            Password not required
          </span>
        </div>
      </div>
    </div>
  );
}
