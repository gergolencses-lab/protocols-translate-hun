-- Idézetblokkok: keretes doboz, ajánlás, példa.
local function first_inlines(bq)
  local b = bq.content[1]
  if b and (b.t == "Para" or b.t == "Plain") then return b.content end
end

function BlockQuote(bq)
  local inl = first_inlines(bq)
  if not inl or #inl == 0 then return nil end
  if #inl == 1 and inl[1].t == "Strong" then
    local blocks = bq.content:clone()
    blocks[1] = pandoc.Div({ pandoc.Para(inl) }, { class = "sidebar-title" })
    return pandoc.Div(blocks, { class = "sidebar" })
  elseif inl[1].t == "Emph" then
    return pandoc.Div(bq.content, { class = "dedication" })
  elseif inl[1].t == "Str" and inl[1].text == "Példa:" then
    return pandoc.Div(bq.content, { class = "example" })
  end
end
