import { useState } from "react";
import axios from "axios";
import SubmissionList from "./components/SubmissionList";

function App() {
  const [formData, setFormData] = useState({
    FullName: "",
    Email: "",
    Mobile: "",
    Company: "",
    Role: "",
    Address: "",
    City: "",
    State: "",
    PinCode: "",
    Date: "",
    Remarks: "",
  });

  const [submissionsRefresh, setSubmissionsRefresh] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

const handleSubmit = async (e) => {
    e.preventDefault();
    alert("Form successfully submitted! Generating PDF...");
    try {
      const response = await axios.post("http://localhost:8000/generate-pdf/", formData, {
        headers: { "Content-Type": "application/json" },
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "form_output.pdf");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      alert("Failed to generate PDF: " + error.message);
    }
  };

  return (
    <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      flexDirection: "column",
      backgroundColor: "#660909ff",
      padding: "20px",
    }}>
      <h1 style = {{ color: "#f0eaea", marginBottom: "20px" }}>
        Form Submission and PDF Generator
      </h1>

      <form onSubmit={handleSubmit}>
        {Object.entries(formData).map(([key, value]) => (
          <div key={key} style={{ marginBottom: "10px" }}>
            {key !== "Remarks" ? (
              <input
                type={key === "Email" ? "email" : key === "Date" ? "date" : "text"}
                name={key}
                placeholder={key}
                value={value}
                onChange={handleChange}
                required={key !== "Remarks"}
              />
            ) : (
              <textarea
                name={key}
                placeholder={key}
                value={value}
                onChange={handleChange}
              />
            )}
          </div>
        ))}
        <button type="submit">Submit</button>
      </form>

      <SubmissionList refresh={submissionsRefresh} />
    </div>
  );
}

export default App;

// style={{
//   display: "flex",
//   justifyContent: "center",
//   alignItems: "center",
//   minHeight: "100vh",
//   flexDirection: "column",
//   backgroundColor: "#660909ff",
//   padding: "20px",
// }}>

