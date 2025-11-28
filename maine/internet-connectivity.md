# Internet Connectivity Guide for Remote Work in Maine

Critical infrastructure planning for remote software engineering work.

## TL;DR

**Good news:** 65.5% of Maine has fiber available. Your target areas (Orono, Waterville, Brunswick) all have fiber options.

**The rule:** Verify fiber availability at the specific address BEFORE making an offer on any property.

---

## Maine Fiber Coverage Overview

| Metric | Value |
|--------|-------|
| Fiber availability statewide | 65.53% |
| Max available speeds | Up to 5 Gbps |
| Primary fiber provider | Fidium (Consolidated Communications) |
| State connectivity goal | 100% by end of 2024 (achieved via fiber + alternatives) |

### Recent Expansion

The Maine Connectivity Authority has funded broadband for 86,000+ homes and businesses. Lincoln County became the first Maine county with fiber in every town.

---

## Fiber Providers by Region

### Statewide / Major Providers

| Provider | Max Speed | Starting Price | Notes |
|----------|-----------|----------------|-------|
| **Fidium Fiber** | 2 Gbps | ~$70/mo | Best coverage in Maine |
| **Spectrum** | 1 Gbps | ~$50/mo | Cable, not true fiber |
| **EarthLink Fiber** | 5 Gbps | $39.95/mo | Uses local fiber networks |
| **GoNetspeed** | 1 Gbps | ~$65/mo | Growing in southern Maine |
| **GWI** | Varies | ~$50/mo | Local Maine ISP |

### By Target Town

#### Orono / Old Town Area
- **15+ providers** including 7 fiber options
- EarthLink Fiber: up to 5 Gbps
- Fidium Fiber: widely available
- Spectrum: cable backup
- **Verdict:** Excellent connectivity

#### Waterville Area
- Fidium Fiber: expanding coverage
- Spectrum: available
- Coverage varies by specific address
- **Verdict:** Good, but verify address

#### Brunswick Area
- Fidium Fiber: strong coverage
- GoNetspeed: available
- Spectrum: available
- **Verdict:** Excellent connectivity

---

## How to Verify Before Buying

### Step 1: Check the Maps

