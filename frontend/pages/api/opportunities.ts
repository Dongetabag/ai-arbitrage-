import type { NextApiRequest, NextApiResponse } from 'next';

// Mock data generator for opportunities
const generateOpportunities = () => {
  const sources = ['Facebook Marketplace', 'Craigslist', 'OfferUp', 'eBay', 'Mercari', 'Poshmark', 'LetGo'];
  const categories = ['Books', 'Electronics', 'Video Games', 'Musical Instruments', 'LEGO', 'Sporting Goods', 'Baby Equipment', 'Photography', 'Tools'];

  const opportunities = [];
  const now = new Date();

  for (let i = 0; i < 50; i++) {
    const sourcePrice = Math.random() * 200 + 20;
    const targetPrice = sourcePrice * (1.3 + Math.random() * 0.5);
    const profit = targetPrice - sourcePrice - (targetPrice * 0.15); // 15% fees
    const margin = (profit / sourcePrice) * 100;

    const category = categories[Math.floor(Math.random() * categories.length)];
    const source = sources[Math.floor(Math.random() * sources.length)];

    const productTitles = {
      'Books': ['Calculus Textbook', 'Harry Potter Collection', 'Medical Encyclopedia', 'Programming Guide'],
      'Electronics': ['iPad Pro', 'Gaming Laptop', 'Wireless Headphones', 'Smart Watch'],
      'Video Games': ['PlayStation 5', 'Nintendo Switch', 'Xbox Series X', 'Gaming PC'],
      'Musical Instruments': ['Fender Guitar', 'Yamaha Keyboard', 'DJ Controller', 'Drum Set'],
      'LEGO': ['Star Wars Set', 'Harry Potter Castle', 'Millennium Falcon', 'Architecture Series'],
      'Sporting Goods': ['Road Bike', 'Golf Clubs', 'Tennis Racket', 'Yoga Mat Set'],
      'Baby Equipment': ['Stroller', 'Car Seat', 'Crib', 'High Chair'],
      'Photography': ['Canon DSLR', 'Nikon Lens', 'GoPro Hero', 'Ring Light'],
      'Tools': ['Drill Set', 'Table Saw', 'Tool Chest', 'Power Tools']
    };

    const titles = productTitles[category] || ['Item'];
    const title = titles[Math.floor(Math.random() * titles.length)];

    opportunities.push({
      id: `opp_${Date.now()}_${i}`,
      product_title: title,
      source_marketplace: source,
      source_price: parseFloat(sourcePrice.toFixed(2)),
      target_price: parseFloat(targetPrice.toFixed(2)),
      estimated_profit: parseFloat(profit.toFixed(2)),
      profit_margin: parseFloat(margin.toFixed(2)),
      category: category,
      product_category: category,
      ai_decision: margin > 25 ? 'BUY' : 'WATCH',
      ai_confidence: Math.random() * 0.3 + 0.7,
      discovered_at: new Date(now.getTime() - Math.random() * 3600000).toISOString()
    });
  }

  // Sort by profit descending
  return opportunities.sort((a, b) => b.estimated_profit - a.estimated_profit);
};

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
    const { category, status, limit = 50 } = req.query;

    let opportunities = generateOpportunities();

    // Filter by category if provided
    if (category && category !== 'all') {
      opportunities = opportunities.filter(opp =>
        opp.category.toLowerCase() === (category as string).toLowerCase()
      );
    }

    // Apply limit
    const limitNum = parseInt(limit as string, 10);
    opportunities = opportunities.slice(0, limitNum);

    res.status(200).json(opportunities);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
