/* Maiko Kachkachishvili site — backend API (Neon Function)
   Routes:
     POST /register            — public: academy registration
     POST /message             — public: collaboration/contact form
     POST /admin/login         — {password} -> {token}
     POST /admin/password      — change admin password (auth)
     GET  /admin/stats         — dashboard counts (auth)
     GET  /admin/registrations — list w/ ?status=&q=&limit=&offset= (auth)
     PATCH /admin/registrations/:id — {status, admin_note} (auth)
     GET  /admin/messages      — list (auth)
     PATCH /admin/messages/:id — {status, admin_note} (auth)
     GET  /admin/export?type=registrations|messages&token= — CSV download (auth)
*/
import crypto from "node:crypto";

/* SQL over Neon's HTTP endpoint — no driver dependency needed */
const DB_URL = process.env.DATABASE_URL;
const DB_HOST = DB_URL ? new URL(DB_URL.replace(/^postgres(ql)?:/, "https:")).hostname : "";
async function q(query, params = []) {
  const res = await fetch(`https://${DB_HOST}/sql`, {
    method: "POST",
    headers: { "Neon-Connection-String": DB_URL, "Content-Type": "application/json" },
    body: JSON.stringify({ query, params }),
  });
  const data = await res.json();
  if (!res.ok || data.message) throw new Error(data.message || `sql http ${res.status}`);
  return data;
}
const pool = { query: q };

const SECRET = process.env.SESSION_SECRET || "dev-secret";
const TOKEN_TTL_MS = 1000 * 60 * 60 * 12; // 12h sessions

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS, ...headers },
  });

/* ---------- password hashing (scrypt) ---------- */
function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.scryptSync(password, salt, 64).toString("hex");
  return `${salt}:${hash}`;
}
function verifyPassword(password, stored) {
  const [salt, hash] = String(stored).split(":");
  if (!salt || !hash) return false;
  const candidate = crypto.scryptSync(password, salt, 64);
  const expected = Buffer.from(hash, "hex");
  return candidate.length === expected.length && crypto.timingSafeEqual(candidate, expected);
}

/* ---------- session tokens (HMAC) ---------- */
function signToken() {
  const payload = Buffer.from(JSON.stringify({ exp: Date.now() + TOKEN_TTL_MS })).toString("base64url");
  const sig = crypto.createHmac("sha256", SECRET).update(payload).digest("base64url");
  return `${payload}.${sig}`;
}
function verifyToken(token) {
  if (!token) return false;
  const [payload, sig] = String(token).split(".");
  if (!payload || !sig) return false;
  const expect = crypto.createHmac("sha256", SECRET).update(payload).digest("base64url");
  if (sig.length !== expect.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expect))) return false;
  try {
    return JSON.parse(Buffer.from(payload, "base64url").toString()).exp > Date.now();
  } catch {
    return false;
  }
}
function authed(request, url) {
  const h = request.headers.get("Authorization") || "";
  const token = h.startsWith("Bearer ") ? h.slice(7) : url.searchParams.get("token");
  return verifyToken(token);
}

/* ---------- helpers ---------- */
const clean = (v, max = 500) => String(v ?? "").trim().slice(0, max);

async function getAdminHash() {
  const { rows } = await pool.query("SELECT value FROM admin_settings WHERE key='admin_password'");
  return rows[0]?.value || null;
}

function csv(rows, columns) {
  const esc = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;
  const head = columns.map((c) => esc(c.label)).join(",");
  const body = rows.map((r) => columns.map((c) => esc(r[c.key])).join(",")).join("\n");
  return "﻿" + head + "\n" + body; // BOM so Excel opens Georgian text correctly
}

const DIRECTIONS = ["group_vocal", "individual_vocal", "folk_song", "piano", "composition", "other"];
const REG_STATUSES = ["new", "contacted", "enrolled", "rejected", "archived"];
const MSG_STATUSES = ["new", "read", "replied", "archived"];

