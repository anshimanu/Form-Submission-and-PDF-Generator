import { useState } from "react";
import axios from "axios";

function Form() {
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/submit/",
        formData,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      alert("Form submitted successfully!");
    } catch (error) {
      console.error("Submission failed:", error);
      alert("Failed to submit form. Check backend connection or data format.");
    }
  };

  return (
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
  );
}

export default Form;
