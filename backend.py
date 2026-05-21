from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import random
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 게임 데이터 설정 (main.py에서 복사)
CHAPTERS = {
    1: {"name": "초보자의 숲", "boss": "거대 슬라임"},
    2: {"name": "메마른 사막", "boss": "모래 폭풍 정령"},
    3: {"name": "차가운 설산", "boss": "설원 예티"},
}

JOB_STATS = {
    "전사": {"hp": 120, "atk": 18, "def": 10, "mp": 30},
    "마법사": {"hp": 80, "atk": 12, "def": 5, "mp": 80},
    "권사": {"hp": 100, "atk": 16, "def": 8, "mp": 50},
    "도적": {"hp": 90, "atk": 19, "def": 6, "mp": 40},
    "용기사": {"hp": 110, "atk": 17, "def": 12, "mp": 55},
}

JOB_SKILLS = {
    "전사": [
        {"name": "도발", "mp": 10, "desc": "2턴 동안 상대를 도발하여 일반공격만 가능하게 만듦"},
        {"name": "베기", "mp": 8, "desc": "강력한 베기 공격 (공격력 1.2배)"},
        {"name": "막기", "mp": 5, "desc": "적의 다음 공격을 완벽하게 막음"},
        {"name": "휩쓸기", "mp": 12, "desc": "광범위 공격 (공격력 1.1배)"},
    ],
    "마법사": [
        {"name": "파이어볼", "mp": 15, "desc": "화염 마법 공격 (공격력 1.3배)"},
        {"name": "아이스볼", "mp": 15, "desc": "냉기 마법 공격 (공격력 1.3배)"},
        {"name": "베리어", "mp": 12, "desc": "방어력을 30% 증가시킴"},
        {"name": "힐", "mp": 20, "desc": "HP를 50 회복"},
    ],
    "권사": [
        {"name": "정권지르기", "mp": 8, "desc": "정권 공격 (공격력 1.1배)"},
        {"name": "막기", "mp": 5, "desc": "적의 다음 공격을 완벽하게 막음"},
        {"name": "투지", "mp": 10, "desc": "2턴 동안 공격력을 1.5배로 상승"},
        {"name": "급소치기", "mp": 15, "desc": "급소를 노린 공격 (데미지 1.5배, 명중률 70%)"},
    ],
    "도적": [
        {"name": "표창던지기", "mp": 8, "desc": "빠른 표창 공격 (공격력 1.2배)"},
        {"name": "고속이동", "mp": 10, "desc": "2턴 동안 회피율을 30% 증가"},
        {"name": "찌르기", "mp": 7, "desc": "재빠른 찌르기 (공격력 1.1배)"},
        {"name": "연속찌르기", "mp": 18, "desc": "3회 연속 공격 (공격력 0.8배 x 3)"},
    ],
    "용기사": [
        {"name": "용의분노", "mp": 20, "desc": "용의 힘으로 공격 (공격력 1.4배)"},
        {"name": "투지", "mp": 10, "desc": "2턴 동안 공격력을 1.5배로 상승"},
        {"name": "베기", "mp": 8, "desc": "강력한 베기 공격 (공격력 1.2배)"},
        {"name": "막기", "mp": 5, "desc": "적의 다음 공격을 완벽하게 막음"},
    ],
}

ITEM_STORE = [
    {"name": "HP 물약", "type": "potion", "subtype": "hp", "power": 50, "price": 20},
    {"name": "MP 물약", "type": "potion", "subtype": "mp", "power": 30, "price": 20},
    {"name": "장검", "type": "gear", "slot": "weapon", "atk": 5, "allowed": ["전사", "용기사"], "price": 100},
    {"name": "스태프", "type": "gear", "slot": "weapon", "atk": 6, "allowed": ["마법사"], "price": 100},
    {"name": "단검", "type": "gear", "slot": "weapon", "atk": 5, "allowed": ["도적"], "price": 100},
    {"name": "장갑", "type": "gear", "slot": "weapon", "atk": 4, "allowed": ["권사"], "price": 100},
    {"name": "강철 갑옷", "type": "gear", "slot": "armor", "hp": 15, "def": 6, "price": 120},
    {"name": "신비한 로브", "type": "gear", "slot": "armor", "hp": 12, "def": 3, "price": 100},
    {"name": "은빛 갑옷", "type": "gear", "slot": "armor", "hp": 18, "def": 5, "price": 140},
    {"name": "힘의 반지", "type": "gear", "slot": "accessory", "atk": 3, "hp": 10, "def": 1, "price": 90},
    {"name": "생명의 목걸이", "type": "gear", "slot": "accessory", "atk": 1, "hp": 20, "def": 1, "price": 90},
    {"name": "용의 펜던트", "type": "gear", "slot": "accessory", "atk": 2, "hp": 15, "def": 2, "price": 110},
]

