-- Execute extracted production functions and complete wrapper modules, with mocked engine APIs.
local checked = 0
local function check(condition, message)
    assert(condition, message)
    checked = checked + 1
end
local warfare, story, info, faction, new_faction, new_story
local function mode(w, s, i, f, nf, ns)
    warfare, story, info, faction, new_faction, new_story = w, s, i, f or "isg", nf, ns
end
IsWarfare = function() return warfare end
IsStoryMode = function() return story end
has_alife_info = function(key) assert(key == "story_mode_disabled"); return info end
printf = function() end
db = {actor = {}}
xr_conditions = {is_actor_from_faction = function(_, _, p) return faction == p[1] end}
axr_main = {config = {r_value = function(_, _, key)
    if key == "new_game_faction" then return new_faction end
    if key == "new_game_story_mode" then return new_story end
    error("Unexpected config field")
end}}

local state, smart, population, registry, registrations
local function fixture()
    state = {}
    smart = {props = {base = 1}, first_update = true}
    population, registry, registrations = 2, nil, 0
    SIMBOARD = {smarts_by_names = {jup_b208 = smart}}
    alife_storage_manager = {get_state = function() return state end}
    get_stalker_pop_factor = function() return population end
    smart_terrain_warfare = {
        uniques = {jup_b208 = {1, 1, 0, 0, 0}},
        is_main_base = function() return registry ~= nil end,
        get_main_base_faction = function() return registry and registry.faction end,
        set_main_base = function(name, entry)
            assert(name == "jup_b208")
            registry = entry
            registrations = registrations + 1
        end,
        set_max_population = function(s) s.max_population = s.default_max_population * population end,
    }
    spawn_squad = function() error("Restore must never spawn a squad") end
    return assert(loadstring(sources.hq .. [[
return {mode=unisg_hq_mode, restore=unisg_hq_restore, reset=unisg_hq_reset_registration,
        reset_services=unisg_services_reset}
]]))()
end

local hq = fixture()
for _, w in ipairs({false, true}) do
    for _, s in ipairs({false, true}) do
        for _, i in ipairs({false, true}) do
            mode(w, s, i)
            check(hq.mode() == (w and not s and i), "Saved mode must use both saved checks")
            for _, f in ipairs({"isg", "stalker"}) do
                for _, choice in ipairs({false, true}) do
                    mode(w, s, i, f, f, choice and true or nil)
                    check(hq.mode() == (w and not choice), "New-game choice must override stale saved mode")
                end
            end
        end
    end
end

for _, invalid in ipairs({"unmarked", "story", "warfare", "smart"}) do
    hq = fixture()
    state.walo_unisg_hq_native_v03 = invalid ~= "unmarked"
    mode(invalid ~= "warfare", invalid == "story", true)
    if invalid == "smart" then SIMBOARD.smarts_by_names.jup_b208 = nil end
    hq.restore()
    check(registrations == 0 and smart_terrain_warfare.uniques.jup_b208[3] == 0,
          "Ineligible restore must not register HQ or services")
end
hq = fixture()
mode(true, false, true)
state.walo_unisg_hq_native_v03 = true
hq.restore()
hq.restore()
check(registrations == 1 and registry.faction == "isg" and registry.protect == false and registry.resurrect,
      "Restore must register once and preserve native capture/resurrection")
check(smart.max_population == 4 and smart_terrain_warfare.uniques.jup_b208[3] == 1
      and smart_terrain_warfare.uniques.jup_b208[4] == 1, "Native capacity and service slots")
hq.reset()
hq.reset_services()
check(registry == nil and smart_terrain_warfare.uniques.jup_b208[3] == 0
      and smart_terrain_warfare.uniques.jup_b208[4] == 0, "Save switch must reverse owned changes")
hq = fixture()
state.walo_unisg_hq_native_v03 = true
hq.restore()
registry = {faction = "dolg"}
smart_terrain_warfare.uniques.jup_b208[3] = 2
hq.reset()
hq.reset_services()
check(registry.faction == "dolg" and smart_terrain_warfare.uniques.jup_b208[3] == 2,
      "Cleanup must not overwrite another mod's later changes")
