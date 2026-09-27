-- Félkövér alcím-bekezdések (pl. **MIELŐTT KELET FELÉ UTAZOL**): a forrásban sima
-- bekezdések, ezért a tördelő a lap aljára hagyhatná őket. Div.run-head-be
-- csomagoljuk, amelyet a CSS a következő bekezdéssel együtt tart.
-- A sidebar.lua UTÁN kell futnia (a dobozcímek már Div.sidebar-title-ben vannak).
local function is_run_head(blk)
  if blk.t ~= "Para" then return false end
  local c = blk.content
  local n = #c
  while n > 0 and (c[n].t == "Space" or c[n].t == "SoftBreak") do n = n - 1 end
  return n == 1 and c[1].t == "Strong"
end

local function process(blocks)
  for i, blk in ipairs(blocks) do
    if is_run_head(blk) then
      blocks[i] = pandoc.Div({ blk }, { class = "run-head" })
    elseif blk.t == "Div" and not blk.classes:includes("sidebar-title") then
      process(blk.content)
    end
  end
end

function Pandoc(doc)
  process(doc.blocks)
  return doc
end
