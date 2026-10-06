import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function Home() {
  return (
    <div>

      {/* HERO SECTION */}
      <div className="hero-bg">

        <Navbar />
        
        <div className="hero-content">
          <h1 className="hero-title">
            Verify Academic Credentials
          </h1>

          <p className="hero-sub">
            A modern platform for issuing and verifying certificates securely.
          </p>

          <Link to="/login">
            <button className="button hero-button">Get Started</button>
          </Link>
        </div>

      </div>

      {/* FEATURES */}
      <div className="section">
        <h2>Platform Features</h2>

        <div className="grid">

          <div className="card">
            <h3>Secure Certificates</h3>
            <p>Universities issue tamper-proof digital certificates.</p>
          </div>

          <div className="card">
            <h3>Instant Verification</h3>
            <p>Employers can verify certificates within seconds.</p>
          </div>

          <div className="card">
            <h3>Student Ownership</h3>
            <p>Students maintain permanent digital access.</p>
          </div>

        </div>
      </div>

      {/* ROLES */}
      <div className="section light">
        <h2>Who Uses CertiVeri</h2>

        <div className="grid">

          <div className="card role-card">
            <h3>Students</h3>
            <p>
              Access issued certificates anytime and share verified credentials
              with employers securely.
            </p>
          </div>

          <div className="card role-card">
            <h3>Universities</h3>
            <p>
              Issue tamper-proof digital certificates and maintain
              trusted academic records.
            </p>
          </div>

          <div className="card role-card">
            <h3>Employers</h3>
            <p>
              Verify candidate credentials instantly and eliminate
              fake certificates.
            </p>
          </div>

        </div>
      </div>

      {/* WORKFLOW */}
      <div className="section workflow">
        <h2>How It Works</h2>

        <div className="workflow-grid">

          <div className="workflow-step">
            <div className="step-number">1</div>
            <h3>University Issues</h3>
            <p>The university uploads and issues a digital certificate.</p>
          </div>

          <div className="workflow-step">
            <div className="step-number">2</div>
            <h3>Student Receives</h3>
            <p>The student accesses and shares the certificate.</p>
          </div>

          <div className="workflow-step">
            <div className="step-number">3</div>
            <h3>Employer Verifies</h3>
            <p>The employer verifies the certificate authenticity.</p>
          </div>

        </div>
      </div>

      {/* CTA */}
      <div className="cta">
        <h2>Start Using CertiVeri Today</h2>
        <p>Secure, transparent, and reliable certificate verification.</p>

        <Link to="/login">
          <button className="button">Go to Login</button>
        </Link>
      </div>

      {/* FOOTER */}
      <div className="footer">
        <p>© 2026 CertiVeri</p>
      </div>

    </div>
  );
}

export default Home;