hq = fixture()
registry = {faction = "dolg"}
state.walo_unisg_hq_native_v03 = true
hq.restore()
check(registrations == 0 and registry.faction == "dolg", "Existing foreign registry must survive")

for name, source in pairs(sources.gates) do
    local gate = assert(loadstring(source))()
    for _, w in ipairs({false, true}) do
        for _, s in ipairs({false, true}) do
            for _, i in ipairs({false, true}) do
                mode(w, s, i)
                check(not not gate() == (w and not s and i), "Mode isolation: " .. name)
            end
        end
    end
    if name:find("field_science", 1, true) then
        mode(true, false, true, "stalker")
        check(not gate(), "Scientific missions require an ISG actor")
    end
end
local menu_gate = assert(loadstring(sources.menu_gate))()
for _, f in ipairs({"isg", "stalker"}) do
    for _, w in ipairs({false, true}) do
        for _, s in ipairs({false, true}) do
            check(menu_gate({selected_faction=f, ck_warfare={GetCheck=function() return w end},
                             ck_story={GetCheck=function() return s end}}) == (f == "isg" and w and not s),
                  "Menu must hide the HQ start outside UNISG/non-Story Warfare")
        end
    end
end

local function load_module(source, extra)
    local env = setmetatable(extra, {__index=_G})
    env.RegisterScriptCallback = function() end
    local chunk = assert(loadstring(source))
    setfenv(chunk, env)
    chunk()
    env.on_game_start()
    return env
end
local point, owner, place, calls = {x=383.105,y=4.494,z=-126.328}, "isg", "jupiter", 0
local saving = load_module(sources.saving, {
    db={actor={position=function() return point end}},
    level={name=function() return place end},
    SIMBOARD={smarts_by_names={jup_b208=setmetatable({}, {__index=function() return owner end})}},
    gameplay_disguise={get_default_comm=function() return faction end},
    ish_campfire_saving={is_within_friendly_base=function(arg)
        calls = calls + 1; return "native", arg
    end},
})
local wrapped = saving.ish_campfire_saving.is_within_friendly_base
saving.on_game_start()
check(saving.ish_campfire_saving.is_within_friendly_base == wrapped, "Saving wrapper must not stack itself")
mode(true, false, true)
check(wrapped() == true and calls == 0, "Allow saving only inside friendly ISG HQ")
for _, failure in ipairs({"story", "warfare", "info", "faction", "owner", "level", "distance"}) do
    mode(failure ~= "warfare", failure == "story", failure ~= "info", failure == "faction" and "stalker" or "isg")
    owner = failure == "owner" and "dolg" or "isg"
    place = failure == "level" and "zaton" or "jupiter"
    point = failure == "distance" and {x=0,y=0,z=0} or {x=383.105,y=4.494,z=-126.328}
    local result, argument = wrapped("sentinel")
    check(result == "native" and argument == "sentinel", "Saving must delegate: " .. failure)
end
local dao = load_module(sources.dao, {
    drx_da_main={drx_da_spawn_anomaly_on_smart=function(...) return "native", ... end},
})
wrapped = dao.drx_da_main.drx_da_spawn_anomaly_on_smart
dao.on_game_start()
check(dao.drx_da_main.drx_da_spawn_anomaly_on_smart == wrapped, "DAO wrapper must not stack itself")
mode(true, false, true)
check(wrapped("file", "jup_b208", "type", "jupiter", "data") == false, "Block new HQ anomaly only")
for _, failure in ipairs({"story", "warfare", "info", "smart", "level"}) do
    mode(failure ~= "warfare", failure == "story", failure ~= "info")
    local result, file = wrapped("file", failure == "smart" and "other" or "jup_b208", "type",
                                failure == "level" and "zaton" or "jupiter", "data")
    check(result == "native" and file == "file", "DAO must delegate: " .. failure)
end
return checked
