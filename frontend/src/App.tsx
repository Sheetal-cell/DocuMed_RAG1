import { useState } from "react";
import {
  Activity,
  BookOpen,
  Bot,
  Check,
  Clipboard,
  FileText,
  Menu,
  Send,
  ShieldCheck,
  Sparkles,
  Stethoscope,
  User,
  X,
} from "lucide-react";

import "./App.css";

interface Source {
  source: string;
  page: number;
  distance: number;
}

interface ApiResponse {
  question: string;
  answer: string;
  sources?: Source[];
}

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const askQuestion = async (customQuestion?: string) => {
    const query = (customQuestion ?? question).trim();

    if (!query || loading) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: query,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: query,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to connect to DocuMed API.");
      }

      const data: ApiResponse = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the DocuMed backend. Please make sure the FastAPI server is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const uploadPdf = async (
  event: React.ChangeEvent<HTMLInputElement>
) => {

  const file = event.target.files?.[0];

  if (!file) return;

  if (file.type !== "application/pdf") {

    alert("Please select a PDF file.");

    return;
  }

  setLoading(true);

  try {

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
      "http://127.0.0.1:8000/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Upload failed.");
    }

    const data = await response.json();

    if (!data.success) {
      throw new Error(
        data.message || "Unable to process PDF."
      );
    }

    alert(
      `${data.filename} uploaded successfully.\n\n` +
      `${data.chunks} text chunks added to the knowledge base.`
    );

  } catch (error) {

    console.error(error);

    alert(
      "Unable to upload the PDF. " +
      "Please make sure the DocuMed backend is running."
    );

  } finally {

    setLoading(false);

    // Allow the same file to be selected again
    event.target.value = "";
  }
};

  const copyAnswer = async (text: string) => {
    await navigator.clipboard.writeText(text);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1500);
  };

  const clearChat = () => {
    setMessages([]);
  };

  const suggestedQuestions = [
    "What is the HEARTS technical package?",
    "What is hypertension?",
    "What are the main modules of HEARTS?",
  ];

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div className="brand">
            <div className="brand-icon">
              <Stethoscope size={24} />
            </div>

            <div>
              <h2>DocuMed</h2>
              <span>Medical RAG Assistant</span>
            </div>
          </div>

          <button
            className="mobile-close"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <button
          className="new-chat"
          onClick={clearChat}
        >
          <Sparkles size={18} />
          New conversation
        </button>

        <label className="upload-pdf">
  <FileText size={18} />
  Upload PDF

  <input
    type="file"
    accept=".pdf,application/pdf"
    onChange={uploadPdf}
    hidden
  />
</label>

        <div className="sidebar-section">
          <p className="section-title">
            <BookOpen size={15} />
            KNOWLEDGE BASE
          </p>

          <div className="document-card">
            <div className="document-icon">
              <FileText size={20} />
            </div>

            <div>
              <strong>heart.pdf</strong>
              <span>Cardiovascular protocols</span>
            </div>

            <div className="status-dot" />
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="safety-card">
            <ShieldCheck size={19} />

            <div>
              <strong>Medical safety</strong>
              <p>
                DocuMed provides document-grounded
                information and is not a substitute
                for professional medical advice.
              </p>
            </div>
          </div>

          <div className="version">
            DocuMed RAG • Local AI
          </div>
        </div>
      </aside>

      {/* MAIN */}

      <main className="main">

        {/* HEADER */}

        <header className="topbar">

          <button
            className="menu-button"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={22} />
          </button>

          <div className="mobile-brand">
            <div className="brand-icon">
              <Stethoscope size={20} />
            </div>

            <strong>DocuMed</strong>
          </div>

          <div className="topbar-right">

            <div className="ai-status">
              <span className="online-dot" />
              AI Online
            </div>

            <div className="model-badge">
              <Bot size={16} />
              Qwen + LoRA
            </div>

          </div>
        </header>

        {/* CHAT */}

        <section className="chat-area">

          {messages.length === 0 ? (

            <div className="welcome">

              <div className="welcome-icon">
                <Activity size={34} />
              </div>

              <div className="welcome-badge">
                <Sparkles size={15} />
                Document-grounded medical AI
              </div>

              <h1>
                Ask your medical
                <br />
                <span>documents.</span>
              </h1>

              <p>
                DocuMed retrieves relevant information from
                trusted medical documents and generates
                grounded answers using your local AI model.
              </p>

              <div className="suggestions">

                {suggestedQuestions.map((item) => (

                  <button
                    key={item}
                    onClick={() => askQuestion(item)}
                  >
                    <span>{item}</span>
                    <Send size={15} />
                  </button>

                ))}

              </div>

            </div>

          ) : (

            <div className="messages">

              {messages.map((message, index) => (

                <div
                  key={index}
                  className={`message-row ${message.role}`}
                >

                  <div className="avatar">

                    {message.role === "user" ? (
                      <User size={17} />
                    ) : (
                      <Bot size={18} />
                    )}

                  </div>

                  <div className="message-content">

                    <div className="message-name">
                      {message.role === "user"
                        ? "You"
                        : "DocuMed"}
                    </div>

                    <div className="message-text">
                      {message.content}
                    </div>

                    {message.role === "assistant" &&
                      message.sources &&
                      message.sources.length > 0 && (

                        <div className="sources">

                          <div className="sources-title">
                            <BookOpen size={15} />
                            Retrieved sources
                          </div>

                          {message.sources.map(
                            (source, sourceIndex) => (

                              <div
                                className="source"
                                key={sourceIndex}
                              >
                                <FileText size={15} />

                                <span>
                                  {source.source}
                                </span>

                                <span className="page">
                                  Page {source.page}
                                </span>

                                 <span className="distance">
    Distance {source.distance.toFixed(4)}
  </span>
                              </div>

                            )
                          )}

                        </div>

                      )}

                    {message.role === "assistant" && (

                      <button
                        className="copy-button"
                        onClick={() =>
                          copyAnswer(message.content)
                        }
                      >
                        {copied ? (
                          <>
                            <Check size={14} />
                            Copied
                          </>
                        ) : (
                          <>
                            <Clipboard size={14} />
                            Copy
                          </>
                        )}
                      </button>

                    )}

                  </div>

                </div>

              ))}

              {loading && (

                <div className="message-row assistant">

                  <div className="avatar">
                    <Bot size={18} />
                  </div>

                  <div className="message-content">

                    <div className="message-name">
                      DocuMed
                    </div>

                    <div className="typing">
                      <span />
                      <span />
                      <span />
                      <em>Searching medical documents...</em>
                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </section>

        {/* INPUT */}

        <div className="composer-wrapper">

          <div className="composer">

            <textarea
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={(e) => {

                if (
                  e.key === "Enter" &&
                  !e.shiftKey
                ) {
                  e.preventDefault();
                  askQuestion();
                }

              }}
              placeholder="Ask DocuMed about your medical documents..."
              rows={1}
            />

            <button
              className="send-button"
              onClick={() => askQuestion()}
              disabled={!question.trim() || loading}
            >
              <Send size={19} />
            </button>

          </div>

          <p className="disclaimer">
            DocuMed can make mistakes. Always verify important
            medical information with a qualified healthcare professional.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;