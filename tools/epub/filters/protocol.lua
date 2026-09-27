-- Protokollcímek: szám körben + címke, alatta a cím; blokkcímek (Mit tegyél? stb.).
-- A protokollon kívüli 3. szintű szakaszok (pl. „Mi az edzés?”) és alcímeik egy
-- szinttel lejjebb kerülnek: így a --split-level=2 csak fejezetnél és protokollnál
-- bont fájlt, a tartalomjegyzék pedig – mint az eredetiben – csak ezeket listázza.
package.path = PANDOC_SCRIPT_FILE:match("(.*/)") .. "?.lua;" .. package.path
local C = require("common")

local BLOCK_LABELS = {
  ["Mit tegyél?"] = true, ["Mit ne tegyél?"] = true,
  ["Hogyan működik?"] = true, ["Gyakori kérdések"] = true,
}

local function protocol_header(h, t)
  local n, label, title = t:match("^(%d+)%. ([^:]*protokoll): (.+)$")
  if not n then return nil end
  h.classes:insert("protocol")
  -- Magyar sorrend: „1. alvásprotokoll: Cím”. A szöveg változatlan (tartalomjegyzék),
  -- a CSS a „. ” és „: ” elválasztót elrejti, a számot körbe teszi.
  h.content = {
    C.span(n, "protocol-num"),
    C.span(". ", "sep"),
    C.span(label, "protocol-label"),
    C.span(": ", "sep"),
    C.span(title, "protocol-title"),
  }
  return h
end

function Pandoc(doc)
  local demote = false -- egy protokollon kívüli 3. szintű szakaszon belül vagyunk
  for _, blk in ipairs(doc.blocks) do
    if blk.t == "Header" then
      local t = C.plain(blk.content)
      if blk.level <= 2 then
        demote = false
      elseif blk.level == 3 then
        if protocol_header(blk, t) then
          demote = false
        else
          demote = true
          blk.level = 4
          blk.classes:insert("section-head")
        end
      elseif demote then
        blk.level = blk.level + 1
      elseif blk.level == 4 and BLOCK_LABELS[t] then
        blk.classes:insert("block-label")
      end
    end
  end
  return doc
end
