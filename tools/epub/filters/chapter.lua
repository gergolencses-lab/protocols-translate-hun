-- Fejezetnyitók, embléma, szerzőfotó, epub:type a front/back matterhez.
package.path = PANDOC_SCRIPT_FILE:match("(.*/)") .. "?.lua;" .. package.path
local C = require("common")

local EPUB_TYPES = {
  ["Ajánlás"] = "dedication",
  ["Bevezetés"] = "introduction",
  ["Köszönetnyilvánítás"] = "acknowledgments",
  ["Copyright"] = "copyright-page",
}

function Header(h)
  if h.level ~= 2 then return nil end
  local t = C.plain(h.content)
  local n, title = t:match("^(%d+)%. fejezet: (.+)$")
  if n then
    h.classes:insert("chapter-opener")
    h.attributes["epub:type"] = "chapter"
    -- A szöveg változatlan marad („1. fejezet: Alvásprotokollok”), így a
    -- tartalomjegyzékben is ez látszik; a tagolást a CSS végzi.
    h.content = {
      C.span(n .. ". fejezet", "chapter-label"),
      C.span(": ", "sep"),
      C.span(title, "chapter-title"),
    }
    return h
  end
  if EPUB_TYPES[t] then
    h.attributes["epub:type"] = EPUB_TYPES[t]
    -- Az ajánlás oldalán az eredetiben nincs cím; a tartalomjegyzékben megmarad.
    if t == "Ajánlás" then h.classes:insert("no-title") end
    return h
  end
end

local function sole_image(blk)
  if (blk.t == "Para" or blk.t == "Plain") and #blk.content == 1 and blk.content[1].t == "Image" then
    return blk.content[1]
  end
end

function Para(p)
  local img = sole_image(p)
  if not img then return nil end
  if img.src:match("chapter%-emblem") then
    return pandoc.Div({ pandoc.Plain({ img }) }, { class = "emblem" })
  elseif img.src:match("andrew%-huberman") then
    return pandoc.Div({ pandoc.Plain({ img }) }, { class = "author-photo" })
  end
end