class Player:
    def __init__(self, name, job_class):
        self.name = name
        self.job_class = job_class
        stats = JOB_STATS[job_class]
        self.base_max_hp = stats["hp"]
        self.hp = stats["hp"]
        self.base_atk = stats["atk"]
        self.base_def = stats["def"]
        self.mp = stats["mp"]
        self.max_mp = stats["mp"]
        self.exp = 0
        self.skills_learned = JOB_SKILLS[job_class]
        self.gold = 30
        self.inventory = {"HP 물약": 1, "MP 물약": 1}
        self.equipment = {"weapon": None, "armor": None, "accessory": None}
        self.status_effects = {}
        self.is_blocking = False
        self.is_taunted = False

    def get_atk(self):
        weapon_bonus = self.equipment["weapon"]["atk"] if self.equipment["weapon"] else 0
        accessory_bonus = self.equipment["accessory"]["atk"] if self.equipment["accessory"] else 0
        return self.base_atk + weapon_bonus + accessory_bonus

    def get_max_hp(self):
        armor_bonus = self.equipment["armor"]["hp"] if self.equipment["armor"] else 0
        accessory_bonus = self.equipment["accessory"]["hp"] if self.equipment["accessory"] else 0
        return self.base_max_hp + armor_bonus + accessory_bonus

    def get_def(self):
        armor_bonus = self.equipment["armor"]["def"] if self.equipment["armor"] else 0
        accessory_bonus = self.equipment["accessory"]["def"] if self.equipment["accessory"] else 0
        return self.base_def + armor_bonus + accessory_bonus

    def get_atk_multiplier(self):
        return 1.5 if "투지" in self.status_effects else 1.0

    def get_def_multiplier(self):
        return 1.3 if "베리어" in self.status_effects else 1.0

    def get_evasion_rate(self):
        return 0.3 if "고속이동" in self.status_effects else 0.0

    def reduce_status_effects(self):
        expired = []
        for effect in list(self.status_effects.keys()):
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                expired.append(effect)
        for effect in expired:
            del self.status_effects[effect]
            if effect == "도발":
                self.is_taunted = False
            elif effect == "막기":
                self.is_blocking = False

    def to_dict(self):
        return {
            "name": self.name,
            "job_class": self.job_class,
            "hp": self.hp,
            "max_hp": self.get_max_hp(),
            "mp": self.mp,
            "max_mp": self.max_mp,
            "atk": self.get_atk(),
            "def": self.get_def(),
            "gold": self.gold,
            "inventory": self.inventory,
            "equipment": self.equipment,
            "status_effects": self.status_effects,
            "is_blocking": self.is_blocking,
            "is_taunted": self.is_taunted,
            "skills": self.skills_learned
        }

class GameState:
    def __init__(self):
        self.player = None
        self.current_chapter = 1
        self.current_stage = 1
        self.in_battle = False
        self.in_shop = False
        self.is_boss = False
        self.enemies = []
        self.logs = []
        self.game_over = False
        self.game_clear = False

    def add_log(self, msg):
        self.logs.append(msg)

    def to_dict(self):
        return {
            "player": self.player.to_dict() if self.player else None,
            "current_chapter": self.current_chapter,
            "current_stage": self.current_stage,
            "in_battle": self.in_battle,
            "in_shop": self.in_shop,
            "is_boss": self.is_boss,
            "enemies": self.enemies,
            "logs": self.logs[-50:], # 최근 50개 로그만 전송
            "game_over": self.game_over,
            "game_clear": self.game_clear
        }

game_state = GameState()

class StartRequest(BaseModel):
    name: str
    job_class: str

@app.get("/api/game/data")
def get_game_data():
    return {
        "jobs": list(JOB_STATS.keys()),
        "job_stats": JOB_STATS,
        "items": ITEM_STORE
    }

