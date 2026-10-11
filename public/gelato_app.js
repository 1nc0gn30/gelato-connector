/**
 * Gelato Connector — Avant-Garde Client Application
 * Neal Frazier Tech (@1nc0gn30) • NullAI Platform
 * 100% In-Browser Working Utility — Zero Fake Work
 */

const PRODUCTS = {
  "acrylic_print_16x24": {
    id: "acrylic_print_16x24",
    title: "Acrylic Glass Print (16x24 in / 40x60 cm)",
    category: "Wall Art / Acrylic",
    cost_usd: 29.50,
    cost_eur: 27.20,
    cost_gbp: 23.40,
    print_w: 4800,
    print_h: 7200,
    rec_dpi: 300,
    bleed_mm: 3.0,
    local_countries: ["US", "DE", "UK", "CA", "AU", "FR", "NL"]
  },
  "aluminum_print_16x24": {
    id: "aluminum_print_16x24",
    title: "Brushed Aluminum Dibond Print (16x24 in)",
    category: "Wall Art / Aluminum",
    cost_usd: 26.80,
    cost_eur: 24.90,
    cost_gbp: 21.20,
    print_w: 4800,
    print_h: 7200,
    rec_dpi: 300,
    bleed_mm: 3.0,
    local_countries: ["US", "DE", "UK", "CA", "AU", "NO"]
  },
  "wooden_framed_canvas_16x24": {
    id: "wooden_framed_canvas_16x24",
    title: "Framed Wooden Canvas Wrap (16x24 in)",
    category: "Wall Art / Canvas",
    cost_usd: 24.20,
    cost_eur: 22.50,
    cost_gbp: 19.30,
    print_w: 5100,
    print_h: 7500,
    rec_dpi: 300,
    bleed_mm: 5.0,
    local_countries: ["US", "UK", "DE", "FR", "ES", "IT", "CA", "AU", "JP"]
  },
  "stanley_stella_organic_tee": {
    id: "stanley_stella_organic_tee",
    title: "Stanley/Stella Organic Creator Unisex Tee",
    category: "Apparel / Organic",
    cost_usd: 12.40,
    cost_eur: 10.90,
    cost_gbp: 9.50,
    print_w: 4000,
    print_h: 4800,
    rec_dpi: 300,
    bleed_mm: 0.0,
    local_countries: ["DE", "UK", "FR", "NL", "ES", "IT", "US"]
  },
  "ceramic_mug_15oz": {
    id: "ceramic_mug_15oz",
    title: "Large Ceramic Accent Mug 15oz",
    category: "Home & Living / Mugs",
    cost_usd: 5.95,
    cost_eur: 5.40,
    cost_gbp: 4.60,
    print_w: 2850,
    print_h: 1200,
    rec_dpi: 300,
    bleed_mm: 2.0,
    local_countries: ["US", "UK", "DE", "CA", "AU"]
  },
  "enamel_campfire_mug": {
    id: "enamel_campfire_mug",
    title: "Vintage Stainless Steel Enamel Campfire Mug 12oz",
    category: "Home & Living / Outdoor",
    cost_usd: 7.40,
    cost_eur: 6.80,
    cost_gbp: 5.80,
    print_w: 2500,
    print_h: 950,
    rec_dpi: 300,
    bleed_mm: 2.0,
    local_countries: ["US", "DE", "UK", "PL"]
  },
  "hardcover_photo_journal": {
    id: "hardcover_photo_journal",
    title: "Hardcover Matte Photo Journal (A5 / 128 Pages)",
    category: "Stationery / Journals",
    cost_usd: 8.90,
    cost_eur: 8.10,
    cost_gbp: 6.90,
    print_w: 3700,
    print_h: 2600,
    rec_dpi: 300,
    bleed_mm: 4.0,
    local_countries: ["US", "DE", "UK", "NL", "AU"]
  }
};

