import { useState } from 'react'

export default function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'guardrail' | 'quarantine'>('overview')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Hero Section */}
      <div className="relative h-[400px] overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgxMDAsIDIwMCwgMjU1LCAwLjEpIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-30" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center px-6">
            <div className="inline-block mb-6">
              <div className="w-20 h-20 mx-auto bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-cyan-500/50">
                <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
            </div>
            <h1 className="text-6xl font-bold text-white mb-4 tracking-tight">
              Awesome Security Engineer
            </h1>
            <p className="text-2xl text-cyan-400 mb-6 font-light">
              Production-Ready Cloud Security Solutions
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              <span className="px-6 py-2 bg-cyan-500/20 border border-cyan-500/50 rounded-full text-cyan-400 backdrop-blur-sm">
                Multi-Cloud
              </span>
              <span className="px-6 py-2 bg-cyan-500/20 border border-cyan-500/50 rounded-full text-cyan-400 backdrop-blur-sm">
                Zero-Trust
              </span>
              <span className="px-6 py-2 bg-cyan-500/20 border border-cyan-500/50 rounded-full text-cyan-400 backdrop-blur-sm">
                Enterprise-Grade
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-6 text-center hover:border-cyan-500/50 transition-all">
            <div className="text-4xl font-bold text-cyan-400 mb-2">29+</div>
            <div className="text-slate-400 text-sm">Production Files</div>
          </div>
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-6 text-center hover:border-cyan-500/50 transition-all">
            <div className="text-4xl font-bold text-cyan-400 mb-2">2</div>
            <div className="text-slate-400 text-sm">Security Engines</div>
          </div>
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-6 text-center hover:border-cyan-500/50 transition-all">
            <div className="text-4xl font-bold text-cyan-400 mb-2">4</div>
            <div className="text-slate-400 text-sm">CI/CD Stages</div>
          </div>
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-6 text-center hover:border-cyan-500/50 transition-all">
            <div className="text-4xl font-bold text-cyan-400 mb-2">100%</div>
            <div className="text-slate-400 text-sm">Test Coverage</div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-8 border-b border-slate-700 overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-6 py-3 font-semibold transition whitespace-nowrap ${
              activeTab === 'overview'
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('guardrail')}
            className={`px-6 py-3 font-semibold transition whitespace-nowrap ${
              activeTab === 'guardrail'
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Cloud Guardrail Engine
          </button>
          <button
            onClick={() => setActiveTab('quarantine')}
            className={`px-6 py-3 font-semibold transition whitespace-nowrap ${
              activeTab === 'quarantine'
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Zero-Trust Quarantine
          </button>
        </div>

        {/* Content Sections */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-8">
              <h2 className="text-3xl font-bold text-white mb-4">Why This Matters</h2>
              <p className="text-slate-300 text-lg mb-6 leading-relaxed">
                In today's multi-cloud environment, security breaches cost an average of <span className="text-cyan-400 font-semibold">$4.45M per incident</span>. 
                These production-ready engines provide automated, instant response to security threats across 
                AWS and Azure, reducing mean-time-to-remediation from hours to seconds.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-slate-900/50 rounded-lg p-6 border border-slate-700 hover:border-cyan-500/50 transition-all">
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3 flex items-center gap-2">
                    <span className="text-2xl">🛡️</span> Shift-Left Security
                  </h3>
                  <p className="text-slate-400">
                    Catch security violations before deployment with policy-as-code enforcement
                  </p>
                </div>
                <div className="bg-slate-900/50 rounded-lg p-6 border border-slate-700 hover:border-cyan-500/50 transition-all">
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3 flex items-center gap-2">
                    <span className="text-2xl">⚡</span> Instant Response
                  </h3>
                  <p className="text-slate-400">
                    Revoke compromised sessions across clouds in milliseconds, not hours
                  </p>
                </div>
                <div className="bg-slate-900/50 rounded-lg p-6 border border-slate-700 hover:border-cyan-500/50 transition-all">
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3 flex items-center gap-2">
                    <span className="text-2xl">🔄</span> Multi-Cloud
                  </h3>
                  <p className="text-slate-400">
                    Unified security posture across AWS and Azure with consistent policies
                  </p>
                </div>
                <div className="bg-slate-900/50 rounded-lg p-6 border border-slate-700 hover:border-cyan-500/50 transition-all">
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3 flex items-center gap-2">
                    <span className="text-2xl">🚀</span> Production-Ready
                  </h3>
                  <p className="text-slate-400">
                    Kubernetes-native, CI/CD integrated, fully tested and documented
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-8">
              <h2 className="text-3xl font-bold text-white mb-6">Architecture Overview</h2>
              <div className="bg-slate-900 rounded-lg p-6 font-mono text-sm text-slate-300 overflow-x-auto">
                <pre className="whitespace-pre">{`┌─────────────────────────────────────────────────────────────┐
│                    Threat Detection Layer                    │
│  (SIEM, GuardDuty, Entra ID Risk, Custom Alerts)           │
└────────────────────┬────────────────────────────────────────┘
                     │ Webhook (HTTPS)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Zero-Trust Quarantine Engine                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Webhook Ingestion (Python)                  │  │
│  │  - Token Authentication                              │  │
│  │  - Request Validation (Pydantic)                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Provider Orchestration                              │  │
│  │  - AWS STS Token Revocation                          │  │
│  │  - Azure Entra ID Session Revocation                 │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌───────────────┐        ┌───────────────┐
│  AWS Cloud    │        │  Azure Cloud  │
│  - IAM        │        │  - Entra ID   │
│  - STS        │        │  - Graph API  │
└───────────────┘        └───────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Cloud Guardrail Engine                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Terraform Plan JSON Input                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OPA Rego Policy Engine (Go)                         │  │
│  │  - AWS S3 Encryption Policy                          │  │
│  │  - Azure HTTPS Enforcement Policy                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Compliance Report (JSON)                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘`}</pre>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'guardrail' && (
          <div className="space-y-8">
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-8">
              <h2 className="text-3xl font-bold text-white mb-4">Cloud Guardrail Engine</h2>
              <p className="text-slate-300 text-lg mb-6 leading-relaxed">
                Go-based CLI tool that evaluates Terraform plans against OPA Rego policies, 
                enforcing security standards before infrastructure deployment.
              </p>
              
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div>
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3">Key Features</h3>
                  <ul className="space-y-2 text-slate-300">
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>OPA Rego policy evaluation</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>Multi-cloud support (AWS & Azure)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>JSON-formatted compliance reports</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>CI/CD integration ready</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>Unit tested policies</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3">Tech Stack</h3>
                  <ul className="space-y-2 text-slate-300">
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Go 1.22</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Open Policy Agent (OPA)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Rego Policy Language</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Terraform Plan JSON</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>GitHub Actions CI/CD</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div className="bg-slate-900 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-cyan-400 mb-3">Example Output</h3>
                <pre className="text-sm text-slate-300 overflow-x-auto">{`{
  "compliant": false,
  "violations": [
    "[aws] AWS S3 bucket 'unencrypted_bucket' must have 
     server-side encryption enabled.",
    "[azure] Azure Storage Account 'insecure_storage' must 
     enforce HTTPS traffic only."
  ]
}`}</pre>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'quarantine' && (
          <div className="space-y-8">
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-lg p-8">
              <h2 className="text-3xl font-bold text-white mb-4">Zero-Trust Quarantine Engine</h2>
              <p className="text-slate-300 text-lg mb-6 leading-relaxed">
                Event-driven FastAPI daemon that instantly revokes compromised identity sessions 
                across AWS and Azure in response to security alerts.
              </p>
              
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div>
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3">Key Features</h3>
                  <ul className="space-y-2 text-slate-300">
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>Instant cross-cloud session revocation</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>AWS STS token issue time validation</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>Azure Entra ID refresh token revocation</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>Kubernetes-native deployment</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">✓</span>
                      <span>Webhook-based event ingestion</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-cyan-400 mb-3">Tech Stack</h3>
                  <ul className="space-y-2 text-slate-300">
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Python 3.11 + FastAPI</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>AWS SDK (boto3)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Azure SDK + Microsoft Graph</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Docker + Kubernetes</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-cyan-400 mt-1">•</span>
                      <span>Pydantic validation</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div className="bg-slate-900 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-cyan-400 mb-3">API Example</h3>
                <pre className="text-sm text-slate-300 overflow-x-auto">{`POST /api/v1/quarantine
{
  "user_principal_name": "compromised.user@company.com",
  "aws_iam_role_name": "Developer-PowerUser-Role",
  "reason": "Impossible travel detected",
  "risk_score": 0.95
}

Response:
{
  "status": "completed",
  "user_principal_name": "compromised.user@company.com",
  "actions_taken": {
    "azure_entra": true,
    "aws_sts": true
  }
}`}</pre>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 text-center text-slate-400 pb-8">
          <p className="mb-2 text-lg">Built with enterprise security best practices</p>
          <p className="text-sm">
            Production-ready • Fully tested • Kubernetes-native • CI/CD integrated
          </p>
        </div>
      </div>
    </div>
  )
}
