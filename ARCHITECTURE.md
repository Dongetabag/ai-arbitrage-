# System Architecture

## Overview

The AI Arbitrage System is a multi-module autonomous platform designed to find, purchase, and resell products for profit with minimal human intervention.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAIN ORCHESTRATOR                            │
│                           (main.py)                                  │
└────────────┬─────────────────────────────────────────────┬──────────┘
             │                                             │
    ┌────────▼─────────┐                        ┌─────────▼──────────┐
    │  AI REASONING    │◄───────────────────────┤   DATABASE         │
    │    ENGINE        │                        │   MANAGER          │
    │                  │                        │                    │
    │ - GPT-4/Claude   │                        │ - PostgreSQL       │
    │ - Decision Logic │                        │ - SQLAlchemy ORM   │
    │ - Risk Analysis  │                        │ - Metrics          │
    └────────┬─────────┘                        └─────────▲──────────┘
             │                                             │
    ┌────────┴──────────────────────────────────────────┬─┴──────────┐
    │                                                   │            │
┌───▼───────────┐  ┌──────────────┐  ┌───────────────┐  │  ┌─────────▼────┐
│   MARKET      │  │ COMMUNICATION│  │   PURCHASE    │  │  │   LISTING    │
│   MONITORING  │  │              │  │   ENGINE      │  │  │   MANAGER    │
│               │  ├──────────────┤  │               │  │  │              │
│ - Scrapers    │  │ Negotiation  │  │ - Automation  │  │  │ - Amazon FBA │
│ - API Polling │  │ Manager      │  │ - Payments    │  │  │ - eBay       │
│ - Validation  │  │              │  │ - Receipts    │  │  │ - Optimization│
└───┬───────────┘  └──────┬───────┘  └───────────────┘  │  └──────────────┘
    │                     │                              │
    │              ┌──────▼──────┐              ┌────────▼──────────┐
    │              │   SELLER    │              │   CUSTOMER        │
    │              │COMMUNICATOR │              │   SUPPORT AI      │
    │              │             │              │                   │
    │              │ - Twilio    │              │ - Auto-response   │
    │              │ - SendGrid  │              │ - Escalation      │
    │              │ - Marketplace│              │ - Ticket Mgmt     │
    │              └─────────────┘              └───────────────────┘
    │
┌───▼────────────────────────────────────────────────────────────────┐
│                     API INTEGRATIONS                                │
├────────────┬──────────┬───────────┬──────────┬──────────┬──────────┤
│  Keepa    │BookScouter│TCGPlayer  │ Reverb  │BuyBotPro │ Tactical │
│  Amazon   │  Books    │  Cards    │ Music   │Restrict  │Arbitrage │
└───────────┴──────────┴───────────┴──────────┴──────────┴──────────┘
```

## Data Flow

### 1. Opportunity Discovery Flow
```
Marketplace Scan → Raw Listings
                        ↓
              Filter & Deduplicate
                        ↓
              Extract Product ID (ISBN/UPC/ASIN)
                        ↓
              Validate Pricing (API Call)
                        ↓
              Calculate Profit & Fees
                        ↓
              Save to Database
                        ↓
              AI Analysis
                        ↓
              Decision: Purchase/Negotiate/Skip
```

### 2. Purchase Flow
```
AI Decision: PURCHASE
         ↓
Check Safety Limits
         ↓
    Approved?
    ↙      ↘
  NO       YES
   ↓        ↓
Skip   Contact Seller
         ↓
   Negotiate (if needed)
         ↓
    Process Payment
         ↓
   Confirm Purchase
         ↓
   Update Database
         ↓
   Create Listing
```

### 3. Listing Flow
```
Purchase Confirmed
         ↓
   AI Generate Listing
   (Title, Description, Bullets)
         ↓
   Calculate List Price
   (Cost + Margin + Fees)
         ↓
   Choose Platform
   (Amazon FBA priority)
         ↓
   Create Listing via API
         ↓
   Monitor Performance
         ↓
   Adjust Price if needed
