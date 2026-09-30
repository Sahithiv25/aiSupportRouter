"use client";

import { useState } from "react";

type Decision = {
  intent: string;
  priority: string;
  amount: number | null;
  risk_level: string;
  requires_human_approval: boolean;
  recommended_action: string;
  reasoning: string;
};

type ApiResponse = {
  decision: Decision;
  tool_result: string;
};

export default function Home() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function analyzeRequest() {
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-blue-50 text-blue-950">
      <div className="mx-auto max-w-4xl px-6 py-14">

        <h1 className="text-4xl font-bold text-blue-900">
          AI Support Request Router
        </h1>

        <p className="mt-3 mb-8 text-lg text-blue-700">
          Analyze customer requests and route them to the appropriate business action.
        </p>

        <div className="rounded-2xl border-2 border-blue-200 bg-white p-6 shadow-md">
          <label className="mb-3 block font-semibold text-blue-900">
            Customer Request
          </label>

          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Example: I was charged twice for my order. Each charge was $84 and I want a refund."
            className="
              min-h-40
              w-full
              rounded-xl
              border-2
              border-blue-200
              bg-white
              p-4
              text-blue-950
              placeholder:text-blue-300
              outline-none
              focus:border-blue-500
              focus:ring-2
              focus:ring-blue-200
            "
          />

          <button
            onClick={analyzeRequest}
            disabled={loading}
            className="
              mt-5
              rounded-lg
              bg-blue-600
              px-6
              py-3
              font-semibold
              text-white
              hover:bg-blue-700
              disabled:opacity-50
            "
          >
            {loading ? "Analyzing..." : "Analyze Request"}
          </button>
        </div>

        {result && (
          <div className="mt-8 space-y-6">

            <div className="rounded-2xl border-2 border-blue-200 bg-white p-6 shadow-md">
              <h2 className="mb-6 text-2xl font-bold text-blue-900">
                AI Decision
              </h2>

              <div className="grid gap-4 sm:grid-cols-2">
                <ResultItem label="Intent" value={result.decision.intent} />
                <ResultItem label="Priority" value={result.decision.priority} />
                <ResultItem
                  label="Amount"
                  value={
                    result.decision.amount !== null
                      ? `$${result.decision.amount}`
                      : "N/A"
                  }
                />
                <ResultItem label="Risk Level" value={result.decision.risk_level} />
                <ResultItem
                  label="Human Approval"
                  value={
                    result.decision.requires_human_approval
                      ? "Required"
                      : "Not Required"
                  }
                />
                <ResultItem
                  label="Recommended Action"
                  value={result.decision.recommended_action}
                />
              </div>

              <div className="mt-6 rounded-xl border border-blue-200 bg-blue-50 p-4">
                <p className="text-sm font-semibold text-blue-700">
                  Reasoning
                </p>

                <p className="mt-1 text-blue-950">
                  {result.decision.reasoning}
                </p>
              </div>
            </div>

            <div className="rounded-2xl border-2 border-blue-300 bg-blue-100 p-6 shadow-md">
              <h2 className="text-xl font-bold text-blue-900">
                Tool Execution
              </h2>

              <p className="mt-2 font-medium text-blue-950">
                {result.tool_result}
              </p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

function ResultItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
      <p className="text-xs font-bold uppercase tracking-wide text-blue-600">
        {label}
      </p>

      <p className="mt-1 text-base font-semibold text-blue-950">
        {value}
      </p>
    </div>
  );
}