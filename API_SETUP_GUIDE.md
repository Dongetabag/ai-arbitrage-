# API Setup Guide

## Priority APIs (Set up first for maximum profit)

### 1. Keepa API - Amazon Price Tracking ⭐⭐⭐
**Cost:** €19-195/month  
**Purpose:** Real-time Amazon pricing, sales rank, Buy Box history

**Setup:**
1. Go to https://keepa.com/#!api
2. Create account and subscribe to API plan
3. Copy API key to `.env` as `KEEPA_API_KEY`

**Why it's critical:** Amazon is your primary selling platform. Keepa provides accurate pricing data to calculate profits.

---

### 2. BookScouter API - Textbook Buyback ⭐⭐⭐
**Cost:** FREE  
**Purpose:** Aggregates 30+ book buyback vendors

**Setup:**
1. Go to https://bookscouter.com/api
2. Register for free API key
3. Add to `.env` as `BOOKSCOUTER_API_KEY`

**Why it's critical:** Books have 47.3% average margin - highest profit category.

---

### 3. BuyBotPro API - Restriction Checker ⭐⭐⭐
**Cost:** $40-130/month  
**Purpose:** Check if ASINs are restricted/gated on Amazon

**Setup:**
1. Go to https://www.buybotpro.com
2. Subscribe to API plan
3. Add key to `.env` as `BUYBOT_PRO_API_KEY`

**Why it's critical:** Prevents buying items you can't sell on Amazon (restricted brands/categories).

---

## Secondary APIs (High-value categories)

### 4. TCGPlayer API - Trading Cards ⭐⭐
**Cost:** Free with approval  
**Purpose:** Trading card pricing (Pokemon, Magic, Yu-Gi-Oh)

**Setup:**
1. Apply at https://www.tcgplayer.com/developers
2. Wait for approval (3-5 days)
3. Add credentials to `.env`

**Usage:** 36.8% average margin category

---

### 5. PriceCharting API - Video Games ⭐⭐
**Cost:** $5-15/month  
**Purpose:** Video game, console, and collectibles pricing

**Setup:**
1. Go to https://www.pricecharting.com/api
2. Subscribe to plan
3. Add key as `PRICECHARTING_API_KEY`

**Usage:** 34.2% average margin category

---

### 6. Reverb API - Musical Instruments ⭐⭐
**Cost:** Free  
**Purpose:** Musical instrument marketplace and pricing

**Setup:**
1. Go to https://reverb.com/api
2. Create developer account
3. Generate OAuth token
4. Add as `REVERB_API_KEY`

**Usage:** 31.7% average margin category

---

### 7. BrickLink API - LEGO Pricing ⭐
**Cost:** Free  
**Purpose:** LEGO set pricing and availability

**Setup:**
1. Go to https://www.bricklink.com/v3/api.page
2. Create consumer key
3. Requires OAuth 1.0 setup
4. Add credentials to `.env`

**Usage:** 29.4% average margin category

---

## Marketplace APIs

### Amazon SP-API ⭐⭐⭐
**Required for:** Selling on Amazon FBA

**Setup:**
1. Register as Amazon seller (Professional account required)
2. Go to Seller Central > Apps & Services > Develop Apps
3. Create developer profile
4. Register application
5. Generate LWA credentials and refresh token
6. Add to `.env`:
   ```
   AMAZON_SP_API_KEY=your_lwa_app_id
   AMAZON_SP_API_SECRET=your_lwa_client_secret
   AMAZON_SP_API_REFRESH_TOKEN=your_refresh_token
   AMAZON_SELLER_ID=your_seller_id
   ```

**Docs:** https://developer-docs.amazon.com/sp-api/

---

### eBay API ⭐⭐
**Required for:** Selling on eBay

**Setup:**
1. Create eBay developer account at https://developer.ebay.com
2. Create application (Production keys)
3. Generate User Token
4. Add to `.env`:
   ```
   EBAY_APP_ID=your_app_id
   EBAY_CERT_ID=your_cert_id
   EBAY_DEV_ID=your_dev_id
   EBAY_USER_TOKEN=your_user_token
   ```

**Docs:** https://developer.ebay.com/api-docs/

---

### Facebook Graph API ⭐
**Optional:** Automated Facebook Marketplace posting

**Setup:**
1. Create Facebook Developer account
2. Create app with marketplace permissions
3. Generate long-lived access token
4. Add as `FACEBOOK_ACCESS_TOKEN`

**Note:** Facebook Marketplace has limited automation support. Manual listing may be required.

---

## Communication APIs

### Twilio - SMS/Phone ⭐⭐
**Cost:** Pay-as-you-go ($0.0075/SMS)  
**Purpose:** Contact sellers via SMS

**Setup:**
1. Sign up at https://www.twilio.com
2. Get phone number
3. Copy credentials:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=your_number
   ```

---

### SendGrid - Email ⭐⭐
**Cost:** Free tier (100 emails/day)  
**Purpose:** Email communication and notifications

**Setup:**
1. Sign up at https://sendgrid.com
2. Create API key
3. Add as `SENDGRID_API_KEY`

---

## Optional Premium Tools

### Tactical Arbitrage - Automated Scanning
**Cost:** $89/month  
**Purpose:** Scans 1,400+ sites overnight

**Setup:**
1. Subscribe at https://tacticalarbitrage.com
2. Get API credentials
3. Add as `TACTICAL_ARBITRAGE_API_KEY`

**Note:** Can find 100+ opportunities per day automatically

---

### Authentication Services

#### Entrupy - Luxury Goods Authentication
**Cost:** $300/year + $6-30 per scan  
**Purpose:** AI authentication for luxury items

**Setup:** Contact Entrupy for business account

#### LegitCheck - Sneaker Authentication
**Cost:** $1-3 per check  
**Purpose:** Verify authentic sneakers

---

## Testing Your Setup

Run this command to test all API connections:

```bash
python scripts/test_apis.py
```

It will check each API and report which ones are working.

## Cost Summary for Initial Setup

**Minimum (Books only):**
- BookScouter: FREE
- Keepa: €19/month (~$20)
- SendGrid: FREE
- **Total: ~$20/month**

**Recommended (Top 5 categories):**
- Keepa: €39/month (~$42)
- BuyBotPro: $40/month
- BookScouter: FREE
- TCGPlayer: FREE
- PriceCharting: $15/month
- SendGrid: FREE
- Twilio: ~$10/month
- **Total: ~$107/month**

**Full System (All 10 categories):**
- All above
- Reverb API: FREE
- BrickLink: FREE
- Tactical Arbitrage: $89/month
- **Total: ~$196/month**

**Expected ROI:** With proper execution, should generate $2,000-5,000/month profit, making API costs negligible.

