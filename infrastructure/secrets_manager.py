"""
Secure Credentials Management
Uses python-dotenv for local, AWS Secrets Manager for production
"""

import os
from typing import Dict, Optional
from loguru import logger
import json


class SecretsManager:
    """
    Centralized secrets management
    
    Development: python-dotenv
    Production: AWS Secrets Manager or Vault
    """
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv('ENVIRONMENT', 'development')
        
        if self.environment == 'production':
            self._init_aws_secrets()
        else:
            self._init_dotenv()
    
    def _init_dotenv(self):
        """Initialize python-dotenv for local development"""
        
        from dotenv import load_dotenv
        
        load_dotenv()
        logger.info("Loaded secrets from .env file")
    
    def _init_aws_secrets(self):
        """Initialize AWS Secrets Manager"""
        
        try:
            import boto3
            
            self.secrets_client = boto3.client('secretsmanager')
            logger.info("AWS Secrets Manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize AWS Secrets Manager: {e}")
            self.secrets_client = None
    
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get secret value
        
        Tries:
        1. Environment variable
        2. AWS Secrets Manager (if production)
        3. Default value
        """
        
        # Try environment variable first
        value = os.getenv(key)
        if value:
            return value
        
        # Try AWS Secrets Manager in production
        if self.environment == 'production' and self.secrets_client:
            try:
                response = self.secrets_client.get_secret_value(SecretId=key)
                return response['SecretString']
            except Exception as e:
                logger.debug(f"AWS secret '{key}' not found: {e}")
        
        # Return default
        return default
    
    def get_secrets_dict(self, secret_name: str) -> Dict:
        """
        Get dictionary of secrets (for grouped credentials)
        
        Example: All eBay credentials in one secret
        """
        
        if self.environment == 'production' and self.secrets_client:
            try:
                response = self.secrets_client.get_secret_value(SecretId=secret_name)
                return json.loads(response['SecretString'])
            except Exception as e:
                logger.error(f"Failed to get secrets dict '{secret_name}': {e}")
        
        return {}
    
    def rotate_secret(self, key: str, new_value: str):
        """
        Rotate a secret (update value)
        """
        
        if self.environment == 'production' and self.secrets_client:
            try:
                self.secrets_client.update_secret(
                    SecretId=key,
                    SecretString=new_value
                )
                logger.info(f"Rotated secret: {key}")
            except Exception as e:
                logger.error(f"Failed to rotate secret: {e}")
        else:
            logger.warning("Secret rotation only available in production with AWS")


class CredentialVault:
    """
    Vault integration for production credential storage
    Alternative to AWS Secrets Manager
    """
    
    def __init__(self, vault_url: str = None, vault_token: str = None):
        self.vault_url = vault_url or os.getenv('VAULT_URL')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN')
        
        if self.vault_url and self.vault_token:
            self._init_vault()
    
    def _init_vault(self):
        """Initialize Vault client"""
        
        try:
            import hvac
            
            self.client = hvac.Client(
                url=self.vault_url,
                token=self.vault_token
            )
            
            if self.client.is_authenticated():
                logger.info("Vault authenticated successfully")
            else:
                logger.error("Vault authentication failed")
                self.client = None
        
        except ImportError:
            logger.warning("hvac library not installed - Vault unavailable")
            self.client = None
        except Exception as e:
            logger.error(f"Vault initialization failed: {e}")
            self.client = None
    
    def read_secret(self, path: str, key: str) -> Optional[str]:
        """Read secret from Vault"""
        
        if not self.client:
            return None
        
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response['data']['data'].get(key)
        except Exception as e:
            logger.error(f"Vault read error: {e}")
            return None
    
    def write_secret(self, path: str, data: Dict):
        """Write secret to Vault"""
        
        if not self.client:
            return
        
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data
            )
            logger.info(f"Secret written to Vault: {path}")
        except Exception as e:
            logger.error(f"Vault write error: {e}")


# Global secrets manager instance
secrets = SecretsManager()


def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Convenience function to get secrets
    
    Usage:
        api_key = get_secret('OPENAI_API_KEY')
    """
    return secrets.get_secret(key, default)