1. **FCC National Broadband Map:** [broadbandmap.fcc.gov](https://broadbandmap.fcc.gov/)
   - Enter specific address
   - Shows all reported ISPs and speeds

2. **Maine Connectivity Authority:** [maineconnectivity.org](https://www.maineconnectivity.org/)
   - State-specific data
   - Shows planned expansion areas

3. **BroadbandNow:** [broadbandnow.com/Maine](https://broadbandnow.com/Maine)
   - Aggregated provider data
   - User reviews

### Step 2: Call the Providers

Maps can be outdated. Before making an offer:
1. Call Fidium: 1-844-4-FIDIUM
2. Call local providers serving the area
3. Ask: "Is fiber available at [exact address]? When can you install?"

### Step 3: Talk to Neighbors

If possible during a property visit, knock on a neighbor's door and ask what internet they have. Real-world verification.

---

## Starlink as Backup

If fiber isn't available at your dream property, Starlink is a viable alternative.

### Starlink Residential

| Metric | Value |
|--------|-------|
| Download Speed | 25-100 Mbps typical |
| Upload Speed | 5-20 Mbps |
| Latency | 25-50ms |
| Monthly Cost | $120/mo |
| Equipment | $499 one-time |
| Contract | None |

### Can You Work Remote on Starlink?

| Task | Starlink Capable? |
|------|-------------------|
| Video calls (Zoom, Meet) | ✅ Yes, works well |
| SSH/terminal work | ✅ Yes |
| Git push/pull | ✅ Yes |
| Large file transfers | ⚠️ Slower but works |
| Low-latency gaming | ⚠️ Marginal |
| Streaming 4K | ✅ Yes |

**Reality check:** Many remote workers use Starlink successfully. It's not fiber, but it's not dial-up either. For software engineering (code, git, video calls), it's sufficient.

### Starlink Considerations

**Pros:**
- Available almost anywhere in Maine
- No contracts
- Improving performance over time
- Works during power outages (with battery backup)

**Cons:**
- Weather can affect signal (heavy snow, storms)
- Upload speed limited compared to fiber
- Latency higher than fiber
- Trees can block signal (need clear sky view)

### Installation Tips

- Need clear view of northern sky
- Roof mount or pole mount options
- Can use Starlink app to check for obstructions before buying property
- Some trees are manageable; dense forest is not

---

## Redundancy Strategy for Critical Remote Work

If your job is mission-critical, consider:

### Option 1: Fiber + Cellular Backup
- Primary: Fiber (Fidium, etc.)
- Backup: Phone hotspot or dedicated cellular modem
- Failover: Router with automatic switchover (Peplink, etc.)
- Cost: ~$100/mo total

### Option 2: Fiber + Starlink
- Primary: Fiber
- Backup: Starlink
- True redundancy for critical work
- Cost: ~$200/mo total

### Option 3: Starlink + Cellular
- For properties without fiber
- Starlink primary
- Cellular backup
- Works anywhere with cell signal

---

## Internet Speed Requirements for Remote Software Engineering

| Activity | Download Needed | Upload Needed |
|----------|-----------------|---------------|
| Video conferencing | 5-10 Mbps | 3-5 Mbps |
| Screen sharing | 5 Mbps | 5 Mbps |
| Git operations | 10-50 Mbps | 10-20 Mbps |
| Docker/container pulls | 50-100 Mbps | N/A |
| IDE cloud sync | 10 Mbps | 10 Mbps |
| General browsing | 5 Mbps | 1 Mbps |

**Minimum viable:** 50 Mbps down / 10 Mbps up
**Comfortable:** 200 Mbps down / 20 Mbps up
**Ideal:** 500 Mbps+ down / 50 Mbps+ up

Both fiber (typically 1 Gbps symmetric) and Starlink (25-100 Mbps) exceed minimum requirements.

---

## Cost Comparison

| Service | Monthly | Annual |
|---------|---------|--------|
| Fidium 1 Gbps | ~$70 | $840 |
| Spectrum 500 Mbps | ~$70 | $840 |
| Starlink | $120 | $1,440 |
| Starlink + Fiber (redundant) | $190 | $2,280 |

**Value calculation:** The $50/mo premium for Starlink over fiber is worth it if it means you can buy a more affordable/desirable property without fiber.

---

## Expansion Projects to Watch

Maine is actively expanding fiber:

- **Lincoln County:** Full fiber coverage completed
- **Waldoboro:** Fidium partnership, now connected
- **Dedham:** 60 miles of fiber installed for 1,648 residents
- **Katahdin region:** 5 towns received fiber grants

The state received $110 million in federal funds for broadband expansion. Areas currently without fiber may have it within 1-2 years.

**Strategy:** If a property is in a planned expansion zone, you might:
1. Buy now at lower price
2. Use Starlink temporarily
3. Switch to fiber when it arrives
4. End up with great property at below-market cost

---

## Questions for Real Estate Agent

1. "What internet service is available at this address?"
2. "Have neighboring properties reported fiber availability?"
3. "Is this area in a planned fiber expansion zone?"
4. "Do any current offers have internet contingencies?"

---

## Sources

- [BroadbandNow Maine](https://broadbandnow.com/Maine)
- [Maine Connectivity Authority](https://www.maineconnectivity.org/)
- [FCC National Broadband Map](https://broadbandmap.fcc.gov/)
- [Starlink](https://www.starlink.com/)
- [Press Herald: Connecting Maine](https://www.pressherald.com/2025/11/13/connecting-maine-how-fiber-internet-is-reshaping-communities/)
- [Lincoln County News: First Maine County with Fiber](https://lcnme.com/currentnews/lincoln-county-is-first-maine-county-with-fiber-internet-in-every-town/)
