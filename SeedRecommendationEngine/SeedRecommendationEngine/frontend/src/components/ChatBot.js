import React, { useState, useRef, useEffect } from "react";
import { sendChatMessage } from "../api";
import "./ChatBot.css";

const QUICK_SUGGESTIONS = [
  {
    label: "පොළොන්නරුව (සැප්තැම්බර්)",
    query: "ඉදිරියට එන සැප්තැම්බර් මාසයේ පොළොන්නරුවේ වගාවන් වල තත්ත්වය කොහොමද? මොනවද වගා කරන්න හොඳ?",
  },
  {
    label: "NPK & pH Crop Match",
    query: "My soil test shows N=90, P=45, K=40, and pH=6.5. What is the most recommended crop for high yield?",
  },
  {
    label: "அமில மண் மேலாண்மை",
    query: "மண்ணின் அமிலத்தன்மையை (pH 5.5க்கு கீழ்) எவ்வாறு சீரமைப்பது?",
  },
  {
    label: "පසේ ආම්ලිකතාවය (Dolomite)",
    query: "පසේ ආම්ලිකතාවය (pH අඩු වීම) පාලනය කරන්නේ කොහොමද? ඩොලමයිට් යොදන්නේ කෙසේද?",
  },
  {
    label: "Dry Zone Water Mgmt",
    query: "What are the best irrigation and water conservation practices for dry zone agriculture in Sri Lanka?",
  },
];

function formatMessageContent(rawText) {
  if (!rawText) return null;
  const clean = rawText
    .replace(
      /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{2300}-\u{23FF}\u{2B50}\u{2B55}\u{200D}\u{FE0F}]/gu,
      ""
    )
    .trim();

  const lines = clean.split("\n");

  return lines.map((line, idx) => {
    const trimmed = line.trim();
    if (!trimmed) {
      return <div key={idx} style={{ height: "0.4rem" }} />;
    }

    const parts = [];
    const regex = /\*\*(.*?)\*\*/g;
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(trimmed)) !== null) {
      if (match.index > lastIndex) {
        parts.push(trimmed.substring(lastIndex, match.index));
      }
      parts.push(
        <strong key={match.index} style={{ fontWeight: 700 }}>
          {match[1]}
        </strong>
      );
      lastIndex = regex.lastIndex;
    }
    if (lastIndex < trimmed.length) {
      parts.push(trimmed.substring(lastIndex));
    }

    const contentElements = parts.length > 0 ? parts : trimmed.replace(/\*\*/g, "");
    const isBullet = trimmed.startsWith("•") || trimmed.startsWith("- ") || /^\d+\./.test(trimmed);
    const isHeader = trimmed.endsWith(":") && !isBullet && trimmed.length < 80;

    if (isHeader) {
      return (
        <p
          key={idx}
          style={{
            fontWeight: 700,
            marginTop: "0.5rem",
            marginBottom: "0.2rem",
            color: "#14532d",
          }}
        >
          {contentElements}
        </p>
      );
    }

    return (
      <p
        key={idx}
        style={{
          margin: isBullet ? "0.15rem 0 0.15rem 0.4rem" : "0.22rem 0",
          lineHeight: "1.5",
        }}
      >
        {contentElements}
      </p>
    );
  });
}

