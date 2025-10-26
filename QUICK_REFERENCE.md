# 🚀 **QUICK REFERENCE - AI Arbitrage System**

## ⚡ **Quick Commands**

### **Check API Configuration**
```bash
./check_api_usage.sh
```

### **Start System**
```bash
# Standalone
python main.py

# Docker (Full Dashboard)
docker-compose up -d
```

### **Stop System**
```bash
# Kill standalone
pkill -f "python.*main.py"

# Stop Docker
docker-compose down
```

### **View Logs**
```bash
# Latest log file
tail -f logs/arbitrage_*.log

# Check for Gemini
tail -f logs/arbitrage_*.log | grep "Gemini"
```

---

## 🔑 **API Keys**

### **Google Gemini (FREE)**
- **Get Key**: https://makersuite.google.com/app/apikey
- **Free Tier**: 1,500 requests/day
- **Cost**: $0/month ✅

### **Edit .env File**
```bash
# TextEdit (Easy)
open -a TextEdit .env

# Terminal
nano .env
```

---

## 📊 **Monitor Usage**

### **Google Gemini Dashboard**
https://makersuite.google.com/app/apikey

### **OpenAI Dashboard (Past Charges)**
https://platform.openai.com/account/usage

---

## 🛑 **Emergency Stop**

If you see unexpected charges:

```bash
# Stop all processes
pkill -f "python.*main.py"
docker-compose down

# Check what's running
./check_api_usage.sh

# Review .env file
cat .env | grep API
```

---

## ✅ **Health Check**

System is healthy when you see:

```
✅ CORRECT: Using Google Gemini (FREE)
✅ Google API key configured
✅ No arbitrage processes running (or running with Gemini)
```

---

## 📖 **Documentation**

- **API_CHARGES_FIXED.md** - Complete summary
- **STOP_OPENAI_CHARGES.md** - Detailed guide
- **WHATS_HAPPENING_NOW.md** - Current status
- **check_api_usage.sh** - Health check script

---

## 💰 **Cost Savings**

| Period | OpenAI GPT-4 | Google Gemini |
|--------|--------------|---------------|
| Daily | $1.50-5.00 | **$0** ✅ |
| Monthly | $50-150 | **$0** ✅ |
| Yearly | $600-1,800 | **$0** ✅ |

---

## 🎯 **Setup Checklist**

- [ ] Get Google Gemini API key
- [ ] Add to .env file
- [ ] Run `./check_api_usage.sh`
- [ ] Verify shows "Using Google Gemini"
- [ ] Start system
- [ ] Check logs for "✅ AI Engine initialized with Google Gemini"
- [ ] Start making money! 💰

---

**Last Updated**: October 26, 2025  
**Status**: ✅ Ready with FREE Google Gemini

