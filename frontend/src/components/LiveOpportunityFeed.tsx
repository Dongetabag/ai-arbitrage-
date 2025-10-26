/**
 * Live Opportunity Feed Component
 * Real-time WebSocket updates for new opportunities
 */

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface LiveOpportunity {
  id: number;
  product_title: string;
  source_price: number;
  estimated_profit: number;
  profit_margin: number;
  category: string;
  ai_decision: string;
}

export default function LiveOpportunityFeed() {
  const [opportunities, setOpportunities] = useState<LiveOpportunity[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws/opportunities');

    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'opportunity') {
        setOpportunities(prev => [data.data, ...prev].slice(0, 10));
        
        // Show notification for high-profit opportunities
        if (data.data.estimated_profit > 50) {
          showNotification(data.data);
        }
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  const showNotification = (opp: LiveOpportunity) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('🎯 High-Profit Opportunity!', {
        body: `${opp.product_title}\nProfit: $${opp.estimated_profit.toFixed(2)}`,
        icon: '/logo.png',
      });
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">🔴 Live Feed</h2>
        <div className="flex items-center">
          <div className={`w-2 h-2 rounded-full mr-2 ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-gray-400">
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto">
        <AnimatePresence>
          {opportunities.map((opp) => (
            <motion.div
              key={opp.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="bg-gray-750 rounded p-4 border-l-4 border-green-500"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex-1">
                  <div className="font-medium text-sm mb-1">{opp.product_title}</div>
                  <div className="text-xs text-gray-400">{opp.category}</div>
                </div>
                <div className="text-right">
                  <div className="text-green-400 font-bold">
                    +${opp.estimated_profit.toFixed(2)}
                  </div>
                  <div className="text-xs text-gray-400">
                    {(opp.profit_margin * 100).toFixed(0)}% margin
                  </div>
                </div>
              </div>
              
              <div className="flex justify-between items-center text-xs">
                <span className="text-gray-400">
                  Buy: ${opp.source_price.toFixed(2)}
                </span>
                <span className={`px-2 py-1 rounded ${
                  opp.ai_decision === 'PURCHASE' ? 'bg-green-900 text-green-200' :
                  opp.ai_decision === 'NEGOTIATE' ? 'bg-yellow-900 text-yellow-200' :
                  'bg-gray-700 text-gray-300'
                }`}>
                  {opp.ai_decision}
                </span>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {opportunities.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            Waiting for opportunities...
          </div>
        )}
      </div>
    </div>
  );
}