@app.post("/api/game/start")
def start_game(req: StartRequest):
    global game_state
    if req.job_class not in JOB_STATS:
        raise HTTPException(status_code=400, detail="Invalid job class")
    
    game_state = GameState()
    game_state.player = Player(req.name, req.job_class)
    game_state.add_log(f"✨ {req.job_class} {req.name}이(가) 탄생했습니다!")
    return game_state.to_dict()

@app.get("/api/game/state")
def get_state():
    return game_state.to_dict()

class RouteRequest(BaseModel):
    route: str

def advance_stage():
    game_state.current_stage += 1
    if game_state.current_stage > 10:
        game_state.add_log(f"🎉 챕터 {game_state.current_chapter} 정복!")
        game_state.current_chapter += 1
        game_state.current_stage = 1
        if game_state.current_chapter > 3:
            game_state.game_clear = True
            game_state.add_log("🏆 전설의 용사가 되셨습니다! 게임 클리어!")

@app.post("/api/game/choose_route")
def choose_route(req: RouteRequest):
    if game_state.in_battle or game_state.in_shop or not game_state.player:
        raise HTTPException(status_code=400, detail="Cannot choose route now")
    
    route = req.route
    if game_state.current_stage == 10:
        route = "battle" # 보스 스테이지는 무조건 전투 강제
        
    if route == "rest":
        p = game_state.player
        p.hp = p.get_max_hp()
        p.mp = p.max_mp
        game_state.add_log("💤 캠프에서 휴식을 취하여 HP와 MP가 모두 회복되었습니다.")
        advance_stage()
        
    elif route == "shop":
        game_state.in_shop = True
        game_state.add_log("🛒 상점에 입장했습니다.")
        
    elif route == "battle":
        chapter_data = CHAPTERS.get(game_state.current_chapter, {"name": "알 수 없는 땅", "boss": "최종 보스"})
        game_state.is_boss = (game_state.current_stage == 10)
        
        num_monsters = 1 if game_state.is_boss else random.randint(1, 3)
        enemy_base_name = chapter_data['boss'] if game_state.is_boss else f"스테이지 {game_state.current_stage} 몬스터"
        
        game_state.enemies = []
        for i in range(num_monsters):
            name = f"{enemy_base_name} {i+1}" if num_monsters > 1 else enemy_base_name
            game_state.enemies.append({
                "id": i,
                "name": name,
                "hp": 100 if game_state.is_boss else 30,
                "atk": 12 if game_state.is_boss else 8,
                "def": 3 if game_state.is_boss else 1,
                "effects": {},
                "is_taunted": False,
                "is_blocking": False
            })
        
        game_state.in_battle = True
        if num_monsters > 1:
            game_state.add_log(f"⚔️ {num_monsters}마리의 {enemy_base_name}가 출현하였습니다!")
        else:
            game_state.add_log(f"⚔️ 1마리의 {game_state.enemies[0]['name']}(이)가 출현하였습니다!")
            
        if game_state.is_boss:
            game_state.add_log("⚠️ 주의: 보스 몬스터입니다!")
            
    return game_state.to_dict()

@app.post("/api/game/leave_shop")
def leave_shop():
    if not game_state.in_shop:
        raise HTTPException(status_code=400, detail="Not in shop")
    game_state.in_shop = False
    game_state.add_log("🚶 상점을 나와 다음 지역으로 이동합니다.")
    advance_stage()
    return game_state.to_dict()

class BattleActionRequest(BaseModel):
    action_type: str # "attack", "skill", "item", "flee"
    target_id: Optional[int] = None
    skill_name: Optional[str] = None
    item_name: Optional[str] = None

