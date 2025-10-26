"""
Machine Learning Price Prediction & Dynamic Pricing
Uses scikit-learn and pandas for intelligent pricing decisions
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
from pathlib import Path
from loguru import logger
from typing import Dict, List, Optional
import json


class PricePredictionModel:
    """
    ML-powered price prediction for optimal listing prices
    """
    
    def __init__(self, model_path: str = "ml/models/price_predictor.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'source_price', 'category_encoded', 'condition_encoded',
            'seller_rating', 'days_since_listing', 'season_encoded',
            'avg_market_price_30d', 'sales_rank', 'competitor_count'
        ]
        
        if self.model_path.exists():
            self.load_model()
    
    def train(self, historical_data: pd.DataFrame):
        """
        Train price prediction model on historical sales data
        
        Args:
            historical_data: DataFrame with columns:
                - source_price, target_price, actual_sale_price
                - category, condition, seller_rating
                - days_to_sell, profit_margin
        """
        
        logger.info("Training price prediction model...")
        
        # Feature engineering
        X = self._engineer_features(historical_data)
        y = historical_data['actual_sale_price']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train ensemble model
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        logger.info(f"Model trained - MAE: ${mae:.2f}, R²: {r2:.3f}")
        
        # Save model
        self.save_model()
        
        return {'mae': mae, 'r2': r2}
    
    def predict_optimal_price(self, opportunity: Dict) -> Dict:
        """
        Predict optimal listing price for maximum profit
        
        Returns:
            {
                'predicted_price': float,
                'confidence_interval': (lower, upper),
                'expected_days_to_sell': int,
                'predicted_margin': float
            }
        """
        
        if not self.model:
            logger.warning("Model not trained, using rule-based pricing")
            return self._rule_based_pricing(opportunity)
        
        # Prepare features
        features = self._prepare_features(opportunity)
        features_scaled = self.scaler.transform([features])
        
        # Predict
        predicted_price = self.model.predict(features_scaled)[0]
        
        # Calculate confidence interval (simplified)
        # In production, use quantile regression or ensemble variance
        price_std = predicted_price * 0.10  # 10% uncertainty
        confidence_interval = (
            predicted_price - 1.96 * price_std,
            predicted_price + 1.96 * price_std
        )
        
        # Estimate days to sell (based on price vs market avg)
        market_avg = opportunity.get('market_average_price', predicted_price)
        price_ratio = predicted_price / market_avg if market_avg > 0 else 1.0
        
        # Lower price = faster sale
        base_days = 14
        if price_ratio < 0.9:
            expected_days = int(base_days * 0.5)  # 7 days
        elif price_ratio < 1.0:
            expected_days = int(base_days * 0.75)  # 10 days
        elif price_ratio < 1.1:
            expected_days = base_days  # 14 days
        else:
            expected_days = int(base_days * 1.5)  # 21 days
        
        # Calculate predicted margin
        total_cost = opportunity['source_price'] + opportunity.get('estimated_fees', 0)
        predicted_margin = (predicted_price - total_cost) / predicted_price if predicted_price > 0 else 0
        
        return {
            'predicted_price': round(predicted_price, 2),
            'confidence_interval': (round(confidence_interval[0], 2), round(confidence_interval[1], 2)),
            'expected_days_to_sell': expected_days,
            'predicted_margin': predicted_margin,
            'recommendation': self._get_pricing_recommendation(predicted_price, opportunity)
        }
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features for ML model"""
        
        features = pd.DataFrame()
        
        # Numeric features
        features['source_price'] = df['source_price']
        features['seller_rating'] = df['seller_rating'].fillna(3.0)
        features['days_since_listing'] = (pd.Timestamp.now() - pd.to_datetime(df['listed_at'])).dt.days
        
        # Categorical encoding
        features['category_encoded'] = pd.Categorical(df['category']).codes
        features['condition_encoded'] = pd.Categorical(df['condition']).codes
        features['season_encoded'] = pd.to_datetime(df['listed_at']).dt.quarter
        
        # Market features
        features['avg_market_price_30d'] = df.get('market_avg_30d', df['target_price'])
        features['sales_rank'] = df.get('sales_rank', 10000)
        features['competitor_count'] = df.get('competitor_count', 5)
        
        return features[self.feature_columns]
    
    def _prepare_features(self, opportunity: Dict) -> List[float]:
        """Prepare features for single prediction"""
        
        from datetime import datetime
        
        features = [
            opportunity['source_price'],
            self._encode_category(opportunity.get('category', 'other')),
            self._encode_condition(opportunity.get('condition', 'used')),
            opportunity.get('seller_rating', 3.0),
            0,  # days_since_listing (new item)
            (datetime.now().month - 1) // 3 + 1,  # season (quarter)
            opportunity.get('market_avg_30d', opportunity.get('target_price', 0)),
            opportunity.get('sales_rank', 10000),
            opportunity.get('competitor_count', 5)
        ]
        
        return features
    
    def _encode_category(self, category: str) -> int:
        """Encode category to numeric"""
        categories = ['books', 'trading_cards', 'video_games', 'musical_instruments', 
                     'lego', 'sporting_goods', 'baby_equipment', 'electronics', 
                     'photography', 'tools', 'other']
        return categories.index(category) if category in categories else len(categories) - 1
    
    def _encode_condition(self, condition: str) -> int:
        """Encode condition to numeric"""
        conditions = {'new': 5, 'like new': 4, 'very good': 3, 'good': 2, 'acceptable': 1, 'poor': 0}
        return conditions.get(condition.lower(), 2)
    
    def _rule_based_pricing(self, opportunity: Dict) -> Dict:
        """Fallback rule-based pricing if ML model not available"""
        
        source_price = opportunity['source_price']
        target_price = opportunity.get('target_price', source_price * 2)
        fees = opportunity.get('estimated_fees', target_price * 0.15)
        
        # Target 25% margin
        optimal_price = (source_price + fees) / 0.75
        
        # Round to psychological price point
        optimal_price = round(optimal_price - 0.01, 2)  # e.g., $49.99
        
        return {
            'predicted_price': optimal_price,
            'confidence_interval': (optimal_price * 0.9, optimal_price * 1.1),
            'expected_days_to_sell': 14,
            'predicted_margin': 0.25,
            'recommendation': 'Rule-based pricing (ML model not trained)'
        }
    
    def _get_pricing_recommendation(self, predicted_price: float, opportunity: Dict) -> str:
        """Get human-readable pricing recommendation"""
        
        market_avg = opportunity.get('market_avg_30d', predicted_price)
        
        if predicted_price < market_avg * 0.9:
            return "Aggressive pricing - Quick sale expected"
        elif predicted_price < market_avg:
            return "Competitive pricing - Good balance of speed and profit"
        elif predicted_price < market_avg * 1.1:
            return "Premium pricing - Higher profit, slower sale"
        else:
            return "High pricing - May take longer to sell"
    
    def save_model(self):
        """Save trained model to disk"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'features': self.feature_columns
        }, self.model_path)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_columns = data['features']
            
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")


class DynamicPricingStrategy:
    """
    Dynamic pricing that adjusts based on market conditions
    Uses scikit-learn for optimization
    """
    
    def __init__(self):
        self.price_history = []
    
    def calculate_dynamic_price(self,
                               current_price: float,
                               days_listed: int,
                               views_count: int,
                               watchers_count: int,
                               competitor_prices: List[float]) -> float:
        """
        Calculate optimal price adjustment based on performance
        
        Uses ML to determine:
        - If price is too high (low views/watchers)
        - If we should increase price (high demand)
        - Optimal competitive positioning
        """
        
        # Calculate metrics
        avg_competitor_price = np.mean(competitor_prices) if competitor_prices else current_price
        min_competitor_price = np.min(competitor_prices) if competitor_prices else current_price * 0.9
        
        # Engagement rate (views to watchers conversion)
        engagement_rate = watchers_count / views_count if views_count > 0 else 0
        
        # Decision logic
        new_price = current_price
        
        # Low views = price too high
        if days_listed > 7 and views_count < 10:
            new_price = current_price * 0.95  # 5% reduction
            logger.info(f"Low views ({views_count}) - reducing price to ${new_price:.2f}")
        
        # High engagement but not selling = price slightly high
        elif engagement_rate > 0.10 and days_listed > 14:
            new_price = current_price * 0.97  # 3% reduction
            logger.info(f"Good engagement but no sale - small reduction to ${new_price:.2f}")
        
        # Beat competition by small margin
        elif avg_competitor_price > 0:
            target_price = min_competitor_price * 0.99  # Just below lowest competitor
            if target_price < current_price and target_price > current_price * 0.90:
                new_price = target_price
                logger.info(f"Matching competition at ${new_price:.2f}")
        
        # If selling well (high watchers), can increase price
        elif watchers_count > 5 and days_listed < 7:
            new_price = current_price * 1.03  # 3% increase
            logger.info(f"High demand - increasing price to ${new_price:.2f}")
        
        # Round to .99 ending
        new_price = round(new_price - 0.01, 2)
        
        return new_price
    
    def optimize_for_goal(self,
                         current_price: float,
                         goal: str,
                         market_data: Dict) -> float:
        """
        Optimize price for specific goal
        
        Goals:
        - 'max_profit': Maximize profit margin
        - 'quick_sale': Sell within 7 days
        - 'balanced': Balance speed and profit
        """
        
        market_avg = market_data.get('average_price', current_price)
        
        if goal == 'max_profit':
            # Price at market average or slightly above
            optimal_price = market_avg * 1.05
            
        elif goal == 'quick_sale':
            # Price 10% below market for fast sale
            optimal_price = market_avg * 0.90
            
        else:  # balanced
            # Price 3-5% below market
            optimal_price = market_avg * 0.97
        
        logger.info(f"Optimized for '{goal}': ${optimal_price:.2f}")
        
        return round(optimal_price - 0.01, 2)


class RecommendationEngine:
    """
    Product recommendation system for cross-selling
    Uses collaborative filtering
    """
    
    def __init__(self):
        self.user_item_matrix = None
        self.model = None
    
    def build_recommendations(self, purchase_history: pd.DataFrame):
        """
        Build product recommendations based on purchase patterns
        
        "Customers who bought X also bought Y"
        """
        
        logger.info("Building recommendation engine...")
        
        # Create user-item matrix
        self.user_item_matrix = purchase_history.pivot_table(
            index='customer_id',
            columns='product_category',
            values='purchase_count',
            fill_value=0
        )
        
        # Use item-based collaborative filtering
        from sklearn.metrics.pairwise import cosine_similarity
        
        item_similarity = cosine_similarity(self.user_item_matrix.T)
        
        self.similarity_df = pd.DataFrame(
            item_similarity,
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns
        )
        
        logger.info("Recommendation engine built")
    
    def get_recommendations(self, category: str, n: int = 5) -> List[str]:
        """Get recommended categories based on purchase"""
        
        if self.similarity_df is None:
            return []
        
        if category not in self.similarity_df.columns:
            return []
        
        # Get most similar categories
        similar = self.similarity_df[category].sort_values(ascending=False)[1:n+1]
        
        return similar.index.tolist()

