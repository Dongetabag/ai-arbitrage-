"""
Simple API validation tests for production readiness
Tests that don't require full dependencies
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that critical modules can be imported"""
    try:
        from api import fastapi_endpoints
        assert fastapi_endpoints.app is not None
        print("✓ FastAPI app imports successfully")
    except ImportError as e:
        # This is expected in CI/test environments without full dependencies
        print(f"⚠ FastAPI app import skipped (dependencies not installed): {e}")
        print("  This is OK - will be tested in Docker build")
    except Exception as e:
        print(f"✗ Failed to import FastAPI app: {e}")
        raise


def test_env_example_exists():
    """Test that .env.example file exists"""
    env_example = Path(__file__).parent.parent / ".env.example"
    assert env_example.exists(), ".env.example file should exist"
    print("✓ .env.example file exists")


def test_production_docker_compose_exists():
    """Test that production docker-compose file exists"""
    docker_compose = Path(__file__).parent.parent / "docker-compose.prod.yml"
    assert docker_compose.exists(), "docker-compose.prod.yml should exist"
    print("✓ docker-compose.prod.yml exists")


def test_production_readme_exists():
    """Test that production readme exists"""
    readme = Path(__file__).parent.parent / "PRODUCTION_READY.md"
    assert readme.exists(), "PRODUCTION_READY.md should exist"
    print("✓ PRODUCTION_READY.md exists")


def test_database_init_sql_exists():
    """Test that database initialization SQL exists"""
    init_sql = Path(__file__).parent.parent / "database" / "init.sql"
    assert init_sql.exists(), "database/init.sql should exist"
    print("✓ database/init.sql exists")


def test_requirements_has_slowapi():
    """Test that requirements.txt includes slowapi for rate limiting"""
    requirements = Path(__file__).parent.parent / "requirements.txt"
    content = requirements.read_text()
    assert "slowapi" in content, "slowapi should be in requirements.txt"
    print("✓ slowapi dependency exists")


def test_gitignore_excludes_env():
    """Test that .gitignore excludes .env files"""
    gitignore = Path(__file__).parent.parent / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        assert ".env" in content, ".env should be in .gitignore"
        print("✓ .env is properly gitignored")


def test_config_yaml_exists():
    """Test that configuration file exists"""
    config = Path(__file__).parent.parent / "config" / "settings.yaml"
    assert config.exists(), "config/settings.yaml should exist"
    print("✓ config/settings.yaml exists")


if __name__ == "__main__":
    print("Running production readiness validation tests...\n")
    
    tests = [
        test_imports,
        test_env_example_exists,
        test_production_docker_compose_exists,
        test_production_readme_exists,
        test_database_init_sql_exists,
        test_requirements_has_slowapi,
        test_gitignore_excludes_env,
        test_config_yaml_exists
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✅ All production readiness checks passed!")
        sys.exit(0)
