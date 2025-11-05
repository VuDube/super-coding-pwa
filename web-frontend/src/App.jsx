import React, { useState, useCallback } from 'react'

export default function App() {
  const [prompt, setPrompt] = useState("")
  const [provider, setProvider] = useState("openrouter")
  const [response, setResponse] = useState("")
  const [loading, setLoading] = useState(false)

  const send = useCallback(async () => {
    if (!prompt || loading) return
    
    setLoading(true)
    setResponse("")
    
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "no-cache"
        },
        body: JSON.stringify({ 
          prompt,
          provider,
          timestamp: new Date().toISOString()
        })
      })
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }
      
      const data = await res.json()
      if (data.ok) {
        setResponse(data.response)
      } else {
        setResponse("Error: " + (data.detail || "Unknown error"))
      }
    } catch (e) {
      setResponse("Error: " + (e.message || String(e)))
    } finally {
      setLoading(false)
    }
  }, [prompt, provider, loading])

  return (
    <div className="app">
      <h1>Super Coding PWA</h1>
      <div>
        <label htmlFor="provider-select">Provider: </label>
        <select 
          id="provider-select"
          value={provider} 
          onChange={(e) => setProvider(e.target.value)}
          disabled={loading}
        >
          <option value="openrouter">OpenRouter</option>
          <option value="huggingface">HuggingFace</option>
        </select>
      </div>
      <div style={{marginTop:8}}>
        <textarea 
          value={prompt} 
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the coding task or ask a question..."
          disabled={loading}
          aria-label="Prompt input"
        />
      </div>
      <div style={{marginTop:8}}>
        <button 
          onClick={send} 
          disabled={loading || !prompt}
          aria-busy={loading}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
      <div className="response" role="status" aria-live="polite">
        {loading ? "Loading..." : response}
      </div>
      <hr />
      <small>Version: 2025.11.05</small>
    </div>
  )
}
