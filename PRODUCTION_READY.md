# 🚀 Production Deployment Guide

## Overview

This guide covers deploying the AI Arbitrage Platform to production with best practices for security, scalability, and reliability.

## Prerequisites

- Docker & Docker Compose installed
- Domain name configured (for SSL)
- Environment variables configured
- API keys obtained

## Quick Start (Production)

### 1. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your production values
nano .env
```

**Critical Environment Variables:**
- `ENVIRONMENT=production`
- `SECRET_KEY` - Generate a secure random key (min 32 chars)
- `DB_PASSWORD` - Strong database password
- `REDIS_PASSWORD` - Strong Redis password
- `GOOGLE_API_KEY` - Your Google Gemini API key
- All marketplace API keys

### 2. Start Production Stack

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check service health
docker-compose -f docker-compose.prod.yml ps
```

### 3. Verify Deployment

```bash
# Check API health
curl http://localhost/health

# Check database connectivity
docker-compose -f docker-compose.prod.yml exec postgres pg_isready

# Check Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

## Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Port 80/443)                   │
│              Reverse Proxy & Load Balancer               │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌───▼─────────┐ ┌──▼────────────┐
│  Python API    │ │   Main App   │ │ Celery Workers│
│   (FastAPI)    │ │  (Scanner)   │ │   (Tasks)     │
│   Port 8000    │ │              │ │               │
└────────────────┘ └──────────────┘ └───────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌───▼─────┐ ┌──────▼──────┐
│   PostgreSQL   │ │  Redis   │ │   MongoDB   │
│  (Transact.)   │ │ (Cache)  │ │  (Scrapes)  │
└────────────────┘ └──────────┘ └─────────────┘
```

## Production Features Enabled

### ✅ Security
- Security headers (X-Frame-Options, CSP, etc.)
- CORS properly configured
- Rate limiting (100 req/min default)
- SQL injection protection
- Input validation with Pydantic
- Secrets managed via environment variables

### ✅ Reliability
- Health checks for all services
- Automatic restart on failure
- Database connection pooling
- Graceful shutdown handling
- Resource limits configured

### ✅ Monitoring
- Structured logging
- Health check endpoints
- Error tracking ready (Sentry)
- Prometheus metrics ready

### ✅ Performance
- Redis caching enabled
- Database query optimization
- Connection pooling
- Multi-worker deployment
- Resource limits configured

## API Endpoints

### Health & Status
- `GET /health` - Service health check
- `GET /` - API information

### Opportunities
- `GET /api/opportunities` - List opportunities
  - Query params: `category`, `status`, `limit`
  - Rate limit: 30/minute

### Statistics
- `GET /api/stats/daily` - Daily statistics
- `GET /api/stats/performance` - Overall performance
  - Rate limit: 30/minute

### Actions
- `POST /api/purchase/approve` - Approve purchase
  - Rate limit: 10/minute
- `POST /api/scan/trigger` - Trigger marketplace scan
  - Rate limit: 5/minute
- `GET /api/scan/status` - Get scan status

## Scaling

### Horizontal Scaling

Scale specific services:
```bash
# Scale API workers
docker-compose -f docker-compose.prod.yml up -d --scale python-api=4

# Scale Celery workers
docker-compose -f docker-compose.prod.yml up -d --scale celery_worker=6
```

### Resource Limits

Default limits per service:
- **Python API**: 2 CPU, 2GB RAM
- **PostgreSQL**: 1 CPU, 1GB RAM
- **Redis**: 0.5 CPU, 2GB RAM
- **MongoDB**: 1 CPU, 2GB RAM

Adjust in `docker-compose.prod.yml` under `deploy.resources`.

## Monitoring

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f python-api

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 python-api
```

### Check Resource Usage
```bash
docker stats
```

### Database Monitoring
```bash
# PostgreSQL stats
docker-compose -f docker-compose.prod.yml exec postgres psql -U arbitrage_user -d arbitrage_db -c "SELECT * FROM pg_stat_activity;"

# Redis stats
docker-compose -f docker-compose.prod.yml exec redis redis-cli INFO stats
```

## Backup & Recovery

### Database Backup
```bash
# Backup PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U arbitrage_user arbitrage_db > backup_$(date +%Y%m%d).sql

# Restore PostgreSQL
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U arbitrage_user arbitrage_db < backup.sql

# Backup MongoDB
docker-compose -f docker-compose.prod.yml exec mongodb mongodump --out /backup

# Backup Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli SAVE
```

### Data Volumes
```bash
# List volumes
docker volume ls

# Backup volume
docker run --rm -v arbitrage_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data.tar.gz /data
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Recommended)

1. Install certbot:
```bash
apt-get install certbot python3-certbot-nginx
```

2. Generate certificate:
```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. Update nginx configuration in `nginx/nginx.conf`

4. Restart nginx:
```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

## Security Checklist

- [ ] Change all default passwords in `.env`
- [ ] Generate strong `SECRET_KEY` and `API_KEY`
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up VPC/private network (cloud)
- [ ] Enable database encryption at rest
- [ ] Configure backup strategy
- [ ] Set up monitoring alerts
- [ ] Review and restrict CORS origins
- [ ] Enable audit logging
- [ ] Set up intrusion detection
- [ ] Configure rate limiting
- [ ] Regular security updates

## Troubleshooting

### API Not Responding
```bash
# Check if container is running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs python-api

# Restart service
docker-compose -f docker-compose.prod.yml restart python-api
```

### Database Connection Issues
```bash
# Check PostgreSQL is healthy
docker-compose -f docker-compose.prod.yml exec postgres pg_isready

# Check connections
docker-compose -f docker-compose.prod.yml exec postgres psql -U arbitrage_user -c "SELECT count(*) FROM pg_stat_activity;"
```

### High Memory Usage
```bash
# Check resource usage
docker stats

# Restart memory-intensive services
docker-compose -f docker-compose.prod.yml restart celery_worker
```

### Slow Performance
1. Check Redis cache is working
2. Review database query performance
3. Check network latency
4. Scale worker instances
5. Optimize Celery task concurrency

## Maintenance

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Verify health
curl http://localhost/health
```

### Database Migrations
```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec python-api alembic upgrade head
```

### Clean Up Old Data
```bash
# Connect to database
docker-compose -f docker-compose.prod.yml exec postgres psql -U arbitrage_user arbitrage_db

# Run cleanup queries
DELETE FROM opportunities WHERE created_at < NOW() - INTERVAL '90 days';
```

## Performance Tuning

### PostgreSQL
```sql
-- Increase connection pool
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
```

### Redis
```bash
# Increase memory limit
docker-compose -f docker-compose.prod.yml exec redis redis-cli CONFIG SET maxmemory 4gb
```

### Nginx
Edit `nginx/nginx.conf`:
- Increase worker_processes
- Tune worker_connections
- Enable gzip compression
- Configure caching

## Support

- **Documentation**: See `/docs` directory
- **Logs**: `logs/arbitrage_*.log`
- **Health Check**: `curl http://localhost/health`
- **API Docs**: `http://localhost/docs` (dev only)

## Production Checklist

- [ ] Environment variables configured
- [ ] Database backed up
- [ ] SSL certificates installed
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Alerts configured
- [ ] Rate limiting tested
- [ ] Health checks verified
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] Team trained

---

**🎯 Your AI Arbitrage Platform is now production-ready!**

For advanced deployment options (Kubernetes, cloud platforms), see:
- `RAILWAY_DEPLOYMENT_GUIDE.md`
- `kubernetes/deployment.yaml`
- `PRODUCTION_DEPLOYMENT.md`
