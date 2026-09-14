"""
seed.py — Seeds the GARCS database with starter content: passages tagged
with a grade_band, and questions tagged with skill_tag (literal/inferential/
critical) and difficulty (easy/medium/hard), per Chapter 3.6.3.

Place this file in the same folder as your Phase 1 app.py and run:
    python seed.py

Grade-band convention used here (keep this consistent with your Chapter 3
write-up so it's documented somewhere):
    grade_band 1 -> Grades 5-6
    grade_band 2 -> Grades 7-8
    grade_band 3 -> Grades 9-10

Re-running this script is safe: it clears existing Passage/Question rows
first, so you won't get duplicates every time you re-seed during dev.

This gives you 6 passages x 3 questions = 18 questions, with at least one
question in every (skill_tag, difficulty) combination -- so
sequencing.pick_next_question() always has at least one candidate no
matter which skill/difficulty the engine targets. This is a STARTER set.
Your roadmap's target for a real pilot is 15-25 passages x 3-5 questions
each -- keep adding entries to PASSAGES below using the same structure.

Content note: these passages/questions were drafted for engineering
purposes (to give the adaptive engine real data to run against). Before
your pilot, it's worth having a reading/curriculum-literate reviewer (your
adviser, a co-author, or a teacher) sanity-check wording and grade-level
appropriateness -- content validity matters for a reading comprehension
thesis in a way that's hard for me to fully verify from here.
"""

from app import app, db, Passage, Question  # adjust if your Phase 1 file has a different name


