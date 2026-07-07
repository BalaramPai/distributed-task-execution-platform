import './App.css'

function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f5f7fb",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: "700px",
          backgroundColor: "white",
          padding: "40px",
          borderRadius: "16px",
          boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
        }}
      >
        <h1
          style={{
            fontSize: "36px",
            marginBottom: "10px",
            color: "#2563eb",
          }}
        >
          Distributed Task Platform
        </h1>

        <p
          style={{
            fontSize: "18px",
            color: "#555",
            marginBottom: "30px",
          }}
        >
          Welcome! This platform lets you manage distributed background tasks.
        </p>

        <button
          style={{
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            padding: "12px 24px",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "16px",
          }}
        >
          Create Task
        </button>

        <hr style={{ margin: "30px 0" }} />

        <h2>Task Statistics</h2>

        <ul
          style={{
            marginTop: "15px",
            lineHeight: "2",
            fontSize: "18px",
          }}
        >
          <li>🟡 Pending : 0</li>
          <li>🔵 Running : 0</li>
          <li>🟢 Completed : 0</li>
          <li>🔴 Failed : 0</li>
        </ul>
      </div>
    </div>
  );
}

export default App;