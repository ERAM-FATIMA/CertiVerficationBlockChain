import { useEffect, useState } from "react";
import { getCertificates } from "../../api/studentApi";
import "../../assets/styles.css";
import DashboardLayout from "../../components/DashboardLayout";
import api from "../../api/client"; // 👈 for baseURL

function StudentDashboard() {
  const [certificates, setCertificates] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState(null);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("access_token");

  // ===== FETCH CERTIFICATES =====
  const fetchCertificates = async () => {
    try {
      const data = await getCertificates();

      if (data.msg) {
        setMessage(data.msg);
        return;
      }

      setCertificates(data);
    } catch (err) {
      setMessage("Error fetching data");
    }
  };

  useEffect(() => {
    fetchCertificates();
  }, []);

  return (
    <div className="page-bg student-pg">
      <DashboardLayout title="CertiVeri - Student">
        {message && <p className="info-text">{message}</p>}

        {/* TABLE */}
        <div className="card">
          <h3>My Certificates</h3>

          {certificates.length === 0 ? (
            <p>No certificates found</p>
          ) : (
            <table className="cert-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Program</th>
                  <th>Block</th>
                  <th>View</th>
                </tr>
              </thead>

              <tbody>
                {certificates.map((cert) => (
                  <tr key={cert.certificate_id}>
                    <td>{cert.certificate_id}</td>
                    <td>
                      {cert.degree} - {cert.branch}
                    </td>
                    <td>{cert.block_index}</td>
                    <td>
                      <button
                        className="button"
                        onClick={() =>
                          setSelectedPdf(`${api.defaults.baseURL}${cert.pdf_url}`)
                        }
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* PREVIEW */}
        <div className="card">
          <h3>Certificate Preview</h3>

          {!selectedPdf ? (
            <p>Select a certificate to preview</p>
          ) : (
            <iframe
              src={selectedPdf}
              width="100%"
              height="500px"
              style={{ border: "1px solid #ddd", borderRadius: "8px" }}
            />
          )}
        </div>
      </DashboardLayout>
    </div>
  );
}

export default StudentDashboard;