# Deployment Guide

## Quick Start

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

### 3. Initialize Database
```bash
python scripts/init_db.py
```

### 4. Run the System
```bash
python main.py
```

## Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop system
docker-compose down
```

## Configuration Checklist

- [ ] OpenAI or Anthropic API key
- [ ] Amazon SP-API credentials
- [ ] eBay API credentials
- [ ] Keepa API key
- [ ] BookScouter API key (for books category)
- [ ] SendGrid API key (for email)
- [ ] Twilio credentials (for SMS)
- [ ] Database connection string
- [ ] Set max purchase limits
- [ ] Configure notification preferences

## Safety Recommendations

1. Start with `auto_purchase: false` - review all purchases manually
2. Set conservative spending limits initially
3. Test with low-value categories first (books, video games)
4. Monitor the first 100 opportunities closely
5. Gradually enable full automation after validation

## Monitoring

- View logs in `logs/` directory
- Check database for metrics
- Set up email/SMS alerts for high-value opportunities
- Monitor daily spend vs profit

## Troubleshooting

**System not finding opportunities:**
- Check API keys are valid
- Verify network connection
- Check marketplace scan intervals

**Purchases failing:**
- Verify payment method configuration
- Check daily spend limits
- Review auto_purchase setting

**Listings not creating:**
- Verify marketplace API credentials
- Check product category mappings
- Review listing content for policy violations