@app.post("/api/game/action")
def battle_action(req: BattleActionRequest):
    if not game_state.in_battle or game_state.game_over:
        raise HTTPException(status_code=400, detail="Not in battle")
    
    p = game_state.player
    alive_enemies = [e for e in game_state.enemies if e["hp"] > 0]
    
    target = None
    if req.target_id is not None:
        target = next((e for e in alive_enemies if e["id"] == req.target_id), None)
        
    # 플레이어 행동 처리
    if p.is_taunted and req.action_type not in ["attack", "item"]:
        game_state.add_log("💫 도발 상태! 기본공격 또는 아이템 사용만 가능합니다!")
        return game_state.to_dict()
        
    if req.action_type == "attack":
        if not target:
            target = alive_enemies[0]
        damage = random.randint(p.get_atk() - 5, p.get_atk() + 5)
        damage = int(damage * p.get_atk_multiplier())
        damage = max(1, damage - target["def"])
        
        if target["is_blocking"]:
            game_state.add_log(f"🛡️ {target['name']}이(가) 공격을 완벽하게 방어했습니다!")
            target["is_blocking"] = False
        else:
            target["hp"] -= damage
            game_state.add_log(f"💥 {target['name']}에게 {damage}의 대미지를 입혔습니다!")
            
    elif req.action_type == "skill":
        skill = next((s for s in p.skills_learned if s["name"] == req.skill_name), None)
        if not skill or p.mp < skill["mp"]:
            game_state.add_log("❌ 스킬을 사용할 수 없거나 MP가 부족합니다.")
            return game_state.to_dict()
            
        p.mp -= skill["mp"]
        s_name = skill["name"]
        
        if s_name == "도발":
            if not target: target = alive_enemies[0]
            target["is_taunted"] = True
            target["effects"]["도발"] = 2
            game_state.add_log(f"💫 {s_name}를 사용했습니다! {target['name']}이(가) 도발 상태에 빠졌습니다!")
            
        elif s_name in ["베기", "파이어볼", "아이스볼", "정권지르기", "표창던지기", "찌르기", "용의분노"]:
            if not target: target = alive_enemies[0]
            mult = {"베기": 1.2, "파이어볼": 1.3, "아이스볼": 1.3, "정권지르기": 1.1, "표창던지기": 1.2, "찌르기": 1.1, "용의분노": 1.4}.get(s_name, 1.0)
            damage = max(1, int(random.randint(p.get_atk() - 5, p.get_atk() + 5) * mult * p.get_atk_multiplier()) - target["def"])
            if target["is_blocking"]:
                game_state.add_log(f"🛡️ {target['name']}이(가) 공격을 방어했습니다!")
                target["is_blocking"] = False
            else:
                target["hp"] -= damage
                game_state.add_log(f"💫 {s_name}! {target['name']}에게 {damage}의 대미지!")
                
        elif s_name == "휩쓸기":
            game_state.add_log(f"💫 {s_name}! (광범위 공격)")
            for t in alive_enemies:
                damage = max(1, int(random.randint(p.get_atk() - 5, p.get_atk() + 5) * 1.1 * p.get_atk_multiplier()) - t["def"])
                if t["is_blocking"]:
                    game_state.add_log(f"🛡️ {t['name']}이(가) 방어했습니다!")
                    t["is_blocking"] = False
                else:
                    t["hp"] -= damage
                    game_state.add_log(f"💥 {t['name']}에게 {damage}의 대미지!")
                    
        elif s_name == "힐":
            heal = min(50, p.get_max_hp() - p.hp)
            p.hp += heal
            game_state.add_log(f"💚 {s_name} 사용! {heal} HP 회복!")
            
        # 기타 버프 스킬들 처리 (간략화)
        elif s_name in ["투지", "고속이동", "베리어"]:
            p.status_effects[s_name] = 2
            game_state.add_log(f"💫 {s_name} 버프가 적용되었습니다!")
        else:
            game_state.add_log(f"💫 {s_name}를 사용했습니다!")
            
    elif req.action_type == "item":
        if req.item_name == "HP 물약" and p.inventory.get("HP 물약", 0) > 0:
            p.inventory["HP 물약"] -= 1
            p.hp = min(p.get_max_hp(), p.hp + 50)
            game_state.add_log("💚 HP 물약을 사용하여 체력을 회복했습니다.")
        elif req.item_name == "MP 물약" and p.inventory.get("MP 물약", 0) > 0:
            p.inventory["MP 물약"] -= 1
            p.mp = min(p.max_mp, p.mp + 30)
            game_state.add_log("🔷 MP 물약을 사용하여 마력을 회복했습니다.")
        else:
            game_state.add_log("❌ 물약이 부족합니다.")
            return game_state.to_dict()
            
    elif req.action_type == "flee":
        if game_state.is_boss:
            game_state.add_log("🚫 보스전에서는 도망칠 수 없습니다!")
            return game_state.to_dict()
        game_state.add_log("🏃 전투에서 도망쳤습니다.")
        game_state.in_battle = False
        return game_state.to_dict()

    # 적 턴 처리
    process_enemy_turn()
    
    # 승패 판정
    check_battle_end()

    return game_state.to_dict()

