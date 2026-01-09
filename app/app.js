const catalog = [
  {
    keys: ["cobalt", "amex cobalt"],
    issuer: "American Express",
    network: "Amex",
    name: "Amex Cobalt",
    annualFee: "$12.99/mo",
    highlights: [
      "5x points on dining",
      "5x points on groceries",
      "2x points on travel",
    ],
    multipliers: [
      { category: "restaurant", rate: "5x" },
      { category: "grocery", rate: "5x" },
      { category: "travel", rate: "2x" },
      { category: "general", rate: "1x" },
    ],
    rewardRules: { restaurant: 5, grocery: 5, travel: 2, general: 1 },
  },
  {
    keys: ["scotia", "gold amex"],
    issuer: "Scotiabank",
    network: "Amex",
    name: "Scotiabank Gold Amex",
    annualFee: "$120",
    highlights: ["5x points on dining", "5x points on groceries", "3x on transit"],
    multipliers: [
      { category: "restaurant", rate: "5x" },
      { category: "grocery", rate: "5x" },
      { category: "transit", rate: "3x" },
      { category: "gas", rate: "3x" },
      { category: "general", rate: "1x" },
    ],
    rewardRules: { restaurant: 5, grocery: 5, transit: 3, gas: 3, general: 1 },
  },
  {
    keys: ["rogers", "world elite"],
    issuer: "Rogers",
    network: "Mastercard",
    name: "Rogers World Elite",
    annualFee: "$0",
    highlights: ["2% back on transit", "1.5% back everywhere"],
    multipliers: [
      { category: "transit", rate: "2%" },
      { category: "general", rate: "1.5%" },
    ],
    rewardRules: { transit: 2, general: 1.5 },
  },
  {
    keys: ["aeroplan", "td"],
    issuer: "TD",
    network: "Visa",
    name: "TD Aeroplan Visa",
    annualFee: "$139",
    highlights: ["2x on travel", "1.5x on grocery and gas"],
    multipliers: [
      { category: "travel", rate: "2x" },
      { category: "grocery", rate: "1.5x" },
      { category: "gas", rate: "1.5x" },
      { category: "general", rate: "1x" },
    ],
    rewardRules: { travel: 2, grocery: 1.5, gas: 1.5, general: 1 },
  },
  {
    keys: ["avion", "rbc"],
    issuer: "RBC",
    network: "Visa",
    name: "RBC Avion Visa Infinite",
    annualFee: "$120",
    highlights: ["2x on travel", "1.5x on dining"],
    multipliers: [
      { category: "travel", rate: "2x" },
      { category: "restaurant", rate: "1.5x" },
      { category: "general", rate: "1x" },
    ],
    rewardRules: { travel: 2, restaurant: 1.5, general: 1 },
  },
];

const merchants = [
  { name: "Sunrise Diner", category: "restaurant", lat: 43.65, lng: -79.38 },
  { name: "Maple Grocery", category: "grocery", lat: 43.66, lng: -79.39 },
  { name: "Paws & Co.", category: "pet_store", lat: 43.648, lng: -79.382 },
  { name: "Station Cafe", category: "coffee", lat: 43.647, lng: -79.374 },
  { name: "HealthMart Pharmacy", category: "pharmacy", lat: 43.653, lng: -79.391 },
];

const aliasMap = {
  coffee: "restaurant",
  pet_store: "general",
  pharmacy: "general",
};

const form = document.getElementById("card-form");
const output = document.getElementById("benefits-output");
const matchPill = document.getElementById("match-pill");
const savedCards = document.getElementById("saved-cards");
const clearBtn = document.getElementById("clear-btn");
const sweepBtn = document.getElementById("sweep-btn");
const sweepOutput = document.getElementById("sweep-output");
const amexToggle = document.getElementById("amex-toggle");

const saved = [];

function normalize(value) {
  return (value || "").toLowerCase();
}

function findMatch(name, issuer) {
  const key = normalize(name);
  const issuerKey = normalize(issuer);

  return catalog.find((item) => {
    const keyHit = item.keys.some((token) => key.includes(token));
    const issuerHit = normalize(item.issuer) === issuerKey;
    return keyHit || issuerHit;
  });
}

function renderBenefits(card, matched) {
  const multipliers = card.multipliers
    .map((entry) => `<span>${entry.category}: ${entry.rate}</span>`)
    .join(" ");

  output.innerHTML = `
    <div class="benefits">
      <div class="benefit-card">
        <div class="benefit-title">${card.name}</div>
        <div class="kv">
          <span>Issuer: ${card.issuer}</span>
          <span>Network: ${card.network}</span>
          <span>Annual fee: ${card.annualFee}</span>
        </div>
      </div>
      <div class="benefit-card">
        <div class="benefit-title">Highlights</div>
        <div class="kv">${card.highlights.map((item) => `<span>${item}</span>`).join(" ")}</div>
      </div>
      <div class="benefit-card">
        <div class="benefit-title">Category multipliers</div>
        <div class="kv">${multipliers}</div>
      </div>
      <button id="save-btn">Save card</button>
    </div>
  `;

  matchPill.textContent = matched ? "Matched" : "Fallback";
}

