import React, { useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import "chart.js/auto"; // Required for Chart.js v3
import "./App.css"; // Import the CSS file

function App() {
  const [company, setCompany] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [file, setFile] = useState(null);
  const [uploadResponse, setUploadResponse] = useState("");

  const analyzeCompany = async () => {
    try {
      const response = await axios.post("http://localhost:5000/analyze", { company });
      setAnalysis(response.data);
    } catch (error) {
      console.error("Error analyzing company:", error);
    }
  };

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadResponse(response.data.text);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const data = {
    labels: ["2020", "2021", "2022", "2023", "2024"],
    datasets: [
      {
        label: "Revenue",
        data: analysis ? sample_data[company]["Revenue"] : [],
        backgroundColor: "rgba(75,192,192,0.2)",
        borderColor: "rgba(75,192,192,1)",
      },
    ],
  };

  return (
    <div className="App">
      <h1>FundamentaX</h1>

      <div>
        <h2>Analyze Company</h2>
        <input
          type="text"
          placeholder="Enter company name"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        />
        <button onClick={analyzeCompany}>Analyze</button>

        {analysis && (
          <div>
            <h3>Financial Ratios</h3>
            <pre>{JSON.stringify(analysis.ratios, null, 2)}</pre>

            <h3>Unusual Patterns</h3>
            <pre>{JSON.stringify(analysis.patterns, null, 2)}</pre>

            <h3>Revenue Trend</h3>
            <Line data={data} />
          </div>
        )}
      </div>

      <div>
        <h2>Upload Financial Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile}>Upload</button>

        {uploadResponse && (
          <div>
            <h3>Extracted Text</h3>
            <pre>{uploadResponse}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
