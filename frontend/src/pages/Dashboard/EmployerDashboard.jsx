import { useState } from "react";
import "../../assets/styles.css";
import DashboardLayout from "../../components/DashboardLayout";
import { verifyCertificate } from "../../api/employerApi";

function EmployerDashboard() {

  const [file, setFile] = useState(null);
  const [verificationResult, setVerificationResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("access_token");

  // ===== VERIFY CERTIFICATE =====
  const handleVerifyCertificate = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const data = await verifyCertificate(formData);
      setVerificationResult(data);

    } catch (err) {
      alert(err.response?.data?.detail || "Verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-bg university-page">
        <DashboardLayout title="CertiVeri - Employer">

        {/* VERIFY CARD */}
        <div className="card">
          <h2>Verify Certificate</h2>
          <p>Upload a PDF certificate to check authenticity using blockchain.</p>

          <form onSubmit={handleVerifyCertificate}>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <button type="submit" className="button" disabled={loading}>
              {loading ? "Verifying..." : "Verify"}
            </button>
          </form>
        </div>

        {/* RESULT */}
        {verificationResult && (
          <div
            className="card"
            style={{
              marginTop: "20px",
              borderLeft:
                verificationResult.status === "VALID"
                  ? "6px solid green"
                  : "6px solid red",
            }}
          >
            <h3>
              {verificationResult.status === "VALID"
                ? "✅ Certificate is Valid"
                : "❌ Certificate is Invalid"}
            </h3>

            {verificationResult.status === "VALID" && (
              <p>
                Stored in Block #
                <strong> {verificationResult.block_index}</strong>
              </p>
            )}
          </div>
        )}

      </DashboardLayout>
    </div>
    
  );
}

export default EmployerDashboard;