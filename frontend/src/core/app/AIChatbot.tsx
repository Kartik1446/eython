import React, { useState, useRef, useEffect } from 'react'

interface Message {
  id: string
  sender: 'user' | 'assistant'
  text: string
  timestamp: string
}

interface AIChatbotProps {
  projectName?: string
}

const HINDSIGHT_API_URL = 'https://api.hindsight.vectorize.io/v1/default/banks/cybersecurity-assistant/reflect'
const HINDSIGHT_PROMO_CODE = 'MEMHACK1019'
const HINDSIGHT_API_KEY = 'hsk_50b425c99734390d6a9f74d59a7f5e78_021b3c05d1268660'

export const AIChatbot: React.FC<AIChatbotProps> = ({ projectName = 'Honeypot Network' }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: `Hello! I am your **Hindsight AI Threat Actor Attribution Analyst** for **${projectName}**.\n\nAsk me about security concepts, telemetry analysis, or guidance!\n\n🎁 **Coupon Code: MEMHACK1019** (Claim free credits on [Hindsight Cloud](https://vectorize.io))`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    if (isOpen) {
      scrollToBottom()
    }
  }, [messages, isOpen])

  const handleSend = async (textToSend?: string) => {
    const queryText = (textToSend || input).trim()
    if (!queryText || loading) return

    const userMsg: Message = {
      id: String(Date.now()),
      sender: 'user',
      text: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }

    setMessages((prev) => [...prev, userMsg])
    if (!textToSend) setInput('')
    setLoading(true)

    try {
      const response = await fetch(HINDSIGHT_API_URL, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${HINDSIGHT_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: `[Context: ${projectName}] ${queryText}`,
        }),
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      const assistantMsg: Message = {
        id: String(Date.now() + 1),
        sender: 'assistant',
        text: data.text || 'I analyzed your query but received an empty response.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      setMessages((prev) => [...prev, assistantMsg])
    } catch (err: unknown) {
      const errorText = err instanceof Error ? err.message : 'Unknown error'
      const errMsg: Message = {
        id: String(Date.now() + 1),
        sender: 'assistant',
        text: `⚠️ **Error communicating with Hindsight AI**: ${errorText}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      setMessages((prev) => [...prev, errMsg])
    } finally {
      setLoading(false)
    }
  }

  const quickPrompts = ['What SSH commands indicate brute-force bots?', 'Map honeypot telemetry to MITRE ATT&CK', 'How to deploy low-interaction traps?', 'Analyze attacker IOC payloads']

  return (
    <div style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 999999, fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          style={{
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #8B5CF6 0%, #0084FF 100%)',
            border: 'none',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            transition: 'transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.08)'
            e.currentTarget.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.6)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)'
            e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.4)'
          }}
          title="Open AI Assistant (Hindsight)"
          aria-label="Open AI Assistant"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            <circle cx="12" cy="11" r="3" />
            <path d="M12 8v1" />
          </svg>
          <span
            style={{
              position: 'absolute',
              top: '2px',
              right: '2px',
              width: '14px',
              height: '14px',
              backgroundColor: '#10B981',
              borderRadius: '50%',
              border: '2px solid #0D1117',
            }}
          />
        </button>
      )}

      {isOpen && (
        <div
          style={{
            width: '420px',
            maxWidth: 'calc(100vw - 32px)',
            height: '580px',
            maxHeight: 'calc(100vh - 80px)',
            backgroundColor: '#0D1117',
            border: '1px solid #30363D',
            borderRadius: '16px',
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.6)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            color: '#E6EDF3',
          }}
        >
          <div
            style={{
              padding: '14px 18px',
              background: 'linear-gradient(180deg, #161B22 0%, #0D1117 100%)',
              borderBottom: '1px solid #30363D',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: 'linear-gradient(135deg, #8B5CF6 0%, #0084FF 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#fff',
                }}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  <circle cx="12" cy="11" r="2" />
                </svg>
              </div>
              <div>
                <div style={{ fontWeight: 600, fontSize: '15px', color: '#F0F6FC' }}>Hindsight AI Assistant</div>
                <div style={{ fontSize: '11px', color: '#8B949E', display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <span style={{ width: '7px', height: '7px', borderRadius: '50%', backgroundColor: '#10B981', display: 'inline-block' }} />
                  {projectName} • Connected
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '6px' }}>
              <button
                onClick={() =>
                  setMessages([
                    {
                      id: 'welcome',
                      sender: 'assistant',
                      text: `Chat reset. How can I assist you with **${projectName}**?`,
                      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    },
                  ])
                }
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#8B949E',
                  cursor: 'pointer',
                  padding: '6px',
                  borderRadius: '6px',
                  fontSize: '12px',
                }}
                title="Clear Chat"
              >
                Clear
              </button>
              <button
                onClick={() => setIsOpen(false)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#8B949E',
                  cursor: 'pointer',
                  padding: '6px 8px',
                  borderRadius: '6px',
                  fontSize: '18px',
                  lineHeight: '1',
                }}
                title="Close"
              >
                ×
              </button>
            </div>
          </div>

          <div
            style={{
              flex: 1,
              padding: '16px',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '14px',
              fontSize: '13.5px',
              lineHeight: '1.5',
            }}
          >
            {messages.map((m) => (
              <div
                key={m.id}
                style={{
                  alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '85%',
                }}
              >
                <div
                  style={{
                    backgroundColor: m.sender === 'user' ? '#8B5CF6' : '#161B22',
                    color: m.sender === 'user' ? '#FFFFFF' : '#C9D1D9',
                    border: m.sender === 'user' ? 'none' : '1px solid #30363D',
                    borderRadius: m.sender === 'user' ? '14px 14px 2px 14px' : '14px 14px 14px 2px',
                    padding: '10px 14px',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}
                >
                  {m.text}
                </div>
                <div
                  style={{
                    fontSize: '10px',
                    color: '#6E7681',
                    marginTop: '4px',
                    textAlign: m.sender === 'user' ? 'right' : 'left',
                  }}
                >
                  {m.timestamp}
                </div>
              </div>
            ))}

            {loading && (
              <div
                style={{
                  alignSelf: 'flex-start',
                  backgroundColor: '#161B22',
                  border: '1px solid #30363D',
                  borderRadius: '14px 14px 14px 2px',
                  padding: '10px 16px',
                  display: 'flex',
                  gap: '6px',
                  alignItems: 'center',
                }}
              >
                <span style={{ fontSize: '12px', color: '#8B949E' }}>Hindsight thinking...</span>
                <span style={{ display: 'inline-block', width: '6px', height: '6px', backgroundColor: '#8B5CF6', borderRadius: '50%' }} />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div
            style={{
              padding: '8px 14px',
              display: 'flex',
              gap: '6px',
              overflowX: 'auto',
              borderTop: '1px solid #21262D',
              backgroundColor: '#0D1117',
              scrollbarWidth: 'none',
            }}
          >
            {quickPrompts.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(q)}
                disabled={loading}
                style={{
                  whiteSpace: 'nowrap',
                  fontSize: '11px',
                  padding: '4px 10px',
                  borderRadius: '12px',
                  backgroundColor: '#161B22',
                  border: '1px solid #30363D',
                  color: '#8B5CF6',
                  cursor: 'pointer',
                }}
              >
                {q}
              </button>
            ))}
          </div>

          <div
            style={{
              padding: '12px 14px',
              borderTop: '1px solid #30363D',
              backgroundColor: '#161B22',
              display: 'flex',
              gap: '8px',
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSend()
              }}
              placeholder="Ask AI Cyber Assistant..."
              disabled={loading}
              style={{
                flex: 1,
                backgroundColor: '#0D1117',
                border: '1px solid #30363D',
                borderRadius: '8px',
                padding: '10px 12px',
                color: '#F0F6FC',
                fontSize: '13px',
                outline: 'none',
              }}
            />
            <button
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
              style={{
                backgroundColor: input.trim() && !loading ? '#8B5CF6' : '#21262D',
                border: 'none',
                borderRadius: '8px',
                padding: '0 14px',
                color: input.trim() && !loading ? '#FFFFFF' : '#484F58',
                fontWeight: 600,
                cursor: input.trim() && !loading ? 'pointer' : 'default',
              }}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
export default AIChatbot
