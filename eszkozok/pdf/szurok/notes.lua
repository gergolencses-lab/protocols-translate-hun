-- Nyomtatott jegyzetek az eredeti könyv szerint: a szövegben felső indexes szám,
-- fejezetenként újrainduló számozással; maguk a jegyzetek a könyv végi
-- „Jegyzetek” fejezet azonos című alcíme alá kerülnek, oda-vissza linkkel.
-- A többi szűrő ELŐTT kell futnia (a címsorok itt még sima szövegek).
package.path = PANDOC_SCRIPT_FILE:match("(.*/)") .. "../../kozos/szurok/?.lua;" .. package.path
local C = require("common")

local ACCENTS = { ["á"]="a", ["é"]="e", ["í"]="i", ["ó"]="o", ["ö"]="o", ["ő"]="o",
                  ["ú"]="u", ["ü"]="u", ["ű"]="u",
                  ["Á"]="a", ["É"]="e", ["Í"]="i", ["Ó"]="o", ["Ö"]="o", ["Ő"]="o",
                  ["Ú"]="u", ["Ü"]="u", ["Ű"]="u" }

-- Locale-független: macOS-en a Python által beállított LC_CTYPE=UTF-8 mellett a
-- lower() és a %w bájtonként Latin-1-ként kezeli az UTF-8 ékezeteket, és elrontja őket.
local function chapter_key(title)
  local n = title:match("^(%d+)%. fejezet")
  if n then return string.format("c%02d", tonumber(n)) end
  local s = title
  for k, v in pairs(ACCENTS) do s = s:gsub(k, v) end
  s = s:gsub("[A-Z]", string.lower)
  return (s:gsub("[^a-z0-9]+", "-"):gsub("^-+", ""):gsub("-+$", ""))
end

function Pandoc(doc)
  local notes, order = {}, {}      -- notes[title] = { {key, n, blocks}, ... }
  local title, key, count = nil, nil, 0

  -- 1. menet: a jegyzetek cseréje hivatkozásra, fejezetenként számozva.
  for i, blk in ipairs(doc.blocks) do
    if blk.t == "Header" and blk.level == 2 then
      title = C.plain(blk.content)
      key, count = chapter_key(title), 0
    elseif title then
      doc.blocks[i] = blk:walk({
        Note = function(note)
          count = count + 1
          local id = key .. "-" .. count
          if not notes[title] then notes[title] = {}; table.insert(order, title) end
          table.insert(notes[title], { id = id, n = count, blocks = note.content })
          return pandoc.Superscript({
            pandoc.Link({ pandoc.Str(tostring(count)) }, "#n-" .. id, "",
                        { id = "r-" .. id, class = "noteref" })
          })
        end,
      })
    end
  end

  local function note_list(list)
    local divs = {}
    for _, nt in ipairs(list) do
      local blocks = nt.blocks:clone()
      local back = { pandoc.Link({ pandoc.Str(nt.n .. ".") }, "#r-" .. nt.id, "", { class = "backref" }),
                     pandoc.Space() }
      if blocks[1] and (blocks[1].t == "Para" or blocks[1].t == "Plain") then
        blocks[1] = pandoc.Para(back .. blocks[1].content)
      else
        table.insert(blocks, 1, pandoc.Para(back))
      end
      table.insert(divs, pandoc.Div(blocks, { id = "n-" .. nt.id, class = "note" }))
    end
    return pandoc.Div(divs, { class = "notes-list" })
  end

  -- 2. menet: a jegyzetek beillesztése a Jegyzetek fejezet alcímei alá.
  local out, in_notes, placed = {}, false, {}
  local function flush_unplaced()
    for _, t in ipairs(order) do
      if not placed[t] then
        io.stderr:write("notes.lua: nincs alcím a Jegyzetekben: " .. t .. "\n")
        table.insert(out, pandoc.Header(3, pandoc.Inlines(t), { class = "notes-chapter" }))
        table.insert(out, note_list(notes[t]))
        placed[t] = true
      end
    end
  end
  for _, blk in ipairs(doc.blocks) do
    if blk.t == "Header" and blk.level == 2 then
      if in_notes then flush_unplaced() end
      in_notes = C.plain(blk.content) == "Jegyzetek"
      if in_notes then blk.identifier = "jegyzetek"; blk.classes:insert("notes-title") end
      table.insert(out, blk)
    elseif in_notes and blk.t == "Header" and blk.level == 3 then
      local t = C.plain(blk.content)
      blk.classes:insert("notes-chapter")
      table.insert(out, blk)
      if notes[t] then table.insert(out, note_list(notes[t])); placed[t] = true end
    else
      table.insert(out, blk)
    end
  end
  if in_notes then flush_unplaced() end
  doc.blocks = out
  return doc
end
