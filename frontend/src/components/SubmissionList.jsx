import { useEffect, useState } from "react";
import axios from "axios";

function SubmissionList() {
  const [submissions, setSubmissions] = useState([]);

  const fetchSubmissions = async () => {
    try {
      const response = await axios.get("http://localhost:8000/submissions/"); // Your API endpoint
      setSubmissions(response.data);
    } catch (error) {
      console.error("Error fetching submissions:", error);
    }
  };

  // Fetch submissions on component mount
  useEffect(() => {
    fetchSubmissions();
  }, []);

  return (
    <div style ={{ marginTop: "40px", color: "#f0eaea" }}>
      <h3>Previous Submissions</h3>
      {submissions.length === 0 ? (
        <p>No submissions yet.</p>
      ) : (
        <table border="1" cellPadding="5" bordercolor="#b4a2a2">
          <thead>
            <tr>
              <th>FullName</th>
              <th>Email</th>
              <th>Mobile</th>
              <th>Company</th>
              <th>Role</th>
              <th>Address</th>
              <th>City</th>
              <th>State</th>
              <th>PinCode</th>
              <th>Date</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map((sub) => (
              <tr key={sub._id}>
                <td>{sub.FullName}</td>
                <td>{sub.Email}</td>
                <td>{sub.Mobile}</td>
                <td>{sub.Company}</td>
                <td>{sub.Role}</td>
                <td>{sub.Address}</td>
                <td>{sub.City}</td>
                <td>{sub.State}</td>
                <td>{sub.PinCode}</td>
                <td>{sub.Date}</td>
                <td>{sub.Remarks}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default SubmissionList;

// bordercolor="#b4a2a2"
// style ={{ marginTop: "40px", color: "#f0eaea" }}