export default function ChatBot({ isFloating = false, onClose }) {
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      role: "assistant",
      content:
        "ආයුබෝවන්! / Hello! / வணக்கம்! \nමම ශ්‍රී ලංකාවේ පස, දේශගුණය සහ බෝග නිර්දේශ කිරීම සඳහා පුහුණු කළ Trilingual Agricultural AI Assistant (SLM) වෙමි. ඔබට අවශ්‍ය ප්‍රදේශය, මාසය, පසේ pH හෝ NPK පෝෂක මට්ටම් පිළිබඳව සිංහල, ඉංග්‍රීසි හෝ දෙමළ භාෂාවෙන් විමසන්න.",
      detected_language: "si",
      model_source: "fine_tuned_qwen_lora",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedLang, setSelectedLang] = useState("auto");
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: "user",
      content: query.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await sendChatMessage(query.trim(), selectedLang);
      const fullReply = response.reply;
      const assistantMsgId = (Date.now() + 1).toString();

      const assistantMessage = {
        id: assistantMsgId,
        role: "assistant",
        content: "",
        fullContent: fullReply,
        isStreaming: true,
        detected_language: response.detected_language,
        model_source: response.model_source,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Typewriter streaming
      let charIdx = 0;
      const step = fullReply.length > 500 ? 4 : 2;
      const interval = setInterval(() => {
        charIdx += step;
        if (charIdx >= fullReply.length) {
          charIdx = fullReply.length;
          clearInterval(interval);
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsgId ? { ...m, content: fullReply, isStreaming: false } : m
            )
          );
        } else {
          const partial = fullReply.slice(0, charIdx);
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsgId ? { ...m, content: partial, isStreaming: true } : m
            )
          );
        }
      }, 16);
    } catch (err) {
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "සම්බන්ධතා දෝෂයකි. කරුණාකර Backend සේවාව (FastAPI) ක්‍රියාත්මකව පවතීදැයි පරීක්ෂා කරන්න.\nConnection error. Please ensure the backend is running at http://localhost:8002.",
        detected_language: "en",
        model_source: "error",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleClear = () => {
    setMessages([
      {
        id: "cleared-welcome",
        role: "assistant",
        content: "සංවාදය Reset කරන ලදී. ඔබට අවශ්‍ය කෘෂිකාර්මික ගැටලුව විමසන්න!",
        detected_language: "si",
        model_source: "fine_tuned_qwen_lora",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      },
    ]);
  };

  return (
    <div className={`chatbot-container ${isFloating ? "floating-mode" : ""}`}>
      {/* Header */}
      <div className="chatbot-header">
        <div className="chatbot-title-area">
          <div className="chatbot-avatar" style={{ fontSize: "0.75rem", fontWeight: "bold" }}>
            SLM
          </div>
          <div className="chatbot-title-text">
            <h3>
              Agri-SLM Chatbot
              <span className="chatbot-status-tag">
                <span className="status-dot"></span> Offline AI
              </span>
            </h3>
            <p>Sinhala (සිංහල) • English • Tamil (தமிழ்)</p>
          </div>
        </div>

        <div className="chatbot-controls">
          <select
            className="lang-selector"
            value={selectedLang}
            onChange={(e) => setSelectedLang(e.target.value)}
            title="Select Language / භාෂාව තෝරන්න"
          >
            <option value="auto">Auto Detect</option>
            <option value="si">සිංහල (Sinhala)</option>
            <option value="en">English</option>
            <option value="ta">தமிழ் (Tamil)</option>
          </select>

          <button className="clear-btn" onClick={handleClear} title="Clear conversation">
            Clear
          </button>

          {isFloating && onClose && (
            <button className="clear-btn" onClick={onClose} title="Close Chat">
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="chatbot-messages">
        {messages.length === 1 && (
          <div className="chat-welcome-card">
            <h4>Sri Lanka Agricultural Intelligence SLM</h4>
            <p>
              Ask about district-wise crop suitability (Maha/Yala), seasonal weather impacts, soil pH
              and NPK remediation, and seed selection.
            </p>
            <div className="suggestion-chips">
              {QUICK_SUGGESTIONS.map((s, idx) => (
                <button
                  key={idx}
                  className="chip-btn"
                  onClick={() => handleSend(s.query)}
                  disabled={loading}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message-row ${msg.role}`}>
            <div
              className="message-avatar"
              style={{ fontSize: "0.75rem", fontWeight: "bold", textAlign: "center" }}
            >
              {msg.role === "user" ? "U" : "AI"}
            </div>
            <div className="message-content-wrapper">
              <div className="message-bubble">
                {msg.content ? (
                  formatMessageContent(msg.content)
                ) : (
                  <p style={{ margin: "0.25rem 0", color: "#64748b", fontStyle: "italic" }}>
                    Generating response...
                  </p>
                )}
                {msg.isStreaming && <span className="streaming-cursor">▌</span>}
              </div>
              <div className="message-meta">
                <span>{msg.timestamp}</span>
                {msg.detected_language && (
                  <span className="lang-badge">{msg.detected_language}</span>
                )}
                {msg.model_source && msg.model_source !== "error" && (
                  <span className="model-badge">
                    {msg.model_source === "fine_tuned_qwen_lora" ? "Custom SLM" : "Domain Engine"}
                  </span>
                )}
                {msg.role === "assistant" && (
                  <button
                    className="copy-btn"
                    onClick={() => handleCopy(msg.id, msg.content)}
                    title="Copy text"
                  >
                    {copiedId === msg.id ? "✓ Copied" : "Copy"}
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message-row assistant">
            <div
              className="message-avatar"
              style={{ fontSize: "0.75rem", fontWeight: "bold", textAlign: "center" }}
            >
              AI
            </div>
            <div className="message-bubble typing-bubble">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="chatbot-input-bar">
        <input
          type="text"
          placeholder="ඔබගේ කෘෂිකාර්මික ගැටලුව මෙහි ලියන්න... (Ask in Sinhala, English, or Tamil)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          className="send-btn"
          onClick={() => handleSend()}
          disabled={!input.trim() || loading}
          title="Send message"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
