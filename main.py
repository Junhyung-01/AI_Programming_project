import random
import time

# 1. 게임 데이터 설정
CHAPTERS = {
    1: {"name": "초보자의 숲", "boss": "거대 슬라임"},
    2: {"name": "메마른 사막", "boss": "모래 폭풍 정령"},
    3: {"name": "차가운 설산", "boss": "설원 예티"},
    # 10챕터까지 동일한 방식으로 추가 가능
}

# 직업별 기본 능력치 설정
JOB_STATS = {
    "전사": {"hp": 120, "atk": 18, "def": 10, "mp": 30},
    "마법사": {"hp": 80, "atk": 12, "def": 5, "mp": 80},
    "권사": {"hp": 100, "atk": 16, "def": 8, "mp": 50},
    "도적": {"hp": 90, "atk": 19, "def": 6, "mp": 40},
    "용기사": {"hp": 110, "atk": 17, "def": 12, "mp": 55},
}

# 직업별 스킬 정의
JOB_SKILLS = {
    "전사": [
        {"name": "도발", "mp": 10, "desc": "2턴 동안 상대를 도발하여 일반공격만 가능하게 만듦"},
        {"name": "베기", "mp": 8, "desc": "강력한 베기 공격 (공격력 1.2배)"},
        {"name": "막기", "mp": 5, "desc": "적의 다음 공격을 완벽하게 막음"},
        {"name": "휩쓸기", "mp": 12, "desc": "광범위 공격 (공격력 1.1배)"},
    ],
    "마법사": [
        {"name": "파이어볼", "mp": 7, "desc": "화염 마법 공격 (공격력 1.3배)"},
        {"name": "아이스볼", "mp": 7, "desc": "냉기 마법 공격 (공격력 1.3배)"},
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

    def show_status(self):
        print(f"\n--- {self.name}의 상태 (직업: {self.job_class}) ---")
        print(f"HP: {self.hp}/{self.get_max_hp()} | MP: {self.mp}/{self.max_mp}")
        print(f"공격력: {self.get_atk()} | 방어력: {self.get_def()}")
        print(f"골드: {self.gold}")
        if self.skills_learned:
            print(f"배운 스킬: {', '.join([s['name'] for s in self.skills_learned])}")
        print("장착 중:")
        print(f"  무기: {self.equipment['weapon']['name'] if self.equipment['weapon'] else '없음'}")
        print(f"  방어구: {self.equipment['armor']['name'] if self.equipment['armor'] else '없음'}")
        print(f"  장신구: {self.equipment['accessory']['name'] if self.equipment['accessory'] else '없음'}")
        print("인벤토리:")
        print(f"  HP 물약: {self.inventory.get('HP 물약', 0)} | MP 물약: {self.inventory.get('MP 물약', 0)}")
        if self.status_effects:
            status_str = ", ".join([f"{k}({v}턴)" for k, v in self.status_effects.items()])
            print(f"상태 효과: {status_str}")

    def equip_item(self, item):
        slot = item["slot"]
        self.equipment[slot] = item
        self.hp = min(self.hp, self.get_max_hp())
        print(f"✅ {item['name']}을(를) 장착했습니다.")

    def add_status_effect(self, effect_name, duration):
        self.status_effects[effect_name] = duration
        if effect_name == "도발":
            self.is_taunted = True
        elif effect_name == "막기":
            self.is_blocking = True

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

    def get_atk_multiplier(self):
        return 1.5 if "투지" in self.status_effects else 1.0

    def get_def_multiplier(self):
        return 1.3 if "베리어" in self.status_effects else 1.0

    def get_evasion_rate(self):
        return 0.3 if "고속이동" in self.status_effects else 0.0

    def use_potion(self, potion):
        if potion == "HP 물약" and self.inventory.get("HP 물약", 0) > 0:
            self.inventory["HP 물약"] -= 1
            heal = min(50, self.get_max_hp() - self.hp)
            self.hp += heal
            print(f"💚 HP를 {heal}만큼 회복했습니다!")
        elif potion == "MP 물약" and self.inventory.get("MP 물약", 0) > 0:
            self.inventory["MP 물약"] -= 1
            restore = min(30, self.max_mp - self.mp)
            self.mp += restore
            print(f"🔷 MP를 {restore}만큼 회복했습니다!")
        else:
            print("❌ 해당 물약이 없습니다.")


def get_choice(options):
    """번호 선택 공통 함수"""
    while True:
        print("\n" + "-" * 30)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        choice = input("선택지를 입력하세요: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("❌ 잘못된 입력입니다. 숫자를 입력해주세요.")

def get_target(enemies):
    if len(enemies) == 1:
        return enemies[0]
    print("\n🎯 대상을 선택하세요:")
    options = [f"{e['name']} (HP: {e['hp']})" for e in enemies]
    choice = get_choice(options)
    return enemies[choice - 1]

def battle(player, enemy_base_name, num_enemies=1, is_boss=False):
    """전투 로직"""
    enemies = []
    for i in range(num_enemies):
        name = f"{enemy_base_name} {i+1}" if num_enemies > 1 else enemy_base_name
        enemies.append({
            "name": name,
            "hp": 100 if is_boss else 30,
            "atk": 12 if is_boss else 8,
            "def": 3 if is_boss else 1,
            "effects": {},
            "is_taunted": False,
            "is_blocking": False
        })
    
    if num_enemies > 1:
        print(f"\n⚔️ {num_enemies}마리의 {enemy_base_name}가 출현하였습니다!")
    else:
        print(f"\n⚔️ 1마리의 {enemies[0]['name']}(이)가 출현하였습니다!")
        
    if is_boss:
        print("⚠️ 주의: 보스 몬스터입니다!")

    while any(e["hp"] > 0 for e in enemies) and player.hp > 0:
        alive_enemies = [e for e in enemies if e["hp"] > 0]
        
        print(f"\n나의 HP: {player.hp}/{player.get_max_hp()}")
        for e in alive_enemies:
            print(f"{e['name']} HP: {e['hp']}")
        
        # 플레이어 행동
        if player.is_taunted:
            print("💫 도발 상태! 기본공격 또는 아이템 사용만 가능합니다!")
            action = get_choice(["기본공격", "아이템 사용"])
        else:
            action = get_choice(["기본공격", "스킬 사용", "아이템 사용", "도망치기"])
        
        if action == 1:
            # 기본공격
            target = get_target(alive_enemies)
            damage = random.randint(player.get_atk() - 5, player.get_atk() + 5)
            damage = int(damage * player.get_atk_multiplier())
            damage = max(1, damage - target["def"])

            if target["is_blocking"]:
                print(f"🛡️ {target['name']}이(가) 공격을 완벽하게 방어했습니다!")
                target["is_blocking"] = False
            else:
                target["hp"] -= damage
                print(f"💥 {target['name']}에게 {damage}의 대미지를 입혔습니다!")
        
        elif action == 2 and not player.is_taunted:
            # 스킬 사용
            skill = use_skill_menu(player)
            if skill:
                if skill["name"] == "도발":
                    if player.mp >= skill["mp"]:
                        player.mp -= skill["mp"]
                        target = get_target(alive_enemies)
                        target["is_taunted"] = True
                        target["effects"]["도발"] = 2
                        print(f"\n💫 {skill['name']}를 사용했습니다!")
                        print(f"😤 {target['name']}이(가) 도발 상태에 빠졌습니다! (2턴)")
                
                elif skill["name"] in ["베기", "파이어볼", "아이스볼", "정권지르기", "표창던지기", "찌르기", "용의분노"]:
                    target = get_target(alive_enemies)
                    multiplier = {"베기": 1.2, "파이어볼": 1.3, "아이스볼": 1.3, "정권지르기": 1.1, "표창던지기": 1.2, "찌르기": 1.1, "용의분노": 1.4}.get(skill["name"], 1.0)
                    player.mp -= skill["mp"]
                    damage = random.randint(player.get_atk() - 5, player.get_atk() + 5)
                    damage = int(damage * multiplier * player.get_atk_multiplier())
                    damage = max(1, damage - target["def"])
                    
                    if target["is_blocking"]:
                        print(f"🛡️ {target['name']}이(가) 공격을 완벽하게 방어했습니다!")
                        target["is_blocking"] = False
                    else:
                        target["hp"] -= damage
                        print(f"\n💫 {skill['name']}를 사용했습니다!")
                        print(f"💥 {target['name']}에게 {damage}의 대미지를 입혔습니다!")
                
                elif skill["name"] == "연속찌르기":
                    target = get_target(alive_enemies)
                    player.mp -= skill["mp"]
                    print(f"\n💫 {skill['name']}를 사용했습니다!")
                    for i in range(3):
                        damage = random.randint(player.get_atk() - 5, player.get_atk() + 5)
                        damage = int(damage * 0.8)
                        damage = max(1, damage - target["def"])
                        if not target["is_blocking"]:
                            target["hp"] -= damage
                            print(f"💥 {i+1}번째 공격: {target['name']}에게 {damage}의 대미지!")
                        else:
                            print(f"🛡️ {target['name']}이(가) {i+1}번째 공격을 방어했습니다!")
                            target["is_blocking"] = False
                            break
                
                elif skill["name"] == "막기":
                    player.mp -= skill["mp"]
                    player.is_blocking = True
                    print(f"\n💫 {skill['name']}를 사용했습니다!")
                    print(f"🛡️ {player.name}이(가) 막기 자세를 취했습니다!")
                
                elif skill["name"] == "투지":
                    player.mp -= skill["mp"]
                    player.add_status_effect("투지", 2)
                    print(f"\n💫 {skill['name']}를 사용했습니다!")
                    print(f"⚡ {player.name}의 공격력이 1.5배 증가했습니다! (2턴)")
                
                elif skill["name"] == "고속이동":
                    player.mp -= skill["mp"]
                    player.add_status_effect("고속이동", 2)
                    print(f"\n💫 {skill['name']}를 사용했습니다!")
                    print(f"⚡ {player.name}의 회피율이 30% 증가했습니다! (2턴)")
                
                elif skill["name"] == "베리어":
                    player.mp -= skill["mp"]
                    player.add_status_effect("베리어", 2)
                    print(f"\n💫 {skill['name']}를 사용했습니다!")
                    print(f"🛡️ {player.name}의 방어력이 30% 증가했습니다! (2턴)")
                
                elif skill["name"] == "힐":
                    player.mp -= skill["mp"]
                    heal_amount = min(50, player.get_max_hp() - player.hp)
                    player.hp += heal_amount
                    print(f"\n💫 {skill['name']}를 사용했습니다!")
                    print(f"💚 {heal_amount}의 HP를 회복했습니다!")
                
                elif skill["name"] == "급소치기":
                    target = get_target(alive_enemies)
                    hit_chance = random.random()
                    if hit_chance < 0.7:
                        player.mp -= skill["mp"]
                        damage = random.randint(player.get_atk() - 5, player.get_atk() + 5)
                        damage = int(damage * 1.5 * player.get_atk_multiplier())
                        damage = max(1, damage - target["def"])
                        
                        if target["is_blocking"]:
                            print(f"🛡️ {target['name']}이(가) 공격을 완벽하게 방어했습니다!")
                            target["is_blocking"] = False
                        else:
                            target["hp"] -= damage
                            print(f"\n💫 {skill['name']}를 사용했습니다!")
                            print(f"💥 급소 명중! {target['name']}에게 {damage}의 대미지를 입혔습니다!")
                    else:
                        player.mp -= skill["mp"]
                        print(f"\n💫 {skill['name']}를 사용했습니다!")
                        print(f"❌ 급소치기가 빗나갔습니다!")
                
                elif skill["name"] == "휩쓸기":
                    player.mp -= skill["mp"]
                    print(f"\n💫 {skill['name']}를 사용했습니다! (광범위 공격)")
                    for target in alive_enemies:
                        damage = random.randint(player.get_atk() - 5, player.get_atk() + 5)
                        damage = int(damage * 1.1 * player.get_atk_multiplier())
                        damage = max(1, damage - target["def"])
                        
                        if target["is_blocking"]:
                            print(f"🛡️ {target['name']}이(가) 공격을 완벽하게 방어했습니다!")
                            target["is_blocking"] = False
                        else:
                            target["hp"] -= damage
                            print(f"💥 {target['name']}에게 {damage}의 대미지를 입혔습니다!")
        elif (action == 2 and player.is_taunted) or action == 3:
            # 아이템 사용
            use_item_menu(player)
        else:
            if not is_boss:
                print("🏃 전투에서 도망쳤습니다.")
                return False
            print("🚫 보스전에서는 도망칠 수 없습니다!")
        
        # 플레이어 상태 효과 감소
        player.reduce_status_effects()
        
        # 적 상태 효과 감소 및 적의 공격
        alive_enemies = [e for e in enemies if e["hp"] > 0]
        for enemy in alive_enemies:
            effects_to_remove = []
            for effect in enemy["effects"]:
                enemy["effects"][effect] -= 1
                if enemy["effects"][effect] <= 0:
                    effects_to_remove.append(effect)
            for effect in effects_to_remove:
                del enemy["effects"][effect]
                if effect == "도발":
                    enemy["is_taunted"] = False
            
            # 적의 공격
            if player.hp > 0:
                print(f"\n🔴 {enemy['name']}의 공격!")
                
                # 회피 판정
                evasion = random.random()
                if evasion < player.get_evasion_rate():
                    print(f"⚡ {player.name}이(가) 공격을 회피했습니다!")
                else:
                    enemy_damage = random.randint(enemy["atk"] - 3, enemy["atk"] + 3)
                    
                    if player.is_blocking:
                        print(f"🛡️ {player.name}이(가) 공격을 완벽하게 방어했습니다!")
                        player.is_blocking = False
                    else:
                        final_damage = max(1, int(enemy_damage - (player.get_def() * player.get_def_multiplier())))
                        player.hp -= final_damage
                        print(f"🩸 {enemy['name']}에게 {final_damage}의 대미지를 입었습니다!")
                        print(f"   → 현재 나의 HP: {player.hp}/{player.get_max_hp()}")
    
    return player.hp > 0


def use_skill_menu(player):
    """스킬 선택 메뉴"""
    print("\n⚡ 사용 가능한 스킬:")
    for i, skill in enumerate(player.skills_learned, 1):
        mp_status = "✓" if player.mp >= skill["mp"] else "✗"
        print(f"{i}. {skill['name']} (MP: {skill['mp']}) {mp_status}")
    
    choice = input("스킬을 선택하세요 (0: 취소): ")
    if choice == "0" or not choice.isdigit() or int(choice) < 1 or int(choice) > len(player.skills_learned):
        return None
    
    skill_idx = int(choice) - 1
    skill = player.skills_learned[skill_idx]
    
    if player.mp < skill["mp"]:
        print(f"❌ MP가 부족합니다! (필요: {skill['mp']}, 보유: {player.mp})")
        return None
    
    return skill


def show_shop(player):
    print("\n🏪 상점에 오신 것을 환영합니다!")
    while True:
        print("\n구매 가능한 아이템:")
        available = []
        for i, item in enumerate(ITEM_STORE, 1):
            allowed = item.get("allowed")
            can_use = allowed is None or player.job_class in allowed
            status = "(사용 가능)" if can_use else "(사용 불가)"
            if item["type"] == "potion":
                desc = f"{item['power']} 회복"
            else:
                stats = []
                if "atk" in item:
                    stats.append(f"ATK+{item['atk']}")
                if "hp" in item:
                    stats.append(f"HP+{item['hp']}")
                desc = ", ".join(stats)
            print(f"{i}. {item['name']} - {item['price']}골드 {status} ({desc})")
            available.append((item, can_use))
        print("0. 나가기")

        choice = input("구매할 번호를 입력하세요: ")
        if choice == "0":
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(available):
            print("❌ 올바른 번호를 입력해주세요.")
            continue

        item, can_use = available[int(choice) - 1]
        if player.gold < item["price"]:
            print("❌ 골드가 부족합니다.")
            continue
        if item["type"] == "gear" and not can_use:
            print(f"❌ {player.job_class}는(은) 이 장비를 사용할 수 없습니다.")
            continue

        player.gold -= item["price"]
        if item["type"] == "potion":
            player.inventory[item["name"]] = player.inventory.get(item["name"], 0) + 1
            print(f"✅ {item['name']}을(를) 구매했습니다.")
        else:
            player.equip_item(item)
        print(f"남은 골드: {player.gold}골드")


def use_item_menu(player):
    print("\n🎒 사용 가능한 아이템:")
    items = [item for item in player.inventory if player.inventory[item] > 0]
    if not items:
        print("❌ 사용 가능한 물약이 없습니다.")
        return

    for i, item in enumerate(items, 1):
        print(f"{i}. {item} x{player.inventory[item]}")
    print("0. 취소")

    choice = input("사용할 아이템 번호를 입력하세요: ")
    if choice == "0":
        return
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(items):
        print("❌ 올바른 번호를 입력해주세요.")
        return

    selected = items[int(choice) - 1]
    player.use_potion(selected)


def main():
    player_name = input("캐릭터 이름을 입력하세요: ")
    
    # 직업 선택
    print("\n=== 직업 선택 ===")
    jobs = ["전사", "마법사", "권사", "도적", "용기사"]
    job_choice = get_choice(jobs)
    selected_job = jobs[job_choice - 1]
    
    player = Player(player_name, selected_job)
    print(f"\n✨ {selected_job} {player_name}이(가) 탄생했습니다!")
    player.show_status()
    
    current_chapter = 1
    current_stage = 1

    while current_chapter <= 10:
        chapter_data = CHAPTERS.get(current_chapter, {"name": f"알 수 없는 땅 {current_chapter}", "boss": "최종 진화형 보스"})
        
        print(f"\n==============================")
        print(f"   CHAPTER {current_chapter}: {chapter_data['name']}")
        print(f"==============================")

        while current_stage <= 10:
            print(f"\n📍 현재 위치: {current_chapter}챕터 - {current_stage}스테이지")
            choice = get_choice(["전투", "상태 보기", "상점", "아이템 사용", "휴식 (HP/MP 회복)"])

            if choice == 1:
                # 10번째 스테이지는 보스전
                is_boss = (current_stage == 10)
                num_monsters = 1 if is_boss else random.randint(1, 3)
                enemy = chapter_data['boss'] if is_boss else f"스테이지 {current_stage} 몬스터"
                
                win = battle(player, enemy, num_monsters, is_boss)
                
                if win:
                    reward = 30 if is_boss else 10 * num_monsters
                    player.gold += reward
                    print(f"\n✨ 몬스터를 처치했습니다! 골드 {reward}을 획득했습니다.")
                    current_stage += 1
                else:
                    if player.hp <= 0:
                        print("\n💀 당신은 쓰러졌습니다... 게임 오버.")
                        return
            elif choice == 2:
                player.show_status()
            elif choice == 3:
                show_shop(player)
            elif choice == 4:
                use_item_menu(player)
            elif choice == 5:
                player.hp = player.get_max_hp()
                player.mp = player.max_mp
                print("\n💤 충분한 휴식으로 HP와 MP가 모두 회복되었습니다.")

        print(f"\n🎉 축하합니다! 챕터 {current_chapter}를 정복하셨습니다!")
        current_chapter += 1
        current_stage = 1

    print("\n🏆 전설의 용사가 되셨습니다! 게임 클리어!")

if __name__ == "__main__":
    main()