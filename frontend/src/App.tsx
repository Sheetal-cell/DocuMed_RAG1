import { useState } from "react";
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

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data: ApiResponse = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      console.error(err);
      setError(
        "Could not connect to DocuMed. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">✚</div>

          <div>
            <h1>DocuMed</h1>
            <p>Medical Knowledge Assistant</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          RAG Online
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="badge">AI-POWERED MEDICAL DOCUMENT SEARCH</div>

          <h2>
            Ask questions.
            <br />
            <span>Get document-grounded answers.</span>
          </h2>

          <p>
            DocuMed retrieves relevant information from your medical
            documents and uses your fine-tuned language model to generate
            grounded answers.
          </p>
        </section>

        <section className="chat-card">
          <div className="input-area">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask something about the medical documents..."
              rows={4}
            />

            <button onClick={askQuestion} disabled={loading}>
              {loading ? "Thinking..." : "Ask DocuMed →"}
            </button>
          </div>

          {error && <div className="error">{error}</div>}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              Searching documents and generating answer...
            </div>
          )}

          {answer && !loading && (
            <div className="answer-section">
              <div className="answer-header">
                <span>DOCUMED ANSWER</span>
              </div>

              <div className="answer">
                {answer}
              </div>

              {sources.length > 0 && (
                <div className="sources">
                  <h3>Retrieved Sources</h3>

                  {sources.map((source, index) => (
                    <div className="source" key={index}>
                      <strong>{source.source}</strong>

                      <span>
                        Page {source.page}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </section>

        <section className="features">
          <div>
            <div className="feature-icon">🔎</div>
            <h3>Retrieval</h3>
            <p>
              Searches your document knowledge base for relevant information.
            </p>
          </div>

          <div>
            <div className="feature-icon">🧠</div>
            <h3>Fine-tuned LLM</h3>
            <p>
              Uses your Qwen model with the DocuMed LoRA adapter.
            </p>
          </div>

          <div>
            <div className="feature-icon">📚</div>
            <h3>Grounded Answers</h3>
            <p>
              Answers are generated using retrieved document context.
            </p>
          </div>
        </section>
      </main>

      <footer>
        <p>
          DocuMed • Retrieval-Augmented Generation System
        </p>

        <p>
          For educational and informational purposes only.
        </p>
      </footer>
    </div>
  );
}

export default App;