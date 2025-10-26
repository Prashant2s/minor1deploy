import { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Upload from "./pages/Upload.jsx";
import Records from "./pages/Records.jsx";
import RecordDetail from "./pages/RecordDetail.jsx";
import MyCertificates from "./pages/MyCertificates.jsx";

function Navigation() {
  const navigate = useNavigate();
  const [userType, setUserType] = useState("");

  useEffect(() => {
    setUserType(sessionStorage.getItem("userType") || "");
  }, []);

  const handleLogout = () => {
    sessionStorage.removeItem("userLoggedIn");
    sessionStorage.removeItem("userType");
    navigate("/login");
  };

  return (
    <nav
      style={{
        padding: "12px 24px",
        borderBottom: "1px solid #eee",
        backgroundColor: "#f8f9fa",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        position: "sticky",
        top: 0,
        zIndex: 1000,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          maxWidth: "1800px",
          margin: "0 auto",
          flexWrap: "wrap",
          gap: "16px",
        }}
      >
        {/* JUET Logo and Title */}
        <div className="juet-logo-container" style={{ display: "flex", alignItems: "center", cursor: "pointer" }} onClick={() => window.location.href = '/'}>
          <img
            src="/juet-official-logo.png"
            alt="Jaypee University of Engineering & Technology (JUET)"
            className="juet-official-logo"
            style={{
              height: "50px",
              width: "auto",
              marginRight: "12px",
              objectFit: "contain"
            }}
          />
          <div style={{ display: "flex", flexDirection: "column" }}>
            <h1 style={{
              fontSize: "18px",
              fontWeight: "bold",
              color: "#2E5BBA",
              margin: 0,
              lineHeight: 1.1
            }}>
              JUET Certificate Verifier
            </h1>
            <span style={{
              fontSize: "12px",
              color: "#666",
              marginTop: "2px"
            }}>
              AI-Powered Verification System
            </span>
          </div>
        </div>
        
        {/* Navigation Links */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <Link
            to="/"
            style={{
              textDecoration: "none",
              color: "#2E5BBA",
              fontWeight: "bold",
              fontSize: "16px",
              padding: "8px 16px",
              borderRadius: "6px",
              border: "2px solid #2E5BBA",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#2E5BBA";
              e.target.style.color = "white";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "transparent";
              e.target.style.color = "#2E5BBA";
            }}
          >
            AI Certificate Verifier
          </Link>
          <Link
            to="/upload"
            style={{
              textDecoration: "none",
              color: "#666",
              fontSize: "16px",
              fontWeight: "500",
              padding: "8px 16px",
              borderRadius: "6px",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#e9ecef";
              e.target.style.color = "#333";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "transparent";
              e.target.style.color = "#666";
            }}
          >
            Upload
          </Link>
          <Link
            to="/my-certificates"
            style={{
              textDecoration: "none",
              color: "#666",
              fontSize: "16px",
              fontWeight: "500",
              padding: "8px 16px",
              borderRadius: "6px",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#e9ecef";
              e.target.style.color = "#333";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "transparent";
              e.target.style.color = "#666";
            }}
          >
            My Certificates
          </Link>
          <Link
            to="/records"
            style={{
              textDecoration: "none",
              color: "#666",
              fontSize: "16px",
              fontWeight: "500",
              padding: "8px 16px",
              borderRadius: "6px",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#e9ecef";
              e.target.style.color = "#333";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "transparent";
              e.target.style.color = "#666";
            }}
          >
            All Records
          </Link>
          
          {/* User Info and Logout */}
          <div style={{ 
            display: "flex", 
            alignItems: "center", 
            gap: "12px",
            marginLeft: "20px",
            paddingLeft: "20px",
            borderLeft: "1px solid #dee2e6"
          }}>
            <span style={{
              fontSize: "14px",
              color: "#666",
              fontWeight: "500"
            }}>
              {userType === "admin" ? "👤 Admin" : "👤 Student"}
            </span>
            <button
              onClick={handleLogout}
              style={{
                padding: "8px 16px",
                background: "#dc3545",
                color: "white",
                border: "none",
                borderRadius: "6px",
                fontSize: "14px",
                fontWeight: "500",
                cursor: "pointer",
                transition: "background 0.3s"
              }}
              onMouseEnter={(e) => e.target.style.background = "#c82333"}
              onMouseLeave={(e) => e.target.style.background = "#dc3545"}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

// Protected Route Component
function ProtectedRoute({ children }) {
  const isLoggedIn = sessionStorage.getItem("userLoggedIn") === "true";
  return isLoggedIn ? children : <Navigate to="/login" />;
}

function AppContent() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/*" element={
          <ProtectedRoute>
            <>
              <Navigation />
              <main style={{
                minHeight: "calc(100vh - 80px)",
                backgroundColor: "#f8f9fa",
                overflow: "auto",
                padding: "20px 0",
              }}>
                <Routes>
                  <Route path="/" element={<Upload />} />
                  <Route path="/upload" element={<Upload />} />
                  <Route path="/my-certificates" element={<MyCertificates />} />
                  <Route path="/records" element={<Records />} />
                  <Route path="/records/:id" element={<RecordDetail />} />
                </Routes>
              </main>
            </>
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}

function App() {
  return <AppContent />;
}

export default App;
