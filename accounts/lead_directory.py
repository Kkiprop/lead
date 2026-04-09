import re


LEAD_DIRECTORY = [
    {
        'id': 'nairocap-partners',
        'firm_name': 'NairoCap Partners',
        'location': 'Nairobi, Kenya',
        'focus': 'Early-stage fintech and logistics ventures across East Africa.',
        'stage': 'Seed to Series A',
        'contact_name': 'Amina Wekesa',
        'contact_email': 'partnerships@nairocap.africa',
        'phone': '+254 20 555 0141',
        'website': 'https://www.nairocap.africa',
        'keywords': ['venture capital', 'nairobi', 'kenya', 'east africa', 'fintech', 'logistics'],
    },
    {
        'id': 'savannah-growth',
        'firm_name': 'Savannah Growth Fund',
        'location': 'Nairobi, Kenya',
        'focus': 'Growth funding for climate, agri-tech, and commerce startups.',
        'stage': 'Pre-Series A to Series B',
        'contact_name': 'Daniel Mworia',
        'contact_email': 'invest@sgf.vc',
        'phone': '+254 20 555 0164',
        'website': 'https://www.sgf.vc',
        'keywords': ['venture capital', 'nairobi', 'climate', 'agri-tech', 'commerce'],
    },
    {
        'id': 'rift-valley-ventures',
        'firm_name': 'Rift Valley Ventures',
        'location': 'Nairobi, Kenya',
        'focus': 'B2B SaaS, developer tooling, and digital infrastructure.',
        'stage': 'Pre-seed to Seed',
        'contact_name': 'Mercy Njeri',
        'contact_email': 'hello@riftvalleyventures.com',
        'phone': '+254 20 555 0190',
        'website': 'https://www.riftvalleyventures.com',
        'keywords': ['venture capital', 'nairobi', 'saas', 'developer tooling', 'infrastructure'],
    },
    {
        'id': 'east-africa-catalyst',
        'firm_name': 'East Africa Catalyst',
        'location': 'Nairobi, Kenya',
        'focus': 'Cross-border commerce, mobility, and future-of-work startups.',
        'stage': 'Seed',
        'contact_name': 'Peter Kimani',
        'contact_email': 'team@eacatalyst.vc',
        'phone': '+254 20 555 0108',
        'website': 'https://www.eacatalyst.vc',
        'keywords': ['venture capital', 'nairobi', 'mobility', 'future of work', 'commerce'],
    },
    {
        'id': 'uhuru-capital',
        'firm_name': 'Uhuru Capital',
        'location': 'Lagos, Nigeria',
        'focus': 'Embedded finance, SME software, and digital payments.',
        'stage': 'Seed to Series A',
        'contact_name': 'Ife Akinola',
        'contact_email': 'pipeline@uhurucapital.com',
        'phone': '+234 1 555 0723',
        'website': 'https://www.uhurucapital.com',
        'keywords': ['venture capital', 'lagos', 'nigeria', 'payments', 'finance', 'sme'],
    },
    {
        'id': 'atlas-frontier',
        'firm_name': 'Atlas Frontier Ventures',
        'location': 'Cape Town, South Africa',
        'focus': 'AI-enabled enterprise products and industrial software.',
        'stage': 'Pre-seed to Series A',
        'contact_name': 'Kelvin Kiprop',
        'contact_email': 'kkiprop060@gmail.com',
        'phone': '+254 721 555 188',
        'website': 'https://www.atlasfrontier.ke',
        'keywords': ['venture capital', 'cape town', 'south africa', 'ai', 'enterprise', 'software'],
    },
    {
        'id': 'baobab-scale',
        'firm_name': 'Baobab Scale',
        'location': 'Kigali, Rwanda',
        'focus': 'Health-tech, education, and public-interest technology.',
        'stage': 'Seed to Series A',
        'contact_name': 'Chantal Uwase',
        'contact_email': 'capital@baobabscale.africa',
        'phone': '+250 252 555 011',
        'website': 'https://www.baobabscale.africa',
        'keywords': ['venture capital', 'kigali', 'rwanda', 'health-tech', 'education'],
    },
    {
        'id': 'equator-bridge',
        'firm_name': 'Equator Bridge Ventures',
        'location': 'Nairobi, Kenya',
        'focus': 'Energy access, carbon markets, and climate resilience businesses.',
        'stage': 'Seed to Growth',
        'contact_name': 'Joseph Mutiso',
        'contact_email': 'climate@equatorbridge.vc',
        'phone': '+254 20 555 0173',
        'website': 'https://www.equatorbridge.vc',
        'keywords': ['venture capital', 'nairobi', 'climate', 'energy', 'carbon', 'resilience'],
    },
]


def search_investors(query):
    normalized_query = (query or '').strip().lower()
    if not normalized_query:
        return []

    terms = re.findall(r'[a-z0-9]+', normalized_query)
    if not terms:
        return []

    ranked_results = []
    for lead in LEAD_DIRECTORY:
        searchable_text = ' '.join(
            [
                lead['firm_name'],
                lead['location'],
                lead['focus'],
                lead['stage'],
                lead['contact_name'],
                lead['contact_email'],
                ' '.join(lead['keywords']),
            ]
        ).lower()
        score = 0
        for term in terms:
            if term in searchable_text:
                score += 1
        if normalized_query in searchable_text:
            score += 2
        if score:
            ranked_results.append((score, lead))

    ranked_results.sort(key=lambda item: (-item[0], item[1]['firm_name']))
    return [lead for _, lead in ranked_results]