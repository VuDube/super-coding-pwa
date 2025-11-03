import React, { useState } from 'react'

export default function App() {
  const [prompt, setPrompt] = useState("")
  const [provider, setProvider] = useState("ollama")
  const [response, setResponse] = useState("")
  const [loading, setLoading] = useState(false)

  async function send() {
    setLoading(true)
    setResponse("")
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, provider })
      })
      const j = await res.json()
      if (j.ok) setResponse(j.response)
      else setResponse("Error: " + JSON.stringify(j))
    } catch (e) {
      setResponse("Error: " + String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>Super Coding PWA</h1>
      <div>
        <label>Provider: </label>
        <select value={provider} onChange={(e) => setProvider(e.target.value)}>
          <option value="ollama">Ollama (local)</option>
          <option value="huggingface">HuggingFace</option>
          <option value="openrouter">OpenRouter</option>
        </select>
      </div>
      <div style={{marginTop:8}}>
        <textarea value={prompt} onChange={(e)=>setPrompt(e.target.value)} placeholder="Describe the coding task or ask a question..." />
      </div>
      <div style={{marginTop:8}}>
        <button onClick={send} disabled={loading || !prompt}>Send</button>
      </div>
      <div className="response">
        {loading ? "Loading..." : response}
      </div>
      <hr />
      <small>Backend must be running at / (dev proxy or reverse proxy). See README for setup.</small>
    </div>
  )
}
