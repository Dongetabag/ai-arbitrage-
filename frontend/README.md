# AI Arbitrage Dashboard - Frontend

Beautiful React/Next.js dashboard for the AI Arbitrage System.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open browser
open http://localhost:3000
```

## Features

- 📊 Real-time opportunity feed
- 📈 Interactive charts (Recharts)
- 🔴 Live WebSocket updates
- ✅ One-click purchase approval
- 📱 Mobile-responsive
- 🎨 Modern dark theme
- ⚡ Fast performance (Next.js)

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Tech Stack

- **Framework:** Next.js 14
- **UI:** React 18
- **Styling:** TailwindCSS
- **Charts:** Recharts
- **Icons:** React Icons
- **Real-time:** Socket.IO
- **HTTP:** Axios

## Pages

- `/` - Main dashboard
- `/analytics` - Advanced analytics
- `/opportunities` - Opportunity list
- `/settings` - Configuration

## Connecting to Backend

The dashboard connects to your Python FastAPI backend running on port 8000.

Make sure the backend is running:
```bash
cd ..
source venv/bin/activate
python main.py
```

Then start the frontend:
```bash
npm run dev
```

