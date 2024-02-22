(please read original README)

Tweaks

Script\Design\character_behavior.py    
    Line 853 - 855
    if hypnosis then try add submission，每10分钟催眠增加1经验

Script\UI\Flow\creator_character_flow.py    
    Line 913
    if first bonus money then add originium

Script\Settle\default.py   
    Line 3065
    if hypnosis >= 50 then do not trigger TARGET_ADD_SMALL_DISGUST 
    if sleeping sex then no TARGET_ADD_SMALL_DISGUST

    Line 1154
    reduce penetrating vision cost from 5 to 1
    internal vision should reduce from 10 to 2
    Script\Design\character_behavior.py
    possible related code

Script\Settle\default.py
    L4711
    TODO add cum amount to stomach

Script\Design\cooking.py
    Line 489
    Line 514
    if hypnosis then accept cum food