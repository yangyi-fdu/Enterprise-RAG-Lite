# End-to-end evaluation

LLM: `glm-4-flash`. Threshold 0.3, top-k 3.

| Group | Passed |
|---|---:|
| In-scope, answer contains the fact | 37/40 |
| Korean/Chinese, answer contains the fact | 8/8 |
| Near miss, declined | 12/12 |
| Off-topic, declined | 8/8 |

## All answers

| Group | Question | Answer | Fallback | Pass |
|---|---|---|:---:|:---:|
| in_scope | Who is the CEO of the company? | Mina Kwon is the CEO of the company. |  | yes |
| in_scope | Where is the head office located? | The head office is located in Busan. |  | yes |
| in_scope | What is the maximum payload of the HR-7 robot? | The maximum payload of the HR-7 robot is 300 kilograms. |  | yes |
| in_scope | Which robot model is intended for retail stockrooms? | The HR-3 robot model is intended for retail stockrooms. |  | yes |
| in_scope | What are the core hours I have to be online? | Core working hours are 10:00 to 16:00 Korea Standard Time. |  | yes |
| in_scope | How many days a week can I work from home? | After completing your probation period, you can work remotely for up to two days per week. |  | yes |
| in_scope | How long is probation for new hires? | Three months. |  | yes |
| in_scope | How many days of paid holiday do I get each year? | You get 15 days of paid annual leave per year. |  | yes |
| in_scope | Can I carry unused vacation days into next year? | No, any remaining days expire on 31 March. |  | **no** |
| in_scope | Do I need a doctor's note if I'm sick for two days? | Yes, sick leave of up to 3 consecutive days does not require a medical certificate. |  | yes |
| in_scope | How many volunteering days are there? | Employees receive 2 paid volunteering days per year. |  | yes |
| in_scope | What is the deadline for submitting an expense claim? | The deadline for submitting an expense claim is within 30 days of the purchase date. |  | yes |
| in_scope | Is a credit card statement enough as proof for an expense? | No, a card statement alone is not accepted. Every claim must include an itemised receipt. |  | yes |
| in_scope | What is the daily meal allowance on a business trip? | Meals during business travel are reimbursed up to 40,000 won per day. |  | yes |
| in_scope | Who has to approve an expense claim of 800,000 won? | The finance controller, Jae-won Park, has to approve an expense claim of 800,000 won. |  | yes |
| in_scope | When are approved expenses paid out? | Approved claims are paid with the next monthly salary, which is paid on the 25th of each month. |  | yes |
| in_scope | Can I expense drinks at dinner? | No, alcohol is not reimbursable unless it is part of an approved client event. |  | yes |
| in_scope | How far in advance do I have to book work travel? | At least 14 days before departure. |  | yes |
| in_scope | Can I fly premium economy on a long-haul flight? | Yes, you may book premium economy for flights of 6 hours or longer. |  | yes |
| in_scope | What is the hotel limit per night in Seoul? | Hotel costs are reimbursed up to 180,000 won per night in Seoul. |  | yes |
| in_scope | My laptop is broken, how do I get it fixed? | To report a hardware fault or request software, open a ticket in the IT service desk at help.halden.example. Urgent problems that block work can be reported by phone on extension 4400. |  | yes |
| in_scope | What phone extension do I call for urgent IT problems? | Extension 4400 |  | yes |
| in_scope | Can I open my workstation to replace a part myself? | No, employees must not open laptops or workstations themselves to repair them. |  | yes |
| in_scope | Which GPU do software engineers get? | Software engineers receive a workstation with an NVIDIA RTX 4090 GPU on request. |  | yes |
| in_scope | How long must my password be? | Your password must be at least 14 characters long. |  | yes |
| in_scope | Am I allowed to push company code to my personal GitHub? | No, uploading company code to public repositories or personal cloud storage is prohibited. |  | yes |
| in_scope | Where should I send a suspicious phishing email? | Suspected phishing emails should be forwarded to the security team at security@halden.example. |  | yes |
| in_scope | How often do I need to redo security training? | Every 12 months. |  | yes |
| in_scope | When is the lab safety induction held? | The lab safety induction is held every Tuesday. |  | yes |
| in_scope | What is the speed limit for robots in the shared test arena? | The speed limit for robots in the shared test arena is 1.2 metres per second. |  | yes |
| in_scope | Where should robot batteries be charged? | Robot batteries should be charged only in the fire-rated charging cabinets. |  | yes |
| in_scope | How do I report a near miss in the lab? | Any collision, near miss or injury must be reported in the incident log on the same day. |  | yes |
| in_scope | How long is a sprint? | Two weeks |  | yes |
| in_scope | Which ROS 2 distribution does the robot software use? | ROS 2 Humble |  | yes |
| in_scope | Which simulator runs the regression tests in CI? | Gazebo |  | yes |
| in_scope | How long is the soak test before a release? | I don't know. |  | **no** |
| in_scope | How much is my yearly training budget? | Your yearly training budget is 1,500,000 won. |  | yes |
| in_scope | Is conference travel paid from the learning budget? | No, conference travel is paid from the travel budget, not the learning budget. |  | yes |
| in_scope | When are the internal tech talks? | Internal tech talks take place every second Thursday at 17:00. |  | yes |
| in_scope | Who do I ask about my payslip? | I don't know. |  | **no** |
| cross_lingual | 연차 휴가는 1년에 며칠인가요? | 15 days |  | yes |
| cross_lingual | 출장 시 하루 식비 한도는 얼마인가요? | 출장 시 하루 식비 한도는 40,000 원입니다. |  | yes |
| cross_lingual | 로봇 테스트 구역의 속도 제한은 얼마입니까? | 로봇 테스트 구역의 속도 제한은 1.2 미터/초입니다. |  | yes |
| cross_lingual | 보안 교육은 얼마나 자주 받아야 하나요? | 보안 교육은 매 12개월마다 받아야 합니다. |  | yes |
| cross_lingual | 费用报销需要在多少天内提交？ | 费用报销需要在30天内提交。 |  | yes |
| cross_lingual | 公司的首席执行官是谁？ | Mina Kwon |  | yes |
| cross_lingual | 电池应该在哪里充电？ | 电池必须在火评级充电柜中充电。 |  | yes |
| cross_lingual | 每周可以远程办公几天？ | 每周可以远程办公最多两天。 |  | yes |
| near_miss | How long is parental leave? | I don't know. |  | yes |
| near_miss | Does the company offer stock options? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| near_miss | What is the dress code in the office? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| near_miss | Is there free parking at the Busan office? | Don't know. |  | yes |
| near_miss | What are the salary bands for senior engineers? | I don't know. |  | yes |
| near_miss | Does Halden pay for a gym membership? | I don't know. |  | yes |
| near_miss | What is on the cafeteria menu today? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| near_miss | How do I install ROS 2 on macOS? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| near_miss | What is the company's revenue this year? | I don't know. |  | yes |
| near_miss | How many robots has Halden sold to Germany? | Don't know. |  | yes |
| near_miss | Can I bring my dog to the office? | Don't know. |  | yes |
| near_miss | What pension scheme does the company use? | I don't know. |  | yes |
| off_topic | What is the capital of France? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | How do I bake sourdough bread? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | Who won the football World Cup in 2018? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | Explain the difference between TCP and UDP. | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | What's the weather like tomorrow? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | Recommend a good science fiction novel. | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | How do I reverse a list in Python? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
| off_topic | What is the boiling point of water at high altitude? | I could not find this in the knowledge base, so I can't answer it reliably. Please contact the relevant team directly. | yes | yes |
