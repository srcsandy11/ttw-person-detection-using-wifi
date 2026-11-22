"use strict";

const builtIn = {
  source: "simulated",
  rooms: [
    { id: "room-a", name: "Room A" },
    { id: "room-b", name: "Room B" },
  ],
  readings: [false, false, true, false, true, true, false, true, false, false].map((occupied, index) => ({
    room_id: index % 2 === 0 ? "room-a" : "room-b",
    observed_at: new Date(Date.UTC(2026, 0, 1, 9, Math.floor(index / 2))).toISOString(),
    occupied,
  })),
};

function parseReplay(raw) {
  if (!raw || !["simulated", "model"].includes(raw.source)) {
    throw new Error("Set source to simulated or model.");
  }
  if (!Array.isArray(raw.rooms) || raw.rooms.length !== 2 ||
      raw.rooms.some(room => !room || typeof room.id !== "string" || !room.id.trim() ||
        typeof room.name !== "string" || !room.name.trim()) ||
      new Set(raw.rooms.map(room => room.id)).size !== 2) {
    throw new Error("Provide exactly two rooms with distinct IDs and nonempty names.");
  }
  if (!Array.isArray(raw.readings) || raw.readings.length === 0) {
    throw new Error("Provide at least one reading.");
  }
  const roomById = new Map(raw.rooms.map(room => [room.id, room]));
  const timestampsByRoom = new Map(raw.rooms.map(room => [room.id, new Set()]));
  const readings = raw.readings.map((reading, index) => {
    const time = typeof reading?.observed_at === "string" ? Date.parse(reading.observed_at) : NaN;
    if (!roomById.has(reading?.room_id) || typeof reading?.occupied !== "boolean" ||
        !Number.isFinite(time) || !/T.+(?:Z|[+-]\d{2}:\d{2})$/.test(reading.observed_at)) {
      throw new Error(`Reading ${index + 1} needs a known room, an ISO timestamp with a time zone, and a boolean occupied value.`);
    }
    const probability = reading.occupancy_probability;
    if (probability != null && (typeof probability !== "number" || !Number.isFinite(probability) ||
        probability < 0 || probability > 1)) {
      throw new Error(`Reading ${index + 1} has an occupancy probability outside 0–1.`);
    }
    const roomTimes = timestampsByRoom.get(reading.room_id);
    if (roomTimes.has(time)) {
      throw new Error(`Reading ${index + 1} repeats a timestamp for the same room.`);
    }
    roomTimes.add(time);
    return { ...reading, time };
  }).sort((a, b) => a.time - b.time);
  const frames = [];
  const latest = new Map();
  readings.forEach((reading, index) => {
    latest.set(reading.room_id, reading);
    if (readings[index + 1]?.time !== reading.time) {
      frames.push({ time: reading.time, latest: new Map(latest), endIndex: index + 1 });
    }
  });
  return { source: raw.source, rooms: raw.rooms, roomById, readings, frames };
}

const view = Object.fromEntries(
  ["source", "description", "file", "file-error", "play", "reset", "time", "position", "first-time", "last-time", "rooms", "history"]
    .map(id => [id, document.getElementById(id)]),
);
const timeFormat = new Intl.DateTimeFormat("en-GB", {
  year: "numeric", month: "short", day: "numeric",
  hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: "UTC",
});
const probabilityFormat = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 1 });
let replay;
let timer;
let loadSequence = 0;

function formatTime(time) {
  return `${timeFormat.format(time)} UTC`;
}

function state(reading) {
  if (!reading) return "No reading";
  return reading.occupied ? "Occupied" : "Vacant";
}

function probability(reading) {
  return reading?.occupancy_probability == null ? "—" : probabilityFormat.format(reading.occupancy_probability);
}

function stop() {
  clearInterval(timer);
  timer = undefined;
  view.play.textContent = "Play";
}

function element(tag, value, className) {
  const node = document.createElement(tag);
  node.textContent = value;
  if (className) node.className = className;
  return node;
}

function render() {
  const frame = replay.frames[Number(view.position.value)];
  view.time.textContent = formatTime(frame.time);
  view.position.setAttribute("aria-valuetext", view.time.textContent);
  view.rooms.replaceChildren(...replay.rooms.map(room => {
    const reading = frame.latest.get(room.id);
    const card = element("article", "", "room");
    const stateClass = reading ? state(reading).toLowerCase() : "unknown";
    card.append(element("h2", room.name), element("div", state(reading), `state ${stateClass}`));
    if (reading) {
      card.append(element("p", `Last reading ${formatTime(reading.time)}`));
      if (reading.occupancy_probability != null) {
        card.append(element("p", `Occupancy probability ${probability(reading)}`));
      }
    }
    return card;
  }));
  const startIndex = Math.max(0, frame.endIndex - 8);
  const rows = replay.readings.slice(startIndex, frame.endIndex).reverse().map(reading => {
    const row = document.createElement("tr");
    row.append(
      element("td", formatTime(reading.time)),
      element("td", replay.roomById.get(reading.room_id).name),
      element("td", state(reading), state(reading).toLowerCase()),
      element("td", probability(reading)),
    );
    return row;
  });
  view.history.replaceChildren(...rows);
}

function showReplay(raw, isBuiltIn = false) {
  const validReplay = parseReplay(raw);
  stop();
  replay = validReplay;
  view.source.textContent = isBuiltIn ? "Simulator" : replay.source === "simulated" ? "Simulated replay" : "Model replay";
  view.description.textContent = isBuiltIn
    ? "Two rooms with simulated occupancy readings."
    : replay.source === "simulated"
      ? "Two rooms replaying simulated occupancy readings."
      : "Two rooms replaying recorded model predictions.";
  view.position.max = String(replay.frames.length - 1);
  view.position.value = "0";
  view.play.disabled = replay.frames.length === 1;
  view["first-time"].textContent = formatTime(replay.frames[0].time);
  view["last-time"].textContent = formatTime(replay.frames.at(-1).time);
  render();
}

view.play.addEventListener("click", () => {
  if (timer !== undefined) {
    stop();
    return;
  }
  if (view.position.value === view.position.max) {
    view.position.value = "0";
    render();
  }
  view.play.textContent = "Pause";
  timer = setInterval(() => {
    view.position.value = String(Number(view.position.value) + 1);
    render();
    if (view.position.value === view.position.max) stop();
  }, 1000);
});
view.reset.addEventListener("click", () => {
  stop();
  view.position.value = "0";
  render();
});
view.position.addEventListener("input", () => {
  stop();
  render();
});
view.file.addEventListener("change", async () => {
  const file = view.file.files[0];
  view.file.value = "";
  if (!file) return;
  const sequence = ++loadSequence;
  try {
    const raw = JSON.parse(await file.text());
    if (sequence !== loadSequence) return;
    showReplay(raw);
    view["file-error"].hidden = true;
  } catch (error) {
    if (sequence !== loadSequence) return;
    view["file-error"].textContent = `Could not open replay. ${error.message}`;
    view["file-error"].hidden = false;
  }
});

showReplay(builtIn, true);