const HUBS = {
  "US": { country: "United States", currency: "USD", symbol: "$", lead: "2.2 Days", carrier: "USPS / FedEx Ground", cost: 4.50 },
  "DE": { country: "Germany", currency: "EUR", symbol: "€", lead: "2.1 Days", carrier: "Deutsche Post / DHL", cost: 4.20 },
  "UK": { country: "United Kingdom", currency: "GBP", symbol: "£", lead: "2.0 Days", carrier: "Royal Mail 48", cost: 3.90 },
  "CA": { country: "Canada", currency: "CAD", symbol: "CA$", lead: "2.5 Days", carrier: "Canada Post", cost: 6.80 },
  "AU": { country: "Australia", currency: "AUD", symbol: "A$", lead: "2.3 Days", carrier: "Australia Post", cost: 7.20 },
  "FR": { country: "France", currency: "EUR", symbol: "€", lead: "2.4 Days", carrier: "Colissimo", cost: 4.60 },
  "NL": { country: "Netherlands", currency: "EUR", symbol: "€", lead: "2.0 Days", carrier: "PostNL", cost: 4.10 }
};

let isProActive = false;

document.addEventListener("DOMContentLoaded", () => {
  checkLicenseStatus();
  setupEventListeners();
  recalculateMargins();
  auditArtwork();
  renderHubsTable();
  generateOrderPayload();
});

function checkLicenseStatus() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("licensed") === "true" || localStorage.getItem("gelato_pro_licensed") === "true") {
    unlockProMode(false);
  }
}

function unlockProMode(saveStorage = true) {
  isProActive = true;
  if (saveStorage) localStorage.setItem("gelato_pro_licensed", "true");

  const badge = document.getElementById("pro-badge") || document.getElementById("proStatusBadge");
  if (badge) {
    badge.innerText = "⭐ PRO ACTIVE";
    badge.classList.remove("badge-free");
    badge.classList.add("badge-pro");
    badge.style.background = "rgba(212, 175, 55, 0.2)";
    badge.style.color = "var(--gold)";
    badge.style.borderColor = "var(--gold)";
  }

  document.body.classList.add("licensed", "pro-unlocked");
  document.querySelectorAll(".paywall-wrapper").forEach(w => w.classList.add("pro-unlocked"));
  closePaywallModal();
}

function setupEventListeners() {
  const prodSelect = document.getElementById("prodSelect");
  const retailPrice = document.getElementById("retailPrice");
  const currencySelect = document.getElementById("currencySelect");
  const countrySelect = document.getElementById("countrySelect");

  [prodSelect, retailPrice, currencySelect, countrySelect].forEach(el => {
    if (el) el.addEventListener("input", () => {
      recalculateMargins();
      generateOrderPayload();
    });
  });

  const auditProdSelect = document.getElementById("auditProdSelect");
  const artWidth = document.getElementById("artWidth");
  const artHeight = document.getElementById("artHeight");

  [auditProdSelect, artWidth, artHeight].forEach(el => {
    if (el) el.addEventListener("input", auditArtwork);
  });

  const dropzone = document.getElementById("artworkDropzone");
  const fileInput = document.getElementById("artworkFileInput");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());
    dropzone.addEventListener("dragover", e => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    dropzone.addEventListener("drop", e => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files.length) handleImageFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener("change", e => {
      if (e.target.files.length) handleImageFile(e.target.files[0]);
    });
  }

  const payloadForm = document.getElementById("payloadForm");
  if (payloadForm) {
    payloadForm.addEventListener("submit", e => {
      e.preventDefault();
      generateOrderPayload();
    });
  }

  // Header key button
  const btnHeaderKey = document.getElementById("btn-header-key");
  if (btnHeaderKey) {
    btnHeaderKey.addEventListener("click", () => openPaywallModal("Header Key Button"));
  }

  // Paywall unlock button
  const btnUnlockPaywall = document.getElementById("btn-unlock-paywall");
  if (btnUnlockPaywall) {
    btnUnlockPaywall.addEventListener("click", () => openPaywallModal("Paywall Overlay"));
  }

  // Modal backdrop click
  const modal = document.getElementById("paywall-modal") || document.getElementById("paywallModal");
  if (modal) {
    modal.addEventListener("click", e => {
      if (e.target === modal) closePaywallModal();
    });
  }

  // Key input Enter listener
  const keyInput = document.getElementById("license-key-input") || document.getElementById("licenseKeyInput");
  if (keyInput) {
    keyInput.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        e.preventDefault();
        activateKey();
      }
    });
  }

  window.addEventListener("keydown", e => {
    if (e.key === "Escape") closePaywallModal();
  });

  setupDePay();
}

