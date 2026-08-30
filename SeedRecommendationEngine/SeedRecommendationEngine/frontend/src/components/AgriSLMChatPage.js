import React, { useState, useRef, useEffect } from "react";
import { sendChatMessage, uploadChatFile, fetchChatStatus } from "../api";
import "./AgriSLMChatPage.css";

const SESSIONS_STORAGE_KEY = "agri_slm_chat_sessions_v1";
const ACTIVE_SESSION_STORAGE_KEY = "agri_slm_active_session_id_v1";

const QUICK_SUGGESTIONS = [
  {
    label: "පොළොන්නරුව (මහ කන්නය)",
    query: "ඉදිරියට එන සැප්තැම්බර් මාසයේ පොළොන්නරුවේ වගාවන් වල තත්ත්වය කොහොමද? මොනවද වගා කරන්න හොඳ?",
    lang: "si",
  },
  {
    label: "NPK & pH Crop Match",
    query: "My soil test shows N=90, P=45, K=40, and pH=6.5. What is the most recommended crop for high yield?",
    lang: "en",
  },
  {
    label: "පසේ ආම්ලිකතාවය (Dolomite)",
    query: "පසේ ආම්ලිකතාවය (pH 5.2) පාලනය කරන්නේ කොහොමද? ඩොලමයිට් යෙදිය යුතු මාත්‍රාව කුමක්ද?",
    lang: "si",
  },
  {
    label: "யாழ்ப்பாணம் பயிர்ச்செய்கை",
    query: "யாழ்ப்பாணத்தில் செப்டம்பர் மாதத்தில் என்னென்ன பயிர்களை வெற்றிகரமாக பயிரிடலாம்?",
    lang: "ta",
  },
  {
    label: "Dry Zone Water Management",
    query: "What are the most effective irrigation and water conservation techniques for dry zone field crops in Sri Lanka?",
    lang: "en",
  },
  {
    label: "අනුරාධපුර බඩඉරිඟු හා ධාන්‍ය",
    query: "අනුරාධපුර ප්‍රදේශයේ රතු-දුඹුරු පසට (RBE) වඩාත්ම ගැළපෙන ධාන්‍ය හා අතිරේක බෝග මොනවාද?",
    lang: "si",
  },
];

const INITIAL_WELCOME_MESSAGE = {
  id: "welcome-init",
  role: "assistant",
  content:
    "ආයුබෝවන්! / Hello! / வணக்கம்!\n\n" +
    "මම ශ්‍රී ලංකාවේ පස, දේශගුණය සහ බෝග නිර්දේශ කිරීම සඳහා විශේෂිත වූ Trilingual Agri-SLM Research Assistant වෙමි.\n\n" +
    "මම කිසිදු Cloud API Key එකක් භාවිතා නොකර, 100%ක් Offline ඔබගේ පරිගණකයේම ක්‍රියාත්මක වන Trained ML Models (Accuracy 99.5%) මඟින් ක්‍රියාත්මක වෙමි.\n\n" +
    "ඔබට අවශ්‍ය කෘෂිකාර්මික ගැටලුව සිංහල, ඉංග්‍රීසි හෝ දෙමළ භාෂාවෙන් විමසන්න, නැතහොත් පස් පරීක්ෂණ වාර්තාවක් (PDF/CSV) upload කරන්න!",
  detected_language: "si",
  model_source: "trained_ml_classifier",
  timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
};