```

### 4. Support Flow
```
Customer Message Received
         ↓
    Categorize Inquiry
    (Shipping/Return/Question)
         ↓
   Check for Escalation Keywords
         ↓
   Escalate? → YES → Human Review
         ↓
        NO
         ↓
   AI Generate Response
         ↓
   Confidence > 80%?
    ↙            ↘
   NO            YES
    ↓             ↓
  Review    Auto-Send
```

## Technology Stack

### Backend
- **Python 3.11** - Core language
- **SQLAlchemy** - ORM for database
- **PostgreSQL** - Primary database
- **Redis** - Caching and queues
- **Celery** - Async task processing

### AI/ML
- **OpenAI GPT-4** - Primary reasoning
- **Anthropic Claude** - Alternative AI
- **LangChain** - AI orchestration

### Web Scraping
- **Selenium** - Dynamic content scraping
- **BeautifulSoup** - HTML parsing
- **Scrapy** - Large-scale scraping
- **Playwright** - Modern web automation

### APIs & Integrations
- **Keepa API** - Amazon pricing
- **Amazon SP-API** - Amazon selling
- **eBay SDK** - eBay operations
- **Twilio** - SMS communication
- **SendGrid** - Email delivery
- **Stripe** - Payment processing

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD (optional)

## Security Considerations

### API Key Management
- All keys stored in environment variables
- Never committed to git
- Rotated regularly

### Payment Security
- Stripe for secure transactions
- PCI compliance through third parties
- Transaction logging and auditing

### Data Privacy
- Customer data encrypted at rest
- GDPR/CCPA compliant data handling
- Automatic data retention policies

## Scalability

### Horizontal Scaling
- Multiple scanner instances
- Distributed task queue (Celery)
- Load-balanced web scrapers

### Vertical Scaling
- Database optimization (indexes, partitioning)
- Redis caching for API responses
- Async I/O for concurrent operations

### Cost Optimization
- API call caching
- Rate limiting
- Batch operations where possible

## Monitoring & Observability

### Logging
- **Loguru** - Structured logging
- **Log Levels:** DEBUG, INFO, WARNING, ERROR
- **Log Rotation:** Daily, 30-day retention

### Metrics
- Prometheus metrics export
- System performance tracking
- Business KPIs dashboard

### Error Tracking
- **Sentry** - Error monitoring
- Automatic alert on critical errors
- Stack traces and context

### Alerting
- Email notifications (SendGrid)
- SMS alerts (Twilio)
- Telegram bot integration (optional)

## Module Responsibilities

### Core Module (`core/`)
- AI reasoning and decision making
- Profit calculation logic
- Risk assessment algorithms

### Monitoring Module (`monitoring/`)
- Marketplace scanners
- Price validators
- Category keyword management

### Communication Module (`communication/`)
- Seller messaging
- Negotiation management
- Multi-channel delivery

### Purchasing Module (`purchasing/`)
- Transaction execution
- Payment processing
- Receipt management

### Selling Module (`selling/`)
- Listing creation and optimization
- Marketplace integration
- Price management

### Support Module (`support/`)
- AI customer support
- Ticket management
- Response generation

### Database Module (`database/`)
- ORM models
- Database manager
- Query optimization

### Integrations Module (`integrations/`)
- External API wrappers
- Rate limiting
- Error handling

## Future Enhancements

### Phase 2
- [ ] Machine learning for price prediction
- [ ] Image recognition for product identification
- [ ] Voice-based negotiation (Twilio Voice)
- [ ] Mobile app for manual approvals

### Phase 3
- [ ] Multi-user support
- [ ] White-label reseller platform
- [ ] Advanced analytics dashboard
- [ ] Automated accounting integration

### Phase 4
- [ ] International marketplace support
- [ ] Cryptocurrency payment options
- [ ] Blockchain-based authentication
- [ ] API marketplace for third-party developers

