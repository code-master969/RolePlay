def show_intro():
    print("欢迎来到推理游戏：《消失的古董》")
    print("通过调查线索和和角色互动，找出古董失踪的真相。\n")

characters = {
    "管家王": {
        "background": "年过五十，忠诚但经济拮据，负责李先生家中事务。",
        "hidden_clue": "他有大量未公开的债务，最近情绪低落。",
        "questions": {
            "你昨晚去哪儿了？": "我昨晚一直在整理书房，李先生可以作证。",
            "你是否欠债？": "这跟案子有什么关系？我为什么要欠债呢？",
            "你和李先生的关系如何？": "我们一直很信任彼此。"
        }
    },
    "女儿小美": {
        "background": "艺术学院学生，性格活泼，对父亲的古董非常感兴趣。",
        "hidden_clue": "曾偷偷将古董放进学校的展览中。",
        "questions": {
            "你喜欢那尊古董吗？": "当然，那是我最喜欢的收藏品。",
            "你昨晚在哪？": "我和朋友在画室，没有回家。",
            "你为什么会把古董带到学校？": "只是为了展览展示，没想到会出事。"
        }
    },
    "邻居张先生": {
        "background": "神秘邻居，偶尔来访，和李先生关系一般。",
        "hidden_clue": "最近突然买了辆新车，资金来源成疑。",
        "questions": {
            "你怎么看李先生？": "他是个好人，不过我不太清楚他的财务状况。",
            "你新车的钱从哪儿来？": "这是我的私事，与你无关。",
            "你昨晚在家吗？": "我昨晚出去了，没人在家能证明。"
        }
    }
}

character_states = {
    "管家王": {
        "asked_relationship": False
    }
}

def ask_butler(question):
    if question == "你和李先生的关系如何？":
        character_states["管家王"]["asked_relationship"] = True
        return "我们一直很信任彼此。"
    elif question == "你是否欠债？":
        if character_states["管家王"]["asked_relationship"]:
            return "这跟案子有什么关系？我为什么要欠债呢？"
        else:
            return "这话题有点突然，我们先聊聊别的吧。"
    elif question == "你昨晚去哪儿了？":
        return "我昨晚一直在整理书房，李先生可以作证。"
    else:
        return None

clues = {
    "门窗": {
        "info": "门窗完好，没有被破坏，但门锁有撬过的痕迹。",
        "unlocked": True,
        "is_red_herring": False
    },
    "监控断片": {
        "info": "监控录像在关键时刻出现断片。",
        "unlocked": False,
        "unlock_condition": "门窗",
        "is_red_herring": False
    },
    "管家行踪": {
        "info": "管家王昨晚加班，无人作证他的行踪。",
        "unlocked": False,
        "unlock_condition": "监控断片",
        "is_red_herring": False
    },
    "小美兴趣": {
        "info": "小美对古董非常感兴趣，曾将古董带去学校展览。",
        "unlocked": False,
        "unlock_condition": "管家行踪",
        "is_red_herring": False
    },
    "邻居新车": {
        "info": "邻居张先生最近买了辆新车，资金来源成疑。",
        "unlocked": False,
        "unlock_condition": "管家行踪",
        "is_red_herring": True  # 误导线索
    },
    "神秘电话": {
        "info": "有人半夜打电话给李先生，但内容未知。",
        "unlocked": False,
        "unlock_condition": "监控断片",
        "is_red_herring": True  # 误导线索
    }
}

def unlock_clues():
    changed = True
    while changed:
        changed = False
        for clue, data in clues.items():
            if not data["unlocked"]:
                cond = data.get("unlock_condition")
                if cond and clues.get(cond, {}).get("unlocked", False):
                    data["unlocked"] = True
                    changed = True

# 调查线索时加入重试
def investigate():
    print("\n可以调查的线索：")
    for clue, data in clues.items():
        if data["unlocked"]:
            hint = "（可能是误导线索）" if data["is_red_herring"] else ""
            print(f"- {clue} {hint}")
    print() 
    while True:
        choice = input("请输入想调查的线索名称（输入‘返回’取消）：").strip()
        if choice == "返回":
            return
        if choice in clues and clues[choice]["unlocked"]:
            info = clues[choice]['info']
            if clues[choice]["is_red_herring"]:
                info += " （提示：此线索可能是误导！）"
            print(f"\n线索信息：{info}")
            print() 
            break
        else:
            print("该线索尚未解锁或不存在，请重新输入。")
            print() 

def talk_character():
    print("\n可以交谈的角色：")
    for name in characters:
        print(f"- {name}")
    while True:
        choice = input("请输入想交谈的角色名称（输入‘返回’取消）：").strip()
        if choice == "返回":
            return
        if choice in characters:
            char = characters[choice]
            print(f"\n{choice}的背景：{char['background']}")
            print() 
            while True:
                ask = input("你想问什么？（输入“退出”结束交谈）\n可问问题示例：" + ", ".join(char["questions"].keys()) + "\n")
                if ask == "退出":
                    break
                if choice == "管家王":
                    answer = ask_butler(ask)
                    if answer:
                        print(f"{choice}回答：{answer}")
                        print()
                    else:
                        print(f"{choice}看起来不想回答这个问题。")
                        print() 
                else:
                    answer = char["questions"].get(ask)
                    if answer:
                        print(f"{choice}回答：{answer}")
                        print()
                    else:
                        print(f"{choice}看起来不想回答这个问题。")
                        print() 
            break
        else:
            print("角色不存在，请重新输入。")
            print()

# 只统计解锁的线索数量，不包括角色hidden_clue
def guess_suspect():
    suspect = input("你猜测的凶手是谁？请输入名字（管家王/女儿小美/邻居张先生）：").strip()
    unlocked_clues_count = sum(1 for c in clues.values() if c["unlocked"])
    if unlocked_clues_count < 5:
        print("线索不足，建议多调查和多和角色交流后再猜测。")
        print() 
        return False
    if suspect == "管家王":
        print("恭喜你，猜对了！管家王因债务偷走了古董。游戏结束。")
        print() 
        return True
    else:
        print("猜错了，请继续调查。")
        print() 
        return False

def main():
    show_intro()
    while True:
        unlock_clues()
        print("\n请选择操作：")
        print("1. 调查线索")
        print("2. 和角色交谈")
        print("3. 猜凶手")
        print("4. 退出游戏")
        choice = input("请输入操作编号：").strip()
        if choice == "1":
            investigate()
            print()
        elif choice == "2":
            talk_character()
        elif choice == "3":
            if guess_suspect():
                break
        elif choice == "4":
            print("游戏结束，欢迎下次再来！")
            break
        else:
            print("输入无效，请重新选择。")

if __name__ == "__main__":
    main()