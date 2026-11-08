"use strict";

const PAGE_SIZE = 100;
const DATA_BASE = new URL("data/", document.baseURI);
const TRUSTED_MERKLE_ROOT = "aaa1c91c06f8950ff53347e1efe67bcd2cbc1751fa827d0f9225ccfb69eca0d6";
const elements = Object.fromEntries(
  [
    "record-count", "prime-count", "composite-count", "merkle-root",
    "part-select", "load-part", "download-part", "query", "search-all",
    "status", "results", "previous", "next", "page-label", "part-sha",
  ].map((id) => [
    id.replace(/-([a-z])/g, (_match, letter) => letter.toUpperCase()),
    document.getElementById(id),
  ]),
);

let manifest;
let visibleRecords = [];
let currentPage = 0;
let currentPart;

function setStatus(message) {
  elements.status.textContent = message;
}

function addCell(row, value) {
  const cell = document.createElement("td");
  cell.textContent = value;
  row.append(cell);
}

async function sha256(bytes) {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
}

function fromHex(value) {
  return Uint8Array.from(value.match(/.{2}/g), (byte) => Number.parseInt(byte, 16));
}

function toHex(bytes) {
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function verifyManifestRoot(parts) {
  let level = await Promise.all(parts.map(async (part) => {
    const leaf = new Uint8Array(1 + 32);
    leaf[0] = 0;
    leaf.set(fromHex(part.sha256), 1);
    return sha256(leaf);
  }));
  while (level.length > 1) {
    if (level.length % 2) level.push(level[level.length - 1]);
    const parents = [];
    for (let index = 0; index < level.length; index += 2) {
      const node = new Uint8Array(1 + 64);
      node[0] = 1;
      node.set(level[index], 1);
      node.set(level[index + 1], 33);
      parents.push(sha256(node));
    }
    level = await Promise.all(parents);
  }
  return toHex(level[0]);
}

function showPage() {
  const start = currentPage * PAGE_SIZE;
  const records = visibleRecords.slice(start, start + PAGE_SIZE);
  elements.results.replaceChildren();
  for (const fields of records) {
    const row = document.createElement("tr");
    for (const field of fields) addCell(row, field);
    elements.results.append(row);
  }
  const pageCount = Math.max(1, Math.ceil(visibleRecords.length / PAGE_SIZE));
  elements.pageLabel.textContent = `Page ${currentPage + 1} / ${pageCount} — ${visibleRecords.length.toLocaleString("fr-CA")} résultats`;
  elements.previous.disabled = currentPage === 0;
  elements.next.disabled = currentPage + 1 >= pageCount;
}

async function fetchVerifiedPart(part) {
  const response = await fetch(new URL(part.file, DATA_BASE));
  if (!response.ok) throw new Error(`Téléchargement impossible : ${part.file} (${response.status})`);
  const bytes = new Uint8Array(await response.arrayBuffer());
  const actualHash = toHex(await sha256(bytes));
  if (actualHash !== part.sha256) throw new Error(`SHA-256 invalide pour ${part.file}`);
  if (typeof DecompressionStream === "undefined") throw new Error("Ce navigateur ne prend pas en charge la décompression gzip sécurisée.");
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
  const text = await new Response(stream).text();
  const rows = text.trimEnd().split("\n").map((line) => line.split("\t"));
  if (rows.length !== part.count || rows.some((row) => row.length !== 4)) {
    throw new Error(`Nombre ou format de lignes invalide dans ${part.file}`);
  }
  return rows;
}

async function loadPart() {
  currentPart = manifest.parts[Number(elements.partSelect.value)];
  elements.downloadPart.href = new URL(currentPart.file, DATA_BASE);
  elements.downloadPart.download = currentPart.file;
  elements.partSha.textContent = currentPart.sha256;
  setStatus(`Téléchargement et vérification SHA-256 de ${currentPart.file}…`);
  elements.loadPart.disabled = true;
  try {
    visibleRecords = await fetchVerifiedPart(currentPart);
    currentPage = 0;
    showPage();
    setStatus(`${currentPart.count.toLocaleString("fr-CA")} ancrages du fragment vérifiés et affichés.`);
  } catch (error) {
    setStatus(error.message);
    throw error;
  } finally {
    elements.loadPart.disabled = false;
  }
}

async function searchAllParts() {
  const query = elements.query.value.trim();
  if (!query) {
    setStatus("Saisissez une ancre numérique ou un identifiant de rapport.");
    return;
  }
  elements.searchAll.disabled = true;
  elements.loadPart.disabled = true;
  elements.results.replaceChildren();
  const matches = [];
  try {
    for (let index = 0; index < manifest.parts.length; index += 1) {
      const part = manifest.parts[index];
      setStatus(`Recherche exacte : fragment ${index + 1}/${manifest.parts.length}…`);
      const records = await fetchVerifiedPart(part);
      for (const record of records) {
        if (record[0] === query || record[2] === query) matches.push(record);
      }
    }
    visibleRecords = matches;
    currentPage = 0;
    showPage();
    setStatus(`${matches.length.toLocaleString("fr-CA")} correspondance(s); tous les fragments ont été vérifiés.`);
  } catch (error) {
    setStatus(error.message);
    throw error;
  } finally {
    elements.searchAll.disabled = false;
    elements.loadPart.disabled = false;
  }
}

async function initialize() {
  try {
    const response = await fetch(new URL("data/manifest.json", document.baseURI));
    if (!response.ok) throw new Error(`Manifeste indisponible (${response.status})`);
    manifest = await response.json();
    const root = await verifyManifestRoot(manifest.parts);
    if (root !== TRUSTED_MERKLE_ROOT || manifest.merkle_root !== TRUSTED_MERKLE_ROOT) {
      throw new Error("La racine de Merkle du manifeste ne correspond pas à celle publiée dans le document.");
    }
    elements.recordCount.textContent = manifest.records.toLocaleString("fr-CA");
    elements.primeCount.textContent = manifest.primes_proven.toLocaleString("fr-CA");
    elements.compositeCount.textContent = manifest.composites.toLocaleString("fr-CA");
    elements.merkleRoot.textContent = manifest.merkle_root;
    for (const [index, part] of manifest.parts.entries()) {
      const option = document.createElement("option");
      option.value = String(index);
      option.textContent = `Fragment ${String(part.number).padStart(2, "0")} — ${part.count.toLocaleString("fr-CA")} ancrages`;
      elements.partSelect.append(option);
    }
    await loadPart();
  } catch (error) {
    setStatus(error.message);
  }
}

elements.loadPart.addEventListener("click", () => loadPart().catch(() => {}));
elements.searchAll.addEventListener("click", () => searchAllParts().catch(() => {}));
elements.previous.addEventListener("click", () => { currentPage -= 1; showPage(); });
elements.next.addEventListener("click", () => { currentPage += 1; showPage(); });
elements.partSelect.addEventListener("change", () => loadPart().catch(() => {}));
elements.query.addEventListener("keydown", (event) => {
  if (event.key === "Enter") searchAllParts().catch(() => {});
});

initialize();
