/**
 * Analytics Dashboard
 * Advanced visualizations with Plotly.js
 */

import React from 'react';
import dynamic from 'next/dynamic';
import { useQuery } from '@tanstack/react-query';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function Analytics() {
  // Fetch performance data
  const { data: performance } = useQuery({
    queryKey: ['performance'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/api/stats/performance');
      return response.json();
    },
  });

  // Sample data for visualizations
  const categoryPerformance = {
    data: [
      {
        x: ['Books', 'Trading Cards', 'Video Games', 'Instruments', 'LEGO'],
        y: [47.3, 36.8, 34.2, 31.7, 29.4],
        type: 'bar',
        marker: {
          color: ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444'],
        },
        name: 'Avg Margin %',
      },
    ],
    layout: {
      title: 'Category Performance - Profit Margins',
      paper_bgcolor: '#1f2937',
      plot_bgcolor: '#374151',
      font: { color: '#fff' },
      xaxis: { title: 'Category' },
      yaxis: { title: 'Average Margin (%)' },
    },
  };

  // ROI Comparison
  const roiComparison = {
    data: [
      {
        labels: ['Books', 'Trading Cards', 'Video Games', 'Instruments', 'Electronics'],
        values: [850, 680, 542, 471, 386],
        type: 'pie',
        marker: {
          colors: ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444'],
        },
      },
    ],
    layout: {
      title: 'Profit Distribution by Category ($)',
      paper_bgcolor: '#1f2937',
      font: { color: '#fff' },
    },
  };

  // Daily profit trend (line chart)
  const profitTrend = {
    data: [
      {
        x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        y: [250, 320, 280, 410, 380, 520, 450],
        type: 'scatter',
        mode: 'lines+markers',
        line: {
          color: '#10b981',
          width: 3,
          shape: 'spline',
        },
        marker: {
          size: 8,
          color: '#10b981',
        },
        name: 'Daily Profit',
      },
      {
        x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        y: [200, 200, 200, 200, 200, 200, 200],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: '#ef4444',
          width: 2,
          dash: 'dash',
        },
        name: 'Target ($200/day)',
      },
    ],
    layout: {
      title: 'Profit Trend - Last 7 Days',
      paper_bgcolor: '#1f2937',
      plot_bgcolor: '#374151',
      font: { color: '#fff' },
      xaxis: { title: 'Day' },
      yaxis: { title: 'Profit ($)' },
      showlegend: true,
    },
  };

  // Conversion funnel
  const conversionFunnel = {
    data: [
      {
        type: 'funnel',
        y: ['Opportunities Found', 'AI Analyzed', 'Negotiations Started', 'Purchases Made', 'Items Sold'],
        x: [1000, 450, 120, 65, 48],
        textinfo: 'value+percent previous',
        marker: {
          color: ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981', '#059669'],
        },
      },
    ],
    layout: {
      title: 'Conversion Funnel - Last 30 Days',
      paper_bgcolor: '#1f2937',
      font: { color: '#fff' },
      margin: { l: 150 },
    },
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-2">📊 Analytics & Insights</h1>
        <p className="text-gray-400">Deep dive into profit engine performance</p>
      </header>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard
          title="Total ROI"
          value="487%"
          change="+12.3%"
          trend="up"
        />
        <MetricCard
          title="Avg Profit/Item"
          value="$28.50"
          change="+$2.15"
          trend="up"
        />
        <MetricCard
          title="Inventory Turnover"
          value="18 days"
          change="-3 days"
          trend="up"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-800 rounded-lg p-6">
          <Plot
            data={categoryPerformance.data}
            layout={categoryPerformance.layout}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <Plot
            data={roiComparison.data}
            layout={roiComparison.layout}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </div>
      </div>

      {/* Full-width charts */}
      <div className="bg-gray-800 rounded-lg p-6 mb-8">
        <Plot
          data={profitTrend.data}
          layout={profitTrend.layout}
          config={{ responsive: true }}
          style={{ width: '100%', height: '400px' }}
        />
      </div>

      <div className="bg-gray-800 rounded-lg p-6">
        <Plot
          data={conversionFunnel.data}
          layout={conversionFunnel.layout}
          config={{ responsive: true }}
          style={{ width: '100%', height: '500px' }}
        />
      </div>
    </div>
  );
}

function MetricCard({ title, value, change, trend }: any) {
  const trendColor = trend === 'up' ? 'text-green-400' : 'text-red-400';
  const trendIcon = trend === 'up' ? '↑' : '↓';

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
      <div className="text-gray-400 text-sm mb-2">{title}</div>
      <div className="text-3xl font-bold mb-2">{value}</div>
      <div className={`text-sm ${trendColor}`}>
        {trendIcon} {change} from last period
      </div>
    </div>
  );
}

