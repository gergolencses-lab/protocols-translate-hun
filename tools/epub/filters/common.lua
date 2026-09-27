-- Közös segédfüggvények. A szűrők a --shift-heading-level-by ELŐTTI szinteket
-- látják: fejezet = 2, protokoll = 3, blokkcím = 4.
local M = {}

-- A címsor szövege, a kötött szóközt és a lágy elválasztójelet normál alakra hozva.
function M.plain(inlines)
  return (pandoc.utils.stringify(inlines):gsub("\194\160", " "):gsub("\194\173", ""))
end

function M.span(text, class)
  return pandoc.Span(pandoc.Inlines(text), { class = class })
end

return M