function formatMessageContent(rawText) {
  if (!rawText) return null;
  // 1. Strip any emoji unicode characters
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
      return <div key={idx} className="msg-spacer" style={{ height: "0.45rem" }} />;
    }

    // Replace bold **text** with clean <strong>
    const parts = [];
    const regex = /\*\*(.*?)\*\*/g;
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(trimmed)) !== null) {
      if (match.index > lastIndex) {
        parts.push(trimmed.substring(lastIndex, match.index));
      }
      parts.push(
        <strong key={match.index} className="msg-strong">
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
    const isHeader = trimmed.endsWith(":") && !isBullet && trimmed.length < 90;

    if (isHeader) {
      return (
        <p
          key={idx}
          className="msg-line msg-header-line"
          style={{
            fontWeight: 700,
            marginTop: "0.65rem",
            marginBottom: "0.25rem",
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
        className={`msg-line ${isBullet ? "msg-bullet-line" : ""}`}
        style={{
          margin: isBullet ? "0.2rem 0 0.2rem 0.5rem" : "0.25rem 0",
          lineHeight: "1.55",
        }}
      >
        {contentElements}
      </p>
    );
  });
}

function generateNewSession() {
  const newId = "session_" + Date.now();
  return {
    id: newId,
    title: "New Agricultural Consultation",
    createdAt: new Date().toLocaleDateString([], {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }),
    messages: [INITIAL_WELCOME_MESSAGE],
  };
}

export default function AgriSLMChatPage({ onNavigateHome }) {
  const [sessions, setSessions] = useState(() => {
    try {
      const saved = localStorage.getItem(SESSIONS_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.warn("Failed to load sessions from localStorage:", e);
    }
    return [generateNewSession()];
  });

  const [activeSessionId, setActiveSessionId] = useState(() => {
    try {
      const savedId = localStorage.getItem(ACTIVE_SESSION_STORAGE_KEY);
      if (savedId) return savedId;
    } catch (e) { }
    return sessions[0]?.id || "session_default";
  });

  const activeSession = sessions.find((s) => s.id === activeSessionId) || sessions[0];
  const messages = activeSession?.messages || [];

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedLang, setSelectedLang] = useState("auto");
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileExtracting, setFileExtracting] = useState(false);
  const [engineStatus, setEngineStatus] = useState({
    status: "connecting",
    engine_name: "Agri-SLM Engine",
    device: "Local Engine",
    ml_model_accuracy: 99.55,
  });
  const [copiedId, setCopiedId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);
  const activeStreamIntervals = useRef({});

  // Cleanup active intervals on unmount
  useEffect(() => {
    return () => {
      Object.values(activeStreamIntervals.current).forEach((interval) => clearInterval(interval));
    };
  }, []);

  const handleSkipStreaming = (msgId) => {
    if (activeStreamIntervals.current[msgId]) {
      clearInterval(activeStreamIntervals.current[msgId]);
      delete activeStreamIntervals.current[msgId];
    }
    setSessions((prev) =>
      prev.map((s) => ({
        ...s,
        messages: s.messages.map((m) =>
          m.id === msgId ? { ...m, content: m.fullContent || m.content, isStreaming: false } : m
        ),
      }))
    );
  };

  // Save sessions to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(SESSIONS_STORAGE_KEY, JSON.stringify(sessions));
    } catch (e) { }
  }, [sessions]);

  // Save active session ID
  useEffect(() => {
    try {
      localStorage.setItem(ACTIVE_SESSION_STORAGE_KEY, activeSessionId);
    } catch (e) { }
  }, [activeSessionId]);

  // Fetch backend engine status on load
  useEffect(() => {
    let isMounted = true;
    async function checkStatus() {
      try {
        const statusData = await fetchChatStatus();
        if (isMounted) {
          setEngineStatus(statusData);
        }
      } catch (err) {
        if (isMounted) {
          setEngineStatus({
            status: "offline",
            engine_name: "Backend Offline",
            device: "Please ensure FastAPI is active on port 8002",
            ml_model_accuracy: 99.55,
          });
        }
      }
    }
    checkStatus();
    const interval = setInterval(checkStatus, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleCreateNewChat = () => {
    const newSession = generateNewSession();
    setSessions((prev) => [newSession, ...prev]);
    setActiveSessionId(newSession.id);
    setSelectedFile(null);
    setInput("");
  };

  const handleDeleteSession = (sessionId, e) => {
    e.stopPropagation();
    if (sessions.length <= 1) {
      const fresh = generateNewSession();
      setSessions([fresh]);
      setActiveSessionId(fresh.id);
      return;
    }
    const updated = sessions.filter((s) => s.id !== sessionId);
    setSessions(updated);
    if (activeSessionId === sessionId) {
      setActiveSessionId(updated[0].id);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setSelectedFile(file);
    if (!input.trim()) {
      setInput(`Please analyze this ${file.name} laboratory soil report and provide ML crop recommendations.`);
    }
  };

  const handleSend = async (textOverride = null) => {
    const text = (textOverride !== null ? textOverride : input).trim();
    if ((!text && !selectedFile) || loading) return;

    const userTimestamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsgId = Date.now().toString();

    const userMessage = {
      id: userMsgId,
      role: "user",
      content: text || `Uploaded document for agronomic evaluation: ${selectedFile?.name}`,
      attachedFileName: selectedFile ? selectedFile.name : null,
      timestamp: userTimestamp,
    };

    const updatedMessagesWithUser = [...messages, userMessage];

    let sessionTitle = activeSession.title;
    if (sessionTitle === "New Agricultural Consultation" && text) {
      sessionTitle = text.slice(0, 32) + (text.length > 32 ? "..." : "");
    }

    setSessions((prev) =>
      prev.map((s) =>
        s.id === activeSessionId
          ? { ...s, title: sessionTitle, messages: updatedMessagesWithUser }
          : s
      )
    );

    const currentFile = selectedFile;
    setInput("");
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    setLoading(true);

    try {
      let response;
      if (currentFile) {
        setFileExtracting(true);
        response = await uploadChatFile(currentFile, text, selectedLang, activeSessionId);
      } else {
        response = await sendChatMessage(text, selectedLang, activeSessionId);
      }

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
        agro_zone: response.agro_zone,
        soil_type: response.soil_type,
        extracted_features: response.extracted_features,
        recommended_crops: response.recommended_crops,
        soil_remediation: response.soil_remediation,
        latency_ms: response.latency_ms,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSessionId
            ? { ...s, messages: [...updatedMessagesWithUser, assistantMessage] }
            : s
        )
      );

      // Token-by-token streaming simulation
      let charIdx = 0;
      const step = fullReply.length > 800 ? 6 : fullReply.length > 400 ? 4 : 2;
      const interval = setInterval(() => {
        charIdx += step;
        if (charIdx >= fullReply.length) {
          charIdx = fullReply.length;
          clearInterval(interval);
          delete activeStreamIntervals.current[assistantMsgId];
          setSessions((prev) =>
            prev.map((s) =>
              s.id === activeSessionId
                ? {
                  ...s,
                  messages: s.messages.map((m) =>
                    m.id === assistantMsgId
                      ? { ...m, content: fullReply, isStreaming: false }
                      : m
                  ),
                }
                : s
            )
          );
        } else {
          const partial = fullReply.slice(0, charIdx);
          setSessions((prev) =>
            prev.map((s) =>
              s.id === activeSessionId
                ? {
                  ...s,
                  messages: s.messages.map((m) =>
                    m.id === assistantMsgId
                      ? { ...m, content: partial, isStreaming: true }
                      : m
                  ),
                }
                : s
            )
          );
        }
      }, 15);

      activeStreamIntervals.current[assistantMsgId] = interval;
    } catch (err) {
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "සම්බන්ධතා දෝෂයකි. Backend සේවාව (FastAPI) http://localhost:8002 හි ක්‍රියාත්මකව පවතීදැයි පරීක්ෂා කරන්න.\n\n" +
          "Connection error. Please ensure the backend server is running at http://localhost:8002.",
        detected_language: "en",
        model_source: "error",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSessionId
            ? { ...s, messages: [...updatedMessagesWithUser, errorMessage] }
            : s
        )
      );
    } finally {
      setLoading(false);
      setFileExtracting(false);
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

  const handleClearCurrentChat = () => {
    setSessions((prev) =>
      prev.map((s) =>
        s.id === activeSessionId
          ? {
            ...s,
            title: "Cleared Consultation",
            messages: [
              {
                id: "cleared-reset",
                role: "assistant",
                content: "සංවාදය Reset කරන ලදී. ඔබට අවශ්‍ය නව කෘෂිකාර්මික ගැටලුවක් විමසන්න!",
                detected_language: "si",
                model_source: "trained_ml_classifier",
                timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              },
            ],
          }
          : s
      )
    );
  };

  const handleExportReport = () => {
    let report = "=========================================================\n";
    report += "SRI LANKA AGRICULTURAL SLM RESEARCH CONSULTATION REPORT\n";
    report += `Generated On: ${new Date().toLocaleString()}\n`;
    report += `Session: ${activeSession.title}\n`;
    report += "Engine: Agri-SLM Trilingual Classifier (Accuracy 99.5%)\n";
    report += "Cloud Dependency: None (100% On-Device & Private)\n";
    report += "=========================================================\n\n";

    messages.forEach((msg, idx) => {
      const sender = msg.role === "user" ? "USER / FARMER" : "AGRI-SLM RESEARCH ASSISTANT";
      report += `[${idx + 1}] ${sender} (${msg.timestamp})\n`;
      report += `Language: ${msg.detected_language || "N/A"} | Source: ${msg.model_source || "N/A"}\n`;
      if (msg.agro_zone) report += `Agro-Ecological Zone: ${msg.agro_zone}\n`;
      if (msg.soil_type) report += `Dominant Soil: ${msg.soil_type}\n`;
      if (msg.recommended_crops && msg.recommended_crops.length > 0) {
        report += `Ranked Crop Suitability: ${msg.recommended_crops.map((c) => `${c.crop} (${c.confidence}%)`).join(", ")}\n`;
      }
      report += `\n${msg.content}\n`;
      report += "---------------------------------------------------------\n\n";
    });

    const blob = new Blob([report], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `Agri_SLM_Report_${activeSessionId}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="agri-chat-page-root">
      {/* Sidebar */}
      <aside className={`agri-chat-sidebar ${sidebarOpen ? "open" : "collapsed"}`}>
        <div className="sidebar-header">
          <div className="sidebar-brand">
            <span className="brand-badge">AGRI-SLM</span>
            <div className="brand-text">
              <h3>Research Assistant</h3>
              <p>Trilingual Agro-Intelligence</p>
            </div>
          </div>
          <button
            className="sidebar-collapse-btn"
            onClick={() => setSidebarOpen((prev) => !prev)}
            title={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
          >
            {sidebarOpen ? "◀" : "▶"}
          </button>
        </div>

        <div className="sidebar-actions">
          <button className="new-chat-btn" onClick={handleCreateNewChat}>
            <span className="btn-plus">＋</span>
            <span>New Agricultural Chat</span>
          </button>
        </div>

        {/* Sessions History List */}
        <div className="sidebar-section">
          <div className="section-heading">CONSULTATION SESSIONS</div>
          <div className="sessions-list">
            {sessions.map((s) => (
              <div
                key={s.id}
                className={`session-item ${s.id === activeSessionId ? "active" : ""}`}
                onClick={() => setActiveSessionId(s.id)}
              >
                <span className="session-bullet">•</span>
                <div className="session-info">
                  <div className="session-title">{s.title}</div>
                  <div className="session-date">{s.createdAt}</div>
                </div>
                <button
                  className="session-delete-btn"
                  onClick={(e) => handleDeleteSession(s.id, e)}
                  title="Delete consultation"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Test Presets */}
        <div className="sidebar-section">
          <div className="section-heading">RESEARCH PROMPTS</div>
          <div className="preset-chips-list">
            {QUICK_SUGGESTIONS.map((preset, idx) => (
              <button
                key={idx}
                className="preset-chip"
                onClick={() => handleSend(preset.query)}
                disabled={loading}
              >
                <span className="chip-lang-tag">{preset.lang.toUpperCase()}</span>
                <span className="chip-text">{preset.label}</span>
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Chat Workspace */}
      <main className="agri-chat-main">
        {/* Workspace Top Header Bar */}
        <header className="chat-top-header">
          <div className="header-left">
            {!sidebarOpen && (
              <button
                className="open-sidebar-btn"
                onClick={() => setSidebarOpen(true)}
                title="Open sidebar"
              >
                ☰
              </button>
            )}
            <div className="active-session-title-box">
              <h2>{activeSession.title}</h2>
              <span className="privacy-badge">Private Local Model</span>
            </div>
          </div>

          <div className="header-actions">
            {/* Language Selector */}
            <div className="lang-select-wrapper">
              <label htmlFor="lang-select">Language:</label>
              <select
                id="lang-select"
                className="lang-dropdown"
                value={selectedLang}
                onChange={(e) => setSelectedLang(e.target.value)}
              >
                <option value="auto">Auto Detect (ස්වයංක්‍රීය)</option>
                <option value="si">සිංහල (Sinhala)</option>
                <option value="en">English</option>
                <option value="ta">தமிழ் (Tamil)</option>
              </select>
            </div>

            <button className="action-btn" onClick={handleExportReport} title="Export research conversation">
              Export Report
            </button>

            <button className="action-btn clear-action" onClick={handleClearCurrentChat} title="Clear conversation">
              Clear
            </button>
          </div>
        </header>

        {/* Message Feed Area */}
        <div className="chat-messages-container">
          {messages.length === 1 && (
            <div className="research-welcome-banner">
              <div className="welcome-banner-badge">AGRICULTURAL RESEARCH ENGINE</div>
              <h3>Trilingual Agronomic Intelligence & Decision Support Suite</h3>
              <p>
                This system runs custom-trained machine learning classifiers and agro-ecological domain rules
                grounded in Sri Lanka's 25 districts, Maha/Yala seasonal calendars, and laboratory soil test analysis.
              </p>
              <div className="welcome-feature-grid">
                <div className="feature-box">
                  <h4>Soil Lab Report Analysis</h4>
                  <p>Upload PDF or CSV soil test sheets to extract N, P, K, pH, and get ML-ranked crop recommendations.</p>
                </div>
                <div className="feature-box">
                  <h4>25 Districts & Agro-Zones</h4>
                  <p>Accurate seasonal cultivation calendars for Dry, Intermediate, and Wet zone microclimates.</p>
                </div>
                <div className="feature-box">
                  <h4>Trilingual Grounding</h4>
                  <p>Native comprehension and generation in Sinhala (සිංහල), English, and Tamil (தமிழ்).</p>
                </div>
                <div className="feature-box">
                  <h4>Zero Cloud API Dependency</h4>
                  <p>Fully local inference with guaranteed farmer data privacy and zero API key requirements.</p>
                </div>
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className={`message-row ${msg.role}`}>
              <div className="msg-avatar">
                <span className="avatar-initial">{msg.role === "user" ? "U" : "AI"}</span>
              </div>

              <div className="msg-bubble-container">
                <div className="msg-bubble">
                  {msg.attachedFileName && (
                    <div className="msg-file-tag">
                      <span className="tag-icon">File:</span>
                      <span className="tag-filename">{msg.attachedFileName}</span>
                    </div>
                  )}

                  <div className="msg-text-content">
                    {msg.content ? (
                      formatMessageContent(msg.content)
                    ) : (
                      <p className="msg-line streaming-placeholder">Reasoning and synthesizing neural response...</p>
                    )}
                    {msg.isStreaming && <span className="streaming-cursor">▌</span>}
                  </div>

                  {/* Streaming active indicator with Skip action */}
                  {msg.isStreaming && (
                    <div className="streaming-action-bar">
                      <span className="streaming-badge">SLM Token Stream</span>
                      <button
                        className="skip-stream-btn"
                        onClick={() => handleSkipStreaming(msg.id)}
                        title="Display full response immediately"
                      >
                        Skip Typing
                      </button>
                    </div>
                  )}

                  {/* Research Cards for ML Insights (Shown once streaming completes) */}
                  {msg.role === "assistant" && !msg.isStreaming && (msg.agro_zone || msg.recommended_crops) && (
                    <div className="msg-research-card fade-in">
                      <div className="card-header-bar">
                        <span>AGRONOMIC DECISION METRICS</span>
                        {msg.latency_ms && <span className="latency-tag">{msg.latency_ms} ms</span>}
                      </div>

                      <div className="metrics-pills-row">
                        {msg.agro_zone && (
                          <div className="metric-pill">
                            <span className="pill-k">Zone</span>
                            <span className="pill-v">{msg.agro_zone}</span>
                          </div>
                        )}
                        {msg.soil_type && (
                          <div className="metric-pill">
                            <span className="pill-k">Soil Order</span>
                            <span className="pill-v">{msg.soil_type}</span>
                          </div>
                        )}
                        {msg.recommended_crops && msg.recommended_crops.length > 0 && (
                          <div className="metric-pill highlight">
                            <span className="pill-k">Top Crop</span>
                            <span className="pill-v">
                              {msg.recommended_crops[0].sinhala_name || msg.recommended_crops[0].crop} (
                              {msg.recommended_crops[0].confidence}%)
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <div className="msg-meta-bar">
                  <span className="msg-time">{msg.timestamp}</span>
                  {msg.detected_language && (
                    <span className="lang-tag">{msg.detected_language.toUpperCase()}</span>
                  )}
                  {msg.model_source && msg.model_source !== "error" && (
                    <span className="model-source-tag">
                      {msg.model_source === "trained_ml_classifier"
                        ? "ML Classifier (99.5% Acc)"
                        : "Agri-Reasoning Engine"}
                    </span>
                  )}
                  {msg.role === "assistant" && (
                    <button
                      className="msg-copy-btn"
                      onClick={() => handleCopy(msg.id, msg.content)}
                      title="Copy response"
                    >
                      {copiedId === msg.id ? "✓ Copied" : "Copy"}
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="msg-avatar">
                <span className="avatar-initial">AI</span>
              </div>
              <div className="msg-bubble-container">
                <div className="msg-bubble typing-indicator-box">
                  <div className="typing-pulse-dot"></div>
                  <div className="typing-pulse-dot"></div>
                  <div className="typing-pulse-dot"></div>
                  <span className="typing-status-text">
                    {fileExtracting ? "Extracting soil test parameters..." : "Agri-SLM is reasoning..."}
                  </span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar & Attachment Zone */}
        <footer className="chat-bottom-input-zone">
          {/* File Preview Attachment Chip */}
          {selectedFile && (
            <div className="file-attachment-preview">
              <span className="file-icon">[Document]</span>
              <span className="file-name">{selectedFile.name}</span>
              <span className="file-size">({(selectedFile.size / 1024).toFixed(1)} KB)</span>
              <button
                className="remove-file-btn"
                onClick={() => {
                  setSelectedFile(null);
                  if (fileInputRef.current) fileInputRef.current.value = "";
                }}
                title="Remove attached file"
              >
                ✕
              </button>
            </div>
          )}

          {/* Hidden File Input */}
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: "none" }}
            accept=".pdf,.csv,.txt"
            onChange={handleFileSelect}
          />

          <div className="chat-input-bar">
            <button
              className="attach-file-btn"
              onClick={() => fileInputRef.current?.click()}
              title="Upload Soil Test Lab Report (PDF, CSV, TXT)"
              disabled={loading}
            >
              <span className="attach-label">Upload Report</span>
            </button>

            <textarea
              className="chat-textarea"
              placeholder="ඔබගේ කෘෂිකාර්මික ගැටලුව ලියන්න හෝ පස් පරීක්ෂණ වාර්තාවක් එක් කරන්න... (Sinhala, English, Tamil)"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              rows={1}
            />

            <button
              className="send-message-btn"
              onClick={() => handleSend()}
              disabled={(!input.trim() && !selectedFile) || loading}
              title="Send question"
            >
              {loading ? "..." : "Send"}
            </button>
          </div>
          <div className="input-helper-note">
            Press <strong>Enter</strong> to send, <strong>Shift+Enter</strong> for newline. Supported files: PDF, CSV, TXT.
          </div>
        </footer>
      </main>
    </div>
  );
}