def process_enemy_turn():
    p = game_state.player
    p.reduce_status_effects()
    
    alive_enemies = [e for e in game_state.enemies if e["hp"] > 0]
    for e in alive_enemies:
        if p.hp <= 0: break
        
        # 상태 이상 감소
        expired = []
        for ef in list(e["effects"].keys()):
            e["effects"][ef] -= 1
            if e["effects"][ef] <= 0:
                expired.append(ef)
        for ef in expired:
            del e["effects"][ef]
            if ef == "도발": e["is_taunted"] = False
            
        game_state.add_log(f"🔴 {e['name']}의 공격!")
        
        if random.random() < p.get_evasion_rate():
            game_state.add_log(f"⚡ {p.name}이(가) 공격을 회피했습니다!")
        else:
            dmg = max(1, int(random.randint(e["atk"] - 3, e["atk"] + 3) - (p.get_def() * p.get_def_multiplier())))
            if p.is_blocking:
                game_state.add_log(f"🛡️ {p.name}이(가) 완벽하게 방어했습니다!")
                p.is_blocking = False
            else:
                p.hp -= dmg
                game_state.add_log(f"🩸 {dmg}의 대미지를 입었습니다!")

def check_battle_end():
    p = game_state.player
    alive_enemies = [e for e in game_state.enemies if e["hp"] > 0]
    
    if p.hp <= 0:
        game_state.add_log("💀 당신은 쓰러졌습니다... 게임 오버.")
        game_state.game_over = True
        game_state.in_battle = False
        
    elif len(alive_enemies) == 0:
        reward = 30 if game_state.is_boss else 10 * len(game_state.enemies)
        p.gold += reward
        game_state.add_log(f"✨ 전투 승리! {reward} 골드를 획득했습니다.")
        game_state.in_battle = False
        
        game_state.current_stage += 1
        if game_state.current_stage > 10:
            game_state.add_log(f"🎉 챕터 {game_state.current_chapter} 정복!")
            game_state.current_chapter += 1
            game_state.current_stage = 1
            if game_state.current_chapter > 3: # 3챕터까지만 있다고 가정
                game_state.game_clear = True
                game_state.add_log("🏆 전설의 용사가 되셨습니다! 게임 클리어!")

class BuyRequest(BaseModel):
    item_index: int

@app.post("/api/game/shop/buy")
def buy_item(req: BuyRequest):
    if game_state.in_battle:
        raise HTTPException(status_code=400, detail="Cannot shop in battle")
    
    p = game_state.player
    item = ITEM_STORE[req.item_index]
    
    allowed = item.get("allowed")
    if allowed and p.job_class not in allowed:
        game_state.add_log(f"❌ {p.job_class}는(은) 이 장비를 사용할 수 없습니다.")
        return game_state.to_dict()
        
    if p.gold < item["price"]:
        game_state.add_log("❌ 골드가 부족합니다.")
        return game_state.to_dict()
        
    p.gold -= item["price"]
    if item["type"] == "potion":
        p.inventory[item["name"]] = p.inventory.get(item["name"], 0) + 1
        game_state.add_log(f"✅ {item['name']} 구매 완료!")
    else:
        p.equipment[item["slot"]] = item
        p.hp = min(p.hp, p.get_max_hp())
        game_state.add_log(f"✅ {item['name']} 장착 완료!")
        
    return game_state.to_dict()


# ---------------------------------------------------------------------------
# static 파일 서빙 (Unified Single-Server Deployment)
# ---------------------------------------------------------------------------
dist_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, "assets")), name="assets")
    
    # /images 폴더도 static 파일로 서빙하도록 마운트 설정
    images_path = os.path.join(dist_path, "images")
    if os.path.exists(images_path):
        app.mount("/images", StaticFiles(directory=images_path), name="images")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(dist_path, "index.html"))

    # SPA 라우팅 대비용 catch-all route
    @app.get("/{catchall:path}")
    def read_index(catchall: str):
        if catchall.startswith("api/") or "." in catchall:
            raise HTTPException(status_code=404, detail="Not Found")
        return FileResponse(os.path.join(dist_path, "index.html"))


if __name__ == "__main__":
    import uvicorn
    # Render 등 클라우드 플랫폼에서 부여하는 dynamic port에 바인딩
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("backend:app", host="0.0.0.0", port=port, reload=False)