function renderSaved() {
  if (saved.length === 0) {
    savedCards.innerHTML = "<div class=\"empty-state\">No saved cards yet.</div>";
    return;
  }

  savedCards.innerHTML = saved
    .map(
      (card) => `
        <div class="saved-card">
          <h3>${card.name}</h3>
          <div class="kv">
            <span>${card.issuer}</span>
            <span>${card.network}</span>
            <span>Fee: ${card.annualFee}</span>
          </div>
        </div>
      `
    )
    .join("");
}

function buildFallback(name, issuer, network) {
  return {
    name: name || "Custom card",
    issuer: issuer || "Unknown issuer",
    network: network || "Unknown network",
    annualFee: "Unknown",
    highlights: [
      "Default 1% back on everything",
      "Mocked benefits - needs API verification",
    ],
    multipliers: [
      { category: "general", rate: "1%" },
      { category: "restaurant", rate: "1%" },
      { category: "grocery", rate: "1%" },
    ],
    rewardRules: { general: 1, restaurant: 1, grocery: 1 },
  };
}

function nearestMerchant(lat, lng) {
  let best = null;
  let bestDist = Number.POSITIVE_INFINITY;

  merchants.forEach((merchant) => {
    const dist = Math.hypot(lat - merchant.lat, lng - merchant.lng) * 111;
    if (dist < bestDist) {
      bestDist = dist;
      best = { ...merchant, distanceKm: dist };
    }
  });

  return bestDist <= 0.3 ? best : null;
}

function fallbackCategory(lat, lng) {
  const buckets = ["restaurant", "pet_store", "grocery", "coffee", "pharmacy", "general"];
  const key = Math.floor(Math.abs(lat * 1000) + Math.abs(lng * 1000)) % buckets.length;
  return buckets[key];
}

function recommendCard(category, acceptsAmex) {
  const resolved = aliasMap[category] || category;
  let best = null;
  let bestScore = -Infinity;

  catalog.forEach((card) => {
    if (!acceptsAmex && card.network === "Amex") {
      return;
    }
    const rate = card.rewardRules[resolved] || card.rewardRules.general || 1;
    if (rate > bestScore) {
      bestScore = rate;
      best = card;
    }
  });

  return best;
}

function generateGrid(center, span, step) {
  const [lat0, lng0] = center;
  const points = [];
  for (let lat = lat0 - span; lat <= lat0 + span; lat += step) {
    for (let lng = lng0 - span; lng <= lng0 + span; lng += step) {
      points.push([Number(lat.toFixed(6)), Number(lng.toFixed(6))]);
    }
  }
  return points;
}

function renderSweep(rows) {
  sweepOutput.innerHTML = `
    <div class="sweep-grid">
      ${rows
        .map(
          (row) => `
          <div class="sweep-row">
            <div>
              <strong>${row.category}</strong><br />
              <span>${row.source}</span>
            </div>
            <div>
              <strong>${row.recommended}</strong><br />
              <span>Best for ${row.resolved}</span>
            </div>
            <div>
              <strong>${row.lat}, ${row.lng}</strong><br />
              <span>${row.confidence}% confidence</span>
            </div>
          </div>
        `
        )
        .join("")}
    </div>
  `;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const name = document.getElementById("card-name").value.trim();
  const issuer = document.getElementById("card-issuer").value.trim();
  const network = document.getElementById("card-network").value.trim();

  const matched = findMatch(name, issuer);
  const card = matched
    ? {
        ...matched,
        issuer: matched.issuer,
        network: matched.network,
      }
    : buildFallback(name, issuer, network);

  renderBenefits(card, Boolean(matched));

  const saveBtn = document.getElementById("save-btn");
  saveBtn.addEventListener("click", () => {
    saved.push(card);
    renderSaved();
    matchPill.textContent = "Saved";
  });
});

clearBtn.addEventListener("click", () => {
  form.reset();
  output.innerHTML = "Submit a card to see mocked benefits.";
  matchPill.textContent = "Waiting";
});

sweepBtn.addEventListener("click", () => {
  const acceptsAmex = amexToggle.checked;
  const points = generateGrid([43.651, -79.382], 0.008, 0.004);
  const rows = points.map(([lat, lng]) => {
    const match = nearestMerchant(lat, lng);
    const category = match ? match.category : fallbackCategory(lat, lng);
    const source = match ? `POI: ${match.name}` : "fallback";
    const resolved = aliasMap[category] || category;
    const card = recommendCard(category, acceptsAmex);
    return {
      lat,
      lng,
      category,
      source,
      resolved,
      recommended: card ? card.name : "No match",
      confidence: match ? 82 : 35,
    };
  });

  renderSweep(rows);
});

renderSaved();