PASSAGES = [
    {
    "title": "RACE Passage (high10024.txt)",
            "grade_band": 3,
            "grade_level_estimate": 10.8,
            "body": "One thinks of princes and presidents as some of the most powerful people in the world; however, governments, elected or otherwise, sometimes have had to struggle with the financial powerhouses called tycoons. The word tycoon is relatively new to the English language. It is Chinese in origin but was given as a title to some Japanese generals. The term was brought to the United States, in the late nineteenth century, where it eventually was used to refer to magnates who acquired immense fortunes from sugar and cattle, coal and oil, rubber and steel, and railroads. Some people called these tycoons \"capitals of industry\" and praised them for their contributions to U.S. wealth and international reputation. Others criticized them as cruel \"robber barons\", who would stop at nothing in pursuit of personal wealth.\nThe early tycoons built successful businesses, often taking over smaller companies to eliminate competition. A single company that came to control an entire market was called a monopoly. Monopolies made a few families very wealthy, but they also placed a heavy financial burden on consumers and the economy at large.\nAs the country expanded and railroads linked the East Coast to the West Coast, local monopolies turned into national corporations called trusts. A trust is a group of companies that join together under the control of a board of trustees. Railroad trusts are an excellent example. Railroads were privately owned and operated and often monopolized various routes, setting rates as high as they desired. The financial burden this placed on passengers and businesses increased when railroads formed trusts. Farmers, for example, had no choice but to pay, as railroads were the only means they could use to get their grain to buyers. Exorbitant   goods rates put some farmers out of business.\nThere were even accusations that the trusts controlled government itself by buying votes and manipulating elected officials. In 1890 Congress passed the Sherman Antitrust. Act, legislation aimed at breaking the power of such trusts. The Sherman Antitrust Act focused on two main issues. First of all, it made illegal any effort to interfere with the normal conduct of interstate trade. It also made it illegal to monopolize any part of business that operates across state lines.\nOver the next 60 years or so, Congress passed other antitrust laws in an effort to encourage competition and restrict the power of larger corporations.",
            "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
            "questions": [
                {
                    "prompt": "The Sherman Antitrust Act  _  .",
                    "choices": [
                        "affected only the companies doing business within state lines",
                        "sought to eliminate monopolies in favor of competition in the market-place",
                        "promoted trade with a large number of nations",
                        "provides a financial advantage to the buyer"
                    ],
                    "correct_index": 1,
                    "skill_tag": "inferential",
                    "difficulty": "medium",
                    "needs_review": True
                },
                {
                    "prompt": "One might infer from this passage that lower prices   _  .",
                    "choices": [
                        "are more likely to exist in a competitive market economy",
                        "usually can be found only in an economy based on monopolies",
                        "matter only to people who are poor and living below the poverty level",
                        "are regulated by the government"
                    ],
                    "correct_index": 0,
                    "skill_tag": "inferential",
                    "difficulty": "medium",
                    "needs_review": True
                },
                {
                    "prompt": "It seems likely that many Americans  _  .",
                    "choices": [
                        "believed that the trusts had little influence over government",
                        "expected the wealthy magnates to share money with the poor",
                        "did little to build up American business",
                        "were worried that trusts might manipulate the government"
                    ],
                    "correct_index": 3,
                    "skill_tag": "inferential",
                    "difficulty": "medium",
                    "needs_review": True
                }
            ]
        },
    
    {
            "title": "RACE Passage (high1227.txt)",
            "grade_band": 3,
            "grade_level_estimate": 11.0,
            "body": "Cholesterol                          Dr, Arlene Donar, Medical\nWatchers                                     Director SPECIAL PURCHASE\nALERT-JULY 2008\n\"BEST PRODUCT WE VE EVER SEEN\"--THIS REALLY-WORKS--ON SALE NOW\nNeed to ler your cho1esterol ?  We strongly recommend\nCholesterolblockTM, This really works, and how is the best time to buy, because of a special offer for the first 250 customers only for a limited time.\n*Takes cholesterol out of food, no matter what you eat.\n*Clinically demonstrated effective in university and hospital testing,.\n*Lowers cholesterol absorption up to 42% or more.\n*NO SIEDE EFFCTS unlike LiptorR, ZocorR, CrestorR& other commonly prescribed medications safe and effective.\n*Outsells all other brands on Internet every month.\nLIMITED TIME ONLY---Try Cholesterol Watchers free with purchase.",
            "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
            "questions": [
                {
                    "prompt": "If you happen to be the 200thcustomer to buy Cholesterolblock, you will  _  .",
                    "choices": [
                        "be able to buy it at a low price",
                        "be the luckiest one online",
                        "try it free of charge",
                        "change your diet"
                    ],
                    "correct_index": 0,
                    "skill_tag": "inferential",
                    "difficulty": "medium",
                    "needs_review": True
                },
                {
                    "prompt": "LiptorR, ZocorR,CrestorRare  _  .",
                    "choices": [
                        "diseases",
                        "side effects",
                        "medicines",
                        "cholesterol"
                    ],
                    "correct_index": 2,
                    "skill_tag": "inferential",
                    "difficulty": "medium",
                    "needs_review": True
                },
                {
                    "prompt": "CholesterolblackTM has the following advantages EXCEPT that  _  .",
                    "choices": [
                        "it helps take cholesterol out of whatever food you eat",
                        "it has been proved useful in hospital testing",
                        "it helps people absorb at least 42% cholesterol",
                        "it sells best on Internet every month"
                    ],
                    "correct_index": 2,
                    "skill_tag": "literal",
                    "difficulty": "medium",
                    "needs_review": True
                },
                {
                    "prompt": "Where can you most probably read this passage?",
                    "choices": [
                        "In a travel guide book.",
                        "On a university bulletin board.",
                        "In a health magazine.",
                        "In a doctor's prescription."
                    ],
                    "correct_index": 2,
                    "skill_tag": "literal",
                    "difficulty": "medium",
                    "needs_review": True
                }
            ]
        },
        {
                "title": "RACE Passage (middle1011.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.6,
                "body": "Many Chinese people like American country music( ),such as  the songs of John Denver. But still some people don't know when country music began.\nCountry music is from the folk music  of the Appalachian Mountains in the east of America. There, people sang while playing the violin and guitar. They sang about everyday life, love and their problems. So the songs were sometimes a little sad.\nOne of the most popular country music singers is John Denver, who is also quite famous to the Chinese. For Denver, music was a language that could bring the world together. He says music can bring people together. We will understand  each other better through  music. People are different in colour and they may speak different languages, but people are the same in mind and body . All of them love music and can understand music.\nThe world lost a great man when John Denver died in 1997. But his music and words will live on.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "John Denver is a great  _  singer.",
                        "choices": [
                            "English",
                            "Japanese",
                            "American",
                            "Chinese"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": ".American country music is from the  _  music of America.",
                        "choices": [
                            "pop",
                            "jazz",
                            "light",
                            "folk"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": ".\"Music was a language that could bring the world together\" means  people  _  .",
                        "choices": [
                            "can sing songs together",
                            "from all over the world sing the same songs",
                            "show their feeling through music and so they understand each other better",
                            "know language and music"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": ".John Denver died in  _  .",
                        "choices": [
                            "1997",
                            "1990",
                            "1996",
                            "1999"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": ".Which sentence is right?",
                        "choices": [
                            "Everyone knows when country music began.",
                            "Country music is from the jazz music.",
                            "John Denver is famous to Chinese people, too.",
                            "John Denver doesn't think music can bring people together."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
        },
        {
                "title": "RACE Passage (middle1031.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.0,
                "body": "An old man died and left his son a lot of money. But the son was a foolish young man, and he quickly spent all the money, so that soon he had nothing left. Of course , when that happened, all his friends left him. When he was quite poor and alone, he went to see Nasreddin, who was a kind, clever old man and often helped people when they had troubles.\n'My money has finished and my friends have gone', said the young man. 'What will happen to me now?' 'Don't worry, young man', answered Nasreddin. 'Everything will soon be all right again. Wait , and you will soon feel much happier.'\nThe young man was very glad. 'Am I going to get rich again then?' He asked Nasreddin.\n'No, I didn't mean that', said the old man. 'I meant that you would soon get used to being poor and to having no friends.'",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "An old man died and left his son  _  .",
                        "choices": [
                            "nothing",
                            "some gold",
                            "much money",
                            "only a house"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When the son was   _  , he went to see Nasreddin.",
                        "choices": [
                            "short of money",
                            "quite poor and sick",
                            "in trouble",
                            "quite poor and alone"
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The young man was very glad because Nasreddin said that  _  .",
                        "choices": [
                            "he would become rich again",
                            "he would soon feel much happier",
                            "he would become clever",
                            "he would have more friends"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": ".Nasreddin meant the young man  _  .",
                        "choices": [
                            "would get rich again",
                            "would get used to having nothing",
                            "would get used to being unhappy",
                            "would get out of poorness"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What this story tells us is  _  .",
                        "choices": [
                            "that money is everything",
                            "that money makes the mare go",
                            "to save each penny",
                            "that misfortune  tests the sincerity of friends"
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1035.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.6,
                "body": "Mrs. Baker's sister was ill. She had someone to look after her from Monday to Friday, but not at the weekend, so every Friday evening Mrs. Baker used to go off to spend the weekend with her at her home in a neighbouring town. But as Mr. Baker could not cook, she had arranged   for his sister to come over and spend the weekend looking after him at their home. This meant that Mr. Baker had busy time when he came home from work on Friday evenings. First he had to drive home from the railway station. Then he had to drive his wife to the station to catch her train. And then he had to wait until his sister's train arrived, so as to take her to his house.\nOf course, on Sunday evening he had to drive his sister to the station to catch her train back home, and then wait for his wife's train, so as to bring her home.\nOne Sunday evening, he had seen his sister off on her train and was waiting for his wife's arrival when a porter (  ), who had often seen him at the station, came over and spoke to him, \"You are having a lot of fun,\" he said, \" But one day one of those women is going to catch you with the other, and then you will be in real trouble!\"",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Who was ill?    _",
                        "choices": [
                            "Mr. Baker",
                            "Mrs. Baker",
                            "Mr. Baker's sister",
                            "Mrs. Baker's sister"
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Who looked after the sick person on weekdays?",
                        "choices": [
                            "Mr. Baker's sister",
                            "Mrs. Baker's sister",
                            "Mrs. Baker",
                            "Someone acting as a nurse"
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Why did Mr. Baker go to the railway station on Friday and Sunday evening?   _",
                        "choices": [
                            "Because he had to see his wife and sister off and brought them home.",
                            "To take his sister to his own home.",
                            "To bring his wife back home.",
                            "To look after his sister."
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Where did Mr. Baker spend the weekend?    _",
                        "choices": [
                            "At home",
                            "In his office",
                            "In his sister's home",
                            "In a neighbouring town"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Why did the porter say Mr. Baker would be in trouble?   Because   _  .",
                        "choices": [
                            "Mr. Baker was making fun of the two ladies",
                            "Mrs. Baker would laugh at her husband",
                            "He thought the two women are Mr. Baker's girl friends",
                            "The two ladies were playing games with Mr. Baker"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1045.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.3,
                "body": "Today Newtown is a clean place, but many years ago there were millions of rats there. The rats even attacked ( ) the cats and dogs. Sometimes many of them tried to bite men or women at night. The rats were very large in size and they harmed ( ) many people.\nThe city office ordered every one to kill rats. However, most people were lazy, so they did not kill many rats. The city office could do nothing with the citizens and could do nothing with the rats, either. Some time later, they had to pay some money for each dead rat. That made the people very happy. They at once began to kill rats. They got as many dead rats as they could. And some of them even stopped their own work to kill rats because they could get more pay. Every day a city official( ) put all the dead rats together. He was very busy doing that, because sometimes a man brought hundreds of them in one day. Two weeks later, there were not so many rats in the city as before,  but people still brought many dead rats to the city office. The city officials felt surprised at this but at last they found out people were stealing the dead rats they had collected. So the city official had to order his men to dig a big hole and put the dead rats in it. Soon there were no more rats and the city did not have to pay any more money for that.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The rats in Newtown were once   _",
                        "choices": [
                            "as big as cats",
                            "as dangerous as dogs",
                            "huge in size",
                            "run into cars there"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When the city office first ordered the citizens to kill rats, most people   _  .",
                        "choices": [
                            "had to pay for each dead rat",
                            "stole dead rats",
                            "were too lazy to kill rats",
                            "killed nearly all the rats very soon"
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "A big hole was dug so that   _  .",
                        "choices": [
                            "the rats could come out to attack people at night",
                            "people could take many rats",
                            "the people loved dead rats",
                            "people could not steal dead rats for money"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1061.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.8,
                "body": "Sun Liping, 6 , lives in a small village in Yunnan. Her biggest wish is to have running water in her home. All 35 families in Sun's village have a serious problem--- they don't have enough water. Every day, the villagers have to walk 20 minutes to get water.\nLast year, the worst _ since the 1950s hit Yunnan, making more than 2 million people short of drinking water. This year, the drought is even worse.\nNot only Yunnan, but many other provinces in China are short of water as well, such as Gansu and Qinghai.\nAccording to a report on February 17, each Chinese person has about 28% of the world's average  person's amount of available  water. Two thirds of China's cities are short of water and nearly 300 million people in rural areas don't have safe water for drinking.\nEvery drop of water is important. Waste a drop of water a day and you lose a bucket  a year. How can we use water in a smart way? Here are some tips for you to save water in your daily life:\n1. Put plastic bottles of water in your toilet to cut down the water waste when you flush   your toilet.\n2. Don't keep the water running while you're brushing your teeth or washing your face and hands.\n3. Use low-flow  shower heads .\n4. Use a bucket to collect shower water while you wait for it to warm up.\n5. Make your shower time shorter.\n6. Set up a rain bucket to collect rainwater for watering plants or flowers.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "What is the problem in Sun's village?",
                        "choices": [
                            "They don't have enough food.",
                            "They don't have enough water.",
                            "They have to walk far away to go to school.",
                            "There are fewer and fewer villagers."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following would lead to a waste of water?",
                        "choices": [
                            "Using low-flow shower heads.",
                            "Collecting shower water while waiting for it to warm up.",
                            "Taking a quick shower.",
                            "Keeping the water running while brushing one's teeth."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1071.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.5,
                "body": "Is it difficult for you to get up in the morning? Hiroyuki's bed will solve your problem! Here is how it works.\nThe bed is connected to an alarm clock. First, the alarm clock rings. You have a few minutes to wake up. Next, a tape recorder in the bed plays soft music. The tape recorder in Hiroyuki's bed plays a recording of his girlfriend. She whispered in a soft voice, \"Wake up, darling, please.\" After minutes later, Hiroyuki hears a recording of his boss. His boss shouts, \"Wake up at once , or you'll be late !\"\nIf you don't get up after the second recording, a mechanical \"foot\" in the bed will kick you in the head. The bed waits a few more minutes. What! You're still in bed! Slowly the top of the bed rises higher and higher. The foot of the bed goes lower and lower. Finally you slide off the bed and onto the floor. You are out of bed awake!\nHiroyuki's bed is not in stores. There is only one bed--- the bed Hiroyuki made for a contest. Maybe someday a company will make Hiroyuki's bed and sell it in stores. Maybe people will buy millions of beds. Then Hiroyuki will be rich. If the bed makes Hiroyuki rich, he won't need to work, and he won't need to get up early!",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The bed is useful to the people   _  .",
                        "choices": [
                            "who can't sleep well",
                            "who can't get up early",
                            "who go to bed early",
                            "who go to bed late"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The bed is not connected to   _   .",
                        "choices": [
                            "an alarm clock",
                            "a tape recorder",
                            "a TV",
                            "a mechanical \"foot\""
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What will finally happen to Hiroyuki if he doesn't get up ?",
                        "choices": [
                            "He will slide onto the floor .",
                            "A tape recorder will play a recording of his boss .",
                            "A mechanical \"foot\" will kick him in the head .",
                            "The bed will rise higher and higher"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which is TRUE of the following sentences ?",
                        "choices": [
                            "Hiroyuki's company has made many such beds .",
                            "Hiroyuki's bed is the only one made for a contest .",
                            "Hiroyuki has made a lot of money .",
                            "Hiroyuki needn't get up early now ."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1081.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.8,
                "body": "Daily Horoscope on May 5th\nAries:Everything is getting ready. You are in the right place at the right time. Cheer up and catch good chances.\nTaurus:If something isn't what you think, don't worry. Wait patiently and you will have a better chance. But a mistake now will bring you trouble.\nGemini:Your experience and ability will attract others' attention today. You'll be asked for your opinions, and you will be able to get everything you want.\nCancer: _ and you will make some extra money. This is a great day to go for interviews or talk to someone about your ideas.\nLeo : You'll have success at work but don't spend too much money. A short trip will bring good results.\nVirgo:If you don't know enough about something, keep away from it. Think before you take actions. Be honest, or you'll be in trouble.\nLibra : Joining a good group will make you catch a chance. Then you can get what you want.\nCapricorn :Don't believe anyone who pretends  to know everything. Do everything on your own.\nAquarius:Try your best to help others and you'll attract everyone's attention. Friendship is the most important thing to you.\nPisces:You may meet someone who will invite you to a talk or a meeting. Be careful enough or you'll make enemies.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Who has the best luck on May 5th?",
                        "choices": [
                            "A Gemini.",
                            "A Virgo.",
                            "A Leo.",
                            "A Pisces."
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Who needn't pay attention to others but depend on himself ?",
                        "choices": [
                            "A Libra.",
                            "A Cancer.",
                            "An Aquarius.",
                            "A Capricorn."
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1097.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.6,
                "body": "As young students, you have many dreams. These dreams can be very big, such as winning the Nobel Prize; they can also be small, such as becoming one of the best students in your class.\nOnce you find a dream, what do you do with it? Do you ever try to make your dream real? Follow Your Heart by Andrew Matthews, an Australian writer, tells us that making our dreams real is life's biggest challenge. You may think you're not very good at some school subjects, or that it is impossible for you to become a writer. Those kinds of ideas stop you from realizing your dream, the books says.\nIn fact, everyone can realize his dream. The first thing you must do is to remember what your dream is. Don't let it leave your heart. Keep telling yourself what you want every day and then your dream will come True faster. You should know that a big dream is, in fact, made up of many small dreams.\nYou must also never give up your dream. There will be difficulties on the road to your dreams. But the biggest difficulty comes from yourself. You need to decide what is the most important. Studying instead of watching TV will help you to get better exam results, while saving five yuan instead of buying an ice cream means you can buy a new book.\nAs you get closer to your dream, it may change a little. This is good as you have the chance to learn something more useful and find new hobbies.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Your dreams can be very   _  , such as becoming one of the best students in your class.",
                        "choices": [
                            "big",
                            "small",
                            "high",
                            "low"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Follow Your Heart is a   _   .",
                        "choices": [
                            "movie",
                            "song",
                            "book",
                            "dream"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What idea stops you from realizing your dream?",
                        "choices": [
                            "I can't be a writer.",
                            "I am good at some school subjects.",
                            "I think I am very great",
                            "I am the best student in our class."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Don't let   _   leave your heart.",
                        "choices": [
                            "your idea",
                            "your decision",
                            "your dream",
                            "your book"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Studying TV will help you to get better exam results   _   watching TV.",
                        "choices": [
                            "with",
                            "instead of",
                            "without",
                            "by"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1129.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.6,
                "body": "It's the end of class.When the bell rings, students of Luohu Foreign Languages School in Shenzhen quickly take out their telephones.They want to log on to their micro blogs   to check the interesting things.They want to see what have happened in the last hour.\nSince several years ago, more and more people have used micro blogs in our country.Recent surveys   shows that most students in middle schools have a micro blog and some even update   their blogs over five times per day.\n\"We learn many fresh and interesting things on micro blogs and they have become popular topics in class,\" said Kitty Jiang, 14.\"If you do not know about them, you are _ .\" It is also a great place for students to say something about themselves.\"My parents always ask me to study hard, and encourage me before exams, but it really gives me pressure  ,\" said Alan Wang, 15.\"I share these feelings on my micro blog.My friends always give me answers in the same situation.This makes me feel better.\"\nBut parents worry that micro blogging could be a waste of time.Some unhealthy information may even bring danger to kids, they said.\nMr Shen, a professor   asks parents not to worry too much as long as kids are not crazy about micro blogging.Maybe it can become a window for parents to understand their children.\"If parents can read their children's micro blogs, they'll know what they think, they can know more about their children and help them solve their problems,\" he said.He also gives some advice for kids.\n-Don't micro blog for more than one hour a day.\n-Never micro blog in class.\n-Try to talk face to face with people from time to time.\n-Don't believe all the information on a micro blog.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "According to the passage, what do students log on to their micro blogs to do?",
                        "choices": [
                            "check the things",
                            "write articles",
                            "listen to music",
                            "call their parents"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "From Mr Shen's words, what do micro blogging do?",
                        "choices": [
                            "It makes kids crazy while logging on to it.",
                            "It will bring a lot of unhealthy information.",
                            "It becomes a window to understand young kids.",
                            "It will not solve problems for kids"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following sentence is True according to the passage?",
                        "choices": [
                            "It's good for kids to micro blog for more than one hour a day.",
                            "Kids should believe all the messages on a micro blog because they are useful.",
                            "Many young people have written something on micro blogs since two years ago.",
                            "Kids should try to talk face to face with people, not just micro blogging."
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1132.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.5,
                "body": "In many parts of the world, people live to a healthy old age. What is the secret of their long lives?\nThree things are very important: fresh air, fresh food and a simple way of life. People who live in Himalayas  are famous for their long and healthy lives. They work near their homes in the clean mountains. They don't have buses, cars or trains. They don't sit all day in busy offices. They take more exercise and eat less food than people in the cities. They eat vegetables grown by themselves. They drink milk taken from their own cows. For years, the Hunzas of the Himalayas don't need doctors, for there is not much illness. They are happy and healthy people.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Which is NOT the life of the people living in Himalayas?",
                        "choices": [
                            "They work hard in the fields.",
                            "They eat vegetables grown by themselves.",
                            "They take more exercise and eat more food than people in the cities.",
                            "They drink milk taken from their own cows."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which one is NOT True about the people living in Himalayas?",
                        "choices": [
                            "They live a simple life in the mountains.",
                            "They grow vegetables and milk cows themselves.",
                            "When they are ill, they don't go to see doctors.",
                            "They don't sit all day in busy offices."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which is NOT the secret of long life?",
                        "choices": [
                            "Fresh air.",
                            "Fresh food.",
                            "A simple way of life.",
                            "A simple way of eating."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What are the Hunzas famous for?",
                        "choices": [
                            "Vegetables.",
                            "Milk.",
                            "Food.",
                            "Their long and healthy lives."
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "They do not need doctors, for   _   .",
                        "choices": [
                            "the doctors are not good",
                            "there is not much illness",
                            "there is no illness",
                            "they are happy"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1137.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.3,
                "body": "One day Jack met his good friend Sue in the park.A dog was looking up at the woman beside her.\nJack walked up to Sue and said, \"Hello, how are you? May I sit and talk with you for a moment?\" \"Of course, please sit down,\" Sue said.Jack sat down next to Sue on the bench, and they talked quietly together.The dog continued to look up at Sue, as if( ) waiting to be given some food.\n\"That's a nice dog, isn't he?\" Jack said, pointing at the animal.\n\"Yes, he is.He's handsome.He's strong and healthy.\"\n\"And hungry,\" Jack said.\"He hasn't taken his eyes off you.He thinks you've got some food for him.\"\n\"That's True,\" Sue said.\"But I haven't.\"\nThey both laughed and then Jack said, \"Does your dog bite ?\"\n\"No, \"Sue said, \" He's never bitten anyone.He's always gentle and friendly.\"\nHearing this, Jack decided to hold out his hand and touched the animal's head.Suddenly it jumped up and bit him.\n\"Hey!\" Jack shouted.\"You said your dog didn't bite.\"\nSue answered in surprise, \"Yeah, I did.But this is not my dog.My dog is at home.\"",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Jack and Sue were   _  .",
                        "choices": [
                            "friends",
                            "neighbours",
                            "classmates",
                            "brother and sister"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The dog looked at the woman because   _  .",
                        "choices": [
                            "the woman wanted to feed him",
                            "the woman was friendly",
                            "he was strong and healthy",
                            "he was hungry"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Jack touched the dog because he believed   _  .",
                        "choices": [
                            "the dog was handsome",
                            "Sue's dog was unfriendly",
                            "the dog belonged to Sue",
                            "Sue's dog was at home"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "We can guess from the story that   _  .",
                        "choices": [
                            "Sue gave a wrong answer",
                            "Jack made a mistake",
                            "the dog wasn't dangerous",
                            "both Jack and Sue liked the dog"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the Following can be the best title of the passage?",
                        "choices": [
                            "A Wrong Question",
                            "Sue's Dog",
                            "A pleasant talk",
                            "Sue's Friend"
                        ],
                        "correct_index": 0,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1148.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.5,
                "body": "Millions of people around the world cook their food on fire every day. People must spend lots of money on cooking _ . However, there is a much easier and cheaper way to cook food using energy from the sun.\nSun-cookers have been used for centuries. A Swiss scientist made the first sun-cooker in 1777. Today, people are using sun-cookers in many countries around the world. People use them to cook food and to heat drinking water.\nThere are three kinds of sun-cookers. The first is a box cooker. It is designed with a special wall that collects sun-shine into the box. A box cooker is good for slow cooking of a lot of food.\nThe second kind of sun-cooker is a panel cooker. It has several flat walls that concentrate the sun-shine on the food. People can build panel cookers quickly. They do not cost much. In Kenya, for example, panel cookers cost just two dollars.\nThe third kind of sun-cooker is a parabolic cooker. It has rounded walls that concentrate sunlight into the bottom of the cooker. Food cooks quickly in parabolic cookers. However, these cookers are hard to make. They must be moved again and again to follow the sun. Parabolic cookers can also cause burns and eye injuries if they are not used correctly.\nYou can make sun-cookers from boxes or heavy paper. They will not catch fire. Paper burns at 232degC. A sun-cooker never gets hotter than that. Sun-cookers cook food at low temperatures over long periods of time. This allows people to cook food and do other things at the same time.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "If you want to cook food quickly, which kind of sun-cooker is your best choice?",
                        "choices": [
                            "a box cooker",
                            "a panel cooker",
                            "a parabolic cooker",
                            "fire cooker"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which kind of sun-cooker costs very little?",
                        "choices": [
                            "a box cooker",
                            "a panel cooker",
                            "a parabolic cooker",
                            "fire cooker"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What is the best title of this passage?",
                        "choices": [
                            "How to Be a Good Cook?",
                            "Cooking Meals With the Sun",
                            "How to Save Energy?",
                            "Different Ways of Cooking"
                        ],
                        "correct_index": 1,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1155.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.9,
                "body": "Michael and Derek are good friends, but they like to pull each other's leg sometimes. One day during the holidays they decided to go to London together. They went to the station and bought their tickets. When the train came in, Michael broaden in first and without knowing it, dropped his ticket in the platform as he got into the carriage . Derek, who was close behind saw the ticket fall and quickly picked it up. Without a word to his friend, he put it in his pocket.\nAfter they had been in the train a little while, they heard the ticket inspector coming down the corridor, shouting, \"tickets, please!\" Michael looked for his and of course couldn't find it.\n\"Oh, dear, I can't find my ticket, Derek,\" he said.\n\"Have another look, Michael, it must be somewhere,\" said Derek.\n\"No, I can't find it anywhere. What shall I do?\"\n\"Perhaps you had better hide under the seat, then the inspector won't know you are here.\" So Michael crawled under the seat as fast as he could and lay perfectly still. Presently the door opened and in came the inspector, \"Tickers please!\" he said.\nDerek handed him two tickets and said, \"This is mine. The other belongs to my friend, who prefers to travel under the seat.\"",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Michael lost in his ticket  _  .",
                        "choices": [
                            "when he boarded the train",
                            "while he was getting into the carriage",
                            "as they went to the station",
                            "after they had been in the train for a little while"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which is True according to the passage?",
                        "choices": [
                            "Derek helped Michael look for the ticket.",
                            "Michael and Derek are good friends, but they sometimes fight each other.",
                            "Derek took Michael's ticket and hid it.",
                            "Michael didn't know who had picked up his ticket."
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When the inspector came, Michael   _  .",
                        "choices": [
                            "hid himself as quickly as he could",
                            "remained perfectly still",
                            "was looking for his ticket",
                            "turned to Derek for help"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In the passage \"they like to pull each other's leg\" means  _  .",
                        "choices": [
                            "they like to make fun of each other in a playful way",
                            "they like to help each other in time of need",
                            "they like to pull each other by the leg",
                            "they like to kick each other"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1160.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.4,
                "body": "\"Mum, did you hear anything? I, uh. I thought I saw an alien.\"\n\"Are you all right? Just a dream ! \"Mum answered.\nThen I went back to my room. As I walked to the window, I cried, I saw a little alien, no more than three feet tall, with big and black eyes. It tried to run between my legs and escape through the window. Although I was scared, for some reason, I squeezed   my legs together in time to catch it. It took out something and hurt me. I felt a terrible sense of nothingness and fainted  . Then I woke up.\nAt first, I could hardly move. I wasn't sure whether it was a dream or not. I pulled myself out of the bed and walked downstairs. I saw my mum in the kitchen. She was really getting my brother ready for school, wearing her pink clothes. Then I realized it was just a dream because in my dream she was wearing her work clothes.\nFrom then on, I always dreamt about aliens and all the dreams felt so real. At that time, I really thought maybe I had some kind of relationship with aliens. About two months later, I stopped having such dreams. Later I realized that l used to have those dreams because I always read books or watched TV programs about aliens before I fell asleep!",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "What did the writer first do when he saw the alien?",
                        "choices": [
                            "He was too scared to move.",
                            "He knew it was a dream and wasn't afraid.",
                            "He was so scared that he fainted.",
                            "He thought against the alien."
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The writer found that it was just a dream   _  .",
                        "choices": [
                            "as soon as he woke up",
                            "before he went downstairs",
                            "when he saw his mother",
                            "when he was hurt by the alien"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following is TRUE according to the passage?",
                        "choices": [
                            "The writer had the dream at night.",
                            "The writer's mother's work clothes might not be pink.",
                            "The writer's mother was worried about his dream.",
                            "When the writer had the dream, his family were sleeping."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Why did the writer use to have dreams about aliens?",
                        "choices": [
                            "He had some kind of relationship with aliens.",
                            "He was terribly ill.",
                            "He often did something about aliens before going to bed.",
                            "The dreams were all about the writer's real experiences."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1163.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.4,
                "body": "Dou Kou, a Chinese boy, is called \"the youngest writer in the world\". He has written 3 books so far. Dou Kou was born in Jiangsu Province in 1994. When he was 7 months old, his parents started working in over 30 different cities, such as Xi'an and Shenzhen. This kind of life gave him things to think and write about.\nWhen Dou Kou was 9 months old, he could speak and at the age of one he could say five to six hundred words. At 3, he could look up words in the dictionary. At 4, his father taught him to learn something. His parents like reading very much. So does he. At the age of 5, he began writing fairy tales.\nHis fairy tales are all from his life. One day, he found many mice in the house. They not only ate their food but also hurt his mother's hand. So he thought, \"If we give mice the stomachs (  ) of cows, they'll eat grass and it'll be helpful to people. \" This was his first fairy tale \"Change Stomachs for Mice\". At 6, he wrote a novel about his own life in different cities with his parents.\nNow, he studies well in a middle school. He has written his third book, the novel called \"Eyes of Childhood\". He says, \"I am not different from other children. I just wrote several books,",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "How many books has Dou Kou already finished writing?",
                        "choices": [
                            "3.",
                            "6.",
                            "9.",
                            "12"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Dou Kou began to use a dictionary  _  ,",
                        "choices": [
                            "when he wrote fairy tales",
                            "before his father taught him to study",
                            "after he went to school",
                            "when he kept a diary"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following is Not True?",
                        "choices": [
                            "Change Stomachs for Micewas Dou Kou' s first fairy tale",
                            "Dou Kou likes writing and reading as well.",
                            "Dou Kou's novels make him different from other children of his age.",
                            "Dou Kou's parents don't allow Dou Kou to write at his early age."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which is the best title   of this passage?",
                        "choices": [
                            "Three books by a child",
                            "How to write fairy tales",
                            "Dou Kou, the youngest writer",
                            "How to be a writer"
                        ],
                        "correct_index": 2,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1187.txt)",
                "grade_band": 2,
                "grade_level_estimate": 2.4,
                "body": "Old John went to see a doctor. The doctor examined and said, \" Medicine can't help you. You must have a good rest. Go to a quiet place for a month, go to bed early, drink some milk, walk a lot and smoke one cigar   a day.\"\n\"Thank you very much,\" said old John, \" I will do everything you say.\"\nA month later old John came to the doctor again. \" Well, I'm glad to see you. You look much younger.\" Said the doctor.\n\"Oh , doctor,\" said old John, \"I feel quite well now. I had a good rest. I went to bed early, I drank a lot of milk, and I walks a lot. Your advice certainly helped me. But you asked me to smoke one cigar a day, and the one cigar a day nearly killed   me at first. It's no joke to start smoking at my age.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The doctor   _  .",
                        "choices": [
                            "asked him to take some medicine",
                            "asked him not to take any medicine",
                            "didn't say any word about medicine",
                            "gave him some medicine"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Old John   _   after a month.",
                        "choices": [
                            "didn't get well",
                            "got well",
                            "was old",
                            "got bad"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which one is True?",
                        "choices": [
                            "Old John smoked before",
                            "Old John smoked less than  before",
                            "Old John didn't smoke before",
                            "Old John didn't smoke a cigar a day"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When Old John was ill, he looked  _  .",
                        "choices": [
                            "young",
                            "old",
                            "younger",
                            "older"
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The best title  of this passage should be  _  .",
                        "choices": [
                            "Old John",
                            "Old John is ill",
                            "The Doctor's Advice",
                            "The Doctor"
                        ],
                        "correct_index": 2,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1263.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.1,
                "body": "Alan is a 16-year-old boy. He is the only child in his family. Alan is an American high school student. He lives in New York. Art and music are his favourite subjects . He loves studying and also love sports. He usually goes swimming three or four times every week. Alan's father works in a restaurant  near New York. He likes swimming, too. So Alan often go swimming with his uncle. Cool water always make him happy. American students are different  from us. On Saturdays, he often has parties   with his friends and they always enjoy themselves. On Sundays, he usually studies at home and watches sports programs . His favourite drink is Coke, but Coke is an _ drink. He often eats vegetables and he often does some sports to keep healthy.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Alan's father is a   _  . .",
                        "choices": [
                            "teacher",
                            "waiter",
                            "reporter",
                            "student"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Alan likes   _  .",
                        "choices": [
                            "Art and music",
                            "singing and sports",
                            "studying and sports",
                            "A and C"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "How many people are there in Alan's family ?",
                        "choices": [
                            "1",
                            "3",
                            "4",
                            "5"
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What does Alan often do on Sundays ?",
                        "choices": [
                            "He often go swimming with his father.",
                            "He often has parties with his friends.",
                            "He usually studies at home and watch TV.",
                            "He always does some sports."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1292.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.1,
                "body": "It is Sunday today. Anna goes shopping with her mother. She wants her mother to buy a new coat for her. In Snoopy Shop, she finds a yellow coat. She tries it on. It's too small. She wants a big one, but the big one is not yellow. Anna doesn't like other colors.\"Let's go to another  shop to have a look.\" her mother says. Then they go to D.D.Cat Shop. The shop is big and they see many kinds of coats in different colors and sizes . Anna tries on a yellow one. It looks nice on her. So they take it for forty-five yuan.\n,.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Anna goes shopping with her   _  .",
                        "choices": [
                            "mother",
                            "father",
                            "friends",
                            "sister"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Anna wants a new   _  .",
                        "choices": [
                            "shirt",
                            "skirt",
                            "coat",
                            "dress"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The yellow coat is too   _   for Anna in Snoopy Shop.",
                        "choices": [
                            "long",
                            "big",
                            "short",
                            "small"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "_   is Anna's favorite color.",
                        "choices": [
                            "Yellow",
                            "Blue",
                            "Red",
                            "Green"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Anna's new coat is   _  yuan.",
                        "choices": [
                            "40",
                            "45",
                            "50",
                            "55"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle13.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.3,
                "body": "What is color? Why do some of the things around us look red, some green, others blue?\nColors are really made by deflected   light. We see color because most of the things reflect light. In the same way, if something is green, it reflects most of the green light. If something reflects all light, it is white. If it doesn't reflect any light, it is black.\nSome of the light is reflected and some is taken in   and turned into   heat  .The darker the color is, the less light is reflected, the more light is taken in. So dark-colored clothes are warmer in the sun than light-colored clothes.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "When something reflects light, we can   _  .",
                        "choices": [
                            "see its color",
                            "see its heat",
                            "not see its color",
                            "see nothing"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Something looks white because it reflects   _  .",
                        "choices": [
                            "some light",
                            "no light",
                            "all light",
                            "most light"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "the dark-colored clothes are warm because   _   is taken in.",
                        "choices": [
                            "more light",
                            "less light",
                            "more color",
                            "less color"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In summer   _   make people feel cool.",
                        "choices": [
                            "dark-colored clothes",
                            "red-colored clothes",
                            "green-colored clothes",
                            "light-colored clothes"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What's the best title of this passage(  )?",
                        "choices": [
                            "Dark color",
                            "Color",
                            "Heat",
                            "Clothes"
                        ],
                        "correct_index": 1,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1302.txt)",
                "grade_band": 2,
                "grade_level_estimate": 6.4,
                "body": "Vision-phones \nRadio,telephone and television are widely used in the world. When you switch on the radio, you can listen.But when you use a telephone,not only can you listen to others but also you can chat with them,however, you can't see anything at all. Television is much better than both of them. People can watch TV and listen to it,but they can't take part in what they see.\nToday, some people are using a type of telephone called vision-phone. With it two people who are talking can see each other.\nVision-phones can be of great use when you have something to show the person whom you are calling,It may also have other uses in the future.Some day you may be able to call up a library and ask to read a book right over your vision-phone. You may be able to do some shopping through it, too. Perhaps in the near future, vision-phones will come into wide use in our everyday life.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "According to the passage, we can guess that the  _   was invented last.",
                        "choices": [
                            "radio",
                            "vision-phone",
                            "telephone",
                            "television"
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Maybe the vision-phone can take the place of  _   some day.",
                        "choices": [
                            "the telephone",
                            "the radio",
                            "the television",
                            "all the above"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In the future, you can use a vision-phone to   _",
                        "choices": [
                            "ask an assistant to read a book for you",
                            "read a book",
                            "ask an assistant to bring you a book",
                            "ask an assistant to do some shopping for you"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1381.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.2,
                "body": "In a school some trouble was caused by the students. They are very naughty and didn't obey the school rules.They often fought with each other and they didn't forgive each other. One day a new teacher came to this school. When he heard that, he came up with a good idea.\nHe told each of his students to bring a clear plastic bag and a bag of potatoes to school. For every person they didn't want to forgive in their lives, they chose a potato, wrote the person's name on it, and put it in the plastic bag.\nSome of their bags were very heavy. They were then told to carry this bag with them everywhere for one week. They would put it beside their bed at night, on the seat when sitting in a car or on a bus, and next to their desk at school. Days of carrying the bags around with them made students get to know what a weight they were carrying in their minds. And they had to pay attention to it all the time so they didn't forget it or leave it in embarrassing   places. As time passed by, the potatoes went bad and smelt nasty.\nToo often we think of _ as a gift to other people, and it clearly is for ourselves! If we choose to keep our sadness and hatred   in our hearts, we will have to carry them around all our lives. After that, the students got on well with each other and didn't fight anymore. Learn to forgive , and you will be happier at the same time.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The new teacher asked the students to bring   _   to school.",
                        "choices": [
                            "a clear plastic bag of potatoes",
                            "a clear plastic bag and a potato",
                            "some clear plastic bags of potatoes",
                            "a clear plastic bag and a bag of potatoes"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "They wrote the person's name on the potato, who  _  .",
                        "choices": [
                            "they liked",
                            "they didn't forgive",
                            "hated them",
                            "liked them"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "From this passage we can know that   _  .",
                        "choices": [
                            "we should learn to forgive",
                            "we should know something about potatoes",
                            "we shouldn't use plastic bags",
                            "we should take potatoes to school"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of following is NOT True?",
                        "choices": [
                            "Tolerance is a gift for other people and ourselves.",
                            "Carrying a bag of potatoes made the students embarrassed.",
                            "The students had to take bags of potatoes with them everywhere.",
                            "The students had to take bags of potatoes with them for about two weeks."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1386.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.1,
                "body": "Good health needs a good sleep. Going to bed before you're tired. Not eating or reading in bed. Go to bed at the same time before midnight and get up at the same time. Your body likes routine   for a good night's sleep.\nSTAY FREE OF FLU\nStudies show that a cold or flu virus   can live on our hands for long. So wash all parts of your hands often with soap and water. For more ways to prevent  the spread of flu, please call HealthLine at 1800 848 1313.\nORAL   HEALTH\nBrush your teeth twice daily and visit the dentist at least once a year. The mouth is a mirror  of disease . The oral examination  is not only for the health of teeth, but the whole body. For more of it, please visit www. mydr. com. au.\nFIT FOR LIFE\nStudies have shown that many diseases have something to do with less or no physical   activity. Try to do it for 30 minutes a day, 5 days or more a week. For more information, please call HealthLine at 1800 438 2000.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "If you want to get a good sleep, you'd better   _  .",
                        "choices": [
                            "go to bed after you're tired",
                            "go to sleep at midnight",
                            "follow the bedtime routine",
                            "eat something or read in bed"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "To prevent from catching a cold or flu, it's good for you   _  .",
                        "choices": [
                            "to clean your fingers often",
                            "to brush your teeth twice daily",
                            "to get up early every morning",
                            "to wash all parts of your hands"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "You should visit the dentist at least once a year, because   _  .",
                        "choices": [
                            "the oral examination is necessary",
                            "you don't often brush your teeth",
                            "some diseases may be in the mirror",
                            "you don't have a good night's sleep"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Studies have shown that many diseases have something to do with   _  .",
                        "choices": [
                            "having no oral examination",
                            "washing hands with cold water",
                            "sleeping too late sometimes",
                            "doing little physical activity"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When you want to learn more about the flu, you can   _  .",
                        "choices": [
                            "visit www. mydr. com. Au",
                            "call HealthLine at 1800 848 1313",
                            "visit the dentist in your place",
                            "call HealthLine at 1800 438 2000"
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1388.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.2,
                "body": "Andrew Engel was puzzled. He was sitting in class, but had no idea what the other students were talking about. He had done his homework, paid attention to lectures, and taken notes, but nothing was familiar. \"Everyone is so much cleverer than I am,\" he thought. It was a strange feeling, as he was always a good student in high school.\nHe felt even more puzzled a few days later. He got lost on his way to his favorite cinema. What's worse, he began having trouble finding the right words when speaking. He asked, \"What's for dinner, Mom?\" after he had just eaten. Poor Andrew, he was only 15!\nHis parents were worried and took Andrew to see a doctor. A brain scan  made it clear: Andrew had a malignant brain tumor  . It was pressing on the part of the brain that makes new memory. He should be operated on as soon as possible. Andrew was _ !\nDoctors removed the tumor, but Andrew's memory was still poor. He was told he would probably never go back to school. Andrew was eager to enter a university, but it seemed that his dream wouldn't come True.\n\"Even though they told me this, I knew I wanted to go back to school,\" Andrew said. \"I wanted to get my memory back.\"\nAndrew began by auditing  an English class at a nearby school. In class, he took notes carefully and read his notes several times a day, then typed them again and again. He studied twelve hours a day, seven days a week. He worked ten times harder than other students. In 2007, at age 29, he graduated from a local university. Six months later, Andrew found a job.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Andrew's strange behavior  including all the following except  _  .",
                        "choices": [
                            "having no idea what the other students were talking about",
                            "getting lost on his way to his favorite cinema",
                            "having trouble finding the right words when speaking",
                            "not knowing who he was"
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The tumor in Andrew's brain   _  .",
                        "choices": [
                            "didn't damage his memory",
                            "didn't have to be removed",
                            "caused his forgetfulness",
                            "is still in his brain"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Andrew studied very hard at the nearby school because   _  .",
                        "choices": [
                            "he wanted to realize his dream",
                            "he liked to stay with other students",
                            "he wanted to forget his illness",
                            "his parents wanted him to do so"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following is the best title of the article?",
                        "choices": [
                            "A man with an amazing brain",
                            "An unusual story of memory lost and found",
                            "How to improve your memory",
                            "Never lose your memory"
                        ],
                        "correct_index": 1,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1390.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.5,
                "body": "Dear Sally, Please take these things to your brother Bob: his dictionary, pen, notebook, keys, and a baseball. The dictionary is on the bed. The pen is in the pencil case. I put the pencil case on the sofa. The notebook is on the desk. The keys are on the dresser. The baseball is under the bed. Thanks, Grandma\n,.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Sally is Bob's   _  .",
                        "choices": [
                            "sister",
                            "aunt",
                            "mom",
                            "grandma"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Where's Bob's dictionary?",
                        "choices": [
                            "On the bed.",
                            "On the sofa.",
                            "On the desk.",
                            "On the dresser."
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The   _   is / are under the bed.",
                        "choices": [
                            "pen",
                            "notebook",
                            "keys",
                            "baseball"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Grandma tells   Sally to take   _   things to Bob.",
                        "choices": [
                            "three",
                            "four",
                            "five",
                            "six"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1417.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.2,
                "body": "When I was a little girl, my family lives in a small village. There was a very beautiful river near my home. The water was clean and cool. I liked to go fishing there with mom. We would catch fish, look for clams and play in the water. There were also a lot of  birds near the river. We would spend all day watching the birds. Life was beautiful and wonderful in the old days.\nNow my family lives in the city. Last Sunday my daughter asked me to take her to see the beautiful river I was always talking about. \"I want to go fishing there with you and Grandma ao much,\" she said.\nWhen we went to the river, we only saw a factory and a mountain of garbage . My mom was surprised, my daughter was quite _ and I was sad--the river was my best friend. I grew up with it. Now there are no fish in it; the birds are gone, too. I hear it crying for help. But what can I do ?",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Where was the writer born?",
                        "choices": [
                            "In a city",
                            "In a village",
                            "In a foreign country",
                            "In a mountain"
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When the writer went back to see the river, what did she find?",
                        "choices": [
                            "The pollution in the river was very serious.",
                            "The river was a good place for children to play.",
                            "Bird-watching was more and more popular along the river.",
                            "There were many more fish in the river."
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Who is \"Grandma\" in the reading?",
                        "choices": [
                            "The writer's daughter",
                            "The writer's mom",
                            "The writer",
                            "The writer's grandmother"
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What did the writer mean when she said, \"I grew up with it\"?",
                        "choices": [
                            "She helped clean the garbage out of the river.",
                            "She spent much time playing around the river.",
                            "She had many friends who lived near the river.",
                            "She grew well by eating fish and clams from the river."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1422.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.2,
                "body": "Most people who work in the offices have a boss, so do I. But my boss is a little unusual. What's unusual about him? It's a big dog. Many men have dogs, but few men bring their dogs to the office every day. My boss's dog, Robinson, is a big and brown one. My boss brings him to work every day. He takes the dog to meetings and he takes the dog to lunch. When there is a telephone call for my boss, I always know if he is in the office. I only look under his desk. If I see something brown and hairy under it, I know my boss is somewhere in the office. If there is no dog, I know my boss is out.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "People  _  bring dogs to the office.",
                        "choices": [
                            "usually",
                            "often",
                            "seldom",
                            "sometimes"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "My boss is Robinson's  _  .",
                        "choices": [
                            "boss",
                            "master",
                            "friend",
                            "teacher"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Robinson goes to meetings  _  my boss.",
                        "choices": [
                            "for",
                            "without",
                            "instead of",
                            "with"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Robinson is always under the desk if the boss is  _  .",
                        "choices": [
                            "in the office",
                            "at the meetings",
                            "out of the office",
                            "out of the work"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The passage tells us the boss  _  the dog very much.",
                        "choices": [
                            "looks like",
                            "hates",
                            "likes",
                            "dislikes"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1427.txt)",
                "grade_band": 2,
                "grade_level_estimate": 6.3,
                "body": "I felt very sad not to be able to get the ticket for the film Titantic last Friday. I learned in the newspaper that ticket could be bought at the cinema box office   in Richland Hill every day between 10:00 and 4:00. Because I work from 9:00 to 5:30, the only time I could go to the cinema was during my 45-minute lunch time. It is a pity that the cinema is on the other side of the town, and the bus service between my office and Richland Hills is not very good. But if you are lucky, you can make the round  trip in 45 minute.\nLast Monday I stood at the bus stop for fifteen minutes, waiting for a bus. By the time I saw one come around the corner, there was not enough time left to make the trip---- so I had to go back to the office. The same thing happened on Wednesday. On Thursday my luck changed, I got on a bus right away and arrived at the cinema in twenty minutes. But when I got there, I found a long line of people at the box office. I heard one man say he had been waiting in line for fifty-five minutes. I found that I would not have enough time to wait in line, I caught the next bus and went back across the town.\nBy Friday I understood my only hope was to make the trip by car.it was not cheap,but I felt it would be worth ot to see the film. The trip by car only took 10 minutes, but it felt like one hour to me. When I reached the cinema, I was _ to see that nobody was waiting in line. But quickly found out that it was because they had already sold all the tickets.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "It seems that the writer of the story works  _  .",
                        "choices": [
                            "in a small town",
                            "in Richland Hills",
                            "on a farm near the town",
                            "at a bus service Center"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "He tried to go to the cinema bo buy a ticket but really got there  _  .",
                        "choices": [
                            "five times",
                            "four times",
                            "three times",
                            "twice"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following is True according to the story?",
                        "choices": [
                            "The writer was too busy to have time for a rest during the day.",
                            "The buses running between his office and Richland Hills were always on time on Thursday.",
                            "He could buy the tickets neither before nor after work hours.",
                            "It always took him about twenty minutes to get to the cinema by bus."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What's the title of the story?",
                        "choices": [
                            "How to Get a Ticket",
                            "Tickets Sold out",
                            "A Wonderful Film",
                            "The Way to the Cinema"
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1438.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.2,
                "body": "The weather is getting warmer and warmer. It is fun to play outside, but people are afraid to play outside these days, because of the H7N9 virus. The H7N9 virus is one type of influenza A H7 viruses. It is a new type of bird flu. Influenza A H7 viruses mainly affectbirds but sometimes they can also affect humans. Most people infected with H7N9 virus look like they had a common flu. They had a fever, a cough and shortness of breath. Some had bad pneumonia. This March, H7N9 virus hit Shanghai, Anhui, Jiangsu and Zhejiang. Up until April 11th, the number of people infected had reached 35. Nine of these people died.\nBut don't be afraid , some cases are curable. A 4-year-old boy in Shanghai and a 67-year-old man in Hangzhou got the virus, and they are getting better. Besides, it's not easy to be infected by the H7N9 virus.\nThere are some ways to save ourselves from this. First, wash your hands with soap and running water before you eat and after you use the toilet. You should do the same after you touch animals or animal waste. Second, cover your nose and mouth with your elbow when coughing. Third, you should have a good rest and do some exercises, so your body can become strong enough to beat the virus.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "How's the weather during these days?",
                        "choices": [
                            "cold",
                            "warm",
                            "hot",
                            "cool"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "How many people have been infected H7N9 until April 11th?",
                        "choices": [
                            "35",
                            "25",
                            "45",
                            "30"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which place didn't find H7N9 in March?",
                        "choices": [
                            "Shanghai",
                            "Jiangsu",
                            "Zhejiang",
                            "Beijing"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which sentence is not True about the H7N9?",
                        "choices": [
                            "It is a new type of bird flu.",
                            "It is very easy to be infected by the H7N9.",
                            "Some of the H7N9 cases are curable.",
                            "Most people infected with H7N9 virus look like they had a common flu."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "How can we save ourselves from the H7N9 virus?",
                        "choices": [
                            "Wash your hands before you eat and after you use the toilet, touch animals or animals waste.",
                            "Cover your nose and mouth with your elbow when coughing.",
                            "Have a good rest and do some exercise to make your body strong enough.",
                            "All of above."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1455.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.0,
                "body": "A wise man was visiting a village with his students. He found a group of family members shouting in anger at each other. He turned to his students and asked: \"Why do people shout in anger at each other?\"\nHis students thought for a while, and one of them said: \"Because when we lose our calm, we shout.\"\n\"But, why should you shout when the other person is just next to you? You can just as well tell him what you have to say in a soft manner,\" said the wise man.\nStudents gave some other answers but none were any good.\n\"When two people are angry at each other, their hearts become distanced,\" the wise man explained. \"To cover that distance they must shout to be able to hear each other. The angrier they are, the louder they will have to shout to hear each other and cover that great distance.\"\nThe wise man then gave an example: \"What happens when two people fall in love? They don't shout at each other but talk softly because their hearts are very close. When they love each other even more, what happens? They don't need to talk. They only look at each other and that's all. That is how close two people are when they love each other.\"\nHe looked at his students and said: \"So when you argue, do not let your hearts get distant. Do not say words that distance you from others. Otherwise, there will come a day when the distance is so great that you will not find the path to return.\"",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "What did they find when a wise man and his students were visiting a village?",
                        "choices": [
                            "A group of people were traveling there.",
                            "A group of family members were playing there.",
                            "His students were shouting with a group of people.",
                            "A group of family members were shouting at each other angrily."
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "One of the students thinks family members shout at each other because  _  .",
                        "choices": [
                            "they are not friends",
                            "they don't like each other",
                            "they lose their calm",
                            "they are far from each other"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What will happen when two people are angry with each other?",
                        "choices": [
                            "They fight with each other.",
                            "Their hearts become distanced.",
                            "They are far away from each other.",
                            "They are too angry to say a word."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What will usually happen to two people at first when they fall in love with each other according to the passage?",
                        "choices": [
                            "They talk softly.",
                            "They shout at each other.",
                            "They talk more.",
                            "They don't say anything to each other."
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What's the topic of the passage?",
                        "choices": [
                            "Shouting is bad.",
                            "Don't shout.",
                            "Cover the distance with love.",
                            "The distance of love."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1463.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.5,
                "body": "There are fifty students in our class. There are twenty-four boys and twenty-six girls. Some students live near the school, and some others live far from school. About half of the students usually come to school by bike. They often get to school at a quarter to seven. About fifteen students often come to school by bus. They often get to school very early, too. Another ten students come to school on foot. Their homes are near the school, but they are often late for school, because they get up late.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "_   live near the school.",
                        "choices": [
                            "Some of the students",
                            "Half of the students",
                            "No students",
                            "All the students"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "_   students come to school by bike.",
                        "choices": [
                            "Twenty-five",
                            "Twenty-four",
                            "Twenty-three",
                            "Fifty"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Ten of the students   _  .",
                        "choices": [
                            "come to school by bike",
                            "come to school late",
                            "come to school very early",
                            "live in the school"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Some students get to school by bike at   _  .",
                        "choices": [
                            "7:35",
                            "7:30",
                            "6:45",
                            "6:30"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "_   students come to school on foot.",
                        "choices": [
                            "Thirty",
                            "Twenty",
                            "Thirty-eight",
                            "Ten"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle148.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.2,
                "body": "Mr. Green was traveling around the country in his car. One evening he was driving along a road and looking for a small hotel when he saw an old man at the side of the road. He stopped his car and said to the old man, \"I want to go to the Sun Hotel. Do you know it?\"\n\"Yes.\" The old man answered. \"I'll show you the way.\"\nHe got into Mr. Green's car and they drove for about twelve miles. When they came to a small house, the old man said, \"Stop here.\"\nMr. Green stopped and looked at the house. \"But this isn't a hotel.\" He said to the old man.\n\"No,\" the old man answered, \"This is my house. And now I'll show you the way to the Sun Hotel. Turn around and go back nine miles. Then you'll see the Sun Hotel on the left.\"",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Where did Mr. Green want to sleep that night?",
                        "choices": [
                            "In his car.",
                            "In his own house.",
                            "In a hotel.",
                            "In the old man's house."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Why did Mr. Green stop his car?",
                        "choices": [
                            "Because he found a hotel.",
                            "Because the lights were red.",
                            "Because he saw an old man.",
                            "Because he saw a friend."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Where did the old man promise  to take Mr. Green?",
                        "choices": [
                            "To Mr. Green's house.",
                            "To the old man's house.",
                            "To the SunHotel.",
                            "To the country."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Why didn't the old man stop Mr. Green when they passed the hotel?",
                        "choices": [
                            "Because he wanted Mr. Green to sleep in his house.",
                            "Because he wanted to get home.",
                            "Because he didn't see the hotel.",
                            "Because he didn't know the hotel."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "How far was it from the place where Mr. Green met the old man to the Sun Hotel?",
                        "choices": [
                            "About nine miles.",
                            "About three miles.",
                            "About twenty-one miles.",
                            "About twelve miles."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1554.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.9,
                "body": "Peter was getting ready to graduate from the college. He loved a beautiful sports car for many months, and knew his father could well afford it for him. He told his father all that he wanted.\nAs the graduation day was coming near, Peter had got nothing from his father. On the morning of his graduation, his father called him into his study. He told his son how proud he was to have such a good son, and told how much he loved him. Then he gave his son a beautiful gift box. He opened the box, finding a lovely book, a Bible , with the young man's name in it. Angrily he raised his voice to his father and said, \"With all your money you give me a Bible?\" He then ran out of the house, leaving the Bible.\nMany years later, Peter was very successful in business. He had a beautiful house and a wonderful family. Realizing his father was old, he thought he should go to see him. He had not seen him since that graduation day. Unfortunately, he was told that his father had died.\nWhen he reached his father's house, he began to take care of his father's papers. And then he found the Bible, just as he had left it years ago. With tears, he opened it and began to turn the pages. As he was reading, from the back of the Bible dropped a car key. That was the key to the sports car he wanted so much. Sudden sadness and regret  filled his heart.\nSometimes we don't realize the good luck that we already have because we don't know the gift box is packed in a different way. The gift box may be the door to happiness. It is just waiting for us to open.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The son would like his father to buy him  _  .",
                        "choices": [
                            "a beautiful house",
                            "a Bible",
                            "a beautiful box",
                            "a sports car"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The son ran out of the house angrily because   _  .",
                        "choices": [
                            "his father said something wrong to him",
                            "his father gave him nothing",
                            "he thought his father only gave him a Bible",
                            "his father didn't love him"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Many years later, the son  _  .",
                        "choices": [
                            "was told his father was still healthy",
                            "became a successful man",
                            "had a hard life",
                            "went to see his father quite often"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "How did the son feel when he got the car key?",
                        "choices": [
                            "Excited and happy.",
                            "Worried and sad.",
                            "Disappointed and upset.",
                            "Sad and regretful."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "From the story, the writer wants to tell us   _  .",
                        "choices": [
                            "we may miss good luck because they are not packed as we expect",
                            "we should look after our parents carefully",
                            "our parents will give us everything we ask for",
                            "we should accept any gift that our parents give us"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle157.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.6,
                "body": "October 1st, 2011\nDear Ann,\nI hope that you and your children will be here in two weeks. My husband and I will  go to meet you at the train station. Our town is small but it is nice and beautiful. Your son Tom can go to the sports center every day. He can play games and go swimming there. Jill  is also lucky. My son has a cat and two sheep and I have two horses. She can play with them all day.\nPlease don't worry. I'm sure you'll have a good time here. See you soon.\nBest wishes,\nLinda",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The letter was from   _  .",
                        "choices": [
                            "Ann",
                            "Linda",
                            "Jill",
                            "Tom"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Ann and her children will go to Linda's home on about  _  .",
                        "choices": [
                            "October 1",
                            "October 7",
                            "October 15",
                            "October 28"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Linda lives in   _   .",
                        "choices": [
                            "a big city",
                            "a small town",
                            "a big town",
                            "a country"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Ann and her children are going to Linda's home   _  .",
                        "choices": [
                            "by bus",
                            "by car",
                            "on foot",
                            "by train"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "From the letter we know that Tom loves  _  and Jill loves  _  .",
                        "choices": [
                            "sports; animals",
                            "music; animals",
                            "sports; dancing",
                            "animals; sports"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1584.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.9,
                "body": "The ant  works every day but the monkey plays in the tree every day in summer. One day the ant is carrying some candy to her home. Her home is next to a big tree. The monkey is playing games in the tree. He says to the ant, \"Why are you working every day? It is warm today. Don't work. Come and play games with me.\" But the ant says, \"Winter will come and it will be very cold. I want to _ lots of food. I will sleep all day in winter.\"\nWinter will not come soon. You can work in autumn,\" says the monkey.\nSummer and autumn are over. There is snow  everywhere. The monkey can't find any food. Do you know what will happen?",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "_  works every day in summer.",
                        "choices": [
                            "The mouse",
                            "The monkey",
                            "The ant",
                            "The dog"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In summer the monkey   _   every day.",
                        "choices": [
                            "sleeps",
                            "plays in the tree",
                            "eats bananas",
                            "walk the ant"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "One day the ant is carrying   _   to her home.",
                        "choices": [
                            "some candy",
                            "some bread",
                            "some meat",
                            "some rice"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which is TRUE?",
                        "choices": [
                            "The ant asks the monkey not to work",
                            "The ant's home is next to a big tree.",
                            "The house is clever.",
                            "The monkey will sleep all day in winter because he has lots of food."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1593.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.6,
                "body": "A kind of little cars may some day take the place of today's cars. If everyone drives such cars in the future,there will be less pollution from the cars. There will also be more space for parking cars in cities,and the streets will be less crowded. Three such cars can park in the space now needed for one car of the usual size.\nThe little cars will cost much less to own and to drive. Driving will be safer,too,as these little cars can go only 65 kilometers an hour. The cars of the future will be fine for getting around a city,but they will not be useful for long trips. Little cars will go 450 kilometers before needing to stop for more gas .\nIf big cars are still used along with the small ones,two sets of roads will be needed in the future. Some roads will be used for the big,quick cars and other roads will be needed for the slower,smaller ones.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "There is much pollution from the cars today because  _  .",
                        "choices": [
                            "people drive big cars",
                            "the cars go 65 kilometers an hour",
                            "people drive small cars",
                            "the cars can go 450 kilometers an hour"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The usual size of cars today are  _  that of future cars.",
                        "choices": [
                            "smaller than",
                            "the same as",
                            "three times as large as",
                            "a little larger than"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "We can learn from the passage that  _  .",
                        "choices": [
                            "big cars cost less to own and to drive",
                            "the cars of the future will be much smaller than today's cars",
                            "big cars are not useful for long trips",
                            "small cars are faster than big ones"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The street will be less crowded in the future because  _  .",
                        "choices": [
                            "there will be fewer cars",
                            "there will be fewer people in the street",
                            "driving future cars will be safe",
                            "future cars will be much smaller"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Two sets of roads may be needed in the future because  _  .",
                        "choices": [
                            "there will be too many cars in the future",
                            "more and more people will get around a city",
                            "big cars will be used along with the small ones",
                            "it looks more beautiful to have two sets of roads"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle163.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.9,
                "body": "When you are reading something in English, you may often meet with a new word. What's the best way to know it?\nYou may look it up in the English-Chinese dictionary. It will tell you a lot about the word: the pronunciation, the Chinese meaning and how to use the word. But how can you know where the word is thousands of English words? How to find it in the dictionary both quickly and correctly?\nFirst, all the English words are arranged  in the letter order. In the dictionary you can first see the words beginning with letter A, then B, C, D.... That means, if there are two words \"desert\" and \"pull\", \"desert\" will be certainly before \"pull\". Then if there are two words both beginning with the same letter, you may look at the second letter. Then the third, the fourth... For example, \"pardon\" is before \"plough\", \"judge\" before \"just\", etc.\nDo you understand how to look up in the dictionary?\nThe dictionary will be your good friend. I hope you'll use it as often as possible in your English study.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "This passage is about  _  .",
                        "choices": [
                            "new words in writing",
                            "different dictionaries",
                            "the best way of reading",
                            "using an English-Chinese dictionary"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In the dictionary you may not find  _  .",
                        "choices": [
                            "how to pronounce the word",
                            "the spelling of the word",
                            "who used the word first",
                            "how to use the word"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In an English-Chinese dictionary, the last word  _  .",
                        "choices": [
                            "begins with Z",
                            "begins with A",
                            "is a short one",
                            "is not often used"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which group of words is in the right order in an English-Chinese dictionary?",
                        "choices": [
                            "perhaps, produce, plenty",
                            "straight, subject, surprise",
                            "century, center, business",
                            "foreign, entrance, headache"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "In the passage the writer tries to tell us that  _  .",
                        "choices": [
                            "we have to use a dictionary when we read something in English",
                            "an English-Chinese dictionary can tell us everything about a word",
                            "an English-Chinese dictionary can help us a lot in our English study",
                            "all English-Chinese dictionary are the same"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1638.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.1,
                "body": "Mr Jones was a millionaire . One day he went to stay at a hotel in New York. He hoped to have the cheapest room to live in. Mr Jones asked, \"What price  is the room?\". The boss   told him. \"And which floor is it on?\" Again the boss told him. \"Is that the cheapest room you have? I' m staying here by myself and only need a small room. \"\nThe boss said, \"That room is the smallest and cheapest we have. But why do you choose a poor room like that? When your son stays here, he always stays at our dearest room. Yours is the cheapest. \" \"Yes,\" said Mr Jones, \"his father is a very rich man, but mine isn' t. \"",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Mr Jones was a   _  .",
                        "choices": [
                            "rich man",
                            "writer  `",
                            "worker",
                            "farmer"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Mr Jones wanted to have  _   room to live in.",
                        "choices": [
                            "a beautiful",
                            "a dear",
                            "the cheapest",
                            "a larger"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The boss told Mr Jones that they had  _   room.",
                        "choices": [
                            "no the cheapest",
                            "the cheapest",
                            "no the dearest",
                            "no small"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Mr Jones' son often stays at   _  room.",
                        "choices": [
                            "the smallest",
                            "a cheap",
                            "a small",
                            "the dearest"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Mr Jones was born   in a   _  family.",
                        "choices": [
                            "rich",
                            "big",
                            "poor",
                            "a farmer's"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1641.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.4,
                "body": "It's a fine day. The White family get up at seven o'clock. They have breakfast at seven forty. And then they go to the park. They take a basket of food and a carpet . The park is not far from their home, so they ride bikes there. Then they get to the park, it's half past eight. Mr. and Mrs. White are talking with each other. Their son, ted, is playing with a ball. Their daughter, Jenny, is taking photos.\nAfter about an hour, Ted and Jenny sit down to relax. At that time, they see a _ eating a pine nut in a big tree. When they see the squirrel eating, they feel hungry . They go to help their parents take the food out of the basket. Ted has a hamburger. Hamburgers are his favorite food. Jenny has an apple. Mr. and Mrs. White have some bread. They have a great time in the park.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "What do the family take to the park?",
                        "choices": [
                            "A basket of food and a book.",
                            "A carpet and a dog.",
                            "A basket of food and a carpet.",
                            "Food and clothes."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When do they get to the park?",
                        "choices": [
                            "At 8:30 a.m.",
                            "At 8:00 a.m.",
                            "At 7:40 a.m.",
                            "At 7:00 a.m."
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What is Jenny doing in the park?",
                        "choices": [
                            "She is reading a book.",
                            "She is taking photos.",
                            "She is playing with a ball.",
                            "She is drawing pictures."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following is NOT True?",
                        "choices": [
                            "The White family ride bikes to the park.",
                            "Ted plays with a ball for about an hour.",
                            "Four people are in Mr. White's family.",
                            "Hamburgers are Jenny's favorite food."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1642.txt)",
                "grade_band": 2,
                "grade_level_estimate": 2.4,
                "body": "For many school in Thailand, there are two terms. The first term is from the first week of May to the first week of October. The second term starts from the first week of November and finishes at the last week of February or the first week of March. The students don't get a _ for Christmas . But they get a 3-4 days' break for the New Year.\nFor many students, a school day is very long. They usually get to school at 7:30 a.m. Classes begin at 8:00 a.m. there are three classes in the morning and they are 50 minutes each . Students have lunch at 11:00 a.m. they don't have dining halls so they have to eat in the classroom. Lunch time finishes at 12:25 p.m. there are three classes in the afternoon. School finishes at 3:15 p.m. many schools have a \"homework\" lesson after school, so students usually go home after 4:45 p.m.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "How long is the first term in Thailand schools?",
                        "choices": [
                            "For six months.",
                            "For five months.",
                            "For four months.",
                            "For three moths."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "When do students usually get to school?",
                        "choices": [
                            "At 7:00 a.m.",
                            "At 7:30 a.m.",
                            "At 8:00 a.m.",
                            "At 8:30 a.m."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Why do students have to eat lunch in the classroom?",
                        "choices": [
                            "Because their dining halls are very small.",
                            "Because they must do their homework after lunch.",
                            "Because they don't have dining halls.",
                            "Because they bring lunch to school."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What can we learn from the passage?",
                        "choices": [
                            "There are three terms in Thailand schools.",
                            "Students don't go to school in November.",
                            "Students usually go home at 3:15 p.m.",
                            "Students have six classes a day."
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1650.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.3,
                "body": "Motor cars were first made in England just before 1900. The parts for the bodies and engines were hand-made and the cars were built from these. One at a time. This took a long time, and the cars cost a lot of money. Then a quicker and cheaper way of making cars was found. Instead of making all the parts at their own works, some car factories asked other factories to make some of them. All the parts were then fitted together in the car factories.\nModern car-making factoriess are so large that each one is really a lot of factories close together. Each workshop makes some parts. The pieces of a car body are joined together by welders  . All the bits and pieces that make up each car are collected and put ready for the assembly line  , where they are fitted together.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The first motor cars were probably made by  _  .",
                        "choices": [
                            "Europeans",
                            "the Whites",
                            "the Blacks",
                            "the English"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "A quicker and cheaper way of making motor cars was  _  .",
                        "choices": [
                            "found in 1900",
                            "that all parts of motor cars were no longer made by hand",
                            "the one that they should be made in a large car factories",
                            "the different parts of motor cars were produced in different works"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "\"Modern car-making factories\" means \"  _  \".",
                        "choices": [
                            "the factories which modern cars are making at",
                            "the factories where cars are made by modern workers",
                            "the new factories at which cars are being made",
                            "the factories where modern cars are made"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle168.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.9,
                "body": "Dear Nancy,\nMy name is Xiao Ming. I want to be in a club in our school. I'm not famous  now. But maybe I can be famous someday  ! I can't sing or dance or act in movies, but I can do many other things. I can play three _ : the guitar, the violin and the drums  . I think I can be in the music club. Maybe I can be a famous musician  . I like to read story books and I can write stories. Maybe I can be a famous writer. I like sports, too, but I don't think I can be a famous and successful  sportsman. Can I join you?\nXiao Ming",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Xiao Ming thinks he can be a famous   _   or a famous writer.",
                        "choices": [
                            "musician",
                            "actor",
                            "sportsman",
                            "singer"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What clubs do you think Xiao Ming can join? He can join  _  .",
                        "choices": [
                            "sports club and music club",
                            "paint club and music club",
                            "swimming club and reading club",
                            "football club and art   club"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1688.txt)",
                "grade_band": 2,
                "grade_level_estimate": 5.8,
                "body": "Suzy won an award in the USA for her popular talk show on TV. Her show is very popular so even people all over the world know it. Why is her show so popular? Because she cares about people and the world. She usually invites important people to her show to talk about some important _ that everyone cares about. And she is not afraid to fight with the bad things. One of her famous stories is about the \"mad cow disease \". When Suzy learned that some businessmen  sold bad beef and lied to people that the cows were without \"mad cow disease\", she got angry and worried. She didn't want people to get sick, so she told everyone in her show that she decided not to eat beef any more. She knew that people would follow her and the businessmen would be angry, but she was not afraid. She knew what was the right thing to do.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Why is Suzy's show popular?",
                        "choices": [
                            "Because people all over the world know her.",
                            "Because only important people go to her show.",
                            "Because she cares about the world.",
                            "Because her show is easy to watch."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which is Right about Suzy?",
                        "choices": [
                            "Fighting with others is her hobby",
                            "Talk shows make her famous",
                            "She never eats beef.",
                            "She hates businessmen."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What do you think of Sue? She is  _  .",
                        "choices": [
                            "rude",
                            "happy",
                            "polite",
                            "brave"
                        ],
                        "correct_index": 3,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1689.txt)",
                "grade_band": 2,
                "grade_level_estimate": 3.4,
                "body": "How can I get good grades at school? How can I finish so much homework every evening? What should I do if I'm not interested in my classes ? Who will teach us this term ? Maybe you have such questions in your mind before school starts.\nWell, I want to give you some good advice on these problems.\nFirst, keep calm.Don't worry about all the question you have. Put your heart into learning,and you can find something you are interested in.Do it actively.\nSecond, try your best to finish your homework quickly.Don't spend a lot of time on it.Do more reading or writing in English.Think about the problems you have and solve them at once.Don't stay up late,or you can't study well the next day.\nThird, think of something instead of copying or repeating.If you can remember the words in your way,you can tell your teachers you don't like the way of copying them again and again.Be sure you can pass the test.I think your teachers will agree with you.And they can give you something interesting to do.\nSchool is really a good place for you to learn.Believe in your teachers and yourself.You are the best one and you can do everything well.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The writer writes the passage to  _",
                        "choices": [
                            "give students some good ways of learning.",
                            "ask students not to listen to their teachers.",
                            "ask students not to do their homework",
                            "tell students what a good teacher is."
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What does the writer tell students to do about their homework?",
                        "choices": [
                            "They should spend a lot of time on it.",
                            "They should stay up late doing it.",
                            "They should do more reading or writing in English.",
                            "They should have boring work to do."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What's the third piece of advice about?",
                        "choices": [
                            "How to get on with friends?",
                            "How to get high grades.",
                            "What kind of schoolwork is better for students.",
                            "How to finish the homework in a short time."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "According to the passage, students should believe in  _  .",
                        "choices": [
                            "themselves and their teachers",
                            "themselves and their parents",
                            "their parents and teachers",
                            "themselves and their classmates"
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1700.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.3,
                "body": "Good morning. The program today is about music. The word \"music\" comes from the Greek word \"muse\". The Muses are the goddesses of the arts. The Music is only one of the arts. It is like the spoken language, but it uses sounds. Today's program brings together music from different concerts of the world. Who invented music? Who sang the first song? No one knows exactly the answers to these questions. But we know that music plays an important part in almost everyone's life. Babies and young children love to hear people singing to them. When they are a little older, they like to sing the songs they have heard. When children go to school, their world of music grows. In the middle grades, students take music lessons. When they reach high school, they become interested in listening to pop music.\nThe records we have chosen for you today are from American country music, Indian music, pop music and so on. Music has meaning for everyone. It can make people happy or it can make them sad. In this program we shall study the language of music. We shall be trying to find out more about how music works. We shall try to find out how music says what people feel.\nNow, here comes the music today , I shall explain why they are all good music.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Which is NOT the purpose of this music program?",
                        "choices": [
                            "To study the language of music .",
                            "To learn more about the music.",
                            "To give a complete background to the music.",
                            "To give people some music to listen to."
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The speaker is probably  _  .",
                        "choices": [
                            "a host",
                            "a singer",
                            "a dancer",
                            "a teacher"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1734.txt)",
                "grade_band": 2,
                "grade_level_estimate": 6.5,
                "body": "This month in Travelers Corner there are three teenagers' experiences in year-abroad programmes.\nMariko Okada - Tokyo\nMy year abroad in the United States was a fantastic experience. I'm not a shy person, and I was very comfortable speaking to everyone. So I got lots of speaking practice. I also learned lots of interesting things about American culture. When I got home, my friends all said that I had improved so much! I hope to go back again in the future.\nCarla Fonseca - Rio de Janeiro\nI spent last year studying English in London. I'm from a small town, and London is a very big city. Sometimes I felt it was too big. There were so many people to talk to, but I always felt bad about my English. I missed my family, and I really missed my two cats. My roommate was always using our telephone, so I hardly had the chance for a nice long talk with my parents. I think it was a good experience for me, but I'm glad to be home!\nAlvin Chen - Hong Kong\nStudying in New Zealand was a fun experience for me, but it was also lots of hard work! I had English classes six hours a day, five days a week----with lots of homework. I also kept a diary of my experience. I like to write, and I wrote two or three pages in my diary every day. On Saturdays, my homestay family took me to lots of interesting places and showed me so many wonderful things about the culture. I'm really glad I went!",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "All the three teenagers went abroad  _  .",
                        "choices": [
                            "to study English",
                            "to visit friends",
                            "to have a holiday",
                            "to find a job"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Who didn't really enjoy the stay in a foreign country very much?",
                        "choices": [
                            "Mariko.",
                            "Carla.",
                            "Alvin.",
                            "None of them."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Travelers Corner is most probably  _  .",
                        "choices": [
                            "a sports club newsletter",
                            "a science documentary",
                            "a travel magazine",
                            "a news website"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle175.txt)",
                "grade_band": 2,
                "grade_level_estimate": 4.5,
                "body": "A young man went to the local expert  on gems and said he wanted to become a gemologist . The expert turned him down because he feared the youth would not have the patience to learn. The young man asked for a chance. Finally, the expert told the youth, \"Be here tomorrow.\"\nThe next morning the expert put a jade  stone in the youth's hand and told him to hold it. The expert then went about his work, cutting, weighing and setting gems. The boy sat quietly and waited.\nThe following morning the expert again put the jade stone in the youth's hand and told him to hold it. On the third, fourth and fifth days, the expert asked the young man to do the same thing. On the sixth day, the youth held the jade stone but he could no longer stand  the silence. \"Master, when am I going to learn something?\" he asked.\n\"You will learn.\" the expert said and went about his business.\nSeveral more days went by and the youth almost lost his patience. But one morning as the master put the stone in the youth's hand, the young man said without looking at his hand, \"This is not the same jade stone!\"\n\"You have begun to learn.\" said the master.\nPractice makes perfect. The experience we learned from practice teaches us and develops our abilities. Experience is the best teacher. Even the most successful person had no absolute confidence once. It is experience that gives people confidence. The truth is: if you do the work and gain the experience, you'll have more confidence because you'll actually know what you're doing.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "The phrase \"turned ... down\" probably means   _  .",
                        "choices": [
                            "refused",
                            "accepted",
                            "forgave",
                            "doubted"
                        ],
                        "correct_index": 0,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "The expert let the young man hold the jade stone for so many days because he wanted to see if the young man was   _  .",
                        "choices": [
                            "brave",
                            "patient",
                            "clever",
                            "honest"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What may be the best title for this passage?",
                        "choices": [
                            "An Experienced Gemologist",
                            "Experience, the Best Teacher",
                            "Experience of a Young Man",
                            "A Confident Teacher"
                        ],
                        "correct_index": 1,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1793.txt)",
                "grade_band": 2,
                "grade_level_estimate": 8.6,
                "body": "At present, more and more people are crazy about travelling. Why do people travel?  \"To see more of the world,\" many people would say. But travelling abroad now means much more than that for the growing number of Chinese tourists. Of course it offers us good opportunities to meet people from other countries, learn about their culture and customs.\nAccording to the United Nations World Tourism Organization (UNWTO), more than 1 billion people travelled to another country in 2012. In 2012, Chinese people travelled abroad 30 percent more than in 2011. The prosperity   of the tourism industry can also bring both our country and foreign countries great economic benefits  . Chinese people usually join large tourist groups and visit several countries in one trip.\nChinese people don't just travel for sightseeing. The China International Travel Service Company said that all their tour trips sold out a month before Christmas Day. Stores offered discounts   during that time, so shopping in Europe and the United States is popular among Chinese travellers.\nIn December, China is going through a very cold winter. So many people like to go to some countries in Southeast Asia because the weather there is quite pleasant.\nThe improvement of living standards means more Chinese can travel abroad. But many of them don't have a sense of public manners. A report by Living Social website in March 2012 even listed Chinese as the world's second worst tourists.\nIf you want to change that bad name, remember to avoid the following: littering, spitting, snatching bus seats, line-jumping, taking off shoes in public, talking loudly and smoking in non-smoking areas. Besides, we should learn some necessary manners of foreign countries.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "Chinese people travel abroad not to   _  .",
                        "choices": [
                            "go shopping",
                            "see more of the world",
                            "go sightseeing",
                            "make money"
                        ],
                        "correct_index": 3,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "According to the United Nations World Tourism Organization,   _  .",
                        "choices": [
                            "30% of the people who travelled abroad are Chinese",
                            "the number of people who travelled abroad rose by 30%",
                            "more than 1 billion people travelled abroad in 2012",
                            "more than 1 billion Chinese people travelled abroad in 2012"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "Which of the following is NOT True about Chinese people?   _",
                        "choices": [
                            "Chinese people like joining large tourist groups.",
                            "Many Chinese like to go to Southeast Asia in winter for sightseeing.",
                            "More and more Chinese people can travel abroad now.",
                            "Chinese are the second worst tourists in the world."
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "As a good tourist, you should   _  .",
                        "choices": [
                            "litter and spit here and there",
                            "jump the line and take off the shoes in public",
                            "have a sense of public manners",
                            "speak loudly and smoke as you like"
                        ],
                        "correct_index": 2,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What's the best title of the passage?   _",
                        "choices": [
                            "Travelling",
                            "Travelling abroad",
                            "Chinese tourists",
                            "Chinese people like travelling"
                        ],
                        "correct_index": 1,
                        "skill_tag": "critical",
                        "difficulty": "medium",
                        "needs_review": True
                    }
                ]
            },
            {
                "title": "RACE Passage (middle1813.txt)",
                "grade_band": 2,
                "grade_level_estimate": 1.7,
                "body": "Li Ling is a good teacher. She will be 29 years old next year. She is from Huaiyang, Henan province  . Her school is very small. There are eight classrooms in the school. In her school, all the students are free. Some of them are left-behind children  . Li Ling is a kind girl. She loves here students very much.\nLi Ling works hard every day. Every summer she often buys old books for her students in Zhengzhou. She moves   China! She wants to have a good school.",
                "source": "RACE (Lai et al., 2017) - non-commercial research use only - https://arxiv.org/abs/1704.04683",
                "questions": [
                    {
                        "prompt": "What is Li Ling?",
                        "choices": [
                            "A mother.",
                            "A doctor",
                            "A teacher.",
                            "A farmer."
                        ],
                        "correct_index": 2,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "How old is Li Ling?",
                        "choices": [
                            "27.",
                            "28.",
                            "29",
                            "30"
                        ],
                        "correct_index": 1,
                        "skill_tag": "inferential",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What does she do for her students?",
                        "choices": [
                            "She cooks food for them.",
                            "She buys old book for them.",
                            "She teaches them English.",
                            "She gives her money to them."
                        ],
                        "correct_index": 1,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    },
                    {
                        "prompt": "What is Li Ling's dream  ?",
                        "choices": [
                            "She wants to have a good school.",
                            "She wants to be a kind teacher.",
                            "She wants to help left-behind children.",
                            "She wants to move China."
                        ],
                        "correct_index": 0,
                        "skill_tag": "literal",
                        "difficulty": "easy",
                        "needs_review": True
                    }
                ]
            },
        


]

import os
from app import app


def seed():
    with app.app_context():
        # Clear existing content so re-running this script during dev
        # doesn't pile up duplicate passages/questions.
        # db.session.query(Question).delete()
        # db.session.query(Passage).delete()
        # db.session.commit()

        passages_added = 0
        questions_added = 0

        for p_data in PASSAGES:
            # 1. Check if the passage already exists by title
            passage = Passage.query.filter_by(title=p_data["title"]).first()

            if not passage:
                # Create new passage if it doesn't exist
                passage = Passage(
                    title=p_data["title"],
                    body=p_data["body"],
                    grade_band=p_data["grade_band"]
                )
                db.session.add(passage)
                db.session.flush()  # Generates passage.id
                passages_added += 1

            # 2. Add only new questions for this passage
            for q_data in p_data["questions"]:
                existing_question = Question.query.filter_by(
                    passage_id=passage.id,
                    prompt=q_data["prompt"]
                ).first()

                if not existing_question:
                    db.session.add(
                        Question(
                            passage_id=passage.id,
                            prompt=q_data["prompt"],
                            choices=q_data["choices"],
                            correct_index=q_data["correct_index"],
                            skill_tag=q_data["skill_tag"],
                            difficulty=q_data["difficulty"],
                        )
                    )
                    questions_added += 1

        db.session.commit()
        print(f"Seeding complete! Added {passages_added} new passages and {questions_added} new questions.")
        print("All student accounts, skill states, and response history were preserved.")


if __name__ == "__main__":
    seed()
