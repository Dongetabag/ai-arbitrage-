/**
 * Main Dashboard - React with Next.js
 * Real-time arbitrage opportunity monitoring
 */

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { useQuery } from '@tanstack/react-query';
import io from 'socket.io-client';

// Dynamic import for Plotly (client-side only)
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface Opportunity {
  id: number;
  product_title: string;
  source_price: number;
  target_price: number;
  estimated_profit: number;
  profit_margin: number;
  category: string;
  ai_decision: string;
  ai_confidence: number;
  discovered_at: string;
}

interface DailyStats {
  opportunities_found: number;
  purchases_completed: number;
  listings_created: number;
  sales_completed: number;
  total_profit: number;
  avg_margin: number;
}

export default function Dashboard() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [socket, setSocket] = useState<any>(null);

  // Fetch daily stats
  const { data: stats, isLoading: statsLoading } = useQuery<DailyStats>({
    queryKey: ['dailyStats'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/api/stats/daily');
      return response.json();
    },
    refetchInterval: 60000, // Refresh every minute
  });

  // Fetch opportunities
  const { data: opportunitiesData, isLoading: oppsLoading } = useQuery<Opportunity[]>({
    queryKey: ['opportunities'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/api/opportunities?limit=50');
      return response.json();
    },
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  // WebSocket for real-time updates
  useEffect(() => {
    const socketConnection = io('ws://localhost:8000');
    
    socketConnection.on('new_opportunity', (data: Opportunity) => {
      console.log('New opportunity:', data);
      setOpportunities(prev => [data, ...prev].slice(0, 50));
    });

    socketConnection.on('purchase_completed', (data: any) => {
      console.log('Purchase completed:', data);
      // Show notification
    });

    setSocket(socketConnection);

    return () => {
      socketConnection.disconnect();
    };
  }, []);

  // Update opportunities when data changes
  useEffect(() => {
    if (opportunitiesData) {
      setOpportunities(opportunitiesData);
    }
  }, [opportunitiesData]);

  // Profit by category chart data
  const profitByCategory = React.useMemo(() => {
    const categoryMap: Record<string, number> = {};
    
    opportunities.forEach(opp => {
      categoryMap[opp.category] = (categoryMap[opp.category] || 0) + opp.estimated_profit;
    });

    return {
      x: Object.keys(categoryMap),
      y: Object.values(categoryMap),
      type: 'bar' as const,
      marker: { color: '#10b981' },
    };
  }, [opportunities]);

  // Price distribution chart
  const priceDistribution = React.useMemo(() => {
    const prices = opportunities.map(o => o.source_price);
    
    return {
      x: prices,
      type: 'histogram' as const,
      marker: { color: '#3b82f6' },
      nbinsx: 20,
    };
  }, [opportunities]);

  // Profit margin over time
  const marginOverTime = React.useMemo(() => {
    const sortedOpps = [...opportunities].sort(
      (a, b) => new Date(a.discovered_at).getTime() - new Date(b.discovered_at).getTime()
    );

    return {
      x: sortedOpps.map(o => o.discovered_at),
      y: sortedOpps.map(o => o.profit_margin * 100),
      type: 'scatter' as const,
      mode: 'lines+markers' as const,
      marker: { color: '#8b5cf6' },
      line: { shape: 'spline' as const },
    };
  }, [opportunities]);

  if (statsLoading || oppsLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900">
        <div className="text-white text-2xl">Loading Dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-2">🤖 AI Arbitrage Dashboard</h1>
        <p className="text-gray-400">Real-time profit engine monitoring</p>
      </header>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Opportunities Found"
          value={stats?.opportunities_found || 0}
          icon="🔍"
          color="blue"
        />
        <StatCard
          title="Purchases Completed"
          value={stats?.purchases_completed || 0}
          icon="🛒"
          color="green"
        />
        <StatCard
          title="Total Profit"
          value={`$${stats?.total_profit?.toFixed(2) || '0.00'}`}
          icon="💰"
          color="yellow"
        />
        <StatCard
          title="Avg Margin"
          value={`${((stats?.avg_margin || 0) * 100).toFixed(1)}%`}
          icon="📈"
          color="purple"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Profit by Category */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Profit by Category</h2>
          <Plot
            data={[profitByCategory]}
            layout={{
              paper_bgcolor: '#1f2937',
              plot_bgcolor: '#1f2937',
              font: { color: '#fff' },
              xaxis: { title: 'Category' },
              yaxis: { title: 'Estimated Profit ($)' },
              height: 300,
              margin: { t: 20, b: 60, l: 60, r: 20 },
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </div>

        {/* Price Distribution */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Purchase Price Distribution</h2>
          <Plot
            data={[priceDistribution]}
            layout={{
              paper_bgcolor: '#1f2937',
              plot_bgcolor: '#1f2937',
              font: { color: '#fff' },
              xaxis: { title: 'Price ($)' },
              yaxis: { title: 'Count' },
              height: 300,
              margin: { t: 20, b: 60, l: 60, r: 20 },
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </div>
      </div>

      {/* Margin Over Time */}
      <div className="bg-gray-800 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Profit Margin Trend</h2>
        <Plot
          data={[marginOverTime]}
          layout={{
            paper_bgcolor: '#1f2937',
            plot_bgcolor: '#1f2937',
            font: { color: '#fff' },
            xaxis: { title: 'Time' },
            yaxis: { title: 'Profit Margin (%)' },
            height: 300,
            margin: { t: 20, b: 60, l: 60, r: 20 },
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </div>

      {/* Opportunities Table */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Opportunities</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left">Product</th>
                <th className="px-4 py-3 text-left">Category</th>
                <th className="px-4 py-3 text-right">Buy Price</th>
                <th className="px-4 py-3 text-right">Sell Price</th>
                <th className="px-4 py-3 text-right">Profit</th>
                <th className="px-4 py-3 text-right">Margin</th>
                <th className="px-4 py-3 text-center">AI Decision</th>
                <th className="px-4 py-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {opportunities.map((opp) => (
                <tr key={opp.id} className="border-b border-gray-700 hover:bg-gray-750">
                  <td className="px-4 py-3">
                    <div className="max-w-xs truncate">{opp.product_title}</div>
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-1 bg-blue-900 text-blue-200 rounded text-sm">
                      {opp.category}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">${opp.source_price.toFixed(2)}</td>
                  <td className="px-4 py-3 text-right">${opp.target_price.toFixed(2)}</td>
                  <td className="px-4 py-3 text-right text-green-400">
                    ${opp.estimated_profit.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-right">
                    {(opp.profit_margin * 100).toFixed(1)}%
                  </td>
                  <td className="px-4 py-3 text-center">
                    <DecisionBadge decision={opp.ai_decision} confidence={opp.ai_confidence} />
                  </td>
                  <td className="px-4 py-3 text-center">
                    <button className="px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm">
                      Approve
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// Stat Card Component
function StatCard({ title, value, icon, color }: any) {
  const colorClasses = {
    blue: 'bg-blue-900 border-blue-700',
    green: 'bg-green-900 border-green-700',
    yellow: 'bg-yellow-900 border-yellow-700',
    purple: 'bg-purple-900 border-purple-700',
  };

  return (
    <div className={`${colorClasses[color]} border rounded-lg p-6`}>
      <div className="flex items-center justify-between mb-2">
        <div className="text-3xl">{icon}</div>
        <div className="text-2xl font-bold">{value}</div>
      </div>
      <div className="text-gray-300 text-sm">{title}</div>
    </div>
  );
}

// Decision Badge Component
function DecisionBadge({ decision, confidence }: { decision: string; confidence: number }) {
  const badges: Record<string, { color: string; text: string }> = {
    PURCHASE: { color: 'bg-green-600', text: '✓ Buy' },
    NEGOTIATE: { color: 'bg-yellow-600', text: '↔ Negotiate' },
    SKIP: { color: 'bg-red-600', text: '✗ Skip' },
    AUTHENTICATE: { color: 'bg-blue-600', text: '🔍 Auth' },
  };

  const badge = badges[decision] || { color: 'bg-gray-600', text: decision };

  return (
    <div className="flex flex-col items-center">
      <span className={`${badge.color} px-2 py-1 rounded text-xs font-semibold`}>
        {badge.text}
      </span>
      <span className="text-xs text-gray-400 mt-1">{(confidence * 100).toFixed(0)}%</span>
    </div>
  );
}

