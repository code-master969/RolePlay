import streamlit as st

st.set_page_config(page_title="推理游戏：《消失的古董》", layout="centered")

# 角色和线索数据
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
        "is_red_herring": True
    },
    "神秘电话": {
        "info": "有人半夜打电话给李先生，但内容未知。",
        "unlocked": False,
        "unlock_condition": "监控断片",
        "is_red_herring": True
    }
}

character_states = {
    "管家王": {
        "asked_relationship": False
    }
}

# 解锁逻辑
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

# 显示介绍
st.title("🕵️ 推理游戏：《消失的古董》")
st.markdown("通过调查线索和角色互动，找出古董失踪的真相。")

# 交互式选项
option = st.sidebar.radio("请选择操作", ["调查线索", "和角色交谈", "猜凶手"])

unlock_clues()

if option == "调查线索":
    st.subheader("调查线索")
    available = [clue for clue in clues if clues[clue]["unlocked"]]
    choice = st.selectbox("请选择要调查的线索：", available)
    clue = clues[choice]
    text = clue["info"]
    if clue["is_red_herring"]:
        text += " （提示：此线索可能是误导！）"
    st.info(text)

elif option == "和角色交谈":
    st.subheader("和角色交谈")
    name = st.selectbox("选择要交谈的角色：", list(characters.keys()))
    char = characters[name]
    st.markdown(f"**{name}的背景**：{char['background']}")
    question = st.selectbox("你想问什么？", list(char["questions"].keys()))
    
    if st.button("问"):
        if name == "管家王":
            if question == "你和李先生的关系如何？":
                character_states[name]["asked_relationship"] = True
            if question == "你是否欠债？" and not character_states[name]["asked_relationship"]:
                st.warning("这话题有点突然，我们先聊聊别的吧。")
            else:
                st.success(char["questions"][question])
        else:
            st.success(char["questions"][question])

elif option == "猜凶手":
    st.subheader("猜凶手")
    guess = st.selectbox("你猜测的凶手是谁？", list(characters.keys()))
    clue_count = sum(1 for c in clues.values() if c["unlocked"])
    if st.button("提交猜测"):
        if clue_count < 4:
            st.warning("线索不足，建议多调查和多和角色交流后再猜测。")
        elif guess == "管家王":
            st.success("🎉 恭喜你，猜对了！管家王因债务偷走了古董。游戏结束。")
        else:
            st.error("猜错了，请继续调查！")