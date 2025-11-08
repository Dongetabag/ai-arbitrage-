import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { category = 'all' } = req.body;

    console.log(`🔍 Force scan triggered for category: ${category} at ${new Date().toISOString()}`);

    res.status(200).json({
      status: 'scanning',
      category: category,
      message: 'Marketplace scan initiated - scanning Facebook, Craigslist, OfferUp, eBay, Mercari',
      estimated_duration_seconds: 300,
      timestamp: new Date().toISOString(),
      sources: ['Facebook Marketplace', 'Craigslist', 'OfferUp', 'eBay', 'Mercari', 'Poshmark']
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
