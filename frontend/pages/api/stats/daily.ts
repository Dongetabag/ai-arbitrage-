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
    const today = new Date().toISOString().split('T')[0];

    // Generate realistic daily stats
    const stats = {
      opportunities_found: Math.floor(Math.random() * 30) + 40,
      purchases_completed: Math.floor(Math.random() * 5) + 3,
      sales_completed: Math.floor(Math.random() * 4) + 2,
      total_profit: parseFloat((Math.random() * 2000 + 1000).toFixed(2)),
      avg_margin: parseFloat((Math.random() * 0.2 + 0.25).toFixed(3)),
      date: today
    };

    res.status(200).json(stats);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
