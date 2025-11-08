import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    const totalOpps = Math.floor(Math.random() * 500) + 1000;
    const totalPurchases = Math.floor(totalOpps * 0.15);
    const totalSales = Math.floor(totalPurchases * 0.85);
    const totalRevenue = totalSales * 250;
    const totalProfit = totalRevenue * 0.35;

    const stats = {
      total_opportunities: totalOpps,
      total_purchases: totalPurchases,
      total_sales: totalSales,
      total_revenue: parseFloat(totalRevenue.toFixed(2)),
      total_profit: parseFloat(totalProfit.toFixed(2)),
      conversion_rate: parseFloat(((totalPurchases / totalOpps) * 100).toFixed(2)),
      avg_profit_per_sale: parseFloat((totalProfit / totalSales).toFixed(2))
    };

    res.status(200).json(stats);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
