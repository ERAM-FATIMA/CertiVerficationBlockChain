import { useState } from "react";
import "../../assets/styles.css";
import { registerStudent, issueCertificate } from "../../api/universityApi";
import { getAllStudents } from "../../api/universityApi";
import DashboardLayout from "../../components/DashboardLayout";

function UniversityDashboard() {

  const [view, setView] = useState("register");
  const [students, setStudents] = useState([]);
  const [loadingStudents, setLoadingStudents] = useState(false);

  const [studentData, setStudentData] = useState({
    name: "",
    email: "",
    password: "",
    degree: "",
    branch: ""
  });

  const [certData, setCertData] = useState({
    student_id: "",
    cgpa: "",
    year: ""
  });

  const token = localStorage.getItem("access_token");

  // REGISTER
  const handleRegisterStudent = async (e) => {
    e.preventDefault();

    try {
      await registerStudent(studentData);
      alert("Student Registered Successfully!");
    } catch (err) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  const fetchStudents = async () => {
    try {
      setLoadingStudents(true);
      const data = await getAllStudents();
      setStudents(data);
    } catch (err) {
      alert("Error fetching students");
    } finally {
      setLoadingStudents(false);
    }
  };

  // ISSUE
  const handleIssueCertificate = async (e) => {
    e.preventDefault();

    const payload = {
      student_id: Number(certData.student_id),
      cgpa: Number(certData.cgpa),
      year: Number(certData.year),
    };

    try {
      await issueCertificate(payload);
      alert("Certificate Issued Successfully!");
    } catch (err) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  return (

    <div className="page-bg university-page">
    <DashboardLayout title="CertiVeri - University">

      {/* TOGGLE BUTTONS */}
      <div className="uni-toggle">
        <button
          className={view === "register" ? "active-toggle" : ""}
          onClick={() => setView("register")}
        >
          Register Student
        </button>

        <button
          className={view === "view" ? "active-toggle" : ""}
          onClick={() => {
            setView("view");
            fetchStudents();
          }}
        >
          View Students
        </button>

        <button
          className={view === "issue" ? "active-toggle" : ""}
          onClick={() => setView("issue")}
        >
          Issue Certificate
        </button>
      </div>

      {/* FORM AREA */}
      <div className="uni-form-container">

        {view === "register" && (
          <div className="card">
            <h3>Register Student</h3>

            <form onSubmit={handleRegisterStudent}>
              <input className="input" placeholder="Name"
                onChange={(e) => setStudentData({ ...studentData, name: e.target.value })} required />

              <input className="input" placeholder="Email"
                onChange={(e) => setStudentData({ ...studentData, email: e.target.value })} required />

              <input className="input" type="password" placeholder="Password"
                onChange={(e) => setStudentData({ ...studentData, password: e.target.value })} required />

              <input className="input" placeholder="Degree"
                onChange={(e) => setStudentData({ ...studentData, degree: e.target.value })} required />

              <input className="input" placeholder="Branch"
                onChange={(e) => setStudentData({ ...studentData, branch: e.target.value })} required />

              <button className="button">Register</button>
            </form>
          </div>
        )}

        {view === "issue" && (
          <div className="card">
            <h3>Issue Certificate</h3>

            <form onSubmit={handleIssueCertificate}>
              <input className="input" type="number" placeholder="Student ID"
                onChange={(e) => setCertData({ ...certData, student_id: e.target.value })} required />

              <input className="input" type="number" step="0.1" placeholder="CGPA"
                onChange={(e) => setCertData({ ...certData, cgpa: e.target.value })} required />

              <input className="input" type="number" placeholder="Year (e.g. 2024)"
                onChange={(e) => setCertData({ ...certData, year: e.target.value })} required />

              <button className="button">Issue</button>
            </form>
          </div>
        )}
        {view === "view" && (
          <div className="card">
            <h3>Registered Students</h3>

            {loadingStudents ? (
              <p>Loading...</p>
            ) : students.length === 0 ? (
              <p>No students found</p>
            ) : (
              <table className="cert-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Degree</th>
                    <th>Branch</th>
                  </tr>
                </thead>

                <tbody>
                  {students.map((stu) => (
                    <tr key={stu.id}>
                      <td>{stu.id}</td>
                      <td>{stu.name}</td>
                      <td>{stu.email}</td>
                      <td>{stu.degree}</td>
                      <td>{stu.branch}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

      </div>

    </DashboardLayout>
    </div>
  );
}

export default UniversityDashboard;