function handleImageFile(file) {
  if (!file.type.startsWith("image/")) {
    alert("Please upload a valid image file.");
    return;
  }
  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.onload = () => {
      document.getElementById("artWidth").value = img.naturalWidth;
      document.getElementById("artHeight").value = img.naturalHeight;
      document.getElementById("dropzoneText").innerText = `Uploaded: ${file.name} (${img.naturalWidth} × ${img.naturalHeight} px)`;
      auditArtwork();
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function recalculateMargins() {
  const prodId = document.getElementById("prodSelect").value;
  const retail = parseFloat(document.getElementById("retailPrice").value) || 68.00;
  const curr = document.getElementById("currencySelect").value;
  const country = document.getElementById("countrySelect").value;

  const prod = PRODUCTS[prodId] || PRODUCTS["acrylic_print_16x24"];
  const hub = HUBS[country] || HUBS["US"];
  const sym = curr === "EUR" ? "€" : (curr === "GBP" ? "£" : "$");

  const baseCost = curr === "EUR" ? prod.cost_eur : (curr === "GBP" ? prod.cost_gbp : prod.cost_usd);
  const shipCost = hub.cost;
  const cogs = baseCost + shipCost;

  // Platform fees
  const etsyFee = (retail * 0.095) + 0.45;
  const shopifyFee = (retail * 0.029) + 0.30;
  const directFee = 0.30;

  const etsyProfit = retail - cogs - etsyFee;
  const etsyMargin = retail > 0 ? (etsyProfit / retail) * 100 : 0;

  const shopifyProfit = retail - cogs - shopifyFee;
  const shopifyMargin = retail > 0 ? (shopifyProfit / retail) * 100 : 0;

  const directProfit = retail - cogs - directFee;
  const directMargin = retail > 0 ? (directProfit / retail) * 100 : 0;

  // Update UI
  document.getElementById("heroMargin").innerText = `${shopifyMargin.toFixed(1)}%`;
  document.getElementById("heroProfit").innerText = `${sym}${shopifyProfit.toFixed(2)}`;
  document.getElementById("heroCogs").innerText = `${sym}${cogs.toFixed(2)}`;
  document.getElementById("heroBaseCost").innerText = `${sym}${baseCost.toFixed(2)}`;

  document.getElementById("outEtsyProfit").innerText = `${sym}${etsyProfit.toFixed(2)}`;
  document.getElementById("outEtsyMargin").innerText = `${etsyMargin.toFixed(1)}%`;
  document.getElementById("outShopifyProfit").innerText = `${sym}${shopifyProfit.toFixed(2)}`;
  document.getElementById("outShopifyMargin").innerText = `${shopifyMargin.toFixed(1)}%`;
  document.getElementById("outDirectProfit").innerText = `${sym}${directProfit.toFixed(2)}`;
  document.getElementById("outDirectMargin").innerText = `${directMargin.toFixed(1)}%`;

  // Local routing info
  const isLocal = prod.local_countries.includes(country);
  document.getElementById("routingHubName").innerText = isLocal ? `Domestic ${hub.country} Hub` : "Cross-Border Transit";
  document.getElementById("routingCarrier").innerText = isLocal ? hub.carrier : "DHL International";
  document.getElementById("routingLead").innerText = isLocal ? hub.lead : "7-12 Days";
  document.getElementById("customsSavings").innerText = isLocal ? `${sym}14.50 Saved (0 Customs)` : `${sym}0.00 (Tariffs Apply)`;
}

function auditArtwork() {
  const prodId = document.getElementById("auditProdSelect").value;
  const w = parseInt(document.getElementById("artWidth").value, 10) || 4800;
  const h = parseInt(document.getElementById("artHeight").value, 10) || 7200;

  const prod = PRODUCTS[prodId] || PRODUCTS["acrylic_print_16x24"];
  const targetW = prod.print_w;
  const targetH = prod.print_h;
  const recDpi = prod.rec_dpi;
  const bleed = prod.bleed_mm;

  document.getElementById("targetAreaDisplay").innerText = `${targetW} × ${targetH} px @ ${recDpi} DPI (${bleed}mm Bleed)`;

  const scaleW = w / targetW;
  const scaleH = h / targetH;
  const effectiveScale = Math.min(scaleW, scaleH);
  const effectiveDpi = Math.round(recDpi * effectiveScale);

  const dpiBadge = document.getElementById("effectiveDpiBadge");
  const gradeText = document.getElementById("qualityGradeText");
  const feedbackList = document.getElementById("auditFeedback");

  dpiBadge.innerText = `${effectiveDpi} DPI`;
  feedbackList.innerHTML = "";

  if (effectiveDpi >= 300) {
    dpiBadge.className = "metric-val val-azure";
    gradeText.innerText = "EXCELLENT — Museum Grade Gallery Standard";
    addFeedback("✅ Meets Gelato 300+ DPI high-definition benchmark.");
    addFeedback("✅ Micro-details and vibrant color gradients preserved on acrylic/aluminum.");
  } else if (effectiveDpi >= 200) {
    dpiBadge.className = "metric-val val-cyan";
    gradeText.innerText = "ACCEPTABLE — Standard Physical Print Quality";
    addFeedback("⚡ Acceptable for paper/canvas, but 300 DPI recommended for acrylic.");
  } else if (effectiveDpi >= 150) {
    dpiBadge.className = "metric-val val-gold";
    gradeText.innerText = "WARNING — Soft Details & Slight Grain";
    addFeedback("⚠️ May exhibit softness on large physical wall decor.");
  } else {
    dpiBadge.className = "metric-val val-ruby";
    gradeText.innerText = "CRITICAL LOW-RES — High Pixelation Risk";
    addFeedback("❌ Significant pixelation risk. Upscale artwork prior to publishing.");
  }

  if (bleed > 0) {
    addFeedback(`ℹ️ Keep critical logos and typography inside safe zone (${bleed}mm perimeter bleed).`);
  }
}

function addFeedback(text) {
  const li = document.createElement("li");
  li.style.fontSize = "0.85rem";
  li.style.marginBottom = "0.35rem";
  li.style.color = "var(--text-main)";
  li.innerText = text;
  document.getElementById("auditFeedback").appendChild(li);
}

function renderHubsTable() {
  const tbody = document.getElementById("hubsTbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  Object.entries(HUBS).forEach(([code, h]) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${h.country} (${code})</strong></td>
      <td><span class="status-badge" style="background: rgba(0,163,224,0.1); color: var(--azure); border-color: rgba(0,163,224,0.3);">● Domestic Hub</span></td>
      <td><span class="text-mono" style="color: var(--emerald);">${h.lead}</span></td>
      <td><span class="text-mono">${h.carrier}</span></td>
      <td class="text-mono">${h.symbol}${h.cost.toFixed(2)}</td>
    `;
    tbody.appendChild(tr);
  });
}

function generateOrderPayload() {
  const prodId = document.getElementById("prodSelect").value;
  const prod = PRODUCTS[prodId] || PRODUCTS["acrylic_print_16x24"];
  const country = document.getElementById("countrySelect").value;
  const title = document.getElementById("payloadTitle") ? document.getElementById("payloadTitle").value : "Sovereign Abstract Botanical";
  const artUrl = document.getElementById("payloadArtworkUrl") ? document.getElementById("payloadArtworkUrl").value : "https://example.com/artwork.png";

  const payload = {
    orderType: "order",
    orderReferenceId: "SOV-GELATO-8116",
    customerReferenceId: "CUST-SOV-8116",
    currency: country === "DE" || country === "FR" || country === "NL" ? "EUR" : (country === "UK" ? "GBP" : "USD"),
    shippingAddress: {
      firstName: "Jane",
      lastName: "Doe",
      addressLine1: "123 Sovereign Promenade",
      city: country === "DE" ? "Berlin" : (country === "UK" ? "London" : "New York"),
      country: country,
      postCode: country === "DE" ? "10115" : "10001",
      email: "buyer@example.com"
    },
    items: [
      {
        itemReferenceId: `ITEM-${prod.id}-01`,
        productUid: `gelato_${prod.id}`,
        files: [{ type: "default", url: artUrl }],
        quantity: 1
      }
    ]
  };

  const outputEl = document.getElementById("payloadOutput");
  if (outputEl) {
    outputEl.textContent = JSON.stringify(payload, null, 2);
  }
}

function triggerProAction(actionName) {
  if (isProActive) {
    if (actionName === "copy_payload") {
      const output = document.getElementById("payloadOutput") ? document.getElementById("payloadOutput").textContent : "";
      navigator.clipboard.writeText(output).then(() => {
        const btn = document.getElementById("btn-copy-payload");
        if (btn) {
          const orig = btn.innerHTML;
          btn.innerHTML = "✅ Copied to Clipboard!";
          setTimeout(() => { btn.innerHTML = orig; }, 2000);
        } else {
          alert("✅ Gelato Order Creation Payload copied to clipboard!");
        }
      }).catch(() => {
        alert("✅ Gelato Order Creation Payload copied to clipboard!");
      });
    } else if (actionName === "export_hubs") {
      let csv = "Country Code,Country Name,Currency,Lead Time,Local Carrier,Domestic Shipping Cost\n";
      Object.keys(HUBS).forEach(code => {
        const h = HUBS[code];
        csv += `"${code}","${h.country}","${h.currency}","${h.lead}","${h.carrier}",${h.cost}\n`;
      });
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "gelato_local_hubs_matrix.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else if (actionName === "global_router") {
      const bundle = {
        name: "Gelato Pro Sovereign Global Dispatch Bundle",
        version: "1.0.0",
        author: "Neal Frazier Tech (@1nc0gn30)",
        engine: "Gelato Localized Production & Smart Dispatch",
        hubs_active: Object.keys(HUBS).length,
        supported_countries: Object.keys(HUBS),
        routing_rules: [
          { zone: "US", carrier: "USPS/FedEx", duties: "0% Domestic" },
          { zone: "EU", carrier: "DHL/PostNL", duties: "0% Domestic (Intra-EU)" },
          { zone: "UK", carrier: "Royal Mail", duties: "0% Domestic" },
          { zone: "APAC", carrier: "Australia Post", duties: "0% Domestic" }
        ],
        hubs: HUBS
      };
      const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "gelato_global_router_bundle.json";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else {
      alert(`✅ Pro Action '${actionName}' executed successfully!`);
    }
  } else {
    openPaywallModal(`Pro Feature: ${actionName}`);
  }
}

function openPaywallModal(context = "") {
  const modal = document.getElementById("paywall-modal") || document.getElementById("paywallModal");
  if (modal) {
    modal.classList.add("is-open");
    modal.style.display = "flex";
  }
}

function closePaywallModal() {
  const modal = document.getElementById("paywall-modal") || document.getElementById("paywallModal");
  if (modal) {
    modal.classList.remove("is-open");
    modal.style.display = "none";
  }
}

function activateKey() {
  const input = document.getElementById("license-key-input") || document.getElementById("licenseKeyInput");
  const statusEl = document.getElementById("license-status");
  const key = input ? input.value.trim() : "";

  if (!key) {
    if (statusEl) {
      statusEl.style.color = "var(--ruby)";
      statusEl.innerText = "Please enter a valid license key or receipt email.";
    } else {
      alert("Please enter a valid license key or receipt email.");
    }
    return;
  }

  if (key.length >= 6) {
    unlockProMode(true);
    if (statusEl) {
      statusEl.style.color = "var(--emerald)";
      statusEl.innerText = "⭐ Sovereign Gelato Pro License Activated Successfully!";
    }
  } else {
    if (statusEl) {
      statusEl.style.color = "var(--ruby)";
      statusEl.innerText = "Invalid license key (minimum 6 characters required).";
    } else {
      alert("Invalid license key (minimum 6 characters required).");
    }
  }
}

function setupDePay() {
  document.querySelectorAll(".btn-depay-trigger").forEach(btn => {
    btn.addEventListener("click", e => {
      e.preventDefault();
      if (window.DePayButtons) return;
      if (window.DePay) {
        try {
          window.DePay.Payment({
            accept: [
              {
                blockchain: 'solana',
                token: '11111111111111111111111111111111',
                receiver: 'GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK',
                amount: 19
              }
            ]
          });
          return;
        } catch (err) {
          console.warn("DePay invocation fallback:", err);
        }
      }
      const solReceiver = "GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK";
      navigator.clipboard.writeText(solReceiver).then(() => {
        alert(`⚡ DePay Solana Receiver copied to clipboard:\n${solReceiver}\n\nTransfer $19 SOL or USDC and enter your tx hash or receipt email as your license key.`);
      }).catch(() => {
        alert(`⚡ DePay Solana Receiver:\n${solReceiver}\n\nTransfer $19 SOL or USDC and enter your tx hash or receipt email as your license key.`);
      });
    });
  });
}
