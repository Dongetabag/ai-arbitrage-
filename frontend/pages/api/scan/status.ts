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
    const now = new Date();
    const nextScan = new Date(now.getTime() + 10 * 60000);

    res.status(200).json({
      is_scanning: Math.random() > 0.7,
      last_scan: now.toISOString(),
      next_scan: nextScan.toISOString(),
      marketplaces_active: ['Facebook Marketplace', 'Craigslist', 'OfferUp', 'eBay', 'Mercari', 'Poshmark', 'LetGo'],
      categories_active: 10,
      ai_model: 'GPT-4 Turbo',
      total_sources: 100
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
