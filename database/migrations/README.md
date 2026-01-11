# Alembic Database Migrations

This directory contains database migration scripts managed by Alembic.

## Setup

Alembic is already configured in `requirements.txt`. The configuration is in `alembic.ini`.

## Common Commands

### Initialize Alembic (Already done)
```bash
alembic init alembic
```

### Create a new migration
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Create empty migration
alembic revision -m "description of changes"
```

### Apply migrations
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Upgrade one step
alembic upgrade +1
```

### Rollback migrations
```bash
# Downgrade one step
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Rollback all
alembic downgrade base
```

### View migration history
```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic heads
```

## Production Usage

### In Docker Container
```bash
# Apply migrations on container start
docker-compose exec python-api alembic upgrade head

# Create migration
docker-compose exec python-api alembic revision --autogenerate -m "add new field"
```

### With CI/CD
Add to your deployment pipeline:
```bash
# Before starting the application
alembic upgrade head
```

## Migration Best Practices

1. **Always review auto-generated migrations** - Alembic may not catch all changes correctly
2. **Test migrations** - Run upgrade and downgrade in development first
3. **Backup database** - Before running migrations in production
4. **Use transactions** - Migrations should be atomic
5. **Version control** - Commit migration files to git
6. **Data migrations** - Be careful with data transformations
7. **Rollback plan** - Always have a rollback strategy

## Initial Schema

The initial database schema is in `database/init.sql`. This creates all tables on first deployment.

For ongoing changes, use Alembic migrations.

## Example Migration

```python
"""add user preferences table

Revision ID: 001
Create Date: 2024-01-11
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('preferences', sa.JSON),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('user_preferences')
```

## Troubleshooting

### "Can't locate revision identified by"
```bash
# Reset alembic version table
alembic stamp head
```

### "Target database is not up to date"
```bash
# Check current version
alembic current

# Upgrade to latest
alembic upgrade head
```

### Migration conflicts
```bash
# Show branches
alembic branches

# Merge branches
alembic merge -m "merge branches" <rev1> <rev2>
```
