-- Protokollcímek: szám körben + címke, alatta a cím; blokkcímek (Mit tegyél? stb.).
package.path = PANDOC_SCRIPT_FILE:match("(.*/)") .. "?.lua;" .. package.path
local C = require("common")

local BLOCK_LABELS = {
  ["Mit tegyél?"] = true, ["Mit ne tegyél?"] = true,
  ["Hogyan működik?"] = true, ["Gyakori kérdések"] = true,
}

function Header(h)
  local t = C.plain(h.content)
  if h.level == 3 then
    local n, label, title = t:match("^(%d+)%. ([^:]*protokoll): (.+)$")
    if n then
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
  elseif h.level == 4 and BLOCK_LABELS[t] then
    h.classes:insert("block-label")
    return h
  end
end
