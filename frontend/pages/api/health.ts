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
    res.status(200).json({
      status: 'healthy',
      service: 'AI Arbitrage Platform',
      version: '1.0.0',
      environment: process.env.VERCEL_ENV || 'development',
      timestamp: new Date().toISOString(),
      platform: 'Vercel',
      ai_model: 'GPT-4 Turbo',
      features: {
        marketplace_scanning: true,
        ai_negotiation: true,
        price_prediction: true,
        auto_listing: true
      }
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
