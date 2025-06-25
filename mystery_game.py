def show_intro():
    print("欢迎来到推理游戏：《消失的古董》")
    print("通过调查线索和和角色互动，找出古董失踪的真相。\n")

def backgroudStory():
    print("在城市的西郊，有一栋典雅而低调的别墅，属于退休古董收藏家——李先生。他一生钟爱古物，尤其热衷于清代瓷器。他最引以为傲的，是一尊被誉为“清末孤品”的青花瓷观音像，价值连城，常年供奉在书房的玻璃柜中。")
    print("然而就在昨晚，李先生外出会友归来时，发现玻璃柜大开，那尊古董——不翼而飞。\n报警之后，警方封锁了现场，但因案发地点无破门痕迹，又缺乏目击者，只得暂时搁置。李先生焦急万分，决定请你——一位年轻而敏锐的推理爱好者，协助他调查此案。")
    print("这栋别墅只有三人知晓那尊古董的位置与价值：\n管家王：忠心耿耿，却最近常常心事重重；\n女儿小美：热爱艺术，对古董兴趣浓厚；\n邻居张先生：表面关系疏远，却总是神出鬼没。")
    print("案情扑朔迷离，线索零散分布在每一段对话、每一处细节之间。你需要逐步解锁线索，揭开表象之下的秘密……")

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
            "你为什么会把古董带到学校？": "只是为了展览展示，没想到会出事。",
            "你怎么看管家？": "他看起来有点拮据，总是小心翼翼地问工资什么时候发。"
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
        "asked_relationship": False,
        "talk_count": 0,
        "truth_unlocked": False
    },
    "提示获取": {
        "has_money_hint": False
    }
}

def ask_butler(question):
    state = character_states["管家王"]
    state["talk_count"] += 1

    if question == "你和李先生的关系如何？":
        state["asked_relationship"] = True
        return "我们一直很信任彼此。"

    elif question == "你是否欠债？":
        if not clues["银行卡流水"]["unlocked"] or not clues["催债信息"]["unlocked"]:
            return "这话题有点突然，我们先聊聊别的吧。"
        if not state["truth_unlocked"]:
            if state["talk_count"] < 3 or not character_states["提示获取"]["has_money_hint"]:
                return "我只是最近有点拮据，没什么大问题……"
            else:
                state["truth_unlocked"] = True
                return "……好吧，我确实欠了不少债。这一切都是为了还清它们。"

    elif question == "你昨晚去哪儿了？":
        return "我昨晚一直在整理书房，李先生可以作证。"
    
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
    }, "银行卡流水": {
        "info": "管家王最近有大量可疑的转账记录。",
        "unlocked": False,
        "unlock_condition": "管家行踪",
        "is_red_herring": False
    },
    "催债信息": {
        "info": "管家王最近接到多次催债电话，通话记录为证。",
        "unlocked": False,
        "unlock_condition": "银行卡流水",
        "is_red_herring": False
    },
    
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
    unlocked_clues = [clue for clue in clues if clues[clue]["unlocked"]]
    clue_map = {}  # 编号 -> 线索名
    for i, clue in enumerate(unlocked_clues, 1):
        hint = "（可能是误导线索）" if clues[clue]["is_red_herring"] else ""
        print(f"{i}. {clue} {hint}")
        clue_map[str(i)] = clue

    while True:
        choice = input("请输入想调查的线索编号（输入‘0’返回）：").strip()
        if choice == "0":
            return
        if choice in clue_map:
            clue_name = clue_map[choice]
            info = clues[clue_name]['info']
            if clues[clue_name]["is_red_herring"]:
                info += " （提示：此线索可能是误导！）"
            print(f"\n线索信息：{info}\n")
            break
        else:
            print("编号无效，请重新输入。")


def talk_character():
    print("\n可以交谈的角色：")
    role_map = {}
    for i, name in enumerate(characters.keys(), 1):
        print(f"{i}. {name}")
        role_map[str(i)] = name

    while True:
        choice = input("请输入角色编号（输入‘0’返回）：").strip()
        if choice == "0":
            return
        if choice in role_map:
            name = role_map[choice]
            char = characters[name]
            print(f"\n{name}的背景：{char['background']}\n")

            while True:
                # 管家王的动态问题处理
                if name == "管家王":
                    all_questions = ["你和李先生的关系如何？", "你昨晚去哪儿了？"]
                    if clues["银行卡流水"]["unlocked"] and clues["催债信息"]["unlocked"]:
                        all_questions.append("你是否欠债？")
                else:
                    all_questions = list(char["questions"].keys())

                print("可提问问题：")
                q_map = {}
                for i, q in enumerate(all_questions, 1):
                    print(f"{i}. {q}")
                    q_map[str(i)] = q

                q_input = input("请输入问题编号（输入‘0’退出交谈）：").strip()
                if q_input == "0":
                    break
                if q_input in q_map:
                    question = q_map[q_input]
                    if name == "管家王":
                        answer = ask_butler(question)
                        if answer:
                            print(f"{name}回答：{answer}\n")
                        else:
                            print(f"{name}看起来不想回答这个问题。\n")
                    else:
                        answer = char["questions"].get(question)
                        if answer:
                            print(f"{name}回答：{answer}\n")
                            if question == "你怎么看管家？":
                                character_states["提示获取"]["has_money_hint"] = True
                        else:
                            print(f"{name}看起来不想回答这个问题。\n")
                else:
                    print("编号无效，请重新输入。\n")
            break
        else:
            print("编号无效，请重新输入。\n")

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
    backgroudStory()
    while True:
        print("\n请选择操作：")
        print("1. 调查线索")
        print("2. 和角色交谈")
        print("3. 猜凶手")
        print("4. 退出游戏")
        choice = input("请输入操作编号：").strip()
        if choice == "1":
            investigate()
            unlock_clues()
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