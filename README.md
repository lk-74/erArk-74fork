# Tweaks
(please read original README)

# Script\Design\character_behavior.py    

    Line 853 - 855
    if hypnosis then try add submission
    催眠状态下每10分钟update增加1屈服（但是add_time的表现十分诡异所以这项的实际效果得至少打一半折扣）

# Script\UI\Flow\creator_character_flow.py   

    Line 913
    if first bonus money then add originium
    把初始加钱的条目额外加了9999源石，只是为了测试能力而已没有实际意义

# Script\Settle\default.py   

    Line 3065
    if hypnosis >= 50 then do not trigger TARGET_ADD_SMALL_DISGUST 
    if sleeping sex then no TARGET_ADD_SMALL_DISGUST
    催眠程度>=50时不会触发小反感（我是想做成50无视骚扰100无视性行为，但是改的这段code我不知道怎么抓取玩家行为分类）
    睡眠状态（准确说，睡奸状态）不会触发小反感

    Line 1154
    reduce penetrating vision cost from 5 to 1
    internal vision should reduce from 10 to 2
    透视的理智消耗5->1，不确定是否生效（因为add_time的运行方式我还不是很理解）
    如果我没理解错的话腔内透视倍率消耗应该也会降低到2，吧？

# Script\Design\cooking.py
    Line 489
    Line 514
    if hypnosis then accept cum food
    催眠状态下不会拒绝加料的食物（催眠程度50以上会不质疑直接吃，100以上会发现食物加了东西但还是吃）

# Script\UI\Panel\make_food_panel.py
    Line 276
    if semen food then player cum into it
    食物加料会触发玩家射精（call一次射精然后把射精量存到食物里）

# Script\Settle\default.py
    Line 4804
    add cum amount to stomach
    add cum amount to obedience and submission
    食用加料食物会将食物内的精液加到对象嘴里
    根据食用的精液量增加恭顺和屈服（个人喜好而已，过于破坏平衡建议拿掉）