/* ---------- handler ---------- */
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    const method = request.method;

    if (method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });

    try {
      /* ---------- public: registration ---------- */
      if (method === "POST" && path === "/register") {
        const b = await request.json().catch(() => ({}));
        if (clean(b.website)) return json({ ok: true }); // honeypot: pretend success
        const full_name = clean(b.full_name, 200);
        const age = parseInt(b.age, 10);
        const parent_full_name = clean(b.parent_full_name, 200) || null;
        const phone = clean(b.phone, 40);
        const address = clean(b.address, 300);
        const direction = clean(b.direction, 40);
        const consent = b.consent === true || b.consent === "1" || b.consent === "on";

        if (!full_name || !phone || !address) return json({ ok: false, error: "შეავსეთ ყველა სავალდებულო ველი" }, 422);
        if (!Number.isInteger(age) || age < 3 || age > 100) return json({ ok: false, error: "ასაკი არასწორია" }, 422);
        if (age < 18 && !parent_full_name) return json({ ok: false, error: "მიუთითეთ მშობლის სახელი და გვარი" }, 422);
        if (!DIRECTIONS.includes(direction)) return json({ ok: false, error: "აირჩიეთ მიმართულება" }, 422);
        if (!consent) return json({ ok: false, error: "საჭიროა თანხმობა მონაცემების დამუშავებაზე" }, 422);

        await pool.query(
          `INSERT INTO registrations (full_name, age, parent_full_name, phone, address, direction, consent)
           VALUES ($1,$2,$3,$4,$5,$6,$7)`,
          [full_name, age, parent_full_name, phone, address, direction, consent]
        );
        return json({ ok: true });
      }

      /* ---------- public: contact message ---------- */
      if (method === "POST" && path === "/message") {
        const b = await request.json().catch(() => ({}));
        if (clean(b.website)) return json({ ok: true });
        const name_surname = clean(b.name_surname, 200);
        const email = clean(b.email, 200);
        const phone = clean(b.phone, 40);
        const subject = clean(b.subject, 300);
        const message = clean(b.message, 5000);
        if (!name_surname || !email || !phone || !subject || !message)
          return json({ ok: false, error: "შეავსეთ ყველა სავალდებულო ველი" }, 422);
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email))
          return json({ ok: false, error: "ელფოსტა არასწორია" }, 422);
        await pool.query(
          `INSERT INTO messages (name_surname, email, phone, subject, message) VALUES ($1,$2,$3,$4,$5)`,
          [name_surname, email, phone, subject, message]
        );
        return json({ ok: true });
      }

      /* ---------- admin: login ---------- */
      if (method === "POST" && path === "/admin/login") {
        const b = await request.json().catch(() => ({}));
        const stored = await getAdminHash();
        if (!stored || !verifyPassword(String(b.password || ""), stored)) {
          await new Promise((r) => setTimeout(r, 400)); // slow brute force
          return json({ ok: false, error: "პაროლი არასწორია" }, 401);
        }
        return json({ ok: true, token: signToken() });
      }

      /* ---------- admin routes below require auth ---------- */
      if (path.startsWith("/admin/")) {
        if (!authed(request, url)) return json({ ok: false, error: "unauthorized" }, 401);
      }

      if (method === "POST" && path === "/admin/password") {
        const b = await request.json().catch(() => ({}));
        const stored = await getAdminHash();
        if (!stored || !verifyPassword(String(b.old_password || ""), stored))
          return json({ ok: false, error: "ძველი პაროლი არასწორია" }, 401);
        const next = String(b.new_password || "");
        if (next.length < 8) return json({ ok: false, error: "ახალი პაროლი მინიმუმ 8 სიმბოლო" }, 422);
        await pool.query(
          `INSERT INTO admin_settings (key, value, updated_at) VALUES ('admin_password',$1,now())
           ON CONFLICT (key) DO UPDATE SET value=$1, updated_at=now()`,
          [hashPassword(next)]
        );
        return json({ ok: true });
      }

      if (method === "GET" && path === "/admin/stats") {
        const [r1, r2, r3, r4] = await Promise.all([
          pool.query("SELECT status, count(*)::int AS n FROM registrations GROUP BY status"),
          pool.query("SELECT status, count(*)::int AS n FROM messages GROUP BY status"),
          pool.query("SELECT count(*)::int AS n FROM registrations WHERE created_at > now() - interval '7 days'"),
          pool.query("SELECT direction, count(*)::int AS n FROM registrations GROUP BY direction ORDER BY n DESC"),
        ]);
        return json({
          ok: true,
          registrations: Object.fromEntries(r1.rows.map((r) => [r.status, r.n])),
          messages: Object.fromEntries(r2.rows.map((r) => [r.status, r.n])),
          last7days: r3.rows[0].n,
          byDirection: r4.rows,
        });
      }

      if (method === "GET" && path === "/admin/registrations") {
        const status = url.searchParams.get("status");
        const q = clean(url.searchParams.get("q"), 100);
        const limit = Math.min(parseInt(url.searchParams.get("limit") || "50", 10) || 50, 200);
        const offset = parseInt(url.searchParams.get("offset") || "0", 10) || 0;
        const where = [];
        const params = [];
        if (status && REG_STATUSES.includes(status)) { params.push(status); where.push(`status = $${params.length}`); }
        if (q) { params.push(`%${q}%`); where.push(`(full_name ILIKE $${params.length} OR phone ILIKE $${params.length} OR address ILIKE $${params.length})`); }
        const w = where.length ? "WHERE " + where.join(" AND ") : "";
        const total = (await pool.query(`SELECT count(*)::int AS n FROM registrations ${w}`, params)).rows[0].n;
        params.push(limit, offset);
        const { rows } = await pool.query(
          `SELECT * FROM registrations ${w} ORDER BY created_at DESC LIMIT $${params.length - 1} OFFSET $${params.length}`,
          params
        );
        return json({ ok: true, total, rows });
      }

      let m = path.match(/^\/admin\/registrations\/(\d+)$/);
      if (method === "PATCH" && m) {
        const b = await request.json().catch(() => ({}));
        const sets = [];
        const params = [];
        if (b.status !== undefined) {
          if (!REG_STATUSES.includes(b.status)) return json({ ok: false, error: "bad status" }, 422);
          params.push(b.status); sets.push(`status = $${params.length}`);
        }
        if (b.admin_note !== undefined) { params.push(clean(b.admin_note, 2000)); sets.push(`admin_note = $${params.length}`); }
        if (!sets.length) return json({ ok: false, error: "nothing to update" }, 422);
        params.push(m[1]);
        await pool.query(`UPDATE registrations SET ${sets.join(", ")}, updated_at = now() WHERE id = $${params.length}`, params);
        return json({ ok: true });
      }

      if (method === "GET" && path === "/admin/messages") {
        const status = url.searchParams.get("status");
        const q = clean(url.searchParams.get("q"), 100);
        const limit = Math.min(parseInt(url.searchParams.get("limit") || "50", 10) || 50, 200);
        const offset = parseInt(url.searchParams.get("offset") || "0", 10) || 0;
        const where = [];
        const params = [];
        if (status && MSG_STATUSES.includes(status)) { params.push(status); where.push(`status = $${params.length}`); }
        if (q) { params.push(`%${q}%`); where.push(`(name_surname ILIKE $${params.length} OR email ILIKE $${params.length} OR subject ILIKE $${params.length})`); }
        const w = where.length ? "WHERE " + where.join(" AND ") : "";
        const total = (await pool.query(`SELECT count(*)::int AS n FROM messages ${w}`, params)).rows[0].n;
        params.push(limit, offset);
        const { rows } = await pool.query(
          `SELECT * FROM messages ${w} ORDER BY created_at DESC LIMIT $${params.length - 1} OFFSET $${params.length}`,
          params
        );
        return json({ ok: true, total, rows });
      }

      m = path.match(/^\/admin\/messages\/(\d+)$/);
      if (method === "PATCH" && m) {
        const b = await request.json().catch(() => ({}));
        const sets = [];
        const params = [];
        if (b.status !== undefined) {
          if (!MSG_STATUSES.includes(b.status)) return json({ ok: false, error: "bad status" }, 422);
          params.push(b.status); sets.push(`status = $${params.length}`);
        }
        if (b.admin_note !== undefined) { params.push(clean(b.admin_note, 2000)); sets.push(`admin_note = $${params.length}`); }
        if (!sets.length) return json({ ok: false, error: "nothing to update" }, 422);
        params.push(m[1]);
        await pool.query(`UPDATE messages SET ${sets.join(", ")}, updated_at = now() WHERE id = $${params.length}`, params);
        return json({ ok: true });
      }

      if (method === "GET" && path === "/admin/export") {
        const type = url.searchParams.get("type") === "messages" ? "messages" : "registrations";
        if (type === "registrations") {
          const { rows } = await pool.query("SELECT * FROM registrations ORDER BY created_at DESC");
          const body = csv(rows, [
            { key: "id", label: "ID" },
            { key: "full_name", label: "სახელი გვარი" },
            { key: "age", label: "ასაკი" },
            { key: "parent_full_name", label: "მშობელი" },
            { key: "phone", label: "ტელეფონი" },
            { key: "address", label: "მისამართი" },
            { key: "direction", label: "მიმართულება" },
            { key: "status", label: "სტატუსი" },
            { key: "admin_note", label: "შენიშვნა" },
            { key: "created_at", label: "თარიღი" },
          ]);
          return new Response(body, {
            headers: { ...CORS, "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": "attachment; filename=registrations.csv" },
          });
        }
        const { rows } = await pool.query("SELECT * FROM messages ORDER BY created_at DESC");
        const body = csv(rows, [
          { key: "id", label: "ID" },
          { key: "name_surname", label: "სახელი გვარი" },
          { key: "email", label: "ელფოსტა" },
          { key: "phone", label: "ტელეფონი" },
          { key: "subject", label: "თემა" },
          { key: "message", label: "შეტყობინება" },
          { key: "status", label: "სტატუსი" },
          { key: "created_at", label: "თარიღი" },
        ]);
        return new Response(body, {
          headers: { ...CORS, "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": "attachment; filename=messages.csv" },
        });
      }

      if (method === "GET" && path === "/") return json({ ok: true, service: "maiko-site-api" });
      return json({ ok: false, error: "not found" }, 404);
    } catch (e) {
      console.error("handler error:", e);
      return json({ ok: false, error: "server error" }, 500);
    }
  },
};
