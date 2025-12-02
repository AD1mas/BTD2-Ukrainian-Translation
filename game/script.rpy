define p = DynamicCharacter("player_name", window_background="dialoguebox_player.png")
define unknown = Character ("???", window_background="dialoguebox_player.png")
define n = Character ("  ", window_background="dialoguebox_noname.png")
image bedroom = "bedroom.jpg"

label splashscreen:
    scene black
    with Pause(0.5)

    scene endslate with dissolve
    show text "{=endslate_title}{size=90}{color=#cc0000}SOSAV?{/color}{/size}{/=endslate_title}\n{vspace=10}{size=30}ТАК{/size}\nБЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ\nЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ\nЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ\nЯЯЯЯЯЯЯЯЯЯЯЯЯЯ\nЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ\nЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ\n{vspace=10}{size=30}18+ Тільки!{/size}{vspace=20}\nFor a more specific list of warnings, please visit {a=http://www.boyfriendtodeath.com/btd-2-fresh-blood.html}{color=#ffffff}the website{/color}{/a}." with dissolve
    pause
    scene endslate_clean with dissolve
    show text "The characters and actions depicted in this game are entirely fictional.\n{vspace=20}Your choices will affect the story and the outcome, but this is not a story where good triumphs over evil. This is a journey through horrors, from the wildly paranormal to the subtle darkness of human apathy.\n{vspace=20}If you're feeling overwhelmed, close the game and take a break.\n{vspace=20}{color=#cc0000}This game was built to thrill, not to harm.\nPlease take care.{/color}" with dissolve
    pause
    return

transform alpha_dissolve:
    alpha 0.0
    linear 0.5 alpha 1.0
    on hide:
        linear 0.5 alpha 0

screen countdown:
    timer 0.01 repeat True action If(time > 0, true=SetVariable('time', time - 0.01), false=[Hide('countdown'), Jump(timer_jump)])
    bar value time range timer_range xalign 0.5 yalign 0.9 left_bar Frame("bar_time.png", 10, 0) right_bar Frame("bar_time_empty.png", 10, 0) thumb ("thumb.png") xmaximum 300 ymaximum 50 at alpha_dissolve

screen time_bar:
    timer 0.01 repeat True action If(time > 0, true=SetVariable('time', time - 0.01), false=[Hide('countdown'), Jump(timer_jump)])
    bar value time range timer_range xalign 0.98 yalign 0.03 xmaximum 30 ymaximum 400 left_bar Frame("bar_health_empty.png", 10, 0) right_bar Frame("bar_health.png", 10, 0) thumb None bar_vertical True

screen health_bar:
    vbox:
        xalign 0.01 yalign 0.03
        bar value AnimatedValue(health, range=100.0):
            xalign 0.0 yalign 0.0
            xmaximum 30
            ymaximum 400
            left_bar Frame("bar_health_empty.png", 10, 0)
            right_bar Frame("bar_health.png", 10, 0)
            thumb None
            bar_vertical True
        add ConditionSwitch(
             "health <= 0", "bar_health_icon_death.png",
             "health >= 1", "bar_health_icon.png",
             )

screen sanity_bar:
    vbox:
        xalign 0.06 yalign 0.03
        bar value AnimatedValue(sanity, range=100.0):
            xalign 0.0 yalign 0.0
            xmaximum 30
            ymaximum 400
            left_bar Frame("bar_sanity_empty.png", 10, 0)
            right_bar Frame("bar_sanity.png", 10, 0)
            thumb None
            bar_vertical True
        add ConditionSwitch(
             "sanity <= 0", "bar_sanity_icon_death.png",
             "sanity >= 1", "bar_sanity_icon.png",
             )
screen webpage:
    imagemap:
        ground "webpage.png"

        hotspot (75, 107, 558, 146) clicked Jump("cain_start")
        hotspot (72, 264, 555, 151) clicked Jump("law_start")
        hotspot (75, 424, 555, 141) clicked Jump("vince_start")
        hotspot (699, 135, 83, 352) action OpenURL("http://boyfriendtodeath.com/index.html")

    $ ui.timer(120.0, ui.jumps("ending_netflix"))

image endslate = "bloodbg.jpg"
image endslate_clean = "bloodbg_noblood.jpg"
style endslate_title:
    size 150
    color "#fff"
    font "youmurdererbb_reg.ttf"
style endslate_subtitle:
    color "#fff"
    italic "true"
    text_align 0.5


label start:
scene bedroom
play music "mc_main.mp3"
screen input:
    window:

        style "nvl_window"
        text prompt xalign 0.5 yalign 0.4
        input id "input" xalign 0.5 yalign 0.5

$ player_name = renpy.input("What's your name?",length=10)
$ player_name = player_name.strip()
if player_name == "":
    $ player_name="Anon"

$ cain_love = 0
$ law_love = 0
$ vincent_love = 0
$ ren_love = 0
$ health = 100
$ sanity = 100


init python:
    def limit_health():
        try:
            if store.health < 0:
                store.health = 0
            elif store.health > 100:
                store.health = 100
        except:
            pass

    config.python_callbacks.append(limit_health)  
    def limit_sanity():
        try:
            if store.sanity < 0:
                store.sanity = 0
            elif store.sanity > 100:
                store.sanity = 100
        except:
            pass

    config.python_callbacks.append(limit_sanity)

init:

    python:

        import math

        class Shaker(object):
            
            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }
            
            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                
                self.start = [ self.anchors.get(i, i) for i in start ]  
                self.dist = dist    
                self.child = child
            
            def __call__(self, t, sizes):
                
                
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x
                
                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]
                
                xpos = xpos - xanchor
                ypos = ypos - yanchor
                
                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                
                return (int(nx), int(ny), 0, 0)

        def _Shake(start, time, child=None, dist=100.0, **properties):
            
            move = Shaker(start, child, dist=dist)
            
            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)



init:
    $ smallshake = Shake((0, 0, 0, 0), 100.0, dist=2)
init:
    $ largeshake = Shake((0, 0, 0, 0), 100.0, dist=4)

init:
    python:
        def silhouette_matrix (r,g,b,a=1.0):
            return im.matrix((0, 0, 0, 0, r, 
                               0, 0, 0, 0, g,
                               0, 0, 0, 0, b,
                               0, 0, 0, a, 0,))
        def silhouetted (filename, r,g,b, a = 1.0):
            return im.MatrixColor (Image (filename), silhouette_matrix (r,g,b,a))
p "I should go out tonight."
n "I flicked on my computer."
n "There had to be somewhere open late."
call screen webpage






define vincent = DynamicCharacter ("vincent_name", 
    window_background="vincent/dialoguebox_vincent.png",
    show_side_image = ConditionSwitch(
    "vincent_love >= 100", "love_icon_vincent.png",
    "vincent_love >= 90", "love_icon_red.png",
    "vincent_love >= 80", "love_icon_pink.png",
    "vincent_love >= 70", "love_icon_orangered.png",
    "vincent_love >= 60", "love_icon_orange.png",
    "vincent_love >= 50", "love_icon_yellow.png",
    "vincent_love >= 40", "love_icon_green.png",
    "vincent_love >= 30", "love_icon_cyan.png",
    "vincent_love >= 20", "love_icon_blue.png",
    "vincent_love >= 10", "love_icon_purple.png",
    "vincent_love >= 0", "love_icon_black.png",
    "vincent_love <= 0", "love_icon_broken.png",
    )
    )
define farz = DynamicCharacter ("farz_name", window_background="vincent/dialoguebox_farz.png" )
screen vincent_rage_bar:
    vbox:
        xalign 0.99 yalign 0.2
        bar value AnimatedValue(temper, range=100.0):
            xalign 0.0 yalign 0.0
            xmaximum 50
            ymaximum 400
            left_bar Frame("vincent/rage_bar_empty.png", 10, 0)
            right_bar Frame("vincent/rage_bar_full.png", 10, 0)
            thumb None
            bar_vertical True


image poolhall = "vincent/bar.jpg"
image vincent_bedroom_night = "vincent/Bedroom_night.png"
image vincent_bedroom_day = "vincent/Bedroom_day.png"
image falloutshelter = "vincent/falloutshelter.jpg"
image falloutshelter_dark = "vincent/falloutshelter_dark.jpg"
image vincent_hospital = "vincent/hospital.jpg"

init:
    image CG_vincent_skull = "vincent/Skull_cg.png"
    image CG_vincent_keypad = "vincent/keypad_cg.png"
    image CG_vincent_code = "vincent/code_cg.png"
    image CG_vincent_dogtags = "vincent/dogtags_CG.png"
    image CG_vincent_note = "vincent/note_CG.jpg"
    image CG_sano_vincent = "vincent/CG_sano_vincent.jpg"
    image CG_Farz_eyepull = "vincent/CG_Farz_eyepull.jpg"
    image CG_Farz_leaning_on_Vincents_leg = "vincent/CG_Farz_leaning_on_Vincents_leg.jpg"
    image CG_Farz_Stab = "vincent/CG_Farz_Stab.jpg"
    image CG_farz_vincent_kiss = "vincent/CG_farz_vincent_kiss.jpg"
    image CG_vincent_cigburn = "vincent/CG_vincent_cigburn.jpg"
    image CG_vincent_dream = "vincent/CG_vincent_dream.jpg"
    image CG_vincent_dream1 = "vincent/CG_vincent_dream1.jpg"
    image CG_vincent_dream2 = "vincent/CG_vincent_dream2.jpg"
    image CG_VINCENT_gunup_Farzbehind = "vincent/CG_VINCENT_gunup_Farzbehind.jpg"
    image CG_Vincent_gutsonthefloor = "vincent/CG_Vincent_gutsonthefloor.jpg"
    image CG_Vincent_kiss = "vincent/CG_Vincent_kiss.jpg"
    image CG_Vincent_vomit = "vincent/CG_Vincent_vomit.jpg"
    image CG_Vincent_blushy = "vincent/CG_Vincent_blushy.jpg"
    image CG_Vincent_Fuck = "vincent/CG_Vincent_Fuck.jpg"
    image CG_vincent_temper_death = "vincent/CG_vincent_temper_death.jpg"
    image CG_Vincent_Wolf_PINATA = "vincent/CG_Vincent_Wolf_PINATA.jpg"
    image CG_Vincent_Dick_out = "vincent/CG_Vincent_Dick_out.jpg"
    image CG_vincent_SHOTGUN_JOB = "vincent/CG_vincent_SHOTGUN_JOB.jpg"
    image CG_Vincent_Happy = "vincent/CG_Vincent_Happy.jpg"
    image CG_vincent_Neglove_death = "vincent/CG_vincent_Neglove_death.jpg"
    image CG_vincent_door = "vincent/CG_vincent_door.jpg"
    image CG_Vincent_Wolf_vore = "vincent/CG_Vincent_Wolf_vore.jpg"
    image CG_vincent_VS_cain = "vincent/CG_vincent_VS_cain.jpg"
    image CG_vincent_Farz_BJ = "vincent/CG_vincent_Farz_BJ.jpg"
    image CG_Vincent_Aimed_shotgun = "vincent/CG_Vincent_Aimed_shotgun.jpg"
    image CG_Vincent_Cuddle_Farz = "vincent/CG_Vincent_Cuddle_Farz.jpg"
    image CG_Vincent_with_bat = "vincent/CG_Vincent_with_bat.jpg"



image vincent_redvignette = "vincent/redvin.png"
image desk = "vincent/desk.png"

init python:

    vbase,vblush,vexp = 1,0,1

    def draw_vincent(st, at): 
        return LiveComposite(
            (448, 600), 
            (0, 0), "vincent/vincent_base_%d.png"%vbase,
            (0, 0), "vincent/vincent_blush_%d.png"%vblush,
            (0, 0), "vincent/vincent_expression_%d.png"%vexp,
            ),.1   
init:
    image vincent = DynamicDisplayable(draw_vincent)

init python:

    fbase,fexp = 1,1

    def draw_farz(st, at): 
        return LiveComposite(
            (448, 600), 
            (0, 0), "vincent/farz_base_%d.png"%fbase,
            (0, 0), "vincent/farz_expression_%d.png"%fexp,
            ),.1   
init:
    image farz = DynamicDisplayable(draw_farz)


label vince_start:
show screen health_bar
show screen sanity_bar
$ temper = 0
$ farz_love = 0
$ vincent_dayzero_sex = False
$ vbase,vblush,vexp = 1,0,1
$ fbase,fex = 1,1
$ farz_watchover_night2= False
$ vincent_name = "???"
n "A crappy pool hall didn't sound like the best place to spend the night but I was feeling adventurous."
n "I put on some black clothes and examined myself."
n "Maybe that would help from standing out."
n "Who knew?"
scene alleyway with dissolve
n "I walked out of my apartment and headed downtown."
n "Once I arrived I headed in."
scene poolhall with dissolve
play music "vincent/Vincent_Poolhall.mp3"
n "I looked around the pool hall and immediately felt out of place. "
n "Despite being careful, I felt myself bumping into some large men and scantily clad women."
p "Oh excuse me."
show farz
$ fbase,fexp = 1,1
n "The small person I bumped into scoffed and zeroed in on me."
$ farz_name = "???"
farz "Oh you're excused."
farz "Maybe you should watch where you're going."
menu:
    "\"Sorry, it was hard to see you down there.\"":
        $ farz_love -= 10
        $ temper +=10
        $ fexp =2
        farz "What the fuck did you just say to me, bitch?"
        n "He reeled back and punched me in the stomach as hard as he could." with vpunch
        $ health -=5
        n "I felt the air get knocked out of me and looked around, stunned that no one cared."
        n "No one even moved to help me."
        farz "I should just bash your face in."
        n "He advanced on me."
    "\"Sorry, I didn't mean to.\"":

        $ farz_love += 10
        farz "Pft, see that it doesn't happen again."
        n "He looked annoyed that I was still in his face."
        farz "What are you looking at?"
        n "His tone annoyed, he advanced on me."
    "\"Whatever.\"":

        $ farz_love -= 5
        farz "What did you say to me?"
        p "I said whatever, dude."
        p "You don't own the place."
        farz "Maybe not, but I'm not a newbie like you."
        n "I walked towards him and he met me in the middle."

vincent "HEY. Enough."
n "A deep voice with a heavy southern accent stopped us."
$ vbase,vblush,vexp = 2,0,2
show vincent with dissolve:
    subpixel True
    xpos 75
show farz:
    subpixel True
    xpos 550
n "A tall broad shouldered man walked over to us."
n "The proud tone of his walk and the way people moved out of his way-"
n "He wasn't someone to be messed with in this bar."
vincent "What are you shits doin'?"
vincent "We can't have you guys fightin' in here."
vincent "Don't need the pigs poking their noses in our business again."
vincent "Got me?"
n "The smaller man went quiet and shoved me again."
$ farz_name = "Farz"
$ persistent.character_unlock_farz = True
vincent "Farz."
n "Farz narrowed his eyes at Vincent for a moment and gave up."
farz "Fine."
$ fexp =2
farz "You're lucky Vincent is here."
$ vincent_name = "Vincent"
$ persistent.character_unlock_vincent = True
hide farz
show vincent at center
$ vbase,vblush,vexp = 2,0,3
if player_name.lower() == "rot":
    n "He shifted uncomfortably."
    vincent "What are y'all doin in here anyways?"
    $ vbase,vblush,vexp = 2,0,2
    vincent "You look real delicate."
    vincent "Someone like me..."
    vincent "Is bound to break ya."
    p "I don't believe you will."
    $ vbase,vblush,vexp = 2,1,1
    vincent "You don't know that."
    p "I believe it."
    vincent "You're an idiot then."
    p "Maybe so."
    p "But, I still believe you wouldn't hurt me."
    vincent "Maybe not on purpose."
    $ vincent_love += 10
    n "Vincent's face remained red for a moment while he rubbed his arm."
else:
    n "I was thankful that he had stood up for me but, he seemed to be uninterested now."

$ vbase,vblush,vexp = 2,0,3
menu:
    "\"Thank you.\"":
        $ vincent_love += 10
        vincent "You wanna thank me?"
        $ vbase,vblush,vexp = 2,0,1
        n "He spoke in the same gruff tone that he had before but shifted his gaze back to me."
        vincent "You're gonna have to thank me with more than your words."
        n "I felt my voice getting caught in my throat."
        $ vbase,vblush,vexp = 2,0,5
        vincent "Maybe you can just use your mouth."
        n "Vincent leaned over me and I stepped back."
        vincent "I bet you haven't even been with a real man like me."
        $ vbase,vblush,vexp = 2,0,4
        vincent "Want a taste of my cock?"
        n "I didn't say anything, I could feel my face heating up."
        vincent "Offer stands if you REALLY wanna thank me."
        n "He leaned away from me and crossed his arms."
    "\"I could have stood up for myself.\"":

        $ vincent_love -=20
        $ temper += 10
        $ vbase,vblush,vexp = 2,0,1
        vincent "HAH, You a fuckin idiot?"
        n "He didn't seem to have a lot of confidence in me."
        p "I don't think he would have done that."
        n "I tried to sound tough but my voice cracked slightly."
        $ vbase,vblush,vexp = 2,0,5
        vincent "OH MAN! You don't know him very well."
        vincent "That guy, he's a fuckin' hard nut to crack."
        n "The man laughed at me and turned his gaze to me."
        vincent "And YOU are just lucky he didn't crack you."
    "-Say nothing-":

        $ vincent_love -=10
        $ temper += 10
        n "I wasn't sure what to say to him so I stayed quiet."
        vincent "Do I have something on my face?"
        n "Vincent turned his head to me and I swallowed hard."
        vincent "Maybe it's the lack of something on my face that's botherin' you."
        n "He advanced on me and put his hands out."
        n "He clapped his hands on my shoulder causing me to jump." with vpunch
        n "A cold sweat dripped down the back of my neck."
        $ vbase,vblush,vexp = 2,0,6
        vincent "Don't be so jumpy!"
        vincent "I'm sure you were just looking at how handsome I am."
        n "Vincent pushed me and I stumbled back."

if player_name.lower() == "andi":
    vincent "Nice piercings."
    n "I touched my gauges and smiled inwardly."
    n "I felt my face heating up."
    p "Oh... Yeah. I got them done at a place down the street."
    n "He turned his head, as if he was looking down the street where the tattoo parlor would be."
    n "He nodded."
    vincent "Good place."
    n "I bit my lip trying to find a way to speak with him more."
$ vbase,vblush,vexp = 2,0,6
vincent "You look like you got somethin' to say."
vincent "You should just say what you got on your mind."
vincent "Otherwise someone like me might mistake it for you gawkin'."
n "Was I staring?"
n "I wasn't even aware."
n "But, what wasn't there to stare at?"
n "He was large and imposing, people seemed to respect him here."
menu:
    "-Introduce yourself-":
        $ vincent_love +=5
        jump vincent_sweet_mc
    "\"Where'd you get those scars from?\"":

        $ vincent_love +=5
        $ temper += 10
        jump vincent_pushy_mc
    "-Back off-":

        jump vincent_left_alone

label vincent_sweet_mc:
p "My name is %(player_name)s."
n "I tried to sound as polite as I could."
if player_name.lower() == "farz":
    $ vbase,vblush,vexp = 2,2,8
    vincent "Damn. You have the same name as Farz."
    p "It's not that common..."
    vincent "It sure isn't."
    $ vbase,vblush,vexp = 2,0,9
    $ vincent_love +=10
vincent "Hey don't cha think that you should be talking to some other guys in this bar?"
vincent "As much as you enjoy looking at my face."
vincent "I'm sure there's a bunch of dudes who'd be happy to get balls deep in you."
n "Vincent seemed unfazed by the rude way he spoke to me."
n "I bit my lip."
$ vbase,vblush,vexp = 2,0,7
p "...Maybe I don't want that!"
$ vbase,vblush,vexp = 2,0,5
vincent "You came to the wrong bar, and started talking to the wrong guy then."
vincent "Because, I ain't nice."
vincent "I'm not gonna treat you like a fucking delicate flower."
$ vbase,vblush,vexp = 2,0,4
vincent "I'm a fuckin animal."
$ vbase,vblush,vexp = 2,0,5

menu:
    "\"Oh...I guess I'll go then.\"":
        $ vincent_love -=10
        jump vincent_left_alone
    "\"What does that mean?\"":

        $ vincent_love -=5
        $ temper += 10
        vincent "I mean, I could throw you down on the table-"
        vincent "And fuck you in front of all these lovely people."
        n "Some of the men at the bar looked over an eyeballed me with a smirk."
        n "Vincent started to advance on me and I took a step back."
        vincent "They love taking bets on how long it takes me to cum."
        vincent "We could go all night~"
        n "My back hit a wall and I looked up at him."
        p "...Pl-please don't."
        $ vbase,vblush,vexp = 2,0,8
        n "Vincent grinned and put his hand on the wall next to my head."
        vincent "But, I don't really feel like putting on a show for these people tonight."
        vincent "Got priorities to deal with."
        vincent "You understand?"
        $ vbase,vblush,vexp = 2,0,4
        n "He patted me on the face with the other hand and licked his lips."
        vincent "I don't think you have the time for that."
        n "Vincent pushed off the wall and turned away from me."
        $ vbase,vblush,vexp = 2,0,6
        n "He was going to leave me alone?"
        menu:
            "\"WAIT!\"":
                $ vincent_love +=5
                $ temper +=10
                $ vbase,vblush,vexp = 2,0,1
                vincent "...You're fucking kiddin me right?"
                vincent "What did I just say?"
                vincent "I ain't gonna be nice with ya."
                n "I looked at him trying to find words."
                n "Vincent paused and looked me over."
                $ vbase,vblush,vexp = 2,0,6
                n "Almost as if a light went on in his head."
                vincent "You want a one night stand?"
                $ vbase,vblush,vexp = 2,0,4
                n "Vincent cocked his head to the side with a large smirk across his face."
                p "T-That's not what I s-said!"
                n "Vincent put his hand under my chin and pushed my head up forcing me to look up at him."
                $ vbase,vblush,vexp = 2,0,9
                vincent "...Really?"
                vincent "Cause that's what I can see all over your face."
                jump vincent_consensual_sex
            "-Leave him alone-":
                $ vincent_love -=10
                jump vincent_left_alone


label vincent_consensual_sex:
$ vincent_dayzero_sex = True
if player_name.lower() == "farz":
    p "...May-maybe I do.."
    n "I stuttered out."
    $ vbase,vblush,vexp = 2,2,4
else:
    p "...Maybe I do."
    $ vbase,vblush,vexp = 2,0,6
vincent "REALLY?"
$ vbase,vblush,vexp = 2,0,6
n "He looked at the other guys in the bar, one of them quickly looking away from him."
vincent "You got more stones than them."
n "Vincent said pointing at me, I felt my face heat up."
vincent "I gotta respect someone who asks for what they want."
n "He held out his arm and I wrapped my hand around it."
n "His arm was thick and muscular."
n "It felt like only a moment till we were at his house."
scene vincent_bedroom_night with fade
show vincent
$ vbase,vblush,vexp = 1,1,4
play music "vincent/vincent_sex.mp3"
n "I could feel his body pushing up against me as he pushed me up against a wall."
n "He didn't bother getting in the bed before he started to grab my hips."
n "I let out a sharp sound as he kissed my neck."
n "His tongue running against my skin."
vincent "Are you fucking crazy?"
n "He whispered near my ear with a low growl."
n "Vincent grabbed my neck with one hand and lifted me off the floor."
vincent "I can snap your neck like a twig."
n "He squeezed my throat, my breaths came out in small pants."
n "Vincent's grip lightened up as he put one hand under my ass."
vincent "Don't worry, I won't do that."
n "His hands gripped my sides as he rubbed his cock against me."
n "He was already hard."
n "His breathing came in fast pants as he bit down on my skin."
n "I let out a quick gasp as I put my hands on his shoulders."
vincent "That's a good sound."
n "He spoke in a low tone, not speaking to me at all."
n "Vincent rubbed himself against me like he was trying to fuck me through my jeans."
n "Teasing me, getting me ready for what was about to come."
$ vbase,vblush,vexp = 1,1,6
vincent "I'm gonna make you my bitch."
$ vincent_love +=10
$ vbase,vblush,vexp = 7,1,4
n "Vincent pulled out a knife and dragged it on top of my pants."
menu:
    "\"Don't do that, asshole.\"":
        jump vincent_pissed_nightzero
    "\"Be careful...\"":

        jump vincent_maso_nightzero

label vincent_pissed_nightzero:
$ vincent_love -=10
$ temper +=10
$ vbase,vblush,vexp = 7,0,5
vincent "Oh.. Y'all wanna tell me what to do hm?"
n "Vincent dragged his knife on my pants."
$ health -=10
n "Vincent lifted up the knife and forced it into my flesh." with vpunch
n "I let out a loud scream and he pushed his hand over my mouth."
$ vbase,vblush,vexp = 7,0,2
vincent "You were fun, now you seem to be losing your flare."
$ vbase,vblush,vexp = 7,0,5
n "I could feel my tears rolling down my face and running onto his hand while he kept me in place."
n "He pushed the knife deeper and I tried to kick my legs."
vincent "Let's try something else."
n "He pulled out handcuffs from his pocket and snapped them around my wrists."
vincent "You're not goin' anywhere."
$ health -=5
n "He pulled me off the bed and I hit the floor." with hpunch
p "What are you doing?!"
n "I screamed, I didn't know if anyone could hear me."
vincent "Whatever the fuck I feel like."
n "Vincent growled as he pulled the knife out."
$ health -=5
n "I screamed as I felt the dull blade tear back out of my skin."
n "He tore through my clothes like paper."
n "I let out a hard sob as I saw the damage done."
n "The small scratches from the blade, all over my legs."
n "He forced my legs down."
$ vbase,vblush,vexp = 1,0,5
n "Vincent leaned down and kissed the wound, causing me to flinch."
vincent "Ah... nice and sensitive."
n "Vincent said with a low growl as he forced his tongue into the new hole."
$ sanity -=10
n "I let out a scream as his tongue pushed inside of me."
$ sanity -=10
n "His hands anchored me down as he sucked the blood out of my wound."
$ vbase,vblush,vexp = 1,0,5
n "He licked his lips and leaned into me."
$ vbase,vblush,vexp = 1,0,4
vincent "You're going to make a good meal."
$ vbase,vblush,vexp = 1,0,5
n "Vincent tore through my jeans and rubbed his cock between my legs."
vincent "First."
n "Vincent pushed his cock into me without warning."
n "He grabbed a fist full of my hair as he rocked in and out."
n "I swung and kicked my legs uselessly against the large man."
$ temper +=10
n "I could hear him panting as he tore through my body."
$ health -=5
n "His free hand raking down my side, his nails pushing into my skin."
$ health -=5
n "I gasped, my voice already hoarse from screaming."
n "His cock felt like it was burning as it forced its way in and out."
n "I gripped the handcuffs around my wrists."
n "I could feel myself getting light headed."
p "...Ah..."
n "I let out a small sound and looked up at Vincent."
n "I felt something warm fill me up."
vincent "You fadin' already?"
vincent "Shit."
vincent "Maybe I shouldn't be so rough with my toys."
n "I could hear Vincent's voice but it all went black."
scene black
with fade
jump vincent_day1_start

label vincent_maso_nightzero:
$ vincent_love +=10
p "V-Vincent."
vincent "Hey, I ain't gonna do anything."
vincent "Not too bad at least."
vincent "Can't blame a guy for liking rough sex right?"
n "Vincent pushed me down on his bed and scraped my jeans."
p "If you r-rip those you're paying for them."
n "Vincent's eye shifted down to me."
$ vbase,vblush,vexp = 7,1,4
n "He let out a low chuckle."
vincent "I'll buy you whatever you want."
n "Vincent tore through my jeans, leaving small scratches on my skin."
n "He looked at the small cuts and ran his tongue over the scratches, causing me to buck my hips."
vincent "Does it hurt?"
n "I nodded but put up my hand."
p "Don't stop."
vincent "You don't need to tell me twice."
n "He pulled the tatters away from my legs and pulled my underwear off."
$ vbase,vblush,vexp = 1,1,4
n "I looked at my own chest, I pulled off my top and folded my arms in front of me as if that would stop him from looking."
n "Vincent grabbed my arms and licked my neck again."
vincent "Don't hide."
n "He rubbed his cock against me and I let him pin my arms above my head."
vincent "...Louder."
n "He let out a guttural growl, it sounded inhuman."
$ vbase,vblush,vexp = 1,1,10
n "I let out another moan as he slammed his hips into me roughly."
p "...VINCENT~! AAAAHH..."
n "I could feel my voice raising as he commanded me."
n "He grinned and pushed his lips against mine."
n "I could feel his long tongue push into my mouth as he moved his hips."
n "My body felt like it was on fire as he came inside of me and I leaned back."
$ vbase,vblush,vexp = 1,1,6
vincent "Haha.... You're good..."
if player_name == "Farz":
    vincent "You feel so familiar..."
    n "He let low pants as I ran my fingers through his hair."
    n "Vincent pulled me close and held me tightly in his arms."
n "Vincent leaned to the side of me and nuzzled my neck."
vincent "Guy could get used to someone like you."
p "Same... to you."
n "I closed my eyes and fell asleep in his arms."
scene black with dissolve
jump vincent_day1_consenual

label vincent_pushy_mc:
vincent "They make me look cool right?"
vincent "As much as I'd love to be a handsome pretty boy-"
vincent "I think this suits me better."
vincent "Any more questions?"
p "Not really. "
vincent "So what are you doin here?"
vincent "I can't imagine you're here to pick up dudes."
menu:
    "\"I'm here to drink!\"":
        $ vincent_love +=5
        jump vincent_get_drunk
    "\"Not sure... I guess I'll get out of here.\"":
        $ temper +=10
        vincent "Ah... That's probably for the best."
        vincent "You don't exactly fit in here."
        n "He walked away from me."
        n "As much as I didn't want to admit it."
        n "He was probably right."
        n "I sighed and left the pool hall."
        jump vincent_left_alone


label vincent_get_drunk:
$ vbase,vblush,vexp = 2,0,1
if player_name == "Farz":
    vincent "Can you even drink, shrimp?"
else:
    vincent "Can you even drink?"
n "Vincent shoved his shoulder into mine walking past me."
n "I bit my lip and looked at him."
p "I could out drink you."
n "Vincent stopped in his tracks and turned to me."
n "He walked back over to me and slammed his palm on the wall by my head."
n "I felt myself flinch at the sound."
n "I slowly shifted my eyes to the dent he made in the drywall."
$ vbase,vblush,vexp = 2,0,2
vincent "You're fuckin on."
vincent "I'll even pay for the drinks."
vincent "That's just the kind of guy that I am."
n "Vincent let out a low snarl as he walked over to the bar."
n "I examined the wall and quickly followed."
n "I took a seat next to him as the bartender put out shots."
$ vbase,vblush,vexp = 2,0,9
unknown "Don't hurt this one, Vincent.."
$ vbase,vblush,vexp = 2,0,8
vincent "I wouldn't do that!"
$ vbase,vblush,vexp = 2,0,5
n "Vincent flicked me on the nose and grinned."
vincent "I'm a heavy drinker I hope you can keep up."
n "I put my hand around the shot regretting challenging him."
n "I took the drink and gulped it down."
n "It burned all the way down my throat."
$ vbase,vblush,vexp = 2,1,5
n "When I looked over Vincent was gulping down his second."
n "I picked up the next shot and felt Vincent's arm around me."
$ vbase,vblush,vexp = 2,1,6
n "He tugged me close and grinned."
vincent "Feeling it yet, kiddo?"
n "I swatted him away and grinned."
$ vbase,vblush,vexp = 2,1,6
p "Not even close."
if player_name == "Farz":
    vincent "HAHAH! Do you drink alot!?"
    p "Sometimes...I have a high tolerance."
    n "Vincent patted me on the head."
    vincent "Fair enough!"
n "I could feel myself downing another shot."
n "But everything was getting fuzzy."
vincent "You wanna get outta here?"
$ vbase,vblush,vexp = 2,1,4
p "...Yeah let's go."
n "I got up on my feet and wobbled into his arms."
n "Vincent caught me and lifted me up with ease."
n "I knew he was talking to the bartender but I buried my face into his shirt instead, smelling him."
n "He smelled like sweat and alcohol but I didn't mind the scent it was nice."
scene vincent_bedroom_night with dissolve
show vincent
$ vbase,vblush,vexp = 1,1,9
$ vincent_dayzero_sex = True
n "It wasn't too long before we were in his house."
n "It all felt like a blur to me as he took off my clothes."
n "He was so rough with me."
$ vbase,vblush,vexp = 1,1,10
n "I let out a soft moan as he growled into my chest."
n "I couldn't focus, greedily taking whatever he had to give me."
scene black with fade
n "I moaned softly as I felt myself orgasming."
n "I could feel my eyes drifting shut."
jump vincent_day1_drunk



label vincent_left_alone:
scene alleyway with fade
n "There was a cafe down the street."
n "I'll just head over there."
n "I let out a sigh as I headed towards the street."
n "I felt a hand on the back of my neck forcing me into the brick wall." with hpunch
$ vbase,vblush,vexp = 6,0,5
$ health -=5
show vincent
$ fbase,fexp = 2,1
$ vbase,vblush,vexp = 6,0,5
vincent "You are so fucking weak."
n "Vincent smashed my head into the wall and I felt myself crumpling to the ground." with hpunch
$ health -=5
vincent "You shouldn't have come here, brat."
n "A low growling voice drifted into my ear."
n "I could feel my vision blurring as I tasted the coppery blood flowing out of my nose."
vincent "You were ripe for huntin'."
vincent "All I needed to do was catch ya."
show farz:
    subpixel True
    xpos 0
show vincent:
    subpixel True
    xpos 500
farz "Vincent, what are you doing out here?"
vincent "I'm just talkin to our buddy here."
n "Vincent caressed the top of my head and I looked up at Farz."
menu:
    "-Ask for help-":
        $ farz_love +=10
        p "He-Help."
        n "I managed to choke out."
        $ fbase,fexp = 2,5
        farz "They look like shit."
        vincent "Yeah, haha I might have hit them a little too hard."
        n "He didn't seem to be interested in helping me."
    "-Say nothing-":
        $ farz_love +=5
        n "I didn't say anything to these two."
        n "I had nothing else to say."
        farz "They're quiet."
        vincent "They're gonna stay that way too."
    "-Scream at them-":
        $ temper +=10
        $ farz_love -=10
        p "FUCK YOU BOTH."
        n "Vincent kicked me in my chest, it felt like he crushed my ribs."
        vincent "You think this is bad?"
        vincent "It's about to get much worse."
        $ fbase,fexp = 2,5

n "Vincent put his boot on my temple."
vincent "Good night."
$ vincent_love = farz_love
n "He stomped on my head, quickly forcing my vision to black."
$ health -=5
scene black
with fade
jump vincent_day1_start

label vincent_day1_consenual:
scene vincent_bedroom_day with dissolve
play music "vincent/vincent_morningafter.mp3"
n "I woke up the next day with a thick heavy arm draped around me."
n "I cuddled into Vincent's chest as his hand swept through my hair as he woke up slowly."
show vincent
$ vbase,vblush,vexp = 5,0,9
n "He looked at the time and rubbed his eye."
p "I better get going."
n "I leaned away from him and he nodded."
vincent "You wouldn't wanna be caught walkin' out of here."
n "Vincent smacked my ass hard as I got out of the bed."
p "HEY."
n "I could feel a blush creeping up on my face, as I put my clothes back on."
n "I looked at the tattered jeans on the ground."
n "Vincent stood up and tossed a pair of sweatpants at me."
vincent "Take those."
vincent "I expect them back."
$ vbase,vblush,vexp = 5,0,6
n "I felt my blush grow."
vincent "Are you still blushing around me?"
$ vbase,vblush,vexp = 5,0,8
vincent "I saw you naked already!"
p "Yeah well, I wasn't expecting you'd wanna see me again."
vincent "Why wouldn't I?"
n "I brushed my shirt against his face trying to swat him away and he sniffed it."
$ vbase,vblush,vexp = 5,0,11
vincent "...Leave that one with me... "
vincent "I like the way you smell."
p "Fine! But you're buying me a new shirt too."
$ vbase,vblush,vexp = 5,0,8
vincent "Deal."
n "Vincent tossed me one of his shirts."
n "An old band shirt."
vincent "You look really cute now."
n "Vincent got out of bed."
vincent "You have a good day now, darlin'."
n "Vincent waved at me and I nodded."
p "You too."
n "I reached for a door and I heard Vincent make a sound."
$ vbase,vblush,vexp = 5,0,7
vincent "WAIT."
play music "vincent/skeletons_in_closet.mp3"
n "I looked down at my feet as something wet and foul-smelling fell out of the closet."
scene CG_vincent_skull with dissolve
$ sanity -=10
n "It looked like a skull."
vincent "Shit."
p "Wh-what is this?"
n "My shaky voice came."
vincent "That was the wrong door."
scene vincent_bedroom_day with dissolve
show vincent
$ vbase,vblush,vexp = 5,0,5
n "Vincent let out a low growl as he rushed from his spot."
n "It felt like only a moment before he pushed me into the wall."
n "I could feel my head colliding with the brick, a warm trickle of blood down the side of my face."
$ health -=10
n "My ears started to ring as I fell to the ground."
n "Vincent walked over me and sighed."
scene black with fade
vincent "...Damn... {size=12}I really liked ya too..{/size}"
jump vincent_day1_start

label vincent_day1_drunk:
play music "vincent/vincent_morningafter.mp3"
scene vincent_bedroom_day with fade
n "I groaned in my sleep and rolled over."
n "I could feel my stomach turn upside down as my nose touched something fuzzy and warm."
n "I slowly opened my eyes and felt a pang in my head."
p "Ugh."
n "I put my hand on the side of my head and felt it throbbing."
n "What did I do last night?"
show vincent
$ vbase,vblush,vexp = 5,0,6
vincent "Had too much to drink then?"
n "Vincent's mocking tone didn't help my headache."
n "That's right, I had a bunch of drinks with Vincent."
n "I opened my mouth to reply to him and felt like everything was going to burst out of my throat."
n "Vincent leaned back and started laughing as I got up to go to the bathroom."
n " I grabbed the doorknob and pulled it open."
$ vbase,vblush,vexp = 5,0,7
vincent "HOLD UP-"
play music "vincent/skeletons_in_closet.mp3"
n "I could hear Vincent's voice behind me but I couldn't focus on it."
$ sanity -=10
n "A putrid smell hit my face as I kneeled down in front of the closet."
n "A revolting smell emanated off of a skull that tapped me on the knee."
scene CG_vincent_skull with dissolve
n "I reached out for it but I couldn't hold back my nausea any more."
n "I threw up on the floor, coughing and gasping for some fresh air."
n "I felt weak and debilitated but I tried to crawl away from the open closet door."
vincent "...Where do you think you're going?"
n "My eyes shot open remembering who I was with."
scene vincent_bedroom_day with dissolve
show vincent
$ vbase,vblush,vexp = 5,0,5
n "I turned my head and looked up at Vincent."
p "...I-"
vincent "Save it."
n "Vincent looked like he was in no mood for anything I had to say as his foot came down on my head."
scene black with fade
n "My nose cracked against the putrescent skull and everything went black."
jump vincent_day1_start

label vincent_day1_start:
scene black with dissolve
play music "vincent/vincent_mainphase.mp3"
vincent "Wake up."
n "I felt a swift kick to my ribs as the air pushed out of my lungs." with hpunch
n "I started to cough uncontrollably as I looked around the room."
scene falloutshelter with dissolve
n "It looked like a fallout shelter."
p "Wh-what's going on?"
$ vbase,vblush,vexp = 7,0,5
show vincent
n "Vincent tossed a knife up and down."
n "His eye followed it, as if he was thinking what to say next."
n "He tossed the knife directly at my head."
$ vbase,vblush,vexp = 1,0,5
n "I tried to dodge it but, my arm hitched."
n "I was handcuffed to a radiator."
n "The knife sailed past my face cutting my cheek and bouncing off the cement near me."
if vincent_dayzero_sex == True:
    vincent "Look kiddo."
    vincent "You saw a little too much."
    vincent "I couldn't just let you walk out of my house."
    n "He turned his head away from me and scoffed."
$ vbase,vblush,vexp = 7,0,5
n "Vincent walked over and picked up the knife."
n "He lifted it up to my throat and leaned in."
vincent "Ya see I got a little anger issue."
show screen vincent_rage_bar
with dissolve
vincent "Some unresolved inner conflict or some hippy dippy shit like that."
n "He pushed the knife up against my throat, the sharp steel cutting lightly into my skin."
n "The adrenaline picked up and my heart started to pound."
n "He pressed it deep and I could feel my blood dripping onto his blade."
vincent "I thought you could help me solve that."
n "He pulled the blade away and licked the blood off of the broad side."
menu:
    "\"I'm not going to help you psychopath!\"":
        $ temper +=10
        $ vincent_love -=10
        n "Vincent kicked me in the stomach again." with vpunch
        if vincent_love <= 0:
            jump vincent_neglove_death
        if temper >=50:
            jump vincent_temper_death
        $ vbase,vblush,vexp = 7,0,7
        n "He looked unamused by me and grabbed a fist full of my hair."
        n "He pulled it upwards."
        vincent "Hey now, I didn't remember asking for your opinion."
        n "Vincent stabbed the knife into my leg and I scratched at his arm with my free hand."
        $ health -=10
        n "I let out a deafening scream."
        $ vbase,vblush,vexp = 7,0,5
        n "He dropped me on the ground as he ripped the knife from my leg."
        n "I put my free hand on the wound, pressing down on it."
        n "I let out a weak sob."
        vincent "Watch your mouth."
        vincent "My patience isn't that great."
        n "Vincent looked down at my wound and pushed down on it with his palm."
        vincent "That's just a shallow cut."
        vincent "I'm gonna be nice to you and not rip it open."
        n "He forced my hand away from my wound, letting it free bleed."
        n "He licked his finger tip and pushed it in my wound."
        $ health -=10
        n "I felt his finger invade my skin and let out another loud scream."
        vincent "Ah, this whole is nice and tight."
        n "He pulled out his fingers and licked the blood off."
    "\"What do you want to do to me?\"":
        $ vincent_love += 10
        n "Vincent picked his ear and looked at it."
        vincent "Nothing much."
        vincent "I got a problem I gotta deal with soon."
        n "He looked at the calendar hanging on the wall."
        $ vbase,vblush,vexp = 7,0,2
        vincent "Real soon."
        vincent "And I thought you could help out."
        $ vbase,vblush,vexp = 7,0,6
        n "He took my free hand and sniffed my wrist."
        $ vbase,vblush,vexp = 7,1,4
        vincent "You're warm."
        n "I gasped as his nose touched my skin."
        n "I wanted to pull away but he held my arm tight."
        vincent "You'll do just nicely."
    "-Say nothing-":
        $ temper +=10
        n "I didn't know what to say to him."
        n "So I just stared at him vacantly looking for words."
        if vincent_love <= 0:
            jump vincent_neglove_death
        if temper >=50:
            jump vincent_temper_death
        $ vbase,vblush,vexp = 7,0,2
        vincent "What? Why you so quiet?"
        $ health -=10
        $ sanity -=10
        n "Vincent stepped on my knee and forced his heel down."
        n "I twisted in pain and let out a small gasp."
        vincent "You don't need to talk."
        vincent "Not now."
        vincent "Pretty soon you're going to be making plenty of noise."
        $ vbase,vblush,vexp = 7,0,4

label vincent_day1_part1:
n "Vincent turned away from me and walked towards the table, sneering at the calendar as he passed it."
n "He picked up something from the table before kneeling in front of me."
vincent "Let's have some fun together."
$ vbase,vblush,vexp = 7,0,6
n "He walked over and scraped the bottom of my foot with the knife."
vincent "Don't make me tie you down."
$ vbase,vblush,vexp = 7,1,5
vincent "It'll be worse."
vincent "Trust me."
vincent "All I have left is razor wire."
$ vbase,vblush,vexp = 7,1,5
$ vincent_razorwire= False

label vincent_razorwire_scream:
$ time = 1.5
$ timer_range = 1.5
$ timer_jump = 'vincent_day1_part2'
show screen countdown
menu:
    "-Struggle-":
        jump vincent_day1_struggle

label vincent_day1_struggle:
$ vincent_razorwire= True
$ temper +=10
hide screen countdown
n "I struggled despite his warning."
n "Vincent sighed and rubbed his fingers down the sides of his face."
$ vbase,vblush,vexp = 7,0,2
vincent "You wanna be a little shit, huh?"
if temper >=50:
    jump vincent_temper_death
$ vbase,vblush,vexp = 1,0,2
n "Vincent put thick leather gloves on."
n "He looked over his shoulder and he pulled a thick rope of razor wire out of the weapons locker in the corner."
$ vbase,vblush,vexp = 8,0,2
n "I scooted my feet back and whimpered."
p "W-wait."
vincent "Now I didn't wanna DO this to you."
vincent "That's why I gave you a warning."
vincent "But y'all just wanna TEST the very LIMIT of my patience."
vincent "I can't have that in my domain, got it?"
vincent "I don't have time to be this much more frustrated with how things are goin'."
n "Vincent kneeled down and played with the razor wire."
vincent "If you wanna be in pain, MORE pain, then what you were already going to be served."
$ sanity -=10
vincent "Then, that's on you."
vincent "But don't cry to me when you can't handle it anymore."
$ vbase,vblush,vexp = 8,1,2
n "I started to kick my feet more in a desperate attempt to stop him from hurting me further."
n "I let out soft whimpers and struggled hard."
p "P-please stop!"
$ health -=10
n "Vincent grabbed my ankles and lashed the wire around."
$ vbase,vblush,vexp = 8,1,4
n "I could feel the sharp edges of the wire digging into my flesh."
$ health -=10
n "He growled and slapped the wire with his gloved hands."
$ health -=10
if health <= 0:
    jump vincent_health_death
n "I could feel the wire dig deeper as it slapped into my skin."
n "I clenched my teeth as he grabbed my chin."
$ vbase,vblush,vexp = 1,1,5
vincent "If I were you, I'd cooperate now."
n "I growled at him and he gripped down harder on my chin."
vincent "I wouldn't do that. "
n "He snapped his teeth at me and I leaned back."
n "I thought he was going to bite my nose off."
vincent "My bite is way worse than my bark."
n "He threw my head back as he took off his gloves, tossing them aside for the knife he abandoned on the floor."
$ vbase,vblush,vexp = 7,1,5

label vincent_day1_part2:
$ vincent_cigburn= False
$ vincent_footcut= False
$ vincent_kicktwice = False
n "Vincent walked over me and flicked the knife between his fingers."
n "He sighed and looked at my toes playing with them individually."
vincent "You got cute feet."
n "Vincent looked up from my toes and tapped the knife on them."
vincent "It'd be a shame if something happened to them."
n "Vincent put the knife between my toes and pushed down."
n "I let out a hiss between my teeth and looked up at him."
n "Vincent wasn't quite pushing but I could feel how sharp the knife was."
$ vbase,vblush,vexp = 7,1,5
$ health -=10
if health <= 0:
    jump vincent_health_death
n "Vincent slid the knife down my foot, cutting deep into the skin."
n "He pushed into my flesh and I screamed throwing my head back."
if vincent_razorwire == True:
    n "I tried to kick my feet but the razor wire was a quick reminder that there was something holding me down."
p "Please stop."
n "I begged as Vincent stopped cutting me."
$ health -=10
if health <= 0:
    n "I could feel the blood dripping down my feet."
    n "...Was my heart beating so much... that I couldn't..."
    jump vincent_health_death
n "I could feel the tears running down my face."
vincent "I can't have you scurrying around in here."
n "Vincent grabbed the handcuff and shook it."
vincent "I've seen some people get out of these."
vincent "I can't have that now."
vincent "There's a lot of dangerous stuff in here."
$ vbase,vblush,vexp = 7,1,6
vincent "So, let me cut you up a bit more before so I don't have to worry about you."
n "My eyes shot open and looked at him."
n "Despite the grin on his face, I could see a dead seriousness in his eye."
menu:
    "-Beg-":
        $ vincent_love +=10
        jump vincent_footcut
    "-Kick him-":
        jump vincent_cigburn

label vincent_footcut:
$ vincent_footcut= True
p "Please."
p "Please stop."
$ sanity -=10
n "I felt a soft sob escape my lips and Vincent kneeled down to look me in the eye."
vincent "You want me to stop?"
$ vbase,vblush,vexp = 7,0,4
n "He leaned in and sniffed me."
n "I twitched trying to pull away from him but he kept my face still."
$ vbase,vblush,vexp = 7,0,1
n "He stuck his tongue out and licked my cheek, wiping my tears away."
vincent "I'll do that for you but, I still need you to not move around so much."
$ vbase,vblush,vexp = 7,0,4
n "Vincent quickly slashed the underside of my other foot."
n "I let out a loud scream as I felt the blood dripping out of the new wound."
vincent "I don't trust you enough to not leave this spot."
$ health -=10
vincent "If I don't see your little foot prints around my bunker."
vincent "We might get along."
vincent "Maybe."
n "Vincent put the knife back in the holster."
$ vbase,vblush,vexp = 1,0,4
jump vincent_day1_part3

label vincent_cigburn:
$ vincent_cigburn= True
if vincent_razorwire== True:
    n "I tried to kick him."
    $ temper += 10
    n "Vincent's eye widened and he tapped the razor wire with the broad of the blade."
    $ sanity -=10
    $ temper += 10
    vincent "Did you forget?"
    if temper >=50:
        jump vincent_temper_death
else:
    n "I kicked my leg."
$ temper += 10
if temper >=50:
    jump vincent_temper_death
n "Vincent laughed and stood up."
$ vbase,vblush,vexp = 1,0,4
n "He pulled a lighter out of his pocket."
n "He picked up a small box and slid a cigarette out of it."
n "He kneeled down rubbed my other foot with his hand."
show CG_vincent_cigburn with dissolve
n "Vincent lit the tip and took in a breath of smoke."
vincent "Ya know, any other day, I might have been into you kicking me."
vincent "But, honestly, I really don't have a lot of patience for it right now."
n "Vincent hovered just a moment and pushed his cigarette into my uncut foot."
n "I let out a loud scream as the hot cinders touched my skin."
$ sanity -=10
$ health -=10
n "He started to grind the cigarette into my skin."
n "It started to root on my nerves sending the pain shooting up my ankles."
n "I clenched my teeth and felt Vincent blow the cigarette smoke into my face."
vincent "You shouldn't kick me, kiddo."
n "He took away from the cigarette looked at the tip."
scene falloutshelter
show vincent
menu:
    "-Apologize-":
        $ sanity -=10
        n "I bit my lip as he looked back at me."
        p "S-Sorry."
        n "I choked out as he put his hand on my thigh rubbing between my legs."
        vincent "Hey now don't worry about it."
        vincent "Just don't do it again and we'll be all good."
        n "I quickly nodded as he caressed my skin."
        $ vbase,vblush,vexp = 1,0,16
        vincent "Be good now."
        jump vincent_day1_part3
    "-Kick him again-":
        $ vincent_love -=20
        $ temper +=20
        $ sanity -=10
        $ vincent_kicktwice = True
        n "I kicked him again."
        vincent "You're fucking kidding me right?"
        if temper >=50:
            jump vincent_temper_death
        n "He didn't say another word, before he punched me in the face." with vpunch
        $ health -=10
        n "All I saw were stars."
        scene black with fade
        jump vincent_dayone_midnight


label vincent_day1_part3:
$ vincent_disgusting= False
$ vincent_omo= False
if vincent_razorwire== True:
    n "Vincent tore the razor wire off my legs and tossed it aside."
    n "I let out a loud shriek as I felt the sharp wire tear away my flesh from my bone."
    $ health -=10
    n "I could feel my blood dripping out of the wounds."
    n "My feet felt cold."
    $ health -=10
    if health <= 0:
        n "I could feel the blood dripping down my feet."
        n "...Was my heart beating so much... that I couldn't..."
        jump vincent_health_death
    n "I let out another hard sob as I leaned my head down."
    n "I wanted to stay awake but it was so hard."
    vincent "Why don't you do yourself a favor and stay still?"
    n "I nodded my head quickly, he seemed pleased with my answer."
    vincent "You struggle again-"
    vincent "You're gonna get more than razor wire."
    vincent "You got me?"
    n "I nodded as I let out a soft sob."
    n "I didn't know what he meant by more than razor wire but I didn't want to find out."
    n "He reached above my head and started to bandage up my wounds from the wire."
    n "I watched him move carefully around the wound and he looked at me."
    vincent "What."
    p "N-nothing."
    vincent "Good."
    vincent "Keep your mouth shut."
    vincent "I don't want you dyin on me yet."
    hide vincent with dissolve
    n "Vincent patted me on the head and looked away from me cleaning something on the table."
else:
    hide vincent with dissolve
    n "Vincent turned away as I let out soft sobs."
    n "He walked back to his table and started to clean up something."

n "I could feel something churning inside of me and I pushed my legs together."
n "I needed to pee..."
n "My bladder was doing flips from being hurt, but my nervousness was getting the better of it now."
p "...Ah..."
n "Vincent looked over his shoulder as I let out the sound."
show vincent with dissolve
$ vbase,vblush,vexp = 1,0,5
vincent "What now?"
n "I blushed as I looked at him rubbing my knees together."
p "I need...I need to pee."
$ vbase,vblush,vexp = 1,0,9
n "Vincent tilted his head to the side."
vincent "Then go."
vincent "No one's stoppin' you."
n "I stared at him."
n "I guess in a way I knew he wouldn't let me just go to the bathroom and use the toilet."
p "I don't want to do it right here.."
n "Vincent made a sound out of the side of his mouth."
$ vbase,vblush,vexp = 1,0,5
vincent "Well I ain't untyin' you."
vincent "Piss there, or hold it."


menu:
    "-Refuse-":
        $ temper += 10
        $ sanity += 10
        $ vincent_love -= 10
        jump vincent_omo_refuse
    "-Agree-":

        $ sanity -=10
        $ vincent_love +=10
        jump vincent_omo_accept
    "-Wait-":

        $ sanity -= 5
        if sanity <= 0:
            jump vincent_badend_vore
        $ vincent_love -= 10
        jump vincent_omo_wait

label vincent_omo_refuse:
$ vincent_disgusting= True
p "NO THAT'S DISGUSTING!"
p "I'M NOT DOING THAT."
n "Vincent tilted his head to the side and sneered."
vincent "Disgusting huh?"
$ temper += 10
if vincent_love <= 0:
    jump vincent_neglove_death
if temper >=50:
    jump vincent_temper_death
n "Vincent walked over to me and kneeled down."
vincent "Do it."
vincent "Take a piss on my floor."
n "Vincent growled narrowing his eyes at me."
n "I shook my head and squirmed."
p "NO."
n "Vincent moved his tongue in his cheek as he stood back up straight."
n "He turned his back on me and I let out a small sigh of relief."
vincent "I changed my mind."
n "Vincent turned quickly on his heel and stomped on my stomach." with vpunch
$ health -=5
if health <= 0:
    jump vincent_health_death
n "My eyes shot open and I coughed as all the air would pushed out of me."
$ health -=5
if health <= 0:
    jump vincent_health_death
vincent "DO IT I WANNA WATCH." with vpunch
$ health -=5
if health <= 0:
    jump vincent_health_death
n "Vincent smashed my gut over and over." with vpunch
$ health -=5
if health <= 0:
    jump vincent_health_death
n "His heavy boot collided with my stomach." with vpunch
n "I gasped and tried to curl up."
p "St-stop! I DON'T- "
n "I let out loud cries until..."
vincent "AH! Good job!"
n "I felt my urine pool around me and I felt the tears falling."
n "I couldn't even look at him."
p "...Wh-why would... you... "
n "I gasped out and slowly lifted my head."
$ vbase,vblush,vexp = 1,1,4
vincent "'Cause, I like it."
vincent "Isn't that why anyone does anything?"
n "He slapped me across the face as he walked towards the door."
n "His loud laughing echoing off the walls."
vincent "Have a good night, kiddo!"
scene falloutshelter:
    subpixel True
    xalign 0.5
    easeout 0.9 xalign 0.95
n "The door shutting with a loud bang."
scene falloutshelter_dark:
    subpixel True
    xalign 0.9
    easein 1.0 xalign 0.5
n "I closed my eyes and cried, feeling everything getting colder."
scene black with fade
jump vincent_dayone_midnight

label vincent_omo_accept:
$ vincent_omo = True
p "...Ah... I don't... want you to watch."
n "I stammered out."
$ vbase,vblush,vexp = 1,0,8
vincent "I wanna watch!"
vincent "I won't make fun of you."
$ vbase,vblush,vexp = 1,1,9
n "A blush crept over Vincent's face."
vincent "I promise."
n "I shifted my legs and he stopped me."
vincent "Wait!"
vincent "Hold it for a few more seconds."
$ vbase,vblush,vexp = 1,1,4
$ sanity -=10
if sanity <= 0:
    jump vincent_badend_vore
p "Wh-"
n "Before I could even complete my thought he tug my bottoms off from around my waist."
n "I let out a small cry as it went over my feet, they still hurt but the pain was replaced by fear as he flicked open a knife."
vincent "Oh yeah! My bad."
vincent "Lemme get these off too."
n "He grabbed the hem of my underwear and tore through the fabric."
p "Vincent!"
n "I squeaked out as he tossed away the cloth."
vincent "I just wanna get a front row look!"
vincent "It's cute."
n "I tried to clamp my legs together but he pushed them apart."
p "I... Don't..."
vincent "Do it."
n "Vincent growled out between his teeth."
n "He wasn't asking nicely anymore."
n "I closed my eyes as I felt my bladder release."
n "Vincent let out an excited sound as I emptied myself on the floor."
vincent "Aaaahhh~"
n "Vincent scooted in, not seeming to notice it was getting on the knees of his pants."
n "He pressed his cock up against my crotch and I squirmed."
vincent "I'm fuckin hard."
n "I let out a gasp as he pressed up against me."
p "N-no."
$ vbase,vblush,vexp = 1,1,5
n "Vincent slammed me into the radiator and I gasped."
vincent "Not really giving you a choice now."
n "He unbuckled his pants and rubbed his cock on me."
p "PLEASE... ST-STO..."
n "He didn't listen as he pushed his way inside of me."
n "I let out a loud scream feeling my muscles tighten around the hard dick inside of me."
vincent "Fuck! You're tight."
if vincent_dayzero_sex == True:
    jump vincent_noncon_day1_tough
else:
    jump vincent_noncon_day1_easy

label vincent_noncon_day1_easy:
n "Vincent gripped my hair and pushed my head back into the radiator."
n "I let out a gasp as he thrusted into me."
n "The sound of light splashing underneath, made me feel sick."
n "I gripped my hands as he huffed."
p "Please... Stop... "
n "I stopped fighting, he was too strong."
n "I didn't want this."
p "You- You can have anyone!"
n "Vincent leaned into me."
vincent "And I wanna have you."
n "I couldn't hold my tears back anymore."
$ sanity -=10
if sanity <= 0:
    jump vincent_badend_vore
n "I started to cry as he leaned in my neck."
vincent "AH! Fuck you're crying."
vincent "It's so fucking cute."
n "He growled out as he came inside of me, dropping my hips on the floor."
if vincent_love >= 20:
    jump vincent_cleanup
else:
    n "Vincent got up and smirked at me."
    vincent "Have a good night, baby."
    scene falloutshelter:
        subpixel True
        xalign 0.5
        easeout 0.9 xalign 0.95
    n "He walked off and opened the door to the bunker."
    p "WAIT!"
    n "Vincent flicked off the light and slammed the door behind him."
    scene falloutshelter_dark:
        subpixel True
        xalign 0.9
        easein 1.0 xalign 0.5
    n "I cried softly into my chest."
    n "I didn't wanna be awake anymore."
    scene black with dissolve
    jump vincent_dayone_midnight

label vincent_noncon_day1_tough:
$ vbase,vblush,vexp = 1,1,5
vincent "Tighter than you were last night."
n "Vincent gripped my hair and pushed my head back into the radiator."
n "I let out a gasp as he thrusted into me."
n "He was right, it hurt so much more than before."
n "I gritted my teeth."
n "I just wanted him to stop."
n "I could feel the bile turning in my stomach as I leaned my head back."
p "Stop... Goddamn it!"
n "Vincent grinned and pushed his forearm into my throat."
vincent "I'll stop when I fucking feel like it."
n "He leaned in and licked the sweat off my forehead."
vincent "Just take it like the bitch you are."
n "He grinned as he thrusted into me harder."
n "I could feel myself tearing on the inside."
$ sanity -=10
if sanity <= 0:
    jump vincent_badend_vore
p "I-It hurts... "
n "I choked out under his forearm."
n "He leaned into me and grinned."
n "In that low southern drawl he whispered."
vincent "Good."
vincent "I want it to hurt."
vincent "You look so much cuter when you cry."
n "I broke...."
n "I started to feel the tears fall down my cheeks as he slammed me hard."
n "I could feel him moan and cum inside me as he dropped my hips on the ground."
if vincent_love >= 20:
    jump vincent_cleanup
else:
    n "Vincent got up and smirked at me."
    vincent "Have a good night.... Baby."
    scene falloutshelter:
        subpixel True
        xalign 0.5
        easeout 0.9 xalign 0.95
    n "He walked off and opened the door to the bunker."
    scene falloutshelter_dark:
        subpixel True
        xalign 0.9
        easein 1.0 xalign 0.5
    n "It slammed shut behind him and I cried softly into my chest."
    scene black with dissolve
    jump vincent_dayone_midnight

label vincent_omo_wait:
p "I'm going.. to wait."
n "I looked to the side and Vincent arched an eyebrow."
vincent "Yeah sure, kid."
$ temper += 10
vincent "You do that."
n "He grinned at kicked me on the chest, knocking the wind out of me."
if temper >=50:
    n "Vincent turned to the table and gripped the sides."
    n "He started to play with various things on the table as if thinking about something."
    jump vincent_temper_death
if vincent_love <= 0:
    jump vincent_neglove_death
vincent "See ya later, kiddo!"
vincent "Don't stay up too late now."
hide vincent with dissolve
n "Vincent said laughing and walking out of the bunker."
n "The metal door shut and I could hear all the mechanisms latch closed."
n "I leaned my head down and felt my pants get warmer."
n "I let the tears fall down my face and leaned my head down."
jump vincent_dayone_midnight

label vincent_cleanup:
n "I looked up at Vincent as he looked at the mess on himself then me."
$ vbase,vblush,vexp = 1,0,1
$ vincent_love +=10
vincent "Tsk. I better clean this shit up."
$ vbase,vblush,vexp = 1,0,5
n "Vincent grabbed a towel above me and wiped me down tossing the towel aside."
p "..W-Why.."
n "Vincent flicked my forehead."
vincent "Don't look a gift horse in the mouth."
n "He wiped up the cement out from under me."
n "He tossed a blanket on my head."
$ vbase,vblush,vexp = 1,0,6
vincent "Go to sleep, brat."
scene falloutshelter:
    subpixel True
    xalign 0.5
    easeout 0.9 xalign 0.95
hide vincent with dissolve
n "He walked off and shut the door behind him."
scene falloutshelter_dark:
    subpixel True
    xalign 0.9
    easein 1.0 xalign 0.5
n "I curled up underneath the blanket, feeling the warmth."
scene black with dissolve
n "I closed my eyes."
$ sanity +=10
n "I felt grateful for the warm cloth around me."
jump vincent_dayone_midnight


label vincent_dayone_midnight:
screen table_button:
    imagebutton xalign 0.648 yalign 0.5465:
        hover ("vincent/tableButton.png")
        idle ("vincent/table_button_nohighlight.png")
        action (Jump('vincent_table_day1'))

screen back_day1_button:
    imagebutton xalign 0.03 yalign 0.01:
        hover ("vincent/back_hover.png")
        idle ("vincent/back.png")
        action (Jump('back_buttonday1'))
screen vincent_food_day1:
    imagebutton xpos 75 ypos 100:
        hover ("vincent/food_button_hover.png")
        idle ("vincent/food_button.png")
        action (Jump('food_day1'))
screen vincent_key_day1:
    imagebutton xpos 0.45 ypos 185:
        hover ("vincent/key_button_hover.png")
        idle ("vincent/key_button.png")
        action (Jump('key_day1'))
screen vincent_teeth_day1:
    imagebutton xpos 600 ypos 275:
        hover ("vincent/teeth_button_hover.png")
        idle ("vincent/teeth_button.png")
        action (Jump('teeth_day1'))
screen vincent_picture_day1:
    imagebutton xpos 750 ypos 0:
        hover ("vincent/picture_button_hover.png")
        idle ("vincent/picture_button.png")
        action (Jump('picture_day1'))

$ vincent_table_day1 = False
$ vincent_food_day1 = False
$ vincent_key_day1 = False
$ vincent_code_day1 = False
$ vincent_teeth_day1 = False
$ vincent_handcuffoff_day1 = False
if vincent_kicktwice == True:
    n "I opened my eyes and looked around."
    n "The bunker was dark."
    n "How long was I out?"
else:
    n "I picked up my head."
    n "I couldn't sleep."
    n "How could someone sleep in this situation?"
    n "I opened my eyes slowly."
scene falloutshelter_dark:
    xalign 0.0
with dissolve
n "I sighed and yanked the hand cuff."
p "..Come on."
menu:
    "-Pull handcuffs-":
        $ handcuff_pull_nightone = 0
        jump vincent_night1_handcuffpull
    "-Go to sleep-":

        jump vincent_night1_gotosleep
    "-Look around-":

        jump vincent_night1_lookaround


label vincent_table_day1:
$ vincent_table_day1 = True
$ vincent_food_day1 = False
$ vincent_key_day1 = False
$ vincent_code_day1 = False
$ vincent_teeth_day1 = False
hide screen table_button
n "...There was something on the table."
n "I moved in that direction to see what I could find."
label screen_tableday1:
hide screen table_button
hide screen health_bar
hide screen vincent_rage_bar
hide screen sanity_bar
show desk
show screen back_day1_button
show screen vincent_food_day1
show screen vincent_key_day1
show screen vincent_teeth_day1
show screen vincent_picture_day1
if vincent_food_day1 == True:
    hide screen vincent_food_day1
if vincent_key_day1 == True:
    hide screen vincent_key_day1
if vincent_code_day1 == True:
    hide screen vincent_picture_day1
if vincent_teeth_day1 == True:
    hide screen vincent_teeth_day1
n "What can I find..."
jump screen_tableday1

label food_day1:
if vincent_food_day1 == False:
    $ vincent_food_day1 = True
    hide screen vincent_food_day1
    n "I picked up the bag of food and looked at it."
    n "It looked like jerky... Did he make this himself."
    n "I opened up the bag and sniffed it."
    n "It smelled like regular meat..."
    n "My stomach growled and I took a piece out."
    n "I nibbled on it and it tasted great!"
    $ health +=10
    n "I shouldn't take too much..."
    $ temper +=10
    n "I ate the piece pulled out and put it back where I found it. "
    jump screen_tableday1

label picture_day1:
    if vincent_code_day1 == False:
        $ vincent_code_day1 = True
        hide screen vincent_picture_day1
        n "I picked up the picture that was tucked under a box."
        p "What's this?"
        n "I looked at the guys in the picture and tilted my head to the side"
        hide screen table_day1
        hide screen table_button
        hide screen back_day1_button
        scene CG_vincent_code with dissolve
        p "Was he in the army?"
        n "I asked to myself as I looked at the back, which was blank."
        n "I sighed softly, he used to be a good guy right?"
        n "I guess anyone could join the military though."
        n "I bit my lip, maybe it wasn't the best idea to fight with him."
        n "If he had combat experience-"
        n "He could take me down pretty quickly."
        show desk
        show screen back_day1_button
        n "I tucked the picture where I found it."
        jump screen_tableday1

label teeth_day1:
    if vincent_teeth_day1 == False:
        $ sanity -=10
        $ vincent_teeth_day1 = True
        hide screen vincent_teeth_day1
        if sanity <= 0:
            n "My vision went blurry and I blacked out."
            jump vincent_badend_vore
        n "I looked at the table and picked up a tooth."
        p "Why would he keep... this.."
        n "I asked myself then looked down at the table."
        n "The pliers were bloody."
        n "Freshly bloody."
        n "When was the last time he had someone down here."
        n "I touched the pliers and dropped the tooth."
        n "I didn't want to know."
        jump screen_tableday1

label key_day1:
    if vincent_key_day1 == False:
        hide screen vincent_key_day1
        $ vincent_key_day1 = True
        n "I looked down at the key."
        n "He must have left a spare here for safe keeping."
        n "He probably didn't count on anyone getting out of the cuffs."
        n "I sighed and picked it up."
        n "I'd have to hide it."
        n "Maybe I could get out of here when he wasn't looking."
        jump screen_tableday1

label back_buttonday1:
scene falloutshelter_dark:
    xalign 0.0
with dissolve
hide screen table_day1
hide screen table_button
hide screen back_day1_button
hide screen back_day1_button
hide screen vincent_food_day1
hide screen vincent_key_day1
hide screen vincent_teeth_day1
hide screen vincent_picture_day1
show screen health_bar
show screen vincent_rage_bar
show screen sanity_bar
n "Now what do I do?"
menu:
    "-Go to sleep-":
        jump vincent_backtosleep_nightone
    "-Check weapons locker-":
        n "I should check out that weapons locker."
        jump vincent_weaponlocker_try

label vincent_night1_lookaround:
$ sanity +=10
n "I tugged at the handcuff again."
n "I wasn't going to pull out of the cuff anytime soon."
n "Unless, I really wanted to hurt myself, and what would be the point of that."
n "I looked around from my spot."
n "But, there wasn't much to look at."
n "I let out a soft sigh. "
n "Maybe there wasn't anything I could do."
n "I closed my eyes and went back to sleep."
jump vincent_day2_morning

label vincent_night1_gotosleep:
$ health +=10
n "I really shouldn't take my chances."
n "I wasn't sure if Vincent would be coming back any time soon and I didn't want to press my luck."
n "I hung my head down and I tried my best to go back to sleep."
n "The fallout shelter produced no sound."
n "I fell into an uncomfortable sleep."
jump vincent_day2_morning

label vincent_night1_handcuffpull:
$ weapon_unlockattempts= 0
n "I pulled at the handcuff around my arm."
n "It seemed pretty loose."
label vincent_nightone_handcuffpull_attempt:
$ time = 2
$ timer_range = 2
$ timer_jump = 'vincent_nightone_giveup_menu'
show screen countdown
label vincent_night1_handcuffpull_menu:
$ vincent_handcuffoff_day1= False
menu:
    "-Pull-":
        show vincent_redvignette
        $ handcuff_pull_nightone += 1
        $ health -=5
        hide vincent_redvignette with dissolve
        jump vincent_night1_handcuffpull_menu

label vincent_nightone_giveup_menu:
hide screen countdown
if health <=0:
    jump vincent_healthdeath_alone
if handcuff_pull_nightone >=3:
    jump vincent_handcuff_free
n "I gave up..."
n "I better not touch anything..."
n "He'd probably get really angry."
n "I just wanted this to be over."
n "I closed my eyes and fell back asleep."
jump vincent_day2_morning

label vincent_handcuff_free:
$ vincent_handcuffoff_day1 = True
hide screen countdown
n "It came off!"
n "But I looked at my arm."
n "It was all cut up and bloody."
if health <=0:
    n "I stood up and waviered."
    jump vincent_healthdeath_alone
n "I held it close to me."
n "He'd notice that for sure."
if vincent_footcut == True:
    n "I got up but I wobbled."
    n "I forgot Vincent cut my foot."
    n "I leaned against the wall and used it to stablize me."
    p "Damn it..."
    n "I cursed softly to myself as I walked towards his workbench."
if vincent_cigburn == True:
    n "I got up and slipped a bit."
    n "My foot felt like it was were on fire."
    n "I slipped in my own blood as I tried to get across the floor."
    p "AH."
    n "I clapped my hands over my mouth, quickly looking around."
    n "He didn't hear me."
    n "I let out a sigh of relief."
n "I reached for a towel that was tucked in the corner and gingerly pressed it against my arm for now."
show screen table_button
n "I looked at his table, there were a lot of small tools all over the place..."
n "Nothing of true value."
hide screen table_button
n "I sighed and looked at the weapons locker."
n "It had a number combination on it."

label vincent_weapon_locker_choice:
menu:
    "-Try it-":
        jump vincent_weaponlocker_try
    "-Go back to radiator-":
        jump vincent_backtosleep_nightone

label vincent_weaponlocker_try:
if vincent_code_day1 == False:
    jump vincent_unknowncode_day1
scene CG_vincent_keypad
$ locker_combination = renpy.input("What's the number...?",length=4)
if locker_combination== "8590":
    jump vincent_weapon_unlock_death
else:
    jump vincent_weapon_wrong_code

label vincent_weapon_wrong_code:
if weapon_unlockattempts == 1:
    jump vincent_weaponlocker_death
else:
    $ weapon_unlockattempts +=1
    n "The locker buzzed."
    n "That wasn't right!"
    menu:
        "-Try again-":
            jump vincent_weaponlocker_try
        "-Go back to the Radiator-":

            scene falloutshelter_dark with dissolve
            jump vincent_backtosleep_nightone

label vincent_unknowncode_day1:
n "I don't know the code."
scene falloutshelter_dark
jump vincent_backtosleep_nightone

label vincent_weapon_unlock_death:
scene falloutshelter_dark:
    xalign 0.0
with dissolve
n "IT OPENED."
n "I let out a happy sound and I opened the locker."
n "Maybe I could find something to kill that sadistic prick with."
vincent "Hey Kiddo."
n "My eyes shot open hearing a voice behind me."
n "I slowly turned my head and was immediately met with an icy cold glare."
show vincent
play music "vincent/vincent_angry.mp3"
$ vbase,vblush,vexp = 1,0,13
n "I put up my hands and took a step back."
p "I... I can explain."
$ temper +=50
vincent "You can explain!?"
$ temper +=50
vincent "WELL, I WOULD FUCKING LOVE TO HEAR IT!"
n "He looked angry as I pressed my back into the weapon locker."
$ vbase,vblush,vexp = 7,0,13
n "He didn't wait for me to respond as he charged across the room with a knife in his hand."
$ health -=10
n "He plunged it into my arm and threw me to the ground."
n "I let out a loud shriek as I hit the floor."
n "I gripped the knife in my arm and looked up at him."
vincent "You wanna see a gun huh?"
show CG_Vincent_Aimed_shotgun with dissolve
n "I could hear him taking a gun off the rack as I turned my body."
n "He put his foot on my stomach and pressed all his weight into me."
n "Vincent stared at me for am moment as I could feel his boot cracking my sternum."
vincent "Here's a gun for you, little prick."
n "Vincent growled through his teeth."
n "I stammered and tried to back away."
n "He slung his gun off his shoulder."
n "He cocked it with one loud click and I closed my eyes."
$ health -=100
n "All I heard was the shell leave the chamber."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_dayone_weaponlocker = True
scene endslate with Dissolve(1.0)
screen vincent_day1_shot:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Vincent blew you away.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_day1_shot
with Dissolve(1.0)
pause
return

label vincent_backtosleep_nightone:
    if vincent_key_day1 == True:
        n "I better not touch anything else."
        n "I walked back to the radiator and looked down at the cuff."
        n "The key."
        n "I unlocked the cuff and locked it around my wrist."
        n "I was glad I didn't have to force it back in."
        n "I slipped the key under the radiator within my reach and leaned back."
        n "I just wanted this to be over."
        n "I closed my eyes and went back to sleep."
        jump vincent_day2_morning
    else:
        n "I better not touch anything..."
        n "He'd probably get really angry."
        n "I walked back over to my handcuff and looked down at it."
        n "How was I going to get back into the cuff?"
        n "I leaned down and played with it."
        n "It was a little blood, maybe that would be enough to slip my hand back into the closed ring."
        n "I played with the ring and pushed my hand into the handcuff."
        n "I let out a soft whimper as I felt my bones slipping past the metal."
        $ health -=5
        n "I sighed and sat back down."
        n "I just wanted this to be over."
        n "I closed my eyes and fell back asleep."
        jump vincent_day2_morning

label vincent_weaponlocker_death:
scene falloutshelter_dark:
    xalign 0.0
with dissolve
n "The locker wailed loudly."
n "The sound of the alarm bounced off the walls and I clapped my hands over my ears."
n "It was so loud there was no way that Vincent hadn't heard it."
n "As quickly as it started it stopped."
n "I blinked as I looked up, maybe he was out?"
n "I didn't hear anything as I took my hands off my ears."
n "In an instant I could feel a hand on the back of my head as my face collided with the storage locker."
n "Blood poured out of my nose as a sheering pain shot up my face."
n "I stumbled as I turned around looking up at Vincent."
show vincent
$ vbase,vblush,vexp = 1,0,2
n "He didn't look like he was in the mood for an excuse."
p "D-don't."
vincent "Don't what? You wanna see what's in there so bad?"
n "Vincent kicked me out of the way and quickly keyed in the code."
vincent "Oh look!"
n "He pulled out a large knife and stepped closer."
scene falloutshelter_dark:
    subpixel True
    xalign 0.0
    easeout 0.9 xalign 0.95
hide vincent
n "I scrambled to my feet and tried to run."
n "I cringed feeling the pain in my feet."
n "I ran away from him."
n "It was almost like he was giving me a head start."
n "I put my hand over my mouth wanting to cry as I grabbed the wheel on the steel door that was my only exit out...."
n "But, I couldn't spin it fast enough."
n "It was too heavy."
n "My breathing sped up as he grabbed me."
n "My heart sank as I felt a heavy hand on my shoulder."
n "He spun me around and forced me to look at him."
vincent "GOTCHA."
show vincent
$ vbase,vblush,vexp = 1,0,5
n "Vincent jammed the knife between my legs and into my crotch."
$ health -=10
vincent "I love playing catch!"
n "I could feel the knife blade digging into me and I let out a loud cry."
$ health -=10
vincent "Look you're excited too."
n "He licked my neck and smirked."
$ health -=10
vincent "Did you cum?"
$ health -=10
$ vbase,vblush,vexp = 1,0,4
vincent "You're all wet."
$ health -=10
n "I wanted to sink to my feet."
$ health -=10
n "I just wanted to run away."
n "But, the blade in me reminded me that I wasn't going anywhere."
p "St-stop..."
n "I choked out weakly."
vincent "No, I don't think I will."
n "Vincent ripped the knife up through my pelvis."
show CG_Vincent_gutsonthefloor with dissolve
$ health -=100
n "I could feel my body convulsing as I watched him push me back into the floor."
n "I couldn't feel anything as I watched him lick his lips."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_weaponslocker_fail = True
scene endslate with Dissolve(1.0)
screen vincent_weaponslocker_day1_fail:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Vincent caught you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_weaponslocker_day1_fail
with Dissolve(1.0)
pause
return



label vincent_nightone_giveup:
hide screen countdown
if health <=0:
    jump vincent_healthdeath_alone
n "I gave up..."
if vincent_key_day1 == True:
    n "I better not touch anything else."
    n "I walked back to the radiator and looked down at the cuff."
    n "The key..."
    n "I unlocked the cuff and locked it around my wrist."
    n "I was glad I didn't have to force it back in."
    n "I slipped the key under the radiator within my reach and leaned back."
    n "I just wanted this to be over.."
    n "I closed my eyes and went back to sleep."
    jump vincent_day2_morning
else:
    n "I better not touch anything..."
    n "He'd probably get really angry."
    n "I walked back over to my handcuff and looked down at it."
    n "How was I going to get back into the cuff?"
    n "I leaned down and played with it."
    n "It was a little blood, maybe that would be enough to slip my hand back into the closed ring."
    n "I played with the ring and pushed my hand into the handcuff."
    n "I let out a soft whimper as I felt my bones slipping past the metal."
    $ health -=10
    if health <=0:
        jump vincent_healthdeath_alone
    n "I sighed and sat back down."
    n "I just wanted this to be over."
    n "I closed my eyes and fell back asleep."
    jump vincent_day2_morning





label vincent_day2_morning:
if vincent_handcuffoff_day1 == True:
    jump vincent_noncon_alcohol
else:
    jump vincent_daytwo_part2_no_break_out
label vincent_noncon_alcohol:
scene black with fade
n "I woke up the next morning to the door opening."
n "Vincent walked in."
scene falloutshelter with dissolve:
    subpixel True
    xalign 0.95
    easeout 0.9 xalign 0.5
show vincent
$ vbase,vblush,vexp = 3,0,8
vincent "Morning, kiddo!"
n "He kneeled down. "
n "Vincent looked at my arm and I attempted hide it behind my back."
$ vbase,vblush,vexp = 3,0,2
vincent "HEY!"
vincent "Don't try to hide it brat!"
vincent "I already saw it."
n "I squeaked as he grabbed my arm and yanked it out from behind me."
p "OW!"
$ vbase,vblush,vexp = 3,0,9
n "He looked at the wound and cocked an eyebrow."
$ vbase,vblush,vexp = 3,0,8
$ temper +=10
vincent "DID YOU GET OUT !?"
vincent "Even though I WARNED you?"
n "Vincent pushed his finger into my wound."
$ temper +=10
$ vbase,vblush,vexp = 3,0,5
vincent "That's fucking ballsy, I could have came in here at anytime, you dumbass!"
$ vbase,vblush,vexp = 3,0,8
n "Vincent nuzzled my face gently."
vincent "I like that."
vincent "Lemme fix that shit for you."
n "He slapped my face and got up."
n "Vincent looked in his cabinet and pulled out a bottle."
$ vbase,vblush,vexp = 3,0,5
vincent "Give me your arm."
n "He demanded and I quickly brought my arm out."
n "Vincent uncapped the bottle."
n "He took a key off his belt and unlocked the cuff."
n "I kept still."
n "With him this close he could spring over and snap my neck in one second."
n "I gulped as he poured down my arm."
p "OW!"
n "I screamed and brought the arm back to myself."
vincent "Give me your arm back."
menu:
    "\"No!\"":
        $ temper +=10
        n "Vincent shrugged and grabbed my arm."
        vincent "You don't have a choice."
        if temper >=70:
            jump vincent_temper_death
        n "He poured it down my arm as I hissed through my teeth."
        p "IT HURTS!"
        vincent "I'm not surprised."
        n "Vincent put his lips to the bottle and chugged a few big gulps."
        $ vbase,vblush,vexp = 3,1,8
        vincent "It's fuckin Everclear."
    "\"What is that!?\"":

        $ temper +=10
        n "Vincent stared at me."
        if temper >=70:
            jump vincent_temper_death
        n "He drank a few gulps out of it."
        $ vbase,vblush,vexp = 3,1,8
        vincent "Everclear."

n "I scooted back and he inched towards me."
vincent "Come on, loosen up."
$ vbase,vblush,vexp = 3,1,5
n "He got up and grabbed my nose."
n "I started to panic my heart raced hard and opened my mouth to breath."
vincent "Ah there you go sweetie!"
n "Vincent jammed the bottle into my mouth."
n "He let go over my mouth as I choked down the liquid."
n "It felt like it was burning all down my throat."
n "My eyes started to water as I choked it back."
n "Vincent took the bottle out of my mouth and slapped his hand over my mouth."
$ vbase,vblush,vexp = 3,1,6
vincent "Swallow it."
n "I could feel the tears running down my face."
n "It felt like all of my insides were on fire."
n "I swallowed it and immediately regretted it."
n "My head spun as Vincent took his hand off my mouth."
$ vbase,vblush,vexp = 3,1,5
vincent "You look so cute."
n "I slumped on the floor."
n "I couldn't sit straight without something holding me up."
n "I threw up on the floor and Vincent tsked."
vincent "Man, what a waste."
vincent "Whatever."
$ sanity -=10
if sanity <= 0:
    n "My vision went blurry and I blacked out."
    jump vincent_badend_vore
show CG_Vincent_vomit with dissolve
n "He pushed his boot into the back of my head and I smelled my own bile and vomit."
n "I scratched at the floor but he wouldn't let me up."
vincent "Lick it."
p "N-No. Please."
vincent "You heard me."
menu:
    "-Do it-":
        jump vincent_vomit_sex
    "-Refuse-":

        jump vincent_vomit_refuse

label vincent_vomit_refuse:
$ temper +=10
p "NO!"
scene falloutshelter with dissolve
show vincent
n "I screamed loudly at him."
if temper >=70:
    jump vincent_temper_death
n "He shrugged a shoulder."
vincent "Well okay."
n "He picked me back up and kicked me into the wall." with hpunch
$ health -=5
if health <= 0:
    jump vincent_health_death
vincent "Open your mouth."
n "He unzipped his pants and stood above me."
n "I looked at I looked at his fly and then back at him..."
label vincent_vomit_refuse_menu:
$ time = 1
$ timer_range = 1
$ timer_jump = 'vincent_open_mouth_slow'
show screen countdown
menu:
    "-Refuse-":
        hide screen countdown
        n "I kept my mouth shut."
        n "I wasn't going to just roll over and do whatever he wants."
        vincent "Look at your tight lips."
        vincent "Tsktsk."
        n "Vincent took a step back and picked up his knife."
        n "He looked at the edge as I backed up."
        n "I got on my knees and scrambled around."
        n "I couldn't get my footing."
        $ sanity -=20
        $ health -=20
        n "Vincent yanked my head up and pushed the knife to the side of my mouth."
        $ vbase,vblush,vexp = 3,1,5
        vincent "Smile, kiddo."
        $ sanity -=20
        $ health -=20
        n "He yanked the knife through my cheek, the blood quickly filling my mouth."
        $ sanity -=20
        $ health -=20
        n "I sputtered and coughed."
        $ sanity -=20
        $ health -=20
        n "The pain blinding me as I felt his knife on the other side of my cheek, tearing through the muscle and flesh."
        $ sanity -=20
        $ health -=20
        n "I tried to scream but the blood was filling my mouth fast."
        n "I couldn't keep my mouth closed anymore as I looked up at him."
        vincent "Shit!"
        vincent "Over did that Glasgow smile huh?"
        vincent "But lookie here."
        vincent "Your mouth is wide open now."
        n "He opened his jeans and pissed right on my face as I slid to the floor."
        n "I felt my head floating as I slid to the floor."
        $ sanity -=100
        $ health -=100
        vincent "Giving up on me?"
        vincent "That's too bad!"
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/vincent_death.mp3"
        $ persistent.vincent_ending_opened_mouth = True
        scene endslate with Dissolve(1.0)
        screen vincent_ending_opened_mouth:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}He opened your mouth.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_opened_mouth
        with Dissolve(1.0)
        pause
        return

label vincent_open_mouth_slow:
$ sanity -=10
if sanity <= 0:
    n "My vision went blurry and I blacked out."
    jump vincent_badend_vore
n "I opened my mouth and put my hands on his hips."
show CG_Vincent_Dick_out with dissolve
n "He pushed his cock into my mouth, a sweaty scent filled my nose and I gagged as his cock reached the back of my throat."
$ vbase,vblush,vexp = 3,1,9
vincent "Wow you're so delicate."
n "He grinned at me and kept his cock back as I gagged again."
vincent "Drink this then."
n "I felt a warm liquid filling up the back of my throat and my eyes shot open."
n "I tried to back away from him and grabbed his legs."
n "But I felt the wall hit my back."
scene falloutshelter with dissolve:
    subpixel True
    xalign 0.95
show vincent
n "Vincent pinched my nose shut as I tried to cough his piss out of my mouth."
menu:
    "-Swallow-":
        $ sanity -=10
        if sanity <= 0:
            n "My vision went blurry and I blacked out."
            jump vincent_badend_vore
        n "I swallowed his piss and he let my nose go."
        $ vbase,vblush,vexp = 3,1,8
        n "Vincent patted my head gently."
        vincent "There you go."
        vincent "Isn't that better?"
        n "He backed off and I fell to the ground without another sound."
        n "I curled in and tried to make myself small."
        if sanity <=30 and temper >=50:
            jump vincent_beatdown_daytwo
        else:
            jump vincent_daytwo_part2
    "-Struggle-":

        $ temper +=10
        vincent "You're gonna drown in it."
        n "Vincent laughed loudly as he kicked my gut."
        $ health -=5
        if health <= 0:
            jump vincent_health_death
        n "He pulled himself out as I started to cough violently onto the ground."
        $ vbase,vblush,vexp = 3,1,6
        vincent "Well whatever."
        vincent "That was fun at least."
        n "He smirked and patted the back of my head as I curled up into a ball on the ground."
        if sanity <=30 and temper >=50:
            jump vincent_beatdown_daytwo
        else:
            jump vincent_daytwo_part2

label vincent_vomit_sex:
$ vincent_love += 10
$ sanity -=20
n "I licked the floor in front of me gently."
if sanity <= 0:
    n "My vision went blurry and I blacked out."
    jump vincent_badend_vore
scene falloutshelter with dissolve
show vincent
n "I didn't want to be hurt by him anymore."
n "Vincent made a low growl as I did and kneeled down."
vincent "Come here, baby."
n "I crawled over to him and he licked the vomit off my lips."
n "I gasped as his lips came close to mine."
n "I clutched his arm and pressed my lips into his."
n "I could feel his tongue pushing into mine."
n "His kiss was hungry."
n "Like he couldn't get enough."
n "I couldn't think anymore."
$ vbase,vblush,vexp = 3,1,16
vincent "Wanna fuck?"
n "His low growl made my body tremble."
n "I nodded and stuck my tongue out."
n "He pushed me on my back and opened his pants."
n "He didn't seem to care about what he was kneeling in."
n "He pushed his way into me and I leaned my head back."
p "Aaaa~ Vincent. "
$ vbase,vblush,vexp = 3,1,4
vincent "You loosened up now?"
n "I left my mouth open as he nuzzled my neck."
n "It felt like he was sniffing me until he pushed his teeth into my shoulder."
n "I let out a loud scream, but, it trailed off into a moan."
$ vbase,vblush,vexp = 3,1,9
vincent "That's what I like to hear."
n "He licked my shoulder and pushed into me hard."
n "I started to pant as he stared up at him."
n "I should have been disgusted by this."
n "But, it just felt good as he pushed his cock into me."
p "...Vin..vincent..."
n "I let out another moan as I felt my eyes closing."
n "I could just feel his warm cum fill me up."
$ vbase,vblush,vexp = 3,0,5
if sanity <=30 and temper >=50:
    jump vincent_beatdown_daytwo
else:
    jump vincent_daytwo_part2

label vincent_daytwo_part2_no_break_out:
scene falloutshelter with dissolve:
    subpixel True
    xalign 0.95
scene falloutshelter with dissolve:
    subpixel True
    xalign 0.95
    easeout 0.9 xalign 0.5
n "Vincent walked in and looked down at me."
show vincent with dissolve
vincent "Were you good all night long?"
n "He kneeled down and uncuffed me."
vincent "Kinda boring, but I ain't gonna judge."
vincent "I wouldn't break outta here with someone like me watching."
jump vincent_daytwo_part2

label vincent_beatdown_daytwo:
$ vexp = 2
n "I watched Vincent walk away from me and run his hand through his hair."
n "He seemed frustrated by something, I rubbed my knees together."
n "I let out a small sound and Vincent looked over his shoulder at me."
vincent "What's your problem?"
p "What's yours?"
vincent "A smart ass hm?"
vincent "I'm pissed off and trying to calm down so I don't cut you from toe to chin."
n "My toes curled thinking about his threat but..."
menu:
    "-Open your legs-":
        jump vincent_beatdown_daytwo_offer
    "-Keep quiet-":

        $ sanity +=10
        $ vincent_love -=10
        n "I kept my mouth shut and Vincent snorted."
        vincent "That's what I thought."
        n "He moved towards me."
        jump vincent_daytwo_part2

label vincent_beatdown_daytwo_offer:
$ vbase,vblush,vexp = 3,0,7
n "I opened my legs slowly for him, exposing myself."
vincent "What are you doing?"
p "If you... wanna take out your aggression on me."
p "You can go ahead."
$ vbase,vblush,vexp = 3,0,1
n "I could feel myself blushing and my heart pounding as he moved closer to me."
n "He leaned in and sniffed my neck."
n "Vincent let out a pleasured sound and pushed me on the floor."
n "He sat down on my legs."
n "I laid still for him and tensed up."
n "My body was stiff but I was breathing hard looking at his knuckles as he cracked them."
n "He put out his hand right in front of my face and I looked at it."
n "I pressed my lips against his rough knuckles and licked the ridges of his fist."
$ vbase,vblush,vexp = 3,1,1
p "Hurt me, I can take it."
$ vbase,vblush,vexp = 3,1,5
n "Vincent scoffed and punched me right in the face." with vpunch
$ health -= 5
$ temper -= 5
if health <= 0:
    jump vincent_health_death
n "I could feel the blood pouring out of my nose but I felt like he was holding back."
n "I licked my own blood as his eye locked on to my body."
n "He pulled back and punched me in the stomach, I could feel the air pushing escaping me."
$ health -= 5
$ temper -= 5
if health <= 0:
    jump vincent_health_death
n "I let out a gasp of pain, but my legs were shaking with excitement underneath him."
vincent "You really like this hm?"
n "I slowly nodded my head and looked at his crotch, he just had sex with me but he was still hard."
n "I licked my lips and looked up at him pleading."
p "Let me take care of that."
n "Vincent's hands shot out and wrapped around my throat pushing hard."
n "My head started to swim."
$ health -= 5
$ temper -= 5
if health <= 0:
    jump vincent_health_death
vincent "What makes you think you can?"
p "Let me try, I want your cock."
n "I tried to choke out my words as best as I can past his large hands."
n "I must have sounded crazy."
n "Why should he trust me with that?"
n "Vincent let my neck go and leaned back."
vincent "Go for it then."
$ vincent_love +=10
n "I happily moved from my spot and leaned down to his pants, unbuttoning him."
n "He was only half way hardened, and I licked my lips."
n "I pushed his cock into my mouth, running my tongue over every ridge."
n "I pushed my tongue around the head and sucked on it gently."
n "He was getting bigger in my mouth and moved my hands to help the rest of the girth."
n "He pushed his hands through my hair and pulled hard forcing me down on his cock."
vincent "Is that all you got?"
vincent "I need more than that."
n "I could feel my tears welling at the edges of my eyes as I gripped his hips."
n "I let him move my head for me as he forced my head down on his cock."
n "I choked and gagged on it but I tried to keep my rhythm."
n "He let out another growl that sent a shiver down my spine."
n "He forced his cock down hard into the back of my throat."
n "I could feel a warm liquid drip down my throat as I looked up at him."
vincent "Ah... You're pretty good at that."
$ vbase,vblush,vexp = 3,1,11
n "His harsh gaze, softening just slightly as I closed his pants."
n "I made a happy sound as he put his arms out."
n "I shifted towards him and let him hold me for a moment."
n "I ran my fingers along his scars as he let out a soft sigh."
vincent "This is nice..."
jump vincent_daytwo_part2

label vincent_daytwo_part2:
if farz_love >= 20 and vincent_handcuffoff_day1 == True:
    jump farz_watchover_daytwo
else:
    $ fbase,fexp = 1,1
    $ vbase,vblush,vexp = 3,0,2
play music "vincent/farz_main.mp3"
n "I heard a loud banging on the door."
n "Vincent pulled his attention away from me and looked over with a frown."
vincent "What is it now?"
n "He moved away from me and opened the door to let whoever it was in."
show farz:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show vincent:
    subpixel True
    xalign 0.8
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0
n "It was that guy from the bar!"
$ vbase,vblush,vexp = 3,0,2
vincent "What do you want?"
farz "I wanted to talk to you about them."
n "Vincent's eye moved from me to Farz."
vincent "What about them?"
$ fbase,fexp = 1,6
farz "Lemme fight them."
$ vbase,vblush,vexp = 3,0,1
vincent "What the fuck? No."
$ fbase,fexp = 1,1
farz "If they're too weak to beat me, then they won't survive your change."
farz "You know that."
farz "You played with them too much."
farz "You've gone a few full moons without killing someone before going berserk."
vincent "Tsk. Why do you care?"
$ fbase,fexp = 1,7
farz "I want to take care of you."
$ vbase,vblush,vexp = 3,0,2
vincent "I don't- Fine. Fuck it."
$ fbase,fexp = 1,5
n "Vincent shoved pass Farz and held out a knife for me."
vincent "You're gonna need it."

menu:
    "-Take the knife-":
        jump vincent_takeknife
    " -Refuse-":

        jump vincent_refuseknife

label vincent_refuseknife:
    if health >=40:
        $ sanity -=10
        if sanity <= 0:
            n "My vision went blurry and I blacked out."
            jump vincent_badend_vore
        p "No."
        p "I won't do it!"
        farz "How boring."
        farz "Nevermind, they don't have much time to live anyways."
        vincent "See. Now let's get outta here."
        n "Vincent pushed Farz out of the room without a second glance at me."
        hide farz with dissolve
        hide vincent with dissolve
        scene black with fade
        jump vincent_day2_night
    else:
        $ vbase,vblush,vexp = 3,0,7
        p "N-no!"
        vincent "You're fucking kidding right?"
        n "He rolled his eye and looked at Farz."
        $ vbase,vblush,vexp = 3,0,5
        vincent "Go ahead. "
        vincent "They don't have fight left in them."
        n "He stepped out of the way."
        $ fbase,fexp = 1,5
        hide vincent with dissolve
        show farz at center with dissolve
        n "He stepped over me and put his foot on my knee pushing down."
        farz "I want to kill you."
        farz "If you're going to just sit there then that'll just make it easier for me."
        p "We can work together."
        p "Yo-You don't have to do this!"
        n "He snorted loudly and stabbed me."
        $ health -=20
        n "I let out a loud scream and put my hands around his, trying to push him off."
        n "He was a lot stronger than he looked."
        farz "Why would I want to help you?"
        n "He twisted the knife and leaned in."
        $ health -=50
        n "I let out a low hiss between my teeth as the pain shot through my stomach."
        $ fbase,fexp = 1,5
        farz "I like him more than you."
        n "Vincent watched with a grin on his face."
        $ health -=50
        n "He pushed the blade through my stomach spilling my guts all over the floor."
        n "I stared in disbelief at the pile of viscera."
        n "I fell on my side and looked up at him."
        n "He was breathing fast and he tucked his hair behind his ear."
        farz "You were easy."
        show CG_Vincent_Cuddle_Farz with dissolve
        n "Vincent came up behind himF and wrapped his arms around Farz's shoulders."
        vincent "Haha, shit."
        vincent "You're still a fucking badass."
        n "I watched him nuzzle under Vincent's chin as my vision went black."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/vincent_death.mp3"
        $ persistent.vincent_ending_refused_knife = True
        scene endslate with Dissolve(1.0)
        screen vincent_ending_refused_knife:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Vincent replaced you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_refused_knife 
        with Dissolve(1.0)
        pause
        return


label vincent_takeknife:
n "I took the knife from Vincent and looked at the sharp blade."
n "I looked at him."
n "I wasn't sure what I could do right now."
n "I held the knife."
menu:
    "-Attack Vincent-":
        n "I got up and gripped the knife."
        n "I had to try."
        jump vincent_attack_him
    "-Defend yourself-":

        if health <30:
            n "I picked up the knife and tried to focus on it."
            n "I felt a bit dizzy."
            p "Fine."
            n "I charged at the other guy and took a swing in his direction."
            n "I could feel his knee colliding with my stomach." with vpunch
            n "He was stronger than he looked!"
            $ health -=10
            n "I started to cough and he laughed pulling my hair roughly."
            $ fbase, fexp = 1,5
            farz "You can't even stand up."
            n "He yanked me hard into the groud grinding his heel into my back."
            $ health -=10
            n "He stomped down hard and scoffed."
            farz "You're so pathetic."
            n "He sat down on my back and took the knife out of my hand without resistance."
            p "Fuck... you."
            n "He pushed my head into the cement and I could feel my face bounce off the floor."
            n "He sat down on my back and twisted his hand into my hair."
            farz "Vincent's had enough fun with you."
            farz "It's my turn."
            show CG_Farz_Stab with dissolve
            n "He carved the knife down my back cutting deep."
            n "I let out a scream as he traced the ridges of my spine with the tip of the knife."
            n "I struggled as he tapped the bones with the tip of his knife."
            n "He pushed the knife into my side and I let out a loud scream."
            $ health -=50
            n "The pain shot down my leg and I scratched to get away from him."
            n "It was blinding."
            p "STOP!!"
            n "I could only scream as he twisted the knife."
            n "It made me feel sick."
            $ health -=50
            n "Everything was going dark."
            vincent "Holy shit, Farz."
            hide screen health_bar
            hide screen sanity_bar
            hide screen vincent_rage_bar
            play music "vincent/vincent_death.mp3"
            $ persistent.vincent_ending_farz_killed = True
            scene endslate with Dissolve(1.0)
            screen vincent_ending_farz_killed:
                text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                text "\n\n\n\n{=endslate_subtitle}You were too weak.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
            show screen vincent_ending_farz_killed
            with Dissolve(1.0)
            pause
            return
        if vincent_love < 90:
            n "I felt good."
            n "I took the knife and smiled at it."
            n "I think I could do it."
            n "I shifted my heel to the other man in the room and advanced on him."
            n "Leaping from my spot, I charged at him and tackled him to the floor." with hpunch
            n "He grabbed my arm to stop me from stabbing him, but I had to try."
            n "I punched him in the face trying to weaken him."
            n "It wasn't working."
            n "We both struggled for a moment, but I was able to push the knife downwards."
            n "He let out a loud growl, struggling to push me off."
            n "He tried to knee me in the stomach but, I kneeled on his other leg."
            n "Just."
            n "A bit."
            n "More."
            $ fbase, fexp = 1,2
            n "I felt his strength give out and I pushed the knife down."
            play sound "vincent/gunshot.mp3"
            $ health -=30
            pause (.5)
            n "A shot ran out in my ears as I felt the knife hit the floor and my hand was bleeding."
            n "My eyes widened as I pulled my hand close, the gaping hole in my hand was bleeding everywhere."
            vincent "I wasn't going to step in."
            $ health -=10
            n "He lowered his handgun and kicked me aside."
            n "Vincent pulled the other guy to his feet and he lunged at me but Vincent forced him back."
            vincent "Watch it, little bird."
            n "He gripped Vincent's arm angrily but did what he was told."
            show CG_VINCENT_gunup_Farzbehind with dissolve
            vincent "Watching you almost get the upper hand on him-"
            vincent "Turns out I'm not ready for a new packmate."
            n "Vincent looked down at the smaller man for a moment."
            vincent "So, you gotta go."
            n "Vincent held up the handgun he used to shoot my hand and aimed it at my head."
            play sound "vincent/gunshot.mp3"
            $ health -=50
            pause (.5)
            hide screen health_bar
            hide screen sanity_bar
            hide screen vincent_rage_bar
            play music "vincent/vincent_death.mp3"
            $ persistent.vincent_ending_stepped_in = True
            scene endslate with Dissolve(1.0)
            screen vincent_ending_stepped_in:
                text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                text "\n\n\n\n{=endslate_subtitle}Vincent stepped in.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
            show screen vincent_ending_stepped_in
            with Dissolve(1.0)
            pause
            return

        if vincent_love >=90 and health >=30:
            $ vincent_love +=10
            $ fexp = 2
            farz "I won't go down so easy."
            n "He lept at me and Vincent took a step back, his hands up."
            n "Vincent was determined to let us just duke it out."
            n "He reeled back his arm and punched me in the face."
            farz "Vincent's mine."
            n "He was a lot stronger than he looked."
            n "I gripped the knife harder as he grabbed my wrist."
            n "He wasn't even talking anymore just making loud angry sounds."
            n "I gripped the knife and cut his hand."
            n "He leaned back and smashed his forehead into my nose." with hpunch
            $ health -=5
            n "I could feel the blossoming from the middle of my face."
            n "He was unrelenting."
            n "I gripped my knife and stabbed him in the side."
            n "He let out an angry sound as he pushed his hands around my neck."
            n "I choked and sputtered as I tried to pull the knife through."
            $ vexp = 7
            hide farz
            play music "vincent/vincent_Loss.mp3"
            n "I dropped the blade as the man fell on top of me."
            show vincent at center
            vincent "Jesus fucking christ, that guy wouldn't go down would he?"
            n "He grabbed my arm and locked me back on the radiator."
            n "Vincent picked him up and looked down at the body."
            $ vexp = 2
            vincent "Shit."
            n "He didn't even glance back at me as he left the room."
            n "The door shut with a loud hollow bang."
            n "I closed my eyes hoping to shut out the image of what I just did."
            scene black with fade
            jump vincent_day2_night

label vincent_attack_him:
    if vincent_love >=70:
        n "I charged at him and he dodged my blade."
        vincent "WOAH SHIT."
        n "He licked his lips and moved quickly behind me."
        n "I wasn't fast enough...."
        n "I was already hurt."
        n "He grabbed my arm and twisted it behind my back, pushing down hard."
        vincent "Ya know, I was was starting to like you a bit."
        vincent "But if you're going to make life hard."
        vincent "Farz was right."
        vincent "You're not worth keeping around."
        n "He grabbed the back of my head and pushed me down into the ground."
        vincent "Sorry, pup."
        n "He grabbed my hair and started to smash my head into the concrete floor."
        n "The pain radiated through my face as he repeatedly bashed my face into the ground."
        n "I could feel all my front teeth breaking inwards."
        $ health -=50
        n "Blood filled up my senses as he dropped me on the ground."
        $ health -=50
        vincent "Pity."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/vincent_death.mp3"
        $ persistent.vincent_ending_worthless = True
        scene endslate with Dissolve(1.0)
        screen vincent_ending_worthless:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You weren't worth keeping.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_worthless
        with Dissolve(1.0)
        pause
        return
    else:
        screen cain_feather:
            imagebutton xalign 0.97 yalign 0.72:
                idle ("vincent/feather_button.png")
                hover ("vincent/feather_button_hover.png")
                action (Jump('cain_VS_Vincent_ending'))
        n "I got up and charged at him from the right side."
        if persistent.cain_call == True:
            show screen cain_feather
        n "He was blind in that eye, I hoped I could use it to my advantage."
        n "But.... It was short lived as I felt myself getting kicked in the leg." with vpunch
        n "I turned my head and looked at Farz."
        hide screen cain_feather
        $ fbase,fexp = 1,5
        n "That shit eating grin."
        n "Vincent put his boot on my chest and smirked."
        vincent "Nice try."
        n "He pulled out a handgun from the back of his pants and aimed it at my head."
        n "He looked at the other person for a moment."
        vincent "Thanks baby."
        play sound "vincent/gunshot.mp3"
        pause (.5)
        n "He grinned and pulled the trigger."
        $ health -=100
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/vincent_death.mp3"
        $ persistent.vincent_ending_help = True
        scene endslate with Dissolve(1.0)
        screen vincent_ending_help:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Vincent had some help.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_help
        with Dissolve(1.0)
        pause
        return


label farz_watchover_daytwo:
$ farz_watchover_night2= True
play music "vincent/farz_main.mp3"
n "Vincent moved away from me and over to the big door."
n "Vincent opened the door and looked at the little brunette."
$ fbase,fexp = 3,1
show farz:
    xalign .9
show vincent:
    xalign .2
$ vblush, vexp = 0,5
vincent "This little shit got out last night."
vincent "Watch over them, Farz."
vincent "I gotta go pick up shit for tomorrow night."
farz "Of course, Vincent."
n "Vincent leaned down and gave him a small sniff and a kiss behind the ear before he walked away."
hide vincent
show farz at center
n "Farz slammed the giant door shut and spun the wheel, sealing both of us inside."
n "He climbed up on Vincent's table and kept his eyes on me."
menu:
    "-Talk to him-":
        $ farz_love -=10
        p "Hey-"
        $ fbase,fexp = 3,2
        farz "Shut up, no one gave you permission to talk."
        jump farz_daytwo_talk
    "-Say nothing-":

        $ farz_love +=10
        farz "You're lucky you know?"
        farz "H-he's pretty violent around these times."
        farz "You're lucky he didn't kill you."
        jump farz_daytwo_nothing

label farz_daytwo_nothing:
menu:
    "\"Is that what happened to your eye?\"":
        $ farz_love +=10
        n "His hand shot up to touch the swollen skin around his eye."
        farz "He didn't do it because he was pissed at me."
        farz "I asked him to do it."
        p "Why would you ask him to do it?"
        farz "You wouldn't understand."
        if farz_love <=40:
            jump farz_daytwo_teach
        else:
            jump farz_daytwo_punishment
    "\"You're crazy if you think getting tortured is lucky!\"":

        $ farz_love -=10
        farz "You think this is bad?"
        farz "Just wait and see what he's got for you."
        n "He scratched his knife across the table top then picked his nails."
        farz "It's not pretty."
        if farz_love <=40:
            jump farz_daytwo_teach
        else:
            jump farz_daytwo_punishment

label farz_daytwo_talk:
    menu:
        "\"Those are cute ear cuffs.\"":
            $ farz_love +=10
            farz "Oh you think so?"
            n "Farz put his hands to his ears."
            farz "Vincent gave them to me."
            $ fbase,fexp = 3,7
            n "He sounded proud and gave me a happy sigh."
            farz "Relic of his youth or something."
            farz "He doesn't remember but he says they look better on me."
            n "He stuck out his tongue and showed me a tongue ring."
            $ fbase,fexp = 3,5
            farz "He's real good to you if you treat him right."
            farz "Not that you'd know shit about that."
            if farz_love <=40:
                jump farz_daytwo_teach
            else:
                jump farz_daytwo_punishment
        "\"Why do you do anything for him?\"":

            $ farz_love -=10
            p "All he does is beat on you."
            p "Why do you do anything for him?"
            farz "I asked him to hit me."
            farz "You wouldn't understand."
            if farz_love <=40:
                jump farz_daytwo_teach
            else:
                jump farz_daytwo_punishment

label farz_daytwo_teach:
$ vincent_love +=10
p "Maybe you can teach me?"
n "I needed to appeal to him."
n "I didn't know what else to do, and Farz was safe with Vincent."
farz "You want me to teach you how to be a masochist?"
farz "It's not taught, it's something that you just have."
n "I crawled towards Farz and felt my arm hitch on the radiator."
n "Farz got out of his spot and stood above me, just out of reach."
p "Please, I just want to be useful to you."
$ fbase,fexp = 3,2
n "Farz scoffed and kicked me in the stomach, he hit hard." with vpunch
$ health -=5
if health <= 0:
    jump farz_hp_death
farz "What use are you to me?"
n "I put my hands on his foot and he kicked me away." with vpunch
$ health -=5
if health <= 0:
    jump farz_hp_death
p "I can help you... with anything."
p "Whatever you want, name it!"
n "Farz rubbed his chin and grabbed my head."
$ fbase,fexp = 3,5
farz "Anything huh? Vincent needs your blood."
farz "I don't know why."
farz "Maybe just cause he needs to drink it because of his werewolf thing."
farz "You can give it to me."
$ fbase,fexp = 4,5
n "I watched Farz reach into his back pocket and pull out a knife."
n "I flinched and moved back."
farz "Don't you want me to teach you?"
farz "I'm going to teach you."
menu:
    "-Refuse-":
        $ farz_love -=10
        jump farz_daytwo_punishment
    "-Let him teach you-":
        $ farz_love +=10
        jump farz_daytwo_teach_blood

label farz_daytwo_teach_blood:
n "I crawled over to him."
p "Please, teach me."
n "Farz grabbed my arm and looked at the veins in my arm."
farz "You're life doesn't belong to you anymore."
farz "It's mine."
farz "It's Vincent's and we can do whatever we want to you."
n "Farz grabbed my arm and sliced it without even thinking twice."
n "The blood dripped out of it and I screamed holding my arm in pain." with vpunch
$ health -=10
if health <= 0:
    jump farz_hp_death
farz "NOW SMILE."
n "I looked up at him with a defeated look."
menu:
    "-Smile-":
        $ farz_love +=10
        n "I smiled at him as best as I could."
        farz "Good."
        n "He punched me in the face and I reeled back."
        n "I put my hands over my nose and tried to stop the bleeding."
        n "But, I didn't cover up my smile."
        farz "Go to sleep."
        farz "I'll tell Vincent what you did."
        $ vincent_love +=10
        scene black with fade
        n "I watched the door open and listened to it slam shut."
        jump vincent_day2_night
    "-Don't smile-":

        n "I spat in his face."
        farz "You shit."
        n "Farz charged at me and pulled out his knife."
        farz "I'll TEACH YOU MANNERS."
        n "He grabbed my face and plunged his knife into my eye."
        n "I screamed in his face."
        n "I cursed him."
        n "But no matter how much I fought and screamed."
        n "He was stronger than me."
        n "The pain shot through my face as he carved the skin around my eye."
        n "He reached in, shoving his fingers in the open wound."
        show CG_Farz_eyepull with dissolve
        n "Farz didn't say anything as he pulled my eye from my face."
        n "I could feel my body shake and convulse in pain."
        n "I grabbed his arm and tried to push him off."
        $ health -=100
        farz "It's too bad that you couldn't last."
        farz "Vincent might actually like you."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/farz_death.mp3"
        $ persistent.farz_ending_carved_eye = True
        scene endslate with Dissolve(1.0)
        screen farz_ending_carved_eye:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Farz pulled out your eye.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen farz_ending_carved_eye
        with Dissolve(1.0)
        pause
        return

label farz_daytwo_punishment:
n "Farz took out a knife and flicked it open."
n "He looked at the tip and pushed it into his finger."
farz "You know."
farz "I could help you understand."
n "He got up from the table and played with his knife."
n "I backed up into the radiator and Farz kneeled down."
farz "Let's play a little game."
menu:
    "\"No.\"":
        $ farz_love -=10
        p "I don't want to play a game with you."
        n "Farz punched me in the face." with vpunch
        $ health -=10
        if health <= 0:
            jump farz_hp_death
        farz "I'm not giving you a choice."
    "\"Okay...\"":

        $ farz_love +=10
        n "He lit up and pointed to the ground."
        farz "Good choice."

farz "Put your hand out and spread your fingers wide."
n "He spread out his fingers and put his palm down on the floor."
n "I copied him and he put his knife between my fingers."
farz "Watch."
n "He started to stab between my fingers."
n "Farz's motion was so quick that I almost couldn't keep up with my eyes."
n "I fidgeted and Farz cut my finger."
n "I let out a scream as he sliced into my finger."
$ health -=5
if health <= 0:
    jump farz_hp_death
n "The knife almost hit my bone as I tried to pull back my hand."
n "Farz grabbed my wrist and forced my hand back down."
farz "I'm not done."
farz "I need someone to practice on."
menu:
    "-Put your hand down-":
        $ farz_love +=10
        n "I put my hand back down, shaking but I didn't want to infurate him more."
        n "Farz started to stab between my fingers quickly again."
        n "I couldn't even keep up with his movements."
        n "He cut me on some stabs."
        n "Most of them missed my fingers or only gave me small cuts."
        farz "See."
        farz "It's not so scary if you listen."
        n "Farz pulled his knife away from my shaking hand."
        n "It was bleeding and throbbing in pain."
        farz "You should listen to me."
        farz "I can make your life so much easier."
        farz "What's left of it at least."
        scene black with fade
        n "Farz got up and walked away, slamming the heavy metal door shut."
        n "I closed my eyes and clutched my hand close to me."
        jump vincent_day2_night
    "-Refuse-":

        $ farz_love -=10
        n "Farz shrugged."
        farz "Your loss."
        n "He got back up and left me in the room alone as I pulled my hand close to me."
        n "Farz was so quick."
        n "I needed to be careful."
        scene black with fade
        n "I held my hand close to me and shut my eyes."
        n "I just needed to go back to sleep."
        jump vincent_day2_night

label vincent_day2_night:
screen back_day2_button:
    imagebutton xalign 0.03 yalign 0.01:
        hover ("vincent/back_hover.png")
        idle ("vincent/back.png")
        action (Jump('back_buttonday2'))

screen vincent_food_day2:
    imagebutton xpos 75 ypos 100:
        hover ("vincent/food_button_hover.png")
        idle ("vincent/food_button.png")
        action (Jump('vincent_food_day2'))
screen vincent_dogtags_day2:
    imagebutton xpos 600 ypos 275:
        hover ("vincent/dogtag_button_hover.png")
        idle ("vincent/dogtag_button.png")
        action (Jump('vincent_nighttwo_dogtags'))
screen vincent_picture_day2:
    imagebutton xpos 750 ypos 0:
        hover ("vincent/picture_button_hover.png")
        idle ("vincent/picture_button.png")
        action (Jump('vincent_picture_day2'))


$ vincent_food_day2 = False
$ vincent_dogtags_day2= False
$ vincent_picture_day2= False
if farz_watchover_night2== True:
    jump farz_night2
else:
    scene falloutshelter_dark:
        xalign 0.0
    n "I woke up and looked at the handcuff."
if vincent_key_day1 == True:
    n "I picked up the key from under the radiator and looked at it."
    n "I was glad I went looking around the first day."
    n "I might have never gotten out of the cuffs, I was too tired today."
    n "I unlocked the cuff."
    n "Now I could look around."
    jump vincent_night2_lookaround
else:
    n "I was too tired..."
    n "I couldn't pull my arm out."
    n "I leaned back and went back to sleep."
    jump vincent_day_three

label vincent_night2_lookaround:
menu:
    "-Look around-":
        jump vincent_table_night2
    "-Look at weapons locker-":

        n "I might as well see if I could protect myself."
        n "I walked over to the weapons locker."
        jump vincent_weapons_locker_night2
    "-Back to sleep-":

        jump vincent_sleep_night2

label vincent_sleep_night2:
$ vincent_love -=20
$ sanity -=10
$ health +=10
n "I was too tried to keep looking around."
n "I sat back down and locked myself back into the cuff."
n "I closed my eyes and went back to sleep."
jump vincent_day_three

label vincent_weapons_locker_night2:
$ vincent_picture_day2 = vincent_code_day1
if vincent_code_day1 == False or vincent_code_day1 == False:
    jump vincent_night2_nocode
scene CG_vincent_keypad
$ locker_combination = renpy.input("What's the number...?",length=4)
if locker_combination== "8590":
    jump vincent_weapon_unlock_death_night2
else:
    jump vincent_weapon_wrong_code_night2

label vincent_weapon_wrong_code_night2:
if weapon_unlockattempts == 1:
    jump vincent_weaponlocker_death
else:
    $ weapon_unlockattempts +=1
    n "The locker buzzed."
    n "That wasn't right!"
    menu:
        "-Try again-":
            jump vincent_weapons_locker_night2
        "-Go back to the Radiator-":

            scene falloutshelter_dark with dissolve
            $ vincent_love -=10
            n "I didn't want to try anymore."
            n "If this thing was armed..."
            n "I didn't know what Vincent would say if he saw me messing with his stuff."
            jump vincent_day_three

label vincent_night2_nocode:
n "I don't know the code still."
n "I better not touch this."
n "I wandered back to my spot on the floor."
n "Better go to bed."
$ sanity +=10
scene black with fade
jump vincent_day_three

label vincent_weapon_unlock_death_night2:
n "I punched in the numbers and opened up the locker."
n "I breathed deep a sigh of relief as I grabbed the shotgun off the rack."
if vincent_love < 90:
    n "Maybe I could kill that bastard this time."
else:
    n "What was I going to do with this?"
    n "I felt a sinking in my stomach."
    n "Did I really want to kill him?"
scene falloutshelter_dark:
    xalign 0.0
n "I heard the door opening and I quickly shut the locker, scrambling back to my spot on the floor."
n "I didn't bother locking my hand this time."
n "Vincent walked into the room and closed the door behind him."
show vincent
$ vbase,vblush,vexp = 3,0,2
if vincent_love < 90:
    n "Now was my chance.."
else:
    n "I felt the gun behind me and gripped it."
menu:
    "-Shoot Vincent-":
        jump vincent_shot_day2
    "-Drop weapon-" if vincent_love >=90:
        jump vincent_hard_blowjob
    "-Threaten him-":
        $ vincent_love -=10
        jump vincent_hard_gunjob

label vincent_hard_gunjob:
n "I aimed the gun at him."
$ vbase,vblush,vexp = 3,0,13
vincent "WOAH WAIT A SECOND."
vincent "DROP IT."
n "I could feel myself shaking as I lowered the weapon."
n "Vincent grabbed the barrel."
vincent "You fucking idiot, you really think I would fill this with something you could kill me with?"
$ vincent_love -=40
n "Vincent yanked the gun from my hand and rammed the stock into my chest."
n "I felt the air leave my lungs and I started to cough and stumble."
n "He aimed the gun at my leg and fired."
$ health -=40
n "I felt pellets rip through my leg and I let out a loud scream as I fell to the ground."
vincent "It's fucking bird shot."
vincent "For teaching bastards like you a lesson."
$ vbase,vblush,vexp = 3,0,2
n "Vincent pushed his boot into the wound and I whimpered in pain."
$ health -=20
n "He dug his heel in and cocked his head to the side."
$ vincent_love -=40
vincent "Open your mouth."
p "...I-I'm... so-s-"
n "I choked out but he wasn't interested in my apology."
$ vbase,vblush,vexp = 3,0,13
vincent "Open your FUCKING mouth."
n "I complied and opened my mouth for him."
n "He smirked and shoved the barrel of the into my mouth."
show CG_vincent_SHOTGUN_JOB with dissolve
n "I could feel the steel in my throat as he started to rub it in and out."
vincent "Suck on it like your life depends on it."
n "He cocked the gun and shoved me on the ground."
$ vbase,vblush,vexp = 3,0,2
vincent "Cause it does."
n "I started to gag as the hard tip entered my throat."
n "Vincent watched me unwavering as I started to lick the underside of the barrel."
n "I let out a hard choking sound as he pushed his boot into my wound again."
n "Tears started to run down my face as I tried to breath."
n "It was too much."
n "The taste of gunpowder, his heavy boot in my wound."
n "I threw up into the gun and he laughed loudly."
vincent "Is that all you got?"
n "He growled in a low tone and put his finger over the trigger."
vincent "...Pathetic."
n "I could see him pulling the trigger and the pellets entered the back of my throat."
$ health -=100
n "I coughed up blood and laid to the side."
vincent "Too bad... I was starting to like you."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
$ persistent.vincent_dropped_weapon_death = True
scene endslate with Dissolve(1.0)
screen vincent_dropped_weapon_death:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You gave up your gun. {/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_dropped_weapon_death
with Dissolve(1.0)
pause
return

label vincent_hard_blowjob:
n "I looked at the gun and held it out for him to take."
vincent "You fucking idiot, You really think I would fill this with something you could kill me with."
n "Vincent yanked the gun from my hand and tossed it away."
vincent "Why the fuck, did you do that?"
vincent "Goddamn it."
n "He grumbled to himself."
n "He seemed agitated and confused."
$ vbase,vblush,vexp = 3,0,2
n "I opened my mouth to speak but he put his hand up."
vincent "DON'T."
vincent "Don't say a goddamn..."
$ vbase,vblush,vexp = 3,0,13
vincent "FUCKING..."
$ vbase,vblush,vexp = 3,0,2
vincent "...thing to me right now."
n "Vincent looked at the weapons locker and put his hand on the open door."
vincent "How'd you know the code?"
vincent "You put it out in the open, duh."
n "He seemed to be talking to himself."
n "What should I do?"
n "I got up quietly and put my hand on his back."
n "He stiffened as I felt his skin."
vincent "Don't."
n "He warned but I didn't listen."
p "I'm sorry."
n "I said as I ran my hands down his muscular back."
n "He stood perfectly still, listening."
vincent "It takes some serious fucking balls to aim a gun at your captor."
vincent "You don't know what I could have done to you."
n "Vincent spoke in a slow, thoughtful manner."
n "He was thinking about what he was going to do with me."
n "I shuffled around him and looked at his face."
$ vbase,vblush,vexp = 3,0,12
p "I-I'm sorry."
p "I'll do whatever you want."
p "Please."
n "He looked to the side and tsked out of his mouth."
vincent "You can't just do whatever you want."
n "He said as I rubbed my head under his chin."
n "He let out a low growl but it seemed to be.. happy."
p "I know that, I just."
vincent "Wanted to get away from me?"
$ vbase,vblush,vexp = 3,0,2
n "I paused and looked at the gun."
n "That gun didn't make me free."
n "I looked up at him and pawed at his chest."
p "I don't want to get away.."
p "Tell me what... I can do to make it up to you."
n " He gripped my hair and forced me to my knees."
n "He shoved his crotch in my face."
vincent "You know how."
n "Vincent growled between his teeth as I pulled open his jeans."
$ vbase,vblush,vexp = 3,0,1
n "He was only half erect."
n "He must have still been frustrated."
n "I leaned into his cock and took it into my mouth."
n "He let out a ragged breath as I pushed it as deep as I could."
n "It started to get hard inside my mouth."
n "I wanted to make him happy."
$ vbase,vblush,vexp = 3,1,2
n "I started to bob my head taking it deeper and deeper."
n "I shuttered as I choked on the hard flesh and looked up at him with tears in my eyes."
n "He was starting to pant and look happy."
$ vbase,vblush,vexp = 3,1,16
n "He must have liked that."
n "I started to push his cock deep into my throat and gagged on it."
n "I didn't stop despite my reflexes."
n "I choked again but kept taking it down my throat."
n "He pushed me against the wall and fucked my skull."
n "I couldn't breath, but it felt so good."
n "I gagged, bile coming up this time but I didn't care."
n "I let it drip down my chest and around his cock as he took what he wanted from me."
n "The inhuman growls, the way he put his strong hands in my hair."
n "I was intoxicated."
n "He slammed me harder and harder into the wall."
n "My back started to ache but I just wanted more."
n "The bile hit my throat again as it dripped out between us."
n "I coughed it out."
vincent "Fuck..."
n "He growled as he came down my throat."
n "He slowly pulled away."
n "A trail of saliva and vomit between his dick and my lips the only thing connecting us."
n "I swallowed whatever was in my mouth, mostly cum."
$ vbase,vblush,vexp = 3,0,2
vincent "Don't try that shit again."
n "Vincent said pointing at the gun."
n "I grabbed his leg and rubbed my head on his knee."
p "I won't."
n "I said happily as he reached down to pet the top of my head."
n "He didn't seem angry anymore."
n "And I was glad."
n "He let me go as I shuffled back to the wall."
n "He locked up his weapon locker again, this time with a padlock."
n "I wasn't going to try it but I could see his concern."
vincent "Go to sleep, pup."
n "Vincent patted my head again as he passed by."
hide vincent with dissolve
n "I closed my eyes and leaned against the wall."
scene black with fade
jump vincent_day_three

label vincent_shot_day2:
n "I got up and aimed the gun at him."
$ vbase,vblush,vexp = 3,0,7
vincent "Woah wait a second."
n "Vincent said looking at the gun then at me."
vincent "You don't wanna-"
n "I cut him short."
hide vincent with dissolve
n "I shot straight into his chest and he fell backwards."
n "I smiled and held the gun close."
n "I needed to shoot him in the head now."
n "It wouldn't be too hard if he was down."
n "I walked over and aimed the shotgun at his face."
$ vbase,vblush,vexp = 9,0,13
n "But, before I could pull the trigger he grabbed the barrel and yanked it away."
show vincent
n "He bashed the butt of the shotgun into my nose and snarled loudly."
vincent "WHAT THE FUCK DID I JUST SAY?"
$ temper +=100
n "He stood over me and growled as he pulled the pellets out of his chest."
n "He stomped my leg and I heard it crack underneath his boot."
n "I let out a scream as he started to dig in his chest."
$ vincent_love -=100
n "He flicked some metal pieces away and leaned down and grabbed my hair."
vincent "Birdshot ain't gonna kill me!"
vincent "I'm not human!"
n "He picked up the shotgun and shot into my other leg."
$ health -=10
n "I could feel the pellets tearing through my skin and flesh."
$ health -=10
n "I let out another scream as Vincent put the tip of his boot in my mouth."
$ health -=10
vincent "Plus, it's for torturing stupid fucks like you."
vincent "Target practice."
n "I tried to scream but he brought his foot down on my jaw."
$ health -=10
n "He narrowed his eye and stepped down hard."
$ health -=10
n "I could feel his boot cracking my jaw."
$ health -=100
n "Then my throat."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_kill_him = True
scene endslate with Dissolve(1.0)
screen vincent_ending_kill_him:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You couldn't kill him.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_ending_kill_him
with Dissolve(1.0)
pause
return

label back_buttonday2:
scene falloutshelter_dark:
    xalign 0.0
hide screen vincent_food_day2
hide screen vincent_dogtags_day2
hide screen vincent_picture_day2
hide screen back_day2_button
show screen health_bar
show screen vincent_rage_bar
show screen sanity_bar

n "I didn't feel like looking at this anymore."
menu:
    "-Look at weapons locker-":
        n "I might as well see if I could protect myself."
        n "I walked over to the weapons locker."
        jump vincent_weapons_locker_night2
    "-Back to sleep-":

        jump vincent_sleep_night2

label vincent_table_night2:
n "I walked back over to the table maybe there was something useful on it this time."
show desk
show screen back_day2_button
show screen vincent_food_day2
show screen vincent_dogtags_day2
show screen vincent_picture_day2
hide screen health_bar
hide screen vincent_rage_bar
hide screen sanity_bar
label vincent_night2_tableexplore:
if vincent_food_day2 == True:
    hide screen vincent_food_day2
if vincent_dogtags_day2== True:
    hide screen vincent_dogtags_day2
if vincent_picture_day2== True:
    hide screen vincent_picture_day2
if vincent_code_day1 == True:
    hide screen vincent_picture_day2
n "What can I find..?"
jump vincent_night2_tableexplore

label vincent_food_day2:
$ vincent_food_day2 = True
hide screen vincent_food_day2
n "I picked up the bag and looked at the meat."
n "My stomach rumbled but I put it back down quickly."
n "What if this was... people or something?"
n "My mind started to race and I felt sick."
$ sanity -=10
jump vincent_night2_tableexplore

label vincent_picture_day2:
    $ vincent_picture_day2 =  True
    $ vincent_code_day1 = vincent_picture_day2
    hide screen vincent_picture_day2
    n "I picked up the picture that was tucked under a box."
    p "What's this?"
    n "I looked at the guys in the picture and tilted my head to the side"
    hide screen back_day1_button
    scene CG_vincent_code with dissolve
    p "Was he in the army?"
    n "I asked to myself as I looked at the back, which was blank."
    n "I sighed softly, he used to be a good guy right?"
    n "I guess anyone could join the military though."
    n "I bit my lip, maybe it wasn't the best idea to fight with him."
    n "If he had combat experience-"
    n "He could take me down pretty quickly."
    show desk
    show screen back_day2_button
    n "I tucked the picture where I found it."
    jump vincent_night2_tableexplore

label vincent_nighttwo_dogtags:
$ vincent_dogtags_day2 = True
hide screen vincent_food_day2
hide screen vincent_picture_day2
hide screen vincent_dogtags_day2
hide screen back_day2_button
scene CG_vincent_dogtags
n "I picked up his dog tags and looked at them."
p "Vincent Metzger."
n "I whispered out loud to myself."
$ vincent_love +=10
$ temper +=10
play music "vincent/vincent_sad.mp3"
vincent "Yeah that's me."
vincent "What of it."
scene falloutshelter_dark:
    xalign 0.0
    easeout 0.3 xalign 0.5
show screen health_bar
show screen vincent_rage_bar
show screen sanity_bar
n "I turned quickly."
$ vbase,vblush,vexp = 3,0,2
show vincent with dissolve
n "He didn't look like he was going to attack me."
p "You were in the army?"
n "I asked as I held out the dog tags for him."
vincent "Yeah. I was once."
n "He took the tags and looked at them."
p "Why'd you leave?"
$ vbase,vblush,vexp = 3,0,14
vincent "I got attacked."
vincent "That's why I look like I got into a fight with a blender and lost."
p "Do you remember anything before that?"
n "Vincent paused looking for the words."
vincent "No."
n "He tapped his skull and shrugged."
vincent "Lost it all in a car accident."
vincent "All my childhood memories."
vincent "Lost my family too, except my dad."
n "He nodded his head towards the spot on the floor and I walked that direction."
n "I sat down and he cuffed me back to the radiator."
$ vbase,vblush,vexp = 3,0,2
vincent "The key."
n "I smiled sheepishly and gave him the key."
vincent "I know you took it brat."
n "He tussled my hair and looked at it."
vincent "You're pretty brave."
p "Brave or stupid."
$ vbase,vblush,vexp = 3,0,6
vincent "It's one of those two things."
$ vbase,vblush,vexp = 3,0,2
vincent "Stay in this spot alright?"
p "Okay."
n "He held out a can and shook it."
n "I took it and looked at it."
n "It looked like a food supplement."
vincent "It's all I really had-"
vincent "That's not dog food."
p "Do you have a dog?"
$ vbase,vblush,vexp = 3,0,6
vincent "...You could say that."
vincent "Sleep."
$ vbase,vblush,vexp = 3,0,2
vincent "It'll be better if you do."
n "Vincent got up and left me alone again."
$ health +=10
n "I drank the rest of the cold drink and sighed as I went back to bed."
scene black with fade
jump vincent_day_three


label farz_night2:
scene black
play music "vincent/farz_main.mp3"
farz "Hey wake up."
n "I could hear Farz's voice as I opened my eyes."
$ fbase, fexp= 3, 1
scene falloutshelter_dark:
    xalign 0.0
    easein 0.3
show farz
n "He kneeled down and looked at me."
p "Wh-what?"
farz "I have an idea."
n "Farz unlocked me and I rubbed my wrist."
farz "Let's go out."
menu:
    "\"No.\"":
        $ farz_love -=10
        farz "Come on."
        farz "I just wanna take a walk."
        n "I looked at my feet and back at Farz."
        farz "You can lean on me if you want."
        n "I stood up and leaned on Farz."
        n "I knew this was a bad idea, but could I really say no to him."
        n "He'd kill me faster than Vincent would."
    "\"Won't we get in trouble?\"":

        $ farz_love +=10
        farz "Don't worry!"
        farz "We won't get in trouble."
        p "Okay..."
        n "I couldn't help but feel worried."
    "\"Okay.\"":

        $ farz_love +=10
        farz "Haha awesome."
        n "I stood up and stumbled."
        farz "Whoa careful!"

n "We both looked at the door as the knob started to spin."
n "Farz looked at me and narrowed his eyes."
farz "Take the fall."
p "W-what!?"
n "What did he mean?"
n "I stumbled on the wall and leaned against it."
n "Vincent opened the door and looked at the two of us."
n "He grit his teeth."
$ vbase, vexp= 2, 1
show farz:
    subpixel True
    xalign 0.05
    alpha 0.0
    easeout 0.3 alpha 1.0
show vincent:
    subpixel True
    xalign 0.9
    alpha 0.0
    easeout 0.3 alpha 1.0
vincent "What are you little shits doing!?"
menu:
    "\"It was Farz's fault.\"":
        $ fexp = 2
        farz "Yeah right!"
        farz "They're the one that wanted to stretch their-"
        n "Vincent put a hand up immediately silencing Farz."
        n "He put one finger to his lips."
        vincent "Shh."
        vincent "Don't play the blame game."
        n "Vincent leaned his head to the side cracking his neck and bolted forward."
        n "He grabbed my neck and squeezed."
        $ vexp = 5
        vincent "I don't care who's fault it is."
        n "He squeezed harder, cutting off my air."
        n "I scratched at his arm and tried to pull away."
        vincent "But, if you wanna blame Farz for it..."
        n "Vincent's grip got tighter as he started grip my throat."
        n "I let out choked breaths and put my hand on his arm."
        n "I couldn't get out of his vice grip."
        vincent "...Darlin', I ain't gonna stand for that."
        n "I felt my neck snap under this hand."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/vincent_death.mp3"
        $ persistent.vincent_ending_snappedneck = True
        scene endslate with Dissolve(1.0)
        screen vincent_ending_snappedneck:
            text "{=endslate_title}You Died!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Vincent snapped your neck.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_snappedneck 
        with Dissolve(1.0)
        pause
        return
    "\"It's my fault.\"":

        $ farz_love +=10
        vincent "What the fuck?"
        $ vexp = 2
        vincent "What makes you think that you can just walk around like you own the place!?"
        n "Vincent started to advance on me."
        if farz_love >=60 and vincent_love >=90:
            farz "Wait."
            n "Farz slipped in front of me and put his hands on Vincent's collar."
            farz "Wait, Vincent."
            farz "I've been talking to them."
            $ fexp = 6
            farz "I think they'd be good to have around."
            farz "I mean... I did let them out."
            n "Vincent let out a low growl and looked at Farz."
            n "Farz ran his hands up Vincent's neck and to his face."
            $ fexp = 7
            farz "We could use the help."
            farz "Not everyone is going to trust a scarred up guy like you."
            $ vexp = 10
            n "Vincent closed his eye and listened."
            farz "We can hunt for you when you can't."
            n "Vincent put his hand over Farz's letting out a breath."
            vincent "Fine."
            n "Farz smiled and pushed his hand through Vincent's hair."
            $ vexp = 2
            vincent "They're under your watch though."
            vincent "I don't have long."
            $ fexp = 3
            farz "Oh. OH."
            farz "I'll get them out of your way."
            vincent "Yeah.."
            n "Vincent let out a gruff growl."
            vincent "Get the fuck out of here."
            vincent "NOW." with vpunch
            jump farz_day_three
        else:
            n "Vincent charged at me and pinned me on the wall."
            vincent "Get out Farz."
            n "Farz nodded and backed out of the room."
            $ fexp = 5
            n "I heard the door click behind him."
            hide farz with dissolve
            n "He just left me..."
            show vincent at center
            jump vincent_badend_pinata2
    "-Say nothing-":

        n "Vincent charged at me and pinned me on the wall."
        vincent "Get out,Farz."
        n "Farz nodded and backed out of the room."
        $ fexp = 5
        hide farz with dissolve
        show vincent at center
        n "I heard the door click behind him."
        n "He just left me..."
        jump vincent_badend_pinata2


label farz_hp_death:
n "I could feel myself getting tired and looking up."
n "I couldn't keep focus on the man in front of me."
n "I could feel Farz stepping on my back."
farz "Tsk you're so weak."
n "Everything went black."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/farz_death.mp3"
$ persistent.farz_ending_HP_Death = True
scene endslate with Dissolve(1.0)
screen farz_ending_HP_Death:
    text "{=endslate_title}You Died!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You couldn't stand up to him.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen farz_ending_HP_Death
with Dissolve(1.0)
pause
return


label vincent_day_three:
if vincent_love >=100 and sanity >=20:
    jump vincent_highlove
else:
    jump vincent_ending_checks

label vincent_highlove:
scene falloutshelter
play music "vincent/vincent_sad.mp3"
n "I heard the door open and I looked up."
show vincent
n "Vincent wandered into the bunker."
$ vbase,vblush,vexp = 3,0,14
n "Vincent looked frustrated and he kneeled down and unlocked me from my cuff."
p "What are you doing?"
vincent "Can't a guy unlock you without the 20 questions!?"
n "I flinched at his loud tone and he stiffened."
vincent "I can't control my anger when it's this close."
n "He paused, his eye shifting around, looking for the words."
n "Vincent bit back what he was going to say and didn't complete his thought."
p "What's close?"
n "Maybe if I asked myself he'd respond."
vincent "Full moon."
n "He let out a low animalistic growl as he sat down next to me with a soft thud."
n "Vincent looked at me and bit back his words again."
p "W-what's wrong?"
n "I tried to sound strong but my words came out in a stutter anyways."
$ vbase,vblush,vexp = 3,0,3
vincent "Fucking hell."
vincent "The 20 questions."
n "Vincent's aggressive tone didn't hide anything from me."
p "You look like a hurt animal, lashing out at people who are trying to help you."
n "Vincent sealed his lips tight."
n "He knew I was right."
vincent "Alright smart ass."
n "Vincent let out a heavy sigh."
vincent "I wanted to say sorry..."
n "His low angry tone turned soft and dark."
vincent "For this."
$ vbase,vblush,vexp = 3,0,14
n "Vincent motioned in my direction, his eye pausing at every cut."
n "Every part of me that was out of place."
n "Any part that was cut or bloody."
n "Or broken."
n "And in the end, he was the one that did this to me."
n "He was the one that put me here."
n "He hurt me."
menu:
    "-Forgive him.-":
        jump forgive_vincent
    "-Say nothing.-":
        jump dont_forgive_vincent

label forgive_vincent:
n "Maybe I was crazy but..."
p "It's okay."
p "I forgive you."
$ vbase,vblush,vexp = 3,0,1
n "He tucked his face in his arms."
vincent "...Oh..."
n "He sounded dejected."
$ vbase,vblush,vexp = 3,0,14
p "What were you expecting?"
$ vbase,vblush,vexp = 3,0,1
vincent "Shit, I dunno!"
vincent "Maybe YOU screamin' at me?"
vincent "Telling me to fuck myself."
vincent "'Fuck off Vince, you're the one who fuckin put me here.'"
n "Vincent tried to immitate my voice, he did a poor job of it."
n "I stiffled a laugh."
vincent "Laugh it up, pup."
vincent "You're not going to laugh very long."
vincent "Not after-"
$ vbase,vblush,vexp = 3,0,14
n "He stopped himself and bit his bottom lip."
n "Vincent put his head down on his arms."
p "You're dancing around the point."
n "I reached out and started to stroke his hair."
n "It looked like it would be rough."
n "His soft hair slipped through my fingers like silk."
n "I ran my hands through his hair, petting him lightly."
n "Hopefully he wouldn't be angry."
n "My hands weren't the cleanest things."
n "Vincent leaned into my touch letting off a low sound of pleasure."
n "I kept my hand on his head and I felt something growing under my hand."
p "Your ears!"
hide vincent with dissolve
show vincent
$ vbase,vblush,vexp = 4,0,14
vincent "What?"
n "He swatted my hand away and put his hand on the top of his head, feeling for himself."
vincent "Goddamn it!"
$ vbase,vblush,vexp = 4,0,2
p "I wanna touch them!"
$ vbase,vblush,vexp = 4,2,12
vincent "NO FUCK OFF!"

menu:
    "-Pet his ears anyways-":
        n "I reached out to pet his ears and it twitched to the side when my fingers touched it."
        n "I giggled softly."
        n "His warning went on deaf ears, but he didn't seem to mind as much as he lead on."
        vincent "I said fuck off.."
        n "His tail was moving side to side."
        p "It's cute."
        vincent "IT WON'T BE SO CUTE WHEN I'M-"
    "-Catch his tail-":

        n "I grabbed his tail and his ears and shoulders shot straight up."
        vincent "HEY CAREFUL."
        $ vbase,vblush,vexp = 4,2,2
        n "He curled his tail around himself and looked down."

p "What's wrong?"
vincent "There is a REASON why I brought you here."
n "I looked at my injuries."
p "I told you I don't care."
$ vbase,vblush,vexp = 4,0,14
p "So, what about it...?"
vincent "When I turn into a werewolf-"
n "I snorted, What was he talking about."
p "You're kidding right?"
n "Vincent looked at me deadpan."
n "He just pointed at his ears and I put up my hands."
p "Point taken."
vincent "I go after one person."
vincent "The first bastard I see, usually."
n "Vincent gripped his hands and looked at them."
vincent "But, I learned to lock myself down here so I don't go looking around anymore."
vincent "That's why you're here."
jump forgive_vincent_2

label dont_forgive_vincent:
n "I stayed quiet."
n "I was his prisoner after all."
n "He hurt me, that didn't mean I was going to forgive him right away."
vincent "Well, that's all."
n "I looked up at him."
n "Why am I down here?"
vincent "There is a REASON why I brought you here."
n "I looked at my injuries."
p "So, what about it?"
vincent "When I turn into a werewolf-"
n "What was he talking about?"
p "You're kidding right?"
$ temper +=10
$ vblush,vexp = 0,2
n "Vincent looked at me deadpan."
play music "vincent/vincent_changedmind.mp3"
vincent "I go after one person."
$ temper +=10
vincent "The first bastard I see, usually."
$ temper +=10
n "Vincent gripped his hands and looked at them."
vincent "But, I learned to lock myself down here so I don't go looking around anymore."
vincent "That's why you're here."
menu:
    "\"Why take someone down here?\"":
        $ vincent_love -= 30
        n "I spoke a bit scared."
        $ temper +=10
        n "Vincent's eye shifted towards me."
        vincent "You know, you're doing the world a favor."
        vincent "Sacrificing yourself for them."
        vincent "If I had my way-"
        $ temper +=10
        n "He stood up and leaned in."
        vincent "I'd kill those people too."
        n "He locked me on the radiator again and glared."
        vincent "See ya later."
        n "I watched him go and leaned my head down."
        n "He seemed... angry."
        scene black with fade
        jump vincent_ending_checks
    "\"Can't you let me go?\"":

        $ vincent_love -=50
        vincent "I was wrong about you."
        n "He stood up and growled angrily."
        vincent "You just wanna get out of here."
        vincent "And I don't blame you."
        n "His somber tone gone."
        $ vblush,vexp =0,2
        vincent "BUT, I can't let you outta here."
        vincent "And, fucking frankly, I suddenly don't give a fuck what you think of me."
        n "He opened his weapons locker and picked out a wooden bat slinging it over his shoulder."
        vincent "You wanna be let go so badly?"
        $ vblush,vexp = 0,5
        vincent "Well, darlin', I would LOVE to release you from your goddamn earthly bonds."
        n "I jumped up from my spot and tried to run."
        $ health -=10
        play sound "vincent/gunshot.mp3"
        pause (.5)
        n "A gun shot rang out in the bunker as I felt my knee give way."
        $ health -=10
        $ vblush,vexp = 0,2
        vincent "I don't feel like fucking chasing you."
        n "I screamed as I held the bullet wound."
        n "I felt the blood dripping between my fingers and he kicked me in the stomach to get me to turn over."
        n "He pushed the bat against my nose."
        vincent "You know how many people's skulls I've caved in with this baby?"
        n "He started to push harder and I whimpered trying to crawl away."
        vincent "HEY. You're not going anywhere."
        show CG_Vincent_with_bat with dissolve
        n "I could feel the wood smash into my nose with one swift movement, breaking the bone." with vpunch
        $ health -=10
        n "I let out a high pitched scream as the blood filled my senses."
        n "Blood dripped down my face as he pushed his boot into my sternum."
        n "I could feel the air pushing out of my lungs as I put my hands weakly on his boot."
        n "Vincent clentched his teeth and pulled the bat back, smashing my arm." with vpunch
        $ health -=10
        n "I let out a scream as the blunt force shattered my bone."
        n "The pain radiated up my arm and made me feel sick."
        vincent "I can't believe...you."
        $ vblush,vexp = 0,13
        n "He let out a frustrated growl."
        $ vblush,vexp = 0,2
        p "S-"
        vincent "What was that?"
        n "Vincent brought up the bat and smashed my teeth into my face."
        vincent "Who gave you FUCKING permission to talk?"
        n "I coughed."
        n "It was all bone... and blood."
        n "The world was spinning around me."
        n "But I wasn't dead."
        vincent "You're going to die."
        n "I heard him say as my ears rang."
        vincent "I went too easy on you."
        vincent "I FUCKING trusted you."
        vincent "What do I get in return."
        n "I felt his thumbs over my eyes as he pushed them into the sockets."
        n "I could feel my eyes bursting under the pressure of his hands."
        $ temper +=100
        $ health -=100
        scene black with fade
        vincent "Fuck you."
        n "I tried to scream."
        n "It was all blood."
        n "Just kill me."
        n "I felt something tear through me... like a dog."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        play music "vincent/vincent_death.mp3"
        $ persistent.vincent_ending_bat = True
        scene endslate with Dissolve(1.0)
        screen vincent_ending_bat:
            text "{=endslate_title}You Died!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Vincent beat you to death.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_bat 
        with Dissolve(1.0)
        pause
        return



label forgive_vincent_2:
menu:
    "\"Why take someone down here though?\"":
        p "Why can't you just lock yourself down here?"
        vincent "It's the bloodlust."
        vincent "If I don't get a fair amount then well..."
        vincent "Have you heard of the southside cabin massacre?"
        n "I rubbed my chin."
        p "I think I heard about that on the news."
        p "A few years back, they said a pack of wolves-"
        vincent "Murdered 16 people."
        vincent "That was me."
        $ vbase,vblush,vexp = 4,0,14
        p "WHAT!?"
        vincent "I went a year without killing someone."
        vincent "Well, on my full moon nights."
        n "I looked at him narrowing my eyes."
        vincent "Look."
        $ vbase,vblush,vexp = 4,0,12
        vincent "I'm not very good at self control."
        p "You can say that again."
        vincent "But!"
        vincent "It's what happens when I try to be 'conservative' with my murderin'."
        vincent "PEOPLE STILL NEED THEIR ASS BEAT ALRIGHT?"
        $ vbase,vblush,vexp = 4,0,1
        p "Are you trying to convince me or yourself?"
        n "He punched me in the arm and I rubbed it."
        p "Ow."
        $ vbase,vblush,vexp = 4,0,17
        vincent "Don't be a baby."
        vincent "I don't hit that hard."
        p "Yes you do."
    "\"Can't you let me go?\"":

        n "Vincent paused, thinking and looking down."
        n "He looked at his hands with a somber expression and shifted his gaze back to me."
        n "His ears receeded back, his tail gone."
        hide vincent with dissolve
        $ vbase,vblush,vexp = 3,0,14
        show vincent with dissolve
        vincent "You want to be let go that badly..?"
        n "Vincent got up and leaned over me."
        n "I nodded my head and he ran his hand through my hair."
        n "He pushed his hands against my throat and squeezed."
        vincent "It'll be over in a few seconds."
        n "I heard him say."
        n "I started to see stars as I put my hands on his arm."
        n "He wasn't killing me."
        n "I felt something warm hit my hand."
        $ vbase,vblush,vexp = 3,0,15
        n "I gripped his arm."
        p "V-vincent."
        vincent "...I love you."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        scene black with fade
        n "I passed out."
        n "It felt like an eternity of darkness."
        n "I just wanted to talk to Vincent again."
        n "It felt like a dream, watching the wolf in front of me."
        show CG_vincent_dream with dissolve
        n "He turned his back on me and started to walk away."
        show CG_vincent_dream1 with dissolve
        n "I wanted to stop him but."
        show CG_vincent_dream2 with dissolve
        p "DON'T GO."
        n "I screamed into the darkness."
        n "I woke up in a cold sweat and looked around."
        scene vincent_hospital with fade
        n "I was in less pain, all my wounds were covered."
        n "I was in a hospital room."
        n "There were nurses and doctors that roamed around me."
        n "The police asked what happened to me?"
        n "I told them I didn't remember."
        n "I did.. I remembered everything."
        n "They talked about the person who dropped me off."
        n "A tall man with a lot of scars."
        n "I told them he was a friend."
        n "A friend... I felt my tears well up around my eyes."
        n "I wanted to leave."
        n "It was a few days before they discharged me from the hospital."
        n "I was just on my way out when a nurse handed me an envelope."
        n "Her words came like a buzzing in my ears as she spoke."
        n "I shook as I opened the envelope."
        n "There was note inside, an attempt at good handwriting, simple words."
        n "I stared at the note as I clutched it in my hand."
        $ persistent.vincent_ending_letgo = True
        scene CG_vincent_note with Dissolve(1.0)
        pause
        return
    "\"You can't control yourself?\"":

        n "He shook his head."
        vincent "Nah, I wish I could."
        vincent "I'm feral when I'm in werewolf form."
        vincent "One of the perks."
        p "Sounds dangerous."
        vincent "You're damn right it is."

    "\"Who's Sano Kojima?\"" if persistent.character_unlock_sano == True:
        vincent "How do you know that name?"
        vincent "Tsk. I don't know who that is!"
        vincent "He just showed up one day and handed me this red patch."
        n "He seemed frustrated and backed up just a bit."
        n "He looked at the desk and then back to me."
        vincent "What do you know about him?"
        p "I just know he's a doctor, that's all."
        n "I said nervously shifting around."
        n "He sighed and rubbed the back of his head."
        vincent "So, no more than me huh?"
        n "He let out a sigh."
        vincent "Whatever, it doesn't bother me anymore anyways."


label vincent_sano_goodending:
n "Vincent sighed and leaned against the wall."
vincent "No one wants to hear me bitch about life."
vincent "It's shit and we all know it."
$ vbase,vblush,vexp = 4,0,14
n "He stood up and dusted off his jeans."
vincent "You're not going to be around much longer at any rate."
vincent "I'm sorry..."
n "He sounded upset."
n "Vincent turned towards the door."
n "I didn't want him to leave me alone in here."
menu:
    "-Catch him-":
        jump vincent_Catchhim_Goodending
    "\"You don't have to be alone.\"":
        jump vincent_comfort_goodending


label vincent_comfort_goodending:
vincent "I have to be alone."
n "Vincent said turning his back to me."
n "He pulled a black leather collar out of his pocket and gripped it hard."
vincent "I've made it pretty clear that I can't take care of anything."
vincent "Or anyone."
$ vbase,vblush,vexp = 4,0,2
n "He said throwing it into the wall, bounced off the wall with a hollow sound and hit the floor."
n "He stared blankly down at it."
vincent "Not even myself."
n "He said as he reached for the door."
n "I jumped up and grabbed his arm stopping him from opening the latch."
p "Stop."
p "Please... Stop."
$ vbase,vblush,vexp = 4,0,18
n "I begged as I grabbed his arm."
p "I don't want you to leave."
n "Vincent pulled his hand back as if he was going to backhand me but stopped."
n "I didn't flinch."
n "He reached down and put his hand on my cheek."
vincent "Don't look at me like that."
vincent "You're gonna make me-"
$ vbase,vblush,vexp = 4,0,18
p "Change your mind?"
p "It sounds like you already have."
n "He kneeled down in front of me and wrapped his arms around my waist."
n "He buried his face into my stomach and let out a soft sound."
$ vbase,vblush,vexp = 4,0,15
n "I put my hand on his head and ran my fingers through his hair."
vincent "Stop."
vincent "Stop being nice to me."
vincent "I don't deserve it."
menu:
    "-Be firm-":
        jump vincent_firm_powerbottom
    "-Be gentle-":

        n "I put my hands on his shoulders and pushed his arms open."
        p "You do."
        p "I'm not the one that's being broken here."
        n "I said leaning forward and hugging him hard."
        p "You're too hard on yourself."
        n "He wrapped his arms around me and squeezed, he held me tightly."
        n "But, there was a gentle hesitance in his embrace, making sure that he wouldn't squeeze too roughly."
        n "He held on."
        $ vbase,vblush,vexp = 4,0,14
        n "Like he'd never see me again."
        vincent "I'm always hard on myself."
        n "He muttered into my shoulder."
        n "He pulled back slightly and I leaned in."
        n "He met me halfway and kissed my lips."
        $ vbase,vblush,vexp = 4,0,11
        n "His hands were shaking and he pulled away."
        jump vincent_goodending


label vincent_firm_powerbottom:
p "Shut up."
$ vbase,vblush,vexp = 4,0,7
n "Vincent's eye shot open and he looked up at me."
n "I put my hands on his face and pushed him as hard as I could to get him to sit back."
$ vbase,vblush,vexp = 4,0,1
n "He did what I wanted and sat back looking up at me."
p "Shut up."
p "You don't get to decide what I'm feeling for me."
n "I said grinding down on him and placing my hands on his shoulders."
n "He let out a soft panting sound as he put his hands on my hips."
n "I moved my hips over his waist, feeling him getting hard underneath me."
vincent "What are you doing?"
n "He growled softly."
$ vbase,vblush,vexp = 4,2,1
p "You're wanted, you have NO say in it."
n "I said leaning into his soft ear."
p "...I want you."
p "I love you."
vincent "I love you to- AGH"
$ vbase,vblush,vexp = 4,2,10
n "I licked the ear tip and nibbled it."
n "Enjoying the sound of pleasure he made under me."
n "He bucked up against my hips and I could feel his erection through his pants."
p "I'm going to show you."
n "I said seeing that he was letting me do as I pleased."
n "I pulled his jeans open and slid down on top of his erection."
n "It felt different than the other times we were together."
n "This was on my terms."
n "I let out a loud moan as I felt his nails digging into my hips."
n "It wasn't deep enough to do any damage but they'd leave scars."
p "Yes... mark me up... Vincent."
n "I rocked my body on top of him."
n "Vincent moaned and growled underneath me, pushing hard up into me."
n "I could feel his mouth on my chest, sucking on my skin."
n "He bit down and licked my skin, leaving purple marks all over me."
n "I could feel myself getting closer to orgasming as he let out a loud growl underneath me."
vincent "...[player_name]..."
$ vbase,vblush,vexp = 4,2,11
n "I could feel myself tightening as he called out for me."
n "I felt a warm liquid fill me up as I slumped backwards."
vincent "Fine... you win."
n "He said with soft pants as he leaned over me and kissed me gently on the mouth."
p "Good."
jump vincent_goodending

label vincent_Catchhim_Goodending:
n "I sprung up out of my spot."
p "GOTCHA."
n "I tackled him as hard as I could." with vpunch
$ vbase,vblush,vexp = 4,2,7
n "He turned around."
n "Despite my best efforts to tackle him, he didn't budge."
$ vbase,vblush,vexp = 4,2,1
n "I backed up a smile creeping up on my face."
p "Catch me if you can."
n "His eye widened as I teetered away."
n "I looked stupid."
n "I couldn't run very well and I was in some pain."
n "What else could I do to keep him here?"
n "I could hear him thumping behind me and he tackled me back sending us both sailing into the floor."
vincent "You gotta be nuts."
vincent "I just told you I was a werewolf and you wanna play games with me."
n "Vincent rubbed his fingers against my lips."
n "I opened my mouth, licking the tips of his fingers."
n "They tasted like metal."
n "I bit down playfully on his skin."
n "He let out a low pleasured growl."
n "He pulled out his fingers and left them on my face, rubbing his thumb against my cheek."
p "I didn't want you to leave."
p "I-if I'm not gonna be here longer, then-"
p "I want you."
$ vbase,vblush,vexp = 4,2,7
n "Vincent leaned down and nuzzled my neck, sniffing my skin."
vincent "You're insane."
$ vbase,vblush,vexp = 4,2,16
n "Vincent kissed my neck."
n "I let out a small pleasured moan as I felt his tongue on my shoulder."
n "He bit down on me."
n "I was bleeding, but it was nothing."
n "I could take his little love bites."
n "I lifted my hips as he ran his rough hands down my back."
n "He pressed his lips against mine."
n "His kiss sent my body aflame."
n "It was hungry, like he was going to eat me."
n "I moaned into his lips."
n "I wrapped my arms around the back of his neck forcing him down."
n "I pushed my tongue into his mouth, fighting him for dominance."
n "Vincent didn't back down as he filled my mouth."
n "I rubbed against him, I could feel how hard he was under his pants."
p "Vin-vincent."
n "I moaned out finally breaking our kiss for some air."
n "His ears perked as he looked down at me."
show CG_Vincent_blushy with dissolve
p "Please."
n "He let out soft pants and shook his head."
vincent "You have stockholm or something."
p "Maybe."
p "But, fuck it."
n "Vincent laughed as he opened his pants."
$ vbase,vblush,vexp = 4,0,10
n "He rubbed his cock up against me."
n "I scratched his back as I felt him push himself inside of me."
n "He let out a low growl as he moved inside of me."
n "His thick cock working it's way deep inside."
n "This was different than before."
n "I didn't want him to stop."
n "He didn't speak, all he did was growl and moan."
n "He didn't need to speak."
n "The way he caressed my skin."
n "He kissed me."
n "His passion spoke for itself."
n "I let out a moan as rocked his hips in and out of me."
n "His low growls vibrated through my body."
n "I could feel him moving faster as I swung my legs around him."
vincent "F-fuck..."
scene falloutshelter
show vincent
n "I could feel him cum inside as I let him go."
n "I laid on the floor like a wet noodle, panting hard."
n "He leaned into me and kissed my lips."
jump vincent_goodending

label vincent_goodending:
$ vbase,vblush,vexp = 4,0,1
vincent "Fuck what time is it!?"
n "Vincent got up and held his head."
$ vbase,vblush,vexp = 4,0,7
vincent "Nonono FUCK."
n "Vincent growled and looked around quickly."
p "Vincent what's wrong!?"
$ vbase,vblush,vexp = 4,0,2
n "He put his hand on his weapons locker and punched in the code."
vincent "...Fuck..."
scene falloutshelter:
    xalign 0.5
    easeout 0.3 xalign 0.0
n "He growled as he pulled down the rack of guns."
n "They banged loudly on the floor and I looked up at him."
show vincent
p "Ah."
n "I started but he grabbed my throat."
vincent "SHUT UP."
n "He growled quickly and jammed me into the locker shutting it behind him."
n "I grabbed the grate and looked at him."
show CG_vincent_door with dissolve
p "What... are you doing.."
vincent "I...I'm saving you..."
n "He growled with his head down."
vincent "You're the only one..."
vincent "You're the only one worth saving..."
vincent "I love you."
n "I grabbed the fencing between me and him."
vincent "Back UP."
n "He banged on the doors."
menu:
    "-Reach out for him-":
        n "I reached out for him as he let out a growl."
        n "He scratched my arm and I took my hand back."
        p "OW."
        n "It wasn't too bad..."
        n "But... I was feeling a bit dizzy now."
        n "I sat down on the bottom of the locker as he paced around."
        n "He let out an ear splitting howl as I held on tight for the rest of the night."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        $ persistent.vincent_ending_good_ending = True
        scene endslate_clean with Dissolve(1.0)
        screen vincent_ending_good_ending:
            text "{=endslate_title}You survived!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Vincent saved you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_good_ending 
        with Dissolve(1.0)
        pause
        jump extra_goodending
    "-Back up-":
        n "I backed up like he told me to."
        p "Vincent..."
        n "He howled into the night his loud cry bouncing against the walls."
        n "I closed my eyes and waited for that night to be over...."
        hide screen health_bar
        hide screen sanity_bar
        hide screen vincent_rage_bar
        $ persistent.vincent_ending_good_ending = True
        scene endslate_clean with Dissolve(1.0)
        screen vincent_ending_good_ending:
            text "{=endslate_title}You survived!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Vincent saved you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_good_ending 
        with Dissolve(1.0)
        pause
        if persistent.farz_vincent_ending_good == True and persistent.vincent_ending_good_ending == True:
            hide screen vincent_ending_good_ending 
            jump sano_extra
        else:
            return


label extra_goodending:
hide screen vincent_ending_good_ending 
image Vincent_Happy_endslate = "vincent/CG_Vincent_Happy_endslate.jpg"
scene falloutshelter:
    xalign 0.0
with dissolve
play music "vincent/vincent_morningafter.mp3"
n "That one night felt like an eternity."
n "But, I heard the door of the locker open and stared at Vincent's naked body."
show vincent
$ vbase,vblush,vexp = 5,0,2
vincent "Are you okay?"
n "My mind snapped back to his face and I nodded quickly."
p "Yeah, I'm fine."
p "What about you?"
n "Vincent scoffed and went to the door."
vincent "I'm always a little tired after transformation..."
n "I looked at my hand and cradled it."
p "...You scratched me."
$ vbase,vblush,vexp = 5,0,7
n "Vincent held my hand gently."
vincent "...Ah.... I guess We'll be hunting together next full moon.."
$ vbase,vblush,vexp = 5,0,11
show CG_Vincent_Happy with dissolve
n "What did he mean by that?"
n "He opened the door to the bunker and sun flooded into the room."
vincent "I've never had a packmate before."
scene Vincent_Happy_endslate with Dissolve(1.0)
screen vincent_pack:
    text "Vincent turned you.\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_pack
with Dissolve(1.0)
pause
$ renpy.full_restart()

label farz_day_three:
$ vincent_love +=10
n "Farz started to back up slowly."
farz "Come on."
n "He grabbed my hand and ran off with me out of the bunker."
n "He slammed the door shut."
n "My feet were still in pain and throbbing."
n "But, we didn't stop running till we got back into the house."
n "I could hear a loud howl in the bunker."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
scene vincent_bedroom_night with fade
play music "vincent/vincent_sex.mp3"
$ fexp = 6
show farz
farz "Ah... he's gonna be pissy in the morning."
p "What? Why?"
farz "You were supposed to be like the sacrificial lamb."
farz "Kill one, save others or some shit."
farz "Sometimes he doesn't get a victim for the transformation."
farz "It makes him super pissy in the morning."
p "Sounds like fun."
$ fexp = 7
farz "It is, we just have to calm him down!"
farz "You'll like it I promise."
farz "Sit down."
n "He motioned at Vincent's bed."
n "I took a seat and he looked at my wounds."
farz "I'll fix this up."
menu:
    "\"Thank you\"":
        farz "I told him I'd watch you."
        farz "And I'm doing that."
        n "He quickly covered up my wounds and I felt much better already."
    "\"Why are you helping me?\"":

        farz "I thought it'd be fun to have someone else around."
        farz "You just happen to be what I was looking for."
    "\"What's going to happen tomorrow?\"":

        farz "He's probably gonna want to take his frustration out on us."
        n "I let out a small whimper and he slapped one of my wounds making me squeak."
        farz "It won't be bad, not as bad as it was for the last few days."

farz "Let's get some sleep."
farz "We're gonna need it."
n "We curled up on Vincent's bed."
n "And for once, I had a good nights sleep."
scene black with fade
n "The next morning my eyes fluttered open as I pulled the warm comforter around me."
scene vincent_bedroom_day
$ fexp= 5
show farz
farz "You look like shit."
p "Thanks."
$ fexp= 7
farz "I think I have something that might fit you."
n "Farz moved away and dug around in the closet."
n "He held out a pair of shorts, nylon stockings and a tank top."
n "All in black."
farz "Here."
p "Wh-what!? I- That's a little revealing don't you think?"
farz "You wanna make Vincent happy?"
farz "He got some kinks, some of them I bet would look better on you."
p "Okay."
n "I slipped the soft nylons over my legs and pushed the shorts around my waist."
n "I put on the tanktop and rubbed my arm."
p "How do I look?"
farz "You look great!"
n "He walked over to me and pushed me back down on Vincent's bed."
farz "Vincent's going to be coming back up soon."
farz "We should get ready."
n "Farz leaned over me and put his hands around my neck."
n "He slowly pushed his hands into my neck."
farz "You better get used to this, he likes choking people."
n "I felt his crotch against mine and I twisted my hips to rub up against him."
n "I nodded my head and put my hands gently on his arms."
n "Farz rubbed my neck as we grinded our hips together."
p "Ah~"
farz "Hah, I'm getting excited."
n "He rolled over and he pulled me on top of him."
farz "You try it."
farz "It's fun."
n "I nodded my head and pushed my hands around his neck."
n "The collar was in the way a bit, but I managed."
n "I pushed down and felt his breath in my hands."
n "The heart beat in his neck."
n "He looked excited but I didn't push any harder than that."
farz "You're not as strong as Vincent but... it's still fun right?"
farz "Sometimes you gotta get a piece of both worlds before you really appreciate one."
p "You're really smart."
farz "I'm not smart, just passionate."
n "I leaned into him and he wrapped his arms around me."
vincent "What are you two doing...?"
n "We turned our heads to the voice in the doorway."
$ fexp = 7
$ vbase, vexp = 5, 17
show farz:
    xpos 150
show vincent:
    xpos 300
farz "Vincent!"
n "He looked exhaused as he trudged his way into the room."
vincent "Cute outfit."
n "Vincent shoved me and Farz across the bed and sat down."
n "Farz crawled over sat down on his lap."
farz "Vincent, how are you feeling?"
vincent "Like I got hit by a garbage truck."
n "Farz motioned me over and made a motion at his shoulders."
n "I reached over and rubbed Vincent's shoulders."
n "He let out a low growl and he leaned back into my arms."
$ vbase, vexp = 5, 10
vincent "A guy can get used to this."
n "I reached out and held him in my arms as he put one hand on my forearm."
show CG_farz_vincent_kiss with dissolve
n "Farz leaned in and kissed him."
n "I watched on tilting my head to the side watching their passion."
$ vbase, vexp = 5, 11
n "Vincent's eye shifted to me."
show CG_Vincent_kiss with dissolve
vincent "What about you?"
vincent "I bet you want a collar too huh?"
vincent "I'll make you a nice one."
n "He put his free hand behind my head and I pressed my lips against his."
n "I put my hands on his chest as I felt Farz's hand reach down my shorts."
farz "We can make you feel better, sir."
n "Vincent's lips left mine, leaving me short of breath and wanting more."
p "Let us help you."
$ vbase, vblush, vexp = 5,1,6
vincent "Alright, you two wanna do this?"
vincent "Be my guest."
n "Vincent moved Farz off his lap and kneeled."
$ fexp = 8
n "Farz leaned his head against Vincent's leg and looked at Vincent's hard cock."
show CG_Farz_leaning_on_Vincents_leg with dissolve
n "Farz pushed it in his mouth, almost as if he was instructing me how to suck it."
$ vbase, vblush, vexp = 5,0,10
show CG_Farz_leaning_on_Vincents_leg:
    subpixel True
    yalign 0.5
    easeout 0.1 yalign 0.1
n "I watched at full attention, wanting to try it myself."
n "Farz looked over at me."
farz "Open up."
show CG_vincent_Farz_BJ with dissolve
n "He pulled my lips back forcing my mouth wide open."
n "Farz pushed my face down on Vincent's cock as hard as he could."
n "I gagged on his thick cock but Farz wouldn't let me pull back."
farz "Come on you can do it."
n "I looked up at Vincent as he let out a moan."
n "I felt myself getting more excited as Farz's hand moved into my shorts again."
n "Farz let my mouth go as he pulled my shorts off."
n "His fingers working their way inside of me."
vincent "Get them good and ready, Farz."
vincent "I need a good fuck."
farz "Yes sir!"
n "I could feel Farz's hand leave me for only a moment as wet lubricant moved across my ass and inside of me."
n "I let out a small moan as I felt the lube stick between me and my stockings."
n "Farz slipped off my shorts and pulled me off of Vincent."
n "He's been inside of me before."
n "But, some how this was different."
n "I was nervous."
n "I wanted him to feel good."
show CG_Vincent_Fuck with dissolve
n "Farz pulled out a knife and cut a hole in my stockings, exposing everything to Vincent."
n "I tried to move back and forth but Farz held me down."
n "The tip of Vincent's cock slipped easily inside of me."
n "I let out a loud moan and looked up at Farz."
farz "How does it feel?"
p "Ahh ahh...."
n "I couldn't speak, all I could do was make panting sounds at him."
n "I felt my head spinning as I watched the two kiss across me."
n "I nuzzled Farz's pants as he rubbed himself on my face."
p "F-Farz."
n "I unzipped his pants and his cock sprung out of his pants."
n "He rubbed his cock against my lips and he pushed it into my mouth."
n "I felt Vincent's hands around my throat and he pushed down."
n "I tensed up as he pushed."
vincent "Hah... Is that your cock I feel in there, Farz?"
n "I wasn't even sure that Farz was paying attention anymore."
n "I closed my eyes as both men pushed their way inside of me."
n "My head spinning with pleasure."
n "Vincent's strong hands on my neck."
n "I didn't want it to stop but I felt my body lock up."
n "I was cumming and I could feel warm liquid filling me up from both sides."
n "I coughed as Farz pulled his cock out of my mouth."
n "Vincent pulled out of me and laid back between the two of us."
n "I rested my head on Vincent's free shoulder looking at the two of them."
vincent "Welcome to the pack, [player_name]."
n "Farz curled up close and put his hand on top of my own."
n "Vincent pulled us both close to him and gave us a good squeeze before closing his eye to rest."
$ persistent.farz_vincent_ending_good = True
scene endslate_clean with Dissolve(1.0)
screen farz_vincent_ending_good:
    text "{=endslate_title}You Survived.{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You were accepted.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen farz_vincent_ending_good
with Dissolve(1.0)
pause
if persistent.farz_vincent_ending_good == True and persistent.vincent_ending_good_ending == True:
    hide screen farz_vincent_ending_good
    jump sano_extra
else:
    return


label vincent_ending_checks:
if sanity >=30:
    jump vincent_badend_pinata

if sanity <= 30:
    jump vincent_badend_vore

label vincent_badend_pinata:
scene falloutshelter
n "Vincent walked into the bunker and looked at me."
label vincent_badend_pinata2:
play music "vincent/vincent_angry.mp3"
vincent "...Alright. You piece of shit."
show vincent
$ vbase,vblush,vexp = 2,0,5
n "He grabbed his razor wire and started to lash it around me."
n "I let out a scream but he taped my mouth shut."
vincent "No. None of that."
vincent "All I need is your blood."
$ vbase,vblush,vexp = 2,0,13
n "He pulled the wire tight and I let out a muffled scream as the wire grinded into my flesh."
n "I could feel my tears running down my face."
n "He grabbed the meat hook on the ceiling and hooked it on the wire."
n "I could feel the wire getting pulled through my skin."
n "Vincent licked the blood dripping down my leg."
vincent "You look cute hanging up there."
n "Vincent said as he looked at me."
n "Vincent put his hands on his head and started to growl loudly."
$ sanity -=100
n "I wasn't sure what I was even looking at any more."
n "I let out a loud scream."
show CG_Vincent_Wolf_PINATA with dissolve
n "He let out a long howl."
$ health -=100
n "I could feel my blood dripping out of me as he tore through my belly with his claws."
n "All I could hear was his howls."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_pinata = True
scene endslate with Dissolve(1.0)
screen vincent_ending_pinata:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Vincent used you as a pinata.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_ending_pinata
with Dissolve(1.0)
pause
return

label vincent_badend_vore:
hide vincent
scene black with fade
scene falloutshelter_dark with fade
n "I bounced in anticipation."
n "I wanted Vincent to come in for the day...."
n "I needed him."
n "I felt the door open and I looked at it."
n "I felt so excited."
scene falloutshelter with dissolve
$ vbase,vblush,vexp = 4,0,2
show vincent
p "Vincent."
n "I practically moaned out his name as he came in."
n "He leaned over me and I looked at his ears."
vincent "What's your problem?"
n "Did I have a problem?"
n "I just wanted to play with Vincent."
n "He sniffed me and dug his claws into my arm."
n "I moaned out with pain and delight as he pushed his nails into my flesh."
p "A~AAH..."
n "Vincent started to pant as his tail moved back and forth."
n "It was so cute."
n "He reached down and bit my arm."
n "It felt like a delicate nibble at first."
n "I leaned back let him bite me."
n "I moaned out again and it made his ear perk."
$ vbase,vblush,vexp = 4,0,4
vincent "...I'm.... hungry."
n "He growled lightly as he started to bite harder."
n "I felt his teeth tear my flesh and I moaned out."
n "It didn't even hurt anymore."
n "I knew it was supposed to."
n "I laughed and laid back."
p "Eat.. me... Mr. Wolf."
n "I taunted playfully as he chewed my skin."
n "He looked more excited and blood thirsty."
n "He pushed his fingers into my stomach and I screeched."
n "I could feel the tears welling up on the corner of my eyes as he pushed his teeth into my soft innards."
n "I could feel his fingers ripping at my skin."
n "I let out a pleasured sound."
n "What was happening to me?"
n "Why did I like this so much?"
n "I let my eyes roll back into my head as I panted."
n "He was eating me. "
show CG_Vincent_Wolf_vore with dissolve
n "He was yanking out my guts and chewing on them like gum."
n "He let out a loud howl as he ripped through me."
n "Everything was going cold."
n "But, I couldn't stop giggling."
p "EAT ME ALIVE!"
n "Everything went black."
n "All I could hear was chewing."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_badvore = True
scene endslate with Dissolve(1.0)
screen vincent_ending_badvore:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Vincent ate you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_ending_badvore
with Dissolve(1.0)
pause
return


label vincent_healthdeath_alone:
hide screen countdown
n "My vision was getting blurry."
n "I looked down at my feet and saw nothing but blood."
p "...Ugh... shit."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_alone = True
scene endslate with Dissolve(1.0)
screen vincent_ending_alone:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You died alone.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_ending_alone
with Dissolve(1.0)
pause
return

label vincent_neglove_death:
n "Vincent looked to the side and tsked."
vincent "...You are a boring little shit aren't you?"
n "Vincent kneeled down and grabbed my legs."
n "He sniffed me deep and licked my skin."
p "Ahh.. "
n "I felt a chill up my spine as he ran his tongue up my stomach to my chest."
n "I arched my back into his touch."
$ vexp = 4
vincent "You like it when I do this to you?"
n "I felt every inch of myself tremble as he spoke into my chest."
n "I let out a breath but it was cut short."
n "Vincent thrusted a large knife into my chest and started to dig."
n "I coughed out blood and stared at him."
p "AHH!!!"
$ health -=30
n "I could feel him breaking my rib cage."
n "I let out a scream but I kept choking on the blood filling my lungs."
vincent "You really think I was going to keep you."
n "He grinned at me as he broke the rib out of my chest."
$ health -=30
n "I stared at him coughing."
show CG_vincent_Neglove_death with dissolve
n "I felt myself getting weaker as the blood poured out of me."
p "...St-stop..."
$ health -=30
n "Vincent ripped the bone from my chest and gnawed on it."
n "I could feel my vision blurring as Vincent ran his tongue on my rib."
vincent "Your meat tastes amazing."
n "I closed my eyes."
$ health -=30
vincent "I'll enjoy you for days."
n "I could hear him laughing in the darkness as I felt him cut into my stomach."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_neg_lovedeath = True
scene endslate with Dissolve(1.0)
screen vincent_neg_lovedeath:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Vincent didn't like you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_neg_lovedeath
with Dissolve(1.0)
pause
return

label vincent_health_death:
n "Vincent slapped my face."
n "I could feel myself getting more tired."
vincent "Hey what's your problem!?"
vincent "This isn't that bad!"
n "Vincent sighed as he stood up straight."
vincent "Well You couldn't take this much hm?"
n "Vincent put his foot on my chest forcing me down to the floor."
vincent "I'll make it quick.."
n "He lifted his boot and smashed it into my chest."
n "I let out a gasp as he stomped my ribs in."
n "I could hear my bones cracking but-"
n "I couldn't scream."
n "I was too tired."
vincent "Sorry, kiddo, We couldn't have more fun."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_healthdeath = True
scene endslate with Dissolve(1.0)
screen vincent_ending_healthdeath:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You were too tired.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_ending_healthdeath
with Dissolve(1.0)
pause
return

label vincent_temper_death:
n "Vincent dropped what he was doing."
$ vblush, vexp = 0 , 2
n "He grabbed my wrists and handcuffed them in a new set of handcuffs away from the radiator."
p "HEY... WHAT ARE-"
vincent "SHUT IT."
n "Vincent growled between his teeth as he looked up."
n "There was a meat hook on a chain hanging from the ceiling."
n "He yanked it down and hooked the handcuffs on to it."
n "He slapped my face as he walked past me to crank the hook back into the ceiling."
n "I could feel the handcuffs cutting into my wrists."
n "He started to pace back and forth with slow strides."
n "He slowly looked in my direction from time to time."
vincent "Fuck."
n "He walked back to his desk and picked up something from the desk."
n "He slipped something over his hands and walked over to me."
vincent "I need ... some of this aggression out."
n "Vincent flashed his brass knuckles at me and I gulped."
p "Wa-wait... Please."
n "I let out a soft sob as he shook his head."
vincent "NO WAITING."
n "He grabbed my sides and pulled me down quick and sharp."
n "I could feel my arms dislocating from the joint as he pulled."
$ health -=30
p "STOP..."
n "I cried out and thrashed."
$ health -=10
n "But, my movements were all in vain as I felt my joint dislocating."
n "Hot tears streamed down my face as I looked at him."
p "...N-..no I'm sorry..."
p "Please... let me down..."
n "He growled loudly."
n "He took a fighting stance that looked familiar but I didn't have time to think about it before he cracked his knuckles into my leg."
$ health -=10
n "I let out a loud scream that echoed off the walls of the bunker."
$ vexp = 5
vincent "That's right."
vincent "Fucking scream."
$ health -=10
n "He growled under his breath as he set another punch into my leg."
$ vexp = 4
vincent "I wonder if I can break your femur."
$ health -=10
n "He started to send repeating blows into my leg."
$ health -=10
n "I cried as the hard metal and his heavy punches made contact with me."
$ health -=10
n "He was too strong and in what felt like an eternity I could hear a loud snap."
$ vexp = 5
n "I let out a shrill shriek as my femur cracked leaving my leg a bloody mess."
$ health -=50
n "He grabbed my chin as he watched me sob."
vincent "I'm not done with you yet."
n "He scooted back a step as I looked up at him."
n "He rushed forward and smashed my ribs with his elbow."
$ health -=50
n "The pain was blinding, I didn't know how strong he was."
n "I gasped loudly and coughed."
n "I could feel my ribs cracking every time I took a breath."
n "Vincent put his fists up again and sent blow after blow into my torso."
n "I couldn't breath, I let out a scream but all that came out was blood."
show CG_vincent_temper_death with dissolve
n "Vincent looked at me and smirked, smashing his lips on mine, sucking out the blood and blowing in air."
vincent "Don't die on me yet."
vincent "I wanna savor your suffering."
n "Vincent licked my blood off his lips as I looked hazily at him."
n "I opened my mouth to speak but I only let out soft gasps."
n "My vision was getting blurry as he wiped the sweat off his forehead."
vincent "That was a good work out."
n "He grinned as my vision started to fade."
vincent "You're more useful as a punching bag."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "vincent/vincent_death.mp3"
$ persistent.vincent_ending_temperdeath = True
scene endslate with Dissolve(1.0)
screen vincent_ending_temperdeath:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Vincent used you as a punching bag.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen vincent_ending_temperdeath
with Dissolve(1.0)
pause
return


label cain_VS_Vincent_ending:
hide screen cain_feather
n "I closed my eyes."
n "What could I do?"
n "I needed someone..."
hide farz with dissolve
show vincent at center
p "Cain help me."
n "I clutched my hand tightly around a feather I was sure I didn't have before."
$ vexp =1
vincent "What did you say!?"
n "I heard Vincent's voice call out roughly to me."
n "I opened my eyes and looked up."
n "Large black wings."
$ cain_name = "Cain"
play music "cain/cain_shift.mp3"
$ cain_love = 100
$ cbase, cexp= 3,1
$ cain_hideheart = False
show vincent:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show cain:
    subpixel True
    xalign 0.9
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0
cain "Tsk tsk tsk."
cain "Always getting yourself into trouble hm?"
hide vincent with dissolve
n "Cain turned towards me, his glowing eyes locking onto mine."
show cain at center
n "He snapped his fingers and pointed at Farz in the room."
hide cain dissolve
scene falloutshelter:
    subpixel True
    xalign 0.0
    easeout 0.1 xalign 0.0
$ fbase, fexp = 1, 2
show farz
cain "Take care of that will you?"
farz "FUCK YOU."
n "The person called as I tackled him to the ground."
farz "GET OFF OF ME, BITCH."
n "He screamed as he punched me in the face."
n "I grabbed the knife from his other hand and plunged it into his chest."
hide farz with dissolve
scene falloutshelter:
    subpixel True
    xalign 0.0
    easeout 0.1 xalign 0.5
n "I let out a loud cry as I felt someone grab my hair and toss me at Cain."
n "I could feel Cain's hands on my torso, catching me midair."
show cain:
    xalign 0.9
n "It was quiet."
n "I could hear the other person coughing and Vincent's low voice."
n "He said something to them."
n "It was too soft, I couldn't hear it myself."
n "He held Farz close and I knew he was dead."
n "I killed Farz."
n "It was too quiet."
$ cbase, cexp= 3,9
cain "Get up beast, It's your turn."
n "Cain said his tone bored and flat."
$ temper +=100
n "Vincent got up and let out a loud cry."
n "Vincent's pain howl vibrated off the walls."
n "Cain seemed uninteresred in the display as Vincent turned on his heel."
n " He charged straight at me."
show vincent:
    xalign 0.1
$ vexp = 13
vincent "I'M GOING TO RIP YOUR GODDAMN HEAD OFF."
n "Cain pushed me aside and pulled out long silver sword."
cain "This will suffice for you."
n "Cain said as he pushed it into Vincent's chest."
show CG_vincent_VS_cain with dissolve
n "Vincent gnashed his teeth at Cain."
cain "Tsk."
n "Cain pushed the sword in further causing Vincent to cough blood."
n "He looked up at Cain."
cain "Haven't you learned-"
$ cbase, cexp= 3,8
n "Cain's words were cut short by Vincent spitting his own blood into Cain's open mouth."
n "Cain let the sword go."
scene falloutshelter:
    subpixel True
    xalign 0.5
show cain with dissolve
n "Vincent weak laughter filled the room as he stumbled backwards kneeling down near Farz's body again."
vincent "..S-say hi to my dad for me."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
n "Vincent laid down neck to the other body."
n "Cain touched the blood around his mouth and looked at it narrowing his eyes."
cain "...You can't stay out of trouble can you?"
n "Cain put his hand on my shoulder."
n "It felt like a torrent of darkness as I appeared back in my own apartment."
scene bedroom with fade
show cain with dissolve
p "Oh..Th-thank you."
$ cbase, cexp= 3,12
cain "No need for thanks."
n "Cain backed up."
n "I looked around nervously."
n "Something didn't feel right."
n "The walls were shifting inwards."
n "I put my hand on one of the walls."
$ cbase, cexp= 3,18
cain "You owe me now."
cain "Your soul will do."
n "He kicked my knees out from under me."
n "I scrambled desperately to get up but..."
scene black with fade
n "I could feel the ceiling above my head."
n "Everything was closing in and I kneeled down putting my forehead on the floor."
cain "Know your place."
n "Cain's words rumbled in my small box."
n "I couldn't move."
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
play music "cain/cain_death.mp3"
$ persistent.vincent_ending_death = True
$ persistent.cain_ending_vincent_saved = True
scene black with Dissolve(1.0)
screen cain_ending_vincent_saved:
    text "{=endslate_title}You survived!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain saved you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_vincent_saved 
with Dissolve(1.0)
pause
return





define cain = DynamicCharacter ("cain_name", 
    window_background="cain/dialoguebox_cain.png",
    show_side_image = ConditionSwitch(
    "cain_hideheart == True", "cain/love_icon_unknown.png",
    "cain_love >= 100", "love_icon_cain.png",
    "cain_love >= 90", "love_icon_red.png",
    "cain_love >= 80", "love_icon_pink.png",
    "cain_love >= 70", "love_icon_orangered.png",
    "cain_love >= 60", "love_icon_orange.png",
    "cain_love >= 50", "love_icon_yellow.png",
    "cain_love >= 40", "love_icon_green.png",
    "cain_love >= 30", "love_icon_cyan.png",
    "cain_love >= 20", "love_icon_blue.png",
    "cain_love >= 10", "love_icon_purple.png",
    "cain_love >= 0", "love_icon_black.png",
    "cain_love <= 0", "love_icon_black.png",
    )
    )
define sam = DynamicCharacter ("sam_name", window_background="cain/dialoguebox_sam.png" )
define d = DynamicCharacter ("aed_name", window_background="cain/dialoguebox_d.png" )
define damien = DynamicCharacter ("damien_name", window_background="cain/dialoguebox_damien.png" )




init:
    image CG_CainReading = "cain/CG_CainReading.png"
    image CG_CainReading2 = "cain/CG_CainReading2.png"
    image CG_cain_Bath_Tattoo = "cain/Bath_Tattoo_CG.jpg"
    image CG_cain_Bloody_tub = "cain/Bloody_tub_CG.jpg"
    image CG_cain_Bloody_Rose = "cain/Bloody_rose_CG.jpg"
    image CG_Cain_Fall = "cain/Cain_Fall_CG.jpg"
    image CG_cain_ORAL = "cain/CG_ORAL.jpg"
    image CG_CainPainting = "cain/CG_CainPainting.png"
    image CG_Cain_Gutrip = "cain/CG_Cain_Gutrip.png"
    image CG_Cain_Leash = "cain/CG_Cain_Leash.jpg"
    image CG_Cain_kitchenknife = "cain/CG_Cain_kitchenknife.jpg"
    image CG_Cain_meatonfork = "cain/CG_Cain_meatonfork.jpg"
    image CG_Cain_meatonfork_meat = "cain/CG_Cain_meatonfork_meat.jpg"
    image CG_cain_sanity_ending = "cain/CG_cain_sanity_ending.jpg"
    image CG_cain_sanity_ending_move = "cain/CG_cain_sanity_ending_move.jpg"
    image CG_Damien_removedArm = "cain/CG_Damien_removedArm.jpg"
    image CG_Cain_goodEnding = "cain/CG_Cain_goodEnding.jpg"
    image CG_FallenAngel_Cain = "cain/CG_FallenAngel_Cain.png"
    image CG_sam_ending = "cain/CG_sam_ending.jpg"
    image CG_damien_saves_MC = "cain/CG_damien_saves_MC.jpg"
    image CG_Damien_Priest_Fallen = "cain/CG_Damien_Priest_Fallen.jpg"
    image CG_damien_double_vision = "cain/CG_damien_double_vision.jpg"
    image CG_damien_Sex = "cain/CG_damien_Sex.jpg"

image cafe = "cain/cafe.jpg"
image cafe_pulse:
    "cain/cafe.jpg" with dissolve
    pause 0.5
    "cain/cafe_pulse.jpg" with dissolve
    pause 0.5
    repeat

image cain switch:
    "cain/glitchattempt1.png"
    pause 0.15
    "cain/glitchattempt2.png"
    pause 0.15
    "cain/glitchattempt3.png"
    pause 0.15
    "cain/glitchattempt4.png"
    pause 0.15
    repeat
image feather_animation:
    "cain/feather_animation1.png"
    pause 0.09
    "cain/feather_animation2.png"
    pause 0.1
    "cain/feather_animation3.png"
    pause 0.09
    "cain/cain_expression_0.png"

image cain_livingroom = "cain/livingroom.png"
image cain_livingroom_morning = "cain/livingroom_morning.png"
image cain_livingroom_night = "cain/livingroom_night.png"
image cain_bedroom_morning = "cain/bedroom_morning.png"
image cain_bedroom_morning_phone = "cain/bedroom_morning_phone.png"
image cain_bedroom_night = "cain/bedroom_night.png"
image cain_balcony = "cain/balcony.png"
image cain_bathroom = "cain/cainbathroom_day.png"
image cain_bathroom_night = "cain/cainbathroom_night.png"
image sam_bedroom = "cain/Bedroom_Sam.png"
image damien_church = "cain/church_day.png"
image damien_church_night = "cain/church_night.png"



image feather normal = "cain/feather.png"
image CG_CainReading2_glow = "cain/CG_CainReading2_glow.png"
image sam_ice1 = "cain/ice1.png"
image sam_ice2 = "cain/ice2.png"
image sam_ice3 = "cain/ice3.png"
image sam_ice4 = "cain/ice4.png"
image sam_ice1_anim:
    "sam_ice1"
    ypos 1200 xpos -200
    ease 0.05 ypos 600 xpos 100
image sam_ice2_anim:
    "sam_ice2"
    ypos 1200 xpos -200
    ease 0.07 ypos 600 xpos 250
image sam_ice3_anim:
    "sam_ice3"
    ypos 1200 xpos 300
    ease 0.07 ypos 600 xpos 500
image sam_ice4_anim:
    "sam_ice4"
    ypos 1200 xpos 300
    ease 0.05 ypos 600 xpos 650

image cain fake = LiveComposite(
    (407, 600),
    (0, 0), "cain/fake_cain_base.png",
    (0, 0), "cain/fake_cain_smile.png")
image cain fake_grin = LiveComposite(
    (407, 600),
    (0, 0), "cain/fake_cain_base.png",
    (0, 0), "cain/fake_cain_grin.png")
image cain fake_smirk = LiveComposite(
    (407, 600),
    (0, 0), "cain/fake_cain_base.png",
    (0, 0), "cain/fake_cain_smirk.png")
image cain fake_frown = LiveComposite(
    (407, 600),
    (0, 0), "cain/fake_cain_base.png",
    (0, 0), "cain/fake_cain_frown.png")
image cain fake_eyeroll = LiveComposite(
    (407, 600),
    (0, 0), "cain/fake_cain_base.png",
    (0, 0), "cain/fake_cain_eyeroll.png")
image tail = "cain/cain_tail_1.png"
image wings cain = "cain/cain_wings_1.png"
init python:

    cwings,cbase, cexp = 1,1,1

    def draw_cain(st, at): 
        return LiveComposite(
            (450, 600), 
            (0, 0), "cain/cain_base_%d.png"%cbase,
            (0, 0), "cain/cain_expression_%d.png"%cexp,
            ),.1   
init:
    image cain = DynamicDisplayable(draw_cain)

init python:

    sbase,sexp, sglass = 1,1,1

    def draw_sam(st, at): 
        return LiveComposite(
            (448, 600), 
            (0, 0), "cain/sam_base_%d.png"%sbase,
            (0, 0), "cain/sam_expression_%d.png"%sexp,
            (0, 0), "cain/sam_glasses_%d.png"%sglass,
            ),.1   
init:
    image sam = DynamicDisplayable(draw_sam)

init python:

    dbase,dblush, dexp = 0,0,0

    def draw_damien(st, at): 
        return LiveComposite(
            (448, 600), 
            (0, 0), "cain/damien_base_%d.png"%dbase,
            (0, 0), "cain/damien_blush_%d.png"%dblush,
            (0, 0), "cain/damien_expression_%d.png"%dexp,
            ),.1   
init:
    image damien = DynamicDisplayable(draw_damien)

image d 1 = "cain/d_sprite_1.png"
image d 2 = "cain/d_sprite_2.png"
image d 3 = "cain/d_sprite_3.png"
image d 4 = "cain/d_sprite_4.png"
image d 5 = "cain/d_sprite_5.png"
image izm = "cain/izm.png"

label cain_start:
show screen health_bar
show screen sanity_bar
$ cain_boredom = 0
$ cain_hideheart = True
$ cain_name = "???"
$ dbase,dblush, dexp = 0,0,0
$ cwings,cbase, cexp = 1,1,1
$ lookaround_punishment1 = False
$ damien_call_1 = False
$ damien_day2_call = False
$ cain_noon_bathroom = False
$ cain_bedroom_day1 = False
scene bedroom
n "Maybe a cafe would be nice tonight."
n "I left my apartment and headed to the cafe."
scene cafe with fade
play music "cain/cain_intro.mp3"
n " It was actually pretty quiet."
n "The sound of a piano slowly began to cut through the silence like tissue and I was soon completely mesmerized by the bewitching music."
n " I don't even really remember entering the cafe I was so enthralled."
cain "Moonlight Sonata."
n " A suave voice broke me from my stupor."
n "I had suddenly found myself standing next to the source of the alluring music."
show cain fake
$ persistent.character_unlock_cain = True
cain "Enjoying the music?"
n "I stared at him for a moment before responding."
p "Oh! Yes. It's very lovely."
n " He looked up from the keys, his hands continuing their melodious work."
cain "Please, have a seat."
n "He nodded to a nearby chair before returning his attention to the ivories."
n "I took my seat and quietly watched him play."
n "His long fingers danced elegantly across the keys and I couldn't help but be hypnotized all over again."
n "I stared at the side of his face and watched him for a moment."
n "I...I wanted to know more about him."
cain "Is there something on my face?"
n "His joking comment brought me back to reality."
n "Again.. I looked up at him and shook my head."
p "Uh, no."
p "Just amazed by your playing."
n "He chuckled and gave me a side glance."
cain "Now, I know that you didn't come all the way here just to listen to me play."
n "He took his hands off the keys and turned to face me, finally giving me his full attention."
cain "So then, sweetheart, what can I do for you?"
menu:
    "\"Oh, right. I guess a coffee sounds good right about now.\"":
        show cain fake_eyeroll
        $ cain_boredom += 1
        cain "Well, I suppose that IS why most people come to a cafe."
        show cain fake
        n "He teased and stood up."
    "\"Maybe I did just come here for the music. Is that a crime?\"":

        $ cain_love +=10
        n " He laughed at me and crossed his arms."
        cain "As far as I know it's not, but I think you might have to reevaluate your priorities, sugar."
        n "He stood up."
    "\"Maybe I just wanted to find some interesting people to talk to.\"":

        show cain fake_frown
        $ cain_love -=10
        cain "Oh? And do I fit that \"interesting person\" criteria?"
        show cain fake_grin
        n " I couldn't come up with a response."
        n "I only blushed harder."
        n "He then got up from his bench and motioned for me to follow him."
        cain "Come with me."

p "What about the piano?"
n "I asked, pointing at the beautiful instrument."
show cain fake
cain "Don't worry."
cain "It's not going anywhere."
n " He held out his hand and helped me out of my seat."
n "We walked over to the barista's counter together and ordered some coffee."
n "I watched him as he spoke to the woman working behind the counter."
n "I kept my eyes on him."
n "I was finding it exceedingly difficult to look anywhere else."
cain "So what's your name, love?"
n "He asked, his attention now back on me."
n "I snapped back to reality before managing to choke out my name."
p "It's %(player_name)s."
if player_name == "Ashe":
    show cain fake_smirk
    cain "Interesting name."
    show cain fake
show cain fake_grin
n "He brought me over to the table."
n "He pushed a fancy looking coffee with ice cream towards me."
cain "A pleasure to meet you."
$ cain_name = "Cain"
cain "My name is Cain. "
n "Cain picked up a spoon and offered it to me."
cain "Here, give this a try."
cain "This place serves the best affogato that you will ever taste."
show cain fake
menu:
    "\"I don't really like ice cream.\"":
        $ cain_love +=10
        cain "Ah. That's too bad."
        cain "I suppose I should have asked you what you liked first."
        n "Cain chuckled before digging into the dessert himself and pushing his black coffee over to me."
        cain "Maybe you should try this instead."
        cain "The coffee here is still very good."
        n "He dipped his spoon into the bowl and continued to eat the affogato."
        n "I looked down at the steaming dark coffee and took a sip."
        n "Despite the inky color the flavor was rich and flavorful."
        n "He was right."
        n "It WAS very good."
    "-Take the spoon-":

        show cain fake_eyeroll
        $ cain_boredom += 1
        n "I smiled and tried a spoonful."
        show cain fake
        n "It tasted great!"
        n "So great in fact I let the spoon linger in my mouth a bit."
        n "Cain took a sip of coffee from his mug."
        cain "So, how does it taste?"
        n "I could feel my face heating up."
        p "It's really good."
        show cain fake_grin
        n "Cain reached out and patted my free hand."
        n "His hands were warm and my face felt much hotter than it did earlier."
        cain "Glad to hear it."
        show cain fake
        n "He released my hand and returned to his coffee."
    "\"You first?\"":

        show cain fake_frown
        $ cain_love -=10
        cain "Alright. As long as you don't mind having some of my germs with your dessert."
        show cain fake
        n "Cain laughed, picked up the spoon, and took a bite."
        n "He dipped it back in and then held out the spoon for me."
        cain "Open."
        n "I opened my mouth for him and took a bite."
        n "It was so delicious I ended up taking the spoon from him and licked the cream off of it."
        p "It's absolutely delicious."
        show cain fake_grin
        cain "I'm glad you enjoyed it."
        show cain fake

n "Cain looked at the clock hanging above the barista's counter."
cain "Oh my. Is it that time already?"
n "He looked at me and leaned his head to the side."
cain "I suppose time really does fly when you're having fun."
n "He stood up, took my hand in his, and gave it a kiss."
cain "Have a lovely rest of the night, my dear."
cain "Unfortunately I have to go, but I do hope that we meet again."
n "He started making his way towards the exit."

menu:
    "\"Wait!\"":
        show cain fake_eyeroll
        $ cain_boredom += 1
        cain "Yes?"
        show cain fake
        n "I felt my toes curl in my shoes, apprehensive on what to say next. "
        p "N-never mind."
        p "You have a good night too!"
        n "Cain walked over and leaned his face in close to mine."
        cain "...If there is something that you desire, you must ask for it."
        cain "Indecisiveness can be one costly oversight."
        show cain fake_smirk
        cain "If you are too frightened to grab hold of your wishes then you will never have them."
        n "Cain spoke softly and walked away."
        n "I wasn't sure what to say."
        hide cain with dissolve
        n "By the time I was able to think up a retort he had already disappeared."
        n "What...what was that all about?"
    "\"Have a good night!\"":

        $ cain_love +=10
        p "You know, it's kind of funny."
        p "You didn't strike me as the type to have a bedtime."
        n "I teased. He responded with a jovial laugh."
        cain "Well, I'm not as young as I used to be."
        cain "I need to get my beauty sleep."
        n "He pushed his fingers through his hair."
        p "You look fairly young."
        p "How old are you exactly, Cain?"
        show cain fake_smirk
        n "Cain chuckled a little and raised his eyebrows in what seemed like amusement."
        cain "Have a good night, my dear."
        cain "Maybe we'll meet again someday."
        hide cain with dissolve
        n "He waved at me before finally walking out the door."
        n "Yeah...maybe."
    "\"I should probably get going too then.\"":

        show cain fake_frown
        $ cain_boredom += 1
        $ cain_love -=10
        p "It {i}is{/i} getting pretty late."
        show cain fake
        cain "Yes, that's a good idea."
        cain "You don't want stay out too late."
        n "Cain put a hand gently on my shoulder."
        show cain fake_smirk
        n "Something about his tone made me feel a little...uneasy."
        n "It almost felt like {i}he{/i} was threatening me."
        cain "I could walk you home if you like."
        n "He asked, his hand still resting on my shoulder."
        p "N-no thanks."
        p "I think I should be okay by myself."
        n "I said trying to sound polite as possible."
        cain "Well alright then, if you're sure."
        show cain fake_grin
        n "He then took his hand off my shoulder and began making his way toward the door."
        cain "Have a wonderful evening, love."
        n "He looked back at me before leaving."
        cain "And have a safe trip home."
        hide cain with dissolve


n "I noticed a large black feather sitting on the table."
show feather normal
n "I picked it up and examined it."
p "How did this get here?"
n "Something about it was strange."
n "It didn't look like a normal bird feather."
n "It was much larger and thicker than any feather that I've ever seen."
p "What the hell is-"
stop music
play music "cain/heartbeat.mp3"
show cafe_pulse
show feather normal
n "My heart inexplicably started pounding."
n " I dropped the feather back on the table, but the thumping didn't stop."
hide feather normal with dissolve
n "I got up from my seat and rushed out of the cafe."
n "Maybe...maybe I can just walk it off."
n "The pulsing in my chest only grew more severe as I tried to walk home."
n " My heart was beating so loud in my ears that I couldn't even think straight."
scene bg_outside_pub:
    xalign .9
n "It felt like my heart was going to explode."
n "Despite this mysterious affliction I ran home."
n "I ran until my muscles burned and the acid in my stomach crawled up my throat."
n "I put my hand over my mouth as the urge to vomit began to creep in."
n "Almost--almost there!"
n "I pulled the keys out of my pocket and hastily searched through them as I approached my door. "
scene bedroom with dissolve
n "I leaned myself against my door and wiped the sweat from my forehead."
n "I was exhausted from the whole thing."
n "What was happening to me?"
n "Why was I feeling this way?"
n "I could feel tears streaming down my face."
n "I was scared."
n "I shoved my face into one of my pillows and cried into it."
n "I needed help, but I didn't know what to do."
n "I was so tired."
scene black with fade
n "My eyelids fluttered before closing, finally losing the last shred of energy that I had."
play music "cain/cain_calm.mp3"
n "I felt a gentle warmth touch my face."
n "The sun."
n "I groaned as I flipped over in my sheets, feeling how soft they were under my hands."
n "They smelled nice too."
n "Wait... My window didn't catch the sun in the morning."
n "Only during sunset."
n "I sat up quickly and looked around."
scene cain_bedroom_morning with dissolve
n "This wasn't my room."
n "Where was I?"
n "I noticed a note on the night stand next to the bed."
n "I nervously reached for it."
n "'Meet me in the living room.'"
n "Living room?"
n "I looked at the other side of the card."
n "Nothing else was written."
n " I got out of bed and looked at my body."
n "When did I take my clothes off?"
n "I was only in my underwear."
n "I left the strange room, clutching the note close to me. "
show cain_livingroom with fade
n "I wandered into the living room, my eyes scanned the large expensive looking apartment until they found a man standing in front of a window that led out to a balcony."
p "...Cain?"
n "My voice escaped my lips."
n "He turned around to face me and that horrible feeling that I got from the feather started to come back."
play music "cain/cain_shift.mp3"
show cain fake_smirk
cain "Oh, you're awake."
cain "How was your sleep?"
n "I didn't answer."
n "I wasn't in the mood for his jokes."
cain "That well, huh?"
n "His sweet gentle voice from last night turned cruel and sadistic."
p "What's happening?"
p "How did I get here?"
n "My voice was trembling."
n "Even through my anger I couldn't mask the fear and uneasiness I was feeling."
n "Cain laughed diabolically at me. "
show cain switch
$ sanity -=10
if sanity <= 0:
    jump cain_sanity_ending
n "Then, I noticed something...odd happening to Cain."
n "I wasn't sure if what I was seeing was real or just a hallucination."
n "His body was starting to change."
n "His form shifted into someone else entirely."
$ cwings,cbase, cexp = 0,3,1
show cain with dissolve
n "He ran a hand through his red hair and stared at me."
cain "Why, I brought you here of course."
n "I have to get out of here."
n "I took a step back and started inching out of the room before breaking into a run."
n "I didn't get very far, as my body collided with some sort of invisible barrier." with vpunch
n "Hard."
$ cbase, cexp = 3,5
n "Cain sighed as he watched me crumple to the floor."
cain "Tsk, tsk."
$ cbase, cexp = 3,1
n "I rolled around to face him."
n "His bright yellow eyes pierced through me as some phantom hand grabbed my neck and dragged me across the floor."
n "I struggled to breath as the ghostly claw tightened its grip on my throat."
n "I frantically grabbed at my neck, trying to get whatever was choking me to stop."
n "All I could do was writhe and squirm helplessly on the floor."
cain "Don't waste your energy, my pet."
cain "A lowly creature like you has no hope of escaping."
cain "Just accept your fate as my new toy and make this easy on yourself."
n "Cain's hand replaced the unseen one as he picked me up from the ground by my neck."
n "He held me up and stared at me."
n "Jet black wings extended from his back."
show wings cain behind cain with dissolve
$ cwings,cbase, cexp = 1,3,1
n "What was he?"
cain "Alright, I'll tell you."
cain "I'm going to flay your skin, crack your bones, play with your organs, and maybe even drink your blood."
cain "I'll be doing whatever I damn well please."
n "He released my throat and I dropped to the floor."
cain "You will beg for death, and you WILL get it."
cain "Once I've had my fill of you."
cain "But until that time comes you will be living on your knees!"
n "I could feel the same invisible force pinning my entire body to the floor."
n "It felt like a giant rock was slowly crushing me."
n "He didn't even need to lay a finger on me."
n "He...he was a monster."
n "Cain watched me as I fought in vain to pick myself up."
n "He then stomped and grinded the heel of his shoe into the side of my head."
cain "That being said, I'm interested in seeing how long you'll last."
n "Cain removed his foot and turned away."
$ cwings,cbase, cexp = 0,3,1
n "His wings receded into his back as the unseen pressure faded."
hide wings cain with dissolve
show cain
menu:
    "\"Why are you doing this?\"":
        $ cwings,cbase, cexp = 0,3,1
        $ cain_love -=10
        if player_name == "Ashe":
            $ cwings,cbase, cexp = 0,3,2
            cain "...You're not human right?"
            n "I bit my lip and shook my head."
            cain "...That's what I thought."
            cain "I can sniff out your kind from a mile away."
            cain "You just answered your own question, reaper."
            cain "I'll make sure you suffer slow."
        else:
            n "Cain turned back around to face me."
            cain "Why?"
            cain "Because I can, my new precious toy."
            $ cwings,cbase, cexp = 0,3,1
            cain "That's the only reason I need."
            cain "When you have power like mine you can take whatever you want."
            cain "No being on Earth can hope to stand up to me."
            $ sanity -=10
            if sanity <= 0:
                jump cain_sanity_ending
            cain "The taste that you got was barely an iota of what I'm capable of."
    "-Stay quiet.-":

        $ cwings,cbase, cexp = 0,3,5
        $ cain_boredom += 1
        if cain_boredom >=3:
            jump cain_boredom_day1
        else:
            n "I bit my bottom lip."
            $ cwings,cbase, cexp = 0,3,4
            n "What could I say in a situation like this?"
            n "I was going to be this person's...\"plaything\" until got he bored and decided to off me."
            n "I really don't want to know what evil plans that he has for me."
    "\"Why me?\"":

        $ cain_love +=10
        cain "Why you indeed."
        n "Cain leaned against the window."
        cain "You humans are a dime a dozen."
        cain "None of you are as unique as all of you like to believe, but you.....hmm."
        n "He crossed his arms and looked up at the ceiling."
        n "It seemed like he wasn't entirely sure himself."
        if player_name == "Ashe":
            $ cwings,cbase, cexp = 0,3,2
            cain "...You're not human are you?"
            n "I bit my lip and shook my head."
            cain "...That's what I thought."
            cain "I can sniff out your kind from a mile away."
        else:
            cain "Let's just say that you happen to fit my \"interesting person\" criteria."
            n "He shifted his gaze over to me."
            cain "Honestly, you should feel honored that I chose you to be my little puppet.."
            cain "It's a privilege that not too many get to enjoy."

n "I tried to stand up slowly, my legs were wobbling as I did."
n "But, I managed."
$ cwings,cbase, cexp = 0,3,1
cain "Keep me interested in you, love."
n "He went to sit down."
hide cain



menu:
    "-Talk to Cain-":
        jump talk_cain_1
    "-Look around-":
        $ lookaround_punishment1 = False
        jump look_around_morning

label talk_cain_1:
show cain
$ cwings,cbase, cexp = 0,3,4
n "Cain looked over his shoulder at me."
cain "What is it, meat?"
n "His tone suddenly rude and uncouth."
$ cwings,cbase, cexp = 0,3,1
menu:
    "\"So...what now?\"":
        $ cain_love +=10
        p "Should I try to run away?"
        p "Give you the thrill of the chase?"
        $ cwings,cbase, cexp = 0,3,11
        cain "You tried that just a second ago and how did that turn out for you?"
        $ cwings,cbase, cexp = 0,3,1
        n "Lacking any retorts and now slightly embarrassed I looked at the floor."
        n " Cain walked over, backed me into the wall, and leaned in close."
        if player_name == "Ashe":
            $ cwings,cbase, cexp = 0,3,4
            cain "You think you can escape me, reaper?"
            cain "There's no chance."
            cain "You can try to run... But I'll find you."
        else:
            cain "Besides, you have nowhere to run to."
        cain "So just sit down, shut your mouth, look pretty, and do as I say."
        n "He grabbed me by the face and forced me to meet his gaze."
        cain "And you better watch that attitude of yours, pet."
        cain "You forget where you are. Know your place!"
        n "My head was thrown against the wall behind me." with vpunch
        $ health -=5
        n "I rubbed the back of my head, feeling sorry that I said anything."
        jump cain_day1_noon
    "\"Is this the part where I get tied up?\"":

        $ cwings,cbase, cexp = 0,3,5
        $ cain_boredom += 1
        if cain_boredom >=3:
            jump cain_boredom_day1
        p "Restrain me so I can't try to escape?"
        cain "Oh there will be some tying up later, if I'm in the mood for it."
        cain "But it's not going to be what you think it's for."
        n "His eyes shifted to the door for a moment and then back to me."
        $ cwings,cbase, cexp = 0,3,4
        cain "Listen sweetheart, even if you somehow managed out of here, you most certainly die out there."
        p "What do you mean?"
        n "I asked, unclear as to what he meant by that."
        cain "You're in MY domain."
        $ cwings,cbase, cexp = 0,3,9
        cain "There is no way a human like you could survive out there."
        $ cwings,cbase, cexp = 0,3,18
        cain "Lots of nasty creatures outside would love to get their claws on a tasty little morsel like you."
        $ sanity -=10
        n "He said pointing to the door."
        $ cwings,cbase, cexp = 0,3,12
        cain "So if you want to go take your chances out there be my guest, but if you ask me, it's MUCH nicer in here."
        n "Cain raised his arms in approval of his abode."
        p "So I'm dead either way great."
        n "I held my face in my hands, I felt so utterly defeated."
        n "He then walked over and got in close to my ear."
        $ cwings,cbase, cexp = 0,3,9
        cain "That's about the size of it yes."
        jump cain_day1_noon
    "\"Where are we?\"":

        $ cain_love -=10
        $ cwings,cbase, cexp = 0,3,7
        cain "My house of course."
        $ cwings,cbase, cexp = 0,3,9
        cain "You're free to move around as you like."
        cain "I'll get you when I need you."
        n "I looked around the room again and then back at him."
        p "You're...you're going to let me roam free?"
        p "Why?"
        n "He sighed and rubbed his temples."
        $ cwings,cbase, cexp = 0,3,5
        cain "Because this is my domain."
        cain "There isn't a place you can go that I won't be able to find you."
        $ cwings,cbase, cexp = 0,3,9
        cain "I'm also a lot faster than you might think."
        $ sanity -=10
        if sanity <= 0:
            jump cain_sanity_ending
        n "He patted my face hard and walked past me."
        cain "So keep that in mind."
        jump cain_day1_noon


label look_around_morning:
n "I wasn't really in the mood to speak with Cain."
n "I looked around the room."
n "Everything looked pretty normal."
n "I shuffled through his magazines on the table."
n "It was just some business and world news stuff."
n "He seemed like a pretty serious guy, despite his intentions for me."
n "It didn't seem like he was all too interested in speaking with me as well."
n "Cain just sipped his coffee and looked outside."
menu:
    "-Keep looking around-":
        $ lookaround_punishment1 = True
        jump cain_punishment_1
    "\"It's nice out\"":
        $ cain_love +=10
        n "I spoke to him hesitantly, unsure of his mood."
        n "He took a sip his coffee and set it on the window sill."
        show cain
        $ cwings,cbase, cexp = 0,3,7
        cain "Yes...very nice."
        cain "Being locked away for so long you start to forget what the sun looks like."
        $ cwings,cbase, cexp = 0,3,8
        p "Locked away? Like in prison?"
        n "I shifted nervously, but I kept my eyes on him."
        $ sanity -=10
        if sanity <= 0:
            jump cain_sanity_ending
        n "Was...was this guy an ex-con?!"
        n " I felt sweat beginning to crawl down the back of my neck."
        n "He looked out the window again."
        cain "I suppose you could call it that."
        cain "It is a prison of sorts."
        cain "I believe you humans know it by a different name."
        n "Cain's tone was somber, making it apparent that this wasn't a happy subject for him."
        n "Was that why he was keeping me here?"
        n "Did he want someone else to go through what he did?"
        n "Or did he just want someone to take his rage out on?"
        n "Why me of all people?"
        n "I...I don't know."
        n "I didn't want to ask him anymore questions."
        n "I didn't want to think about it."
        jump cain_day1_noon


label cain_punishment_1:
show cain
cain "What are you looking for?"
n "Cain asked as I reached for the door."
n "I dropped my arm and sighed looking over at him."
p "Just looking around."
cain "Why don't you take a seat and talk to me instead?"
n "Cain extended his arm and pointing at the chair across from him."
n "I saw no reason not to and did as he asked."
p "What could we talk about?"
$ cwings,cbase, cexp = 0,3,9
cain "Are you not curious about why you're here?"
cain "I'm an angel you know."
cain "You realize that any sinful thoughts that might be plaguing you."
cain "I might be able to help you with them."
menu:
    "-Tell him about your sins-":
        $ cain_boredom +=1
        $ cwings,cbase, cexp = 0,3,5
        jump tell_cain_sins
    "-Don't tell him anything-":

        $ cain_love +=10
        jump dont_tell_cain_sins

label dont_tell_cain_sins:
n "I didn’t know what it was, but something about his words set me on edge."
$ cwings,cbase, cexp = 0,3,7
n "Whatever he was offering, I wasn’t interested."
n "I averted my gaze. I wasn’t going to admit anything to him."
cain "Oh? Getting quiet now huh?"
n "Cain said putting up his hand, I could feel myself dragging over to him."
n "My body left the chair and his invisible hands pulling me over to him."
$ cwings,cbase, cexp = 0,3,12
cain "No matter, I'll punish you anyways!"
n "His tone was cheerful but deadly."
cain "If you're going to pout like a child, then I'll treat you like one."
$ cwings,cbase, cexp = 0,3,9
cain "Ask daddy for his forgiveness."
menu:
    "-Do as he says-":
        $ sanity -=10
        $ cain_love +=10
        n "I could tell I’d made him angry and I didn’t want things to get worse."
        p "I-I’m sorry."
        n "I stumbled over the words, humiliated."
        n "My face felt hot."
        n "I couldn’t believe I was doing this."
        p "Please forgive me...daddy."
        n "He pulled down my underwear and rubbed his palm against my ass."
        $ cwings,cbase, cexp = 0,3,11
        cain "Bend over my knee, I'll forgive you."
        jump cain_daddy_kink
    "-Refuse-":
        $ sanity +=10
        jump cain_dayone_refuse

label cain_daddy_kink:
menu:
    "\"Okay.\"":
        $ sanity -=10
        n "I was nearly dizzy with embarrassment but I didn’t want to disobey now."
        n "Hesitantly, I lowered my body across his lap, wriggling slightly in discomfort at his knee digging into my stomach."
        p "Like...like this?"
        $ cwings,cbase, cexp = 0,3,18
        cain "Yes, you're a good listener!"
        n "Cain said swatting his hand across my ass."
        n "He sent a few blows into my skin, only leaving a mild stinging sensation as he rubbed his hand on my skin."
        n "His gentle touches soothed my skin and made my heart beat faster."
        n "My face grew hotter as I realized I was relaxing into his touch."
        $ cwings,cbase, cexp = 0,3,4
        cain "How does that feel?"
        n "I bit my lip."
        n "It definitely didn’t feel bad."
        n "The slap had hurt a little bit but after the pain faded I recognized a new feeling blooming in the pit of my stomach."
        p "It...feels good."
        $ cwings,cbase, cexp = 0,3,11
        n "Cain leaned into my shoulder."
        cain "Does it?"
        $ cwings,cbase, cexp = 0,3,9
        n "His lips brushed against my shoulder and he kissed my flesh."
        cain "I wouldn't want to keep you hanging now."
        n "Cain's low tone floating into my ear."
        n "He rubbed his fingers on my ass and they hovered over my entrance."
        cain "Let's do something else."
        n "He stroked around my erogenous zone, slowly pushing his fingers inside of me."
        cain "Ah. You're not even resisting."
        cain "Do you really like this?"
        n "He teased as he pushed his fingers in and out of me."
        n "A moan slipped past my lips before I could stop it."
        n "I didn’t think I’d be able to lie at this point if I wanted to anyway."
        n "My body reacted to his every touch, my back arching and my hips moving without conscious thought."
        p "I really do."
        n "I wasn’t as embarrassed as before."
        n "He slid me off his lap and pulled my hips up."
        $ cwings,cbase, cexp = 0,3,10
        cain "Well, let me indulge you sweetie."
        n "He said as he rubbed his cock up against me."
        $ cwings,cbase, cexp = 0,3,9
        cain "Beg for it."
        n "He commanded in a smooth and deep tone."
        n "I was ready to do whatever he said if it meant he’d touch me more."
        $ sanity -=10
        p "I want you."
        n "I knew I sounded breathless and needy."
        n "I didn’t care."
        p "I want to feel you, all of you."
        p "Please fuck me."
        n "Without another word he forced his way inside of me."
        n "He let out a stable breath and pushed in and out of me."
        $ cwings,cbase, cexp = 0,3,16
        cain "Ah. You feel so good."
        n "He moaned into my back."
        n "He grabbed my arm and twisted it around my back, using it to thrust deep inside of me."
        n "My whole body moved with the force of his thrusts."
        n "I didn’t try to stop the sounds that he brought out of me, long moans and pleasured whimpers."
        $ cwings,cbase, cexp = 0,3,17
        p "Ahh! Cain! Cain…."
        n "I said his name over and over with the same passionate desperation as a prayer."
        p "Oh...oh god."
        n "I knew I wouldn’t last long."
        n "Cain's motions came in hard and fast."
        $ cwings,cbase, cexp = 0,3,9
        cain "You can call me god if you want."
        n "He teased letting out a breath."
        n "My breath hitched at his words."
        n "Having him above me--inside me--telling me something like that made me shiver."
        n "This was worship in a way."
        n "I’d submitted to him and let him do what he wanted to me."
        n "And I’d enjoyed it."
        $ sanity -=10
        n "It was fitting to think of him as a god."
        n "He clenched his teeth and came deep inside of me."
        n "Cain let my hips fall on the couch."
        n "His hand caressing my hair gently, feeling the strands."
        cain "Why don't you rest there?"
        n "Cain pulled off his blazer and dropped it on me."
        n "He got up and left me alone."
        scene black with fade
        n "I snuggled his jacket smelling the cologne on it."
        n "The warmth and smell made my head spin, I closed my eyes and fell asleep."
        jump cain_night_1
    "\"NO!\"":

        $ cain_love -=10
        jump cain_dayone_refuse

label cain_dayone_refuse:
$ cwings,cbase, cexp = 0,3,2
cain "No?"
$ cwings,cbase, cexp = 0,3,5
n "Cain said with a sigh."
$ cwings,cbase, cexp = 0,3,8
n "He grabbed my wrist and forced me over his knee."
cain "We'll just see about that."
n "He tore off my underwear and reeled back sending his palm into my ass with a great amount of force."
n "Pain radiated through my body and a scream tore from my throat."
n "The sound of the slap was almost frightfully loud, echoing in the silence."
$ health -=5
n "I didn’t expect it to hurt so much."
n "I squeezed my eyes shut as tears threatened to fall."
cain "Was that not enough?"
$ cwings,cbase, cexp = 0,3,9
n "Cain said tilting his head to the side."
cain "Well, honey, I got something else then."
n "He put up his hand and I looked over my shoulder."
n "His palm radiated and glowed like a hot iron as he brought it down on my skin."
$ health -=10
n "I could hear the heat searing my flesh."
n "The agonizing burning sensation made me thrash and writhe in pain."
$ health -=10
n "I struggled to get enough air into my lungs as I cried out hoarsely."
n "I wasn’t too proud to beg anymore."
p "No more."
p "It hurts so much."
p "Please...no more."
n "Cain peeled his hand off my ass and looked at my flesh that tore away from me."
$ sanity -=10
cain "Had enough hm?"
n "He licked my blood off his fingers and looked down at me."
n "He grabbed a fist full of my hair and leaned into me."
$ cwings,cbase, cexp = 0,3,7
cain "Next time... You should just do as you're told."
$ cwings,cbase, cexp = 0,3,9
n "He said as he pushed his bloody fingers into my mouth."
n "His hand was no longer hot and my mouth was filled with the flavor of burnt skin and hot blood."
$ sanity -=10
n "My stomach turned at the sick, coppery taste."
n "I swallowed to keep down the bile rising in my throat and nearly heaved again."
n "I shivered, trying to stay calm, but I felt so disgusted and humiliated."
n "He dropped me on the couch and walked away."
scene black
n "I closed my eyes and tried to forget what just happened."
jump cain_night_1

label tell_cain_sins:
n "I considered his words carefully."
$ cwings,cbase, cexp = 0,3,7
n "Did I have any \"sinful thoughts?\"?"
n "At the very least, I knew I had a lot on my mind, and maybe a few things I wasn’t so proud of."
n "I wasn’t sure what I had to lose anymore. I decided to tell him."
$ sanity-=10
n "Cain nodded at every word and folded his fingers in front of his face."
n "He looked thoughtful as I spoke and took a deep breath when I was finished."
cain "You seem to have a lot on your mind."
n "He stood up and put his hands on his hips watching me."
cain "So, do you want absolution, sinner?"
n "I hesitated."
n "He sounded serious about this."
p "What...what do you mean, exactly?"
cain "I mean... I can absolve you of your sins in my domain."
$ cwings,cbase, cexp = 0,3,9
cain "You can be free of your worries and anxiety."
cain "This could be a new start for you after all."
cain "Wouldn't it be nice?"
menu:
    "\"Yeah, that would be nice.\"":
        $ cain_love +=10
        n "I’d been terrified and confused since I got here."
        n "If he was willing to do something to help me, I wasn’t about to turn him down."
        n "Cain made a motion with his hand as if to tell me to turn around."
        $ cwings,cbase, cexp = 0,3,1
        cain "Turn and I'll absolve you."
        n "I turned my back to him and gripped the seat."
        n "I could hear something heavy hit the floor."
        n "He reeled back and I felt something lashing against my skin."
        $ health -=5
        n "The shock and the pain made me cry out."
        n "I looked over my shoulder and saw the instrument of my pain clatter against the floor."
        n "A whip."
        n "Cain pulled the whip back and looked at the leather strips."
        cain "Hmm. I don't think that's nearly enough for you."
        cain "I want to hear you beg for forgiveness."
        $ cwings,cbase, cexp = 0,3,9
        n "He pulled back one more time and whipped me again, this time tearing flesh from my back."
        $ health-=10
        n "I choked on a scream at the sensation, my body tensing in reaction to the pain."
        n "I was in agony."
        n "I just wanted it to be over."
        p "Please. Please, I want to be forgiven."
        n "My voice was hoarse."
        n "It felt like my back was on fire."
        n "I tried not to cry."
        cain "HAHA THAT'S A GOOD PET."
        n "Cain whipped me one more time and dropped the flogger on the floor."
        n "He leaned towards my back and ran his tongue against my blood."
        n "The look on his face sent a shiver down my spine."
        cain "Hm... You taste good."
        $ sanity +=10
        n "Despite everything that had just happened, I felt better somehow."
        n "My heart wasn’t pounding, and my nerves had settled."
        n "It was almost as if I had a clearer conscience than before."
        cain "Isn't it better to just tell the truth, little one?"
        n "Cain said running his fingers down my back, the pain on my back releasing at his touch."
        $ health +=5
        n "Cain looked at me and kissed the back of my head."
        cain "You've been absolved."
        cain "Why don't you clean up and take a load off."
        n "He put a towel next to me and exited the room allowing me a moment of silent thoughts."
        scene black with fade
        n "I closed my eyes and pulled the towel around me, letting it's warmth comfort me."
        $ sanity +=10
        n "I quickly fell into a restful sleep."
        jump cain_night_1
    "\"I changed my mind.\"":

        $ cain_love -=10
        $ cwings,cbase, cexp = 0,3,7
        n "Cain shrugged his shoulders."
        cain "Your loss."
        n "He got up and grabbed my neck."
        cain "You should have really said yes."
        n "He slammed me into the ground, I felt my head bouncing off the hardwood then nothing but blackness."
        scene black with fade
        $ health-=20
        jump cain_night_1


label cain_day1_noon:
scene livingroom:
    xalign 0.5
    easeout 0.9 xalign 0.0
if lookaround_punishment1 == True:
    n "I woke up and looked around."
    show CG_CainReading
    n "Cain was sitting on the living room couch, reading a book."
else:
    n "Cain moved to the couch and took a seat."
    show CG_CainReading
    n "He lifted a book off the table and began to read it."
show CG_CainReading2
cain "It's not polite to stare."
show CG_CainReading2_glow:
    subpixel True
    alpha 0.0
    easein 0.4 alpha 1.0
    easeout 0.3 alpha 0.0
cain "Didn't anyone teach you any manners?"
n "I jumped, startled by Cain's comment."
scene cain_livingroom
n "I didn't even realize that I was staring at him."
show cain

menu:
    "-Yell at him-":
        $ cain_love +=10
        p "Are...are you nuts!?"
        p "You must be fucking insane if you think that I'm going to let you keep me here!"
        n "I shouted, completely fed up with this man's games."
        scene livingroom:
            xalign 0.0
            easeout 0.9 xalign 0.9
        n "I turned around and stormed off towards the door."
        n "A mass of black feathers began to swirl in front of me and my eyes widened as Cain walked out of it. "
        $ cwings,cbase, cexp = 0,3,2
        show feather_animation:
            subpixel True
            alpha 0.0
            easein 0.2 ypos 50 alpha 1.0
            easeout 0.1 alpha 0.0
        show cain with dissolve
        cain "Listen here you impudent little child, I don't have the patience for your defiant drivel."
        n "He examined me with cold eyes before speaking again."
        cain "You're beginning to show me how much of a waste of life you are."
        n "He raised his hand and I could feel myself lifting off the ground."
        n " I kicked and screamed as I floated before being slammed into the wall." with vpunch
        jump cain_roses
    "-Ask him to let you go-":

        $ cain_boredom +=1
        if cain_boredom >=3:
            jump cain_boredom_day1
        $ cwings,cbase, cexp = 0,3,5
        p "Hey, uh....Cain?"
        n "Cain looked up from his book for a moment before closing it and placing it on the table."
        $ cwings,cbase, cexp = 0,3,7
        cain "What is it?"
        n "I took a nervous gulp."
        n "I was finding it hard to answer him with his eyes boring into me like hateful drills."
        cain "Let me guess, you want me to let you go. Right?"
        n "I nodded."
        $ cwings,cbase, cexp = 0,3,11
        n "He got up from his seat and raised his hand."
        scene livingroom:
            xalign 0.0
            easeout 0.05 xalign 0.9
        $ health -=5
        n "An invisible force smashed me into the wall." with vpunch
        jump cain_roses
    "-Back off-":

        $ cwings,cbase, cexp = 0,3,7
        $ cain_love -=10
        jump cain_look_around_day1_noon


label cain_look_around_day1_noon:
$ cain_noon_bathroom = False
n "I should look around more."
menu:
    "-Bathroom-":
        jump cain_day1_bathroom_noon
    "-Bedroom-":
        jump cain_day1_bedroom_noon

label cain_roses:
n "The force relented and I slumped the floor."
show cain
cain "Listen here, love."
n "Cain kneeled down and gently caressed my hair."
n "I felt something wrap around my arms and legs."
n "I looked down to see what appeared to be vines."
n "I didn't get much of a glance since Cain lifted my head up by the chin and forced me to look at him."
$ cwings,cbase, cexp = 0,3,8
cain "Look at me when I'm talking to you, trash."
n "The vines started to twist around my limbs, getting tighter I could feel sharp thorns begin to dig into my flesh."
n "The vines then lifted me off the ground, displaying my entangled body to Cain."
$ health -=10
$ cwings,cbase, cexp = 0,3,7
cain "Now, I wouldn't say that I'm much of a gardener."
cain "Plants don't seem to last long in my care."
cain "I suppose you could say I lack the \"green thumb\" that competent gardeners possess."
n "Cain circled around me as he spoke."
n "All I could do was whimper and squirm as the vines tightened and barbs cut my skin."
$ cwings,cbase, cexp = 0,3,4
cain "But, I do have an appreciation for roses."
cain "Red ones in particular."
n "Cain reached over to the vine that was restraining my left arm and plucked a red rose off it. "
n "He held it up and examined it."
cain "A flower known to represent everlasting love and romance."
n "He shook his head in disapproval before continuing."
cain "You humans try to find meaning in the strangest places."
cain "Somehow you found it fitting to attach intimacy, adoration, and fondness to a small, inconsequential plant."
cain "In doing this, you create a false sense of love in the exchanging of these flowers since you sad mortals are too inept at truly expressing it."
n "Cain crushed the rose in his hand."
cain "Pathetic."
n "He opened his hand and let the petals fall to the floor."
cain "It's just a pretty weed that you all foolishly decided had significance."
$ cwings,cbase, cexp = 0,3,7
show cain
n "I...I could feel the thorns dig deeper."
n "They were growing longer, becoming more akin to spikes than thorns."
n "I gasped as the sharp spines slowly drove themselves into me."
n "I whimpered and tears began to run the down my face."
$ cwings,cbase, cexp = 0,3,9
n "Cain noticed my crying and leaned his face in close to mine."
cain "What's wrong, my pet?"
cain "Did I upset you?"
cain "You've gotten so quiet."

menu:
    " \"STOP!\"":
        $ cain_boredom +=1
        if cain_boredom >=3:
            jump cain_boredom_day1
        $ cwings,cbase, cexp = 0,3,5
        p "Stop....please..."
        n "I sobbed as the vines continued their savage work."
        p "I can't..."
        n "Cain took off his blazer and tossed it aside as he got closer."
        $ cwings,cbase, cexp = 0,6,11
        cain "Stop? The fun hasn't even started yet."
        n "I felt a barb begin to form against the middle of my back."
        $ health -=10
        cain "I have to say though, this is a really good look for you."
        n "He said as he eyed me up and down."
        n "The sharp tip of the newly developing spike struggled to pierce my spine as it fought against the bone."
        $ health -=10
        p "AH! Cain, please!"
        n "I begged."
        n "Cain let out an exasperated sigh."
        $ cwings,cbase, cexp = 0,6,5
        cain "My, you're so fragile."
        cain "And here I was hoping you were made of tougher stock."
        n "I couldn't handle much more of this."
        n "My body was reaching its breaking point."
        if cain_love <=30:
            n "The razor-edged stakes finally penetrated bone as I heard my spine snap and an immense wave of pain shot through my body."
            n "I tried to plead for him to stop, but all I could do was scream and wail in agony."
            p "C-Cain..."
            $ cwings,cbase, cexp = 0,6,4
            n "Cain rested his index finger on my lips."
            cain "Shhhh. Don't worry, sweetheart."
            cain "It'll all be over soon."
            n "A plethora of long bloody barbs protruded from my arms and legs, giving my body the appearance of a nightmarish pincushion."
            n "More spikes ripped through my torso, tearing through skin, muscle, and bone."
            n "I coughed and sputtered up blood onto my chest."
            n "I weakly lifted up my head to look at Cain."
            n "A pressure began to build under my sternum."
            n "Roses burst out of my chest, my vision slowly grew dark."
            show CG_cain_Bloody_Rose with dissolve
            n "I heard Cain speak as my hearing started to fade."
            cain "You know, I think that you might make a wonderful centerpiece."
            cain "Now, where should I put you?"
            cain "You're a little too big for the dining room table."
            hide screen health_bar
            hide screen sanity_bar
            play music "cain/cain_death.mp3"
            $ persistent.cain_ending_centerpeice = True
            scene endslate with Dissolve(1.0)
            screen cain_ending_centerpeice:
                text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                text "\n\n\n\n{=endslate_subtitle}Cain made you a centerpiece.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
            show screen cain_ending_centerpeice
            with Dissolve(1.0)
            pause
            return
        else:
            n "Cain studied me for a moment, contemplating his next move."
            cain "Alright. I'll stop."
            cain "It would be a shame if you were to die now."
            cain "Especially since I've barely had my fun with you."
            n "He waved his hand and the thorns retracted, the vines loosened, and my bloodied body was lowered to the floor."
            n "Cain turned his back to me before walking out of the room."
            cain "Get yourself cleaned up."
            cain "And try not to bleed on everything."
            hide cain with fade
            jump cain_night_1
    "\"It hurts.\"":

        $ cain_love +=10
        n "The pain made it difficult to speak."
        $ health -=10
        n "Cain ran his fingers through my hair and caressed my face."
        n "He took off his blazer and tossed it aside."
        $ cwings,cbase, cexp = 0,6,12
        cain "You don't say."
        n "He ran his fingers up my skin and I trembled at his touch."
        cain "Well love, did you ever think to consider that it's supposed to hurt?"
        $ cwings,cbase, cexp = 0,6,6
        n "Cain rubbed his hands across my body as if he were examining me."
        cain "Hmm. Perhaps I should leave you be for now."
        cain "I'd hate for my new toy's life span to be so short."
        n "The thorns receded and the vines wilted."
        n " I collapsed to the floor and curled myself into a ball."
        $ cwings,cbase, cexp = 0,6,9
        cain "I'm not really in the mood to hunt for a replacement so soon."
        hide cain with fade
        n "Cain stepped over me and walked into the other room."
        n "I looked at my limbs, wanting to see the extent of the damage."
        n "A myriad of cuts and lacerations littered my arms and legs, blood still flowing out from the wounds."
        n " I wept on the cold floor."
        scene black with fade
        n "With any luck...maybe I'll bleed out.."
        jump cain_night_1

label cain_day1_bedroom_noon:
$ cain_bedroom_day1 = True
screen phone_button:
    imagebutton xalign 0.433 yalign 0.632:
        hover ("cain/phone_button_hover.png")
        idle ("cain/phone_button.png")
        action (Jump('damienday1'))

scene cain_bedroom_morning
show screen phone_button
n "I walked into Cain's bedrooom and looked around."
n "It was beautiful and I looked out the window."
n "Nothing more outside than red sky..."
n "I sighed and moved away from the window."
n "There wasn't anything important here."
hide screen phone_button
jump cain_night_1

label cain_day1_bathroom_noon:
$ cain_noon_bathroom = True
scene cain_bathroom with dissolve
$ cain_love +=10
play music "cain/cain_calm.mp3"
n "I walked into the bathroom and inspected the pillar to my right."
n "I placed my hand on it as the sun poured into the room."
n "I then made my way over to an elegant looking bathtub and sat on the rim of it."
n "I closed my eyes, basking in the warm rays."
n "It all felt very serene."
n "The combination of sun's warmth and the silence made me feel calm."
n "For a moment I forgot where I was, I forgot about my situation."
n "It was nice."
$ cwings,cbase, cexp = 0,6,7
show cain
cain "It's a nice bathroom, huh?"
n "Cain's voice broke the tranquil scene."
p "Y-yeah."
n "He walked over and patted my head."
n "I looked up at him, confused as to what kind of plans that he was brewing in that brain of his."
n "Cain looked down at the tub."
$ cwings,cbase, cexp = 0,6,18
cain "Hmm. Maybe I can think up something fun to do in here later."
play music ["cain/cain_shift.mp3" ] fadeout 1.0 fadein 1.0
n "I looked at the tub then back at him."
n "My heart began to race from the look that he was giving me."
n "Cain turned away and exited the room without explaining further."
hide cain with dissolve
n "I got the uneasy feeling that he and I didn't share the same idea of \"fun\"."
n "I got up from the tub and headed out of the bathroom."
n "I probably shouldn't linger here for much longer."
scene black with fade
n "All the peacefulness had left the room anyways."
jump cain_night_1

label cain_night_1:
if cain_bedroom_day1 == True:
    n "I spent some time in Cain's bedroom."
else:
    n "Some time in my stupor I must have wandered back into the bedroom."
scene black with fade
scene cain_bedroom_night
n "Where should I go tonight?"
menu:
    "-Bathroom-" if cain_noon_bathroom == True:
        jump cain_nightone_bathroom
    "-Balcony-":
        jump cain_night_1_Balcony
    "-Livingroom-":
        jump cain_night_1_livingroom

label cain_night_1_livingroom:
scene cain_livingroom:
    subpixel True
    xalign 0.9
n "I saw Cain at the stove cooking something."
$ cwings,cbase, cexp = 0,8,9
n "Steak?"
p "What's that?"
scene cain_livingroom:
    subpixel True
    xalign 0.9
show cain with dissolve
cain "It's steak."
p "What kind?"
cain "Beef, silly child."
$ cwings,cbase, cexp = 0,8,4
cain "What else would I be eating?"
cain "I was a human once as well, you know."
n "I narrowed my eyes and I could feel myself being lifted off the ground."
p "H-HEY!"
n "I screamed as he slammed me down on the table."
n "He loomed over me."
cain "Stay still, pet."
$ cwings,cbase, cexp = 0,8,9
n "He placed the hot meat on my stomach."
n "I felt it burning through my skin and I slapped my hands over my mouth to muffle the scream."
n "I could feel my stomach muscles tighten as he leaned over me. "
cain "You don't need to scream."
cain "Just don't move. "
n "Cain took out a sharp looking fork and stabbed it into the meat. "
n "It grazed my skin."
n "I let out a small relieved sigh but quickly stiffened back up when he took out a knife."
n "A sharp ritual dagger."

menu:
    "\"WHAT ARE YOU DOING!?\"":
        $ cain_love +=10
        $ cwings,cbase, cexp = 0,8,9
        n "Cain let out an exasperated sighed and he pushed the fork harder into the meat stabbing me."
        $ health -=5
        $ sanity -=10
        if sanity <= 0:
            jump cain_sanity_ending
        cain "Be a good dinner plate."
        n "His words were pointed, warning me of the pain that was coming."
    "-Stay still-":
        $ cain_boredom +=1
        if cain_boredom >=3:
            jump cain_boredom_day1
        $ cwings,cbase, cexp = 0,8,5
        n "I stayed still and did as he asked."
        $ cwings,cbase, cexp = 0,8,4
        n "I was trembling slightly but Cain didn't seem to notice it."

n "Cain pushed the knife into the meat and began cutting through it."
n "I could feel the sharp teeth of the knife digging into the upper layer of my skin."
$ health -=5
$ cwings,cbase, cexp = 0,8,11
n "I let out a small pained noise."
cain "This meat is a bit over cooked."
n "Cain looked at the piece of meat."
$ cwings,cbase, cexp = 0,8,7
cain "Still a bit bloody though."
n "It was covered in my blood as he put it into his mouth."
n "He looked at me as I trembled lightly."
$ cwings,cbase, cexp = 0,8,1
cain "Are you hungry?"
n "He didn't let me begin before he started to cut into my thigh."
$ health-=10
n "I screamed and he put his hand over my mouth pushing me down on the table."
cain "Don't scream."
$ sanity-=10
if sanity <= 0:
    jump cain_sanity_ending
n "Cain pushed the knife into my muscle."
n "The pain shot through my skin as he tore off the piece of flesh from my body."
$ health-=10
n "He cut a perfect square of meat out of me."
show CG_Cain_meatonfork_meat
cain "Say Ah..."
menu:
    "-Refuse-":
        p "NO."
        n "Cain sighed and look at his knife."
        cain "What good are you then?"
        n "Cain stabbed the knife into my gut and ripped my organs out of my stomach."
        n "I started to scream."
        p "STOP!! STOP!!"
        p "IT HURTS!"
        $ health -=100
        $ sanity -=10
        n "Everything was cold and painful."
        n "I just wanted to die."
        cain "...You're not dying yet..."
        $ health +=100
        $ sanity -=10
        n "He said softly as I felt myself keeping consciousness."
        $ health -=100
        $ sanity -=10
        n "I gasped for air... I knew I should be dead."
        $ health +=100
        $ sanity -=10
        n "But he was keeping me alive."
        $ health -=100
        $ sanity -=10
        show CG_Cain_Gutrip
        n "He pushed the guts into my open mouth."
        $ health +=100
        $ sanity -=10
        cain "...What's wrong sweetie?"
        $ health -=100
        cain "Too much?"
        $ health +=100
        $ sanity -=10
        n "He pushed the coppery cords into my throat."
        $ health -=10
        $ sanity -=10
        n "I couldn't breath."
        $ health -=10
        $ sanity -=10
        n "I just wanted die."
        $ health -=10
        $ sanity -=10
        n "I gagged and choked."
        $ health -=10
        $ sanity -=10
        n "I wanted it out of my mouth."
        $ health -=10
        $ sanity -=10
        n "Cain pushed more of the cords in as I tried to breath through my nose."
        $ health -=10
        $ sanity -=10
        cain "Eat it."
        $ health -=10
        $ sanity -=10
        n "What other choice did I have."
        n "I swallowed what was in my throat as much as I could."
        n "Cain started to laugh as my mind blanked out."
        $ health -=100
        $ sanity -=100
        cain "You can go now."
        hide screen health_bar
        hide screen sanity_bar
        play music "cain/cain_death.mp3"
        $ persistent.cain_ending_autocani = True
        scene endslate with Dissolve(1.0)
        screen cain_ending_autocani:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You ate yourself.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen cain_ending_autocani
        with Dissolve(1.0)
        pause
        return
    "-Open mouth-":


        $ sanity -=10
        $ cain_love +=10
        n "I opened my mouth and let him feed me the bit of me he took off."
        n "It tasted horrible and it made me sick knowing where it came from."
        cain "How was that, lovely?"
        if sanity <= 0:
            jump cain_sanity_ending
        show CG_Cain_meatonfork with dissolve
        menu:
            "\"Fuck you..\"":
                $ cain_love -=10
                $ sanity +=10
                $ cwings,cbase, cexp = 0,8,7
                cain "Feisty."
                n "He elbowed my wound causing me to cry out."
                $ cwings,cbase, cexp = 0,8,12
                cain "Go to sleep."
                scene black with fade
                n "All I could think of was the seering pain"
                jump cain_Morning_day2
            "\"It was good.\"":
                $ cain_love +=10
                n "I smiled weakly."
                n "He could fix this for me right?"
                $ cwings,cbase, cexp = 0,8,4
                p "It was good."
                $ sanity -=10
                if sanity <= 0:
                    jump cain_sanity_ending
                n " I said trying to sound perky."
                n "I was losing some blood and light headed but I smiled for him. "
                n "Cain put his hand on my head."
                $ cwings,cbase, cexp = 0,8,10
                cain "That's a good pet."
                n "He pushed the food off me and pushed a napkin on my wound."
                scene cain_livingroom with dissolve:
                    subpixel True
                    xalign 0.9
                show cain with dissolve
                n "I let out a loud squeal at the pain."
                cain "Hold it there till tomorrow, darling."
                n "He said as he left me on the table."
                n "I laid my head back with the napkin on my stomach."
                n "Somehow it felt better."
                n "I closed my eyes and passed out from the blood loss."
                scene black with fade
                jump cain_Morning_day2
            "-Say nothing-":
                $ cain_love -=10
                $ sanity -=10
                n "I curled up and tried to forget what just happened."
                if sanity <= 0:
                    jump cain_sanity_ending
                $ cwings,cbase, cexp = 0,8,12
                cain "Take care of that yourself. You're capable."
                n "Cain said as he backed away from me."
                n "I collected a napkin close by and passed out."
                scene black with fade
                jump cain_Morning_day2


label cain_night_1_Balcony:
scene cain_livingroom_night with dissolve
play music "cain/cain_calm.mp3"
n "I walked into the living room and looked around."
n "It was a little dark in here, but I managed to see a silhouette on the balcony."
n "I crept through the darkness and carefully made my way towards the patio."
n "Cain didn't react to my opening of the sliding door, maintaining his focus to something off in the distance."
scene cain_balcony with fade
cain "Come over here."
$ cwings,cbase, cexp = 0,7,14
show cain
n "His tone was different from earlier."
n "It sounded more soft and thoughtful."
n "I wandered over to him and looked at the horizon."
n "I noticed that the sky looked different."
n "Something about it seemed off."
n "It looked kind of unnatural."
menu:
    "\"Where are we?\"":
        n "Cain gave me a quick side glance."
        $ cwings,cbase, cexp = 0,7,15
        cain "My, you're an inquisitive one."
        n "He stared thoughtfully at the sunset for a moment."
        cain "I'll tell you."
        n "Cain leaned on the rail."
        $ cwings,cbase, cexp = 0,7,14
        cain "We are in what you humans know as Tartarus."
        cain "Although Tartarus is different from what you know it to be in your realm."
        cain "It acts as a halfway point between hell and earth instead of a prison for the damned."
        cain "That's what Hell is for."
        cain "But for a Fallen like me, Tartarus is more of a haven."
    "\"What are you looking at?\"":
        n "Cain kept his eyes on the horizon."
        cain "Hm? The sunset."
        n "Cain said as he nodded over to the skyline."
        cain "Don't tell you've never seen a sunset before."
        n "It was definitely no sunset that I have ever seen."
        n " It looked kind of...abnormal to me."
        cain "Say what you will about this place, the sunset is always beautiful in Tartarus."
    "\"You don't seem like the type to enjoy this scenery.\"":
        p "I mean you're supposed to be a big shot demon right?"
        p "Why aren't you chasing me around or hurting me?"
        n "Cain said nothing as he kept his eye on the horizon."
        p "You don't have anything to say!?"
        p "MAYBE YOU DON'T HAVE THE STONES TO HURT ME!"
        n "Cain put out his hand and flicked it towards the rail."
        n "I watched his hand motion for a second."
        n "It didn't last long as I felt myself lift off the floor."
        cain "Have some class, you animal."
        n "I felt myself falling off the side of the balcony."
        hide screen health_bar
        hide screen sanity_bar
        play music "cain/cain_death.mp3"
        $ persistent.cain_ending_pushed_balcony = True
        scene endslate with Dissolve(1.0)
        screen cain_ending_pushed_balcony:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Cain pushed you off.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen cain_ending_pushed_balcony
        with Dissolve(1.0)
        pause
        return

n "I stood next to Cain and watched the sunset with him."
n "As strange as the sunset in this place was, I couldn't help but think that it did look of pretty."
$ cwings,cbase, cexp = 0,7,15
n " I leaned into his touch without thinking."
cain "Hm?"
$ cwings,cbase, cexp = 0,8,7
n "Cain shifted in front of me and I felt my back hit the rail of the balcony."
n "He leaned down and nuzzled my neck."
p "...C-Cain..."
n "I gasped out as he put his hands on my hips."
$ cwings,cbase, cexp = 0,8,16
cain "You smell nice."
n "Cain whispered into my skin."
n "I trembled as his hands traveled up and down my body."
n "I felt his lips touch my neck and I gasped."
p "Please... Don't.."
play music "cain/cain_shift.mp3"
n "He suddenly grabbed me by my neck and lifted me off the floor."
p "W-What the hell are you doing?!"
$ cwings,cbase, cexp = 0,8,1
n "I kicked and screamed as I hovered above the ground."
n "Cain ripped my underwear off of my legs."
$ sanity -=10
if sanity <= 0:
    jump cain_sanity_ending
cain "Let's have a little fun."
n "Cain said as he dangled me off the side of the balcony."
cain "Let's see how strong your will to live is."
n "I could feel the wind blow against my bare legs."
n "I grabbed on to Cain's arm to secure myself to something in case he decided to just let go."
$ cwings,cbase, cexp = 0,8,1
cain "Beg."
n "He commanded, now stroking his cock with his free hand."
n "I panicked and looked around. "
n "There was no where else to go but down."
$ time = 1
$ timer_range = 1
$ timer_jump = 'balcony_sex'
show screen countdown
menu:
    "-Beg-" if cain_boredom >=3:
        hide screen countdown
        jump balcony_beg
    "-Struggle-":
        hide screen countdown
        jump balcony_struggle

label balcony_beg:
$ cwings,cbase, cexp = 0,8,8
cain "Really?"
cain "Just like that?"
cain "Have you no spine?"
cain "No pride?"
n "I didn't know how to answer him."
n "I...I just didn't want to die."
cain "Tsk. Pathetic."
cain "I had such high hopes for you."
n "He sighed and shook his head."
cain "Maybe I'll see if you have a spine after your pitiful body stains the ground."
n "My eyes widened with fear."
p "N-no! Wait-"
n "He released his grip and I struggled to keep my hold on his arm."
n "The last thing I saw was Cain's vile grin as my hands lost the strength to hold on and finally let go."
show CG_Cain_Fall with dissolve
n "I screamed as I made my rapid descent to the ground below, my screams ceasing when my body violently smacked into the hard stone floor."
n "Overwhelming pain shot through my broken frame."
scene black with fade
n "I could feel blood gush from my fractured skull as my consciousness slowly faded and my vision...went dark..."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_dropped_balcony = True
scene endslate with Dissolve(1.0)
screen cain_ending_dropped_balcony:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain dropped you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_dropped_balcony
with Dissolve(1.0)
pause
return


label balcony_struggle:
p "W-what?! No! HELL no, even!"
n "I shouted, grabbing onto his arm and trying to pull myself closer to the balcony."
n "He started to laugh."
$ cwings,cbase, cexp = 0,8,9
cain "No? Is that your final answer?"
n "I glared at him before giving him my \"answer.\""
p "Fuck. You."
n "Cain's expression changed from one of amusement to one of displeasure."
cain "You know, you've suddenly become a lot heavier."
cain "I don't think I can hold on much longer."
n "My eyes widened as I felt Cain loosen his grip."
cain "Good bye."
n "Cain taunted before releasing his hold completely."
p "N-No! DAMN YOU!"
show CG_Cain_Fall with dissolve
n "I shrieked as I rapidly started plummeting to the ground below."
n "Well, this is it I guess."
n "Thrown from a fallen angel's balcony."
n "I suppose there's worse ways I could have gone."
n "I closed my eyes and braced for the inevitable splat I would make against the harsh floor."
if cain_love < 50:
    $ health -=100
    n "I felt my head hit the ground."
    hide screen health_bar
    hide screen sanity_bar
    play music "cain/cain_death.mp3"
    $ persistent.cain_ending_struggled_balcony = True
    scene endslate with Dissolve(1.0)
    screen cain_ending_struggled_balcony:
        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}You struggled.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen cain_ending_struggled_balcony
    with Dissolve(1.0)
    pause
    return
else:
    scene black with fade
    n "Am...am I dead?"
    n "I feel like should have hit the ground by now."
    n "I opened one eye to see a winged Cain holding me in his arms and flying upwards."
    hide CG_Cain_Fall with dissolve
    p "What the-"
    n "I opened one eye and looked up at Cain."
    cain "You know, perhaps I was being a little hasty I threw you off the balcony."
    cain "I think I can still find a use for you."
    n " I wrapped my arms around his neck."
    p "Yeah whatever."
    $ cwings,cbase, cexp = 1,8,9
    n "Once we made it back up to the balcony, Cain saw it fitting to just roughly plonk me on the floor."
    p "OW! Come on, man..."
    n "I whined, rubbing my now aching bottom"
    n " He chuckled as his large wings receded into his back."
    $ cwings,cbase, cexp = 0,8,9
    cain "Why don't you get some rest."
    cain "I have a long day planned for you tomorrow."
    $ cwings,cbase, cexp = 0,8,1
    n "He stepped over me and walked back inside."
    n "I groaned."
    p "Oh great."
    p "I can't wait."
    n "I walked back inside and quickly moved to the bedroom."
    scene cain_bedroom_night with fade
    n "I jumped into his bed and covered my head hoping that I could sleep that night."
    scene black with dissolve
    jump cain_Morning_day2


label balcony_sex:
p "Hey what are you-"
n "I tried to ask, but was promptly silenced when he forced himself inside of me."
n "I remained motionless with my mouth agape as he continued to drill me."
p "St-stop."
n "I finally choked out."
$ cwings,cbase, cexp = 0,8,2
cain "Quiet."
n "I could feel his cock pull in and out while the scent of the ocean permeated the air."
cain "Ahh.."
$ cwings,cbase, cexp = 0,8,7
n "Cain grunted, pounding harder."
n "I put my hands on the railing to keep myself balanced."
p "Cain..."
n "I moaned as he tightened his grip."
n "My head buzzed from the relentless hammering of my insides."
cain "I...I'm going to cum!"
n "Cain grunted as he fucked me faster."
n "I began to pant as my whole body tensed up, his warm cum filling me."
n "I convulsed in ecstasy as I came with his final thrusts."
n "Cain released his hold on my neck and pulled himself out of me."
n "I fell to my knees, still clinging onto the railing."
n "I was too weak to stand."
n "Not after that."
$ cwings,cbase, cexp = 0,8,7
n "As I struggled to pull myself up, I felt something soft fall on my shoulders."
n "It was Cain's blazer."
n "I placed my hand on it for a moment before pulling it around me."
n "It was strange how warm and comforting it felt."
p "T-thank you."
$ cain_love +=10
n "I said in a timid and tired voice."
n "Cain waved his hand dismissively."
cain "Don't worry about it."
n "He offered me a hand and helped me to my feet."
n "I leaned on his shoulder and he placed a hand on my head."
n "The sound of waves was soothing. The feeling of Cain's shoulder was comfortable."
n "I began to nod off as he gently ran his fingers through my hair."
n "His soft voice interrupted the tranquil silence."
cain "Come on."
cain "Let's get you back inside."
scene black with dissolve
n "I wandered back inside with him and went straight to bed."
jump cain_Morning_day2



label cain_nightone_bathroom:
$ cain_love +=10
n "I reached for the door of the bathroom."
n "What was I doing?"
n "Was I actually going to go see him in the bathroom?"
n "I touched the doorknob and slowly opened the door."
scene cain_bathroom_night with fade
n "Cain wasn't in here but... "
n "The tub was full of water and there were wine glasses on the side."
n "I tilted my head and walked closer to the tub."
n "I felt a pair of heavy hands on my hips and jumped."
p "EEEK!"
n "I squeaked out as I turned around."
$ cwings,cbase, cexp = 0,1,1
show cain
cain "Why are you so jumpy?"
cain "It's just me."
$ cwings,cbase, cexp = 0,1,11
n "'You're exactly why I'm so jumpy,' I thought to myself as I crossed my arms."
cain "You shouldn't be so jumpy around me, I DO live here after all."
n "Cain said with a condescending tone that made me narrow my eyes."
cain "Like what you see?"
n "I opened my mouth to give him a witty response but I looked him over."
n "He was completely naked."
$ cwings,cbase, cexp = 0,1,9
p "AH. WHY ARE YOU-"
cain "Don't ask stupid questions."
cain "It's a bathroom and I want to take a bath."
n "He turned away from me and got into the bath himself."
n "I stared at him and he motioned to me."
cain "Come on."
n "It sounded more like a command than a request so I took off my clothes and gingerly got into the water with him."
n "Cain picked up a wine glass that was filled with a dark red liquid."
n "I watched him sip it and I cringed."
n "I wasn't sure what it was but it looked gross. "

menu:
    "\"What is that?\"":
        jump bath_what_is
    "\"What are you?\"":
        jump bathroom_what_are


label bath_what_is:
p "...What is that?"
n "I asked looking at the glass."
$ cwings,cbase, cexp = 0,1,1
cain "It's wine."
p "Why does it look like that?"
n "I scooted closer and he swirled it in his glass."
n "Cain pushed back his wet hair."
$ cwings,cbase, cexp = 0,2,13
cain "It's..."
n "He let out a dark chuckle and looked at me, his eyes piercing through me making me feel small again."
cain "Demon wine."
p "So like blood!?"
n "I said in a panicked voice."
cain "I'm not a vampire!!"
cain "It's made out of pomegranate and a few other ingredients."
cain "Want to try it?"
menu:
    "\"Yes.\"":
        jump bath_drink_yes
    "\"No.\"":
        jump bath_drink_no


label bath_drink_yes:
$ cain_love +=10
p "...Um. Okay."
n "He held up the glass and took a sip of it before shifting towards me."
n "He pushed his lips against mine and my eyes shot open."
n "I struggled and put my hands on his shoulders."
n "I tried to push against him but he was too strong."
n "I could feel the liquid filling up my mouth."
n "I swallowed it and it felt like my body was on fire."
p "AHH... What was in that..?"
n "My voice came out breathy and panting."
cain "Well..."
$ cwings,cbase, cexp = 0,2,13
n "Cain looked at my body and flicked my nipple."
n "I let out a loud moan and put my hands over my mouth."
n "He let out another loud laugh and licked his lips."
$ cwings,cbase, cexp = 0,2,24
cain "Looks like it works on you much faster than any demon."
n "He rubbed his hands down my sides and I felt my toes curling up."
n "His touch was making my head spin."
$ cwings,cbase, cexp = 0,2,16
n "He leaned into my ear and licked it, nipping softly."
n "I let out another moan."
cain "You feeling it yet?"
n "He whispered into my ear."
cain "I'm going to take what I want now."
$ cwings,cbase, cexp = 0,2,17
n "I quickly nodded my head as he stood over me."
n "I could feel myself orgasming as he pushed his cock inside of me."
cain "So soon? We're not done here."
n "Cain started to thrust in me faster."
n "I could hear the water splashing out of the bath."
n "He grabbed my shoulders and pushed my head under the water."
n "I could feel terror pulsing through my body."
n "I grabbed his arm as he held me down."
n "But he didn't let me up."
n "I felt bubbles of air leave my mouth and I smacked his arm twice."
if cain_love < 50:
    n "He let me go and I pushed my head up for air but I hit the top of the water like a wall."
    n "It felt like I was looking through glass as I put my hands against it."
    n "He started to thrust faster in me."
    n "My lungs filling with water."
    n "I could feel him cumming inside of me as everything went dark..."
    hide screen health_bar
    hide screen sanity_bar
    play music "cain/cain_death.mp3"
    $ persistent.cain_ending_drown = True
    scene endslate with Dissolve(1.0)
    screen cain_ending_drown:
        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}Cain drowned you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen cain_ending_drown
    with Dissolve(1.0)
    pause
    return
else:
    n "He let me go and I came up for air."
    cain "You're lucky I knew what you meant."
    n "I breathed hard, I didn't think he would let me up."
    p "Y-you can keep going if you want.."
    n "Cain put his hands on my hips again."
    $ cwings,cbase, cexp = 0,2,13
    cain "Don't mind if I do."
    n "He started to thrust again and I wrapped my arms around his shoulders."
    n "Cain put his lips against my shoulder and started to suck on the skin as he moved."
    n "I pulled my legs tight around him and he came inside of me."
    n "He nuzzled me."
    cain "You're fun, love."
    cain "Let's see if you can keep it up."
    n "He turned from me and I looked up at his back."
    scene CG_cain_Bath_Tattoo with fade
    n "His tattoo seemed daunting some how."
    n "I reached out and touched it."
    n "He looked over his shoulder at me."
    cain "Hm?"
    p "Your tattoo."
    scene cain_bathroom_night with fade
    show cain
    $ cwings,cbase, cexp = 0,2,13
    n "He grabbed my chin and leaned down."
    cain "It's not a tattoo."
    cain "It's a curse brand."
    n "He leaned in close."
    $ cwings,cbase, cexp = 0,2,6
    cain "Maybe if you're a good pet, I'll give you one too."
    n "He let go of my chin and put his hand out."
    cain "Come. Time for mortals to sleep."
    n "I took his hand and he pulled me out of the water."
    n "He wrapped a warm towel around me and nudged me towards the door."
    cain "Go I'm right behind you."
    n "I looked behind me as I wandered into Cain's bedroom."
    hide cain
    scene cain_bedroom_night with dissolve
    n "I laid down with the towel around me."
    n "I curled up and closed my eyes."
    n "I felt an arm circle my torso and I slipped into sleep."
    scene black with fade
    jump cain_Morning_day2

label bath_drink_no:
$ cain_love -=10
$ cwings,cbase, cexp = 0,2,25
$ cain_boredom += 1
n "I shook my head."
p "No thank you."
n "He shrugged and seemed to be uninterested in me."
n "Cain ran a hand through his hair pushing the wet spikes back."
$ cwings,cbase, cexp = 0,2,25
n "I kept my eyes on him but, something was bothering me."
n "I shifted uncomfortably as I felt the water boil around me."
p "AH.. WHAT THE FUCK!?"
$ cwings,cbase, cexp = 0,2,26
n "I swore as Cain put his hands out."
cain "You're boring me."
$ cwings,cbase, cexp = 0,2,6
n "I could feel my body getting dragged from one side of the tub to the other."
n "He wrapped his arms around me and held me down as I started to struggle."
n "My skin was turning red."
p "STOP!"
n "I shrieked as he watched my flesh."
cain "Why should I?"
cain "You're mine to do what I please with."
n "The hot water boiled around me and thrashed hard."
n "Cain's skin pristine and white against my red flesh."
n " I could feel blisters forming on me."
p "P..Please stop..."
n "Cain took one finger and pushed it into a blister popping it and causing my blood to squirt out from under the water."
n "I let out another shriek as he put my hands on his arms."
n "I could feel his finger poking around in the hole."
cain "Hm? What was that?"
$ cwings,cbase, cexp = 0,2,27
n "Cain dug his finger into my open sore."
p "PLEASE STOP..."
cain "I don't think so."
n "Cain snapped his fingers as black chains emerged from the water chaining my neck, wrists and legs down."
n "He got out of the water and leaned over the tub watching me."
n "I could feel my skin splitting and my blood flowing out of me as it filled the tub."
show CG_cain_Bloody_tub with dissolve
n "Everything was getting numb."
n "I couldn't feel the heat anymore, just blackness."
scene black with dissolve
cain "Well... That was interesting enough."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_boiled = True
scene endslate with Dissolve(1.0)
screen cain_ending_boiled:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain boiled you alive.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_boiled
with Dissolve(1.0)
pause
return

label bathroom_what_are:
cain "What am I?"
n "Cain mused on the question for a moment running a hand through his hair."
$ cwings,cbase, cexp = 0,2,27
$ sanity -=10
if sanity <= 0:
    jump cain_sanity_ending
cain "I'm a fallen angel."
cain "Cursed, really."
n "Cain said as he turned his back to me for a moment."
show CG_cain_Bath_Tattoo with fade
n "The large tattoo on his back flashed at me."
n "I put my hand on the black marks and ran my fingers down it."
p "Cain."
n "I muttered to myself."
cain "What?"
scene cain_bathroom_night
show cain
n "He responded gruffly as he turned around. "
p "Your name is really familiar."
cain "If you read anything about mythology."
cain "Perhaps you've heard about me."
p "Cain and Abel?"
$ cwings,cbase, cexp = 0,2,28
cain "Abel was my brother."
cain "He deserved what he got."
n "There was no remorse in his voice."
p "How old are you?"
cain "Ancient."
cain "It's just recently that I could do what I want."
menu:
    "\"Do you enjoy robbing the cradle?\"":
        jump bedroom_robbing
    "\"Recently?\"":

        jump bathroom_Recently

label bathroom_Recently:
$ cain_love -=10
$ cwings,cbase, cexp = 0,2,25
cain "Recently enough."
n "Cain looked at his nails and leaned back in the tub."
$ cwings,cbase, cexp = 0,2,28
cain "I was bound to hell."
cain "Cursed to be a torturer for all eternity."
cain "But, I broke out."
cain "I suppose you can say I like spitting in my captors faces and watching them struggle to find me and kill me."
n "Torturer for all eternity."
$ sanity -=10
if sanity <= 0:
    jump cain_sanity_ending
n "I felt my throat dry up."
cain "I suppose I should leave you to your bath then."
$ cwings,cbase, cexp = 0,2,6
n "Cain got out of the tub and tussled my hair as he went."
hide cain with dissolve
n "I sat in the water."
n " What would he do if he came back?"
n "I couldn't fight him..."
n "I started to breath hard and I got out of the water."
n "I might as well try to sleep."
n "I didn't want to be in here by myself, exposed as I was."
scene cain_bedroom_night with fade
n "I ran into the bedroom, which was empty and crawled under the blankets."
scene black with dissolve
jump cain_Morning_day2


label bedroom_robbing:
$ cain_love +=10
$ cwings,cbase, cexp = 0,2,29
n "He let out a hearty laugh and put his hand on my head."
cain "Only as much as you enjoy robbing the grave."
p "So none."
cain "You're pretty feisty for someone in your situation."
p "I ha-have to be."
p "I don't want to just roll over for you."
n "Cain seemed surprised and patted my head."
$ cwings,cbase, cexp = 0,2,30
cain "Why don't I leave you alone for the night."
cain " Enjoy your bath."
n "He climbed out of the bath."
n "He wrapped a towel around his waist and walked out of the bathroom."
hide cain
n "I leaned my head under the water a bit."
n "The warm water surrounding me."
$ health += 10
$ sanity += 10
n "It made me feel safe."
n "I only spent a few minutes by myself before I slipped out of the bathroom and into Cain's bedroom."
scene cain_bedroom_night with dissolve
show cain
n "He was laying down with his arms behind his head."
cain "Why don't you come here... and rob the grave."
$ cwings,cbase, cexp = 0,2,6
menu:
    "-Go over-":
        $ cain_love +=10
        $ sanity -=10
        if sanity <= 0:
            jump cain_sanity_ending
        n "I walked over and crawled on his lap."
        cain "Are you serious...?"
        $ cwings,cbase, cexp = 0,2,27
        n "I could feel his hand behind my neck as he pulled me down for a kiss."
        n "I leaned back and rubbed myself against him."
        n "I could feel his cock under the sheets and rolled my hips against him."
        $ cwings,cbase, cexp = 0,2,31
        cain "You're crazy."
        cain "Haven't I hurt you enough? "
        n "I heard him moan under his breath."
        $ cwings,cbase, cexp = 0,2,16
        p "Maybe I want you to hurt me..."
        n "I pulled the sheet away and rubbed myself against him."
        n "His arm shot out and he pushed his thumb into my mouth."
        $ cwings,cbase, cexp = 0,2,17
        cain "Why don't you use this instead?"
        n "I licked his thumb and let out a small moan."
        n "I moved away from his hand and leaned down."
        show CG_cain_ORAL
        n "His cock in my face."
        n "It smelled clean enough, I gave it a tiny lick and Cain grabbed my hair hard."
        cain "No teasing love."
        n "He said as he pushed my mouth on his cock."
        n "I opened my mouth as wide as I could and felt his cock in the back of my throat."
        n "I let out a little moan as he leaned over me and sent his hand into my ass."
        n "I moaned into his cock as he smacked me."
        scene cain_bedroom_night
        show cain
        cain "Little masochist..."
        n "He picked up a feather from his side table."
        $ cwings,cbase, cexp = 0,2,17
        cain "...How much of one are you?"
        n "He dragged the soft feather against my back and I choked."
        n "I wanted to scream or laugh but, it turned into a moan as I felt the feather's soft edge turn sharp."
        n "I could feel him cutting into my back."
        n "I looked up at him with tears in my eyes and he scratched the blade against my back again."
        $ cwings,cbase, cexp = 0,2,13
        cain "Oh? So you do like that huh?"
        n "He pushed deeper with the blade."
        n "I moaned loudly taking Cain's cock into the back of my throat."
        n " He suddenly thrusted forward and cut down my back."
        n "He was panting loud as he put his blade down and put his hands on my head."
        $ cwings,cbase, cexp = 0,2,16
        cain "Fuck..."
        n "He moaned as he pushed deep in my throat."
        n "I could feel his warm cum sliding down my throat."
        n "I pulled back coughing."
        p "You're so rough."
        $ cwings,cbase, cexp = 0,2,13
        n "He put his hand on my head and laughed."
        cain "Sorry."
        n "My back was aching but I felt okay about it. I nuzzled against him."
        n "He pressed his hand against my back wiping off the blood."
        cain "You're very interesting, love."
        p "...So are you... old man..."
        scene black with fade
        n "I closed my eyes and fell asleep on him."
        jump cain_Morning_day2
    "-Refuse-":

        $ sanity +=10
        $ cwings,cbase, cexp = 0,2,26
        $ cain_boredom +=1
        $ cain_love -=10
        if cain_boredom >=3:
            jump cain_boredom_day1
        p "I thought you were going to leave me alone."
        cain "Haha You caught me. Come here..."
        n "I felt a force nudge me towards him and I crawled on the bed."
        cain "You win."
        $ cwings,cbase, cexp = 0,2,13
        n "He said as I crawled to his side."
        n "I leaned my head on his shoulder and nuzzled him."
        n "He was so warm."
        $ cwings,cbase, cexp = 0,2,29
        n "I closed my eyes and leaned against him."
        scene black with fade
        n "I could feel myself falling asleep."
        jump cain_Morning_day2

label cain_Morning_day2:
screen phone_button_day2:
    imagebutton xpos 337 ypos 366:
        hover ("cain/phone_button_hover.png")
        idle ("cain/phone_button.png")
        action (Jump('damien_day2'))

$ enteredcain_bedroom_day2 = False
scene cain_bedroom_morning with dissolve
n "I looked around and got up."
n "I didn't see Cain anywhere."
scene cain_livingroom_morning with fade
n "I walked into the main room and looked around."
menu:
    "-Look in the kitchen-":
        jump day2kitchen_morning
    "-Look in the bedroom-":
        jump day2bedroom_Morning


label day2bedroom_Morning:
if damien_call_1 == True:
    scene cain_bedroom_morning_phone
    show screen phone_button_day2 
    with fade
    $ enteredcain_bedroom_day2 = True
    n "I headed back into the bedroom and looked around."
    n "Why did I even come back in here?"
    n "I let out a heavy sigh as I walked to the bed and took a seat."
    hide screen phone_button_day2
    jump day2noon
else:
    scene cain_bedroom_morning with fade
    $ enteredcain_bedroom_day2 = True
    n "I headed back into the bedroom and looked around."
    n "Why did I even come back in here?"
    n "I let out a heavy sigh as I walked to the bed and took a seat."
    jump day2noon


label day2kitchen_morning:
scene cain_livingroom_morning:
    subpixel True
    xalign 0.5
    easeout 0.9 xalign 0.95
n "I walked into the small kitchen area and looked inside the cabinets."
n "I was met with a drawer full of knives."
menu:
    "-Take knife-":
        n "I smiled to myself and grabbed one."
        jump cain_bedroom_stabattempt
    "-Leave-":
        $ cain_boredom +=1
        n "I looked over the knives and decided to leave them."
        n "I shut the drawer and walked off to the bedroom."
        scene cain_bedroom_morning with fade
        jump day2noon


label cain_bedroom_stabattempt:
n "I looked at the knife, it looked pretty sharp."
n "I gripped the handle tight and sneered."
n "Maybe if I got the drop on him I could take him down."
scene cain_bedroom_morning with fade
n "I walked softly towards Cain's bedroom and peeked into the door, he was sitting on the chair in his room with his back to the door."
n "I lit up and hid the knife behind my back as I tiptoed towards him."
n "I lifted the knife as my heart started to race."
n "NOW."
n "I brought my arm down on him but it stopped."
p "AH."
n "He didn't look up from his book as I could feel myself being thrown into the back wall."
scene cain_bedroom_morning with fade
$ cwings,cbase, cexp = 0,3,7
show cain
n "It felt like there was an invisible hand around my neck as I kicked my legs."
cain "You know... If you weren't so noisy you might have been able to stab me."
n "He got up and picked the knife off the floor."
n "Cain looked down the blade."
cain "This is pretty sharp isn't it?"
n "He snapped his fingers and my legs started to spread for him."
n "I gasped loudly trying to close them, but the pressure was too much."
p "AHHH LE-LET go.."
show CG_Cain_kitchenknife
n "Cain walked over to me waving the kitchen knife."
cain "I don't think so, darling."
$ cwings,cbase, cexp = 0,3,1
n "He poked the tip of the blade into my knee and I let out a soft whimper."
n "I didn't want to give him the satisfaction."
n "But, that feeling faded as he dragged the knife up my inner thigh."
n "I let out a loud cry as he dug in, he licked his lips as he watched the blood spill out of my leg and dropped the knife before he hit my groin."
cain "...Very sharp, indeed..."
scene cain_bedroom_morning with fade
show cain
n "Cain leaned down and licked the blood off my leg."
n "I gasped as his tongue hit the cut and he looked up at me."
menu:
    "\"GET OFF OF ME.\"":
        $ cain_love +=10
        $ cwings,cbase, cexp = 0,3,9
        cain "I don't think so.."
        n "Cain said as he bit down on my leg."
        $ health-=10
        n "I let out a cry as he bit me and sucked out my blood."
        n "I could feel myself getting light headed."
        $ cwings,cbase, cexp = 0,3,4
        $ sanity -=10
        if sanity <= 0:
            jump cain_sanity_ending
        n "He leaned up to me and pressed his lips against mine, pushing my own blood into my mouth."
        n "I wanted to scream..."
        n "Pull my head away..."
        n "But I couldn't."
        $ sanity -=10
        if sanity <= 0:
            jump cain_sanity_ending
        n "I gulped down my own blood and he dropped me on the floor."
        cain "Be careful with that knife."
        n "He stepped over my body and I curled up into a ball."
        hide cain with fade
        n "The door behind him slammed."
        n "I coughed lightly trying to get the blood taste out of my mouth."
        scene black with fade
        jump day2night
    "\"Stop, please...\"":

        $ cain_love -=10
        $ cain_boredom +=1
        if cain_boredom >=3:
            jump cain_boredom_day2
        cain "Stop?"
        $ cwings,cbase, cexp = 0,3,5
        p "...P-please stop.."
        n "I whimpered out."
        n "Cain rolled his eyes and dropped me on the floor."
        $ cwings,cbase, cexp = 0,3,7
        cain "You're pathetic."
        $ health-=5
        n "He put his foot on my head and pushed down."
        cain "I could just stomp you...."
        n "I let out a small cry as he pushed on my head."
        $ health-=5
        n "He kicked me in the face and I let out a scream as I felt blood drop out of my nose."
        n "He leaned down and grabbed my chin."
        $ cwings,cbase, cexp = 0,3,8
        cain "Tsk."
        cain "If you're going to be brave, you should stick to your guns."
        n "Cain tossed my head back and sent a hard kick into my stomach."
        cain "Stay on the floor where you belong."
        hide cain
        n "I curled up and cried softly to myself as I heard the door shut behind him."
        scene black with fade
        jump day2night
    "-Moan-":


        jump knifeattempt_moan

label knifeattempt_moan:
$ cain_love +=10
$ cwings,cbase, cexp = 0,3,11
cain "You liked that?"
n "Cain stared at me as I tried to keep my mouth shut."
n "Damn it."
n "Why did I?"
n "The pressure around my neck lightened a bit as I took another breath."
n "It tightened just enough to feel good."
p "Aaah."
n "I moaned softly as he rubbed the blood with his thumb."
$ cwings,cbase, cexp = 0,3,4
cain "You know, It's very alluring."
cain "You trying to kill me."
cain "Was that just foreplay?"
$ cwings,cbase, cexp = 0,3,9
n "He rubbed himself against me and I shook my head."
p "...I want.. I want you dead..."
p "I wanna leave..."
n "Cain unzipped himself."
cain "Really?"
$ cwings,cbase, cexp = 0,3,18
n "He pressed his cock against me and shut my mouth."
n "I didn't want to like this."
n "He pushed himself inside of me as I curled my toes in. "
n "I didn't want this."
$ cwings,cbase, cexp = 0,3,12
n "I let out a gasp as he pressed his lips against mine."
n "I could feel his tongue in my mouth."
n "Fuck it. "
$ sanity -=50
if sanity <= 0:
    jump cain_sanity_ending
n "I pushed my fingers through his red hair as he slammed me against the wall."
$ cwings,cbase, cexp = 0,3,9
p "I ha-hate you..."
n "I stammered out between breaths."
cain "I know."
n "He put his hands underneath my ass as he pushed into me hard."
n "I could feel my body tighten up as he grabbed a handful of my hair and pulled it."
p "F-FUCK..."
n "I felt myself orgasming as he came into me."
n "Cain laughed lightly as he placed me on his bed."
cain "You're different."
n "He patted my head and licked my blood off his hand."
cain "You can call me master if you want."
menu:
    "-Call him master-":
        $ cain_love +=10
        p "Fine. Master."
        cain "Good."
        n "He leaned in and nuzzled me."
        cain "Keep it that way."
        n "Cain got off the bed and walked away."
        hide cain with fade
        jump day2night
    "-Refuse-":

        if cain_boredom >=3:
            jump cain_boredom_day2
        $ cain_boredom +=1
        $ cwings,cbase, cexp = 0,3,5
        cain "HAHA... Suit yourself."
        $ cwings,cbase, cexp = 0,3,4
        n "He caressed my hair."
        cain "...I'll get you to say it... Soon."
        n "Cain got off the bed and walked away."
        hide cain with fade
        jump day2night



label day2noon:
    if damien_day2_call == True or enteredcain_bedroom_day2 == True:
        $ cain_love += 10
        n "I picked up my head at the sound of someone coming inside."
        n "Cain sat down next to me."
        $ cwings,cbase, cexp = 0,3,1
        show cain
        cain "Hello pet."
    else:
        n "I walked into the bedroom and saw the back of Cain's head."
        $ cwings,cbase, cexp = 0,3,1
        show cain
        n "He was sitting on the bed and he looked over his shoulder at me and put up his hand."
        cain "Come here pet."
        n "He said as I could feel myself being dragged across the ground."
n "He put his hand on my face."
if cain_love >70:
    cain "Why don't you start calling me master, love?"
    n "He said as he snapped his fingers."
    n "I could feel a leather collar snapping around my neck and my eyes widened."
    $ cwings,cbase, cexp = 0,3,4
    show CG_Cain_Leash
    cain "You look pretty in a little collar."
    n "I nibbled my lip and crawled over to him."
    p "...Y...Yes... Master."
    n "I said softly as I nuzzled his arm."
    $ cwings,cbase, cexp = 0,3,9
    n "Cain gently rubbed his hand against my head and I could feel a rush."
    n "It pounded in my skull and I could feel myself panting."
    n "I opened my mouth to say something but all that came out was a moan."
    cain "You like that, my lovely little kitten?"
    n " I could feel his hands through my hair as I leaned into his shoulder."
    n "He stroked my hair down to my lower back."
    n "He pushed his fingers inside of me."
    n "I let out a moan and looked up at him."
    $ cwings,cbase, cexp = 0,3,20
    cain "...You could have this all the time you know."
    n "I felt his fingers moving around inside of me as he pushed deeper."
    cain "Wouldn't you want to be my sweet kitten?"
    n "I let out a moan as he started to move his fingers faster."
    n "Every bit of his touch setting my body a light and making me pant and shake."
    n "I came on his hand and he leaned in kissing me hard."
    scene cain_bedroom_morning
    show cain
    n "I closed my eyes and let his tongue search my mouth."
    n "My head was spinning as his tongue played with mine."
    $ cwings,cbase, cexp = 0,3,10
    cain "...Think about it."
    hide cain with fade
    n "He stood up and left the room, leaving me feeling."
    n "Lonely."
    jump day2night
else:
    cain "Hm.."
    $ cwings,cbase, cexp = 0,3,5
    n "He looked at the walls of his bedroom as he snapped his fingers."
    n "Chains shot out of his wall as they grabbed my wrists."
    n "I struggled to get free."
    cain "You are unforgivably boring."
    n "Cain stood over me."
    n "The chains gripped me tight and pulled me on the bed."
    n "He put his foot in the middle of my chest and pushed down."
    cain "Ask me nicely to let you go."
    n "Cain said as he pushed into my sternum."
    menu:
        "-Ask for more-":
            jump cain_askformore
        "-Ask him to stop-":
            jump cain_asktostop

label cain_asktostop:
$ cain_love +=10
n "I bit my lip."
n "I didn't want to beg for my life."
n "I just wanted him to stop."
p "P-Please stop."
n "He gave me one swift kick into my chest." with vpunch
$ health -=5
$ cwings,cbase, cexp = 0,3,2
n "I could hear something in my chest crack."
n "I let out a loud scream and tried to put my hands on his shoe but the chains strung me tighter."
n "I could feel my arms pulling from their sockets."
n "They were holding on by just a small thread as I screamed again."
n "I could hear the joints popping and I cringed biting my lip."
$ health -=10
cain "Louder."
cain "I can't hear you from down there."
n "Cain mocked as he pushed down on my chest."
n "I was glad that the bed was soft and sunk me down."
n "If not, I'm sure he would have cracked more of my ribs."
$ health -=5
p "PLEASE LET ME GO."
$ cwings,cbase, cexp = 0,3,9
cain "Alright."
cain "Just cause you asked so nicely."
n "He dropped me on the bed as I held my arms."
n "I pulled and huddled up keeping all my limbs close to me."
n "He flicked my forehead and walked away from me. "
hide cain with fade
jump day2night

label cain_askformore:
n "I looked at him and he cocked his head to the side."
p "I want more.."
n "I said, hoping it would make him happy."
$ cwings,cbase, cexp = 0,3,9
cain "Oh? You want me to be rough?"
n "He said as he gripped his hand."
n "I could feel chains hook around my ankles."
cain "Let's play a game then.."
n "Cain put out his hand as the chains stretched me out."
n "I felt my limbs stretching tight as I looked up at him."
$ health-=10
n "The metal was digging into my wrists. "
cain "Want more hm?"
n "Cain put out his hand and my limbs tugged up above my head and my legs pulled down."
$ health-=10
n "I screamed as loud as I could as he pulled my limbs."
cain "...Do you know what a rack is?"
n "My joints started to pull at the seams."
n "I could feel my muscles pull apart and I looked up at him."
$ cwings,cbase, cexp = 0,3,12
$ health-=10
p "Please... please stop."
n "I begged as the chains slowly pulled me apart."
cain "Stop? Why would I want to do that?"
$ health-=20
cain "You asked so nicely for more."
$ health-=20
$ sanity-=20
n "I could hear something creaking in my limbs."
$ health-=20
$ sanity-=20
n "I sobbed as Cain stood to the side watching me."
$ health-=20
$ sanity-=20
n "I heard a loud crack as pain shot out from all of my limbs."
$ health-=20
$ sanity-=20
n "I could feel my bones breaking under the stretch of the chains."
$ health-=20
$ sanity-=20
n "I felt my body convulsing and Cain's loud laughter filled my ears."
$ health-=20
$ sanity-=20
cain "HAHAH You won't be needing those anymore."
$ health-=20
$ sanity-=20
n "Cain said as I could feel my limbs quickly being torn from their spots."
n "My blood flew into the air as I went cold..."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_rippedapart = True
scene endslate with Dissolve(1.0)
screen cain_ending_rippedapart:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain ripped you apart.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_rippedapart
with Dissolve(1.0)
pause
return

label day2night:
    if cain_love >=90:
        jump cain_nighttwo_livingroom
    else:
        jump cain_nighttwo_sleep
label cain_nighttwo_sleep:
n "I didn't want to do anything."
n "I just wanted to sleep."
n "I laid down in his bed and closed my eyes."
jump cain_day3

label cain_nighttwo_livingroom:
scene cain_livingroom_night with fade
play music "cain/cain_calm.mp3"
$ cain_hideheart= False
n "I decided to go to the living room and looked around."
n "There wasn't really anything I could look at."
$ cbase, cexp = 9, 3
n "Except, I pulled out an easel from the corner and looked at it."
show cain with fade
cain "Are you going to paint?"
n "Cain asked as he came in from the balcony."
menu:
    "\"Yes.\"":
        $ cain_love +=10
    "\"No.\"":
        $ cain_boredom +=1
        if cain_boredom >=3:
            jump cain_boredom_day2
        cain "Too bad."
        n "I put the easel back and walked into his bedroom."
        n "I didn't want to do anything. I just wanted to sleep."
        n "I laid down in his bed and closed my eyes."
        jump cain_day3

p "Do you have anything for it?"
cain "I only have black paint."
n "I nodded my head."
p "That's okay."
n "He opened the closet and pulled out a canvas for me."
n "He put a toolbox next to the easel and I opened it."
n "It was full of fancy unused brushes and a bottle of black paint."
menu:
    "\"Do you paint?\"":
        $ cbase, cexp = 9, 22
        cain "No, I never had a talent for it."
    "\"You never used these.\"":

        $ cbase, cexp = 9, 22
        cain "I don't have a talent for painting."
    "\"Thank you.\"":

        $ cbase, cexp = 9, 23
        cain "Of course, I would like to see what you can do."

$ cbase, cexp = 9, 3
n "I picked up a brush and dipped it into the black ink."
n "I just wanted to paint something.. anything to take my mind off of my situation."
n "Cain took a seat on his couch watching me."
cain "Have you studied art before?"

menu:
    "\"At school.\"":
        cain "Respectable."
        p "If you like school."
        cain "Having instruction isn't usually something someone likes."
        $ cbase, cexp = 9, 22
        cain "Especially if it feels like your instructor is belittling your intelligence."
        $ cbase, cexp = 9, 3
    "\"A bit.\"":

        cain "It's better than nothing."
        p "Ignorance is bliss sometimes."
        cain "That depends on your definition of bliss."
        cain "Sometimes ignorance, especially of others, can cause misfortune."
        p "Walking into the wrong person in a cafe for instance."
        $ cbase, cexp = 9, 23
        cain "Exactly."
    "\"Just what I learned online.\"":

        $ cbase, cexp = 9, 23
        cain "Self taught knowledge can be admirable."
        $ cbase, cexp = 9, 3
        cain "You can't really trust everything you read."
        cain "Especially online."
        p "A person can lie to you just as well as anything online."
        cain "True."

$ cbase, cexp = 9, 3
cain "Any knowledge is power, my dear."
cain "You just need to know how to seek it out."
p "These days it's not so hard to find information about anything really."
p "You just need a computer."
n "I just watched my hand move as I painted."
cain "An old man like me?"
cain "I barely know how to use the internet"
cain "My knowledge comes from experience."
cain "And I have many years of experience."
p "Sounds eternal."
cain "It can be."
p "\"Midway upon the journey of our life\""
p "\"I found myself within a forest dark,\""
cain "\"For the straight forward pathway has been lost.\""
cain "The Inferno, Dante's divine comedy."
p "This situation that I find myself in isn't far from a divine comedy in it's own rights."
cain "I wouldn't call it divine."
p "You know what I mean."
cain "I suppose so."
p "What was it like?"
p "Working as a torturer?"
cain "It was supposed to be my punishment."
cain "However, do one thing long enough and you acquire a taste for it."
p "It can also grow stale."
cain "I won't deny that."
cain "You do get to see things that many people do not."
cain "Such as, this scene, I haven't seen personally in a while."
menu:
    "\"A human in your house?\"":
        cain "Someone painting."
        p "Lots of people paint."
    "\"Painting?\"":
        cain "Yes."
        p "Lots of people paint."
    "\"Someone else around you?\"":
        $ cbase, cexp = 9, 22
        pause(0.5)
        cain "Yes."
        $ cbase, cexp = 9, 3
        cain "Being bound to hell isn't usually jovial."
        p "I'm glad I can amuse you with my painting."
        cain "I like it."
        cain "I haven't seen someone paint in a long time."
        p "Lots of people paint."

cain "Many people paint on computers."
cain "I prefer watching people paint on a canvas."
cain "You don't have the luxury of just pressing the back button to delete a mistake."
cain "Or the world of your art at the click of a button."
cain "It's to easy to be rid of something you had done."
cain "The canvas is much more like the soul."
cain "You can't just erase what you've done."
cain "You just have to paint over it or accept it for what it is."
cain "I'd rather see everything than be rid of it in the blink of an eye."
p "Are you really one to talk?"
p "You're an angel."
p "You're supposed to be perfect."
$ cbase, cexp = 9, 22
cain "Hm?"
$ cbase, cexp = 9, 3
cain "I'm a fallen angel, I AM supposed to be what's wrong with the waking world."
cain "I was human once, just like you."
p "Then what happened?"
cain "I killed my brother."
n "He had no remorse in his voice."
n "Cain seemed to be proud of it."
menu:
    "\"Because you were evil and your brother was good.\"":
        cain "According to who?"
        cain "Who's the real judge of that?"
        p "Anyone with morality."
        cain "Morality is fleeting."
        cain "I just do things that are enjoyable."
    "\"Did you enjoy it?\"":
        cain "Perhaps."
        p "Not sure?"
        cain "I have a different way of thinking than I did back then."
        cain "What is enjoyable now, wasn't enjoyable back then."
        p "So no?"
        cain "Now I didn't say that."
        cain "Perhaps it was enjoyable for a different reason."
        cain "Being rid of a nuisance could be a reason enough to enjoy it."
    "\"How'd it feel?\"":
        cain "It was fun or so I vaguely remember."
        cain "It's been a long time."
        p "How does it feel to kill anyone?"
        cain "To me?"
        cain "It's boring."
        cain "You know I had an apprentice once."
        p "You trained someone?"
        cain "He was already a doctor, I just helped him out a bit."
        cain "Gave him a new pretty blue eye."
        p "You helped someone?"
        cain "Don't sound so incredulous."
        p "He must have been special to you."
        cain "He was, he still is."
        cain "Sano Kojima..."
        p "You almost sound like you're in love with him."
        cain "Would that be so far-fetched?"
        p "I just wasn't aware that was a feeling you could have."
        cain "You have much to learn about me yet."

p "What do you enjoy doing?"
cain "This."
p "What's that?"
n "I felt his hands on my hips."
n "I didn't let go of the brush."
n "I didn't want to think about what he was doing to me."
n "But I let out a gasp as he touched me."
cain "Pain was all I delivered for many centuries."
p "You think this isn't painful?"
p "Being trapped here?"
n "I watched Cain's fingers dip into my paint and I felt him drag the black ink across my side."
n "I let out a shuddered breath and tried to keep my mind away from what he was doing."
n "He tugged off my underwear and I shifted my hips, lifting them up for him."
n "Why was I just doing what he wanted...?"
cain "I can make it less painful for you."
n "Cain lifted my hips up to his waist."
n "I felt him against me."
p "How would that make it less painful?"
p "You're just doing what you want now."
cain "Shouldn't we all?"
n "Cain leaned over and whispered in my ear."
cain "In fact you're doing something you want right now."
p "Not yet I'm not."
n "I flicked my butt upward, rubbing his cock hard with my ass causing him to moan softly."
$ cbase, cexp = 9, 33
cain "I enjoy your honesty."
n "Cain moved his hand and pulled himself out of his pants."
n "I went to put my paintbrush down but Cain grabbed my hand."
cain "Don't. Keep painting."
n "He commanded and I nodded."
n "I kept my brush on the canvas and tried to move it."
n "I watched Cain's black stained hands move across my stomach, leaving ink all over my body."
n "I tensed up as he pushed his cock inside of me."
n "I let out a loud cry, but I started to moan as I gripped the paint brush."
n "I wasn't even moving it anymore."
n "I felt his thick cock move inside of me and gripped the easel."
p "H-harder."
n "I begged as I grit my teeth."
cain "Oh... demanding."
cain "I like that."
show wings cain behind cain with dissolve
n "He said as black wings burst from his back."
n "I watched the feathers move near me and I leaned into the wing, nuzzling the soft feathers as he pushed inside."
n "Fucking me harder as I had asked."
n "I dropped the paintbrush on the ground as he fucked me from behind."
$ cbase, cexp = 9, 34
p "Cai-cain..."
n "I moaned out as he started to move faster."
n "He gripped my hips and came inside of me leaning into the back of my neck and kissing my skin."
$ cbase, cexp = 9, 3
cain "...I like your painting."
n "He growled into my ear."
n "I looked up at the painting my eyes widening."
n "I slipped to the ground just looking up at the painting."
hide wings cain with dissolve
hide cain with dissolve
show CG_CainPainting
p "What is this..."
n "I said to myself not realizing that Cain had already left my side."
n "I collected myself and went to the bedroom to go to sleep."
jump cain_day3

label cain_day3:
    if cain_love <100 and damien_day2_call == False:
        jump cain_badending

    if cain_love >=100 and damien_day2_call == False:
        jump cain_good_ending_fallen
    else:

        scene cain_bedroom_morning
        menu:
            "-Look for phone-" if damien_day2_call == True:
                jump damien_day3
            "-Stay in bed-":

                n "I closed my eyes and went back to sleep."
                jump cain_badending

label cain_badending:
$ sam_name = "???"
scene sam_bedroom with fade
play music "cain/sam_main.mp3"
n "I opened my eyes and looked around."
n "I was back home!"
n "What happened?"
n "Maybe everything that just happened was a dream?"
n "I sat up and felt a pain shooting in my side."
p "OW!"
n "I looked down at my side and it was bleeding through the sheet."
n "My heart started to race as I looked at myself."
n "I was still naked and covered in injuries."
p "..N-no..."
n "I whispered as turned my arm over."
n "That cross and wings."
n "I saw it at Cain's house."
n "But, why was I home?"
sam "Excuse me."
n "An unfamiliar voice called to my side."
$ sbase, sexp, sglass = 1,1,1
show sam
n "I felt a cold sinking feeling as I slowly turned my head towards the man to my side."
n "It felt like an ice cold bucket of water was dumped over my head as the man approached me."
n "My blood felt cold as he leaned into me"
sam "Do you know who I am?"
n "He asked me in a low dark droll."
n "I sat up straight, any pain or embarrassment shut down by his voice."
n "I opened my mouth to speak but, I couldn't say anything."
n "I shook my head."
n "He sighed and pushed up his glasses."
sam "I didn't think so."
sam "My name is Samael. I'm here to take you."
$ sam_name = "Samael"
$ persistent.character_unlock_sam = True
p "Take me?"
n "I croaked out finally."
sam "Your life."
sam "Your time is up."
p "N-No wa-wait!"
n "I stammered out putting out my hand trying to push him away."
$ sbase, sexp, sglass = 1,2,1
n "Samael grabbed my arm and looked at the mark on it."
n "His red eyes narrowed."
$ sbase, sexp, sglass = 1,1,1
sam "...What's this?"
p "I.. I don't know I think Cain-"
sam "...That's all you need to say."
n "He put my arm down."
n "He put out his hand as the room dropped colder."
n "My toes and fingers started to tingle. "
sam "I was going to take your life, but..."
show sam_ice1_anim
show sam_ice2_anim
show sam_ice3_anim
show sam_ice4_anim
$ health -=100
n "Sam gripped his hand and large ice spikes pushed through my skin."
n "I let out a loud scream as the cold spears pierced my flesh."
n "I coughed blood on the ice as I gripped the spikes."
n "I tried to pull myself away but I was getting weak."
sam "You're going to Judecca, I have some questions for you."
n "I started to sink into the floor."
n "He put his boot against the bridge of my nose."
show CG_sam_ending with dissolve
sam "You don't need to be awake for this part."
n "He smashed my nose in."
n "I could feel myself slipping into unconsciousness as a wave of cold blackness overcame me."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_traitor = True
scene endslate with Dissolve(1.0)
screen cain_ending_traitor:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain abandoned you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_traitor
with Dissolve(1.0)
pause
return


label cain_good_ending_from_damien:
$ cwings,cbase, cexp = 0,3,16
play music "cain/cain_sexy.mp3"
cain "...I don't want to let you go."
n "Cain said softly into the top of my head."
n "I clutched him close to me and bit my lip."
$ cwings,cbase, cexp = 0,3,10
p "I don't want to leave you master, please don't get rid of me."
n "I begged, I knew what his original intentions were."
n "He wanted me to die but..."
cain "I have a proposition for you."
n "Cain spoke directly into my ear and touched my hair lightly."
n "I quivered and nodded my head that I was listening."
$ cwings,cbase, cexp = 0,3,20
cain "Stay here, I'll make you a demon and you can be my precious pet forever."
cain "How does that sound?"
n "I looked to the side and thought for a moment."
p "...Okay."
n "I finally said as he put his hands on my hips."
cain "Good."
n "He pushed his lips on mine."
$ cwings,cbase, cexp = 1,3,21
n "I could feel my body getting hotter."
n "Was he killing me?!"
n "My knees started to feel weak."
n "This wasn't a normal heat."
n "I felt my body shifting under his hands. "
cain "What are you going to become?"
cain "A sex demon?"
cain "Cyclops? Oni?"
cain "Let's find out together."
n "He said as he watched me shift."
n "I could feel an aura coming off of him that made me pant and go bleary eyed."
n "I gripped his blazer."
show CG_FallenAngel_Cain with dissolve
n "Were those... horns...?"
n "And a tail?"
n "Something about the sight of him like this made my heart race."
n "He put his hand on my head and I could feel a wave of pleasure hit me as the final stages of my transformation hit."
cain "There you go my sweet little demon."
cain "You're mine now."
p "Yes master!{image=icon_heart.png}"
hide screen health_bar
hide screen sanity_bar
$ persistent.cain_ending_demon= True
scene endslate_clean with Dissolve(1.0)
screen cain_ending_demon:
    text "{=endslate_title}You Survived!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain made you into a demon.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_demon
with Dissolve(1.0)
pause
return

label cain_good_ending_fallen:
scene cain_bedroom_morning with fade
n "I woke up and looked down at myself."
n "I was clothed."
n "These weren't my usual clothes but I didn't mind."
n "It was nice to be covered for once."
scene cain_livingroom_morning with fade
n "I slid out of bed and wandered into the living room, Cain was sitting reading again."
$ cexp = 3
show cain with dissolve
p "What are you reading?"
n "I asked placing my chin on his shoulder, there were a lot of words I didn't understand."
cain "Can you read it?"
p "Not really."
cain "I wouldn't expect you to understand it at any rate."
cain "It's all magic."
n "I paused."
p "What are you looking up?"
n "Cain sighed and closed the book."
$ cexp = 22
cain "Something important."
p "That being?"
$ cexp = 3
cain "When did you get so inquisitive?"
p "When you answered all my questions last night."
cain "What a mistake."
n "He joked and I cocked an eyebrow at him."
n "Cain forced my arms around him and leaned into my embrace."
n "He took a deep breath."
cain "You're trapped here."
p "I know. You're keeping me here."
cain "Even if I didn't keep you here, the world has marred you."
cain "It's like wading through blood, there's no chance of you leaving without someone noticing it."
p "What do you propose we do about it?"
$ cexp = 32
cain "We..."
$ cexp = 3
n "He mused on my words as his own thoughts floated through his head."
cain "I have a proposition for you."
p "That being?"
cain "You can stay here of your own free will or die out there."
p "Doesn't sound like I've got much of a choice."
cain "No. You don't."
cain "But, it's a choice I want you to make on your own."

menu:
    "\"I'll stay here.\"":
        jump cain_goodending_fallen2
    "\"I'll go.\"":

        cain "Good luck out there."
        p "...Yeah."
        n "I pushed off of him and walked out of his home."
        n "He didn't follow me."
        scene black with fade
        n "Where was I going?"
        n "I wandered for a long time."
        hide screen health_bar
        hide screen sanity_bar
        play music "cain/cain_death.mp3"
        $ persistent.cain_ending_wander= True
        scene black with Dissolve(1.0)
        screen cain_ending_wander:
            text "\n\n\n\n{=endslate_subtitle}You wandered forever.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen cain_ending_wander
        with Dissolve(1.0)
        pause
        return

label cain_goodending_fallen2:
cain "Smart of you."
p "I try."
n "I leaned my head against Cain's and played with the collar on his shirt."
p "So, what now?"
p "Do I become your loving spouse or something?"
cain "What about my second in command?"
n "I paused and looked at him."
p "What do you mean?"
cain "You must have felt it."
cain "You have a darkness in you, just waiting to come out."
cain "You didn't have to think to paint a picture of you destroying angels."
cain "That just came naturally to you."
cain "Life can be easier with someone watching your back."
p "And you chose me to do it?"
p "What if I just betray you?"
cain "You won't."
p "You don't know that."
n "Cain grabbed the front of my top and dragged me into his lap."
n "I hit his legs with a thump and looked up at him."
cain "I do know it."
cain "Your carnal desires, your subconscious thoughts, they all lead to one place."
n "He put his hand on my thigh and moved it upwards."
n "I cursed, wishing that I had been naked now."
cain "Right here."
cain "With me."
n "I lifted my body towards his as he moved his hands around my back, fiddling with the bottom of my top."
p "Don't play with me."
cain "I don't play."
cain "You say that as if I have a sense of innocence to play."
n "I shifted my weight, straddling him between my legs."
n "He rubbed his hands on my thighs."
n "I rubbed my crotch against his trying to feel him."
p "What do you want me to do?"
cain "Have sex with me."
n "I cocked my head to the side and rested my hands on his shoulders."
p "You're asking me?"
cain "I need your consent."
p "You didn't before, what makes this time different?"
cain "It'll be different."
p "You just sit there then."
n "Cain's eyes widened as he looked up at me."
p "I'll do it."
n "I opened his pants and reached down to his cock, stroking it between my hands."
n "It pulsed and I smiled."
p "How's this for consent?"
n "He bit his bottom lip watching my hand move."
p "I will have sex with you."
$ cexp = 33
p "Whether I have to take it or not."
n "I pushed my bottoms from my hips and tossed them away."
n "He put his hand behind my neck and pressed his lips against mine."
n "I positioned myself over him looking down at his throbbing cock."
n "I asked for this, I needed it."
n "I pushed myself down on him and he let out a low grunt as I did."
n "He took my hands into his hand, I stabilized myself on him."
n "I moved my hips, making sure he felt every inch of my movement."
$ cexp = 34
n "He closed his eyes and rocked himself inside of me."
p "Cain."
show CG_Cain_goodEnding with dissolve
n "I whispered out as I leaned my forehead against his."
n "His body against mine."
n "He was squeezing me so tightly, like he wasn't going to let me go."
n "I didn't care, he was my world now."
n "I felt his body heat up quickly and I squeezed around him."
n "I felt his warm cum fill me up and something different."
n "Small black feathered wings sprouted from my back only enough to circle my shoulders."
n "I forced my hips down as I came over him, panting hard."
$ cexp = 33
n "The new wings fluttered with excitement as Cain reached out to touch them."
cain "They'll grow as you get stronger."
n "Cain's tone, soft, panting, more tired than I ever heard him after sex."
n "I looked at them then back to him."
n "I wrapped my arms around his shoulders."
n "I felt... free."
hide screen health_bar
hide screen sanity_bar
$ persistent.cain_ending_fallen= True
scene endslate_clean with Dissolve(1.0)
screen cain_ending_fallen:
    text "{=endslate_title}You Survived!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain saw your value.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_fallen
with Dissolve(1.0)
pause
return


label cain_boredom_day1:
n "Cain sighed and shook his head."
cain "Don't you have anything better to say?"
cain "You sound so weak."
n "He grabbed my face and forced my mouth open."
cain "You won't be needing this."
cain "You have nothing good to say anyways."
n "He pulled my tongue out of my head and punched my jaw into it."
$ health-=50
n "I could feel my teeth sinking into the soft muscle severing it from my mouth."
n "I wanted to scream or cry, but all I could feel was blood pooling in my mouth."
n "I let out a scream, that came in gurgles and blood."
n "Cain looked at my tongue and tossed it away as he pushed me on the ground."
n "The pain was unbearable."
$ health-=50
n "I could feel myself fading as I looked up at Cain."
cain "You brought this on yourself, you boring creature."
n "I felt my eyes getting heavy."
n "The blood was pooling in my mouth and Cain wouldn't let me spit it out."
n "He kept his hand over my mouth as I blacked out."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_bordom1= True
scene endslate with Dissolve(1.0)
screen cain_ending_bordom1:
    text "{=endslate_title}You died.{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain got bored.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_bordom1
with Dissolve(1.0)
pause
return


label cain_boredom_day2:
n "Cain sighed and shook his head."
cain "Still fighting after all this time?"
cain "It seems as though I can't break you."
n "He grabbed my face and forced my mouth open."
cain "You won't be needing this."
cain "You have nothing good to say anyways."
n "He pulled my tongue out of my head and punched my jaw into it."
$ health-=50
n "I could feel my teeth sinking into the soft muscle severing it from my mouth."
n "I wanted to scream or cry, but all I could feel was blood pooling in my mouth."
n "I let out a scream, that came in gurgles and blood."
n "Cain looked at my tongue and tossed it away as he pushed me on the ground."
n "The pain was unbearable."
$ health-=50
n "I could feel myself fading as I looked up at Cain."
cain "You brought this on yourself, you boring creature."
n "I felt my eyes getting heavy."
n "The blood was pooling in my mouth and Cain wouldn't let me spit it out."
n "He kept his hand over my mouth as I blacked out."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_bordom2= True
scene endslate with Dissolve(1.0)
screen cain_ending_bordom2:
    text "{=endslate_title}You died.{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You couldn't be tamed.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_bordom2
with Dissolve(1.0)
pause
return

label cain_sanity_ending:
n "I felt the world around me shift into blackness as I watched Cain's eyes, they seemed to be the only thing breaking through the dark haze of my mind."
scene black with fade
play music "cain/cain_sanity_ending.mp3"
n "When I came to I looked up at a large blade hanging above my head."
n "Perched still in the darkness, the only thing I could see was the razor sharp blade."
show CG_cain_sanity_ending with dissolve
n "I went to move but I felt my arm lock in place by a rusted shackle."
n "The cold sweat collecting on my brow as I panicked."
cain "\"Impia tortorum longas hic turba furores Sanguinis innocui, non satiata, aluit.\""
n "I heard Cain's voice ring out in the empty and desolate halls of the chamber I was trapped in."
cain "It feels almost trite that I'd be using this method to finish you."
cain "But, your mental state isn't in the best of health."
cain "Perhaps the literary beauty of this moment is wasted on you."
show CG_cain_sanity_ending_move with dissolve
n "I watched the blade swing above my head."
n "It only seemed to be moving back and forth, at first."
n "The blade's rhythmic swings almost hypnotizing."
cain "It's not wasted on me."
cain "I'll watch you suffer, no matter how long it takes."
n "Cain's deep laugh rang through the darkness as I watched the blade come for me."
n "He didn't say anything more, I only listened to the sound of the rushing blade."
n "The darkness only bred a cold longing for anything."
n "Anything but that blade."
n "By the time it reached me."
$ health-=100
n "I was begging for the release it would bring."
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_sanity= True
scene endslate with Dissolve(1.0)
screen cain_ending_sanity:
    text "{=endslate_title}You died.{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain left you in the pit.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_sanity
with Dissolve(1.0)
pause
return


image cain_cloud1 = "cain/cloud.png"
image cain_cloud2 = "cain/cloud2.png"
image damien_bedroom = "cain/damienbedroom.png"
image cain_cloud1_animation:
    "cain_cloud1"
    yalign 0.5
    easein 0.75 xalign 0.2
    easeout 0.75 xalign 0.5
    easein 0.75 xalign 0.8
    easeout 0.75 xalign 0.5
    repeat
image cain_cloud2_animation:
    "cain_cloud2"
    yalign 0.5
    easein 0.75 xalign 0.3
    easeout 0.75 xalign 0.5
    easein 0.75 xalign 0.7
    easeout 0.75 xalign 0.5
    repeat

label damienday1:
$ damien_name = "???"
n "I walked over to Cain's side table and looked at the phone."
n "It started to ring, I squeaked and picked it up."
hide screen phone_button
p "...Hello?"
n "I whispered into the receiver."
n "The black screen lit up with the image of a man."
n "It must have been the guy calling."
scene damien_church
play music "cain/damien_church.mp3"
show damien
$ dbase, dexp = 3,3
damien "CAIN I SWEAR TO GOD..."
damien "STOP SENDING ME WEIRD PICTURES. "
$ persistent.character_unlock_damien = True
menu:
    "-Hang up-":
        scene cain_bedroom_morning
        n "I hung up."
        n "That guy sounded really angry."
        n "I put the phone back down."
        n "I really shouldn't mess with that stuff."
        n "I headed back out into the living room."
        jump cain_night_1
    "\"I'm not Cain.\"":

        $ damien_call_1 = True
        p "...I'm not... Cain."
        n "I said a bit louder."
        $ dbase, dexp = 3,4
        n "The angry guy stopped growling and looked at the phone."
        $ dbase, dexp = 3,1
        damien "What?"
        $ dbase, dexp = 3,5
        damien "What are you doing on his phone?"
        p "I don't know what I'm doing here."
        p "I-I'm scared."
        n "He paused for a moment, thinking."
        $ damien_name = "Damien"
        damien "My name is Damien."
        damien "Please try to calm down and speak quietly."
        n "I could hear the desperation in his voice."
        p "I was at a cafe and woke up here."
        $ dbase, dexp = 3,2
        n "Damien made a sound of frustration."
        damien "Tsk! This typical bullshit..."
        n "I wasn't the first one."
        $ dbase, dexp = 3,1
        damien "If you can please call me back tomorrow on this phone."
        damien "I want to help you but I don't have all my tools to track the call."
        damien "What's your name...?"
        p "My name is %(player_name)s."
        damien "I'm going to do my best... Okay?"
        damien "I want you out of there safe."
        scene cain_bedroom_morning
        hide damien
        n "I nodded and looked at the door."
        p "I have to go...."
        n "I panicked into the phone and hung up."
        n "I quickly deleted the recent call and put the phone back on the table."
        n "Cain opened the door and I laid down on his bed."
        $ cwings,cbase, cexp = 0,3,1
        play music "cain/cain_shift.mp3"
        show cain
        cain "...What are you doing in here?"
        p "...I'm just... laying on your bed. "
        cain "Alright."
        cain "I thought I heard you talking to yourself."
        cain "Perhaps I was mistaken."
        hide cain
        n "Cain walked out of the room."
        n "That was close..."
        n "Was Damien really going to help me?"
        n "I wondered if I could trust him..."
        jump cain_night_1

label damien_day2:
$ aed_name = "???"
hide screen phone_button_day2
n "I looked at the phone on the side table."
n "Did I really want to make Cain angry? "
n "What if he found out?"
n "I wasn't even sure if he was home."
n "I picked up the phone, this was my only life line out."
n "I shook as I looked through Cain's address book."
n "Damien... "
$ damien_day2_call = True
n "The phone rang and I put it up to my ear."
damien "What do you want?"
n "A grumpy voice came through the other side."
p "It... It's me..."
n "He gasped and I could hear a bunch a clambering sounds."
damien "Hey %(player_name)s."
damien "Stay on the line with me a little bit huh?"
n "Damien said as he turned on his face cam."
$ dbase, dexp = 2,1
scene damien_church
show damien
play music "cain/damien_church.mp3"
$ dbase, dexp = 2,6
n "He seemed relieved to see my face."
p "Hey."
p "Tell me a bit about yourself."
p "So we're not sitting and staring at each other huh?"
n "I stammered out."
$ dbase, dexp = 2,1
n "Damien set himself in front of the camera."
damien "I dunno what you want me to tell you."
damien "I'm a priest and Cain-"
damien "-is my half-brother."
$ dbase, dexp = 2,2
damien "I hate him though."
damien "He's not beyond doing this stuff to people."
$ dbase, dexp = 2,1
n "Damien motioned at me."
damien "That's why I need to get you out of there."
$ dbase, dexp = 2,7
n "Could I trust him not to tell Cain?"
n "They were brothers after all."
$ dbase, dexp = 2,1
damien "...Cain isn't know for his brotherly love."
damien "This is still true."
damien "He's tried to kill me on several occasions."
n "Maybe it was the look on my face but..."
p "Did you read my mind?"
$ dbase, dexp = 2,6
n "Damien laughed and tilted his head to the side."
damien "If I could read your mind, it'd probably be a lot easier to find you."
p "True."
$ dbase, dexp = 2,1
n "Damien went quiet for a moment."
damien "Trust me... I am trying to save you."
n "I felt my heart calm down and I nodded."
damien ".D write down these coordinates."
show damien:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show d 4:
    subpixel True
    xalign 1.0
    ypos 70
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0 xalign 0.9
n "Damien started to speak in a commanding tone to someone."
$ aed_name = ".D"
$ persistent.character_unlock_aed = True
d "Got it."
damien "We're gonna see you soon... We'll get you out."
n "Damien said as he reached out to the camera."
n "I closed my eyes and could feel myself crying."
damien "You'll be okay soon."
p "Okay."
n "Something about his voice."
n "Told me everything was going to be okay."
damien "Good. Tomorrow."
damien "I'll be there. Hold out."
play music "cain/cain_shift.mp3"
scene cain_bedroom_morning
n "I nodded and Damien hung up the phone."
n "I put it back on the side table and curled up on Cain's bed."
jump day2noon

label damien_day3:
n "I stayed in the bedroom and looked at the phone."
n "Maybe Damien wasn't coming back for me."
n "I sighed and sat down on Cain's bed with my knees up."
n "I could feel something.... different."
p "...Hello?"
n "I called out softly."
n "I could hear heavy footsteps approaching me."
n "I quickly got to my feet and looked around."
n "The door slowly opened and I looked at the blonde male."
show damien
$ dbase, dexp = 2,1
p "...Damien."
n "I said softly as he looked at me."
damien "Shhh It's me."
damien "I'm here to get you out."
damien "It's okay. You're safe now."
n "I looked around."
n "Was this it? I held out my hand to hold his."
n "But, I paused."
n "Was this really the right way to do this?"
n "Cain seemed happy with me."
n "I have a way out but, did I really want to scorn what Cain and I have?"


menu:
    "-Call for Cain {image=icon_heart.png}-" if cain_love >=80:
        $ cain_love +=20
        jump cain_damien_call_highlove

    "-Call for Cain-" if cain_love < 80:
        jump cain_damien_call_lowlove
    "-Go with Damien-":

        jump go_with_damien

label cain_damien_call_highlove:
$ cain_hideheart = False
n "I retracted my hands and took a deep breath in."
p "CAIN!!!"
n "I screamed at the top of my lungs and Damien took his hand back."
damien "WHAT ARE YOU DO-"
$ cwings,cbase, cexp = 0,3,10
n "Before Damien could even react I watched his arm separate from his body."
show CG_Damien_removedArm
hide damien
n "Damien let out a blood curling scream as he held his arm socket and fell to the ground."
n "Cain walked up behind him licking his fingers."
cain "What do we have here?"
cain "Little brother?"
scene cain_bedroom_morning
show cain at center
n "He stomped Damien's side and kicked him across the room."
cain "Thank you for calling me, darling!"
n "I wandered behind him and clutched the bottom of his blazer."
p "He was trying to 'save' me..."
n "I mumbled into Cain's back."
cain "Looks like you failed again."
$ cwings,cbase, cexp = 0,3,9
cain "How foolish of you to walk into my domain without-"
show cain_cloud1_animation
show cain_cloud2_animation
n "I could hear a gas can going off."
n "It rolled into the room and a shadow darted across the room to Damien."
n "The figured picked Damien under the good side."
show cain:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show d 4 zorder 4:
    subpixel True
    xalign 1.0
    ypos 70
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0 xalign 0.9
cain "What is this?! TSK."
$ cwings,cbase, cexp = 1,3,9
n "A young man picked up Damien who was breathing hard."
show d 5:
    subpixel True
    xalign 0.9
    ypos 70
d "Fucking Christ Damien! Are you okay?"
n "He asked in a hushed tone."
n "He must have been apart of the same order as Damien."
n "Damien nodded slowly and looked at Cain."
damien "...This isn't over."
n ".D narrowed his eyes."
show d 1:
    subpixel True
    xalign 0.9
    ypos 70
d "Do you even realize what you’ve just done...?"
n "His voice dripped with calm animosity towards me as he backed up."
cain "You're not getting away."
n "Cain said as he moved forward but Damien and .D disappeared in a cloud of black mist."
hide cain_cloud1_animation
hide cain_cloud2_animation
hide d 1 with fade
show cain at center
show wings cain behind cain with dissolve
n "Cain sighed and shook his head."
n "He blew the smoke away with his wings."
hide cain_cloud1_animation with dissolve
hide cain_cloud2_animation with dissolve
cain "He'll be back."
n "He picked up Damien's arm and tossed it away like garbage then looked at me."
cain "You did well calling me as you did."
n "Cain said as he reached over and touched my hair."
$ persistent.cain_call = True
cain "You can call me anytime."
cain "You can call it a favor."
cain "Just give me a ring, love."
n "I reached out and he pulled me close caressing the top of my head."
p "Thank you, master."
n "I said softly into his chest."
jump cain_good_ending_from_damien

label cain_damien_call_lowlove:
n "I retracted my hands and took a deep breath in."
p "CAIN!!!"
n "I screamed at the top of my lungs and Damien took his hand back."
damien "What the fuck are you doing?!"
n "We quickly looked around, but nothing came."
damien "You-"
n "Damien bit back his words and took a step back."
damien "You deserve whatever he does to you."
hide damien with dissolve
n "Damien ran into the next room and the floor let out a low rumble."
n "I could hear clapping behind me and quickly turned around."
$ cwings,cbase, cexp = 0,3,10
show cain
cain "Good job."
cain "You should have went with him."
n "Cain charged forward and I felt my arm separate from my body."
cain "That'll teach you to touch my things."
n "I fell to my knees as my arm started to bleed out."
$ health -=100
n "Cain stood over me and put his foot on my head."
cain "Pathetic."
n "He pushed my face in my own blood grinding his heel into the back of my skull."
n "I could only struggle until the blackness took over."
scene black with fade
hide screen health_bar
hide screen sanity_bar
play music "cain/cain_death.mp3"
$ persistent.cain_ending_arm = True
scene endslate with Dissolve(1.0)
screen cain_ending_arm:
    text "{=endslate_title}You Died!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Cain cut off your arm. {/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_arm
with Dissolve(1.0)
pause
$ renpy.full_restart()


label go_with_damien:
image veni = "cain/veni.png"
n "I took Damien's hand and he pulled me close."
damien ".D! Let's get out of here."
n "Damien called into the other room."
n "A hooded figure stepped out into the open."
show damien:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show d 4:
    subpixel True
    xalign 1.0
    ypos 70
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0 xalign 0.9
n "He must have been hiding just in case something went wrong."
d "I got your back."
n " It was finally over."
scene black with fade
n "It felt like I was weightless as I floated away with Damien and .D."
n "In the blink of an eye I was in a place... that looked like a church."
scene damien_church with fade
play music "cain/damien_church.mp3"
n "I clutched my wounds and looked at Damien and .D."
show damien:
    subpixel True
    xalign 0.05
show d 4:
    subpixel True
    xalign 0.9
    ypos 70
p "Where are we?"
d "We're in the church."
damien "You're safe now. But."
n "Damien paused and looked at .D for a moment."
show d 3:
    subpixel True
    xalign 0.9
    ypos 70
d "You have to stay here until Cain gets bored."
damien "My brother is unrelenting."
damien "If he kept you alive that long."
damien "There's a good chance he likes you more than a normal human."
damien "You'll be safe here."
damien "As long as it takes, you can stay here with us."
show CG_damien_saves_MC with dissolve
n "As long as it takes."
n "I rushed forward and hugged Damien hard."
n "I felt his strong arms around me as he put his hand on the back of my head."
n "He slowly touched my hair and held me close."
damien "...Don't worry... I'll protect you."
hide screen health_bar
hide screen sanity_bar
$ persistent.cain_ending_damien = True
scene endslate_clean with Dissolve(1.0)
screen cain_ending_damien:
    text "{=endslate_title}You Survived!{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Damien saved you. {/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen cain_ending_damien
with Dissolve(1.0)
pause
jump damien_D_after

label damien_D_after:
hide screen cain_ending_damien
scene damien_church
n "I clutched my wounds and looked at Damien and .D."
show damien:
    subpixel True
    xalign 0.05
show d 4:
    subpixel True
    xalign 0.9
    ypos 70
n "Damien sighed as I walked away and turned around the corner."
n "I still wanted to listen in on their conversation."
n "I peeked around and saw Damien and .D standing across from each other."
d "How do we keep getting ourselves into these situations?"
n ".D asked looking at Damien with an accusatory stare."
show d 3:
    subpixel True
    xalign 0.9
    ypos 70
damien "Yeah, yeah It's my fault."
damien "That's why I asked you to stay back while I got them out."
show d 4:
    subpixel True
    xalign 0.9
    ypos 70
n ".D sighed and turned to leave but Damien leaned back."
$ dexp = 7
damien "Do you think it's weird?"
d "What's weird?"
damien "We're priests."
damien "We're supposed to be protecting people from the supposed 'dark' underbellies."
damien "Yet... We both have demon boyfriends."
show d 3:
    subpixel True
    xalign 0.9
    ypos 70
d "I don't know what you mean."
show veni:
    ypos 0
    xpos 0
    subpixel True
    easeout 0.05 zoom 1.5 ypos 0
    easeout 0.05 zoom 1.0 ypos 0
    pause 0.5
damien "You know.. I have Veni."
damien "He's a demon and You're dating that one demon."
damien "The one with goggles."
show d 2:
    subpixel True
    xalign 0.9
    ypos 70
d "What!?"
show izm:
    ypos 0
    xpos 600
    subpixel True
    easeout 0.05 zoom 1.5 ypos 0
    easeout 0.05 zoom 1.0 ypos 0
    pause 0.5
d "Izm?"
d "Are you sure you didn't sustain a head injury?"
d "You seem to be delusional."
hide veni with dissolve
hide izm with dissolve
n ".D said in a warning tone."
n "Almost like he was covering something up..."
damien "You sure you’re not dating?"
damien "You guys looked awfully close."
n "Damien teased as .D stormed away."
hide d 2 with dissolve
show damien at center
d "WE'RE NOT DATING."
damien "...Sure you're not."
n "Damien watched .D walk into the other room."
damien "...If you're not right now you're gonna be."
menu:
    "-Walk away-":
        n "I'll just leave them be."
        n "I should really gather myself up."
        scene black with Dissolve(1.0)
        screen leave_them_alone_damien:
            text "You walked away.\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        show screen leave_them_alone_damien
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Talk to Damien-":

        play music "cain/damien_main.mp3"
        n "Damien walked up to me and I looked up at him."
        $ dexp = 5
        damien "What's wrong?"

n "He looked at the wooden pew and nodded towards it."
damien "Sit."
$ dexp = 1
n "He said in a commanding tone, and I immediately sat down."
damien "You sure are good at listening to commands."
n "Damien flopped down next to me."
n "He put his arms up on the pew and I scooted closer to him."
menu:
    "-Ask more about him-":
        p "What about you?"
        p "What are you all about?"
        n "Damien snorted and leaned back."
        damien "I'm just some grumpy dude who tries to pick up people like you, people who Cain's picked up."
        n "Damien's green eyes didn't leave the ceiling."
        p "I know that much."
        $ dexp = 1
        p "What about YOU, Damien?"
        $ dexp = 2
        pause(0.7)
        $ dexp = 1
        damien "...I can't say anything good about myself, so I'd rather let you get your own impression of me."
        damien "If I only can say bad shit about myself, then that's all you'll get into your head."
        damien "It's better if you learn from being around me, then you can make your own decision."
    "-Cuddle-":

        n "I leaned into him and put my head on his chest."
        n "I slowly rubbed my head into his chest."
        n "He put one arm around me and caressed the top of my head."
        damien "Haha, what are you doing?"
        $ dblush, dexp =1, 6
        damien "You a cat or something?"
        damien "Affectionate now that I rescued you from that vulture?"
        n "Damien yanked me into his lap and nuzzled the top of my head."
        $ dexp = 7
        damien "That's fine, I'm always up for cuddling anyways."
        n "He rubbed his hands into my back."
        n "I clung close to him and let him squeeze me tight, his hands were warm and strong."
    "-Ask about Cain-":

        p "Am I really safe here?"
        n "I asked looking at Damien."
        damien "IN HERE?"
        damien "Yeah you are."
        damien "Out there."
        damien "I can't promise anything."
        n "Damien pointed at the door."
        damien "I'm not sure how much Cain liked you."
        damien "So I can't be certain."

$ dblush, dexp =0, 7
damien "Hey shouldn't you get to bed?"
n "Damien got up and I slipped my feet on the ground."
n "I nodded quickly and he took a breath in like he was going to tell me something."
$ dexp = 2
pause(0.9)
$ dexp = 1
damien "Ah. Nevermind. Go sleep."
n "He shoved me a bit."
p "You're rough for a Priest."
n "He put his hands out and shrugged."
$ dexp = 7
damien "Never said I was a good one."
n "He said with a small laugh as he slipped into the shadows."
hide damien with dissolve
n "I watched the tail of his coat slip out of sight and I sighed."
n "I wandered away into my own room."
scene black with fade
n "Who could sleep?"
n "I walked into the hallway and looked at the shrine."
scene damien_church_night with fade
$ dbase, dexp = 1, 3
n "It was dark, was there anyone else living here besides those two?"
n "It didn't seem to be an open church, just two guys walking around sometimes."
n "No sermons, no visitors."
n "I felt my bare feet against the concrete and pulled the robe that was on my bed around me."
n "Where was Damien anyways?"
n "I poked my head into a room that was empty."

menu:
    "-Go back to sleep-":
        n "I looked at the time."
        n "I should just let Damien sleep."
        n "I let out a sigh and walked back to my room."
        scene black with Dissolve(1.0)
        screen damien_back_to_bed:
            text "You went back to bed.\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        show screen damien_back_to_bed
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Look around more-":

        scene damien_bedroom with fade
        n "I quickly moved on to the next one."
        n "It was filled with random bones, magic spells, magic circles, books, cups, and little plants."
        n "And a bed with a blond man sleeping in the middle."

menu:
    "-Wake him up-":
        n "I reached out to touch him."
        jump damien_bed
    "-Get in bed with him-":

        n "I kneeled down on his bed."
        jump damien_bed
    "-Let him sleep-":

        n "I turned away to leave."
        damien "Why are you snooping around in my room?"
        n "I heard from behind me."
        n "I turned around to see Damien looking at me."
        $ dexp = 1
        show damien
        p "I thought you were asleep."
        damien "I don't sleep very well."
        n "He said as he patted the spot next to him and sat up."
        jump damien_ask

label damien_bed:
    show damien
    $ dexp = 1
    n "Damien grabbed my robe and pinned me to the bed, a sharp blade to my neck."
    damien "I don't sleep very well."
    damien "Why are you sneaking up on me?"
    n "Damien said examining my face."
menu:
    "\"That's not how you threaten me, I like it.\"":
        n "Damien's cheeks puffed out a little and he pulled back the knife."
        n "He laughed and closed it."
        damien "Well, I haven't heard that one in a while."
        n "He sat back and looked down at me."
        damien "You're lucky I slept with my boxers on today."
        p "Sounds unlucky to me."
        jump damien_lonely
    "\"Damn dude, chill out!\"":

        damien "Hey fam!"
        damien "I have to deal with shit like Cain all day, of course I'm jumpy."
        n "Damien said taking his blade away from my neck."
        jump damien_lonely
    "\"Don't hurt me..\"":

        damien "Oh shit... Sorry."
        damien "I'm pretty paranoid."
        n "Damien rolled off me and closed his knife."
        jump damien_lonely

label damien_ask:
n "He sat at the edge of the bed."
damien "So, what are you doing in my room?"
n "I looked at him then looked at my hands."

label damien_lonely:
p "I was lonely."
damien "I know that feeling, think my company would be better?"
n "He laid back down on his bed."
p "It's better than being alone, plus, you look bored."
$ dexp = 8
damien "Ass."
n "He said as he pulled me up on his lap."
n "I sat on top of him looking down at him."
$ dexp = 1

menu:
    "\"This is lewd, aren't you supposed to be a man of the cloth?\"":
        damien "Pft, hardly."
        damien "All I do is exorcisms."
        damien "They just let me stay here, I'm more effective than a human priest."
        n "Damien said as he ran his hands up my thighs."
        n "I shuddered as his rough hands made their way up my robes."
        n "He pushed his fingers into my skin."
        n "I felt my toes curl as he pressed his fingers into my muscles."
        p "What are you doing?"
        damien "I'm just touching you."
        damien "That a crime?"
        n "He put his hands up and put them behind his head."
        $ dexp = 7
        p "Tease."
        n "I huffed."
        damien "You're the one who complained."
        p "I wasn't complaining."
        p "I just asked."
        damien "That sounds like a 'you' problem."
    "\"Don't tell me you were this lonely, Daddy.\"":

        n "Damien snorted."
        $ dexp = 8
        damien "Daddy? You into that kinda thing?"
        $ dexp = 7
        n "He grabbed the front of my robes and tugged me down to eye level."
        n "The musky scent of his cologne and sweat hitting my nose."
        damien "Or would you just rather call me Father?"
        damien "Because, I can punish you all night long, sinner."
        n "Damien whispered into my lips."
        n "His voice felt... dangerous."
        n "His usual tone dropping into a confident growl, sending a chill up my spine."
        n "He let my robes go and leaned back, his hands behind his head."
    "-Touch him-":

        n "He folded his hands behind his head, content with just looking at me."
        n "But, I wasn't content with just looking at him."
        n "I put my hands on his chest, running my fingers on his tattoo."
        p "13 hm?"
        damien "It's for necromancy."
        damien "Helps me focus."
        p "Is that why you have bones in your room?"
        $ dexp = 7
        damien "That and they look badass."
        n "He let out a contented sigh as I ran my hands on his torso, rubbing his skin."

damien "Did you just come in here to talk?"
n "Damien asked as he pulled an arm from behind his head and played with the tie around my waist."
damien "Or did you wanna do something else."
n "He said as he tugged it, I could almost feel all of me being exposed to him."
n "I bit my bottom lip thinking about what I wanted to say."

menu:
    "\"I want you to hurt me.\"":
        jump damien_maso
    "\"Let's fuck.\"":

        jump damien_nympho
    "\"Punish me, Father.\"":

        jump damien_kinky


label damien_maso:
damien "Masochist hm?"
n "He grabbed a fist full of my hair and pushed me down on the bed."
n "He twisted my arm behind my back and rubbed his body against me."
n "He pulled my arm and leaned into the back of my neck."
damien "Sadism is my forte..."
n "He said as he pushed my arm."
n "It felt like it was going pull right out of my socket as he yanked."
n "I let out a moan as he twisted me."
n "He didn't say anything more as he rubbed his cock against me."
n "I could feel it through his thin boxers."
n "He lifted up my robes and rubbed his hand across my ass."
damien "I need to get you underwear or something."
n "He lifted up his hand and slapped me across the ass."
p "AHHH!"
n "I let out a scream as his hand made contact with my skin."
n "Those muscles weren't just for show."
n "I could feel my skin pulsing with my heart beat."
n "I didn't have to ask him to hit me again."
n "Blow after blow with his heavy strong hands, I felt my head spinning as he flipped me over."
$ dbase, dblush, dexp= 4,1,1
n "His cock rubbing between my legs."
p "Damien."
n "I whined out."
damien "What is it?"
n "He grumbled almost in an annoyed tone."
n "He pushed my legs together and rubbed between them."
p "I want more..."
n "He let my legs fall to the side and cocked his head to one side."
damien "You're gonna have to beg louder than that."
n "He pushed his hands into my throat and held down."
n "My breath coming in haggard gasps."
p "F-Fuck.. me.."
n "He pushed harder."
damien "Louder, I wanna feel your voice vibrate in my hands."
n "I whimpered as he pushed into me, licking the sweat off his upper lip."
p "PLEASE, I WANT YOUR COCK!"
n "I screamed out."
n "He pushed his mouth on mine, silencing me in an instant as he pushed his cock into me."
n "He grabbed my robe belt and pulled it off me, exposing me to him fully."
damien "Cute."
$ dbase, dblush, dexp= 4,1,7
n "He lashed my robe belt around my wrists and pulled it tightly above my head tying me to his headboard."
p "Damien.."
n "I whined out as he put his hands on my hips, grinding in deep, his cock rubbing inside of me."
n "I could feel the corner of my eyes welling up with tears as he gripped his hand and and sent another hard blow into my side."
n "I felt the air escape my lungs."
n "He pushed his fingers into my mouth."
n "Touching my tongue and forcing them a bit further than comfortable."
n "I let out a small retching sound, but he pulled his fingers back before I could vomit."
n "I could feel him touching my tongue and rubbing against it."
n "I felt helpless as he searched my mouth, making me gag."
n "I licked his fingers trying to get him to relent but, it was too much."
n "I moaned on his hand. "
n "He let out a low chuckle as he lifted my legs, pushing deep inside."
n "I could feel myself tightening up around him and I gripped the rope around my wrists."
n "Damien let out a low grunt and came inside of me without warning."
show CG_damien_Sex with dissolve
n "I felt him drop me and I moved my hands to touch him but, I was still tied up."
n "He looked at my arms and untied them for me, letting them drop above my head."
n "I reached up and hugged him close to me."
n "He kissed me on the lips and rolled onto his bed next to me."
damien "You're staying here tonight."
n "Damien put his arms around me and I snuggled in close."
p "I wouldn't have it any other way."
scene black with fade
jump damien_end

label damien_nympho:
damien "You want me to fuck you hm?"
n "Damien said sliding off of the bed and standing up."
n "He snapped his fingers and clothes materialized around him."
hide damien with dissolve
$ dbase, dblush, dexp= 3,0,7
show damien with dissolve
p "Nice clothes."
damien "Yeah?"
damien "I used to have black hair too, but people trust you more when you look 'traditional'."
p "How'd you do that anyways?"
damien "Magic, one of the perks knowing magic is that you can be lazy."
n "He walked around me and I eyeballed him."
p "What?"
n "I watched him circle me, much like a vulture himself and he pulled off his belt and moved quickly behind me."
n "He put the belt around my neck and dragged me close to his body."
damien "You want me to fuck you, I'll need you to get on the ground."
n "He said into my ear as I struggled against him."
n "I thrashed and kicked hard but, he was much stronger than me."
n "He dragged me to the floor and stomped on my back, pushing hard against my spine, just enough to force me to moan."
damien "Look at you, trash."
damien "Writhing around on the floor like a grub."
n "He grabbed my hair and pulled my head up."
damien "You're just lucky enough to be here."
n "He pulled a cigarette out of his pocket and lit it."
n "He blew smoke into my face making me cough."
damien "Flip over."

menu:
    "-No-":
        n "I shook my head and Damien sneered."
        damien "A brat hm?"
        n "He kicked me across the stomach forcing me over."
        n "I let out a breath and a loud moan at the kick."
    "-Yes-":

        n "I rolled over when he asked."
        n "He leaned down and ran his fingers through my hair."

n "Damien pushed his boot on my chest and the tip of his toe in my face."
damien "Lick it."
n "He commanded as I put my hands on his heavy leather boots."
n "It gripped it and squeezed down on the rubber."
n "I stuck my tongue out and licked the top of the leather."
n "It tasted dirty, and gritty, but the look on Damien's face."
n "It made me writhe in pleasure as he pushed his boot all over my tongue."
n "I panted and gripped his foot."
p "Please... fuck me.."
n "I moaned out as I twisted under his shoe."
n "He licked his lips and pointed at his belt."
n "I quickly moved to open his pants, his cock right in my face."
$ dbase, dblush, dexp= 3,1,7
damien "Clean it up, then I'll fuck you."
n "I pushed the head of his cock in my mouth."
n "It was sweaty and tasted like his pre-cum."
n "But, I didn't care."
n "To me, it tasted just like I thought it would."
n "He let out a low growl as I pushed his cock into the back of my throat, letting him fuck my mouth."
n "Damien put his hands on my shoulders and thrusted deep inside forcing me to gag but I didn't puke."
n "He pulled his cock out, a thin line of spit coming from the tip of his cock to my mouth."
damien "Spread your legs."
n "Damien growled in a low tone."
n "I leaned back and spread my legs open exposing everything to him."
n "He leaned down and without warning pushed his way inside of me."
p "AH~!"
n "I moaned out I gripped the back of my legs."
n "He leaned into my neck and bit down as he rocked into me."
n "I knew it would leave a mark but I didn't care."
n "I panted hard as I felt the length his cock reach as far as it could."
n "He continued to bite and suck on my neck, knowing it would leave a dark mark on me."
n "His mark."
n "I tensed up around him and cried out finally letting my legs go so I could hold on to him."
n "I could feel his body moving still."
n "I could feel myself orgasming"
damien "Is that all you got?"
damien "I'm just getting started."
n "Damien said into my ear, his smooth voice making me shudder."
n "I laid out for him as he pinned my arms to the ground."
n "I hear him moving in and out of me but, I couldn't handle it anymore."
n "My tongue flopped out of my head as I moaned loud, at a complete loss for words."
n "I could feel his cum fill me up as he let out another moan."
n "I let my legs flop uselessly to the ground as he picked me up from my spot on the floor."
show CG_damien_double_vision with dissolve
n "His eyes.... I leaned my head on his shoulder and closed my own eyes."
p "...You're not human, are you?"
damien "No. I'm your fallen angel."
n "I clung to his arm as we laid down in his bed."
n "I knew I should have been afraid of another fallen angel."
n "But, I wasn't. I felt safe with him."
scene black with fade
jump damien_end

label damien_kinky:
n "Damien stood up."
damien "You want redemption, Sinner?"
hide damien with dissolve
$ dbase, dblush, dexp= 2,0,7
show damien with dissolve
n "Damien snapped his fingers and his uniform appeared around him."
n "He grabbed my chin and forced me on my feet."
damien "Strip, I have something for you."
n "I slowly slipped the robe off my shoulders as dropped it on the ground."
n "He grabbed my head and forced it over his bed."
damien "Bend over."
n "He reached behind his bed and pulled out a thin straight stick of wood."
damien "I'm gonna need to give you 40 lashes."
n "He pulled his arm back and smacked me across the ass."
n "He didn't hold back as I felt the wood strike my skin."
n "A sharp pain shot through my skin."
n "I let out a loud gasp and panted."
damien "I'm going to make you sorry."
n "He whispered into my ear."
n "I tilted my head back as he struck me again."
p "AH~"
n "I moaned out as the wood whipped across my skin again."
n "I rubbed my face into his sheets as I felt the sting."
n "They smelled like cigarettes and... him."
n "I could feel myself drooling as he struck me repeatedly."
n "Every lash across my skin stinging with a painful pleasure."
p "D-damien.."
n "I can finally moan out as I heard the wood snap across my ass."
n "There was blood I could feel it dripping down my legs."
n "But I didn't care."
$ dbase, dblush, dexp= 2,1,7
damien "Whoops... I got to into it."
n "Damien's breaths were ragged and excited."
n "He tossed away the broken switch and touched the blood on me."
damien "You're bleeding."
n "He leaned down and licked it."
n "I yelped and tensed up."
damien "I know how to stop it."
n "Damien wandered away from me for a moment, leaving me alone and shaking with excitement."
n "I felt his warm cock between my asscheeks and I arched my back."
p "AH."
n "I squeaked."
n "He let out a low chuckle as I felt something hit my skin."
n "It was hot."
n "I let out another moan as it dripped down my skin."
n "I looked at him and saw the candle hanging over me."
n "He dripped more wax over my tender skin and I moaned as it touched me."
n "I gripped the sheets as I rubbed my ass against his cock."
p "I..I want you.."
n "He tilted his head to the side as I felt more hot wax burn my skin."
n "I let out another moan and started to pant."
damien "What was that?"
damien "I couldn't quite hear you."
n "Damien eyes unlocking from my skin and moving to my face."
n "I felt like a could hear the sounds of a cicada."
p "I want you to fuck me."
n "I begged a bit louder."
n "He tossed away the candle and I heard it bounce away."
n "I gripped the sides of my hips and without another word he pushed his cock into me."
n "I felt myself tighten around him as he rubbed himself inside of me."
n "He pulled my arms back yanking them hard."
n "I felt my body tense up around him as he rhythmically pushed his way in and out of me."
n "I couldn't even think."
n "I felt his hands on me, the chatter of the cicada getting louder."
n "He put his hands on my neck and squeezed as I let out a breath."
n "I tried my best to keep my cool but I could feel myself orgasming under his hands."
show CG_Damien_Priest_Fallen with dissolve
n "My head was spinning but I could swear I saw dark metal wings."
p "Damien."
n "I moaned out as curled up on his bed."
n "I closed my eyes as I felt his body hit the bed with me."
n "I reached out and hugged him, closing my eyes and feeling his warmth around me."
scene black with fade
jump damien_end

label damien_end:
show damien_bedroom with fade
n "I woke up in Damien's arms and I nuzzled him softly."
n "He let out a soft grunt, he was actually sleeping this time."
$ dbase, dblush, dexp = 1,0,1
show damien
damien "..Ah...Good morning."
n "He grumbled."
n "He didn't seem like a morning person."

menu:
    "-Kiss-":
        n "I kissed him softly and he returned the kiss putting his hands lightly on my hips."
        $ dbase, dblush, dexp = 1,1,6
        damien "Ah. I can get used to that."
        n "He muttered into my lips as he sat up."
        n "I slipped off his bed and picked up my robe."
    "-Spank his butt-":

        n "I spanked him right on the ass."
        p "GET UP."
        n "I yelled with a happy smile on my face."
        $ dbase, dexp = 1,4
        n "His eyes shot open and he shoved me."
        damien "Brat. I'll get you for that."
        $ dbase, dexp = 1,1
        n "He pushed me off the bed and leaned over the side."
        n "I scooped my robe around me and stuck my tongue out at him."
        damien "Don't stick that out unless you plan on using it."
        n "I could feel my face heat up and he helped me to my feet."
    "-Push him off the bed-":

        n "I tried to shove him off the bed to get him up."
        p "Get up."
        n "I attempted to roll him off the bed."
        n "He barely moved as he grabbed me."
        n "I flailed uselessly and looked at him, his face resting on my chest."
        p "Let's get up, I'm hungry."
        n "I pushed fingers through his hair."
        n "It was thick and soft, I felt it with my fingers."
        n "He must have taken good care of it."
        damien "Alright fine."
        n "He muttered as he let me go to get up."
hide damien with dissolve
$ dbase, dblush, dexp = 3,0 ,7
show damien with dissolve
n "He snapped his fingers and his outfit materialized around him."
p "Lazy."
n "He walked beside me and bumped me hard with his hip."
n "I stumbled but didn't fall."
damien "I had to learn to put my clothes on that way."
damien "I can teach you too."
p "...Really?"
damien "Of course. It's magic, all you need is a master."
n "He cocked his eyebrows and looked at me."
p "You just want me to call you master don't you?"
damien "Stroke my ego just a little."
image Church_day_endslate = "cain/Church_day_endslate.jpg"
menu:
    "-Call him master-":
        p "Fine, Master Damien."
        n "I said pushing him out of his room."
        damien "Ahhh~ That felt so good though."
        n "Damien faked a moan as he stepped into the hallway."
    "-Don't call him master-":
        p "No gross!"
        n "I yelled my face as red as a beet."
        n "I pushed him out of his room."
        $ dbase, dexp = 3, 7
        damien "I'll break you yet~!"

scene damien_church with fade
show damien:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show d 4 zorder 4:
    subpixel True
    xalign 1.0
    ypos 70
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0 xalign 0.9
n ".D stared at us as we wandered out Damien's room."
d "I'm not going to ask."
damien "...Good idea."
n "Damien watched his partner walk away."
hide d with dissolve
show damien at center
p "Oops."
damien "Don't worry, [player_name]."
damien "He'll get over it."
p "I'm not worried."
n "I grinned and looped my arm with Damien's to get breakfast with him."
n "He rubbed his face against the top of my head and gripped my hand."
n "His large warm hand, covering mine and squeezing it gently."
scene Church_day_endslate with Dissolve(1.0)
screen damien_stay:
    text "You stayed with Damien.\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
show screen damien_stay
with Dissolve(1.0)
pause
$ renpy.full_restart()






define ren = DynamicCharacter ("ren_name", 
    window_background="ren/dialoguebox_ren.png",
    show_side_image = ConditionSwitch(
    "ren_hideheart == True", Null(),
    "ren_love >= 100", "love_icon_ren.png",
    "ren_love >= 90", "love_icon_red.png",
    "ren_love >= 80", "love_icon_pink.png",
    "ren_love >= 70", "love_icon_orangered.png",
    "ren_love >= 60", "love_icon_orange.png",
    "ren_love >= 50", "love_icon_yellow.png",
    "ren_love >= 40", "love_icon_green.png",
    "ren_love >= 30", "love_icon_cyan.png",
    "ren_love >= 20", "love_icon_blue.png",
    "ren_love >= 10", "love_icon_purple.png",
    "ren_love >= 0", "love_icon_black.png",
    "ren_love <= 0", "love_icon_broken.png",
    )
    )

define law = DynamicCharacter ("lawrence_name", 
    window_background="lawrence/dialoguebox_lawrence.png",
    show_side_image = ConditionSwitch(
    "law_love >= 100", "love_icon_lawrence.png",
    "law_love >= 90", "love_icon_red.png",
    "law_love >= 80", "love_icon_pink.png",
    "law_love >= 70", "love_icon_orangered.png",
    "law_love >= 60", "love_icon_orange.png",
    "law_love >= 50", "love_icon_yellow.png",
    "law_love >= 40", "love_icon_green.png",
    "law_love >= 30", "love_icon_cyan.png",
    "law_love >= 20", "love_icon_blue.png",
    "law_love >= 10", "love_icon_purple.png",
    "law_love >= 0", "love_icon_black.png",
    "law_love <= 0", "love_icon_broken.png",
    )
    )
define ashe = Character ("???", 
    window_background="lawrence/dialoguebox_ashe.png"
    )
define strade = Character ("???", 
    window_background="ren/dialoguebox_strade.png"
    )
$ lsanity = 100
init python:
    def limit_lsanity():
        try:
            if store.lsanity < 0:
                store.lsanity = 0
            elif store.lsanity > 100:
                store.lsanity = 100
        except:
            pass

    config.python_callbacks.append(limit_lsanity)

screen sanity_bar_law:
    vbox:
        xalign 0.99 yalign 0.03
        bar value AnimatedValue(lsanity, range=100.0):
            xalign 0.0 yalign 0.0
            xmaximum 30
            ymaximum 400
            left_bar Frame("lawrence/bar_sanity_law_empty.png", 10, 0)
            right_bar Frame("lawrence/bar_sanity_law.png", 10, 0)
            thumb None
            bar_vertical True
        add ConditionSwitch(
             "lsanity <= 0", "bar_sanity_icon_death.png",
             "lsanity >= 1", "lawrence/bar_sanity_icon_law.png",
             )
screen ren_button:
    imagebutton xpos 248 ypos 419:
        idle ("ren/button_activateren.png")
        hover ("ren/button_activateren.png")
        action (Jump('ren_intro'))
screen button_yourdrink:
    imagebutton xpos 299 ypos 318:
        idle ("lawrence/button_yourdrink.png")
        hover ("lawrence/button_yourdrink_over.png")
        action (Jump('law_drink_yours'))
screen button_rensdrink:
    imagebutton xpos 575 ypos 203:
        idle ("lawrence/button_rensdrink.png")
        hover ("lawrence/button_rensdrink_over.png")
        action (Jump('law_drink_rens'))
screen button_lawsdrink:
    imagebutton xpos 92 ypos 195:
        idle ("lawrence/button_lawsdrink.png")
        hover ("lawrence/button_lawsdrink_over.png")
        action (Jump('law_drink_laws'))
screen button_nodrink:
    imagebutton xpos 590 ypos 500:
        idle ("lawrence/button_refusedrink.png")
        hover ("lawrence/button_refusedrink_over.png")
        action (Jump('law_drink_no'))

image bg_pub = "lawrence/bg_pub.jpg"
image bg_outside_pub = "lawrence/bg_outsidepub.jpg"
image bg_law_backalley = "lawrence/bg_backalley.jpg"
image bg_law_backalley_withren = "ren/bg_backalley_withren.jpg"
image bg_ren_livingroom = "ren/bg_ren_livingroom.jpg"
image bg_ren_basementstairs = "ren/bg_ren_basementstairs.jpg"
image bg_ren_basement = "ren/bg_ren_freezer.jpg"
image bg_law_backalley_ripple = "lawrence/bg_backalley_ripple.jpg"
image bg_law_backalley_withren_ripple = "ren/bg_backalley_withren_ripple.jpg"
image bg_law_apartment = "lawrence/bg_lawapartment.jpg"
image bg_law_apartment_rain = "lawrence/bg_lawapartment_rain.jpg"
image bg_law_door = "lawrence/bg_lawrence_door.jpg"
image bg_wakingup = "lawrence/bg_wakingup.jpg"
image bg_vignette = "lawrence/vignette.png"
image bg_law_bathroom = "lawrence/bg_law_bathroom.jpg"
image bg_apartment_nightmare = "lawrence/bg_lawapartment_nightmare.jpg"
image bg_apartment_nightmare_animated:
    "lawrence/bg_lawapartment_nightmare_bulge3.jpg" with dissolve
    pause 0.5
    "lawrence/bg_lawapartment_nightmare_bulge1.jpg" with dissolve
    pause 0.5
    "lawrence/bg_lawapartment_nightmare_bulge2.jpg" with dissolve
    pause 0.5
    repeat
image bg_river1_animated:
    "lawrence/bg_river1_1.jpg" with dissolve
    pause 0.5
    "lawrence/bg_river1_2.jpg" with dissolve
    pause 0.5
    "lawrence/bg_river1_3.jpg" with dissolve
    pause 0.5
    repeat
image bg_river4 = "lawrence/bg_river1_4.jpg"
image bg_river5_animated:
    "lawrence/bg_river1_5.jpg"
    pause 0.05
    "lawrence/bg_river1_6.jpg"
    pause 0.05
    "lawrence/bg_river1_7.jpg"
    pause 0.05
    repeat


init:
    image cg_lawrence_drinks = "lawrence/cg_lawrence_drinks.jpg"
    image cg_lawrence_vincent = "lawrence/cg_lawrence_vincent.jpg"
    image cg_lawrence_choking = "lawrence/cg_lawrence_choking.jpg"
    image cg_lawrence_sawing = "lawrence/cg_lawrence_sawing.jpg"
    image cg_lawrence_drown = "lawrence/cg_lawrence_drown.jpg"
    image cg_lawrence_stepping = "lawrence/cg_lawrence_stepping.jpg"
    image cg_lawrence_upsidedown = "lawrence/cg_lawrence_upsidedown.jpg"
    image cg_lawrence_bucket = "lawrence/cg_lawrence_bucket.jpg"
    image cg_lawrence_darkness_still = "lawrence/cg_lawrence_darkness_still.jpg"
    image cg_lawrence_buried = "lawrence/cg_lawrence_buried.jpg"
    image cg_lawrence_buried2 = "lawrence/cg_lawrence_buried2.jpg"
    image cg_lawrence_sleeping = "lawrence/cg_lawrence_sleeping.jpg"
    image cg_lawrence_stabbed = "lawrence/cg_lawrence_stabbed.jpg"
    image cg_lawrence_startled = "lawrence/cg_lawrence_startled.jpg"
    image cg_lawrence_startledblush = "lawrence/cg_lawrence_startledblush.jpg"
    image cg_lawrence_sex = "lawrence/cg_lawrence_sex.jpg"
    image cg_lawrence_amputation1 = "lawrence/cg_lawrence_amputation1.jpg"
    image cg_lawrence_lsanity = "lawrence/cg_lawrence_lsanity.jpg"
    image cg_lawrence_lsanity2 = "lawrence/cg_lawrence_lsanity2.jpg"
    image cg_lawrence_drugs = "lawrence/cg_lawrence_drugs.jpg"
    image cg_lawrence_closer = "lawrence/cg_lawrence_closer.jpg"
    image cg_lawrence_shears = "lawrence/cg_lawrence_shears.jpg"
    image cg_lawrence_shutyouup2 = "lawrence/cg_lawrence_shutyouup2.jpg"
    image cg_lawrence_eviscerate1 = "lawrence/cg_lawrence_eviscerate1.jpg"
    image cg_lawrence_eviscerate2 = "lawrence/cg_lawrence_eviscerate2.jpg"
    image cg_lawrence_boneforest = "lawrence/cg_lawrence_boneforest.jpg"
    image cg_lawrence_sanity = "lawrence/cg_lawrence_sanity.jpg"
    image cg_lawrence_smile = "lawrence/cg_lawrence_smile.jpg"
    image cg_lawrence_brighttrees = "lawrence/cg_lawrence_brighttrees.jpg"

    image cg_ren_stradecicle = "ren/cg_ren_stradecicle.jpg"
    image cg_ren_lawrence_1 = "ren/cg_ren_lawrence_1.jpg"
    image cg_ren_lawrence_3 = "ren/cg_ren_lawrence_3.jpg"
    image cg_ren_law_killmc = "ren/cg_ren_law_killmc.jpg"
    image cg_ren_lawrence_4 = "ren/cg_ren_lawrence_4.jpg"
    image cg_ren_lawrence_5 = "ren/cg_ren_lawrence_5.jpg"
    image cg_ren_lawrence_6 = "ren/cg_ren_lawrence_6.jpg"
    image cg_ren_lawrence_7 = "ren/cg_ren_lawrence_7.jpg"
    image cg_ren_lawrence_8 = "ren/cg_ren_lawrence_8.jpg"
    image cg_ren_lawrence_10 = "ren/cg_ren_lawrence_10.jpg"
    image cg_ren_lawrence_12 = "ren/cg_ren_lawrence_12.jpg"
    image cg_ren_nailgunbj = "ren/cg_ren_nailgunbj.jpg"
    image cg_ren_gun = "ren/cg_ren_gun.jpg"
    image cg_ren_sanity = "ren/cg_ren_sanity.jpg"
    image cg_ren_chains3 = "ren/cg_ren_chains3.jpg"
    image cg_ren_chains1 = "ren/cg_ren_chains1.jpg"
    image cg_ren_chains2 = "ren/cg_ren_chains2.jpg"
    image cg_ren_oral1 = "ren/cg_ren_oral1.jpg"
    image cg_ren_oral2 = "ren/cg_ren_oral2.jpg"
    image cg_ren_oral3 = "ren/cg_ren_oral3.jpg"
    image cg_ren_lickheart = "ren/cg_ren_lickheart.jpg"
    image cg_ren_lickheart2 = "ren/cg_ren_lickheart2.jpg"
    image cg_ren_stepping = "ren/cg_ren_stepping.jpg"
    image cg_ren_neutralyandere = "ren/cg_ren_neutralyandere.jpg"
    image cg_ren_neutralmad = "ren/cg_ren_neutralmad.jpg"
    image cg_ren_pole = "ren/cg_ren_pole.jpg"
    image cg_ren_pole7 = "ren/cg_ren_pole7.jpg"
    image cg_ren_pole8 = "ren/cg_ren_pole8.jpg"
    image cg_ren_pole21 = "ren/cg_ren_pole21.jpg"
    image cg_ren_pole25 = "ren/cg_ren_pole25.jpg"
    image cg_ren_pole29 = "ren/cg_ren_pole29.jpg"
    image cg_ren_pole32 = "ren/cg_ren_pole32.jpg"
    image cg_ren_eatmyheart = "ren/cg_ren_eatmyheart.jpg"
    image cg_ren_flashback1 = "ren/cg_ren_flashback1.jpg"
    image cg_ren_flashback2 = "ren/cg_ren_flashback2.jpg"
    image cg_ren_good = "ren/cg_ren_good.jpg"
    image cg_ren_happy = "ren/cg_ren_happy.jpg"

    define audio.law_pub = "lawrence/g-major-restful-and-peaceful-classical-piano-90-bpm_GksJuA4d.mp3"
    define audio.law_pub_outside = "lawrence/busy-road-passing-cars_Gy_tlSNd.mp3"
    define audio.law_haunt = "lawrence/bcc-031814-eeerie-ghost-haunting-music-174.mp3"
    define audio.law_kill = "lawrence/sinking-under_fkDhHUBu.mp3"
    define audio.law_twinkle = "lawrence/bcc-031814-twinkle-twinkle-twisted-little-star-1039.mp3"
    define audio.law_unsettled = "lawrence/unsettled-quiet_zJ8aYrHO.mp3"
    define audio.law_brownnote = "lawrence/low-reversed-long-rumbles_My9LmSNd.mp3"
    define audio.law_day = "lawrence/room-tone-new-york-city-apartment-outside-heavy-traffic_G13BsUNd.mp3"
    define audio.law_day_rain = "lawrence/rain-amb-w-thunder-2_GkCh_fEd.mp3"
    define audio.law_heartbeat = "lawrence/heartbeat-medium-slow-looping_GyDGwHNd.mp3"
    define audio.law_swamp = "lawrence/black-swamp_zy5G-MVd.mp3"
    define audio.law_heaven = "lawrence/heavenly-devilish_fkNBhBHu.mp3"
    define audio.law_reverse = "lawrence/dark-moddy-electro-music-cue_zyG3hSHu.mp3"

    define audio.ren_piano = "ren/all-alone-v2_fyETywru.mp3"
    define audio.ren_warppiano = "ren/bcc-031814-disturbed-and-out-of-tune-piano-855.mp3"
    define audio.ren_warppiano_straight = "<from 16>ren/bcc-031814-disturbed-and-out-of-tune-piano-855.mp3"
    define audio.ren_shocked = "ren/electric-sizzle_zyuNWG4u.mp3"
    define audio.ren_shocker = "ren/jg-032316-sfx-taser-shock-click-sound-long.mp3"
    define audio.ren_vampire = "ren/vampire-vamp60_MJuC7BBd.mp3"
    define audio.ren_obsessed = "ren/obsessed_z12C18Hu.mp3"
    define audio.ren_neutral = "ren/suspense-music-cue_MyEsnBS_.mp3"
    define audio.ren_ubi = "ren/the-revenge_z1WsyIBu.mp3"


image cg_lawrence_darkness_1 = "lawrence/cg_lawrence_darkness_1.png"
image cg_lawrence_darkness_2 = "lawrence/cg_lawrence_darkness_2.png"
image cg_lawrence_darkness_3 = "lawrence/cg_lawrence_darkness_3.png"
image cg_lawrence_darkness_4 = "lawrence/cg_lawrence_darkness_4.jpg"
image cg_lawrence_darkness_5 = "lawrence/cg_lawrence_darkness_5.png"
image cg_lawrence_darkness_2_anim:
    "cg_lawrence_darkness_2"
    yalign 0.5
    easein 0.75 xalign 0.8
    easeout 0.75 xalign 0.5
    easein 0.75 xalign 0.2
    easeout 0.75 xalign 0.5
    repeat
image cg_lawrence_darkness_3_anim:
    "cg_lawrence_darkness_3"
    yalign 0.5
    easein 0.75 xalign 0.3
    easeout 0.75 xalign 0.5
    easein 0.75 xalign 0.7
    easeout 0.75 xalign 0.5
    repeat
image cg_lawrence_darkness_4_anim:
    "cg_lawrence_darkness_4"
    yalign 0.5
    easein 0.75 xalign 0.4
    easeout 0.75 xalign 0.5
    easein 0.75 xalign 0.6
    easeout 0.75 xalign 0.5
    repeat
image cg_lawrence_darkness_anim_end:
    "cg_lawrence_darkness_5"
    alpha 0.0
    yalign 0.5
    xalign 0.5
    easeout 0.2 alpha 1.0
    alpha 0.0
    pause (0.1)
    alpha 0.1
    pause (0.5)
    alpha 0.0
    pause (0.05)
    alpha 0.1
    pause (0.05)
    easeout 0.2 alpha 0.0

image law_sil = silhouetted ('lawrence/law_base_1.png',0,0,0)
image law_sil_crazy = silhouetted ('lawrence/law_base_12.png',0,0,0)
image law_sil_shirtless = silhouetted ('lawrence/law_base_9.png',0,0,0)

image ren_exclaim = "ren/ren_exclaim.png"

init python:

    lbase,lexp,lblush,lbangs = 1,1,1,1
    law_crazy = False

    def draw_law(st, at): 
        if law_crazy == True:
            global lbase, lbangs
            if lbase == 1:
                lbase = 12
                lbangs = 3
            if lbase == 2:
                lbase = 13
                lbangs = 3
            if lbase == 14:
                lbase = 16
            if lbase == 15:
                lbase = 17
            if lbase == 25:
                lbase = 18
                lbangs = 3
            if lbase == 26:
                lbase = 27
                lbangs = 3
        return LiveComposite(
            (493, 600), 
            (0, 0), "lawrence/law_base_%d.png"%lbase,
            (0, 0), "lawrence/law_expression_%d.png"%lexp,
            (0, 0), "lawrence/law_blush_%d.png"%lblush,
            (0, 0), "lawrence/law_bangs_%d.png"%lbangs
            ),.1   
init:
    image law = DynamicDisplayable(draw_law)

init python:

    rtail,rbase,rexp,rears,rbangs,rblush = 1,1,1,1,1,1

    def draw_ren(st, at): 
        if rbase == 7 or rbase == 8 or rbase == 9:
            rexpy = 10
            rexpx = 2
            rearsy = 10
            rearsx = 2
            rbangsy = 10
            rbangsx = 2
            rblushy = 10
            rblushx = 2
        else:
            rexpy = 0
            rexpx = 0
            rearsy = 0
            rearsx = 0
            rbangsy = 0
            rbangsx = 0
            rblushy = 0
            rblushx = 0
        return LiveComposite(
            (493, 600), 
            (0, 0), "ren/ren_tail_%d.png"%rtail,
            (0, 0), "ren/ren_base_%d.png"%rbase,
            (rexpx, rexpy), "ren/ren_expression_%d.png"%rexp,
            (rearsx, rearsy), "ren/ren_ears_%d.png"%rears,
            (rbangsx, rbangsy), "ren/ren_bangs_%d.png"%rbangs,
            (rblushx, rblushy), "ren/ren_blush_%d.png"%rblush
            ),.1   
init:
    image ren = DynamicDisplayable(draw_ren)

init python:

    ashebase,asheexp = 1,1

    def draw_ashe(st, at): 
        return LiveComposite(
            (493, 600), 
            (0, 0), "lawrence/ashe_base_%d.png"%ashebase,
            (0, 0), "lawrence/ashe_expression_%d.png"%asheexp,
            ),.1   
init:
    image ashe = DynamicDisplayable(draw_ashe)

image ashe_wings_up = "lawrence/ashe_wings_1.png"
image ashe_wings_down = "lawrence/ashe_wings_2.png"

image ren_collar_animate:
    "ren/ren_collar_elec1.png"
    pause (0.05)
    "ren/ren_collar_elec2.png"
    pause (0.05)
    repeat
image ren_collar_still:
    "ren/ren_collar.png"

image ren_remote_unpressed:
    "ren/ren_remote.png"
image ren_remote_pressed:
    "ren/ren_remote_press.png"

init python:

    def ren_collar_switch(st, at):
        if ren_shocking == True:
            return LiveComposite(
                (800, 600), 
                (650, 330), "ren_collar_animate"
                ),.1  
        else:
            return LiveComposite(
                (800, 600), 
                (650, 330), "ren_collar_still"
                ),.1 
init:
    image ren_collar = DynamicDisplayable(ren_collar_switch)

init python:

    def ren_remote_switch(st, at):
        if ren_shocking_reverse == True:
            return LiveComposite(
                (800, 600), 
                (650, 330), "ren_remote_pressed"
                ),.1  
        else:
            return LiveComposite(
                (800, 600), 
                (650, 330), "ren_remote_unpressed"
                ),.1 
init:
    image ren_remote = DynamicDisplayable(ren_remote_switch)


transform spriteshake:
    linear 0.02 yoffset +2
    linear 0.02 yoffset 0
    repeat

screen disableclick(time):
    timer time action Hide("disableclick")
    key "mouseup_1" action NullAction()




label ending_netflix:
scene webpage
p "You know what?"
p "I don't even feel like going out."
scene black
n "I shut down the computer."
p "All of those places look like a bad time."
n "I got up and grabbed the ice cream from my freezer."
n "Then I sat down with a spoon, a blanket, and turned on the TV."
n "Time for some movies~"
scene black with dissolve
scene endslate_clean with Dissolve(1.0)
screen ending_netflix:
    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You chilled at home and it was awesome.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen ending_netflix
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_start:
show screen health_bar
show screen sanity_bar
$ lawrence_name = "???"
$ ren_name = "???"
$ ren_hideheart = False
$ law_crazy = False
$ law_sexed = False
$ temp_lsanity = 100
$ drugs = 0
$ struggle = 0
$ drugwarning1 = False
$ drugwarning2 = False
$ lbase,lexp,lbangs,lblush = 1,1,1,0
$ rtail,rbase,rexp,rears,rbangs,rblush = 0,1,1,0,1,0
$ ashebase,asheexp = 1,1

n "I decided to head out to the pub."
play music law_pub fadein 1.0
scene bg_pub
n "The atmosphere and people were quiet."
n "It almost felt like stepping into the past."
n "Maybe just because there wasn't a single TV."
menu:
    "-Order some drinks-":
        $ drugs += 1
        $ law_introdrinking = False
        n "Well if I'm here I might as well drink."
        n "There wasn't much else to do."
        n "I ordered a few drinks and sat by myself."
        n "Surprisingly, I wasn't bored."
        n "The dim lights and quiet conversation of the other patrons was soothing."
        n "I lost track of time and began to doze off a bit."
    "-Just relax-":
        $ law_introdrinking = True
        n "I wasn't in the mood to drink."
        n "I just sat by myself and watched the few patrons mill about."
        n "Their quiet voices and the clinks of glasses on wood made me feel a little sleepy."
        n "I lost track of time and began to doze off a bit."
scene black with dissolve
n "Huh?"
scene bg_pub with hpunch
p "I fell asleep!"
n "I looked around quickly."
n "The bar was empty..."
n "Or, almost empty."
n "There was one man left in the corner, hunched over a drink."
n "How long was I asleep!?"
n "Maybe he knows what time it is..."
n "I got up and approached the man."
p "Hey, sorry to bug you... but do you know what time it is?"
show law
$ lbase,lexp,lbangs = 3,2,1
law "Oh!"
$ lbase,lexp,lbangs = 1,1,1
law "Uhhh..."
law "It's.. It's almost closing time."
law "It's 1:45."
n "He seemed like he was preoccupied with something else."
menu:
    "\"Wow... It's really late.\"":
        law "Haha... uh.. yeah..."
        $ lbase,lexp,lbangs = 1,8,1
        n "He was starting to look really uncomfortable."
        $ lbase,lexp,lbangs = 1,1,1
        law "I'm just waiting for my...friend."
    "\"Are you alright?\"":

        $ lbase,lexp,lbangs = 1,2,1
        law "What?"
        $ lbase,lexp,lbangs = 1,1,1
        law "Y-yeah... I'm fine."
        law "I'm just waiting for my...friend."
    "\"Thanks! I really lost track of time.\"":

        $ lbase,lexp,lbangs = 1,3,1
        law "Ha... yeah..."
        $ lbase,lexp,lbangs = 1,1,1
        law "I can relate to that..."
        law "I'll probably go soon."
        law "I'm just waiting for my...friend."

n "I only wondered about his friend for a moment."
$ lbase,lexp,lbangs = 1,8,1
$ rbase,rexp,rbangs = 1,1,1
show law:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.05
show ren:
    subpixel True
    xalign 1.0
    ypos 70
    alpha 0.0
    pause 0.2
    easeout 0.3 alpha 1.0 xalign 0.9
n "A much shorter guy came out from the bathroom, looking very cheerful."
ren "Alright Lawrence, let's-"
$ lawrence_name = "Lawrence"
$ persistent.character_unlock_lawrence = True
$ rbase,rexp = 1,2
ren "Ah!"
show ren
$ lbase,lexp,lbangs = 1,6,1
ren "There's someone else here?"
n "I smiled awkwardly at the redhead."
$ rbase,rexp = 1,3
n "I thought I caught a flash of panic on his face before he spoke again."
show ren
ren "Well... My name is Ren."
$ ren_name = "Ren"
$ persistent.character_unlock_ren1 = True
$ rbase,rexp = 1,4
$ lbase,lexp,lbangs = 1,1,1
ren "It's nice to meet you!"
n "He looked at me expectantly."
p "Oh!"
p "My name is %(player_name)s."
if player_name.lower() == "strade":
    $ rbase,rexp = 1,5
    ren "W..what?"
    p "I said my name is %(player_name)s."
    $ rbase,rexp = 1,6
    n "Ren gulped and looked uncomfortable."
    ren "T-that's not a very common name..."
    p "Heh... yeah. I guess it isn't."
elif player_name.lower() == "lily" or player_name.lower() == "rose" or player_name.lower() == "daisy" or player_name.lower() == "violet" or player_name.lower() == "ivy" or player_name.lower() == "basil" or player_name.lower() == "fern" or player_name.lower() == "clover" or player_name.lower() == "cypress" or player_name.lower() == "camellia" or player_name.lower() == "poppy" or player_name.lower() == "petunia" or player_name.lower() == "rosemary" or player_name.lower() == "azalea" or player_name.lower() == "blossom" or player_name.lower() == "saffron" or player_name.lower() == "bluebell" or player_name.lower() == "olive" or player_name.lower() == "holly" or player_name.lower() == "hazel" or player_name.lower() == "heather" or player_name.lower() == "marigold" or player_name.lower() == "buttercup" or player_name.lower() == "maple" or player_name.lower() == "iris":
    $ lbase,lexp,lbangs = 1,2,1
    p "It's nice to meet you too!"
    $ lbase,lexp,lbangs,lblush = 1,23,1,1
    $ law_love += 10
    law "{size=12}That's a really nice name...{/size}"
else:
    p "It's nice to meet you too!"
$ lbase,lexp,lbangs,lblush = 1,8,1,0
$ rbase,rexp = 1,7
n "We all looked at each other for a moment."
n "What was up with these two?"
menu:
    "\"Is everything okay Lawrence?\"":
        $ law_introren = False
        $ lbase,lexp,lbangs = 1,1,1
        $ rbase,rexp = 1,2
        $ law_love += 10
        law "Oh...yeah."
        $ lbase,lexp,lbangs = 1,3,1
        n "Lawrence looked even more nervous."
        $ rbase,rexp = 1,8
        n "But Ren flashed a smile"
        ren "Hey, I know!"
        ren "I can get us a round before it closes!"
    "\"Is everything okay Ren?\"":
        $ law_introren = True
        $ lbase,lexp,lbangs = 1,1,1
        $ rbase,rexp = 1,8
        $ ren_love += 10
        ren "Everything's great!"
        $ rbase,rexp = 1,4
        ren "Hey, I know!"
        ren "I can get us a round before it closes!"
    "-Say nothing-":
        $ law_introren = False
        n "They looked at each other awkwardly for a moment."
        n "Then Ren turned to me and smiled."
        $ rbase,rexp = 1,4
        ren "Hey, I know!"
        ren "I can get us a round before it closes!"

p "Oh I-"
show ren:
    subpixel True
    xalign 0.9
    alpha 1.0
    easeout 0.1 xalign 1.0 alpha 0.0
n "He trotted off to the bartender before I could say anything."
$ lbase,lexp,lbangs = 1,6,1
law "I...uh..."
show law:
    subpixel True
    xalign 0.05
    alpha 1.0
    easeout 0.1 xalign 0.15 alpha 0.0
n "Then Lawrence followed him."
n "I stared after them, confused about the whole situation."
n "Ren must be older than he looks, since the bartender is serving him..."
n "I sat down at their table and kept watching."
n "They were talking to each other quickly and quietly."
n "It almost looked like they were arguing."
$ lbase,lexp,lbangs = 1,3,1
$ rbase,rexp = 1,8
show law:
    subpixel True
    xalign 0.05
    alpha 0.0
    easeout 0.3 alpha 1.0
show ren:
    subpixel True
    xalign 0.9
    alpha 0.0
    ypos 70
    easeout 0.3 alpha 1.0
n "But then they both returned and smiled."
n "Lawrence set the drinks down in front of each of us."
scene cg_lawrence_drinks with fade:
law "One more drink for the night..."
label law_pickdrink:
show screen button_yourdrink
show screen button_rensdrink
show screen button_lawsdrink
show screen button_nodrink
$ pub_drugged = False
$ renpy.pause (hard=True)
jump law_pickdrink

label law_drink_yours:
hide screen button_yourdrink
hide screen button_rensdrink
hide screen button_lawsdrink
hide screen button_nodrink
scene bg_pub with fade:
show law:
    xalign 0.05
show ren:
    ypos 70
    xalign 0.9
n "I reached for the drink Lawrence set in front of me."
$ lbase,lexp,lbangs = 1,1,1
n "I took a sip."
n "It was a rum and coke, a comforting drink."
n "I relaxed a bit as I finished it."
n "I looked across the table at my new companions."
n "Lawrence didn't touch his drink."
$ rbase,rexp = 1,3
n "Ren started to look more worried."
jump law_pub_renrun

label law_drink_laws:
hide screen button_yourdrink
hide screen button_rensdrink
hide screen button_lawsdrink
hide screen button_nodrink
scene bg_pub with fade:
show law:
    xalign 0.05
show ren:
    ypos 70
    xalign 0.9
$ pub_drugged = True
$ drugs += 1
$ lbase,lexp,lbangs = 1,2,1
$ rbase,rexp = 1,2
n "I reached across the table and took the drink in front of Lawrence."
law "..."
$ lbase,lexp,lbangs = 1,1,1
n "I took a sip."
$ rbase,rexp = 1,3
n "It was a rum and coke, a comforting drink."
n "I relaxed a bit as I finished it."
$ rbase,rexp = 1,4
n "I looked across the table at my new companions."
n "Lawrence didn't touch the other drink."
$ rbase,rexp = 1,3
n "Ren started to look more worried."
jump law_pub_renrun

label law_drink_rens:
hide screen button_yourdrink
hide screen button_rensdrink
hide screen button_lawsdrink
hide screen button_nodrink
scene bg_pub with fade:
show law:
    xalign 0.05
show ren:
    ypos 70
    xalign 0.9
$ rbase,rexp = 1,2
n "I reached across the table and took the drink Lawrence set in front of Ren."
ren "Oh!"
$ lbase,lexp,lbangs = 1,1,1
$ rbase,rexp = 1,8
n "I took a sip."
n "It was a rum and coke, a comforting drink."
n "I relaxed a bit as I finished it."
n "I looked across the table at my new companions."
n "Lawrence didn't touch his drink."
$ rbase,rexp = 1,3
n "Ren started to look more worried."
jump law_pub_renrun

label law_drink_no:
hide screen button_yourdrink
hide screen button_rensdrink
hide screen button_lawsdrink
hide screen button_nodrink
scene bg_pub with fade:
show law:
    xalign 0.05
show ren:
    ypos 70
    xalign 0.9
$ rbase,rexp = 1,3
$ lbase,lexp,lbangs = 1,1,1
n "I didn't want to seem rude..."
n "But I just met these people."
jump law_pub_renrun

label law_pub_renrun:
ren "It's really late..."
$ rbase,rexp = 1,3
ren "I think...I should leave."
$ lbase,lexp,lbangs = 1,2,1
law "Wait, you're leaving?"
$ rbase,rexp = 1,6
ren "S-sorry.."
show ren:
    subpixel True
    xalign 0.9
    alpha 1.0
    easeout 0.1 xalign 1.0 alpha 0.0
n "Ren ran out the door."
law "Hey wait!!"
show law:
    subpixel True
    xalign 0.05
    alpha 1.0
    easeout 0.1 xalign 0.15 alpha 0.0
n "Then Lawrence ran after him."
n "I stood there baffled."
n "Then I shook my head."
n "Those two are really none of my business."
n "And I {i}really{/i} should be heading home."
stop music fadeout 1.0
play sound law_pub_outside fadein 1.0 loop
scene bg_outside_pub:
    xalign 1.0
n "I grabbed my coat and strolled out of the pub into the crisp night air."
n "Lawrence and Ren were nowhere in sight."
p "Well...That was weird."
n "I started walking down the sidewalk and felt something tap my shoulder."
n "I jumped, startled, and turned around."
play music law_haunt fadein 1.0
show law
$ lbase,lexp,lbangs = 1,13,1
law "..."
p "Ah!"
p "You startled me..."
n "He seemed to be struggling with what to say."
$ lbase,lexp,lbangs = 8,20,2
law "...Ren's path...split from mine."
menu:
    "\"Better luck next time?\"":
        p "It's late. Ren left by himself."
        p "And I should go t-"
    "\"What are you talking about?\"":

        $ temp_lsanity -= 10
        p "Didn't Ren just...leave because it's so late..?"
    "-Ignore him-":

        n "This guy was starting to creep me out."
        n "I took a few steps back."

law "Ren was different..."
menu:
    "\"Relax, man. You can always hang out with him later.\"":
        $ lbase,lexp,lbangs = 1,4,1
        $ temp_lsanity -= 20
        p "Anyway, I'm going home."
    "\"I'm sure Ren just wanted to get home.\"":

        $ temp_lsanity -= 10
        p "And I'm going home too."
    "\"I'm sorry...\"":

        n "My apology didn't seem to calm him down."

$ lbase,lexp,lbangs = 1,21,1
label law_dodge:
$ time = 0.5
$ timer_range = 0.5
$ timer_jump = 'law_dodge_hit'
stop music
play music law_kill
show screen countdown
menu:
    "-Dodge!-":
        hide screen countdown
        jump law_dodge_dodged

label law_dodge_dodged:
n "He took a swing at me!"
$ temp_lsanity -= 20
n "His fist connected with the bricks where my head used to be."
$ lbase,lexp,lbangs = 3,14,1
law "AHGGH!"
scene bg_outside_pub:
    xalign 1.0
    subpixel True
    easeout 0.3 xalign 0.0
show law:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 3.0
n "I started running down the street away from him."
n "This guy is nuts!"
jump law_intro_running

label law_dodge_hit:
p "Wha-" with hpunch
$ health -= 10
n "Before I could react, his fist connected with my face."
n "I stumbled back, my ears ringing."
p "What.. the..."
n "He started walking towards me as I looked back up in a panic."
n "He's crazy!"
scene bg_outside_pub:
    xalign 1.0
    subpixel True
    easeout 0.3 xalign 0.0
show law:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 3.0
n "I started running down the street away from him."
jump law_intro_running

label law_intro_running:
if law_introdrinking == True:
    n "I stumbled a bit as I tried to run."
    n "All the drinks I had earlier in the night were slowing my steps..."
    n "I kept moving."
    n "I couldn't hear him behind me."
    if pub_drugged == True:
        n "I felt a pang of dizziness for a moment."
    n "There was an alley to the right."
else:
    n "I ran as fast as I could."
    n "The cold night air began to sting in my lungs."
    n "I didn't think I could hear him following..."
    if pub_drugged == True:
        n "I felt a pang of dizziness for a moment."
    n "I looked ahead and saw an alley to the right."
menu:
    "-Left-":
        n "I ran across the stre-"
        stop sound
        stop music
        play sound "lawrence/tire-screech_M1B8kfV_.mp3"
        $ health -= 100
        scene black with hpunch
        scene cg_lawrence_vincent with fade
        $ vincent_name = "???"
        vincent "Woah-ho! I didn't see you there!"
        n "I wanted to yell in surprise, but I couldn't seem to move or talk."
        vincent "Tch, and you made a real mess."
        n "I noticed my blood glinting on his bike before everything went cold and dark."
        hide screen health_bar
        hide screen sanity_bar
        hide screen lsanity_bar
        $ persistent.vincent_ending_splattered = True
        scene endslate with Dissolve(1.0)
        stop sound
        stop music
        play music law_twinkle
        screen vincent_ending_splattered:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You didn't look both ways.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen vincent_ending_splattered
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Right-":


        if pub_drugged == True:
            if law_introren == True:
                scene bg_law_backalley_withren:
                    yalign 0.0
                show screen ren_button
                n "I veered into the alleyway and pressed my back against the wall."
                n "I felt another wave of dizziness."
                n "What's wrong with me..?"
                hide screen ren_button
                show bg_law_backalley_withren_ripple:
                    yalign 0.0
                    xalign 0.5
                    alpha 0.0
                    subpixel True
                    easeout 0.3 zoom 1.1 alpha 1.0
                    easeout 0.3 zoom 1.0 alpha 0.0
                pause (0.6)
                show screen ren_button
                n "My vision blurred and I began to feel sick."
                hide screen ren_button
                show bg_law_backalley_withren_ripple:
                    yalign 0.0
                    xalign 0.5
                    alpha 0.0
                    subpixel True
                    easeout 0.3 zoom 1.2 alpha 1.0
                    easeout 0.3 zoom 1.0 alpha 0.0
                pause (0.6)
                hide bg_law_backalley_withren_ripple
                show screen ren_button
                p "Wh...what..."
                n "I couldn't move."
                hide screen ren_button
                scene bg_law_backalley_withren:
                    yalign 0.0
                    xalign 0.5
                    subpixel True
                    easeout_expo 0.7 yalign 1.0
                pause(0.7)
                scene black with vpunch
                stop sound fadeout 1.0
                stop music fadeout 1.0
                n "I couldn't even keep my eyes open..."
                pause(1)
                jump law_night1
            else:
                scene bg_law_backalley:
                    yalign 0.0
                n "I veered into the alleyway and pressed my back against the wall."
                n "I felt another wave of dizziness."
                n "What's wrong with me..?"
                show bg_law_backalley_ripple:
                    yalign 0.0
                    xalign 0.5
                    alpha 0.0
                    subpixel True
                    easeout 0.3 zoom 1.1 alpha 1.0
                    easeout 0.3 zoom 1.0 alpha 0.0
                n "My vision blurred and I began to feel sick."
                show bg_law_backalley_ripple:
                    yalign 0.0
                    xalign 0.5
                    alpha 0.0
                    subpixel True
                    easeout 0.3 zoom 1.2 alpha 1.0
                    easeout 0.3 zoom 1.0 alpha 0.0
                p "Wh...what..."
                n "I couldn't move."
                scene bg_law_backalley:
                    yalign 0.0
                    xalign 0.5
                    subpixel True
                    easeout_expo 0.7 yalign 1.0
                pause(0.7)
                hide bg_law_backalley_ripple
                scene black with vpunch
                stop sound fadeout 1.0
                stop music fadeout 1.0
                n "I couldn't even keep my eyes open..."
                pause(1)
                jump law_night1
        else:
            scene bg_law_backalley:
                yalign 0.0
            n "I veered into the alleyway and pressed my back against the wall."
            n "I think I lost him..."
            show law
            $ lbase,lexp,lbangs = 3,7,1
            n "I gasped as he whipped around the corner."
            p "Sto-"
            n "His hand shot up and grabbed my face."
            $ health -= 20
            n "He pulled back and slammed my head into the cement behind it." with vpunch
            n "I crumpled to the ground as my vision went dark."
            scene black with dissolve
            stop sound fadeout 1.0
            stop music fadeout 1.0
            pause(1)
            jump law_night1
    "-Straight ahead-":

        n "I kept running past the alley."
        n "I slowed slightly to take a look over my shoulder."
        n "What!?"
        n "I felt his whole bodyweight slam into me from behind before I hit the ground." with vpunch
        $ health -= 20
        n "My head cracked on the sidewalk and I fought to stay awake."
        n "I could feel him panting with effort on top of me."
        law "Wh.."
        law "O-oh no."
        scene black with dissolve
        law "Are you okay?"
        stop sound fadeout 1.0
        stop music fadeout 1.0
        pause(1)
        jump law_night1

label law_night1:
play music law_unsettled fadein 1.0
n "My first sensation was panic and dread."
n "I froze- not wanting to move or open my eyes until I could recall what just happened."
n "The next thing I noticed was the smell."
n "Earthy...warm...and something sickly sweet."
n "I tried to identify the familiar smell as I became aware of some sounds."
n "I could hear shuffling and light scrapes of metal on wood."
unknown "{size=12}It's okay...I'll...I'll fix it...{/size}"
n "I slowly opened my eyes."
scene bg_wakingup with dissolve
$ lbase,lexp,lbangs = 7,0,0
show law zorder 2
show bg_law_apartment zorder 1 with dissolve
$ lbase,lexp,lbangs = 7,0,0
show law
law "It'll be easy..."
menu:
    "\"What will be easy?\"":
        $ lbase,lexp,lbangs = 3,2,1
        $ temp_lsanity -= 10
        law "Ah! You!"
    "\"Where am I!?\"":
        $ lbase,lexp,lbangs = 3,2,1
        $ temp_lsanity -= 10
        law "Ah! You!"
    "-Stay silent-":
        n "I wasn't sure I should make any sound."
        n "He kept talking to himself quietly."
        law "It won't be like last time."
        $ lbase,lexp,lbangs = 1,1,1
        law "J-just...stay calm..."
        $ lbase,lexp,lbangs = 3,2,1
        law "AH! You're awake!"

$ lbase,lexp,lbangs = 1,1,1
n "I gulped and stared at him."
p "Where...?"
scene bg_law_apartment:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.0
    pause 0.2
    easeout 0.2 xalign 1.0
    pause 0.2
    easeout 0.2 xalign 0.5
show law:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.7
    pause 0.2
    easeout 0.2 xalign 0.3
    pause 0.2
    easeout 0.2 xalign 0.5
n "My eyes darted around the room."
n "Some sort of studio apartment."
n "There were plants everywhere."
law "Uh...okay, you're probably feeling a little..."
n "I tried to move."
$ sanity -= 10
n "I couldn't."
$ lbase,lexp,lbangs = 1,6,1
law "Hey, calm down."
n "I looked down and saw my arms and legs were tightly taped to a wooden chair."
n "I started to breathe faster and looked back to him."
$ lbase,lexp,lbangs = 1,3,1
law "I... can explain this."
n "Something about this guy seemed..."
$ lsanity = 0
show screen sanity_bar_law
with dissolve
$ lsanity += temp_lsanity
n "Unstable."
menu:
    "\"What do you want with me?\"":
        $ lsanity -= 10
        $ lbase,lexp,lbangs = 3,2,1
        law "What?"
        $ lbase,lexp,lbangs = 1,2,1
        law "No, no, I don't want anything."
        $ lbase,lexp,lbangs = 1,1,1
        law "I mean I do."
        law "I did."
        $ lbase,lexp,lbangs = 4,0,0
        $ lsanity -= 10
        law "Augh..."
        call law_subroutine from _call_law_subroutine
        jump law_night1_explain
    "-Scream for help-":

        $ lbase,lexp,lbangs = 3,15,1
        $ lsanity -= 20
        $ law_love -= 10
        n "I opened my mouth and screamed as loud as I could."
        $ lbase,lexp,lbangs = 3,14,1
        n "Lawrence leapt forward and clamped his hand over my mouth."
        call law_subroutine from _call_law_subroutine_1
        jump law_night1_scream
    "-Let him explain-":

        $ law_love += 10
        n "I nodded slowly, willing him to continue."
        $ lbase,lexp,lbangs = 1,8,1
        law "W-well..."
        jump law_night1_explain

label law_night1_scream:
$ lbase,lexp,lbangs = 3,14,1
play sound law_brownnote fadein 1.0 loop
law "SHH!"
n "He stared at me hard as I stopped making noise behind his hand."
$ lbase,lexp,lbangs = 1,8,1
law "I need you to be...quiet."
n "He slowly removed his hand."
$ lbase,lexp,lbangs = 1,6,1
law "Okay?"
menu:
    "-Nod and stay quiet-":
        $ lbase,lexp,lbangs = 1,16,1
        stop sound fadeout 1.0
        n "I nodded slowly."
        jump law_night1_explain
    "-Scream again-":

        $ lsanity -= 50
        $ lbase,lexp,lbangs = 3,14,1
        n "I took in a deep breath to scream again."
        $ lbase,lexp,lbangs = 3,7,1
        stop music fadeout 1.0
        play music law_kill fadein 1.0
        n "This time he was faster, slamming one hand hard on my face and the other around my neck."
        law "No... no no no...no..."
        $ lbase,lexp,lbangs = 3,21,1
        scene cg_lawrence_choking with dissolve
        n "He pushed his hand harder around my neck."
        $ health -= 10
        show black:
            subpixel True
            alpha 0.0
            easeout 0.5 alpha 0.9
            easeout 1.0 alpha 0.0
        n "I couldn't breathe."
        n "I couldn't make any sound."
        $ sanity -= 20
        $ health -= 20
        law "I...can't..."
        law "You have to be quiet...quiet..."
        n "He only squeezed tighter."
        show black:
            subpixel True
            alpha 0.0
            easeout 0.5 alpha 0.9
            easeout 1.0 alpha 0.0
        $ sanity -= 20
        $ health -= 20
        n "My vision began to spot as I desperately hoped for him to let go."
        $ sanity -= 100
        $ health -= 100
        scene black with dissolve
        stop sound fadeout 3.0
        stop music fadeout 3.0
        n "But he never did."
        hide screen health_bar
        hide screen sanity_bar
        hide screen sanity_bar_law
        $ persistent.law_ending_choked = True
        play music law_twinkle fadein 1.0
        scene endslate with Dissolve(1.0)
        screen law_ending_choked:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Lawrence made you quiet.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen law_ending_choked
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()

label law_night1_explain:
$ lbase,lexp,lbangs = 1,6,1
law "Look..."
$ lbase,lexp,lbangs = 1,1,1
law "Things got a little out of hand."
n "He paused, thinking."
law "I'd been talking to Ren for a couple weeks."
law "Y-you know, on the internet."
law "So I was nervous."
$ lbase,lexp,lbangs = 2,8,1
n "He started to fidget."
law "And then you showed up."
law "And Ren left..."
law "And...and..."
$ lbase,lexp,lbangs = 1,4,1
n "I listened quietly, but he trailed off."
n "I shifted uncomfortably, feeling more nervous."
$ lbase,lexp,lbangs = 1,23,1
law "And now you're here."
$ lexp = 6
law "I couldn't just leave you there!"
n "I pulled slowly at the tape around my wrists, beginning to sweat."
call law_subroutine from _call_law_subroutine_2
$ lbase,lexp,lbangs = 1,1,1
n "He looked away."
law "I should never leave."
$ lbase,lexp,lbangs = 1,8,1
law "It's..."
law "...not worth it..."
$ lbase,lexp,lbangs = 1,4,1
law "All I found was another problem."
menu:
    "\"You have to let me go.\"":
        $ lbase,lexp,lbangs = 1,6,1
        n "I tried to speak with some authority."
        $ law_love -= 10
        p "You can't just keep me here."
        p "If you let me go now, I won't even tell anyone."
        $ lbase,lexp,lbangs = 1,1,1
        p "It'll be like it never happened."
        p "You haven't even done anything serious yet."
        $ lbase,lexp,lbangs = 1,8,1
        n "I paused and looked at him."
        law "No it won't."
        law "Nothing is ever the same."
        $ lbase,lexp,lbangs = 1,4,1
        law "Time won't stop, and I can't stop."
        n "He picked up the roll of duct tape on the table."
        p "You CAN stop!"
        p "Listen to m-"
        $ lbase,lexp,lbangs = 1,9,1
        n "He tore off a piece and placed it gently over my mouth."
        $ sanity -= 10
        n "I tried to scream through it at he tore off another piece."
        law "People are so delicate."
        play sound law_brownnote fadein 1.0 loop
        n "He smoothed the tape over my nose."
        $ sanity -= 20
        n "I looked at him helplessly, panicking and unable to breathe."
        $ lbase,lexp,lbangs = 1,13,1
        law "I barely need to touch you to take away what you need to survive."
        $ sanity -= 10
        n "I struggled as hard as I could, but I was starting to feel dizzy."
        law "A little piece of tape..."
        law "And you'll wither in front of me..."
        n "I slumped forward, unable to struggle any more."
        $ health -= 10
        $ sanity -= 20
        show black:
            subpixel True
            alpha 0.0
            easeout 0.5 alpha 0.9
            easeout 1.0 alpha 0.0
        n "I started to pass out."
        $ lbase,lexp,lbangs = 1,4,1
        stop sound
        n "I was shocked back to myself as he tore the tape from my face." with hpunch
        $ sanity += 30
        n "I wheezed as I took in deep breaths."
        call law_subroutine from _call_law_subroutine_3
        $ lbase,lexp,lbangs = 1,8,1
        law "So you'll just... do as I say for now."
        $ lbase,lexp,lbangs = 1,3,1
        law "Okay?"
        jump law_day1_pacing
    "\"I don't have to be a problem!\"":

        $ lbase,lexp,lbangs = 1,2,1
        n "He paused."
        law "What?"
        p "I..I can be your friend... instead."
        $ lbase,lexp,lbangs = 1,1,1
        law "You're..."
        $ lbase,lexp,lbangs = 1,8,1
        law "I don't think that's a good idea."
        n "I had to think of something to convince him..."
        menu:
            "\"Just give me a chance!\"":
                $ lbase,lexp,lbangs = 1,4,1
                n "He suddenly looked at me with disgust."
                law "Another chance...?"
                $ lbase,lexp,lbangs = 1,21,1
                law "How many chances!?"
                n "He seemed to be getting more agitated."
                law "I've tried a hundred times! A thousand maybe!"
                n "He was breathing harder."
                $ lbase,lexp,lbangs = 1,21,1
                law "It's always fine at first!"
                $ lbase,lexp,lbangs = 1,13,1
                law "And... and then I say... or I do something..."
                p "Lawrence... ju-"
                $ lbase,lexp,lbangs = 1,14,1
                law "And everything is Hell again!"
                law "It won't be long now!"
                $ lsanity -= 10
                $ lbase,lexp,lbangs = 2,11,1
                n "He let out an awkward, angry sounding laugh."
                call law_subroutine from _call_law_subroutine_4
                p "I'm... not like them, Lawrence."
                $ lbase,lexp,lbangs = 1,4,1
                n "He immediately stopped laughing."
                $ lbase,lexp,lbangs = 3,9,1
                n "He slammed his hands down on my legs."
                law "PROVE IT."
                menu:
                    "-Stay quiet-":
                        n "I didn't know how to prove it."
                        n "I gulped and looked at him, trying not to upset him even more."
                        $ lbase,lexp,lbangs = 1,4,1
                        n "He sighed and stood back up."
                        $ lbase,lexp,lbangs = 1,13,1
                        law "That's what I thought."
                        jump law_day1_pacing
                    "\"I'll do anything you want!\"":

                        $ lbase,lexp,lbangs = 3,2,1
                        p "Just say it! I'll prove it!"
                        n "He stared hard at me and tightened his hands around my legs."
                        $ lbase,lexp,lbangs = 3,6,1
                        law "Whatever I..."
                        play sound law_brownnote fadein 1.0
                        n "He just kept staring."
                        p "You're hurting me..."
                        $ lbase,lexp,lbangs = 1,13,1
                        n "He released my thighs and stood up abruptly."
                        law "Ugh..."
                        p "...Lawrence?"
                        $ lsanity -= 30
                        $ lbase,lexp,lbangs = 4,0,0
                        law "I DON'T KNOW WHAT I WANT!"
                        call law_subroutine from _call_law_subroutine_5
                        $ health -= 15
                        $ lbase,lexp,lbangs = 1,21,1
                        n "Before I could say anything, he punched me hard in the face." with hpunch
                        $ lbase,lexp,lbangs = 1,2,1
                        stop sound fadeout 1.0
                        n "I was too shocked to do anything but groan in pain as he stepped back."
                        call law_subroutine from _call_law_subroutine_6
                        jump law_day1_pacing
                    "\"I don't know how.\"":

                        $ lbase,lexp,lbangs = 3,6,1
                        n "I was scared."
                        $ sanity -= 10
                        n "I looked down at myself, taped to this chair in this stanger's apartment."
                        p "I... don't know..."
                        call law_subroutine from _call_law_subroutine_7
                        $ lbase,lexp,lbangs = 3,16,1
                        n "I started to cry."
                        $ law_love += 10
                        $ lsanity += 10
                        $ lbase,lexp,lbangs = 1,16,1
                        n "He slowly took his hands off my legs."
                        $ lbase,lexp,lbangs = 1,6,1
                        law "Oh..."
                        law "Uh...s-sorry..."
                        jump law_day1_pacing
            "\"...I can see you like plants.\"":

                $ lbase,lexp,lbangs = 1,1,1
                n "He paused and glanced around at the ferns and potted flowers in his apartment."
                $ lbase,lexp,lbangs = 2,8,1
                law "I...guess..."
                menu:
                    "\"They say a man who gardens can't be a bad person.\"":
                        play sound law_brownnote fadein 1.0
                        law "Well..."
                        law "They're wrong."
                        $ lbase,lexp,lbangs = 6,12,1
                        n "Lawrence looked at a fern and quickly tore a small leaf away from it."
                        law "Anyone can take care of plants."
                        law "They're silent..."
                        $ lbase,lexp,lbangs = 5,13,1
                        n "He rolled the leaf in his fingers."
                        law "Just soft... short little lives. No one knows about them here."
                        n "He began to crush and smear the leaf between his fingertips."
                        law "No one knows or cares if they die."
                        $ lbase,lexp,lbangs = 5,11,1
                        n "He suddenly smiled."
                        $ sanity -= 10
                        law "...Except for me."
                        stop sound fadeout 1.0
                        call law_subroutine from _call_law_subroutine_8
                        jump law_day1_pacing
                    "\"The flowers are really pretty.\"":

                        $ lbase,lexp,lbangs = 2,9,1
                        n "Lawrence scoffed."
                        $ lbase,lexp,lbangs = 1,9,1
                        law "They're pretty?"
                        $ lbase,lexp,lbangs = 1,13,1
                        n "He looked over at some of his flowers."
                        law "Flowers are liars."
                        $ lbase,lexp,lbangs = 1,4,1
                        n "I must have been giving him a questioning expression, because he looked at me and then explained further."
                        law "They're a big colourful display..."
                        law "Made to trick insects into helping them reproduce... or feeding them."
                        law "They're not honest about what they want."
                        law "Being attractive...to get their way..."
                        $ lbase,lexp,lbangs = 1,9,1
                        law "Kind of like you."
                        menu:
                            "\"Why would I lie to you?\"":
                                $ lbase,lexp,lbangs = 1,4,1
                                n "I continued."
                                p "You have me taped to a chair."
                                $ lbase,lexp,lbangs = 1,1,1
                                p "Lawrence."
                                $ lbase,lexp,lbangs = 2,8,1
                                p "I'm a real person, and you kidnapped me."
                                p "I can't even move."
                                $ lbase,lexp,lbangs = 2,15,1
                                p "You're in control here, okay?"
                                p "I'm not going to lie-"
                                $ lsanity -= 50
                                $ law_love -= 10
                                $ lbase,lexp,lbangs = 4,0,0
                                law "Stop it!!"
                                n "I froze."
                                $ lbase,lexp,lbangs = 8,20,2
                                law "S...stop... talking to me..."
                                law "Like... like I'm crazy..."
                                call law_subroutine from _call_law_subroutine_9
                                jump law_day1_pacing
                            "\"I'm a person, not a flower.\"":

                                $ lbase,lexp,lbangs = 1,2,1
                                n "He looked surprised for a second."
                                n "Then he looked me up and down."
                                $ law_love += 10
                                $ lbase,lexp,lbangs = 1,24,1
                                law "Well...obviously."
                                law "I knew that."
                                jump law_day1_pacing
                            "\"Wait... you think I'm attractive?\"":

                                $ lbase,lexp,lbangs,lblush = 1,22,1,3
                                law "UHH."
                                $ lsanity -= 10
                                $ lblush = 1
                                law "N..well...t-that's not what I..."
                                $ lbase,lexp,lbangs,lblush = 2,24,1,2
                                $ law_love += 10
                                law "N-never mind..."
                                call law_subroutine from _call_law_subroutine_10
                                $ lblush = 3
                                jump law_day1_pacing
                    "\"I like to garden too.\"":

                        $ lbase,lexp,lbangs = 1,2,1
                        law "R-really?"
                        $ lbase,lexp,lbangs = 1,1,1
                        n "He glanced around at all of his plants."
                        $ lbase,lexp,lbangs = 1,8,1
                        law "It's just something I do to keep busy..."
                        law "I mean, I need to have something to think about."
                        law "And... I like taking care of them."
                        $ lbase,lexp,lbangs = 1,10,1
                        n "He began look a little happier."
                        law "They're delicate."
                        law "..."
                        law "{size=12}I like the way they need me...{/size=12}"
                        menu:
                            "-Say nothing-":
                                $ lbase,lexp,lbangs = 1,2,1
                                n "He stopped talking abruptly."
                                $ lsanity -= 10
                                $ lbase,lexp,lbangs = 1,23,1
                                law "Never mind."
                                law "T...they're just plants."
                                call law_subroutine from _call_law_subroutine_11
                                jump law_day1_pacing
                            "\"That's why I like it too.\"":

                                $ lbase,lexp,lbangs = 1,19,1
                                n "He lit up."
                                $ lsanity += 20
                                $ law_love += 10
                                $ lbase,lexp,lbangs = 1,3,1
                                law "You understand?"
                                law "Ah..."
                                $ lbase,lexp,lbangs = 1,10,1
                                $ lblush = 3
                                law "It's kind of nice to meet someone that..."
                                $ lbase,lexp,lbangs,lblush = 2,10,1,1
                                law "W-well you know..."
                                $ lblush = 3
                                n "He trailed off."
                                jump law_day1_pacing

label law_day1_pacing:
show law zorder 1
$ lbase,lexp,lbangs = 1,16,1
n "He paused and took a deep breath."
$ lbase,lexp,lbangs,lblush = 1,13,1,0
law "Ugh..."
n "He began to pace around his apartment."
law "You..."
law "{size=12}What am I gonna do with you...{/size=12}"
show bg_lawapartment_sunrise zorder 0:
    subpixel True
    xalign 0.5
    alpha 0.0
    easeout 20 alpha 1.0
law "It's getting early..."
law "I... should just rest. I... I can't think straight right now."
n "I found myself wondering what time it was."
n "The sun was rising..."
n "But I was too frightened to feel tired."
$ lbase,lexp,lbangs = 1,6,1
law "You're probably tired too..."
law "You're probably diurnal, right?"
$ lbase,lexp,lbangs = 1,1,1
law "I kept you up all night..."
menu:
    "-Stay silent-":
        jump law_day1_tea
    "\"It's okay...\"":
        p "I don't mind."
        $ lbase,lexp,lbangs = 1,2,1
        $ law_love += 10
        law "O-oh.."
        jump law_day1_tea
    "\"I'm really not sleepy.\"":
        $ lbase,lexp,lbangs = 1,23,1
        $ lsanity -= 10
        law "You... I need you to sleep."
        call law_subroutine from _call_law_subroutine_12
        jump law_day1_tea
label law_day1_tea:
$ lbase,lexp,lbangs = 1,6,1
law "I'll just... make you some tea."
law "To help you sleep."
menu:
    "-Accept the tea-":
        n "He already had me taped to a chair... what was the point of refusing?"
        p "Um... thank you..."
        $ law_love += 10
        jump law_day1_accepttea
    "-Politely decline-":

        p "I'm sure I can fall asleep myself."
        $ lbase,lexp,lbangs = 1,6,1
        p "Thank you for the offer though!"
        n "I tried to sound as polite as I could."
        $ lsanity -= 10
        $ law_love -= 10
        call law_subroutine from _call_law_subroutine_13
        $ lbase,lexp,lbangs = 1,9,1
        law "You should drink it."
        n "It seemed less like a suggestion, and more like a warning..."
        menu:
            "-Accept the tea-":
                n "I decided that I wasn't in a position to argue."
                p "Okay, fine... I'll take the tea..."
                $ lbase,lexp,lbangs = 1,4,1
                n "He nodded silently and walked around me."
                jump law_day1_accepttea
            "-Firmly refuse-":
                jump law_day1_refusetea
    "-Firmly refuse-":
        jump law_day1_refusetea

label law_day1_refusetea:
    n "I certainly wasn't going to drink any 'tea' this guy gave me."
    p "I'm not going to drink anything."
    $ lsanity -= 10
    $ lbase,lexp,lbangs = 2,4,1
    n "He visibly tensed up."
    $ lbase,lexp,lbangs = 2,13,1
    law "..."
    call law_subroutine from _call_law_subroutine_14
    $ lbase,lexp,lbangs = 1,4,1
    law "I won't make you sleep."
    $ lbase,lexp,lbangs = 1,1,1
    law "...G-good...uh..."
    law "..."
    hide law
    show bg_lawrence_sleeping_sunrise zorder 1:
        subpixel True
        xalign 0.5
    stop music fadeout 3.0
    stop sound fadeout 3.0
    play sound law_day fadein 3.0 loop
    n "He gave up on talking, threw his sweater and shirt off, and climbed into his bed."
    n "I looked down."
    show bg_lawrence_sleeping_day zorder 2:
        subpixel True
        xalign 0.5
        alpha 0.0
        easeout 15 alpha 1.0
    show bg_lawapartment_day zorder 0:
        subpixel True
        xalign 0.5
        alpha 0.0
        easeout 15 alpha 1.0
    n "I sat in silence only broken by his soft breathing, the quiet humidifier in the room, and the random muffled thumps and shouts from other tenants of this building."
    n "I realized, despairingly, that even my own cries for help would probably be ignored in a noisy place like this..."
    n "I suppose my only options are... to sleep, or try and get out of this chair."
    label law_day1_strugglerest:
    menu:
        "-Struggle-":
            jump law_day1_struggle
        "-Rest-":
            jump law_day1_rest

label law_day1_struggle:
$ struggle += 1
if struggle == 1:
    n "I pulled at the tape around my wrists."
    n "I tried to be quiet, but the tape was so tight."
    $ sanity -= 10
    n "It didn't feel like it was budging at all."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        jump law_daychoke_shortcut
    jump law_day1_strugglerest
elif struggle == 2:
    n "I needed to keep trying."
    $ sanity -= 10
    n "I bit my lip and pulled hard against the tape."
    n "I froze when I heard Lawrence turn over."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        jump law_daychoke_shortcut
    jump law_day1_strugglerest
elif struggle == 3:
    n "My heart was pounding."
    n "I... have to..."
    $ sanity -= 10
    n "I tugged my arm with an involuntary grunt."
    hide bg_lawrence_sleeping_sunrise
    show bg_lawapartment_day zorder 0:
        subpixel True
        alpha 1.0
        xalign 0.5
        easeout 0.3 xalign 1.0
    show bg_lawrence_sleeping_day zorder 2:
        subpixel True
        alpha 1.0
        xalign 0.5
        easeout 0.3 xalign 1.0
    pause(0.5)
    n "Lawrence made a soft sound in bed."
    n "I froze again, sweat beading down my face."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        jump law_daychoke_shortcut
    show bg_lawapartment_day zorder 0:
        subpixel True
        xalign 1.0
        easeout 1.0 xalign 0.5
    show bg_lawrence_sleeping_day zorder 2:
        subpixel True
        xalign 1.0
        easeout 1.0 xalign 0.5
    pause(1.0)
    jump law_day1_strugglerest
elif struggle == 4:
    n "I steeled myself."
    n "I don't have a choice..."
    n "I wrenched my arm as hard as I could, feeling a release."
    n "However, my blood ran cold as I realized the tape had made a loud ripping sound."
    $ lsanity = 10
    label law_daychoke_shortcut:
    stop sound
    play music law_unsettled fadein 1.0
    law "...Ugh..."
    n "No no.... I looked down to my free arm in a panic."
    n "Should I try and replace the tape?"
    n "But I only have one hand free..."
    show bg_lawrence_sleeping_day:
        subpixel True
        alpha 1.0
        easeout 0.3 alpha 0.0
    pause(0.5)
    hide bg_lawrence_sleeping_day 
    n "My dilemma was interrupted by a hand slamming down on my wrist with a vicelike grip."
    n "I looked up with a strange yelp."
    show law
    $ lbase,lexp,lbangs = 9,25,3
    law "It's...It's the middle of the day."
    n "I wanted to say something, apologize, anything."
    n "But my brain wasn't forming words."
    n "I was wincing...He was a lot stronger than he first appeared to be."
    n "He squeezed harder for a moment before letting go."
    play sound law_brownnote fadein 1.0 loop
    law "These... are a problem."
    $ lbase,lexp,lbangs = 10,0,0
    n "He turned to dig around."
    $ lbase,lexp,lbangs = 11,25,3
    n "Before I could find my voice to ask what he was doing, he turned back to me."
    p "N...nonono..."
    $ sanity -= 10
    p "LAWRENCE!"
    $ lexp = 7
    n "He squinted coldly at me for a moment before retrieving his tape and a small cloth."
    law "This was all a mistake..."
    n "I tried to yell, but it was cut off by him shoving the cloth into my mouth and roughly slapping a piece of tape over it."
    $ lexp = 9
    n "He stopped to look over my panicking form, seeming to calm down slightly."
    n "I tried to shriek as he held down my free arm and position the saw just below my elbow."
    $ health -= 10
    $ sanity -= 10
    show cg_lawrence_sawing with dissolve
    n "The scene became blurry as tears filled my eyes and he made the first stroke, tearing through my skin."
    n "I screamed uselessly into the makeshift gag, trying to tear my arm from his grip."
    $ health -= 10
    $ sanity -= 10
    n "He held me down firmly and worked on my arm quickly."
    $ health -= 10
    $ sanity -= 10
    n "I felt like I was choking, struggling to breathe."
    $ health -= 20
    $ sanity -= 10
    n "I began to feel dizzy as I watched his muscles tense from the effort of sawing through my bone."
    n "I realized in a haze of blinding pain that he was holding my severed arm."
    n "He placed it gently on the ground and looked back to me, in my eyes."
    law "You're in pain..."
    n "He said it like he was describing some small miracle of nature."
    n "Like finding a butterfly's cocoon."
    n "I looked up at him dully, trying to move my hand and only feeling pain."
    law "I know it hurts now..."
    n "He moved and positioned the saw over my remaining arm."
    law "But that's just... natural."
    $ health -= 10
    $ sanity -= 10
    n "My body managed somehow to renew its panic as he moved the saw again."
    n "I helplessly shuddered and sobbed as he tore through the flesh."
    n "I felt a small wave of relief as I began to go numb."
    n "He held my other arm, my blood splattered all over his body."
    law "Heh..."
    law "You're dripping..."
    scene black with dissolve
    $ health -= 5
    $ sanity -= 10
    stop music fadeout 3.0
    n "Am I?"
    n "My arms were cold."
    n "My... my arms."
    $ health -= 5
    $ sanity -= 10
    law "...I'll take the rest of you to somewhere pretty."
    n "That sounds nice."
    $ health -= 100
    n "I felt my head drop."
    law "I'll find you again..."
    $ sanity -= 100
    $ health -= 100
    scene black with dissolve
    law "In the dark."
    stop sound fadeout 1.0
    play music law_twinkle fadein 1.0
    hide screen health_bar
    hide screen sanity_bar
    hide screen sanity_bar_law
    $ persistent.law_ending_disarmed = True
    scene endslate with Dissolve(1.0)
    screen law_ending_disarmed:
        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}Lawrence took your arms.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen law_ending_disarmed
    with Dissolve(1.0)
    pause
    $ renpy.full_restart()

label law_day1_rest:
n "My exhaustion and the quiet surroundings were getting to me."
n "I eventually let my head fall to my chest."
scene black with dissolve
n "I dropped into a restless sleep."
pause(1)
jump law_night2

label law_day1_accepttea:
stop music fadeout 3.0
play sound law_day fadein 1.0
hide law
n "He started moving somewhere behind me to make the tea."
hide bg_law_apartment
show bg_lawapartment_sunrise zorder 0:
    alpha 1.0
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.0
n "I strained to see what he was doing but I couldn't turn my head enough."
show bg_lawapartment_sunrise zorder 0:
    subpixel True
    xalign 0.0
    easeout 0.5 xalign 0.5
n "I could only try to relax as I heard him quietly clinking objects out of my view."
n "After waiting in silence, looking at his plants, and hearing some kind of humidifier in the room, I began to feel genuinely tired."
show law
$ lbase,lexp,lbangs = 1,1,1
law "It should be cool enough now..."
n "He returned and glanced at my arms, still taped to the chair."
if law_love >= 30:
    $ lbase,lexp,lbangs,lblush = 1,24,1,1
else:
    $ lbase,lexp,lbangs = 1,23,1
law "Oh..."
n "He leaned forward and brought the cup of tea to my lips gently."
n "It was very warm, and tasted unfamiliar, but not bad."
play music law_haunt fadein 1.0
n "I tried to drink it fairly quickly, but I began to feel a bit strange about halfway through."
p "W...what... is this...?"
$ lbase,lexp,lbangs,lblush = 1,42,1,0
law "...It's proof..."
$ sanity -= 10
law "It doesn't take much to change everything."
show black:
    subpixel True
    alpha 0.0
    easeout 0.5 alpha 0.9
    easeout 1.0 alpha 0.0
p "..What..."
n "This wasn't any normal tea..."
scene black with dissolve
n "As I was about to pass out, I finally recognized that sickly sweet smell."
n "It was him."
$ sanity -= 20
n "It smelled like something rotting."
$ drugs += 1
pause(1)
jump law_night2

label law_night2:
stop music fadeout 1.0
stop sound fadeout 1.0
if lsanity <= 50:
    $ law_crazy = True
if drugs >= 2:
    n "My head was pounding and it took a moment to register my own dry mouth."
n "I slowly opened my eyes."
call law_subroutine from _call_law_subroutine_15
scene bg_lawapartment_sunset with dissolve
show law zorder 2
$ lbase,lexp,lbangs = 2,1,1
play music law_haunt fadein 1.0
law "You're awake."
n "I jolted upright in the chair."
n "H...how long was he watching me!?"
if law_love < 30:
    law "I've had some time to think about it."
    $ lbase,lexp,lbangs = 2,8,1
    law "Uh... you."
    law "And..."
    $ lbase,lexp,lbangs = 1,6,1
    show bg_lawapartment zorder 0:
        subpixel True
        xalign 0.5
        alpha 0.0
        easeout 15 alpha 1.0
    $ sanity -= 10
    law "I can't let you go."
    n "He leaned in closer."
    $ lbase,lexp,lbangs = 2,3,1
    law "Y-you understand, right?"
else:
    $ lbase,lexp,lbangs,lblush = 2,10,1,1
    show bg_lawapartment zorder 0:
        subpixel True
        xalign 0.5
        alpha 0.0
        easeout 15 alpha 1.0
    law "You're beautiful..."
    n "I felt my cheeks redden, shocked."
    p "What...?"
    n "His fingers trailed down my neck as he ignored my question."
    law "I wasn't looking properly before."
    $ lexp = 24
    law "...You were asleep for a long time."
    n "He touched the back of my neck."
    $ lblush = 3
    law "I need to..."
    show law:
        subpixel True
        alpha 1.0
        xalign 0.5
        easeout 0.2 alpha 0.0 xalign 0.6
    n "I watched as he picked up something from the table and moved quickly behind me."
    play sound law_brownnote fadein 5.0 loop
    p "What are you doing?"
    n "I felt something cold and sharp touch the nape of my neck."
    n "My voice rose in panic as I repeated myself."
    p "{b}What are you doing!?{/b}"
    $ sanity -= 10
    $ health -= 5
    p "Sto- AH!"
    law "I love the curve..."
    $ health -= 5
    n "I wimpered as the sharp pain increased."
    law "Of your spine..."
    scene bg_law_apartment:
        subpixel True
        xalign 0.5
        easeout 0.2 xalign 0.0
        pause 0.2
        easeout 0.2 xalign 1.0
        pause 0.2
        easeout 0.2 xalign 0.5
    n "I desperately tried to look at him."
    $ sanity -= 10
    n "I cried out as the movement hurt my neck more."
    n "He sighed happily as I felt something warm run down my back."
    p "Please, Lawre-"
    n "He placed one hand over my mouth, muffling the rest of my begging."
    $ health -= 5
    n "I groaned into his hand as he cut further down, from the back of my neck to between my shoulder blades."
    $ health -= 5
    $ sanity -= 10
    n "I almost took in a whole breath of relief before I felt him push a finger into the opening."
    $ health -= 10
    n "His grip tightened and I screamed behind his hand as he slid his finger down the open wound on my neck."
    n "I was shaking and blood was running down my back now."
    n "I could feel it soaking my shirt."
    law "{size=12}I want to keep it.{/size}"
    call law_subroutine from _call_law_subroutine_32
    n "He breathed softly right next to my ear and moved his hands to rub his fingers around my back to my collar."
    n "I imagined it must look like I was wearing a necklace out of my own blood now."
    show law:
        subpixel True
        alpha 0.0
        xalign 0.4
        easeout 0.2 alpha 1.0 xalign 0.5
    $ lblush = 1
    stop sound fadeout 1.0
    n "He stepped back into my view as I gulped, beginning to feel lightheaded."
    $ sanity -= 10
    law "I can't let you go."
    $ lblush = 3
    n "He leaned in closer."
    $ lbase,lexp,lbangs = 2,3,1
    $ lblush = 0
    law "Y-you understand, right?"
menu:
    "\"I understand...\"":
        $ lsanity += 10
        $ lbase,lexp,lbangs = 1,19,1
        $ law_love += 10
        n "I didn't want to upset him..."
        law "That's a relief..."
        n "He sighed softly, still hovering over me slightly."
        $ lbase,lexp,lbangs = 1,16,1
        law "I was thinking..."
        law "You and I could, uh... do a project."
        p "A... project?"
        $ lbase,lexp,lbangs = 1,19,1
        law "This is perfect."
        n "He reached out to touch my hair, but he moved so gently that I didn't flinch away."
        jump law_night2_wristcut
    "\"What!? No!\"":
        $ lbase,lexp,lbangs = 1,2,1
        $ lsanity -= 20
        p "You can't just keep me here like this!!"
        n "I pulled at the tape around my arms, beginning to panic."
        call law_subroutine from _call_law_subroutine_16
        $ lbase,lexp,lbangs = 1,13,1
        n "He ignored my struggling and stayed close."
        law "That's not true..."
        play music law_unsettled fadein 1.0
        law "I can keep you here."
        $ sanity -= 10
        law "I could do anything to you..."
        n "He placed his hand on my knee, but it did nothing to reassure me."
        law "Your thread is mine."
        $ lbase,lexp,lbangs = 1,19,1
        law "That's what makes this so beautiful."
        law "You're so brittle now."
        law "And... temporary."
        n "I glared up at him, trying to keep the tears at the corner of my eyes from falling."
        law "I couldn't help but notice in the bar, the way you came up to me."
        law "Confident...normal..."
        law "Despite all the things in this world fighting and dying in chaos."
        $ lbase,lexp,lbangs = 1,23,1
        law "Looking at you now, with your pretty face, even when you're crying..."
        $ lbase,lexp,lbangs = 1,19,1
        law "I envy you."
        n "I balked as he sighed wistfully."
        $ sanity -= 20
        law "I wish I could peel your skin away and crawl inside it..."
        $ lbase,lexp,lbangs = 1,11,1
        n "He laughed softly."
        call law_subroutine from _call_law_subroutine_17
        law "But that wouldn't work."
        $ lbase,lexp,lbangs = 1,12,1
        law "Ah."
        n "He finally drew back from me."
        play music law_haunt fadein 1.0
        law "...Anyway..."
        law "Let's get started."
        jump law_night2_wristcut
    "\"Please, at least let me use the bathroom?\"":
        n "I asked him desperately."
        n "I did want to try and get away..."
        n "But it was also true."
        if law_love >= 30:
            jump law_night2_bathroom
        else:
            $ lbase,lexp,lbangs = 1,9,1
            law "Hrn..."
            law "No."
            $ lbase,lexp,lbangs = 1,13,1
            law "I don't think so."
            law "..."
            law "Don't worry."
            $ lbase,lexp,lbangs = 1,4,1
            $ sanity -= 10
            law "I'm not going to keep you much longer."
            call law_subroutine from _call_law_subroutine_18
            jump law_night2_wristcut

label law_night2_bathroom:
$ lbase,lexp,lbangs = 1,1,1
law "..."
$ lbase,lexp,lbangs = 1,8,1
law "I...I guess it's okay."
n "My eyes widened."
n "That really worked!?"
$ lbase = 26
n "I waited patiently as he pulled out a small knife."
law "I'm going to cut the tape."
$ lbase,lexp,lbangs = 1,16,1
law "Then... uh..."
law "You can use the bathroom."
$ lbase,lexp,lbangs = 1,9,1
law "And after..."
law "J-just sit back in the chair."
law "Got it?"
n "I nodded eagerly."
p "Of course."
$ lbase,lexp,lbangs = 1,16,1
n "He silently cut through the tape."
$ lbase = 26
law "...There."
law "Go...ahead..."
show bg_lawapartment zorder 0:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.3 xalign 0.0
show law zorder 1:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 0.9
n "I hoisted myself up shakily."
n "He was watching me carefully...still holding that knife."
scene black with dissolve
n "I slipped into the small dark bathroom and closed the door."
stop sound fadeout 1.0
stop music fadeout 1.0
scene bg_law_bathroom
pause(0.01)
scene black
pause(0.01)
scene bg_law_bathroom
pause(0.01)
scene black
pause(0.01)
play sound law_day fadein 1.0 loop
scene bg_law_bathroom with dissolve
n "Then flicked on the light."
n "I gasped quietly."
n "...Even more plants."
n "It's so warm and musty..."
n "I sighed, gathering my thoughts."
n "Okay."
menu:
    "-Freshen up-":
        n "Well..."
        n "As long as I'm here..."
        n "I used the bathroom and washed up."
        $ sanity += 20
        n "It helped me feel a little better at least..."
        menu:
            "-Examine the room-":
                n "I looked around the bathroom."
                n "I couldn't find anything even close to a weapon..."
                n "There were no windows either."
                n "There's no way out..."
                n "I checked the medicine cabinet."
                n "Only a whole bunch of jars and bowls filled with various powders and liquids."
                if health < 80:
                    n "I rolled my shoulders and hissed in pain."
                    n "Maybe there's something in here that can help..."
                    n "Everything looked... homemade."
                    n "Barely anything was labelled, and the few things that had labels were cryptically scrawled."
                    n "I eventually picked out two that looked promising."
                    n "One was a clear liquid in a bottle labelled 'NUMB'."
                    n "The other was a thick, syrupy amber liquid in a jar labelled 'for pain'."
                    menu:
                        "-Drink from the bottle labelled 'NUMB'-":
                            n "I narrowed my eyes at the bottle."
                            n "If it hurts less, I can think more clearly."
                            n "If I can think clearly...maybe I can make it out of here."
                            n "I popped the top off the bottle, half expecting it to be like water."
                            n "I was suprised by a strong flowery fragrance."
                            n "Of course there's no dosage instructions..."
                            n "Pretty much everything for adults is like, a tablespoon though right?"
                            n "I gathered my courage and took a small sip."
                            n "It didn't have much of a flavour... but..."
                            $ drugs += 1
                            $ health += 20
                            n "After a surprisingly short few minutes, my pain began to subside."
                            n "I let out a triumphant breath."
                            $ sanity += 20
                            n "This feels great!"
                            n "Even better than before!"
                            n "I put the bottle down sloppily and wobbled on my feet."
                            n "I looked at the door."
                        "-Drink from the jar labelled 'for pain'-":
                            n "I squinted at the jar."
                            n "Well I have to do something."
                            n "It really hurts..."
                            n "I shakily pried open the jar."
                            n "It says it's for pain. Pretty self explanitory."
                            n "It smelled sweet... is this just honey?"
                            n "Not seeing a spoon or anything, I just tilted the jar to my lips."
                            n "I'm sure it's-"
                            p "Auck!"
                            n "I coughed and gripped the sink." with vpunch
                            n "It tastes awful!!"
                            n "I grimaced and concentrated on swallowing the thick and sticky substance."
                            $ drugs += 1
                            p "Uughh..."
                            n "I put the jar down and waited for something to happen."
                            n "After a few moments, my injuries started to feel..."
                            n "I leaned forward."
                            $ health -= 10
                            $ sanity -= 10
                            n "It hurts!"
                            n "I shuddered and supressed a whimper."
                            n "It hurts more!!"
                            $ health -= 10
                            $ sanity -= 10
                            n "I slumped against the door as the deep, dull pain spread to the rest of my body."
                            n "Fuck..."
                        "-Leave both alone-":
                            n "I set them down."
                            n "This is stupid."
                            n "I really shouldn't be taking mystery 'medicine' from the bathroom of a psychopath."
                menu:
                    "-Lock the door-":
                        jump law_night2_bathroom_lock
                    "-Leave-":
                        jump law_night2_bathroom_leave
            "-Lock the door-":
                jump law_night2_bathroom_lock
            "-Leave-":
                jump law_night2_bathroom_leave
    "-Examine the room-":
        n "I looked around the bathroom."
        n "I couldn't find anything even close to a weapon..."
        n "There are no windows either."
        n "There's no way out..."
        n "I checked the medicine cabinet."
        n "Only a whole bunch of jars and bowls filled with various powders and liquids."
        if health < 80:
            n "I rolled my shoulders and hissed in pain."
            n "Maybe there's something in here that can help..."
            n "Everything looked... homemade."
            n "Barely anything was labelled, and the few things that had labels were cryptically scrawled."
            n "I eventually picked out two that looked promising."
            n "One was a clear liquid in a bottle labelled 'NUMB'."
            n "The other was a thick, syrupy amber liquid in a jar labelled 'for pain'."
            menu:
                "-Drink from the bottle labelled 'NUMB'-":
                    n "I narrowed my eyes at the bottle."
                    n "If it hurts less, I can think more clearly."
                    n "If I can think clearly...maybe I can make it out of here."
                    n "I popped the top off the bottle, half expecting it to be like water."
                    n "I was suprised by a strong flowery fragrance."
                    n "Of course there's no dosage instructions..."
                    n "Pretty much everything for adults is like, a tablespoon though right?"
                    n "I gathered my courage and took a small sip."
                    n "It didn't have much of a flavour... but..."
                    $ drugs += 1
                    $ health += 20
                    n "After a surprisingly short few minutes, my pain began to subside."
                    n "I let out a triumphant breath."
                    $ sanity += 20
                    n "This feels great!"
                    n "Even better than before!"
                    n "I put the bottle down sloppily and wobbled on my feet."
                    n "I looked at the door."
                "-Drink from the jar labelled 'for pain'-":
                    n "I squinted at the jar."
                    n "Well I have to do something."
                    n "It really hurts..."
                    n "I shakily pried open the jar."
                    n "It says it's for pain. Pretty self explanitory."
                    n "It smelled sweet... is this just honey?"
                    n "Not seeing a spoon or anything, I just tilted the jar to my lips."
                    n "I'm sure it's-"
                    p "Auck!"
                    n "I coughed and gripped the sink." with vpunch
                    n "It tastes awful!!"
                    n "I grimaced and concentrated on swallowing the thick and sticky substance."
                    $ drugs += 1
                    p "Uughh..."
                    n "I put the jar down and waited for something to happen."
                    n "After a few moments, my injuries started to feel..."
                    n "I leaned forward."
                    $ health -= 10
                    $ sanity -= 10
                    n "It hurts!"
                    n "I shuddered and supressed a whimper."
                    n "It hurts more!!"
                    $ health -= 10
                    $ sanity -= 10
                    n "I slumped against the door as the deep, dull pain spread to the rest of my body."
                    n "Fuck..."
                "-Leave both alone-":
                    n "I set them down."
                    n "This is stupid."
                    n "I really shouldn't be taking mystery 'medicine' from the bathroom of a psychopath."
        menu:
            "-Freshen up-":
                n "Well..."
                n "As long as I'm here..."
                n "I used the bathroom and washed up."
                $ sanity += 20
                n "It helped me feel a little better at least..."
                menu:
                    "-Lock the door-":
                        jump law_night2_bathroom_lock
                    "-Leave-":
                        jump law_night2_bathroom_leave
            "-Lock the door-":
                jump law_night2_bathroom_lock
            "-Leave-":
                jump law_night2_bathroom_leave
    "-Lock the door-":
        jump law_night2_bathroom_lock
    "-Leave-":
        jump law_night2_bathroom_leave

label law_night2_bathroom_leave:
n "I guess... I better go back out there."
n "I don't want to make him angry and there doesn't seem to be a better choice."
n "I chewed my lip as I held the doorknob."
n "There's no better choice."
show bg_lawapartment with dissolve
n "I creaked the door open and came out meekly."
n "He was standing between me and the door out of the apartment."
n "I looked at the chair."
n "My prison."
n "And I sat down."
play music law_haunt fadein 1.0
show law with dissolve
$ lbase,lexp,lbangs = 1,16,1
law "..."
$ lbase,lexp,lbangs = 2,10,1
$ law_love += 10
law "Um, thanks for... doing what I said."
$ lbase,lexp,lbangs = 2,24,1
call law_subroutine from _call_law_subroutine_19
n "He mumbled something very quietly about 'tape.'"
p "...Oh."
n "He held up his roll of duct tape."
n "I felt like I might be getting somewhere on his good side."
$ law_love += 10
n "So I held my arms to the arms of the chair for him."
$ lbase,lexp,lbangs = 2,22,1
n "He paused for a moment."
$ lbase,lexp,lbangs = 1,24,1
n "He wrapped the tape around my arms."
n "He seemed to be careful to do it gently."
n "Once he was done, he leaned back and looked away."
$ lbase,lexp,lbangs = 1,1,1
law "I.. I need to go out now."
$ lbase,lexp,lbangs = 2,8,1
law "I'll...be back later..."
law "So I guess..."
law "Um, maybe just rest... okay?"
n "I nodded to him but I don't think he even saw me."
stop music fadeout 1.0
show law:
    xalign 0.5
    alpha 1.0
    easeout 0.1 xalign 0.6 alpha 0.0
n "He moved quickly to leave the apartment."
n "I couldn't see him leave behind me."
n "I sat in the chair alone, in the relative silence again."
n "Just the sound of muffled neighbors, distant car horns, and that soft hissing of the humidifier."
n "I rested my eyes."
stop sound fadeout 1.0
scene black with dissolve
n "And slipped into a deep sleep."
pause(1.5)
jump law_day3

label law_night2_bathroom_lock:
n "This door locks from the inside..."
n "Maybe..."
n "I can wait him out."
n "I tried to turn the lock carefully, but it still made a loud click."
n "My heart was pounding."
pause(1.5)
law "%(player_name)s?"
n "I kept holding the doorknob, beginning to sweat."
n "I heard his footsteps..."
n "I gasped as the door shook in my grip."
pause(1.5)
$ lsanity -= 10
play music law_unsettled fadein 40.0
law "Come out %(player_name)s."
n "I can't give in."
n "I can wait him out."
n "I turned around and pressed my back to the door."

label law_night2_bathroom_lock_loop:
if lsanity < 5:
    jump law_night2_drown
$ ui.timer((1.5), ui.jumps("law_night2_bathroom_lock_loop"))
$ lsanity -= 5
if lsanity == 50:
    menu:
        law "{size=30}%(player_name)s!!{/size}{w=3.0}"
        "-Give up-":
            jump law_night2_bathroom_lock_giveup
    pause(3.0)
if lsanity == 30:
    menu:
        n "-BANG BANG-{w=3.0}"
        "-Give up-":
            jump law_night2_bathroom_lock_giveup
    pause(3.0)
if lsanity == 25:
    menu:
        n "-BANG BANG BANG-{w=3.0}"
        "-Give up-":
            jump law_night2_bathroom_lock_giveup
    pause(3.0)
if lsanity == 20:
    menu:
        n "{size=30}-BANG BANG-{/size}{w=3.0}"
        "-Give up-":
            jump law_night2_bathroom_lock_giveup
    pause(3.0)
if lsanity == 15:
    menu:
        law "........{w=3.0}"
        "-Give up-":
            jump law_night2_bathroom_lock_giveup
    pause(3.0)
menu:
    "-Give up-":
        jump law_night2_bathroom_lock_giveup

label law_night2_drown:
pause (1.5)
$ health -= 20
stop sound
stop music
scene black with vpunch
n "I heard a loud crack and was only aware for a second that I was flying forward, my head colliding with the edge of the tub."
pause(1.5)
play sound law_brownnote fadein 1.0 loop
n "Ugh...what..."
n "My head hurt."
n "I couldn't move; didn't want to open my eyes."
n "Rushing water..."
n "Water?"
play music law_kill fadein 1.0
scene cg_lawrence_drown with dissolve
n "I couldn't breathe."
n "What's happening!?"
$ health -= 20
$ sanity -= 20
n "I tried fighting, clawing."
n "I could tell I was underwater..."
n "But Lawrence's iron grip tightening around my throat was barely letting it in my windpipe."
n "The last few bubbles I had escaped my lips as my thrashing grew weaker."
$ health -= 20
$ sanity -= 20
n "N...no..."
n "My chest burned as I heaved, trying desperately to suck in the water around me."
n "I couldn't do anything."
$ health -= 100
$ sanity -= 100
stop sound fadeout 1.0
stop music fadeout 1.0
scene black with dissolve
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_drown = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_drown:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence held you under.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_drown
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_night2_bathroom_lock_giveup:
n "I can't do this!!!"
p "I...I'm coming out!"
pause(1.5)
n "I heard him step away from the door."
n "He didn't say anything..."
n "I squeezed my eyes shut and unlocked the door."
n "..."
show bg_law_apartment:
    subpixel True
    xalign 0.0
    alpha 0.0
    easeout 0.5 alpha 1.0
n "I stepped out slowly, looking around."
scene bg_law_apartment:
    subpixel True
    xalign 0.0
    easeout 0.5 xalign 1.0
n "W...where..."
scene bg_law_apartment:
    subpixel True
    xalign 1.0
    easeout 0.2 xalign 0.0
show law:
    subpixel True
    xalign -0.3
    easeout 0.2 xalign 0.5
$ lbase,lexp,lbangs = 1,21,1
play music law_kill fadein 1.0
p "AHH!" with hpunch
n "He twisted my arm behind me and pinned me to the wall."
p "L-Lawre-"
$ lbase,lexp,lbangs = 1,7,1
$ sanity -= 10
law "Quiet." with hpunch
n "He pressed his body against mine harshly, wrenching my arm painfully."
n "I wheezed softly, unable to take a breath or speak."
n "My struggle was only punctuated by his ragged breathing."
n "It was right next to my ear... in my neck..."
n "I kept still, hoping he'd calm down."
n "...He began to pull away."
n "I took in a deep breath-"
$ health -= 10
scene black with hpunch
n "Only to have it knocked out of me by a sharp blow to my ribs."
n "I crumpled to the floor, clutching my side."
n "My mind was screaming at me to apologize."
n "I croaked out a sob."
call law_subroutine from _call_law_subroutine_20
n "I opened my eyes for just long enough to see him readying a kick."
p "N-"
$ health -= 20
n "It slammed into me and smashed me into the wall." with hpunch
n "I couldn't make a sound, I couldn't move."
n "All I had was pain and a struggle to breathe."
n "I felt the warmth of tears streaking down my face."
scene cg_lawrence_stepping with dissolve
n "I looked up at him."
law "..."
law "You're mine now."
n "He pressed his foot to my neck, slowly pushing me down to the floor."
law "Do you understand?"
p "Hchh...y.."
n "I couldn't get the words out. I couldn't breathe."
n "I tried nodding desperately."
stop music fadeout 1.0
n "He sighed...with relief."
scene black with dissolve
scene bg_law_apartment with dissolve
show law with dissolve
$ lbase,lexp,lbangs = 1,4,1
play music law_haunt fadein 1.0
n "He stepped back and grabbed my arm to help me stand."
n "Why was he being so gentle now!?"
n "He led me back to the chair."
n "I didn't fight him."
n "I sat and he bent to bind my legs to the chair."
$ lbase,lexp,lbangs = 1,16,1
law "...There."
n "I sat there in shock, breathing hard."
call law_subroutine from _call_law_subroutine_21
$ lbase,lexp,lbangs = 1,13,1
n "I barely noticed him moving until he placed a large metal bucket in front of me."
p "What's...that?"
jump law_night2_wristcut_frombeating


label law_night2_wristcut:
$ lbase,lexp,lbangs = 1,8,1
n "I looked at him questioningly and he bent to grab a large metal bucket."
p "What... do you mean?"
n "He placed the bucket in front of my legs with a soft clank."
n "I looked down into the empty bucket, dread tightening in my gut."
if law_love >= 50:
    $ lexp = 23
    law "I know this isn't fair."
    law "{size=12}Life isn't fair....{/size}"
    n "It almost seemed like he was stalling."
    n "Even though I was the one taped to a chair."
    law "I can tell by your face..."
    $ lexp = 16
    law "You're gentle."
    law "And the world's like a loaded gun..."
    $ lexp = 23
    law "Normally I don't care."
    law "But you're different."
    law "I wish I could tell you that it's going to be okay."
$ lbase,lexp,lbangs = 26,4,1
play music law_unsettled fadein 1.0
n "My attention was caught by the glint of a knife in his hand."
if law_love >= 50:
    law "But it isn't."
n "I wanted to cry out in fear, but that same dread choked me up as he moved the knife."
scene black
law "..."
law "There."
pause(1.0)
stop music fadeout 0.5
play sound law_day fadein 1.0 loop
n "The pain I was expecting never came."
scene bg_law_apartment
show law
n "I looked down."
n "He tore off the cut tape from around my arms."
$ lbase,lexp,lbangs = 1,1,1
n "I looked back up at him."
p "Are you...letting me go?"
stop sound fadeout 0.5
play music law_haunt fadein 1.0
$ lbase,lexp,lbangs = 1,8,1
law "No."
law "I need to...um..."
label law_night2_wristcut_frombeating:
law "I need to get your blood out."
p "W-what!?"
$ lbase,lexp,lbangs = 1,23,1
law "It won't hurt!"
law "Ah...I've got some...medicine."
$ lbase,lexp,lbangs = 1,1,1
law "'Drugs' I guess."
$ lbase,lexp,lbangs = 1,6,1
law "Just some tea."
law "And you won't feel a thing."
menu:
    "\"No way!\"":
        $ law_wrist_drug = False
        $ lbase,lexp,lbangs = 1,2,1
        p "I'm not drinking anything you give me!"
        n "I pushed away from him as hard as I could in the chair."
        $ lbase,lexp,lbangs = 1,23,1
        $ lsanity -= 20
        law "W-well...fine."
        $ lbase,lexp,lbangs = 1,25,1
        law "I guess it doesn't matter if it hurts."
        call law_subroutine from _call_law_subroutine_22
    "\"...Okay.\"":
        $ law_wrist_drug = True
        n "There's no point in suffering needlessly I guess."
        n "He grabbed a water bottle from near his plants."
        law "Uh... it's not hot or anything."
        $ lbase,lexp,lbangs = 1,1,1
        law "Here."
        n "He held the bottle out to me."
        n "It looked like any plain water bottle a jogger would have..."
        n "Happy to finally have the use of my hands back, I took it and held it to my mouth."
        n "It tasted bitter and strange."
        $ lbase,lexp,lbangs = 1,2,1
        law "U-uh! Not so much!"
        n "He took the bottle from me firmly."
        $ lbase,lexp,lbangs = 1,1,1
        law "Just a little should be enough..."
        $ drugs += 1
        n "I considered answering him, but I was distracted by my fingers beginning to tingle."
        call law_subroutine from _call_law_subroutine_23
        p "Oh..."
        n "The feeling spread incredibly quickly."
        n "Like falling into a pit full of those cold glass beads people put in the bottom of a fish tank."
        $ lbase,lexp,lbangs = 1,23,1
        n "My whole body was numb."
        $ lbase,lexp,lbangs = 1,6,1
        law "There."
        law "It... it'll be easier now."
n "He held the knife he cut my tape with, turning it over a bit."
n "I was watching the blade when he gripped my wrist tightly."
n "He licked his lips absentmindedly as he gently moved his thumb over my wrist."
$ lbase,lexp,lbangs = 1,23,1
n "He was feeling me and concentrating..."
n "Then, suddenly, he stopped."
n "And lowered the knife to my skin."
menu:
    "-Pull Away-":
        $ lbase,lexp,lbangs = 1,2,1
        $ lsanity -= 10
        $ sanity -= 10
        n "I jerked my wrist away from him." with hpunch
        p "Stop!"
        call law_subroutine from _call_law_subroutine_24
        $ lbase,lexp,lbangs = 1,21,1
        play music law_unsettled fadein 1.0
        law "DON'T..."
        $ lbase,lexp,lbangs = 26,7,1
        if law_wrist_drug == True:
            n "He tightened his grip painfully and spoke in a quiet tone, dripping with threat."
        else:
            n "He tightened his grip and spoke in a quiet tone, dripping with threat."
        law "Don't fight me, %(player_name)s."
        $ lexp = 9
        law "Your path..."
        law "I'm guiding it now."
        law "Do you understand?"
        n "I looked back at him, unable to find my words."
        n "I was shocked at his sudden change in demeanor."
        $ lbase = 1
        n "He lowered the knife back to my skin."
        $ lbase,lexp,lbangs = 1,25,1
        law "...Well?"
        menu:
            "-Let him cut-":
                jump law_wrist_shortcut
            "-Scream-":

                jump law_wrist_scream
            "-Beg-":

                jump law_wrist_beg
    "-Let him cut-":

        label law_wrist_shortcut:
        play sound law_brownnote fadein 1.0 loop
        n "I froze."
        if law_wrist_drug == True:
            $ health -= 5
            $ lbase,lexp,lbangs = 1,23,1
            n "He pressed the knife through my skin."
            n "I could only feel the same tingling sensation and the light pressure of the knife."
            $ health -= 5
            n "It sank deeper into my wrist and I knew it should be hurting..."
            n "But I just watched...transfixed."
            $ health -= 5
            $ lbase,lexp,lbangs = 1,16,1
            n "He was breathing slowly and evenly as he carefully pulled the blade along my largest vein."
            $ health -= 5
            n "I watched my blood well up, flow around my wrist, and drip quietly into the bucket below."
            call law_subroutine from _call_law_subroutine_25
        if law_wrist_drug == False:
            $ health -= 5
            $ lbase,lexp,lbangs = 1,23,1
            n "He pressed the knife through my skin."
            $ sanity -= 5
            n "I jerked and gasped as pain shot up my arm."
            $ lbase,lexp,lbangs = 1,9,1
            n "His grip tightened painfully around my wrist."
            law "Shh."
            law "You chose to feel this."
            call law_subroutine from _call_law_subroutine_26
            $ health -= 5
            $ sanity -= 5
            n "The rest of my body shook, but he held my arm perfectly still and kept raking the knife through my flesh."
            n "It hurt like fire and I squirmed uselessly."
            n "But I couldn't stop watching."
            $ health -= 5
            $ lbase,lexp,lbangs = 1,16,1
            n "He was breathing slowly and evenly as he carefully pulled the blade along my largest vein."
            $ health -= 5
            n "He paid no attention to my whimpers or the tears streaming down my face."
            n "I saw my blood well up over my shaking wrist, then flow into the bucket below."
            call law_subroutine from _call_law_subroutine_27
        jump law_night2_wristcut2
    "-Grab the knife-":

        $ lbase,lexp,lbangs = 1,2,1
        n "I reflexively grabbed for the knife."
        law "Wha-"
        n "I managed to take it from his hands."
        $ lbase,lexp,lbangs = 1,21,1
        play music law_kill fadein 1.0
        n "We locked eyes, both of us calculating the situation."
        show law:
            xalign 0.5
            alpha 1.0
            easeout 0.2 xalign 0.6 alpha 0.0
        n "He stepped back out of my reach."
        n "This fucking chai-"
        n "Oh."
        n "I bent down quickly to cut the tape around my legs."
        show cg_lawrence_upsidedown with vpunch
        n "I got through one as quickly as I could when I felt my head snap back up, pulled by my hair."
        p "AUGH N-"
        n "My words were stopped by the large blade of garden shears on my neck."
        law "Drop it."
        menu:
            "-Drop the knife-":
                n "My hands were shaking."
                scene black with dissolve
                play music law_unsettled fadein 1.0
                n "I dropped his weapon, squeezing my eyes shut in defeat."
                scene bg_law_apartment
                show law
                $ lbase,lexp,lbangs = 1,25,1
                n "He pressed the shears against my throat as a last warning before lowering them and picking up the knife."
                $ lbase,lexp,lbangs = 1,4,1
                n "He retaped my leg as I watched..."
                n "For a moment, I wondered if I had made the wrong choice."
                n "But I didn't have time to think about it for long."
                n "He went right back to work."
                n "He pressed the knife back to my wrist."
                law "Just relax."

                jump law_wrist_shortcut
            "-Refuse-":
                n "I held the knife tightly, and braced myself to swipe at him."
                p "K...gh.."
                scene cg_lawrence_upsidedown2 with dissolve
                n "He held my head back still, as blood poured from my throat and mouth."
                scene black with dissolve
                $ health -= 100
                $ sanity -= 100
                n "...Fuck."
                hide screen health_bar
                hide screen sanity_bar
                hide screen sanity_bar_law
                $ persistent.law_ending_throat = True
                play music law_twinkle fadein 1.0
                scene endslate with Dissolve(1.0)
                screen law_ending_throat:
                    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                    text "\n\n\n\n{=endslate_subtitle}You were too slow.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                show screen law_ending_throat
                with Dissolve(1.0)
                pause
                $ renpy.full_restart()

label law_wrist_scream:
    $ lbase,lexp,lbangs = 1,14,1
    $ lsanity -= 30
    n "I screamed as loud as I could."
    $ lbase,lexp,lbangs = 1,21,1
    n "Maybe someone would hear me before-"
    $ lbase,lexp,lbangs = 1,7,1
    $ sanity -= 10
    n "His hand clamped over my throat with so much force that the chair almost tipped backwards." with vpunch
    n "For a moment we were both still and silent."
    n "I heard a muted thumping from above accompanied by the muffled voice of an older man upstairs."
    n "\"Shut the fuck up!\""
    n "Lawrence's hand was still on my neck."
    $ lbase,lexp,lbangs = 1,43,1
    law "{size=24}Sorry Mr. Davidson!{/size}"
    $ lbase,lexp,lbangs = 1,11,1
    law "It won't happen again."
    n "His grip tightened."
    $ health -= 15
    $ sanity -= 15
    n "I was beginning to see spots."
    $ lbase,lexp,lbangs = 1,21,1
    law "Will it?"
    n "I tried to shake my head, even though I could barely move it."
    $ lbase,lexp,lbangs = 1,4,1
    n "With one last warning squeeze, he let go of me."
    n "I wheezed and coughed, trying to suck in air quickly."
    if lsanity >= 50:
        if sanity <= 10:
            n "I couldn't think."
            n "My visioned wavered for a moment."
            $ lbase,lexp,lbangs = 1,13,1
            law "..."
            law "Keeping you here isn't working."
            n "I gulped, watching him."
            n "He seemed to be thinking hard."
            $ lbase,lexp,lbangs = 1,9,1
            law "Would you like to leave this place?"
            n "I wanted to answer."
            n "But I couldn't think."
            n "I couldn't..."
            stop music fadeout 1.0
            jump law_ending_burialskip
        else:
            stop music fadeout 1.0
            jump law_ending_burial
    else:
        law "I guess we can't do this the slow way."
        n "He kicked the bucket closer to the chair, between my legs."
        $ lbase,lexp,lbangs = 26,11,1
        law "You're just too much of a problem...aren't you?"
        n "He grabbed the back of the chair and tilted me forward, over the bucket."
        n "The chair creaked from being on only two legs."
        n "I let out a frightened whimper."
        $ health -= 50
        $ lbase,lexp,lbangs = 26,9,1
        play music law_kill fadein 1.0
        n "He flipped the knife in his hand and suddenly slammed it between my ribs." with vpunch
        n "I tried to scream from the pain."
        n "But I only made a choked gurgle."
        n "He held the chair as I shook and looked up at him in shock."
        $ health -= 20
        n "He tore the knife sideways and yanked it out from my flesh."
        $ health -= 10
        scene cg_lawrence_bucket with dissolve
        n "My horrified gaze sank downward."
        n "To the slow river of red seeping down my chest, between my legs, and dripping into the bucket."
        n "I finally managed to cough, but it was just more blood."
        n "I couldn't work my lungs."
        n "Fuzzily, I thought to myself...that's probably for the best."
        scene black with dissolve
        stop music fadeout 1.0
        stop sound fadeout 1.0
        $ health -= 100
        $ sanity -= 100
        hide screen health_bar
        hide screen sanity_bar
        hide screen sanity_bar_law
        $ persistent.law_ending_bleedout = True
        play music law_twinkle fadein 1.0
        scene endslate with Dissolve(1.0)
        screen law_ending_bleedout:
            text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}Lawrence bled you out.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen law_ending_bleedout
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()

label law_wrist_beg:
    p "Please..."
    n "My voice was shaking."
    $ lbase,lexp,lbangs = 1,4,1
    p "Lawrence..."
    p "I don't want to die..."
    $ lbase,lexp,lbangs = 1,1,1
    n "My head dropped as I tried to hold back tears."
    stop music fadeout 1.0
    p "I don't want this..."
    if law_love >= 50:
        play music law_haunt fadein 1.0
        law "..."
        $ lbase,lexp,lbangs = 1,6,1
        law "You're really scared..."
        n "I raised my head."
        p "...Yes..."
        $ lbase,lexp,lbangs = 26,23,1
        law "Strange..."
        law "..."
        $ lbase,lexp,lbangs = 26,24,1
        law "You look... good like that..."
        n "He looked down at the blade in his hand and tilted it."
        n "He mumbled quietly."
        $ lbase,lexp,lbangs = 26,48,1
        law "{size=10}Why do I like this?{/size}"
        $ lbase,lexp,lbangs = 1,4,1
        $ sanity -= 20
        n "He suddenly thrust the knife forward, stopping just short of my face."
        n "I choked out a gasp and started to cry."
        call law_subroutine from _call_law_subroutine_28
        $ lbase,lexp,lbangs = 1,17,1
        $ law_love += 10
        n "He...smiled."
        law "I like you better than other people."
        n "I looked up at him through my shaking and tears."
        $ lbase,lexp,lbangs = 1,12,1
        law "I guess..."
        law "I don't need to bleed you right now."
        $ lbase,lexp,lbangs = 1,1,1
        law "Just..."
        law "Just sit. I uh... have to go out."
        p "Wait- what?"
        law "I still need to leave..."
        stop music fadeout 1.0
        play sound law_day fadein 1.0
        show law:
            xalign 0.5
            alpha 1.0
            easeout 0.2 xalign 0.6 alpha 0.0
        n "He left quickly, slipping through his door and refusing to meet my gaze."
        n "I sighed in the quiet apartment, feeling exhausted from the whole ordeal."
        stop sound fadeout 1.0
        scene black with dissolve
        n "I let myself relax and slipped into a deep sleep."
        pause(1.5)
        jump law_day3
    else:
        law "..."
        play music law_unsettled fadein 1.0
        n "He grasped my arm tightly."
        $ sanity -= 10
        law "What you want doesn't matter to me."
        call law_subroutine from _call_law_subroutine_29
        jump law_wrist_shortcut

label law_night2_wristcut2:
$ lbase,lexp,lbangs = 1,16,1
n "We both watched the dark liquid seep out of me."
n "He seemed to... be relaxed by it."
n "I felt somewhat detached."
n "It was surreal..."
n "Was...this really happening?"
$ lbase,lexp,lbangs = 1,4,1
n "The flow began to slow as I breathed more rapidly."
n "He felt my cold hand, then moved to take my other arm."
$ lbase,lexp,lbangs = 1,23,1
n "He positioned the knife over my undamaged wrist."
menu:
    "-Pull away-":
        jump law_night2_wristcut3
    "-Let him cut-":

        jump law_ending_theriver

label law_night2_wristcut3:
$ lbase,lexp,lbangs = 1,2,1
stop sound fadeout 1.0
p "Please..."
n "I pulled my arm away from him weakly."
p "Lawrence..."
n "I begged."
p "{size=10}I'm scared...{/size}"
if lsanity >= 50:
    if law_love >= 40:
        jump law_night2_wristcut3_apology
    else:
        jump law_night2_wristcut3_stab
else:
    jump law_ending_eviscerate

label law_night2_wristcut3_apology:
$ lbase,lexp,lbangs = 1,22,1
law "Wh..."
n "He dropped the knife abruptly."
n "We both jumped slightly at the clang it made on the metal of the bucket."
law "O-oh...uh..."
$ lbase,lexp,lbangs = 2,24,1
law "Um, I didn't mean..."
n "He looked down at my bloody arm."
n "Then slowly lifted his gaze up my body to my distressed face."
$ lbase,lexp,lbangs = 1,22,1
law "I'm sorry."
hide law
n "He quickly turned from me and walked to the other side of the room to gather something."
n "Did... he change his mind?"
pause(1.5)
show law
$ lbase,lexp,lbangs = 1,1,1
n "When he returned, he had a few cloths, more tape, and what looked like a bowl of green water."
$ lbase,lexp,lbangs = 1,23,1
n "He began to wash the blood off my arm with a cloth and the water."
n "We both sat in a strange silence as he worked."
n "I didn't want to do anything to change his mind again."
$ health += 5
n "I shivered from the cool liquid on my already cold arm, but it didn't sting."
$ lbase,lexp,lbangs = 1,8,1
$ health += 5
n "Once my arm was cleaner, he pressed a clean cloth to it and taped it on."
menu:
    "-Stay silent-":
        n "I didn't want to push my luck."
        n "I sat quietly in the chair."
    "-Thank him-":

        $ lbase,lexp,lbangs = 1,22,1
        p "Thank you, Lawrence."
        $ lbase,lexp,lbangs = 1,24,1
        $ law_love += 10
        p "I really appreciate it."

n "He looked like he wanted to say something."
$ lbase,lexp,lbangs = 1,16,1
n "But he just quietly mumbled something I couldn't quite hear."
n "He held my arms to tape them back to the chair, taking care to be somewhat gentle with my injured wrist."
law "Just..."
law "Just sit. I uh... have to go out."
p "Wait- what?"
show law:
    xalign 0.5
    alpha 1.0
    easeout 0.2 xalign 0.6 alpha 0.0
stop music fadeout 1.0
play sound law_day fadein 1.0 loop
n "But he left quickly, slamming his door and refusing to meet my gaze."
n "I sighed in the quiet apartment, feeling exhausted from fear and blood loss."
scene black with dissolve
stop sound fadeout 1.0
n "I let myself relax and slipped into a deep sleep."
pause(1.5)
jump law_day3

label law_night2_wristcut3_stab:
$ lbase,lexp,lbangs = 1,4,1
law "You don't want to die?"
$ lbase,lexp,lbangs = 1,13,1
law "..."
play sound law_brownnote fadein 1.0 loop
law "Of course not."
$ lbase,lexp,lbangs = 1,9,1
n "He looked at me coldly."
law "You'd rather cling..."
law "...To that temporary state."
n "He leaned forward, brandishing the knife."
law "Warm and noisy."
$ lbase,lexp,lbangs = 1,13,1
law "Colors, sunlight...sweet scents..."
$ lbase,lexp,lbangs = 1,11,1
law "Sensations..."
$ lbase,lexp,lbangs = 1,9,1
law "You want more, don't you?"
menu:
    "\"Um...\"":
        jump law_night2_wristcut3_stab2
    "\"Well,\"":
        jump law_night2_wristcut3_stab2
    "\"Wait!\"":
        jump law_night2_wristcut3_stab2
label law_night2_wristcut3_stab2:
$ lbase,lexp,lbangs = 1,17,1
play music law_unsettled fadein 1.0
$ health -= 20
n "I shrieked as he slammed the blade down through my good arm." with vpunch
call law_subroutine from _call_law_subroutine_30
$ lbase,lexp,lbangs = 1,9,1
n "He covered my mouth to muffle my crying."
law "Fine."
law "Enjoy... I need to leave for a bit."
$ sanity -= 20
n "My bleeding arms were shaking as I choked back more sobs."
p "Y...you're just going to leave me...like this?"
call law_subroutine from _call_law_subroutine_31
$ lbase,lexp,lbangs = 1,8,1
n "He looked over my bloody limbs."
law "I...guess I can't."
$ lbase,lexp,lbangs = 1,9,1
n "I breathed half a sigh of relief before realizing that he'd only grabbed the duct tape."
p "N-no, pl-"
n "He slapped a piece over my mouth, then roughly taped my arms back to the chair."
show law:
    xalign 0.5
    alpha 1.0
    easeout 0.2 xalign 0.6 alpha 0.0
n "I could only manage a pathetic, exhausted whimper as he left my view."
stop music fadeout 1.0
stop sound fadeout 1.0
scene black with dissolve
n "I barely heard the door behind me slam before I passed out."
jump law_day3

label law_day3:
if sanity > 50:
    p "Nnngg..."
    n "My heart was pounding."
    n "Was I asleep...?"
    n "I felt like something was at the edge of my mind."
    n "But I couldn't remember."
else:
    pause(1.0)
    show cg_lawrence_darkness_1 zorder 3
    show cg_lawrence_darkness_4_anim with Dissolve(1.0)
    pause(0.2)
    show cg_lawrence_darkness_3_anim with dissolve
    pause(0.2)
    show cg_lawrence_darkness_2_anim with dissolve
    play sound law_brownnote fadein 5.0 loop
    n "It's... so dark."
    n "I can barely see."
    n "I can't..."
    n "...walk..."
    n "Am I outside?"
    n "I can't remember anything... I can't..."
    n "Outside..."
    n "It's wrong."
    n "Something told me that being outside should feel like freedom."
    n "It's worse than feeling trapped."
    n "I don't feel like I'm being buried...or drowning..."
    n "Just that this nothing is all there is."
    n "All there ever will be."
    pause(1.5)
    n "...All there ever was."
    show cg_lawrence_darkness_4:
        alpha 0.0
        xalign 0.5
        yalign 0.5
        easeout_expo 0.75 xalign 0.5 alpha 1.0
    pause(0.2)
    show cg_lawrence_darkness_3:
        alpha 0.0
        xalign 0.5
        yalign 0.5
        easeout_expo 0.75 xalign 0.5 alpha 1.0
    pause(0.2)
    show cg_lawrence_darkness_2:
        alpha 0.0
        xalign 0.5
        yalign 0.5
        easeout_expo 0.75 xalign 0.5 alpha 1.0
    pause(0.2)
    pause(2.5)
    stop sound fadeout 1.0
    show cg_lawrence_darkness_still
    hide cg_lawrence_darkness_still
    show cg_lawrence_darkness_anim_end
    pause(2.5)
    show black with dissolve

hide cg_lawrence_darkness_4
hide cg_lawrence_darkness_3
hide cg_lawrence_darkness_2
hide cg_lawrence_darkness_4_anim
hide cg_lawrence_darkness_3_anim
hide cg_lawrence_darkness_2_anim
hide cg_lawrence_darkness_1
hide cg_lawrence_darkness_5
hide cg_lawrence_darkness_still
show bg_lawrence_sleeping_rain zorder 1
show bg_law_apartment_rain zorder 0
show black zorder 2:
    subpixel True
    alpha 1.0
    easeout 0.5 alpha 0.0
play sound law_day_rain fadein 1.0 loop
n "I slowly raised my aching head."
n "I tried to move my limbs and found I was fully taped down again."
n "...Fuck."
show bg_lawrence_sleeping_rain:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 1.0
show bg_law_apartment_rain:
    subpixel True
    xalign 0.5
    easeout 0.3 xalign 1.0
n "He's...asleep."
n "I took a few breaths and gathered my thoughts."
show bg_lawrence_sleeping_rain:
    subpixel True
    xalign 1.0
    easeout 0.5 xalign 0.5
show bg_law_apartment_rain:
    subpixel True
    xalign 1.0
    easeout 0.5 xalign 0.5
n "What should I do...?"
$ struggle2 = 0
label law_day3_strugglerest:
menu:
    "-Rest-":
        n "There's no point in struggling now."
        if sanity or health < 50:
            n "I'm much too tired anyway..."
        n "..."
        n "I tried to relax and forget about the nightmares."
        n "...I tried to forget about this nightmare too."
        scene black with dissolve
        stop sound fadeout 1.0
        stop music fadeout 1.0
        n "I eventually passed out again."
        jump law_night3
    "-Struggle-":

        jump law_day3_struggle
label law_day3_struggle:
$ struggle += 1
$ struggle2 += 1
if struggle2 > 3:
    jump law_day3_wakelaw
if struggle == 1:
    n "I pulled at the tape around my wrists."
    n "I tried to be quiet, but the tape was so tight."
    $ sanity -= 10
    n "It didn't feel like it was budging at all."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        n "One arm came free from my panicked struggle."
        jump law_daychoke_shortcut2
    jump law_day3_strugglerest
elif struggle == 2:
    n "I needed to keep trying."
    $ sanity -= 10
    n "I bit my lip and pulled hard against the tape."
    n "I froze when I heard Lawrence turn over."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        n "One arm came free from my panicked struggle."
        jump law_daychoke_shortcut2
    jump law_day3_strugglerest
elif struggle == 3:
    n "My heart was pounding."
    n "I... have to..."
    $ sanity -= 10
    n "I tugged my arm with an involuntary grunt."
    hide bg_lawrence_sleeping_rain
    show bg_lawapartment_rain zorder 0:
        subpixel True
        alpha 1.0
        xalign 0.5
        easeout 0.3 xalign 1.0
    show bg_lawrence_sleeping_rain zorder 2:
        subpixel True
        alpha 1.0
        xalign 0.5
        easeout 0.3 xalign 1.0
    pause(0.5)
    n "Lawrence made a soft sound in bed."
    n "I froze again, sweat beading down my face."
    show bg_lawapartment_rain zorder 0:
        subpixel True
        xalign 1.0
        easeout 1.0 xalign 0.5
    show bg_lawrence_sleeping_rain zorder 2:
        subpixel True
        xalign 1.0
        easeout 1.0 xalign 0.5
    pause(1.0)
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        n "One arm came free from my panicked struggle."
        jump law_daychoke_shortcut2
    jump law_day3_strugglerest
elif struggle == 4:
    n "I held my breath and slowly pulled against the tape."
    n "At first I felt nothing change."
    n "But something budged!"
    n "I pulled carefully."
    n "It was the arms of the chair... they're loose!"
    n "I kept pulling..."
    $ sanity -= 10
    n "The one on the left creaked and I froze."
    n "..."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        n "One arm came free from my panicked struggle."
        jump law_daychoke_shortcut2
    jump law_day3_strugglerest
elif struggle == 5:
    n "I can do this..."
    n "I just need to be really careful."
    n "I moved my left arm, twisting upward."
    n "I could feel the arm of the chair getting looser."
    pause(1.5)
    $ sanity -= 10
    n "-CREAK-"
    n "Shit!"
    n "I gulped."
    n "The blood was pulsing in my ears."
    if sanity <= 0:
        n "I couldn't take it any more!"
        p "AAAUUUGHHHH!!!"
        n "I wrenched at the tape on my arms painfully and yelled."
        n "One arm came free from my panicked struggle."
        jump law_daychoke_shortcut2
    jump law_day3_strugglerest
elif struggle == 6:
    jump law_day3_free

label law_day3_wakelaw:
n "I steeled myself."
n "I don't have a choice..."
n "I wrenched my arm as hard as I could, feeling a release."
n "However, my blood ran cold as I realized the tape had made a loud ripping sound."
label law_daychoke_shortcut2:
$ lsanity = 10
play music law_unsettled fadein 1.0
law "...Ugh..."
n "No no.... I looked down to my free arm in a panic."
n "Should I try and replace the tape?"
n "But I only have one hand free..."
show bg_lawrence_sleeping_rain:
    subpixel True
    alpha 1.0
    easeout 0.3 alpha 0.0
pause(0.5)
hide bg_lawrence_sleeping_rain 
n "My dilemma was interrupted by a hand slamming down on my wrist with a vicelike grip."
n "I looked up with a strange yelp."
show law:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
$ lbase,lexp,lbangs = 9,25,3
law "It's...It's the middle of the day."
n "I wanted to say something, apologize, anything."
n "But my brain wasn't forming words."
n "I was wincing...He was a lot stronger than he first appeared to be."
n "He squeezed harder for a moment before letting go."
law "These... are a problem."
$ lbase,lexp,lbangs = 10,0,0
n "He turned to dig around."
$ lbase,lexp,lbangs = 11,25,3
play music law_kill fadein 1.0
n "Before I could find my voice to ask what he was doing, he turned back to me."
p "N...nonono..."
$ sanity -= 10
$ lexp = 21
p "LAWRENCE!"
$ lexp = 7
$ lbase = 9
n "He squinted coldly at me for a moment before placing the saw down and retrieving his tape and a small cloth."
law "No more noise..."
n "I tried to yell, but it was cut off by him shoving the cloth into my mouth and roughly slapping a piece of tape over it."
$ lexp = 4
n "He stopped to look over my panicking form, seeming to calm down slightly."
$ lbase = 11
n "Just as I began to hope he'd come to his senses, he picked up the saw."
n "I tried to shriek as he held down my free arm and positioned the saw just below my elbow."
$ health -= 10
$ sanity -= 10
scene cg_lawrence_sawing_rain with dissolve
n "The scene became blurry as tears filled my eyes and he made the first stroke, tearing through my skin."
n "I screamed uselessly into the makeshift gag, trying to tear my arm from his grip."
$ health -= 5
$ sanity -= 10
n "He held me down firmly and worked on my arm quickly."
$ health -= 5
$ sanity -= 10
n "I felt like I was choking, struggling to breathe."
$ health -= 10
$ sanity -= 10
n "I began to feel dizzy as I watched his muscles tense from the effort of sawing through my bone."
n "I realized in a haze of blinding pain that he was holding my severed arm."
n "He placed it gently on the ground and looked back to me, in my eyes."
law "You're in pain..."
n "He said it like he was describing some small miracle of nature."
n "Like finding a butterfly's cocoon."
n "I looked up at him dully, trying to move my hand and only feeling pain."
law "I know it hurts now..."
n "He moved and positioned the saw over my remaining arm."
law "But that's natural."
$ health -= 5
$ sanity -= 10
n "My body managed somehow to renew its panic as he moved the saw again."
n "I helplessly shuddered and sobbed as he tore through the flesh."
n "I felt a small wave of relief as I began to go numb."
n "He held my other arm, my blood splattered all over his body."
law "And now you're dripping out...all over."
$ health -= 5
$ sanity -= 10
scene black with dissolve
n "Am I?"
n "My arms were cold."
n "My... my arms."
$ health -= 5
$ sanity -= 10
law "I think your thread ends here."
law "...I'll take the rest of you to somewhere pretty."
n "That sounds nice."
n "I felt my head drop."
law "I'll find you again..."
$ sanity -= 100
$ health -= 100
stop sound fadeout 1.0
stop music fadeout 1.0
scene black with dissolve
law "In the darkness."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_disarmed = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_disarmed:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence took your hands.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_disarmed
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_burial:
$ lbase,lexp,lbangs = 1,13,1
law "..."
law "Keeping you here isn't working."
n "I gulped, watching him."
n "He seemed to be thinking hard."
$ lbase,lexp,lbangs = 1,9,1
law "Would you like to leave this place?"
n "Was...was this a trick?"
law "If you want to leave, you have to do what I say."
n "I tried to agree, but my throat still hurt."
n "After a failed wheeze, I just nodded quickly."
$ lbase,lexp,lbangs = 1,13,1
law "Good."
hide law
n "He walked to the sink at the other end of the room and poured a glass of water."
n "At the edge of my vision, I watched him drop some powder in and mix it."
n "He wasn't trying to hide it."
show law
$ lbase,lexp,lbangs = 1,4,1
n "He came back and held it in front of me."
law "Drink it."
n "He could just kill me any time."
n "At least this... might be a chance..."
n "I resigned with a sigh and took the cup."
n "Thankfully, it didn't taste too bad."
n "I downed the whole thing quickly."
n "It soothed my throat a little."
label law_ending_burialskip:
$ lbase,lexp,lbangs = 1,12,1
p "Uggnn.."
scene black with dissolve
pause(1.5)
scene cg_lawrence_blurry2 with dissolve
n "I tried to move."
n "Opening my eyes was a mistake."
n "Everything's....moving..."
n "I thought I recognized the rumble of a car's engine."
n "But I couldn't focus."
scene black with dissolve
pause(1.5)
play sound law_swamp fadein 1.0 loop
n "I woke up from the feeling of something cold hitting me."
p "Ugghhh..."
n "I was laying..."
n "Somewhere cold."
n "My head hurts..."
n "-Shhhk-"
n "Something hit me again...or...fell on me."
n "I tried to open my eyes more..."
n "Clear my head..."
n "Dirt."
n "It's...I'm outside."
n "-Shhhk-"
show cg_lawrence_buried with Dissolve(1.5)
play music law_unsettled fadein 1.0
n "Oh god."
n "He's burying me!"
n "I began to panic, trying to move my muscles."
n "I could barely move..."
n "My head..."
n "I strained, fear for my life driving me to move my limbs slightly."
n "I grunted from the massive effort it took just to move my arm."
law "..."
n "I froze in fear."
law "Are you awake...?"
n "I closed my eyes and laid still."
n "Maybe he won't-"
$ health -= 10
show cg_lawrence_buried2 with dissolve
n "My eyes shot open as the wind was knocked out of me." with vpunch
n "He jumped down in the hole on top of me."
n "I coughed and tried to plead for my life."
$ health -= 10
n "But he stomped on my chest before I could get anything meaningful out." with vpunch
law "You're an endless fountain of problems."
n "He lifted the shovel."
$ health -= 100
$ sanity -= 100
scene black
stop music
stop sound
law "And brought it down on my neck." with vpunch
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_burial = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_burial:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence buried you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_burial
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_day3_free:
n "I was shaking."
n "I have to..."
n "I gently pulled up on the left arm one more time."
n "I heard a quiet pop..."
n "My arm was free!"
n "I quickly used it to begin freeing my other arm."
n "Taking my time, I was able to pull up the other arm of the chair."
n "With two free arms, it was easy to lean forward and grasp the small knife he'd left on the table in front of me."
n "I slowly and quietly cut the tape from my limbs."
n "Time to stand..."
pause(1.5)
n "I got up slowly."
n "I was dizzy and sore."
n "But I was finally free to move around."
n "...And my captor is still asleep."
menu:
    "-Find a better weapon-":
        jump law_ending_murder
    "-Leave the apartment-":

        jump law_ending_escape

    "{image=icon_lowsanity.png} -Get in bed with him-" if sanity <= 40:
        jump law_day3_bedtime

label law_ending_murder:
n "I glanced over the tables in the room."
n "There's plenty of dangerous things here..."
n "My gaze settled on his large pair of garden shears."
n "A grin crept over my face."
n "How fitting."
show bg_lawapartment_rain zorder 0:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.3 xalign 1.0
show bg_lawrence_sleeping_rain zorder 2:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.3 xalign 1.0
n "It'll be easy..."
scene cg_lawrence_sleeping with dissolve
show cg_lawrence_sleeping_shears with dissolve
play sound law_heartbeat fadein 1.0 loop
n "I crept closer to him."
n "My heart was hammering in my chest."
menu:
    with smallshake
    "-Kill him-":
        n "I approached him silently and slowly."
        n "My hands and breath became steady."
        n "I listened hard to hear his soft breathing."
        n "I smiled."
        n "No more hesitation."
        n "I grasped his shoulder, pulling him down flat."
        n "In the same perfect motion, I slammed the blades down into his stomach with all the force I could muster."
        play music law_unsettled fadein 1.0
        scene cg_lawrence_stabbed with dissolve
        pause(0.5)
        n "I heard the soft sound of the blade slicing into his flesh and organs..."
        n "I was surprised at how easily the shears went into him."
        n "He looked like he was trying to make a sound."
        p "Shhhh."
        n "I twisted the blades slightly, earning a pained gasp."
        p "Remember, you said we had to be quiet."
        n "I watched his blood seep from his wound."
        n "He was shaking."
        n "I leaned down close."
        n "...I wanted to watch this."
        n "He moved his mouth again, trying in vain to say something."
        n "But he only managed a cracked sob."
        n "I locked eyes with him."
        n "And I wrenched the shears deeper."
        n "I panted over his body."
        stop sound fadeout 1.0
        stop music fadeout 1.0
        scene black with dissolve
        n "That felt pretty good."
        hide screen health_bar
        hide screen sanity_bar
        hide screen sanity_bar_law
        $ persistent.law_ending_murder = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen law_ending_murder:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You killed Lawrence instead.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen law_ending_murder
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Back out-":
        n "My hands were shaking."
        n "I..."
        n "He was breathing evenly. Completely unaware of what I could do."
        n "I can't..."
        hide cg_lawrence_sleeping_shears with dissolve
        n "I lowered the shears and backed away from him."
        n "I'll just..."
        n "I'll just leave."
        jump law_ending_escape_from_murder

label law_ending_escape:
n "Now's my chance!"
n "I'm getting the fuck out of here!"
label law_ending_escape_from_murder:
n "I tiptoed towards the door."
n "Okay..."
scene bg_law_door with dissolve:
    zoom 0.67
    xalign 0.5
    yalign 0.0
n "I looked over the door."
n "WHY ARE THERE SO MANY LOCKS?"
n "He had the usual apartment sliding chain..."
n "Another larger one of the same style that looked like he screwed it on himself..."
n "A swivel lock..."
n "One I didn't even recognize...."
n "My brow furrowed at the padlocks."
n "Luckily, a quick look in the nearby plants revealed the keys."
n "I chewed my lip and set to work on them, trying to be completely silent."
pause(1.5)
n "I managed to move the chains with barely any sound."
pause(1.5)
n "What the hell is this guy so afraid of!?"
n "I gently opened the padlocks."
pause(1.5)
n "The guy can punch like a hammer and he's clearly crazy."
n "I scowled as I fiddled with one of the swivel locks."
n "It's like he's afraid of the fuckin' bogeyman."
pause(1.5)
n "-CLICK-"
n "Shit!"
n "I spun around, checking on Lawrence."
n "...He didn't move."
n "I let myself breathe again."
n "Just this last lock..."
play music law_kill fadein 1.0
scene bg_law_door:
    zoom 0.67
    xalign 0.5
    yalign 0.0
    easeout 0.05 zoom 1.0
pause 0.05
scene black with vpunch
$ health -= 10
p "AUGH"
n "My face was slammed into the door from behind."
$ lbase,lexp = 9,21
scene bg_lawapartment_rain:
    xalign 0.0
    easeout 0.2 xalign 0.6
    easeout 0.03 xalign 0.5
show law:
    xalign 1.0
    easeout 0.2 xalign 0.4
    easeout 0.03 xalign 0.5
p "L..law-"
show bg_lawapartment_rain_lightning behind law:
    alpha 0.0
    xalign 0.5
    easeout 0.1 alpha 0.5
    alpha 0.0
    easeout 0.1 alpha 0.8
    pause 0.5
    easeout 0.5 alpha 0.0
show law_sil_shirtless:
    alpha 0.0
    xalign 0.5
    pause 0.1
    easeout 0.1 alpha 0.5
    alpha 0.0
    easeout 0.1 alpha 0.8
    pause 0.5
    easeout 0.5 alpha 0.0
pause 1.8

n "His usual detached look was gone."
n "He was fully focused..."
$ health -= 10
n "I froze in fear, doing nothing as he lunged for me."
scene black with vpunch
n "My head spun as I was thrown to the ground."
$ health -= 10
n "I groaned in pain but it was cut off by a heavy slam on my back."
n "The breath was knocked out of me..."
n "I curled defensively, trying to catch my breath."
p "Please..."
$ health -= 10
scene black
n "He kicked me sharply in the gut." with hpunch
n "I couldn't move."
n "I curled further, crying and trying to gasp."
scene bg_law_door with dissolve:
    yalign 1.0
    xalign 0.5
    zoom 1.5
n "Then he was on top of me, twisting me and pressing my front to the floor."
n "He grabbed the blade I dropped."
p "L-Law...rence..."
n "Even my voice sounded broken..."
scene bg_law_door:
    yalign 1.0
    xalign 0.5
    zoom 1.5
    yanchor 1.0
    easeout_expo 0.2 yalign 0.6 zoom 1
    easeout_expo 0.2 yalign 0.65 zoom 1
n "I choked out another gasp as he grabbed a fistful of my hair and yanked my head backwards."
n "I whimpered."
n "My whole chest was off the floor- He pulled my head back so hard that my spine arched painfully."
n "Then I felt the cold metal pressed against my throat."
p "No..."
$ health -= 100
$ sanity -= 100
n "I felt the warm liquid pour down my chest before I felt the pain."
scene bg_law_door:
    yalign 0.65
    xalign 0.5
    zoom 1
    easeout_expo 0.2 yalign 1.0 zoom 1.5
pause(0.2)
scene bg_law_door with vpunch:
    yalign 1.0
    zoom 1.5
    xalign 0.5
scene black with dissolve
$ health -= 100
$ sanity -= 100
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_escape = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_escape:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence caught you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_escape
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_day3_bedtime:
n "I knew I should probably leave or something..."
show bg_lawapartment_rain zorder 0:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.3 xalign 1.0
show bg_lawrence_sleeping_rain zorder 2:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.3 xalign 1.0
n "But..."
n "I looked at him in the bed."
n "He really...doesn't look scary like that."
n "The bed is small but it looks comfortable..."
n "I rubbed my aching arms."
n "Something was telling me this was a bad idea."
n "But where have all my good ideas gotten me anyway?"
n "I gently pulled up the blanket and crawled in next to him."
n "As I nestled in next to him and his warmth, he began to move."
law "Nnn...?"
scene cg_lawrence_startled at truecenter
law "Uwah!" with hpunch
n "He jumped back from me a little."
p "It's...just me..."
if law_love > 50:
    jump law_day3_bedmates
else:
    jump law_ending_bedtimebad

label law_ending_bedtimebad:
n "He looked at me in disbelief."
law "Y...you're..."
law "..."
n "He blinked a few times."
play music law_unsettled fadein 1.0
n "Then something changed on his face... from suprise to anger."
p "Wai-"
$ health -= 10
scene cg_law_bedchoking with vpunch
n "He quickled rolled over me and wrapped his hands around my neck."
p "Ach..."
n "I was too weak and tired to fight him at all."
n "His weight on me and the tight grip on my throat were such a strange contrast with the warm and soft bedsheets."
scene black with dissolve
stop sound fadeout 1.0
stop music fadeout 1.0
$ health -= 100
$ sanity -= 100
n "Maybe I just didn't want to fight him any more."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_bedtime = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_bedtime:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You startled Lawrence.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_bedtime
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_day3_bedmates:
n "He looked at me in disbelief."
$ law_love += 10
law "Y...you're..."
law "..."
scene cg_lawrence_startledblush at truecenter
n "He started turning red."
law "{size=12}What are you doing...?{/size}"
menu:
    "\"Can I sleep here?\"":
        law "Wh.."
        law "Uhh..."
        $ law_love += 10
        law "I...I guess so..."
        n "He seemed pretty anxious about me..."
        play sound law_heartbeat fadein 1.0 loop
        scene black with dissolve
        n "I closed my eyes and nestled in against him."
        n "I could feel his breathing get calmer."
        n "...And hear his heartbeat."
        n "After a few moments of silence, I felt him gently move his arm around me."
        n "He hugged me close and relaxed."
        n "I don't know when I fell asleep."
        stop sound fadeout 1.0
        n "But I slept well for the first time since meeting him."
        pause(1.5)
        jump law_finalnight_bed
    "\"Can I touch you?\"":

        $ law_love += 10
        play sound law_heartbeat fadein 1.0 loop
        n "He stared hard at me."
        n "He looked like he was trying to decipher some foreign language."
        n "I pressed my body against his to demonstate..."
        n "And gasped in suprise at finding him already hard."
        scene cg_lawrence_sex with dissolve
        n "He grabbed my arms and shifted on top of me so quickly that I was disoriented for a moment."
        n "He was breathing hard, pinning me tightly under him."
        n "I didn't know what to say..."
        law "I'm not going to let you go."
        p "W..what?"
        law "...You're going to die here."
        n "I know the words should have bothered me more."
        n "But something about his tone sounded like..."
        n "He was trying to convince himself, rather than me."
        p "So...it doesn't matter...what we do now."
        p "...Right?"
        n "He seemed surprised- that must have been it."
        n "He narrowed his eyes...making up his mind."
        n "I gasped again as he grabbed my clothing."
        n "He quickly pulled away just enough to expose me."
        n "I let out an involuntary yelp as he slid his fingers over my entrance and pushed two in sharply."
        n "His eyes snapped to me at the sound."
        n "In the grey light they looked so cold."
        n "I got the sensation that it was a warning."
        n "He thrust his fingers roughly again, and I bit my lip this time."
        n "He seemed satisfied at my efforts to be quieter..."
        n "I couldn't help but squirm as he prodded me, but he didn't seem bothered by that."
        n "He put his hand over my mouth."
        n "I looked at him in confusion, I was already being-"
        n "I cried out into his hand as he pushed his cock into me with no warning."
        n "He removed his hand... I let out a soft pained moan."
        law "You're...warm..."
        n "He began to move in time with his panting."
        n "As he moved I began to pant myself..."
        n "I spread my legs more and moved my hips against him."
        n "He held me down and we both started to moan more loudly..."
        n "He seemed too entranced by it all to worry about the sound now."
        n "I knew I shouldn't be feeling like this..."
        n "But I just let go of those thoughts."
        n "With only the feeling left behind, I soon cried out and tensed around him."
        n "I clung to him as he came deep inside me."
        n "...For a while we just laid there, absorbing what just happened."
        law "..."
        law "I've...never done that with someone who's still-"
        n "I looked at him questioningly as he cut off his own sentence."
        law "S-someone...Anyone."
        law "I.."
        n "I waited for him to continue, but he abruptly turned from me."
        n "He seemed frustrated with himself."
        n "I waited a few moments, then put an arm around him."
        n "I held him closer and felt his breathing relax."
        scene black with dissolve
        stop sound fadeout 1.0
        n "I don't know when I fell asleep."
        n "But I slept well for the first time since meeting him."
        $ law_sexed = True
        pause(1.5)
        jump law_finalnight_bed

label law_night3:
scene bg_law_apartment
$ law_crazy = True
show law
$ lbase,lexp,lbangs = 1,1,1
play sound law_day fadein 1.0 loop
n "I woke up with a start."
p "Uhh?"
scene bg_law_apartment:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.0
    pause 0.2
    easeout 0.2 xalign 1.0
    pause 0.2
    easeout 0.2 xalign 0.5
show law:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.7
    pause 0.2
    easeout 0.2 xalign 0.3
    pause 0.2
    easeout 0.2 xalign 0.5
n "Deja vu..."
n "I looked down and groaned."
$ lbase,lexp,lbangs = 2,23,1
law "..."
n "My head felt so fuzzy..."
if law_love >= 90:
    jump law_ending_yandere
elif law_love > 40:
    jump law_ending_closer
else:
    jump law_ending_shutyouup

label law_finalnight_bed:
scene bg_law_apartment
$ law_crazy = True
show law
$ lbase,lexp,lbangs = 1,1,1
play sound law_day fadein 1.0 loop
n "I woke up with a start."
p "Uhh?"
scene bg_law_apartment:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.0
    pause 0.2
    easeout 0.2 xalign 1.0
    pause 0.2
    easeout 0.2 xalign 0.5
show law:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign 0.7
    pause 0.2
    easeout 0.2 xalign 0.3
    pause 0.2
    easeout 0.2 xalign 0.5
n "Deja vu..."
n "I looked down."
n "Why was I in the chair again!?"
n "When did he move me?"
$ lbase,lexp,lbangs = 2,23,1
law "..."
n "Did last night even happen?"
n "My head felt so fuzzy..."
if law_love >= 90:
    jump law_ending_yandere
elif law_love > 50:
    jump law_ending_closer
else:
    jump law_ending_shutyouup

label law_ending_yandere:
show law
$ lbase,lexp,lbangs = 1,6,1
law "I.... I don't know what to do."
$ lbase,lexp,lbangs = 1,23,1
law "There's something about you."
$ lbase,lexp,lbangs = 1,24,1
law "S...something I can't..."
$ lbase,lexp,lbangs = 2,24,1
law "..."
n "Was he shaking...?"
law "Everyone I've met..."
law "I wished they'd just... die faster."
law "But you..."
law "..."
$ lbase,lexp,lbangs = 2,6,1
law "Have you ever heard of soul mates?"
n "I wasn't sure if he wanted a reply...He continued before I had much time to think about it."
$ lbase,lexp,lbangs = 1,8,1
law "The idea that there's someone out there... meant for you."
$ lbase,lexp,lbangs = 1,19,1
law "It's comforting isn't it?"
law "Someone who'd love you, no matter what?"
$ lbase,lexp,lbangs = 1,10,1
law "I think it's a beautiful fantasy."
$ lbase,lexp,lbangs = 1,24,1
play sound law_brownnote fadein 1.0 loop
law "But fantasies aren't real."
law "..."
$ lbase,lexp,lbangs = 1,4,1
law "You know it doesn't work like that, don't you?"
$ lbase,lexp,lbangs = 1,9,1
law "People are temporary..."
law "Just threads passing each other."
law "There's no force in this world that will hold you close to me."
$ lexp = 12
law "...Now that I've met you..."
$ lexp = 10
law "I know I need you."
law "And...I have to hold you close myself."
$ lbase,lexp,lbangs = 1,11,1
law "Do you understand?"
p "I...uh..."
n "I squirmed in the chair."
n "Something was wrong."
n "He took something from the table."
$ lbase,lexp,lbangs = 1,19,1
law "Just one last drink."
law "Okay?"
p "La..Lawrence..."
n "He pressed the cup to my lips and forced the liquid down my throat before I could voice any more protests."
n "The foul taste brought tears to my eyes as I sputtered and coughed."
p "Please..."
law "Shh... it's okay."
$ lbase,lexp,lbangs = 1,42,1
law "I'll take care of you."
stop sound fadeout 1.0
stop music fadeout 1.0
scene black with dissolve
pause(0.5)
play sound law_heartbeat fadein 1.0 loop
n "Wrong...wrong..."
n "Somethings...W..."
pause(0.5)
$ health = 10
$ sanity = 10
n "I can't feel my..."
n "No... I can feel...It's coming back..."
n "The dull ache advanced on me like a train."
n "It slammed through me as searing agony flared all over my body."
play music law_haunt fadein 1.0
scene cg_lawrence_amputation1 with dissolve
n "I opened my eyes, but I couldn't scream."
law "Oh... oh no... don't move."
n "He stopped to brush my sweat slicked hair from my face."
law "I'm not... done yet..."
n "My...legs..."
n "My arms!!!"
law "Shh shh, calm down, okay?"
n "More bitter liquid was poured in my mouth."
show black:
    subpixel True
    alpha 0.0
    easeout 0.5 alpha 0.9
    easeout 0.5 alpha 0.0
pause(1.0)
p "S...stop..."
stop sound fadeout 1.0
stop music fadeout 1.0
scene black with dissolve
pause(1.5)
scene bg_lawapartment with Dissolve(1.5)
play sound law_heartbeat fadein 1.0 loop
n "I realized dully that my eyes were open again."
$ lexp,lblush = 11,4
show law:
    subpixel True
    xalign 0.4
    alpha 0.0
    easeout 0.2 xalign 0.5 alpha 1.0
play music law_haunt fadein 1.0
law "There you are!"
n "He pet me softly."
n "My arms and legs..."
n "I couldn't think."
n "I laid in a haze of drugs and far away pain."
$ lexp = 19
law "It's all right, it's all okay."
n "He kept petting me."
law "I fixed our problem."
n "Blood..."
$ lexp = 48
law "Now nothing can take you from me."
n "M-my arms and legs..."
$ lexp = 42
law "And I'll take care of you..."
n "THEY'RE GONE!"
stop sound fadeout 1.0
stop music fadeout 1.0
scene black with dissolve
law "...Forever."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_yandere = True
play music law_reverse fadein 1.0
scene endslate_clean with Dissolve(1.0)
screen law_ending_yandere:
    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence kept you with him.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_yandere
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_lsanity:
stop sound fadeout 1.0
stop music fadeout 1.0
show law zorder 1
$ lbase,lexp,lbangs = 1,11,1
law "..."
law "Heh..."
play sound law_brownnote fadein 1.0 loop
show bg_vignette zorder 0.5:
    subpixel True
    xalign 0.5
    alpha 0.0
    easeout 5 alpha 1.0
$ lbase,lexp,lbangs = 14,0,0
pause(0.3)
$ lbase,lexp,lbangs = 15,0,0
pause(0.3)
$ lbase,lexp,lbangs = 14,0,0
pause(0.1)
$ lbase,lexp,lbangs = 15,0,0
pause(0.1)
$ lbase,lexp,lbangs = 14,0,0
pause(0.1)
$ lbase,lexp,lbangs = 15,0,0
pause(0.1)
$ lbase,lexp,lbangs = 14,0,0
pause(0.1)
$ lbase,lexp,lbangs = 15,0,0
pause(0.1)
$ lbase,lexp,lbangs = 14,0,0
pause(0.1)
$ lbase,lexp,lbangs = 15,0,0
pause(0.1)
$ lbase,lexp,lbangs = 14,0,0
pause(0.1)
$ lbase,lexp,lbangs = 15,0,0
pause(0.3)
$ lbase,lexp,lbangs = 14,0,0
pause(0.3)
$ sanity -= 20
p "L...lawrence?"
$ lbase,lexp,lbangs = 1,17,1
n "Something about him seemed different."
play music law_haunt fadein 1.0
n "Something... about the whole room seemed different."
n "He stopped and looked right at me."
n "I must have been recoiling."
$ lexp = 26
law "Right, right, you're scared aren't you?"
n "I felt a chill...he was looking at me in a way that made me feel..."
law "Tied up like an animal."
n "He came close to me, over me."
law "You don't want to die, do you?"
n "I shivered as he touched my face and shook my head quickly."
law "But everything dies."
law "I know you haven't seen the river."
law "It's all right."
$ lexp = 47
law "I've seen it and I'm still scared!"
law "Scared just like you."
$ lexp = 17
law "All the time."
if sanity <= 0 and persistent.law_ending_river == True:
    menu:
        "-Say nothing-":
            jump law_ending_lsanity2
        "{image=lawrence/icon_nosanity.png} \"I have seen the river.\"":

            jump law_ending_secret
else:
    pass
label law_ending_lsanity2:
n "I squirmed uselessly."
law "You have every right to be terrified."
$ lexp = 47
law "There're monsters in the dark!"
$ sanity -= 20
law "Hahahaha!"
$ lexp = 48
pause(1.0)
law "Every day I dream about dying."
law "So every night, I stay awake."
$ lexp = 26
law "I see more in the dark."
law "And there's so much to be afraid of."
n "He touched my neck, caressing me softly."
n "It should have been a reassuring gesture."
n "But it wasn't."
law "You're sweet and bright."
$ lexp = 48
law "I guess I picked you before you were supposed to fall.."
law "But I suppose that's the way life is."
n "He ran his fingers over my neck more firmly."
n "I couldn't move away from him."
law "You're still full of warm flesh and blood."
$ lexp = 17
law "But what's underneath?"
$ sanity -= 20
p "P-please...stop..."
$ lbase,lexp = 25,48
law "I was going to kill you nicely."
law "The... the 'right' way."
law "Like how hunters kill rabbits or farmers kill chickens."
$ lexp = 26
law "But I'm not a hunter."
law "And there's nothing anyone can do to stop me..."
law "Heh..."
$ lbase = 1
law "I don't want to kill you like that."
law "I want to peel away your layers and unwind your strings."
$ sanity -= 20
n "I choked on a sob."
law "I'll pull every part of you and spread you out."
law "I'll watch your blood and feel the warmth spill out of you."
law "You'll be a perfect, beautiful mess."
law "Broken... ruined... dead..."
$ lexp = 47
law "And all mine."
$ sanity -= 100
p "No..n-"
n "My protest was cut off by Lawrence shoving a cloth into my mouth and taping it down."
n "I tried to scream as he leaned back, looking me over appreciatively."
law "Don't worry, you don't have to do a thing."
law "You won't even have to breathe for much longer!"
n "He turned the chair I was bound to."
n "I was shaking and sweating."
n "He retrieved a small knife."
scene cg_lawrence_lsanity with dissolve
law "To really see the beauty in the world..."
law "You have to have some patience."
p "NGggghh!"
n "I couldn't shriek or cry."
$ health -= 5
n "I kept shaking as he made a slow, small cut."
$ health -= 5
n "I stared in horror as he continued."
$ health -= 10
n "More tiny cuts."
n "I strained, sobbed, and drooled into the rag stuffed in my mouth."
$ health -= 10
n "He meticulously carved lines in my flesh, peeling away strips of skin."
scene cg_lawrence_lsanity2 with dissolve
n "I learned the true depth of misery."
n "It felt like an eternity as I tried to beg him to just kill me."
n "But I couldn't speak through the gag, and I'm sure he wouldn't have listened."
n "I could do nothing but wait in unyeilding agony as he peeled me apart."
n "My head dropped lower, but I could still hear him."
n "He breathed evenly, calmly."
n "He was even humming softly."
n "I didn't have the strength to scream or even flinch."
stop sound fadeout 1.0
stop music fadeout 1.0
n "And finally, blissfully, I ran out of enough blood to stay conscious."
$ health -= 100
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
play music law_twinkle fadein 1.0
$ persistent.law_ending_lsanity = True
scene endslate with Dissolve(1.0)
screen law_ending_lsanity:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence stopped holding back.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_lsanity
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_drugs:
p "U...ughrr...."
stop music fadeout 1.0
stop sound fadeout 1.0
scene black with dissolve
$ health = 0
$ sanity = 0
$ lsanity = 0
pause(1.5)
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
play sound law_brownnote fadein 1.0 loop
n "My head fell down to my chest."
n "It felt like my stomach was trying to turn inside-out."
n "My head..."
play music law_heartbeat fadein 1.0
p "M...My Heaad..."
if law_crazy == True:
    show law_sil_crazy zorder 2:
        subpixel True
        alpha 0.0
        xalign 0.5
        easeout 1.0 alpha 1.0
        pause 1.0
else:
    show law_sil zorder 2:
        subpixel True
        alpha 0.0
        xalign 0.5
        easeout 1.0 alpha 1.0
        pause 1.0
n "What's wrong?"
n "{size=14}W{/size}hat's wron{size=14}g{/size}?{nw=0.02}"
n "Wh{size=14}a{/size}t's {size=14}w{/size}rong?{nw=0.02}"
"Wh{size=14}a{/size}t's wr{size=14}o{/size}ng?{nw=0.02}"
n "What'{size=14}s{/size} w{size=14}r{/size}ong?{nw=0.02}"
n "{size=14}W{/size}hat's wron{size=14}g{/size}?{nw=0.02}"
n "Wh{size=14}a{/size}t's {size=14}w{/size}rong?{nw=0.02}"
n "Wh{size=14}a{/size}t's wr{size=14}o{/size}ng?{nw=0.02}"
n "What'{size=14}s{/size} w{size=14}r{/size}ong?{nw=0.02}"
n "{size=14}W{/size}hat's wron{size=14}g{/size}?{nw=0.02}"
n "Wh{size=14}a{/size}t's {size=14}w{/size}rong?{nw=0.02}"
n "Wh{size=14}a{/size}t's wr{size=14}o{/size}ng?{nw=0.02}"
n "What'{size=14}s{/size} w{size=14}r{/size}ong?{nw=0.02}"
n "{size=14}W{/size}hat's wron{size=14}g{/size}?{nw=0.02}"
n "Wh{size=14}a{/size}t's {size=14}w{/size}rong?{nw=0.02}"
n "Wh{size=14}a{/size}t's wr{size=14}o{/size}ng?{nw=0.02}"
n "What'{size=14}s{/size} w{size=14}r{/size}ong?{nw=0.02}"
"{size=14}W{/size}hat's wron{size=14}g{/size}?{nw=0.02}"
n "Wh{size=14}a{/size}t's {size=14}w{/size}rong?{nw=0.02}"
"Wh{size=14}a{/size}t's wr{size=14}o{/size}ng?{nw=0.02}"
n "What'{size=14}s{/size} w{size=14}r{/size}ong?{nw=0.02}"
n "{size=14}W{/size}hat's wron{size=14}g{/size}?{nw=0.02}"
n "Wh{size=14}a{/size}t's {size=14}w{/size}rong?{nw=0.02}"
n "Wh{size=14}a{/size}t's wr{size=14}o{/size}ng?{nw=0.02}"
n "What'{size=14}s{/size} w{size=14}r{/size}ong?{nw=0.02}"
show bg_apartment_nightmare_animated zorder 0:
    subpixel True
    alpha 0.0
    xalign 0.5
    easeout 0.5 alpha 1.0
pause(0.5)
show bg_apartment_nightmare_animated zorder 0:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.5 alpha 0.0
pause(0.5)
show bg_apartment_nightmare_animated zorder 0:
    subpixel True
    alpha 0.0
    xalign 0.5
    easeout 0.3 alpha 1.0
pause(0.5)
hide bg_apartment_nightmare_animated zorder 0
show bg_apartment_nightmare_animated zorder 0
p "I..."
p "Oh god..."
stop sound fadeout 1.0
image law_silhouette:
    "lawrence/law_base_19.png"
    pause (0.05)
    "lawrence/law_base_20.png"
    pause (0.05)
    "lawrence/law_base_21.png"
    pause (0.05)
    repeat
image law_silhouette_eyes:
    "lawrence/law_expression_27.png"
    pause (0.09)
    "lawrence/law_expression_28.png"
    pause (0.09)
    "lawrence/law_expression_29.png"
    pause (0.09)
    "lawrence/law_expression_30.png"
    pause (0.09)
    repeat
show law_silhouette
show law_silhouette_eyes
hide law_sil with dissolve
hide law_sil_crazy with dissolve
pause(1.0)
hide law
pause(3.0)
menu:
    "\"Stop...\"":
        pause(1.0)
law "You seem...."
show law_silhouette_eyes4 with Dissolve(0.2)
pause(0.2)
hide law_silhouette_eyes4 with Dissolve(0.2)
law "Uncomfortable."
n "I can't... I can't..."
$ ui.timer(0.3, ui.jumps("drugmenu1"))
menu:
    "\"STOP\"":
        jump law_ending_drugs2
label drugmenu1:
$ ui.timer(0.3, ui.jumps("drugmenu2"))
menu:
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
label drugmenu2:
$ ui.timer(0.1, ui.jumps("drugmenu3"))
menu:
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
label drugmenu3:
$ ui.timer(0.05, ui.jumps("drugmenu4"))
menu:
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
label drugmenu4:
$ ui.timer(0.05, ui.jumps("drugmenu5"))
menu:
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
label drugmenu5:
menu:
    with smallshake
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2
    "\"STOP\"":
        jump law_ending_drugs2

label law_ending_drugs2:
image law_silhouette2:
    "lawrence/law_base_22.png"
    pause (0.05)
    "lawrence/law_base_23.png"
    pause (0.05)
    "lawrence/law_base_24.png"
    pause (0.05)
    repeat
image law_silhouette_eyes2:
    "lawrence/law_expression_27.png"
    pause (0.09)
    "lawrence/law_expression_28.png"
    pause (0.09)
    "lawrence/law_expression_29.png"
    pause (0.09)
    "lawrence/law_expression_30.png"
    pause (0.09)
    repeat
pause(1.5)
show law_silhouette2 zorder 2:
    alpha 0.0
    xalign 0.5
    easeout 0.2 alpha 1.0
show law_silhouette_eyes2 zorder 2:
    zoom 1.4
    xalign 0.5
    ypos 35
    alpha 0.0
    easeout 0.2 alpha 1.0
pause(0.2)
show law_silhouette zorder 1:
    alpha 1.0
    easeout 0.2 alpha 0.0
show law_silhouette_eyes zorder 1:
    alpha 1.0
    easeout 0.2 alpha 0.0
hide law_silhouette
hide law_silhouette_eyes
pause(1.5)
image law_silhouette_eyes3:
    "lawrence/law_expression_35.png"
show law_silhouette_eyes3 zorder 2:
    zoom 1.4
    xalign 0.5
    ypos 35
    alpha 0.0
    easeout 0.1 alpha 1.0
pause(0.01)
image law_silhouette_eyes4:
    "lawrence/law_expression_31.png"
    pause (0.09)
    "lawrence/law_expression_32.png"
    pause (0.09)
    "lawrence/law_expression_33.png"
    pause (0.09)
    "lawrence/law_expression_34.png"
    pause (0.09)
    repeat
image law_silhouette_horns:
    "lawrence/law_expression_36.png"
hide law_silhouette_eyes2
show law_silhouette_eyes4 zorder 2:
    zoom 1.4
    xalign 0.5
    ypos 35
    alpha 0.0
    easeout 0.1 alpha 1.0
pause(0.1)
hide law_silhouette_eyes3
show law_silhouette_horns zorder 3:
    zoom 1.4
    xalign 0.5
    ypos 35
    alpha 0.0
    easeout 0.1 alpha 1.0
    pause (0.01)
    alpha 0.1
    pause (0.01)
    alpha 0.2
    pause (0.01)
    alpha 0.5
    pause (0.2)
    alpha 0.1
    pause (0.2)
    alpha 0.2
    pause (0.01)
    alpha 0.1
    pause (0.2)
    pause (0.01)
    alpha 0.2
    pause (0.01)
    alpha 0.3
    pause (0.2)
    alpha 0.1
    pause (0.2)
    repeat
law "{color=#cc0000}{font=Bubu_Ghost.ttf}{size=35}%(player_name)s{/size}.{/font}{/color}"
law "{cps=20}{color=#cc0000}{font=Bubu_Ghost.ttf}{size=24}You look like you've seen something awful.{/size}{/font}{/color}{/cps}"
n "no no no no {alpha=0.9}no no no no {/alpha}{alpha=0.8}no no no no no {/alpha}{alpha=0.7}no no no no no no {/alpha}{alpha=0.6}no no no no no no {/alpha}{alpha=0.5}no no no no no no {/alpha}{alpha=0.4}no no no no no no {/alpha}{alpha=0.3}no no no no no no {/alpha}{alpha=0.3}no no no no no{/alpha}{alpha=0.2} no no no no no {/alpha}{alpha=0.1} no no no no no{/alpha}"
stop music fadeout 1.0
show law_silhouette_eyes2 zorder 2:
    zoom 1.4
    xalign 0.5
    ypos 35
    alpha 0.0
    easeout 0.2 alpha 1.0
pause(0.75)
show law_silhouette_eyes4 zorder 2:
    zoom 1.4
    xalign 0.5
    ypos 35
    alpha 1.0
    easeout 0.2 alpha 0.0
image law_silhouette_smilep1 = "lawrence/law_expression_37.png"
image law_silhouette_smilep2 = "lawrence/law_expression_38.png"
image law_silhouette_smilep3 = "lawrence/law_expression_39.png"
image law_silhouette_smile:
    "lawrence/law_expression_40.png"
    pause (0.05)
    "lawrence/law_expression_41.png"
    pause (0.05)
    repeat
show law_silhouette_smilep1 zorder 4:
    zoom 1.4
    xalign 0.5
    ypos 35
pause(0.05)
show law_silhouette_smilep2 zorder 4:
    zoom 1.4
    xalign 0.5
    ypos 35
pause(0.05)
show law_silhouette_smilep3 zorder 4:
    zoom 1.4
    xalign 0.5
    ypos 35
pause(0.05)
show law_silhouette_smile zorder 4:
    zoom 1.4
    xalign 0.5
    ypos 35
pause (1.5)
scene black with dissolve
show cg_lawrence_drugs zorder 10:
    alpha 0.0
    xanchor 0.5
    yanchor 0.5
    xalign 0.5
    yalign 0.5
    zoom 1.0
    easein_expo 0.5 alpha 1.0 zoom 1.1
pause 1.0
scene black with dissolve
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_drugs = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_drugs:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You swallowed too many drugs.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_drugs
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_theriver:
scene black with dissolve
pause(1.0)
n "I closed my eyes and breathed."
scene bg_law_apartment with dissolve
show law with dissolve
$ lbase,lexp,lbangs = 1,42,1
stop music fadeout 1.0
law "Are you ready?"
n "I nodded slowly, soothed by his gentle voice."
$ health -= 10
n "He dipped the still-wet blade into my other wrist, finding my vein easily."
n "Somehow, the sensation and the vision of my life's blood pouring out of me didn't bother me any more."
n "I looked up lazily and saw him over me, mumbling barely audible encouragements."
stop sound fadeout 1.0
law "{size=12}It's easy...{/size}{size=10}...easy...{/size}"
play sound law_heartbeat fadein 1.0 loop
$ health -= 10
n "The dripping..."
n "I breathed faster and faster."
n "Cold...blurring."
n "Was...was he talking to me?"
law "{size=10}...so lovely...{/size}"
law "{size=10}...r canvas is perfe...{/size}"
n "I let out a soft sound as my head slumped."
$ health -= 10
n "I could still hear the dripping, but it got quieter as he bent to whisper right next to my ear."
$ health -= 100
law "{size=12}I've seen the river.{/size}"
scene black with dissolve
stop sound fadeout 1.0
law "{size=12}It's beautiful.{/size}"
if sanity >= 30:
    hide screen health_bar
    hide screen sanity_bar
    hide screen sanity_bar_law
    play music law_twinkle fadein 1.0
    scene endslate with Dissolve(1.0)
    screen law_ending_theriver_missed:
        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}You can't see the river.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen law_ending_theriver_missed 
    with Dissolve(1.0)
    $ persistent.law_ending_river_missed = True
    pause
    $ renpy.full_restart()
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
stop sound fadeout 1.0
stop music fadeout 1.0
scene endslate with Dissolve(1.0)
screen law_ending_theriver:
    text "{=endslate_title}You're Dying{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_theriver 
with Dissolve(1.0)
pause(2.0)
hide screen law_ending_theriver 
with Dissolve(1.0)
scene bg_river1_animated with Dissolve(3.0)
pause(3.0)
n "Where am I?"
n "..."
n "I spun around, but it all looked the same."
p "...Hello?"
pause(1.5)
n "...nothing."
n "Total silence."
n "I realized I didn't feel any pain any more either."
n "Just the gentle pull of the shallow water around my calves."
n "I remembered him saying something about a river..."
n "I looked down at the grey water."
n "But there wasn't any shore or edge."
n "It seemed to go on forever..."
$ riverwander = 0
label law_wandermenu:
menu:
    "-Wander-":
        $ riverwander += 1
        n "I picked a direction and walked."
        n "The scenery never changed."
        n "There was no silhouette of any horizon."
        n "Just the pull of the river."
        if riverwander < 10:
            jump law_wandermenu
        else:
            jump law_river_ashe
    "-Lie Down-":
        scene bg_river1_animated zorder 1:
            yalign 2.0
            xalign 0.5
            subpixel True
            easein_expo 3 yalign 0.0
        show bg_river4 zorder 2:
            yalign 2.0
            xalign 0.5
            subpixel True
            easein_expo 3 yalign 0.0
        n "I looked at the water and laid down in it."
        label law_river_shortcut:
        n "I floated easily."
        n "My body was carried with the current, in a direction I could feel but not see."
        n "...Why was I here again?"
        show black zorder 3:
            alpha 0.0
            easeout 2 alpha 0.2
        pause(2)
        n "..."
        n "I... don't remember where I was before this."
        show black zorder 3:
            alpha 0.2
            easeout 2 alpha 0.5
        pause(2)
        n "It doesn't matter."
        n "This feels nice."
        show black zorder 3:
            alpha 0.5
            easeout 5 alpha 1.0
        pause(5)
        n "It is beautiful..."
        $ persistent.law_ending_river = True
        show bg_river5_animated zorder 2
        show black zorder 3:
            alpha 1.0
            easeout 5 alpha 0.0
        pause(6.0)
        scene black with dissolve
        pause
        $ renpy.full_restart()

label law_river_ashe:
    pause(1.5)
    unknown "Please don't make this difficult."
    $ ashebase,asheexp = 1,1
    show ashe_wings_1 zorder 1:
        subpixel True
        alpha 0.0
        ypos -10
        xalign 0.5
        easein_expo 1.5 ypos 50 alpha 1.0
        easeout 0.5 alpha 0.0
    show ashe zorder 2:
        subpixel True
        alpha 0.0
        ypos 0
        xalign 0.5
        easein_expo 1.5 ypos 50 alpha 1.0
        pause (3.0)
    pause(1.5)
    show ashe_wings_2 zorder 0:
        subpixel True
        xalign 0.5
        ypos 50
        alpha 0.0
        easeout 0.5 alpha 1.0
    $ ashebase,asheexp = 2,2
    $ persistent.character_unlock_ashe = True
    ashe "I already have enough work to do."
    menu:
        "-Wander-":
            ashe "..."
            ashe "There's nothing here."
            ashe "No way out."
            ashe "So just lie down."
            menu:
                "-Wander-":
                    $ ashebase,asheexp = 2,3
                    ashe "-Sigh-"
                    ashe "You're already expired."
                    ashe "You're not allowed to stick here."
                    ashe "Souls can rot too."
                    ashe "..."
                    ashe "That's how monsters are born."
                    ashe "Do you want that?"
                    menu:
                        "-Wander-":
                            ashe "Ugh."
                            hide ashe_wings_2
                            show ashe zorder 2:
                                subpixel True
                                alpha 1.0
                                ypos 50
                                xalign 0.5
                                easeout 0.1 ypos 0 alpha 0.0
                            show ashe_wings_1 zorder 0:
                                subpixel True
                                xalign 0.5
                                ypos 50
                                alpha 1.0
                                easeout 0.1 ypos 0 alpha 0.0
                            ashe "Why do I get the stubborn ones..."
                            hide ashe
                            hide ashe_wings_1
                            n "I felt a string around my neck."
                            n "It tightened instantly, impossibly...through me."
                            n "I wavered on my feet before falling backwards into the water."
                            show bg_river4 zorder 2:
                                yalign 2.0
                                xalign 0.5
                                subpixel True
                                easein_expo 3 yalign 0.0
                            jump law_river_shortcut
                        "-Lie Down-":
                            hide ashe_wings_2
                            show ashe zorder 2:
                                subpixel True
                                alpha 1.0
                                ypos 50
                                xalign 0.5
                                easeout 0.1 ypos 0 alpha 0.0
                            show ashe_wings_1 zorder 0:
                                subpixel True
                                xalign 0.5
                                ypos 50
                                alpha 1.0
                                easeout 0.1 ypos 0 alpha 0.0
                            pause(0.1)
                            show bg_river4 zorder 2:
                                ypos -600
                                xalign 0.5
                                subpixel True
                                easein_expo 3.0 ypos 0
                            hide ashe
                            hide ashe_wings_1
                            jump law_river_shortcut
                "-Lie Down-":
                    hide ashe_wings_2
                    show ashe zorder 2:
                        subpixel True
                        alpha 1.0
                        ypos 50
                        xalign 0.5
                        easeout 0.1 ypos 0 alpha 0.0
                    show ashe_wings_1 zorder 0:
                        subpixel True
                        xalign 0.5
                        ypos 50
                        alpha 1.0
                        easeout 0.1 ypos 0 alpha 0.0
                    pause(0.1)
                    show bg_river4 zorder 2:
                        ypos -600
                        xalign 0.5
                        subpixel True
                        easein_expo 3.0 ypos 0
                    hide ashe
                    hide ashe_wings_1
                    show bg_river4 zorder 2:
                        yalign 2.0
                        xalign 0.5
                        subpixel True
                        easein_expo 3 yalign 0.0
                    jump law_river_shortcut
        "-Lie Down-":
            hide ashe_wings_2
            show ashe zorder 2:
                subpixel True
                alpha 1.0
                ypos 50
                xalign 0.5
                easeout 0.1 ypos 0 alpha 0.0
            show ashe_wings_1 zorder 0:
                subpixel True
                xalign 0.5
                ypos 50
                alpha 1.0
                easeout 0.1 ypos 0 alpha 0.0
            pause(0.1)
            show bg_river4 zorder 2:
                ypos -600
                xalign 0.5
                subpixel True
                easein_expo 3.0 ypos 0
            hide ashe
            hide ashe_wings_1
            show bg_river4 zorder 2:
                yalign 2.0
                xalign 0.5
                subpixel True
                easein_expo 3 yalign 0.0
            jump law_river_shortcut

label law_ending_closer:
$ lbase,lexp,lbangs = 1,42,1
law "I don't usually like being close to anybody..."
$ lbase,lexp,lbangs = 1,16,1
n "A long silence stretched out as he looked down at the ground."
$ lbase,lexp,lbangs = 1,19,1
n "He suddenly took a step closer, startling me."
law "You're different."
$ lbase,lexp,lbangs = 1,42,1
law "You draw me in..."
n "He was staring at me so intently... I couldn't look away."
$ lbase,lexp,lbangs = 1,16,1
play music law_haunt fadein 3.0
n "Until I felt a soft touch on my knee."
n "He was gently tracing some shape on my leg."
p "Lawrence..?"
n "I whispered cautiously."
n "He seemed to be focusing intently on whatever he was doing."
law "You draw me in..."
n "He repeated himself."
law "...like a moth."
$ lbase,lexp,lbangs = 1,10,1
n "I gasped as he moved again, sitting on my lap and straddling me in the chair."
n "He was heavy on my legs but I didn't want to make a sound."
n "I didn't want to interrupt him for some reason."
if law_sexed == False:
    n "All this time I'd been trapped here... he'd never touched me like this."
    n "I stared in disbelief as he pressed himself against me."
if law_sexed == True:
    n "I'd already felt his body on mine..."
    n "But something was different this time."
n "I could hear his heavier breathing."
n "I wondered to myself if I should struggle... or make some sort of sound..."
n "The decision was made for me as I felt his hand on the back of my head and I squeaked involuntarily."
$ lexp = 42
$ lblush = 1
law "Shhhh..."
n "He was petting me... running his fingers through my hair."
law "You're soft..."
n "He lowered his head right next to mine to whisper in my ear."
law "Warm and soft..."
$ lexp = 48
$ lblush = 2
n "His hand crept under my shirt and stopped to lay flat against my chest."
law "You're pulsing under your shell."
law "Chrysalis..."
n "He let out a quiet sigh and rubbed his face into the crook of my neck."
n "I shivered slightly at the feeling of his light stubble."
play sound law_brownnote fadein 1.0 loop
law "I need to be...{i}closer{/i}..."
n "My brows furrowed slightly. How could he possibly-"
play music law_unsettled fadein 3.0
n "I yelped loudly in shock as I felt a sharp point below his hand on my chest."
$ sanity -= 5
n "I panicked and tried to look down, but he was still pressed against me."
n "I began to struggle and tried to ask what he was doing-"
n "But by the time I opened my mouth, the pain on my stomach became so much more intense and I could only let out a panicked scream."
n "He leaned back quickly and clamped a hand over my mouth."
law "You have to be quiet."
n "I was finally able to look down-"
$ health -= 5
$ sanity -= 5
n "I made another muffled whimper of horror as I saw the small blade pressed into my skin, already bleeding."
$ lexp = 26
$ lblush = 4
law "Shhhh..."
n "I could feel hot tears filling my eyes."
n "My stifled begging was ignored as he looked intently at my bleeding wound."
$ health -= 5
$ sanity -= 5
n "He pushed the blade in deeper and I screamed harder into his hand."
law "No... Don't interrupt."
n "He was panting."
law "I need... I need you to just be silent for this..."
n "He reached behind himself to the roll of tape on the table."
n "No! Not that fucking tape!"
n "I tried to scream again but was cut off by him slapping the tape quickly over my mouth."
n "I sobbed behind the tape as he settled back into his position around my seeping gut wound."
$ lexp = 42
law "That's okay."
n "He looked at my face for a moment, tilted his head slightly, and then ran a finger over the stream of tears on my cheek."
law "Perfect..."
n "He licked his finger and smiled to himself."
law "May I?"
n "What?"
n "I stared at him, trying to decipher what he was asking."
n "Whatever it was, he apparently wasn't going to wait for permission."
$ health -= 5
$ sanity -= 5
n "He pushed his fingers into the wound and I doubled forward, straining against the tape in agony."
$ health -= 5
$ sanity -= 5
n "My eyes widened in horror as he pressed his fingers deeper."
$ health -= 5
$ sanity -= 5
n "He moaned softly as his entire hand entered my body."
law "I can feel it..."
n "He was half whispering, half sighing the words."
law "Perfect and incomplete in your shell..."
n "I wanted to black out... I couldn't handle this."
scene black with dissolve
n "I tried closing my eyes to at least spare myself the image of him digging deeper into my entrails."
$ health -= 5
$ sanity -= 5
n "Without looking, I began to unwillingly focus on the feeling."
n "Above the searing, blinding pain in my abdomen, I could feel a couple of other unsettling sensations."
n "I could feel lawrence shuddering against me, his heavy breath cooling on the tears streaming down my neck."
$ health -= 5
$ sanity -= 5
n "I felt a sickening, disgusting pressure inside."
scene cg_lawrence_closer with dissolve
n "I dizzily glanced back down."
$ health -= 5
$ sanity -= 5
n "He was...up to his elbow."
n "The whole scene blurred for a moment as I comprehended him reaching up through my organs."
n "My muffled sobbing, frantic panting, and his ragged breathing were interrupted by his voice."
stop sound fadeout 1.0
stop music fadeout 1.0
play sound law_heartbeat fadein 1.0 loop
law "I found it."
scene black with dissolve
n "My ears were starting to hiss and my vision began to darken."
law "I found you..."
$ health -= 100
$ sanity -= 100
stop sound fadeout 1.0
stop music fadeout 1.0
n "He squeezed it softly and it stopped beating."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_closer = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_closer:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence got closer.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_closer
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_shutyouup:
$ lbase,lexp,lbangs = 1,25,1
play music law_unsettled fadein 3.0
n "I began to grow more concerned."
n "He always seemed kind of bitter..."
n "But he really looked fed up now."
hide law
n "He turned away from me without a word."
pause(1.5)
show law
$ lbase,lexp,lbangs = 1,9,1
n "He returned with a small plastic cup full of liquid. He shoved it in front of my face."
law "Drink it."
menu:
    "-Drink it-":
        label law_ending_shutyouup_accept:
        n "Ugh.."
        if drugs > 2:
            n "It smelled terrible. I knew it was more of his drugs... but at this point what could I do?"
        else:
            n "It smelled terrible... but at this point what could I do?"
        n "I looked down at the cup with disdain and opened my mouth."
        n "Maybe it'll make it hurt less..."
        n "He silently tilted the cup to my lips and I drank the liquid."
        n "It tasted a bit better than it smelled at least..."
    "-Refuse-":
        n "I pursed my lips tight and glared at him."
        if drugs > 2:
            n "There is no way I'm taking any more of his crazy drugs."
        $ lexp = 11
        n "He tried to smile at me."
        law "It'll make you feel better."
        n "He wasn't very good at faking it."
        menu:
            "-Give in-":
                jump law_ending_shutyouup_accept
            "-Keep refusing-":
                n "Nothing he could say would make me drink that shit."
                n "I kept my mouth shut."
                $ lexp = 4
                n "I saw him twitch."
                n "He looked at the cup, and to my surprise, he took a large swig."
                $ lexp = 7
                n "With his mouth full, he snapped his hand out to grab my nose."
                n "He was rough... I cried out."
                n "Then, before I could silence myself, his lips were covering my own."
                $ sanity -= 10
                n "I felt the strange tasting liquid gush into my mouth as I began to panic."
                n "He pulled away and snapped my jaw shut with his hand."
                $ lexp = 5
                n "I struggled and sputtered as he looked on coldly, absently licking some of the drug from his lips."
                n "I coughed after I felt most of the substance go down my throat. Damn it..."
n "He watched me intently, leaning back against the table and fondling the empty cup."
n "I was wondering what he was waiting for just as my fingers began to tingle."
p "L...Lawrence... what is..."
$ lexp = 11
play sound law_brownnote fadein 3.0 loop
n "I tensed up as the tingling began to spread all over my arms and legs."
$ health -= 5
$ sanity -= 5
n "It became more intense, and then painful."
p "Oh god!!"
$ lexp = 17
if drugs > 2:
    law "This one's not very nice is it?"
else:
    law "It's not very nice is it?"
$ health -= 5
$ sanity -= 5
scene black with dissolve
pause (0.5)
n "I lurched and strained against the tape and the chair as I felt like my veins were on fire."
n "My muscles were tensing and cramping painfully."
n "I wanted to scream but my tensed jaw wouldn't open."
law "We're just passing threads..."
$ lexp = 9
law "But I don't like you."
law "And now I have the power to weave your thread wherever I want."
scene cg_lawrence_shears with dissolve
n "I rolled my eyes up to see him, now aware that my eyes had filled with tears."
law "I'm going to twist you around."
n "When did... he pick up shears?"
n "He looked at the large blades boredly."
law "I'm going to make you hurt."
$ sanity -= 15
n "This must be a nightmare..."
n "He leaned over my convulsing body and wrenched my jaw open."
n "I gurgled in horror as he grasped my tongue and pushed the shears in my mouth."
$ health -= 15
$ sanity -= 15
n "Despite my entire body being in agony, I could still feel him cut through my tongue."
$ health -= 15
$ sanity -= 15
n "My mouth was instantly flooded with my own warm, metallic blood."
n "I couldn't move or scream."
n "I couldn't even cough."
$ health -= 15
$ sanity -= 15
n "All of my muscles were locked up."
$ health -= 15
$ sanity -= 15
scene cg_lawrence_shutyouup2 with dissolve
n "I was only vaguely aware of him swaying and leaning back against the table, watching me."
$ health -= 15
$ sanity -= 15
n "Blood was pouring down my airway and there was nothing I could do about it."
$ health -= 15
$ sanity -= 15
n "He just kept watching me silently as I drowned in agony in front of him."
stop sound fadeout 1.0
stop music fadeout 1.0
scene black with dissolve
$ health -= 100
$ sanity -= 100
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_shutyouup = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_shutyouup:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}Lawrence shut you up.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_shutyouup
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_eviscerate:
$ lbase,lexp,lbangs = 1,2,1
law "No?"
$ lbase,lexp,lbangs = 25,6,1
n "He paused."
$ lbase,lexp,lbangs = 25,11,1
play sound law_brownnote fadein 1.0 loop
law "You want to see it happen?"
p "See...what happen?"
$ lbase,lexp,lbangs = 1,42,1
law "I'll show you."
n "He held up a small glass bottle."
law "But you have to drink this."
n "I looked at it and gulped."
n "Of course... more drugs..."
n "I looked down and my bleeding wrist, already feeling a bit dizzy."
p "F...fine."
n "He nodded and held the bottle to my lips."
n "I took a deep breath and drank it."
pause (1.5)
$ lbase,lexp,lbangs = 1,6,1
law "How do you feel?"
n "I tried to answer, but I just made a strange gasp."
n "I was losing control of my mouth."
n "My head began to fall forward."
n "I didn't like the way everything was moving around me."
$ drugs += 1
call law_subroutine from _call_law_subroutine_33
$ lbase,lexp,lbangs = 1,16,1
n "Lawrence apparently sensed my distress, because he leaned forward to hold me and keep me still."
$ lbase,lexp,lbangs = 1,19,1
law "It's okay. I can understand you anyway."
n "I heard a soft ripping sound as he cut the tape from my arms."
n "He leaned lower to free my legs and I realized that I couldn't move any part of my body at all."
$ lbase,lexp,lbangs = 1,1,1
law "There we go..."
n "Something nagging at the back of my mind was telling me that I should be afraid."
n "Instead, I felt comforted and warm as he wrapped his arms around my body to lift me up."
scene cg_lawrence_blurry with dissolve
p "Nnng.."
n "Everything was moving again."
law "Just for a moment, %(player_name)s."
scene cg_lawrence_eviscerate1 with dissolve
n "Something solid pressed against my back."
law "See?"
n "I just began to register that it was the floor touching me when he knelt over me."
law "No more moving after this. Don't worry."
n "I felt a rush of relief."
n "He was spreading my arms to the side."
law "You're really pretty."
n "It was kind of hard to keep track of his movements."
law "You're like the last day of summer."
n "I could feel him touching my arms."
n "All of my other senses were...blurry...but his touch was clear."
law "People aren't just red inside."
n "His voice was even and gentle."
law "There's purples, oranges, yellows. Just like leaves."
$ health -= 5
$ sanity -= 5
n "I felt a tiny prick on my arm, then a searing pain."
$ health -= 5
$ sanity -= 5
n "Panic came rushing back to me as I found myself unable to struggle or move away from the slicing."
n "I couldn't even look, but pain was explosive and overwhelming. What was he doing!?"
law "I have to be very gentle..."
$ health -= 5
$ sanity -= 5
scene cg_lawrence_eviscerate2 with dissolve
n "I watched his concentrating face as he began to pull something from my arm."
n "The way he held it, my fevered mind imagined it was some kind of snake...or a string..."
law "They lead all over and around, and always to your heart."
n "His hands were stained with my blood."
n "He was so calm..."
n "It was my vein wasn't it? Why..."
law "Soft red roots~"
n "I felt the same pain sear through my other arm."
law "I want to shine light through them."
n "W...what?"
$ health -= 5
$ sanity -= 5
n "It was getting harder to understand him."
$ health -= 5
$ sanity -= 5
law "I'm going to make that moment. Just one moment in time. You'll be so delicate."
scene cg_lawrence_blurry3 with dissolve
n "The room was spinning."
law "Your roots and leaves..."
law "Just starting to decay."
n "His words were blurring together and I thought I could hear wind through trees."
scene black with dissolve
$ health -= 100
$ sanity -= 100
stop sound fadeout 1.0
stop music fadeout 1.0
law "Just like the last day of summer."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_eviscerate = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_eviscerate:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You became art.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_eviscerate
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_health:
n "I realized I was shivering."
n "I felt... so cold and weak."
scene black with dissolve
stop music fadeout 1.0
stop sound fadeout 1.0
n "My head slumped down."
n "I couldn't keep my eyes open."
law "..."
law "%(player_name)s?"
n "His voice sounded so far away..."
n "And the cold was starting to feel...comfortable."
n "I'll just..."
n "Rest for a bit."
pause(2.0)
play sound law_swamp fadein 10.0 loop
n "...Cold."
n "I'm cold again."
scene cg_lawrence_boneforest
scene black
show cg_lawrence_boneforest_1 at truecenter:
    zoom 0.8
show cg_lawrence_boneforest_2 at truecenter:
    zoom 0.8
show cg_lawrence_boneforest_3 at truecenter:
    zoom 0.8
show cg_lawrence_boneforest_4 at truecenter:
    zoom 0.8
p "U...uhgh?"
n "I can't move..."
show cg_lawrence_boneforest_1:
    xalign 0.5
    yalign 0.5
    easeout 0.4 xalign 0.6
show cg_lawrence_boneforest_2:
    xalign 0.5
    yalign 0.5
    easeout 0.4 xalign 0.7
show cg_lawrence_boneforest_3:
    xalign 0.5
    yalign 0.5
    easeout 0.4 xalign 0.8
show cg_lawrence_boneforest_4:
    xalign 0.5
    yalign 0.5
    easeout 0.4 xalign 1.0
pause 0.6
show cg_lawrence_boneforest_1:
    xalign 0.6
    yalign 0.5
    easeout 0.4 xalign 0.4
show cg_lawrence_boneforest_2:
    xalign 0.7
    yalign 0.5
    easeout 0.4 xalign 0.3
show cg_lawrence_boneforest_3:
    xalign 0.8
    yalign 0.5
    easeout 0.4 xalign 0.2
show cg_lawrence_boneforest_4:
    xalign 1.0
    yalign 0.5
    easeout 0.4 xalign 0.0
pause 0.6
show cg_lawrence_boneforest_1:
    xalign 0.4
    yalign 0.5
    easeout 0.8 xalign 0.5
show cg_lawrence_boneforest_2:
    xalign 0.3
    yalign 0.5
    easeout 0.8 xalign 0.5
show cg_lawrence_boneforest_3:
    xalign 0.2
    yalign 0.5
    easeout 0.8 xalign 0.5
show cg_lawrence_boneforest_4:
    xalign 0.0
    yalign 0.5
    easeout 0.8 xalign 0.5
pause 1.0
n "I used my tiny amount of strength to look around myself."
n "..."
n "No...god no..."
p "S...somebody!"
play music law_brownnote fadein 1.0
n "I was naked...tied."
n "Rope and bones...something's bones...all over me."
p "Why..."
show cg_lawrence_boneforest_1:
    xalign 0.5
    yalign 0.5
    easeout 0.1 xalign 0.6
show cg_lawrence_boneforest_2:
    xalign 0.5
    yalign 0.5
    easeout 0.1 xalign 0.7
show cg_lawrence_boneforest_3:
    xalign 0.5
    yalign 0.5
    easeout 0.1 xalign 0.8
show cg_lawrence_boneforest_4:
    xalign 0.5
    yalign 0.5
    easeout 0.1 xalign 1.0
pause 0.2
show cg_lawrence_boneforest_1:
    xalign 0.6
    yalign 0.5
    easeout 0.1 xalign 0.4
show cg_lawrence_boneforest_2:
    xalign 0.7
    yalign 0.5
    easeout 0.1 xalign 0.3
show cg_lawrence_boneforest_3:
    xalign 0.8
    yalign 0.5
    easeout 0.1 xalign 0.2
show cg_lawrence_boneforest_4:
    xalign 1.0
    yalign 0.5
    easeout 0.1 xalign 0.0
pause 0.2
show cg_lawrence_boneforest_1:
    xalign 0.4
    yalign 0.5
    easeout 0.1 xalign 0.6
show cg_lawrence_boneforest_2:
    xalign 0.3
    yalign 0.5
    easeout 0.1 xalign 0.7
show cg_lawrence_boneforest_3:
    xalign 0.2
    yalign 0.5
    easeout 0.1 xalign 0.8
show cg_lawrence_boneforest_4:
    xalign 0.0
    yalign 0.5
    easeout 0.1 xalign 1.0
pause 0.2
show cg_lawrence_boneforest_1:
    xalign 0.6
    yalign 0.5
    easeout 0.1 xalign 0.4
show cg_lawrence_boneforest_2:
    xalign 0.7
    yalign 0.5
    easeout 0.1 xalign 0.3
show cg_lawrence_boneforest_3:
    xalign 0.8
    yalign 0.5
    easeout 0.1 xalign 0.2
show cg_lawrence_boneforest_4:
    xalign 1.0
    yalign 0.5
    easeout 0.1 xalign 0.0
pause 0.2
n "I could hardly struggle, I was too weak."
n "I shivered against the tree I was bound to."
n "S-something...no..."
n "Many somethings."
p "uuuHHHHHAA!"
n "He'd painted... lines all over me."
n "Something sweet and sticky."
n "Insects were all over it, crawling."
n "Biting."
n "I used what little strength I had left trying to scream."
n "No human came."
stop sound fadeout 1.0
scene black with dissolve
n "Only more scavengers."
stop music fadeout 1.0
$ health -= 100
$ sanity -= 100
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_health = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_health:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You were taken to the woods.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_health
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_sanity:
p "You..."
n "My terror and frustration boiled up."
n "What kind of person... does these things..."
n "What kind of monster..."
$ lbase,lexp,lbangs = 1,44,1
stop sound fadeout 1.0
stop music fadeout 1.0
p "{size=20}What are you!?{/size}"
if lsanity > 20:
    $ lsanity -= 20
n "I almost shouted the question, desperately."
play sound law_brownnote fadein 1.0 loop
n "I looked up at him and was surprised to see a hurt expression."
$ law_love -= 20
law "...What am I..."
$ lbase,lexp,lbangs = 1,45,1
if lsanity > 20:
    $ lsanity -= 20
law "It's always 'what'."
n "He spoke bitterly."
play music law_kill fadein 1.0
law "Well what do you think I am!?"
n "I jumped at him suddenly raising his voice."
n "He lunged forward and grabbed my arms."
law "What!?"
law "A vampire? A witch? S-some...sort of necromancer!?"
law "I'VE HEARD IT ALL BEFORE!"
n "I just looked at him, mouth closed."
n "I didn't want to aggravate him any more."
$ lbase,lexp,lbangs = 1,5,1
n "He slumped down and released my arms."
$ lsanity = 10
law "Maybe I am a monster."
p "I...I'm sorr-"
$ lbase,lexp,lbangs = 1,7,1
n "He gripped my chin harshly."
law "Of course you are!"
n "I tried to sputter out more apologies as he ran his other hand along my face and down my neck."
$ lbase,lexp,lbangs = 1,21,1
law "They're always sorry."
if law_love >= 60:
    $ lexp = 13
    law "Tch."
    law "I... I almost liked you."
n "I gasped as he suddenly pushed me backwards."
scene cg_lawrence_sanity
n "The chair tipped back and I hit the floor with a thud that knocked the wind out of me." with vpunch
law "After I make them sorry."
p "Please, please don't!!!"
$ health -= 20
n "He slammed a heel down on my chest with full force." with vpunch
n "I felt something in my chest break."
$ health -= 20
n "I couldn't breathe."
n "I convulsed on the floor still bound to the chair, tears streaming down my face."
n "He watched me for a moment without a shred of pity."
n "I gathered up a tiny bit of air into my lungs despite how agonizing the effort was."
n "And I used it."
p "Y-you.."
p "{i}Are{/i} a monster."
stop music
stop sound
scene black with vpunch
$ health -= 100
$ sanity -= 100
n "This time the blow came down on my neck."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_sanity = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen law_ending_sanity:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You lost it.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen law_ending_sanity
with Dissolve(1.0)
pause
$ renpy.full_restart()

label law_ending_secret:
$ lbase,lexp,lbangs = 1,2,1
stop sound fadeout 1.0
stop music fadeout 1.0
play sound law_day fadein 1.0 loop
law "..."
law "What?"
$ lexp = 44
n "I looked down at my lap."
n "Have I...?"
n "For some reason, when he said 'the river', I could picture it."
$ law_love += 10
p "I've...been there."
n "I was nearly whispering."
n "What was I talking about...?"
n "I didn't feel like I was lying...?"
$ law_love += 10
p "There was no colour..."
law "..."
p "There was no edge..."
p "No shore."
$ law_love += 30
$ lbase,lexp,lbangs = 1,44,1
law "..."
n "I didn't understand what I was saying."
n "Yet... I could picture as easily as any clear memory."
n "Was it some sort of dream?"
n "I had to convince him I knew."
n "My voice was rising with desperation."
$ lexp = 2
p "It felt like nothing."
p "It was....it was..."
$ lbase,lexp,lbangs,lblush = 2,16,1,3
play music law_heaven fadein 3.0
law "...like waking up?"
n "I looked up at him, finally seeing something completely different."
p "Yes."
$ law_love += 10
p "Like...like waking up."
$ lblush = 1
p "Like the whole world and the people in it are just some nightmare."
$ lexp = 19
law "..."
$ law_love += 10
law "I didn't think..."
$ lexp = 16
law "Uhh..."
law "There was anyone else..."
n "I looked at him empathetically."
p "You're not alone."
p "...Not any more."
$ law_love += 10
law "I used to... regret coming back."
law "I didn't even mean to."
law "I just wanted to stay there."
law "But I accidentally... started dreaming again I guess."
p "Maybe it won't be so bad this time..."
$ lexp,lbase = 19,1
n "I looked as if a weight had been lifted from his shoulders."
$ law_love += 10
p "Maybe... we can have some fun in this world."
$ lexp = 48
law "..."
law "I'd really like that."
n "He grabbed a knife and knelt to cut me free."
scene cg_lawrence_smile with dissolve
n "I stood shakily..."
n "I stumbled forward into his arms."
n "We held each other for a long moment."
n "Our hearts were beating, but we both knew the truth."
scene cg_lawrence_brighttrees with Dissolve(1.0)
n "We have each other now."
n "And the whole world dying all around us."
hide screen health_bar
hide screen sanity_bar
hide screen sanity_bar_law
$ persistent.law_ending_secret = True
scene cg_lawrence_brighttrees with Dissolve(1.0)
screen law_ending_secret:
    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(5, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}You both know the truth.{/=endslate_subtitle}" outlines [(5, "000000", 0, 0)] at truecenter
show screen law_ending_secret
with Dissolve(1.0)
pause
$ renpy.full_restart()




label ren_intro:
$ ren_dom = 0
$ ren_shocking = False
$ ren_food_attack = False
scene bg_law_backalley:
    yalign 0.0
show ren_exclaim:
    ypos 265
    xpos 250
    subpixel True
    easeout 0.05 zoom 1.5 ypos 240
    easeout 0.05 zoom 1.0 ypos 265
    pause 0.5
pause 1
hide ren_exclaim
hide screen ren_button
$ rtail,rbase,rears,rexp = 1,1,1,2
show ren
ren "%(player_name)s!"
ren "Come with me! I'll help you!"
n "I swayed on my feet."
p "R...Ren? You've got... I don't feel..."
$ rbase,rexp = 1,8
ren "I know."
n "I began to collapse as he tried to hold me up."
ren "It'll be okay."
stop music fadeout 1.0
stop sound fadeout 1.0
scene black with dissolve
pause(1)
$ health += 10
$ persistent.character_unlock_ren2 = True
play music ren_piano fadein 1.0
scene bg_ren_livingroom with dissolve:
    subpixel True
    xalign 1.0
$ ren_hideheart = False
n "I woke up in a comfortable chair."
n "...In a strange house."
n "W...what happened!?"
n "I tried to remember as someone familiar approached me."
show ren:
    subpixel True
    alpha 0.0
    xalign 0.5
    easeout 0.1 alpha 1.0
$ rbase,rexp = 1,4
ren "Oh! You're awake!"
$ rbase,rexp = 1,8
ren "Do you feel better now?"
ren "You've been asleep for hours."
n "I groaned and rubbed my head."
n "Right... I went out... and then these two guys..."
menu:
    "\"Where am I?\"":
        $ ren_dom += 5
        $ rbase,rexp = 1,1
        ren "You're safe and sound at S- ...my house!"
        $ rbase,rexp = 1,6
        ren "Heh..."
    "\"...W-what happened?\"":
        $ rbase,rexp = 1,7
        ren "Well you talked to me and my friend Lawrence at the pub."
        ren "Then you left and..."
        pause(1.0)
        $ rbase,rexp = 1,4
        ren "Well I guess you were feeling drunk or sick or something!"
        $ rbase,rexp = 1,6
        ren "You fell down and I couldn't wake you up."
        ren "No way to ask where you live."
        ren "And I couldn't just leave you there in the cold!"
        $ rbase,rexp = 1,8
        ren "So I took you home."
    "\"Thank you for helping me...\"":
        $ ren_love += 10
        $ ren_dom -= 5
        $ rbase,rexp = 1,1
        ren "Well of course!"
        $ rbase,rexp = 1,8
        ren "It's no problem at all."
$ rbase,rexp = 1,8
ren "..."
ren "Anyway!"
ren "Now that you're up, I bet you're feeling hungry."
ren "Why don't I make you something to eat?"
menu:
    "\"About your ears...\"":
        n "I tried not to stare too much, but..."
        p "Um, are they... some sort of costume?"
        $ rbase,rexp = 1,4
        ren "Oh no, they're my real ears and tail!"
        $ rbase,rexp = 1,3
        ren "I know it's probably kind of weird to see."
        ren "I'm a sort of beast-kin."
        n "I guess my confused expression urged him to continue."
        $ rbase,rexp = 1,8
        ren "We're mostly just like humans!"
        ren "I can hide the ears and tail if I want..."
        $ rears,rbase,rexp = 3,1,12
        ren "But someone once told me..."
        ren "'You shouldn't hide who you are.'"
        jump ren_day1_food
    "\"I really should be leaving...\"":
        $ rears,rbase,rexp = 2,1,11
        ren "..."
        $ rears,rbase,rexp = 1,1,1
        ren "I'm sure you can stay for some food."
        $ rbase,rexp = 1,8
        ren "And we only just met."
        $ rears,rbase,rexp = 3,1,13
        ren "It's been so long since I've had anyone to cook for..."
        jump ren_day1_food
    "-Accept his offer-":
        p "Oh...uh..."
        $ rbase,rexp = 1,4
        p "I suppose I could stay a bit longer."
        p "Thanks."
        $ ren_dom -= 5
        $ ren_love += 10
        ren "Great!"
        ren "You're gonna love it, I have these really nice-"
        jump ren_day1_food
label ren_day1_food:
$ rears,rbase,rexp = 1,1,2
ren "Woops!"
$ rbase,rexp = 1,8
ren "I'm rambling."
ren "I'll just be a bit!"
$ rbase,rexp = 1,1
ren "Sit tight!"
show ren:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.2 alpha 0.0 xalign 0.6
stop music fadeout 1.0
p "O...okay..."
hide ren
n "I shifted in the seat."
play music ren_warppiano_straight fadein 1.0
n "...And heard a soft clinking."
n "What the-"
scene bg_ren_livingroom:
    subpixel True
    xalign 1.0
    easeout 0.1 xalign 0.0
window hide
pause(1.5)
n "What the fuck!?"
n "There was a huge chain on the floor!"
n "From the wall to my... ankle."
n "I was about to say something when I noticed something heavy around my neck as well."
n "I reached up."
n "What...what is this...?"
show ren_collar onlayer screens with dissolve
n "Some kind of collar!?"
n "Or... more like a neck sized shackle."
n "I realized moments after that I'd yelled loudly at the discovery."
n "I heard the quiet sounds in the kitchen stop."
n "I stood up, grasping at the metal ring around my neck, not finding any way to open it."
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
$ rbase,rexp = 1,13
n "He returned to the living room leisurely, not seeming too concerned about my distress."
$ rbase,rexp = 1,14
ren "What's wrong, [player_name]?"
menu:
    "\"What the hell is this thing on my neck!?\"":
        $ ren_dom += 5
        $ rears,rbase,rexp = 2,1,13
        ren "..."
    "\"Let me go!\"":
        $ ren_dom += 10
        $ rears,rbase,rexp = 3,1,13
        n "I lunged forward with my demand."
        $ rears,rbase,rexp = 1,1,11
        n "But I was stopped short by the chain." with vpunch
        $ rbase,rexp = 1,15
        ren "You should calm down."
        $ rbase,rexp = 1,8
        ren "Getting all riled up on an empty stomach is no good for you."
        n "I looked at the chain again angrily."
        n "Then I grabbed at the metal ring around my neck again."
        p "What is this!?"
        ren "..."
    "\"W-why am I chained to the wall?\"":
        $ ren_dom -= 5
        $ rbase,rexp = 1,15
        ren "Oh..."
        ren "There's no need to be worried, [player_name]."
        ren "I know it seems a little..."
        $ rbase,rexp = 1,6
        ren "...Different."
        $ rbase,rexp = 1,8
        ren "But just trust me okay?"
        $ rbase,rexp = 1,4
        ren "We'll be best friends before you know it!"
        n "I gulped and reached up to touch the collar around my neck."
        $ rbase,rexp = 1,8
        ren "Ah, that."
$ rears,rbase,rexp = 1,1,12
ren "It's a little hand-me-down."
$ rbase,rexp = 1,8
ren "A gift for my new friend."
menu:
    "\"Uhh...Thank you?\"":
        n "I felt that being polite was probably the best option."
        $ rears,rbase,rexp = 1,1,4
        ren "Well!"
        $ rexp = 1
        ren "You're so welcome!"
        $ rexp = 3
        n "He paused and chewed his lip."
        ren "Although..."
        ren "It's been a pretty long time."
        $ rears,rbase,rexp = 1,2,14
        ren "And I'm not sure if it still works."
        p "...Works?"
        p "Uh...what does it...do?"
        n "I had a feeling but I wanted to be wrong."
        stop sound fadeout 1.0
        stop music fadeout 1.0
        $ rears,rbase,rexp = 1,3,2
        $ ren_shocking = True
        play sound ren_shocked
        show screen disableclick(2.0)
        $ health -= 10
        $ sanity -= 10
        p "{cps=12}Nnnggg!{/cps}{w=2.0}{nw}" with smallshake
        $ rears,rbase,rexp = 1,2,11
        $ ren_shocking = False
        stop sound
        play music ren_obsessed fadein 3.0
        ren "Wow!"
        $ rears,rbase,rexp = 1,2,8
        call ren_subroutine from _call_ren_subroutine_9
        n "I gasped raggedly."
        n "It felt like I was being punched all over at once."
        n "But now it's completely gone..."
        ren "Looks like it still works fine, huh?"
        n "A thousand things went through my head at once."
        n "He put some sort of electric collar on me...where does someone even get something like that? What did he mean by training? Is he crazy enough to kill me? How can I get out of here?"
        $ rears,rbase,rexp = 1,1,7
        stop music fadeout 3.0
        ren "Those potatoes are probably done by now too..."
        play music ren_warppiano fadein 3.0
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "He turned and went back into the kitchen."
        n "I shrank back into the couch."
        n "I suppose I can take this time to figure out my situation..."
        jump ren_day1_food2
    "\"Are you insane!?\"":

        $ rears,rbase,rexp = 2,1,2
        $ ren_dom += 5
        p "This is worse than leaving me outside!"
        $ rbase,rexp = 1,16
        p "You can't just chain people up!"
        p "This is kidnapping!"
        jump ren_day1_shock_therapy
    "\"If you want to be my friend...why would you do this?\"":

        $ rbase,rexp = 1,2
        $ ren_dom -= 10
        p "I... I'll be your friend."
        $ rbase,rexp = 1,3
        p "You don't have to... put these things on me."
        ren "..."
        ren "You don't understand yet."
        jump ren_day1_shock_therapy

label ren_day1_shock_therapy:
$ rbase,rexp = 1,7
ren "Tsk."
n "He reached into his back pocket for something."
$ rbase,rexp = 2,13
ren "I suppose we'll have to start right away with your...{w}training"
p "Wha-"
$ rears,rbase,rexp = 2,3,13
$ ren_shocking = True
play sound ren_shocked
show screen disableclick(2.0)
$ health -= 10
$ sanity -= 10
p "{cps=12}Nnnggg!{/cps}{w=2.0}{nw}" with smallshake
$ rears,rbase,rexp = 1,2,11
$ ren_shocking = False
stop sound
play music ren_obsessed fadein 3.0
ren "Wow!"
$ rears,rbase,rexp = 1,2,8
call ren_subroutine from _call_ren_subroutine
n "I wavered on my feet."
n "It felt like I was being punched all over at once."
n "But now it's completely gone..."
ren "Looks like it still works, huh?"
n "A thousand things went through my head at once."
n "He put some sort of electric collar on me...where does someone even get something like that? What did he mean by training? Is he crazy enough to kill me? How can I get out of here?"
n "I couldn't focus. I just stared at him, still desperately grabbing the collar."
ren "All right, let's try test number two."
n "I tensed up."
ren "Sit."
menu:
    "\"I'm not an animal!\"":
        $ ren_dom += 10
        $ rears,rbase,rexp = 2,2,16
        p "You can shock me all you want!"
        $ rears,rbase,rexp = 4,2,2
        $ ren_love -= 10
        p "Chaining me up just makes you look like a little bitch."
        pause(1.0)
        $ rears,rbase,rexp = 2,2,17
        ren "..."
        $ rears,rbase,rexp = 2,3,17
        show screen disableclick(2.0)
        $ ren_shocking = True
        play sound ren_shocked
        $ health -= 20
        $ sanity -= 20
        ren "...{w=3.0}{nw}" with largeshake
        $ ren_shocking = False
        stop sound
        $ rears,rbase,rexp = 3,2,16
        n "This time it was a lot stronger."
        n "I could feel all of my muscles lock up as I dropped to the floor."
        call ren_subroutine from _call_ren_subroutine_1
        ren "I...I can make you sit."
        menu:
            "\"...\"":
                n "I glared up at him in response."
                n "But I kept my mouth shut."
                $ rears,rbase,rexp = 1,1,11
                ren "That's... a little better."
                n "I could tell he was taking a moment to compose himself."
                $ rears,rbase,rexp = 1,1,1
                ren "How about some dinner?"
                $ rears,rbase,rexp = 1,1,7
                ren "Those potatoes are probably done..."
                show ren:
                    subpixel True
                    alpha 1.0
                    xalign 0.5
                    easeout 0.2 alpha 0.0 xalign 0.6
                stop music fadeout 3.0
                n "He swept out of the room quickly."
                hide ren
                play music ren_warppiano fadein 3.0
                n "I stayed on the floor for a moment before climbing back up into the chair."
                n "I felt stiff...like I'd just completed some hard workout."
                n "Ugh..."
                n "I looked around myself."
                n "I guess eating something and keeping my stength up would probably be the best option."
                jump ren_day1_food2_pet
            "\"Fuck you.\"":

                $ ren_dom += 5
                $ ren_love -= 10
                $ rears,rbase,rexp = 2,1,17
                n "I spat the words in reply."
                ren "Y-you..."
                $ health -= 5
                ren "Rragh!" with vpunch
                n "He reeled back to kick me in the chest."
                call ren_subroutine from _call_ren_subroutine_2
                n "I fell back a bit, but compared to that shock, it hardly hurt at all."
                n "He looked like he was struggling with what to do next."
                label ren_forgotfood_shortcut:
                $ rears,rbase,rexp = 1,1,2
                ren "Oh!"
                $ rears,rbase,rexp = 1,1,11
                ren "I forgot about dinner."
                $ rears,rbase,rexp = 1,1,7
                ren "I'd better go check on those potatoes."
                show ren:
                    subpixel True
                    alpha 1.0
                    xalign 0.5
                    easeout 0.2 alpha 0.0 xalign 0.6
                stop music fadeout 3.0
                n "He left the room quickly."
                hide ren
                play music ren_warppiano fadein 3.0
                n "I groaned quietly and climbed up into the chair."
                n "I guess I can use this time to think of a plan."
                jump ren_day1_food2_pet
    "\"Please stop this...\"":

        $ ren_dom -= 5
        n "I didn't want to let him see me starting to shake."
        p "Please..."
        $ rears,rbase,rexp = 1,2,11
        stop music fadeout 1.0
        ren "..."
        ren "T-that's cute..."
        $ rears,rbase,rexp = 2,2,9
        play music "<from 15.0>ren/obsessed_z12C18Hu.mp3" fadein 1.0
        ren "But I said 'sit'."
        $ rears,rbase,rexp = 2,3,9
        show screen disableclick(2.0)
        $ ren_shocking = True
        play sound ren_shocked
        $ health -= 20
        $ sanity -= 20
        p "AHHHggnnnn!{w=3.0}{nw}" with largeshake
        $ ren_shocking = False
        stop sound
        $ rears,rbase,rexp = 1,2,9
        n "This time it was a lot stronger."
        n "I coughed and shook."
        call ren_subroutine from _call_ren_subroutine_3
        $ ren_dom -= 5
        $ rears,rbase,rexp = 1,2,8
        n "Then without another word, I struggled to sit on my knees on the floor."
        $ rears,rbase,rexp = 1,1,8
        ren "There..."
        ren "That wasn't so hard, right?"
        n "I had trouble thinking clearly."
        n "Did he want me to answer...?"
        jump ren_forgotfood_shortcut
    "-Obey-":

        $ ren_dom -=10
        n "I didn't want to feel that shock again."
        n "And sitting's really no big deal anyway..."
        $ rears,rbase,rexp = 1,2,8
        n "I knelt down and sat on my knees on the floor."
        $ rexp = 4
        ren "Ohh!"
        play music ren_warppiano fadein 1.0
        ren "That's good!"
        $ rears,rbase,rexp = 1,1,1
        ren "That's really good!"
        $ rears,rbase,rexp = 1,1,4
        $ ren_love += 10
        ren "We're already starting to click~"
        $ rears,rbase,rexp = 1,1,2
        ren "Ah!"
        $ rears,rbase,rexp = 1,1,8
        ren "I almost forgot about dinner!"
        $ rears,rbase,rexp = 1,1,1
        ren "You're gonna love it."
        ren "I'll get back to work."
        ren "You deserve a good hot meal! {image=icon_heart.png}"
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "He swept out of the room."
        hide ren
        n "I looked down at my knees."
        n "What the hell have I gotten into...?"
        n "I bit my lip and climbed back up into the chair."
        jump ren_day1_food2

label ren_day1_food2:
    n "I shrank into the soft cushions."
    n "That chain certainly isn't breaking."
    n "I heard the quiet sound of cooking start again in the kitchen."
    n "The shackle on my ankle looked as indestructable as the collar on my neck."
    n "I heard the hiss of something in a skillet."
    n "My eyes travelled down the chain to the wall."
    n "That's...starting to smell really good..."
    n "I shook my head." with hpunch
    n "Concentrate!"
    n "The wall."
    n "It's just a normal house wall."
    n "That's got to be the weak point."
    n "I stared for a while, contemplating if I should just get up right now..."
    n "I don't think that's a good idea."
    n "He'd hear me and he's still got that remote..."
    show ren:
        subpixel True
        alpha 0.0
        xalign 0.6
        easeout 0.2 alpha 1.0 xalign 0.5
    $ rears,rbase,rexp = 1,1,4
    ren "[player_name]!"
    n "I gasped and jumped in the chair."
    p "Oh! I...didn't hear you..."
    n "I stammered and gave him a nervous smile."
    $ rexp = 8
    ren "Heh, yeah, I can be pretty quiet."
    $ rexp = 1
    ren "Anyway, dinner's served!"
    n "He held out a plate heaped in mashed potatoes and steak to me."
    n "I took it, eyes wide."
    p "This... looks really good..."
    $ rexp = 4
    ren "Well looks don't mean much, anyway."
    $ rexp = 10
    ren "What matters is...how it tastes."
    $ rexp = 2
    ren "Oh!"
    $ rexp = 4
    ren "Haha, I forgot a fork."
    ren "I'll be right back."
    $ ren_food_knife = False
    menu:
        "-Say nothing-":
            $ rexp = 8
            n "I tried to keep my thankful smile and nodded."
            $ rexp = 1
            show ren:
                subpixel True
                alpha 1.0
                xalign 0.5
                easeout 0.2 alpha 0.0 xalign 0.6
            n "He ran back to the kitchen."
            n "He seemed to be a pretty good mood."
            n "That's good I suppose..."
            jump ren_day1_food3
        "\"Thank you.\"":

            $ rexp = 2
            $ ren_dom -= 5
            ren "..."
            $ ren_love += 10
            $ rexp = 8
            ren "You're so polite!"
            $ rexp = 1
            ren "Aaaah, I really hit the jackpot!"
            show ren:
                subpixel True
                alpha 1.0
                xalign 0.5
                easeout 0.2 alpha 0.0 xalign 0.6
            n "He practically skipped to the kitchen."
            n "He's in a great mood at least..."
            jump ren_day1_food3
        "\"Can I...also have a knife?\"":

            $ rexp = 14
            ren "..."
            p "Um, you know..."
            p "For the steak?"
            $ rexp = 3
            ren "Hmm."
            $ rexp = 8
            ren "I suppose it would be pretty hard to eat with just a fork!"
            show ren:
                subpixel True
                alpha 1.0
                xalign 0.5
                easeout 0.2 alpha 0.0 xalign 0.6
            n "He left to the kitchen again."
            n "I heard him rattle through some drawer for cutlery."
            $ ren_food_knife = True
            jump ren_day1_food3

label ren_day1_food3:
$ rexp = 1
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
if ren_food_knife == True:
    n "He came back quickly, beaming and holding out a knife and fork."
else:
    n "He came back quickly, beaming and holding out a fork."
n "I took it quietly and looked down at my meal."
$ rexp = 8
n "It seemed awkward to eat in front of someone like this..."
n "But I was starving and it smelled amazing."
n "Everything else is wrong..."
n "I might as well enjoy this..."
n "I took a bite."
p "..."
$ rexp,rears = 3,3
ren "...well?"
menu:
    "\"It's really good!\"":
        $ rexp,rears = 8,1
        $ ren_love += 10
        $ rblush = 1
        p "It...it's really delicious!"
        n "I tried not to sound surprised."
        n "Though he seemed to relax just watching me dig in."
        n "I was so hungry that it was easy to temporarily forget everything else."
        $ rexp = 1
        $ health += 5
        $ sanity += 5
        n "I cleaned my plate and finally looked back up."
        $ rexp = 2
        p "Ah...thank you..."
        $ rexp,rblush = 20,2
        ren "O-oh!"
        ren "I'm glad you liked it!"
        if ren_food_knife == True:
            $ ren_dom -= 10
            n "He took my plate, the knife, and the fork from me."
        else:
            n "He took my plate and fork from me."
        jump ren_day1_knife
    "\"It's fine.\"":

        $ rexp,rears = 2,3
        $ ren_dom += 10
        n "I don't know what he expects, while I'm chained to a wall."
        $ rexp,rears = 3,3
        $ health += 5
        $ sanity += 5
        n "I silently ate the rest."
        if ren_food_knife == True:
            $ ren_dom -= 10
            n "Once I was done, I held up my plate and utensils, avoiding his gaze."
        else:
            n "Once I was done, I held up my plate and fork, avoiding his gaze."
        n "He took them from me without a word."
        jump ren_day1_knife
    "-Say nothing-":

        n "I didn't know what to say."
        n "But I was so hungry..."
        $ rexp,rears = 15,1
        $ health += 5
        $ sanity += 5
        n "I just started eating."
        n "He seemed to relax just from watching me eat quickly."
        n "It was quite a lot, but I finished it easily."
        n "I looked down at my empty plate."
        p "Uh..."
        $ rexp,rears = 1,1
        if ren_food_knife == True:
            $ ren_dom -= 10
            n "He took my plate, the knife, and the fork from me."
        else:
            n "He took my plate and fork from me."
        jump ren_day1_knife

    "-Attack him-" if ren_food_knife == True:
        $ ren_food_attack = True
        $ ren_dom += 10
        $ ren_love -= 20
        n "Now I've got a weapon..."
        n "I need him a little closer."
        $ rexp,rears = 14,1
        p "Um...Ren..."
        p "There's a... something in my potatoes..."
        $ rexp,rears = 3,3
        play sound law_heartbeat fadein 1.0 loop
        ren "Really?"
        n "My heart was hammering in my chest."
        n "He leaned in much closer."
        n "...Perfect."
        $ rexp,rears = 2,1
        show ren:
            subpixel True
            ypos 0
            easeout 0.1 ypos 40
            easein 0.2 ypos 0
        stop sound
        stop music
        n "I swiped for his neck!"
        pause(1.0)
        $ rexp,rears = 18,2
        play music ren_obsessed fadein 1.0
        ren "You..."
        n "I insinctively leaned away."
        n "He was so fast!"
        n "He was...bristling..."
        $ rexp = 17
        ren "Y-you're lucky..."
        ren "I have more patience than he did."
        $ rbase,rexp,rears = 2,16,2
        p "What? Wait!"
        $ rbase,rexp,rears = 3,16,2
        $ ren_shocking = True
        play sound ren_shocked
        show screen disableclick(2.0)
        $ health -= 15
        $ sanity -= 15
        p "{cps=12}!!!!{/cps}{w=2.0}{nw}" with largeshake
        $ rears,rbase,rexp = 1,2,16
        $ ren_shocking = False
        stop sound
        n "I gasped and fell back against the chair."
        n "My plate, the food, and the knife all clattered to the ground."
        call ren_subroutine from _call_ren_subroutine_4
        $ rbase,rexp = 1,19
        ren "Looks like you're going hungry tonight."
        n "I looked down at the mess dully."
        n "He gathered up the plate and utensils."
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        stop music fadeout 3.0
        n "Then he turned to take them to the kitchen with a frustrated sigh."
        jump ren_day1_knife_shortcut

label ren_day1_knife:
show ren:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.2 alpha 0.0 xalign 0.6
n "I chewed my lip as he took them to the kitchen."
n "This house is nice..."
n "I nestled into the comfy chair."
n "And his cooking is so good..."
n "Maybe this isn't so bad..."
label ren_day1_knife_shortcut:
n "I considered pulling my knees up to my chest while I waited."
n "I lifted my foot slightly, hearing the clink of the chain, reminding me."
n "...Right."
show bg_ren_livingroom:
    subpixel True
    xalign 0
    easeout 0.3 xalign 1.0
n "I looked up in time to see him returning."
$ rears,rbase,rexp,rblush = 1,1,3,0
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
label ren_day1_dog_shortcut:
play music ren_warppiano fadein 3.0
ren "All right."
n "He quickly wiped his hands on his shirt."
ren "Maybe it's best that we just get you settled in."
$ rexp = 15
ren "Give you some time to adjust."
n "I just looked at him."
n "What did he mean by 'settled in'?"
$ rexp = 19
n "To my surprise, he pulled out a small key and bent down to my shackle."
ren "Don't forget about your collar."
n "I gulped, reaching up to touch it."
ren "I'm going to open this...but if you aren't good, I'll have to shock you."
$ rexp = 16
n "I nodded slowly."
n "As long as he takes that off, I'm in a better position..."
$ rexp = 15
n "It clicked open and fell to the floor."
$ time = 2.0
$ timer_range = 2.0
$ timer_jump = 'ren_day1_norun'
show screen countdown
menu:
    "-Run!-":
        hide screen countdown
        jump ren_day1_run
    "-Attack him!-":
        hide screen countdown
        jump ren_day1_lunge

label ren_day1_run:
$ ren_dom -= 10
$ rexp,rears = 2,1
stop music
ren "Woah!"
$ ren_shocking = True
play sound ren_shocked
$ rbase,rexp,rears = 3,16,2
show screen disableclick(2.0)
$ health -= 10
$ sanity -= 10
ren "{cps=12}...{/cps}{w=2.0}{nw}" with smallshake
$ rears,rbase,rexp = 3,2,16
$ ren_shocking = False
stop sound
play music ren_warppiano fadein 3.0
n "My muscles locked up mid-stride and I fell face-first to the floor." with vpunch
p "Ugh..."
call ren_subroutine from _call_ren_subroutine_5
ren "..."
$ rears,rbase,rexp = 1,1,15
ren "Come on, [player_name]."
ren "You know that won't work."
n "He leaned down to help me to my feet."
$ rexp = 8
ren "I'm just going to show you your room!"
jump ren_day1_bedroom_shortcut

label ren_day1_lunge:
$ ren_dom += 10
$ rexp,rears = 2,3
show ren:
    subpixel True
    ypos 0
    easeout 0.1 ypos 40
    easein 0.2 ypos 0
stop music fadeout 1.0
n "Aughh!"
$ rbase,rexp,rears = 2,17,2
n "He let out an inhuman growl as he dodged me."
p "No-"
play music ren_obsessed fadein 1.0
$ ren_shocking = True
play sound ren_shocked
$ rbase,rexp,rears = 3,18,2
show screen disableclick(2.0)
$ health -= 10
$ sanity -= 10
p "{cps=12}Sto-AAHH{/cps}{w=2.0}{nw}" with smallshake
$ rears,rbase,rexp = 3,2,17
$ ren_shocking = False
stop sound
n "I fell to the floor."
p "Ughhhnn..."
call ren_subroutine from _call_ren_subroutine_6
ren "..."
$ rears,rbase,rexp = 3,2,11
ren "..."
$ ren_shocking = True
play sound ren_shocked
$ rbase,rexp,rears = 3,9,2
show screen disableclick(2.0)
$ health -= 15
$ sanity -= 15
p "{cps=12}NnnGG!{/cps}{w=2.0}{nw}" with largeshake
$ rears,rbase,rexp,rblush = 2,2,11,1
$ ren_shocking = False
stop sound
call ren_subroutine from _call_ren_subroutine_7
$ ren_love += 10
n "He was panting softly."
$ rexp,rears = 7,3
n "I laid motionless on the ground, letting out half a choked sob."
$ rblush = 0
ren "That wasn't a good idea, [player_name]."
n "He stood over me."
$ rexp = 6
ren "I was just trying to show you your bedroom."
$ rexp = 16
ren "Are you going to come nicely now?"
stop music fadeout 1.0
n "I focused on the remote in his hand."
play music ren_warppiano fadein 3.0
p "Yes! Yes! Okay!"
$ rbase,rexp,rears = 1,8,1
ren "Good. Now get up."
n "I had to brace myself on the chair."
n "It still hurt... my muscles were on fire."
jump ren_day1_bedroom_shortcut

label ren_day1_norun:
$ rexp,rears = 8,1
$ ren_dom -= 10
n "His tail swished slowly as he started to relax."
ren "Okay, come with me!"
$ rexp = 1
ren "I'll show you your room."
n "'My' room...?"
label ren_day1_bedroom_shortcut:
n "He held my arm gently and guided me down a short hallway to a door."
scene bg_ren_bedroom
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
n "He swung the door open..."
n "A simple bedroom."
n "No bars or chains or anything..."
$ rexp = 14
ren "I know it's kind of boring."
ren "But I didn't know what you'd like."
$ rexp = 8
ren "Once I get to know you better, we can spruce it up!"
n "My eyebrows furrowed."
menu:
    "\"How long are you planning to keep me here?\"":
        $ rexp,rears = 6,3
        $ ren_love -= 10
        n "He stiffened at the question."
        ren "J-just..."
        ren "Get some rest."
        $ rexp,rears = 19,3
        ren "..."
        ren "We can talk more tomorrow."
    "\"It's...nice.\"":

        $ ren_love += 10
        $ rexp = 4
        n "He lit up."
        ren "I'm glad you like it!"
        $ rexp = 1
        ren "Just holler if you need anything."
        ren "I'll let you get some rest!"
    "-Say nothing-":

        $ rexp,rears = 6,3
        ren "..."
        ren "W-well..."
        ren "I'm sure you could use some time to relax."
        ren "I'll let you get some rest."

show ren:
    subpixel True
    alpha 1.0
    xalign 0.5
    easeout 0.2 alpha 0.0 xalign 0.6
n "He slipped out the door and closed it behind him, leaving me in the room."
n "I could hear him walking away, but from what I could tell..."
n "He didn't lock it or anything."
n "I looked over to the bed, touching the metal ring around my neck."
n "He has to sleep sometime."
n "Maybe for now... I'll just bide my time."
n "I went to the window first."
n "There didn't even seem to be a way to open it."
n "The glass looked too thick to smash with anything in the room."
n "Outside..."
n "It's some rich-looking suburban neighborhood."
p "Where the hell am I...?"
n "The window was facing some fancy backyards."
n "It looked like the kind of place that had homeowner meetings, book clubs, and backyard barbecues."
p "Tsk."
n "I explored the bedroom slowly."
n "...It was just like a hotel room."
n "Nothing in any of the drawers."
n "Clean looking, clean smelling."
n "Now that I was thinking about it..."
n "The living room sort of looked unused too."
n "Or at least, really new."
n "What kind of person...fox...lives in a house like this?"
n "I flopped on the bed, staring upward."
n "I tried to go through theories in my head, to make this make sense."
n "The theories only grew more and more outlandish as I started to doze."
stop music fadeout 1.0
scene black with dissolve
n "At some point I wouldn't be able to remember, I fell asleep."
jump ren_night1

label ren_day1_food2_pet:
n "I flopped back into the chair."
n "Then I looked down to my leg and gave the chain a tug."
n "That chain certainly isn't breaking."
n "I heard the quiet sound of cooking start again in the kitchen."
n "The shackle on my ankle looked as indestructible as the collar on my neck."
n "I heard the hiss of something in a skillet."
n "My eyes travelled down the chain to the wall."
n "That's...starting to smell really good..."
n "I shook my head." with hpunch
n "Concentrate!"
n "The wall."
n "It's just a normal house wall."
n "That's got to be the weak point."
n "I stared for a while, contemplating if I should just get up right now..."
n "I don't think that's a good idea."
n "He'd hear me and he's still got that remote..."
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
$ rears,rbase,rexp = 1,1,11
ren "[player_name]."
n "I jolted."
n "He's so quiet..."
ren "I've got your dinner."
n "He held up a bowl of steaming potatoes and cut up meat."
n "A...dog bowl."
n "My gaze dropped as he put it on the floor."
ren "...Eat it."
$ rears,rbase,rexp = 3,1,16
n "I looked up and locked eyes with him."
menu:
    "-Eat it-":
        $ ren_dom -= 20
        n "I looked back down and gulped."
        n "I'm so hungry..."
        n "And that smell..."
        $ rears,rbase,rexp = 1,1,11
        n "I shifted to kneel on the ground."
        n "Fuck pride...I'm starving."
        n "I tried to ignore his happily swishing tail as I took a bite from the bowl."
        p "...!"
        n "It's really good..."
        $ health += 5
        $ sanity += 5
        n "I went in for more, feeling less and less awkward as I emptied the bowl."
        $ rexp,rblush = 8,1
        n "I wiped my face and finally looked back up."
        $ rexp = 4
        ren "Wow, you WERE hungry!"
        $ rexp,rblush = 8,0
        n "I pulled myself back into the chair without a word."
        jump ren_day1_dog_shortcut
    "-Kick it-":

        $ ren_dom += 10
        $ ren_love -= 10
        $ rexp,rears = 2,1
        n "I looked him straight in the eye and kicked the dog bowl."
        $ rexp,rears = 16,2
        p "No."
        $ rexp,rears = 17,2
        ren "..."
        $ rexp,rears = 19,2
        ren "F-fine."
        $ rexp,rears = 16,2
        ren "You can just go hungry then."
        $ rexp,rears = 6,3
        ren "..."
        $ rexp = 19
        jump ren_day1_dog_shortcut

label ren_night1:
scene black
pause(1.5)
scene bg_ren_bedroom
$ sanity += 20
$ ren_kitchenknife = False
$ ren_sawcorpse = False
$ ren_sawbasement = False
play sound law_day fadein 1.0 loop
n "I shifted on the soft bed."
n "Waking up slowly, I began to wonder where I was."
n "Then it all came flooding back."
n "I flung myself up and off the bed."
n "I looked to the window."
n "It's... morning."
p "Ugh..."
n "I walked quietly to the bedroom door, straining to hear anything."
n "It's completely silent."
n "I tried the doorknob."
n "The door opened easily."
p "Oh..."
menu:
    "-Stay in the bedroom-":
        label ren_day2_stay_shortcut:
        $ ren_dom -= 30
        n "I thought about my options."
        n "What if Ren is out there...or comes back?"
        n "I shrank back from the door."
        n "What if he gets angry?"
        n "I softly closed the door."
        n "No... I think I'll stay right here."
        n "On my bed."
        n "I curled up on the sheets."
        scene black with dissolve
        n "I'll just rest until he comes back."
        pause 1.5
        scene bg_ren_bedroom with vpunch
        n "I jolted upright at hearing a door slam."
        n "I lost track of time..."
        n "I got up and pressed my ear to the door."
        n "Is he back?"
        jump ren_day2_lawrence
    "-Call for Ren-":

        n "I tentatively poked my head out the door."
        p "Ren?"
        n "I paused, waiting for a reply."
        p "Are you here?"
        pause(1.5)
        n "Nothing but my own voice."
        n "I guess he's not home...?"
        menu:
            "-Stay in the bedroom-":
                jump ren_day2_stay_shortcut
            "-Explore the house-":
                jump ren_day2_explore_option_shortcut
    "-Explore the house-":

        label ren_day2_explore_option_shortcut:
        $ ren_explore_options = 0
        $ ren_explore_frontdoor = False
        $ ren_explore_kitchen = False
        $ ren_explore_upstairs = False
        $ ren_explore_basement = False
        n "Well I'm not just gonna stay in here."
        scene bg_ren_livingroom:
            xalign 1.0
        n "I tiptoed into the living room where I was chained before."
        n "Still no sign of Ren."
        n "I looked around the room at my options."
        n "There's stairs to a second floor..."
        n "Another door under those stairs."
        n "Then of course there's the kitchen... maybe there's a weapon there."
        n "I looked towards the entranceway."
        n "Or I could just make a break for it."
        label ren_day2_explore_shortcut:
        if ren_explore_options >= 2:
            jump ren_day2_timesup
        menu:
            "-Check the kitchen-" if ren_explore_kitchen == False:
                $ ren_explore_kitchen = True
                $ ren_explore_options += 1
                jump ren_day2_explore_kitchen
            "-Explore upstairs-" if ren_explore_upstairs == False:
                $ ren_explore_upstairs = True
                $ ren_explore_options += 1
                jump ren_day2_explore_upstairs
            "-Open the door under the stairs-" if ren_explore_basement == False:
                $ ren_explore_basement = True
                $ ren_explore_options += 1
                jump ren_day2_explore_basement
            "-Leave the house-" if ren_explore_frontdoor == False:
                $ ren_explore_frontdoor = True
                $ ren_explore_options += 1
                jump ren_day2_explore_frontdoor

label ren_day2_explore_kitchen:
scene bg_ren_kitchen with dissolve
n "I wandered into the kitchen."
n "It still smelled faintly of Ren's cooking."
n "I went straight to the drawers."
n "...neat and organized... like the rest of the house."
n "There!"
n "I spotted a large knife."
menu:
    "-Take the knife-":
        $ ren_kitchenknife = True
        n "I grabbed the knife."
        n "At least now I can defend myself..."
    "-Leave the knife-":
        n "...I better not."
        n "I closed the drawer slowly."
n "I looked back towards the living room."
jump ren_day2_explore_shortcut

label ren_day2_explore_basement:
$ ren_sawbasement = True
n "I stared at the simple looking door."
n "There was something weird about it."
n "...The handle was strange."
n "I turned it, and heard a couple clicks."
n "It's heavy!"
n "As I swung the door open, I saw that the other side was thick and metal."
show black
n "What the...hell..."
show bg_ren_basementstairs:
    alpha 0
    ease 1.0 alpha 0.5
    pause (0.05)
    alpha 0
    pause (0.05)
    alpha 0.75
    pause (0.05)
    alpha 0
    pause (0.1)
    ease 0.5 alpha 1
pause(2.5)
scene bg_ren_basementstairs
play sound law_brownnote fadein 2.0 loop
n "I fumbled for a lightswitch and eventually, a flickering light revealed stairs into a dark basement."
n "Something about it was making me nervous."
menu:
    "-Go down-":
        n "I have to know what's down there."
        n "I stepped down the wood stairs, creaking softly."
        n "It smells musty and...coppery?"
        n "I felt along the wall, looking for another light."
        scene bg_ren_basement
        n "There!"
        n "..."
        n "I stared at my surroundings."
        n "It's nothing like the rest of the house..."
        n "It feels old and used and lived-in."
        n "There's stains..."
        n "A shiver crawled up my spine."
        n "Everywhere."
        n "I gulped and took an involuntary step back."
        n "The woodworking tools shone in a sinister way under the artificial basement light."
        n "All I could hear was the hum of a small fridge and a large freezer."
        n "My gaze locked on the deep freeze."
        n "More stains."
        n "I approached it."
        n "I was filled with an irrational need to open it."
        menu:
            "-Open it-":
                $ ren_explore_options += 1
                $ ren_sawcorpse = True
                n "I placed my shaking hands on the lid and lifted."
                n "It opened with a suctioned crack."
                n "My eyes adjusted to the light."
                scene white with dissolve
                scene cg_ren_stradecicle with dissolve
                $ sanity -= 30
                play music ren_obsessed fadein 0.5
                stop sound fadeout 1.0
                p "OH GOD!"
                scene black with vpunch
                scene bg_ren_basement
                n "I stumbled backwards, falling to the floor."
                n "The lid of the freezer fell with a bang."
                p "No... no no..."
                n "He's a murderer!"
                n "I have to get out of here!!"
                n "I scrambled to my feet and ran up the stairs."
            "-Leave it alone-":
                n "I lowered my shaking hand."
                n "No."
                n "My instincts are screaming at me."
                n "I have to get out of this basement."
                n "I turned and ran up the stairs."
    "-Stay-":
        n "Screw this."
        n "I've seen enough horror movies to know better."
        scene bg_ren_livingroom
        n "I closed the strangely thick door and looked back into the living room."
jump ren_day2_explore_shortcut

label ren_day2_explore_upstairs:
n "Maybe there's something upstairs that can help me."
scene bg_ren_hallway with dissolve
n "I climbed the carpeted steps to another floor that looked just like the first."
n "Clean... simple."
n "It looks like one of those example houses people look through to enter a lottery."
n "I spotted an open door to a small bedroom."
n "I walked towards it, the only evidence of something out of place."
scene bg_ren_renroom with dissolve
n "A desk, clothing strewn around, even some garbage."
n "It would look like any single guy's bedroom if there was a bed."
n "But there was just a pile of blankets on the floor..."
n "I looked closer."
n "Covered in orange fur!?"
n "Is this where he sleeps...?"
n "For the first time, I felt like I was invading someone's personal space."
scene bg_ren_hallway with dissolve
n "I backed out of the room and closed the door."
jump ren_day2_explore_shortcut

label ren_day2_explore_frontdoor:
n "I've got to risk it."
n "I'd be crazy not to."
scene bg_ren_doorway with dissolve
n "I walked quickly to the front door."
n "About two meters from the door, I heard a shrill beep."
n "I stopped in my tracks."
n "I think...it came from my collar."
n "Is...is that a warning?"
menu:
    "-Approach the door anyway-":
        n "Well, whatever it is..."
        n "I can't turn back now."
        n "I took a few cautious steps forward-"
        $ ren_shocking = True
        show screen disableclick(3.0)
        play sound ren_shocked
        $ health -= 30
        $ sanity -= 30
        p "{cps=12}!!!!{/cps}{w=2.0}{nw}" with largeshake
        p "{cps=12}{/cps}{w=1.0}{nw}" with largeshake
        call ren_subroutine from _call_ren_subroutine_8
        scene black with vpunch
        $ ren_shocking = False
        stop sound
        pause(1.0)
        scene bg_ren_doorway with Dissolve(2.0)
        $ ren_explore_options += 1
        p "Uggnn..."
        n "My head was buzzing."
        n "I struggled to climb back to my feet."
        n "I... can't do that again..."
    "-Go back to the living room-":

        n "I touched the collar."
        n "He probably did something to it..."
        n "He wouldn't just let me walk out the door."
        n "I took a few steps back and went back into the living room."
jump ren_day2_explore_shortcut

label ren_day2_timesup:
n "I heard a door open and a loud thump."
n "Ren!"
n "I looked around quickly."
n "I... I should get back to the bedroom!"
n "I ran as quickly and quietly as I could back to the room he left me in."
scene bg_ren_bedroom with dissolve
n "I closed the door silently, my heart thudding."
n "I don't think he noticed anything."
n "I let out a sigh of relief before pressing my ear to the door."
label ren_day2_lawrence:
stop music fadeout 1.0
n "More thumps..."
ren "{size=10}Hahaha...come on!{/size}"
ren "{size=10}Isn't this what you wanted...?{/size}"
n "Who is he talking to!?"
n "He was moving farther away."
n "I strained to hear him."
ren "[player_name]!!"
n "I jumped."
play music ren_warppiano fadein 1.0
ren "Are you in your room? Come out here!"
ren "I have a surprise for you~"
if sanity >= 30:
    p "Ye-"
    n "I cleared my throat, realizing my voice was choked."
    p "Yes..."
    n "I came out of the room slowly."
    scene bg_ren_livingroom at right with dissolve
    show ren:
        subpixel True
        alpha 0.0
        xalign 0.6
        easeout 0.2 alpha 1.0 xalign 0.5
    $ rears,rbase,rexp = 1,1,8
    ren "Did you have a nice rest?"
    if ren_dom > 50:
        p "...Sure."
    else:
        n "I hoped he couldn't see me sweating."
        p "Uh...y-yeah..."
    $ rexp = 20
    ren "Great!"
    $ rexp = 8
    ren "Well, come on!"
    ren "I've got everything set up in the spare room."
    n "He motioned me over to a door that I had assumed was for a closet."
    $ rexp = 4
    ren "Check it out~"
    n "I cautiously looked inside the dark room."
else:
    n "No... God..."
    n "I can't take any more..."
    n "I stumbled out to see him."
    scene bg_ren_livingroom at right with dissolve
    ren "Well, come on!"
    ren "I've got everything set up in the spare room."
    n "He motioned me over to a door that I had assumed was for a closet."
    $ rexp = 4
    ren "Check it out~"
    n "I was shaking."
scene black with dissolve
stop music fadeout 1.0
n "My eyes adjusted to the darkness..."
scene cg_ren_lawrence_1 with dissolve
play music ren_vampire fadein 3.0
n "!!!"
show cg_ren_lawrence_2:
    subpixel True
    alpha 0.0
    xpos 10
    easeout 0.1 alpha 1.0 xpos 0
$ rexp = 8
ren "Well?"
p "What..."
n "It was the other guy from the pub."
ren "You remember Lawrence."
n "I just stared, astounded."
ren "Lawrence was going to be my new friend..."
ren "But then you came along! {image=icon_heart.png}"
n "He grinned at the terrified man in the chair."
scene cg_ren_lawrence_3 with dissolve
ren "It's weird how quickly things can change isn't it?"
n "I gulped hard."
p "And what uh... why is he here now?"
$ rexp = 4
n "Ren flashed me a fanged smile."
if ren_kitchenknife == True:
    ren "Well, well."
    ren "It looks like you already know, hm?"
    n "I looked at him in confusion then looked down, following his gaze."
    n "The knife from the kitchen!"
    n "I gasped loudly."
    n "I'd forgotten that I was holding it..."
else:
    n "Then he reached for something behind himself."
    n "He revealed a knife."
    n "Before I could react in fear, he held it out to me."
ren "I want us to share something really special, [player_name]."
n "He couldn't be serious..."
n "I held the knife."
p "You...want me to hurt him?"
n "I heard Lawrence's muffled whimper as Ren looked me over."
ren "Hurt him."
ren "Make him bleed... cry..."
ren "Kill him."
n "The knife quivered in my hand."
if sanity >= 20:
    if ren_food_attack == True:
        n "Ren flashed the remote."
        ren "And don't you dare try to attack me again."
    n "I considered the people in the room and the collar around my neck."
    menu:
        "\"He didn't do anything to deserve this.\"":
            n "I looked into the panicked eyes of the man in the chair."
            p "I mean, sure...he freaked me out a little after we left the pub..."
            p "But that's no reason to kill anyone!"
            n "Ren looked at me dully."
            ren "I used to think that way once..."
            ren "This has nothing to do with what he deserves."
            ren "..."
            ren "The whole world is unfair, [player_name]."
            ren "You need to understand that to be free."
            ren "And he needs to suffer for us to get what we want."
            p "But I don't want this..."
            ren "You NEED this!"
            n "He was getting more excited."
            ren "I know it feels scary at first..."
            ren "But we'll have a bond deeper than you can imagine right now."
            n "He looked down at Lawrence."
            ren "We need blood for that..."
            menu:
                "-Keep refusing-":
                    jump ren_law_refusekill
                "-Give in-":
                    jump ren_law_kill
        "\"Please don't make me...\"":

            $ ren_dom -= 10
            p "Ren..."
            p "I-I'll do anything else..."
            p "Just please don't make me hurt anyone..."
            ren "..."
            ren "Just don't have the stomach for it, do you?"
            n "I shook my head."
            ren "I guess it is asking a little much."
            n "He held out his hand for the knife."
            ren "You can watch me do it."
            n "Lawrence let out another whimper."
            menu:
                "-Give Ren the knife-":
                    $ ren_dom -= 30
                    n "I squeezed my eyes shut and surrended the knife to Ren."
                    ren "I suppose I should be more flexible..."
                    n "He took the knife and moved behind Lawrence."
                    scene cg_ren_lawrence_8 with dissolve
                    n "He moved the knife gently against the skin of Lawrence's neck."
                    ren "I didn't think you'd be so delicate."
                    n "I couldn't tell if he was talking about me or Lawrence."
                    n "But I didn't dare make a sound."
                    n "Ren's arm moved suddenly, swiftly."
                    scene cg_ren_lawrence_10 with dissolve
                    n "He plunged the knife into Lawrence's arm."
                    n "He lurched forward with a muffled scream."
                    n "Ren looked up at me excitedly."
                    n "His eyes seemed more like an animal's now..."
                    n "I just kept watching... frozen in terror."
                    n "He was breathing harder..."
                    n "He twisted the blade and grinned, showing his fangs."
                    n "I couldn't move."
                    n "This can't be real."
                    ren "How do you feel?"
                    n "I moved my lips but no words escaped them."
                    scene cg_ren_lawrence_9 with dissolve
                    n "He wrenched the knife from Lawrence's shoulder and over his neck."
                    ren "Answer me..."
                    n "I forced myself, straining against the fear like a nightmare."
                    p "I..."
                    $ sanity -= 10
                    p "I'm scared!"
                    n "Once the dam broke, the words flowed out of me."
                    p "This is wrong!"
                    p "Can't you see he's in pain!?"
                    $ sanity -= 10
                    p "I'm scared! I'm scared! I'M SCARED!"
                    p "I DON'T WANT THIS!!"
                    n "Ren laughed softly."
                    ren "That's better."
                    scene black with dissolve
                    n "I closed my eyes and sighed in relief."
                    n "That relief only lasted a second before I heard a muffled scream."
                    scene cg_ren_lawrence_11 with vpunch
                    n "I felt helpless once again as I watched him plunge the blade into Lawrence's gut."
                    n "I couldn't look away."
                    scene cg_ren_lawrence_12 with dissolve
                    n "I watched him drag it upwards as blood spilled out."
                    $ sanity -= 10
                    n "His...his organs..."
                    n "I couldn't close my eyes..."
                    $ sanity -= 10
                    n "I saw Lawrences eyes... Ren's... and everything slowly slipping out of him."
                    n "He's still alive..."
                    n "He's still..."
                    scene black with Dissolve(1.5)
                    stop music fadeout 1.0
                    n "I must have stopped breathing."
                    n "I blacked out."
                    jump ren_day3
                "\"I don't want him to die at all!\"":

                    label ren_law_refusekill:
                    n "Ren started to look like he was losing his patience..."
                    p "I...I won't do it!"
                    ren "..."
                    n "He held up the remote."
                    p "No wai-"
                    $ ren_shocking = True
                    play sound ren_shocked
                    show screen disableclick(2.0)
                    $ health -= 10
                    $ sanity -= 10
                    p "{cps=12}AHHH!{/cps}{w=2.0}{nw}" with smallshake
                    $ ren_shocking = False
                    stop sound
                    scene black with vpunch
                    n "I stumbled backward, dropping the knife."
                    label ren_lawrencekill_shortcut:
                    n "He picked it up quickly and turned to Lawrence."
                    ren "Looks like it's you lucky day, Law."
                    n "Ren cut the gag off from Lawrence's face."
                    ren "Do you want to be the one that leaves this room?"
                    law "...Yes."
                    scene bg_ren_darkroom
                    $ rexp,rbase,rears = 9,1,2
                    show ren:
                        ypos 70
                        subpixel True
                        alpha 0.0
                        xalign 1.0
                        easeout 0.2 alpha 1.0 xalign 0.9
                    n "Ren quickly sawed through the zip ties and rope holding Lawrence down."
                    n "Then, handed him the knife."
                    p "W...what...?"
                    p "Wait!"
                    $ lexp,lbase,lbangs,lblush = 13,12,3,0
                    show law behind ren:
                        subpixel True
                        alpha 0.0
                        xalign 0.0
                        easeout 0.2 alpha 1.0 xalign 0.1
                    n "Lawrence stood up."
                    $ rbase = 2
                    p "Please! Lawrence!"
                    $ rexp = 16
                    p "Ren's the one-"
                    $ rbase = 3
                    $ ren_shocking = True
                    play sound ren_shocked
                    show screen disableclick(2.0)
                    $ health -= 15
                    $ sanity -= 15
                    p "{cps=12}Hrk!{/cps}{w=2.0}{nw}" with largeshake
                    $ rbase = 2
                    $ ren_shocking = False
                    stop sound
                    n "I fell backward, hitting the wall behind me." with vpunch
                    $ rexp = 22
                    ren "I'll keep [player_name] down."
                    $ lexp = 9
                    ren "Go ahead."
                    scene cg_ren_law_killmc with dissolve
                    n "Lawrence loomed over me with the knife."
                    law "...I'll make it quick."
                    n "I tried one last desperate scramble for the door."
                    $ ren_shocking = True
                    play sound ren_shocked
                    show screen disableclick(2.0)
                    $ health -= 15
                    $ sanity -= 15
                    scene black
                    p "{cps=12}{/cps}{w=2.0}{nw}" with largeshake
                    $ ren_shocking = False
                    stop sound
                    n "I sobbed after the shock."
                    n "I couldn't move, it hurt so much."
                    $ health -= 100
                    p "AH!" with vpunch
                    n "Then I was pinned to the floor by a knife in my back."
                    p "All I could do was cough weakly and twitch."
                    law "..."
                    stop music fadeout 1.0
                    ren "I knew we'd get along, Law~ {image=icon_heart.png}"
                    hide screen health_bar
                    hide screen sanity_bar
                    hide ren_collar onlayer screens
                    $ persistent.ren_ending_law = True
                    play music law_twinkle fadein 1.0
                    scene endslate with Dissolve(1.0)
                    screen ren_ending_law:
                        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                        text "\n\n\n\n{=endslate_subtitle}You took Law's place.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                    show screen ren_ending_law
                    with Dissolve(1.0)
                    pause
                    $ renpy.full_restart()
        "-Cut Lawrence-":

            label ren_law_kill:
            n "I don't.... have a choice."
            n "I stepped closer to Lawrence with the knife."
            n "I considered apologizing to him..."
            n "But what would be the point?"
            ren "Go on~"
            menu:
                "-Make it quick-":
                    n "I leaned to press the knife to his neck."
                    n "...At least I can try to make this as painless as possible."
                    n "Part of me wanted to look away from him."
                    n "To stop seeing the animal-like fear in his eyes..."
                    n "But I couldn't."
                    n "I looked him in the eye and swept the blade across his flesh."
                    scene black
                    n "It only took a moment."
                    scene cg_ren_lawrence_4 with dissolve
                    n "I watched the blood spread down his chest as he convulsed weakly."
                    n "I could feel hot tears streaming down my face, matching the spill."
                    n "I dropped the knife."
                    n "After what felt like much too long, he finally stopped moving."
                    n "I jumped in surprise, feeling Ren's arm snake around my waist."
                    ren "I knew we'd get along~"
                    p "I...I..."
                    ren "Hey..."
                    scene black with vpunch
                    n "I collpased to my knees."
                    p "I'm a murderer..."
                    n "He rubbed my back affectionately."
                    ren "Don't worry [player_name]."
                    ren "So am I..."
                    ren "I understand you."
                    n "I hugged my knees."
                    $ ren_love += 10
                    ren "I'm the only one that really understands you, now."
                    n "I don't want this..."
                    n "He took his hand from my back and I immediately missed the contact."
                    ren "Why don't you go relax, hm?"
                    ren "I need to wash up {image=icon_heart.png}"
                    n "I nodded, my throat too dry to speak."
                    n "I shakily stood up and staggered out of the small room."
                    scene bg_ren_livingroom:
                        xalign 1.0
                    n "The bright, clean living room felt like a joke."
                    n "After what I just did..."
                    n "I fell onto the couch."
                    n "I buried my face in the cushions."
                    p "This can't be real..."
                    scene black with dissolve
                    stop music fadeout 1.0
                    n "I tried to relax, but ended up just dozing restlessly."
                    jump ren_day3
                "-Do it slowly-":

                    $ ren_dom += 10
                    n "I moved closer to Lawrence, watching as he began to panic more."
                    n "I wasn't sure where to start..."
                    n "I looked at his arm and touched the blade to his skin."
                    n "I've never done this to anyone before..."
                    n "I pressed the knife down, sliding it...testing it."
                    scene cg_ren_lawrence_5 with dissolve
                    n "His arm jerked against the rope and zip ties as he groaned into his gag."
                    n "Such a strong reaction...even though it was so easy..."
                    n "I looked up to his face."
                    n "He was breathing hard."
                    n "Scared."
                    n "I moved the knife over his skin again."
                    n "He muffled more sounds."
                    n "I could tell by the begging look in his eyes that he was trying to say-"
                    n "'No no no...'"
                    n "He wants so badly for this to stop."
                    n "More than he's ever wanted anything."
                    n "I flashed the knife in front of him."
                    p "But there's nothing you can do about it... is there?"
                    n "His head jerked up and I realized I spoke aloud."
                    n "The whole room was silent..."
                    n "Ren and Lawrence were frozen, anticipating what I'd do next."
                    n "I'm the one in charge of this moment..."
                    scene cg_ren_lawrence_6 with dissolve
                    n "I pressed the knife into Lawrence's thigh."
                    n "He began to scream into the gag as I pressed it further into him... slowly."
                    n "Seeing him unable to stop me, even though he so desperately wanted to..."
                    n "I twisted the knife."
                    n "It filled me with something I'd never really felt before."
                    n "Strangely, I was more aware of the collar around my neck as I did it."
                    p "I've been helpless too."
                    n "I pulled the knife out."
                    n "He was shaking... I lifted his chin so he could look at me."
                    n "This was important."
                    p "I understand how you feel, Lawrence."
                    n "I wiped the bloody knife on his shirt."
                    p "You can't stop this."
                    n "Terror flooded his face."
                    n "Why did that feel {i}so good{/i} to say?"
                    n "I pushed the knife into his belly, faster."
                    scene cg_ren_lawrence_7 with dissolve
                    n "I could tell his screaming was becoming hoarser, even with the gag."
                    n "He's so soft..."
                    n "I pulled the knife through his flesh and watched blood and other things that should stay in the human body fall out of him."
                    n "His head fell to his chest."
                    p "..."
                    n "After an amount of time I couldn't properly recount, I realized I was panting."
                    p "Ha...haha..."
                    n "I glanced over at Ren."
                    n "I was surprised to see a hint of fear."
                    n "I grinned at him."
                    p "That wasn't so hard..."
                    n "I sheathed the knife in Lawrence's chest."
                    ren "Ah.. y-yeah."
                    ren "I guess it wasn't!"
                    ren "Haha..."
                    ren "Y-you did great..."
                    n "Was he not expecting me to do it?"
                    n "I scoffed."
                    ren "I should clean up..."
                    n "He smiled at me warmly."
                    ren "You... can just relax now."
                    p "Sure."
                    n "I turned and left him in the small dark room."
                    scene bg_ren_livingroom with dissolve:
                        xalign 1.0
                    n "The living room seemed brighter and more comfortable than before."
                    n "I flopped on the couch, leaning back."
                    n "Something was telling me I should be more bothered by what just happened."
                    stop music fadeout 1.0
                    scene black with dissolve
                    n "I closed my eyes."
                    n "But why bother freaking out now?"
                    n "I relaxed on the soft cushions and ended up dozing."
                    jump ren_day3
else:
    n "I-I can't..."
    scene black with vpunch
    n "I dropped the knife and fell to my knees."
    p "No...no no no..."
    n "I clutched my head"
    p "I CAN'T TAKE ANY MORE!"
    ren "..."
    n "Ren turned his eyes to the knife on the floor."
    ren "Hmph."
    jump ren_lawrencekill_shortcut

label ren_day3:
$ sanity += 20
if ren_dom > 20:
    jump ren_day3_dominant
elif ren_dom > -20:
    jump ren_day3_neutral
else:
    jump ren_day3_submissive

label ren_day3_submissive:
scene bg_ren_livingroom at right with dissolve
$ rtail = 6
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
$ rears,rbase,rexp = 1,4,8
play music ren_warppiano fadein 1.0
ren "Hey [player_name]."
$ rears,rexp = 1,4
ren "You kinda dozed off there!"
p "Uh...?"
n "He's changed clothes... how long was I-"
n "Oh god."
n "I clutched my head, remembering what happened."
$ rears,rexp = 1,14
ren "Are you still feeling upset?"
$ rears,rexp = 1,8
n "Did that really happen!?"
p "Lawrence..."
ren "Oh..."
$ rears,rexp = 1,1
$ sanity -= 10
ren "He's dead! {image=icon_heart.png}"
$ rears,rexp = 1,8
ren "You did such a good job..."
n "No..."
n "I tried to bring my knees to my chest."
n "I was stopped by the sound of metal clinking."
n "I whimpered as I realized I was chained again."
$ rears,rexp = 3,15
ren "Awwww..."
ren "You're so sweet and gentle."
n "I felt like I was breathing too fast."
$ rears,rexp = 1,14
ren "Hey hey..."
ren "Don't panic now!"
n "He rested a hand on my shoulder."
$ rears,rexp = 1,8
ren "You're safe and sound, right where you belong."
menu:
    "{image=icon_lowsanity.png} \"I'm sorry, you're right.\"" if sanity <= 30:
        $ ren_love += 10
        $ rears,rexp = 3,15
        n "I lowered my head."
        n "I can't leave now..."
        n "Not after what I..."
        ren "Don't worry, [player_name]."
        ren "We've got this whole house, plenty of money..."
        $ rears,rexp = 3,15
        ren "I'll take really good care of you."
        n "He crooned softly as he ran fingers through my hair."
        $ rears,rexp = 1,14
        ren "Why don't we take it easy for the rest of the day?"
        n "I looked up at him."
        n "For some reason I wanted to cry."
        $ rears,rexp = 1,1
        ren "I've got movies, and I can make popcorn!"
        n "He patted me before I could respond."
        ren "Just sit tight!"
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "I sat there in stunned silence while Ren ran to the kitchen to... make popcorn."
        n "He was humming softly."
        n "Eventually, the warm smell and sound of kernels giving in to the heat reached me."
        n "He yelled to me."
        ren "What kind of movies do you like?"
        menu:
            "\"Romance\"":
                $ ren_love += 10
                ren "You like those too?"
                n "He returned with the popcorn and began to rummage through a cabinet."
                ren "Hmm... romance, romance..."
                ren "Don't have too many of those unfortunately..."
            "\"Horror\"":
                n "He returned with the popcorn and began to rummage through a cabinet."
                ren "Hmm... horror, horror..."
                ren "So many to pick from!"
            "\"Comedy\"":
                n "He returned with the popcorn and began to rummage through a cabinet."
                ren "Hmm... comedy, comedy..."
                ren "Most of these are in German..."
            "\"I don't know...\"":
                n "He returned with the popcorn and began to rummage through a cabinet."
                ren "Hmm..."
                ren "I'm sure we have {i}something{/i} good..."
        ren "...Oh~"
        n "I watched him pull out an unlabelled disc."
        ren "I have a better idea!"
        n "The thought of protesting was immediately replaced by the still-too-fresh memory of Lawrence's face."
        p "S..sure..."
        scene cg_ren_movies_bg at right with dissolve
        n "He drew the curtains and turned down the lights."
        ren "Now it's a little on the... uh..."
        n "He fiddled with the machine, trailing off and mumbling."
        ren "I mean, I didn't really like them at first."
        show cg_ren_movies_bg:
            xalign 1.0
            easeout 0.5 xalign 0.0
        pause 0.5
        show cg_ren_movies1:
            xalign -0.05
            alpha 0.0
            easeout 0.1 xalign 0.0 alpha 1.0
        n "He got it working and flopped down beside me."
        ren "But they really grew on me!"
        n "He rubbed my leg."
        ren "I'm sure you'll like them too."
        show cg_ren_movies_bg:
            xalign 0.0
            easeout 0.5 xalign 1.0
        show cg_ren_movies1:
            xalign 0.0
            easeout 0.5 xalign 1.0
        n "I flashed him a nervous small smile and turned my attention to the TV."
        show cg_ren_movies_bg2 behind cg_ren_movies1 at right with dissolve
        n "It looked like some sort of home video."
        show cg_ren_movies_bg3 behind cg_ren_movies1 at right
        play sound law_brownnote fadein 2.0 loop
        n "I squinted at the darkness before the room in the video suddenly brightened."
        n "!!!"
        n "It was a person tied to a chair!"
        n "I felt a bit sick, once again being forced to think of what we...what I..."
        p "Is...is this a joke?"
        ren "Shh!"
        n "He was smiling and crunching on a few kernels of popcorn."
        n "The person in the chair was clearly distressed, and their face was hidden under a bag."
        if ren_sawbasement == True:
            n "My eyes widened as I looked behind the stranger in the chair."
            n "It's...the basement."
            n "{i}THIS{/i} basement."
        show cg_ren_movies_bg4 behind cg_ren_movies1 at right with dissolve
        n "Another stranger appeared on screen."
        n "It was hard to identify much about him since he was wearing a bandana over his face."
        n "The stocky man greeted the camera cheerfully."
        n "I could tell he was smiling even though only his eyes were showing."
        n "My stomach turned as I felt more and more nervous."
        n "Ren continued watching as if it was any other movie."
        n "I was about to ask who he was before the man on screen spoke again."
        strade "Oh, you guys are pretty excited this morning!"
        n "He seemed to be addressing something beside the camera."
        n "A laptop...?"
        n "He was reading...something."
        strade "No no, we can't touch the eyes yet. How is she supposed to see us having fun first?"
        strade "Oh!"
        strade "Yeah, that's a better idea!"
        strade "You're a real gentleman, woundfucker88."
        strade "Bahaha!"
        n "I curled into a ball."
        n "Something about the man's laugh sent a shiver down my spine."
        n "My fears were soon realized as he withdrew a large hunting knife."
        n "He touched the woman's hand and I could hear whimpering inside the sack over her head."
        n "Her whimpering turned into a scream as he slammed the knife down, severing her pinky."
        n "I realized that the scream from the TV wasn't the only one in the room and I clamped a hand over my mouth."
        show cg_ren_movies_bg4:
            xalign 1.0
            easeout 0.3 xalign 0.0
        hide cg_ren_movies1
        show cg_ren_movies2:
            xalign 1.0
            easeout 0.3 xalign 0.0
        n "I turned to Ren, horrified to see him still completely relaxed."
        menu:
            "\"I can't take this! Please turn it off...\"":
                hide cg_ren_movies2
                show cg_ren_movies3 at left
                ren "Tsk!"
                ren "I'm trying to help you understand, [player_name]!"
                n "I tried to speak without trembling."
                p "Understand what!?"
                p "This..."
                p "This is sick!"
                p "What we did to Lawrence..."
                p "I don't..."
                p "I..."
                n "I couldn't help but start to cry."
                stop sound fadeout 1.0
                stop music fadeout 1.0
                n "He went silent and turned off the TV."
                n "Out of the corner of my eye I saw him take out the smaller remote."
                p "No no wai-"
                show screen disableclick(2.0)
                $ ren_shocking = True
                play sound ren_shocked
                $ health -= 10
                $ sanity -= 10
                p "AHHHggnnnn!{w=2.0}{nw}" with largeshake
                $ ren_shocking = False
                stop sound
                if health <= 0:
                    jump ren_ending_health
                scene black with vpunch
                n "I fell to the ground and moaned in pain."
                play music ren_obsessed fadein 1.0
                ren "I guess you won't learn just by watching."
                p "Ughn..."
                n "He started to drag me."
                n "His sharp claws in my leg kept me awake for only another couple seconds."
                stop sound fadeout 1.0
                stop music fadeout 1.0
                pause(2.0)
                jump ren_day3_basement
            "\"Who is that guy?\"":

                ren "That's Strade."
                n "He smiled wistfully and popped another kernel in his mouth."
                ren "This used to be his house."
                ren "All this stuff was his."
                n "He took a moment to sigh softly."
                ren "He used to make money like this."
                n "He gestured to the screen as the woman kept screaming."
                n "I was trying to ignore it."
                ren "He wrote all his passwords and stuff on paper."
                ren "So...so everything's mine now."
                show cg_ren_movies_bg5 behind cg_ren_movies2:
                    xalign 0.0
                    easeout 0.3 xalign 1.0
                show cg_ren_movies2:
                    xalign 0.0
                    easeout 0.3 xalign 1.0
                n "I gulped and glanced at the screen."
                n "Strade was lifting her shirt and the blood-"
                p "Ugh..."
                show cg_ren_movies_bg5 behind cg_ren_movies2:
                    xalign 1.0
                    easeout 0.3 xalign 0.0
                show cg_ren_movies2:
                    xalign 1.0
                    easeout 0.3 xalign 0.0
                n "I turned back to Ren."
                ren "He understood things."
                ren "He...taught me things."
                ren "And he took care of me."
                n "Ren's grin glinted from the light of the video."
                ren "Just like I'm gonna take good care of you!"
                hide cg_ren_movies2
                show cg_ren_movies4 at left
                n "Something changed in Ren's expression and I realized that I wasn't hiding my fear."
                scene cg_ren_movies_bg at left
                show cg_ren_movies5 at left
                stop sound fadeout 1.0
                stop music fadeout 1.0
                n "He went silent and turned off the TV."
                ren "Are you afraid of me?"
                ren "Still?"
                p "N...no, Ren..."
                ren "Don't lie to me!"
                n "I only saw him reach for the smaller remote out of the corner of my eye."
                show screen disableclick(2.0)
                $ ren_shocking = True
                play sound ren_shocked
                $ health -= 10
                $ sanity -= 10
                p "AHH!! {w=2.0}{nw}" with largeshake
                $ ren_shocking = False
                stop sound
                if health <= 0:
                    jump ren_ending_health
                scene black with vpunch
                n "I fell to the ground and moaned in pain."
                play music ren_obsessed fadein 1.0
                ren "I guess you won't learn just by watching."
                p "Ughn..."
                n "He started to drag me."
                n "His sharp claws in my leg kept me awake for only another couple seconds."
                stop sound fadeout 1.0
                stop music fadeout 1.0
                pause(2.0)
                jump ren_day3_basement
            "-Keep watching-":

                show cg_ren_movies_bg5 behind cg_ren_movies2:
                    xalign 0.0
                    easeout 0.3 xalign 1.0
                show cg_ren_movies2:
                    xalign 0.0
                    easeout 0.3 xalign 1.0
                n "I didn't want to say anything any more."
                n "I just hugged my knees and watched the sceen on the video unfold."
                n "The man kept checking what I assumed was some sort of chatroom."
                n "I guess he was streaming it at the time."
                n "I didn't dare look away."
                n "He cut her fingers off."
                n "Then he carved lines in her chest, showing her off to the camera."
                n "She was screaming and begging him to stop."
                n "She also called the people in the chatroom all sorts of names."
                n "He just laughed and kept mutilating her."
                show cg_ren_movies_bg6 behind cg_ren_movies2 at right with dissolve
                n "He... he had a power drill."
                n "He was lowering it into her mouth..."
                show cg_ren_movies_bg6 behind cg_ren_movies2:
                    xalign 1.0
                    easeout 0.2 xalign 0.0
                show cg_ren_movies2:
                    xalign 1.0
                    easeout 0.2 xalign 0.0
                ren "Ah!"
                n "My trance broke and my eyes shot to Ren."
                ren "Popcorn is mostly air!"
                ren "This part makes me hungry."
                n "He patted my knee as I stared, bewildered."
                ren "I'll be right back."
                show cg_ren_movies2:
                    xalign 0.0
                    alpha 1.0
                    easeout 0.1 alpha 0.0
                n "He skipped off toward the kitchen."
                $ ren_love += 10
                n "Something small and quiet at the back of my head told me I didn't have to watch any more."
                $ sanity = 10
                show cg_ren_movies_bg7 behind cg_ren_movies2:
                    xalign 0.0
                    easeout 0.5 xalign 1.0
                n "I let go of that something and turned my face back to the screen."
                n "There was blood all over her now, and the man was unzipping his pants."
                n "I watched dully."
                show cg_ren_movies6:
                    xpos -400
                    alpha 0.0
                    easeout 0.1 alpha 1.0
                n "Then I felt ren sit back down beside me."
                show cg_ren_movies_bg7 behind cg_ren_movies6:
                    xalign 1.0
                    easeout 0.3 xalign 0.0
                show cg_ren_movies6:
                    xalign 1.0
                    easeout 0.3 xalign 0.0
                n "I turned my head, no longer afraid."
                n "He clawed open a plastic wrapped package of supermarket meat."
                n "Or...meat by-products..."
                ren "Chicken hearts!"
                ren "Want one?"
                n "It felt so much better to not be afraid."
                hide cg_ren_movies6
                show cg_ren_movies7 at left
                $ ren_love += 20
                p "Yes please..."
                n "He lit up and picked one out, then held it to my lips."
                n "Can't knock it till I try it..."
                n "I accepted the small bloody organ and chewed it slowly."
                n "It was still cold from the fridge."
                ren "Well?"
                show cg_ren_movies_bg7 behind cg_ren_movies7:
                    xalign 0.0
                    easeout 0.4 xalign 1.0
                show cg_ren_movies7:
                    xalign 0.0
                    easeout 0.4 xalign 1.0
                n "I was barely aware of the grisly scene on the TV any more."
                n "I licked blood from my lips and nuzzled closer to him, feeling his tail wrap around me."
                $ ren_love += 20
                p "Maybe...it'd be better warm...?"
                ren "Oh!"
                ren "You're absolutely right!"
                n "He hugged me close."
                stop sound fadeout 1.0
                stop music fadeout 1.0
                scene black with dissolve
                n "I knew..."
                n "I knew I never wanted to leave."
                hide screen health_bar
                hide screen sanity_bar
                hide ren_collar onlayer screens
                $ persistent.ren_ending_movienight = True
                play music law_twinkle fadein 1.0
                scene endslate_clean with Dissolve(1.0)
                screen ren_ending_movienight:
                    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                    text "\n\n\n\n{=endslate_subtitle}You let Ren take care of you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                show screen ren_ending_movienight
                with Dissolve(1.0)
                pause
                $ renpy.full_restart()
    "\"I'm scared...\"":

        $ rears,rexp = 2,11
        ren "..."
        ren "You're {i}scared{/i}?"
        p "I..."
        $ rears,rexp = 2,21
        ren "I've been so generous!"
        ren "AND kind!"
        ren "I've been-"
        ren "..."
        $ rears,rexp = 1,2
        ren "I've been coddling you."
        ren "...Of course this hasn't been working."
        p "Ren..."
        $ rears,rexp = 3,19
        ren "I've been doing it wrong."
        p "Please! I'm sorry!"
        $ rears,rexp = 1,16
        ren "Oh..."
        ren "You're not sorry yet."
        $ rears,rbase,rexp = 1,5,9
        play music ren_obsessed fadein 1.0
        ren "But you will be."
        $ rears,rbase,rexp = 1,6,9
        show screen disableclick(2.0)
        $ ren_shocking = True
        play sound ren_shocked
        $ health -= 10
        $ sanity -= 10
        p "AHH!! {w=2.0}{nw}" with largeshake
        $ ren_shocking = False
        stop sound
        if health <= 0:
            jump ren_ending_health
        $ rears,rbase,rexp = 1,4,9
        stop sound fadeout 1.0
        stop music fadeout 1.0
        scene black with vpunch
        pause(2.0)
        jump ren_day3_basement
    "\"You're a monster!\"":

        $ ren_love -= 10
        $ rears,rexp = 1,16
        ren "..."
        $ rears,rexp = 3,17
        ren "You think..."
        $ rears,rexp = 2,18
        ren "...I'M a monster?"
        n "His fur was bristling."
        if ren_sawcorpse == True:
            p "I...I saw what's in the basement!"
            $ rears,rexp = 1,2
            p "I know you killed that guy!"
            $ rears,rexp = 1,11
            ren "..."
            ren "Heh..."
            $ rears,rexp = 1,20
            play music ren_obsessed fadein 1.0
            ren "HahahaHAHA!"
            $ rears,rexp = 1,4
            ren "You've been looking around the shop huh?"
            n "I recoiled, worried I made a mistake by mentioning it."
            $ rears,rexp = 1,22
            ren "Well... since you're already aquainted..."
            $ rbase = 5
            $ rears,rexp = 2,9
            ren "Why don't we pay Strade another visit?"
            p "Wha-"
            $ rbase = 6
            show screen disableclick(2.0)
            $ ren_shocking = True
            play sound ren_shocked
            $ health -= 10
            $ sanity -= 10
            p "AHH!! {w=2.0}{nw}" with largeshake
            $ ren_shocking = False
            stop sound
            $ rbase = 4
            if health <= 0:
                jump ren_ending_health
            scene black with vpunch
            stop sound fadeout 1.0
            stop music fadeout 1.0
            pause(2.0)
            jump ren_day3_basement
        else:
            $ rbase = 5
            play music ren_obsessed fadein 1.0
            ren "I'll SHOW you a monster."
            $ rbase = 6
            show screen disableclick(2.0)
            $ ren_shocking = True
            play sound ren_shocked
            $ health -= 10
            $ sanity -= 10
            p "AHH!! {w=2.0}{nw}" with largeshake
            $ rbase = 5
            $ ren_shocking = False
            stop sound
            $ rbase = 4
            if health <= 0:
                jump ren_ending_health
            scene black with vpunch
            stop sound fadeout 1.0
            stop music fadeout 1.0
            pause(2.0)
            jump ren_day3_basement

label ren_day3_basement:
if sanity <= 10:
    $ sanity += 10
scene bg_ren_basement2_dark at left with Dissolve(1.5)
show bg_ren_basement2 zorder 0:
    subpixel True
    alpha 0.0
    xalign 0.0
    ease 1.5 alpha 1.0
    pause 1.5
play sound law_day fadein 1.0 loop
p "Ughhhnn...."
$ rears,rexp = 1,22
show ren:
    subpixel True
    alpha 0.0
    xalign 0.4
    easeout 0.2 alpha 1.0 xalign 0.5
ren "Welcome back to the world of the waking, [player_name]!"
scene bg_ren_basement2:
    subpixel True
    xalign 0.0
    easeout 0.2 xalign 1.0
    pause 0.7
    easein 0.2 xalign 0.0
show ren:
    subpixel True
    xalign 0.5
    easeout 0.2 xalign -0.3
    pause 0.7
    easein 0.2 xalign 0.5
play music ren_ubi fadein 2.0
if ren_sawbasement == True:
    p "No..."
    n "The basement..."
    ren "And welcome to the shop~"
else:
    p "W-where am I!?"
    ren "You're in the shop!"
$ rears,rexp = 3,1
n "Ren breathed deep, seeming to smell the air around him."
$ rears,rexp = 1,8
ren "It's so alive down here."
n "I backed up a step and ran into a large metal pole."
$ rears,rexp = 1,22
ren "I haven't tied you up yet."
n "I glanced at the stairs."
$ rears,rexp = 1,11
ren "Because I want you to do something for me."
$ rbase = 5
n "I bit my lip, eyeing the remote in his hand."
n "Waiting for the request."
ren "I want you to strip."
p "...What!?"
$ rears,rexp = 1,16
ren "Take... your clothes off."
menu:
    "-Obey-":
        label ren_strip_obey:
        n "I looked down."
        n "It's not like I have a choice..."
        $ rears,rexp,rbase = 1,22,4
        n "I pulled of my shirt and pants quickly."
        n "I hesitated with only a short glance at Ren before touching my underwear."
        $ rears,rexp,rblush = 1,11,1
        n "I let out a defeated sigh and removed those too."
        n "I tried my best to cover myself awkwardly as he kicked the clothing further from me."
        $ rears,rexp,rblush = 1,8,0
        $ ren_love += 10
        ren "Good..."
        $ rears,rexp = 2,22
        ren "Now sit."
        n "I shivered, not entirely from the cold basement floor on my bare feet."
        $ rears,rexp = 1,22
        n "I slowly crouched and sat with my knees hugged close, my back against the pole."
        $ rears,rexp = 1,13
        ren "Stay still."
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "He moved behind me and gripped my arms."
        n "I squeaked a small protest, but he moved quickly."
        n "He yanked them behind the pole and with the sharp unmistakable noise of a zip tie, I was bound." with hpunch
        show ren:
            subpixel True
            alpha 0.0
            xalign 0.6
            easeout 0.2 alpha 1.0 xalign 0.5
        $ rears,rexp = 1,1
        ren "There!"
        $ rears,rexp = 1,22
        ren "Now we're all set up."
    "\"Can I keep my underwear on?\"":
        ren "No."
        p "..."
        n "I couldn't forget the weight of the electric collar around my neck."
        jump ren_strip_obey
    "-Refuse-":
        p "No way!"
        n "I gripped my shirt."
        $ rbase,rears,rexp = 5,1,19
        ren "Ugh."
        $ rbase,rears,rexp = 6,1,19
        show screen disableclick(2.0)
        $ ren_shocking = True
        play sound ren_shocked
        $ health -= 10
        $ sanity -= 10
        p "Hrkk!! {w=2.0}{nw}" with largeshake
        $ ren_shocking = False
        stop sound
        $ rbase,rears,rexp = 5,1,16
        n "I fell to my knees, gripping uselessly at the collar."
        call ren_subroutine from _call_ren_subroutine_14
        $ rbase = 4
        ren "Come on, [player_name]."
        ren "Now you're just wasting both of our time."
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "He moved behind me while I was still gasping in pain."
        n "He wrenched my arms backward."
        n "And with the sharp unmistakable noise of a zip tie, I was bound."
        show ren:
            subpixel True
            alpha 0.0
            xalign 0.6
            easeout 0.2 alpha 1.0 xalign 0.5
        $ rexp = 22
        label ren_strip_disobey:
        ren "I'll just do it myself."
        $ rears,rexp = 2,9
        n "I wondered how he'd manage to strip me with my arms tied for a moment."
        $ rbase = 11
        n "Then I saw the flash of a knife."
        n "I tried to squirm away from him but he moved fast."
        n "I choked back a whine of protest as he tore easily through my shirt."
        n "It must be really sharp..."
        $ rears,rexp = 2,10
        n "I tried to kick him away but it just made him move faster and more viciously."
        $ health -= 5
        n "I felt the knife hit my skin."
        p "Stop! Agh!"
        n "Every protest made him move more harshly."
        $ rears,rexp = 2,22
        n "He made some sort of... inhuman growl."
        $ rbase = 4
        n "Then pocketed the knife and tore at what was left of my clothes with his claws."
        $ rears,rexp = 2,9
        $ health -= 5
        n "I flinched and writhed as he clawed my flesh underneath on purpose."
        $ rears,rexp,rblush = 1,22,1
        n "Eventually I was left naked and shivering against the pole, covered in bloody scratches."
        call ren_subroutine from _call_ren_subroutine_15
    "-Make a break for it-":
        scene bg_ren_basement2:
            easeout 0.2 xalign 0.0 zoom 1.1
        show ren:
            xalign 0.5
            easeout 0.2 xalign 0.7
        $ rbase,rears,rexp = 5,1,7
        n "I bolted towards the stairs.{nw=0.5}"
        $ rbase,rears,rexp = 6,1,7
        show screen disableclick(2.0)
        $ ren_shocking = True
        play sound ren_shocked
        $ health -= 10
        $ sanity -= 10
        p "Hrkk!! {w=2.0}{nw}" with largeshake
        $ ren_shocking = False
        stop sound
        $ rbase,rears,rexp = 5,1,7
        n "I fell to my knees, gripping uselessly at the collar."
        call ren_subroutine from _call_ren_subroutine_16
        $ rbase = 4
        $ rears,rexp = 2,16
        ren "Come on, [player_name]."
        $ rears,rexp = 2,17
        $ health -= 5
        scene bg_ren_basement2:
            easeout 0.2 xalign 0.0 zoom 1.0
        show ren:
            xalign 0.7
            easeout 0.2 xalign 0.5
        n "He kicked me back to the pole." with hpunch
        call ren_subroutine from _call_ren_subroutine_17
        ren "Now you're just wasting both of our time."
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "He moved behind me while I was still gasping in pain."
        n "He wrenched my arms backward."
        n "And with the sharp unmistakable noise of a zip tie, I was bound."
        show ren:
            subpixel True
            alpha 0.0
            xalign 0.6
            easeout 0.2 alpha 1.0 xalign 0.5
        $ rears,rexp = 1,22
        jump ren_strip_disobey

n "I squirmed on the floor."
p "Please..."
$ rexp = 15
$ rbase = 11
ren "Oh hush."
n "He played with the knife in his hands."
$ rexp = 4
ren "This is a gift!"
n "He stepped closer."
$ rexp = 10
ren "Sometimes lessons hurt, but you'll learn to appreciate them."
n "I pulled my knees closer, curled as tightly as I could with my arms behind me."
$ rexp = 13
ren "Put your legs down."
n "I hesitated."
$ rexp,rears = 16,2
ren "Now."
n "There's nothing I can do."
$ rexp,rears = 8,1
n "I slid my feet forward, trembling."
$ rexp,rblush = 22,1
n "He crouched over my lap, his tail twitching excitedly."
n "He positioned the knife over my chest."
$ rexp = 3
n "I felt a small amount of relief seeing him move it sideways, getting ready to cut rather than stab."
$ health -= 5
$ rexp,rblush = 10,2
n "But the relief was short lived once he sunk the blade in."
n "I hissed in pain and grit my teeth."
n "I wanted to shrink away from the knife, but the pain was making my chest heave."
$ health -= 5
n "He held it firmly and each breath made it cut deeper."
n "I couldn't help but start to cry."
call ren_subroutine from _call_ren_subroutine_18
$ rexp,rblush = 8,2
$ rbase = 4
n "When he leaned back to admire his work, I slowly looked down with a whimper."
n "Is that...a..."
$ ren_love += 10
$ rexp,rblush = 1,2
ren "It's a heart! {image=icon_heart.png}"
n "I could feel hot tears mixing with the blood on my chest."
$ rexp,rblush = 22,2
ren "Do you like it?"
menu:
    "{image=icon_lowsanity.png} \"Yes...\"" if sanity <= 30:
        $ rexp = 2
        stop music fadeout 1.0
        ren "Ohhh!"
        play music ren_neutral fadein 2.0
        $ ren_love += 20
        $ rexp = 1
        ren "I knew you'd understand!!"
        $ rexp = 4
        n "He beamed at me."
        p "I do... I do understand..."
        n "My bloody chest was stinging, but it felt warm too."
        $ rexp = 2
        ren "Ah! I need..."
        $ rexp = 7
        ren "I need power tools!"
        n "My eyes widened with worry as he ran up the basement stairs."
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.4
        n "But... but I..."
        n "I looked around at all the tools in the basement."
        n "Why did he go upstairs...?"
        show ren:
            subpixel True
            alpha 0.0
            xalign 0.4
            easeout 0.2 alpha 1.0 xalign 0.5
        $ rexp = 22
        $ rbase = 15
        n "When he returned I stared in confusion for a moment."
        p "Power...tools..."
        n "Then I recognized the object in his hand with a deep blush."
        p "T-that's a-"
        $ rexp = 10
        ren "A vibrator~"
        n "He knelt back over my legs, running his hands over my thighs."
        n "I squirmed a bit out of shyness."
        $ rexp = 22
        ren "You've been so good..."
        $ rexp = 8
        ren "I want you to feel good too!"
        $ rexp = 10
        $ rbase = 4
        n "I gasped as he shoved the sex toy between my legs."
        p "I- wait, uh-"
        n "I froze in fear as he lifted a remote."
        n "I started to relax, realizing it wasn't the same remote."
        n "But once he pressed the button I tensed up again."
        p "Oh....oh god..."
        n "It felt good...I leaned into him."
        $ ren_love += 10
        $ rexp = 12
        ren "That's better~"
        n "He lowered his head and licked the blood on my chest."
        scene cg_ren_lickheart with dissolve
        n "The vibration...and his tongue..."
        n "I was panting hard and starting to moan."
        n "I started to spread my legs a little without thinking."
        n "He slid his hand between my thighs to touch me and I began to whimper."
        p "R-ren... I..."
        n "He licked me more roughly and dug his claws into my legs."
        p "REN!!"
        $ rexp = 23
        n "I couldn't hold back any more."
        n "I came and shivered under him."
        n "I finally looked back up at him."
        n "He was panting as hard as I was."
        n "Before I could say anything, he kissed me on the lips."
        n "I didn't pull away."
        $ ren_love += 10
        p "Ren...I-I love you..."
        $ rexp = 2
        ren "..."
        $ rexp = 1
        $ ren_love += 10
        ren "I..."
        $ ren_love += 10
        ren "I love you too!!"
        scene cg_ren_lickheart2 with dissolve
        n "He rubbed his head on my neck and dug his claws in again."
        $ rexp = 22
        $ ren_love += 10
        ren "And I'll never ever let you go..."
        scene black with dissolve
        hide screen health_bar
        hide screen sanity_bar
        stop sound fadeout 1.0
        stop music fadeout 1.0
        hide ren_collar onlayer screens
        $ persistent.ren_ending_sextoys = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_sextoys:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}He'll never ever let you go.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_sextoys
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "\"It hurts.\"":
        n "I shivered on the floor."
        $ rexp = 1
        $ rblush = 0
        ren "Hahaha!"
        $ rexp = 4
        ren "Well that IS the idea."
        $ rexp = 22
        ren "...You're looking a little pale."
        label ren_shortcut_crazy:
        n "I pulled my knees back up."
        ren "I haven't even gotten started yet."
        p "What!?"
        $ rexp = 19
        n "I tried to protest but he was ignoring me and frowning at the knife in his hand."
        $ rexp = 7
        ren "Hmm...need something..."
        show ren:
            subpixel True
            alpha 1.0
            xalign 0.5
            easeout 0.2 alpha 0.0 xalign 0.6
        n "He turned and rummaged through the drawers."
        ren "Oh!"
        show ren:
            subpixel True
            alpha 0.0
            xalign 0.6
            easeout 0.2 alpha 1.0 xalign 0.5
        $ rexp = 22
        $ rbase = 12
        n "He brandished some sort of electric gun."
        ren "I always wanted to try this."
        n "He waved it slightly."
        n "A nail gun."
        $ rexp = 4
        ren "I have no idea how it works!"
        n "My throat felt dry."
        n "I couldn't stop staring..."
        n "He pressed the tip to the wooden countertop and pulled the trigger-"
        $ rexp = 2
        n "{size=20}{b}BANG{/b}{/size}"
        ren "Woah!!"
        $ rexp = 4
        n "He turned back to me, grinning."
        ren "That's really scary!"
        n "I choked out a small noise."
        p "P...please..."
        $ rexp = 15
        ren "Hm?"
        p "Please stop..."
        ren "Tsk."
        ren "Why should I?"
        menu:
            "\"I'll do anything...\"":
                $ rblush = 1
                $ rexp = 2
                n "He paused at the offer."
                $ rblush = 2
                ren "...Anything?"
                n "I took another look at the nailgun, weighing my options."
                n "Anything has to be better than that."
                n "I nodded surely."
                $ rexp = 19
                ren "..."
                $ rexp = 16
                ren "Get up on your knees."
                n "He looked a bit nervous."
                n "I struggled to sit up with my arms tied back."
                $ rexp = 23
                n "When I finally managed to get up, he moved forward and pressed against me."
                n "I started to realize what he wanted as he unzipped his jeans."
                n "My eyes widened as he pressed the tip of the nailgun to my shoulder."
                ren "Don't bite me."
                ren "Okay...?"
                n "I looked at him."
                p "I won't..."
                scene cg_ren_nailgunbj with dissolve
                n "He gasped as I moved to take him into my mouth."
                n "Was he not expecting me to!?"
                ren "Ahhh-hh..."
                n "I began to think to myself that this isn't so difficult."
                n "He's an average size and it's-"
                p "Hrk!"
                n "I suddenly felt claws on the back of my head, pushing me onto him."
                n "I tried to recover from my choke and looked up."
                n "He's getting really excited..."
                n "I remembered the nailgun and tried to relax."
                n "I began to move my tongue against him."
                n "He moaned and I could feel him shudder."
                n "I winced as he dug his claws in again."
                n "Hearing him... I began to start breathing harder myself."
                ren "I-I..."
                n "His movements were becoming harsher and more random."
                n "I was panting through my nose and starting to drool."
                $ rexp = 2
                ren "AH-"
                scene bg_ren_basement2 zorder 0 at left
                show ren
                if health >= 10:
                    $ health -= 5
                n "{size=20}{b}BANG{/b}{/size}" with vpunch
                n "He jumped backward and yelped in surprise."
                n "I just stared with my mouth open and dripping in shock."
                n "Then the pain blossomed from my shoulder."
                if sanity <= 20:
                    $ sanity -= 10
                n "I lurched forward and let out a rasping pained moan."
                n "My arms strained against my bonds and the agony just got worse."
                $ rexp = 24
                $ rears = 3
                $ rbase = 4
                ren "I-I'm sorry!"
                n "To my surprise, he knelt down to hold me still and stop me from straining more."
                ren "I didn't mean to pull the trigger!"
                ren "I...I forgot I had it...there..."
                n "I began to calm down and sniffed."
                $ rears = 1
                p "I'm...okay..."
                n "He rubbed his forhead on mine quickly before gripping the tip of the nail."
                p "Wait!"
                n "He pulled it out quickly as I gasped in pain."
                $ rexp = 12
                n "He immediately tossed the nail to the side and bent to lick my shoulder."
                n "I felt my cheeks redden."
                ren "We'll clean this up and bandage you okay?"
                n "He moved to grab his knife and cut the ties around my wrist."
                $ rexp = 8
                ren "And have a nice warm bath."
                n "For some reason, I felt tears well up in my eyes again."
                n "But..."
                n "I was smiling."
                p "That sounds really nice."
                n "He kissed my nose and helped me to my feet."
                ren "Don't worry [player_name]. I'll take really good care of you!"
                stop sound fadeout 1.0
                stop music fadeout 1.0
                scene black with dissolve
                hide screen health_bar
                hide screen sanity_bar
                hide ren_collar onlayer screens
                $ persistent.ren_ending_bjbang = True
                play music law_reverse fadein 1.0
                scene endslate_clean with Dissolve(1.0)
                screen ren_ending_bjbang:
                    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                    text "\n\n\n\n{=endslate_subtitle}Ren will take really good care of you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                show screen ren_ending_bjbang
                with Dissolve(1.0)
                pause
                $ renpy.full_restart()
            "\"You're being crazy!\"":

                ren "..."
                $ rexp = 13
                ren "Do you understand the position you're in right now?"
                n "I clenched my jaw and started to sweat."
                $ rexp = 16
                $ rears = 3
                $ rbase = 4
                ren "And you're insulting me...?"
                n "I pulled my knees closer."
                $ rexp = 17
                $ rears = 2
                ren "Spread your legs."
                n "I looked up at him, shocked."
                $ rbase = 5
                ren "I won't repeat myself."
                menu:
                    "-Obey-":
                        n "If I don't...he'll just shock me."
                        n "Or worse..."
                        n "I bit my lip and shakily let my knees fall to the side."
                        $ rexp = 16
                        $ rears = 3
                        n "The worry of what he was going to do kept my mind fairly far from any embarrassment."
                    "-Refuse-":

                        n "I kept my knees pressed together."
                        n "I'm not going to-"
                        $ rbase,rears,rexp = 6,2,18
                        show screen disableclick(2.0)
                        $ ren_shocking = True
                        play sound ren_shocked
                        $ health -= 20
                        p "!!!! {w=2.0}{nw}" with largeshake
                        $ ren_shocking = False
                        stop sound
                        $ rbase,rears,rexp = 5,2,17
                        n "I coughed and wheezed in pain."
                        call ren_subroutine from _call_ren_subroutine_19
                        n "My legs collapsed uselessly to the sides."

                $ rexp = 16
                $ rears = 1
                $ rbase = 4
                n "He crouched between my thighs."
                p "R-ren..."
                $ rexp = 22
                n "I squeaked as he reached for the sensitive flesh between my legs."
                show black zorder 5
                n "I squeezed my eyes shut as he touched me."
                n "Even through the fear, I could feel my face getting hot."
                ren "..."
                n "He pulled at me and seemed to just...stop."
                hide black
                $ rbase = 12
                n "I opened my eyes again."
                n "I didn't have time to scream."
                $ sanity -= 5
                if health >= 10:
                    $ health -= 5
                n "{size=20}{b}BANG{/b}{/size}" with vpunch
                $ rexp = 22
                $ rbase = 4
                n "He leaned back triumphantly as I began to shake and sob."
                n "I pressed my knees back together but it did nothing for the pain."
                call ren_subroutine from _call_ren_subroutine_20
                p "My...m-my..."
                $ rexp = 16
                ren "Apologize."
                n "I looked up, my eyes red with tears."
                n "It was hard to even remember what to apologize for through the pain."
                p "I...I'm sorry!"
                p "You're not crazy!"
                $ rexp = 19
                n "I sobbed harder."
                p "I'm sorry!!!!"
                $ rexp = 16
                ren "That's better."
                $ rexp = 15
                ren "...You know I'm doing this because I love you..."
                n "His tail twitched."
                $ rears = 3
                $ rexp = 22
                ren "And you love me too, right?"
                menu:
                    "\"Yes.\"":
                        n "Ren stared hard at me."
                        n "I kept my eyes on his, even as tears streamed down my face."
                        $ rears = 1
                        $ rexp = 8
                        n "Suddenly, he relaxed."
                        $ rbase = 4
                        ren "I guess I'll give you a break."
                        $ rexp = 22
                        scene cg_ren_stepping with dissolve
                        n "He stood up and pressed his foot between my legs."
                        n "I cried out at the pressure on my damaged flesh."
                        ren "Even if you're lying..."
                        n "He moved his toes, eliciting more agonized whimpers from me."
                        ren "We have all the time in the world to make it true..."
                        n "I cried and shivered."
                        scene black with dissolve
                        stop sound fadeout 1.0
                        stop music fadeout 1.0
                        n "I'm never going to leave this house."
                        hide screen health_bar
                        hide screen sanity_bar
                        hide ren_collar onlayer screens
                        $ persistent.ren_ending_genitals = True
                        play music law_reverse fadein 1.0
                        scene endslate_clean with Dissolve(1.0)
                        screen ren_ending_genitals:
                            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                            text "\n\n\n\n{=endslate_subtitle}And you got a new piercing.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                        show screen ren_ending_genitals
                        with Dissolve(1.0)
                        pause
                        $ renpy.full_restart()
                    "\"No.\"":
                        $ rexp = 21
                        $ rears = 2
                        ren "..."
                        $ rexp = 19
                        $ rbase = 12
                        n "He looked at the nailgun in his hands."
                        n "His silence was making me rethink my reply."
                        n "Before I could say anything else, he turned and walked away."
                        $ rbase = 4
                        show ren:
                            subpixel True
                            alpha 1.0
                            xalign 0.5
                            easeout 0.2 alpha 0.0 xalign 0.4
                        n "He left the nailgun on the counter and climbed the stairs quitely."
                        n "I wimpered and pulled at the ties on my wrists."
                        n "Why did I say no...?"
                        n "My increasing regret was eventually interrupted by the soft creaking of the wood stairs."
                        show ren:
                            subpixel True
                            alpha 0.0
                            xalign 0.4
                            easeout 0.2 alpha 1.0 xalign 0.5
                        $ rexp = 13
                        n "I didn't have to look him over long to see what he'd left for."
                        $ rbase = 13
                        n "...A gun."
                        n "A real gun."
                        $ rexp = 19
                        ren "It's funny..."
                        n "He raised the weapon."
                        ren "Strade had so many tools."
                        ren "And more knives than I've ever bothered to count."
                        $ rexp = 16
                        ren "But he only had one gun."
                        n "I couldn't move."
                        n "I wasn't even sure I was breathing."
                        $ rexp = 12
                        ren "He must not have liked guns."
                        n "I'm going to die..."
                        $ rexp = 22
                        ren "But I kind of like it."
                        n "I'm going to die in this house..."
                        ren "..."
                        $ rexp = 16
                        ren "Tell me you love me."
                        menu:
                            "-Refuse-":
                                n "I looked down to my bloody lap."
                                n "Why drag this out..."
                                n "If I live through this he'll just torment me forever."
                                n "I looked up."
                                p "No."
                                pause(1.5)
                                label ren_shortcut_shot:
                                $ rears = 2
                                $ rbase = 13
                                $ rexp = 19
                                ren "W-what a mistake..."
                                ren "No one will ever love me like he did..."
                                $ health-=100
                                stop sound fadeout 1.0
                                stop music fadeout 1.0
                                scene white with vpunch
                                scene black with dissolve
                                hide screen health_bar
                                hide screen sanity_bar
                                hide ren_collar onlayer screens
                                $ persistent.ren_ending_shot = True
                                play music law_twinkle fadein 1.0
                                scene endslate with Dissolve(1.0)
                                screen ren_ending_shot:
                                    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                                    text "\n\n\n\n{=endslate_subtitle}Ren shot you in the head.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                                show screen ren_ending_shot
                                with Dissolve(1.0)
                                pause
                                $ renpy.full_restart()
                            "-Do it-":

                                $ rears = 3
                                n "I responded immediately."
                                p "I love you!"
                                p "I love you! I love you!"
                                n "My voice was cracking."
                                $ rexp = 19
                                ren "Hmm."
                                ren "Of course you'd say that..."
                                $ rexp = 7
                                ren "You'd say anything right now, wouldn't you?"
                                $ rexp = 13
                                ren "You probably don't mean it."
                                $ rbase = 14
                                $ rears, rexp = 2,16
                                n "He lowered the gun."
                                p "Ren, I-"
                                $ health -= 20
                                $ sanity -= 10
                                show white zorder 5
                                n "{size=30}{b}BANG{/b}{/size}{w=0.5}{nw}" with vpunch
                                show white:
                                    alpha 1.0
                                    easeout 0.5 alpha 0.0
                                n "The sound rang loud off the walls."
                                n "Then the pain came."
                                n "I looked down at the hole in my leg."
                                p "I...I..."
                                call ren_subroutine from _call_ren_subroutine_21
                                $ rexp = 16
                                label ren_profess:
                                $ time = 1.0
                                $ timer_range = 1.0
                                $ timer_jump = 'ren_profess_fail'
                                show screen countdown
                                menu:
                                    "-Profess your love!-":
                                        hide screen countdown
                                        jump ren_profess_pass

                                label ren_profess_pass:
                                $ rexp = 13
                                $ sanity = 0
                                stop music fadeout 1.0
                                p "I LOVE YOU!"
                                $ rears = 1
                                p "I may have only met you but I've never felt more alive!"
                                p "I'm so scared and it hurts but I know..."
                                n "I was shaking."
                                $ rexp = 2
                                p "I know I'm supposed to be here..."
                                $ rblush = 1
                                p "I want to be with you."
                                $ rexp = 15
                                $ rblush = 2
                                p "I need you..."
                                n "I leaned forward, tears streaming down my face."
                                $ rexp = 12
                                $ rbase = 4
                                p "I'm yours, Ren..."
                                p "I'm all yours..."
                                n "I broke down and sobbed into my lap."
                                n "I didn't flinch when I felt his hand on my head."
                                scene cg_ren_gun with dissolve
                                $ ren_love += 30
                                ren "That's a really good start."
                                stop sound fadeout 1.0
                                hide screen health_bar
                                hide screen sanity_bar
                                hide ren_collar onlayer screens
                                $ persistent.ren_ending_allhis = True
                                play music law_reverse fadein 1.0
                                scene endslate_clean with Dissolve(1.0)
                                screen ren_ending_allhis:
                                    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                                    text "\n\n\n\n{=endslate_subtitle}You're all his.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                                show screen ren_ending_allhis
                                with Dissolve(1.0)
                                pause
                                $ renpy.full_restart()

                                label ren_profess_fail:
                                jump ren_shortcut_shot
            "-Say nothing-":

                n "I couldn't think of anything I could do."
                ren "See?"
                $ rexp = 16
                ren "There's nothing you can do about it."
                $ rexp = 22
                n "He pushed my knee back down with his foot and positioned the gun over my calf."
                p "No! no no!"
                $ rexp = 10
                n "I writhed uselessly as he pulled the trigger."
                $ health -= 5
                $ sanity -= 5
                n "{size=20}{b}BANG{/b}{/size}" with vpunch
                n "I screamed and slumped forward."
                call ren_subroutine from _call_ren_subroutine_22
                $ rexp = 22
                ren "Heh..."
                $ rexp = 4
                ren "That really works huh?"
                n "I looked up through my tears as he moved the tip of the gun up my leg a bit."
                n "I started a sob-"
                $ rblush = 1
                $ rexp = 9
                $ health -= 5
                $ sanity -= 5
                n "{size=20}{b}BANG{/b}{/size}" with vpunch
                n "I jerked hard against my binding."
                n "I could feel the ties cutting into my wrists."
                n "He ignored my sobbing and screaming."
                call ren_subroutine from _call_ren_subroutine_23
                $ rexp = 10
                $ rblush = 2
                n "He just slid the tool slowly up my leg."
                window show
                $ health -= 5
                $ sanity -= 5
                n "{size=20}{b}BANG{/b}{/size}{w=0.5}{nw}" with vpunch
                $ rexp = 1
                $ health -= 5
                $ sanity -= 5
                n "{size=20}{b}BANG{/b}{/size} {size=20}{b}BANG{/b}{/size}{w=0.5}{nw}" with vpunch
                $ health -= 5
                $ sanity -= 5
                n "{size=20}{b}BANG{/b}{/size} {size=20}{b}BANG{/b}{/size} {size=20}{b}BANG{/b}{/size}{w=0.5}{nw}" with vpunch
                ren "Hahahaha!"
                window auto
                call ren_subroutine from _call_ren_subroutine_24
                n "I was shaking."
                n "I couldn't think."
                n "I... wasn't even screaming any more."
                $ rexp = 22
                ren "Come on [player_name]!"
                $ rexp = 15
                ren "You can't be worn out already!"
                n "My wrists... my leg..."
                n "Everything hurts."
                n "I feel dizzy..."
                ren "Hah..."
                show black zorder 10:
                    alpha 0.0
                    ease 15.0 alpha 0.8
                $ renpy.music.set_volume(0.1, 15.0, channel="music")
                n "My head fell forward."
                $ rexp = 12
                ren "I always though it was ridiculous, how he'd get excited that quickly..."
                n "He let out a strange laugh."
                $ rexp = 22
                ren "I guess it's pretty easy to get carried away!"
                n "His voice was sounding further away."
                n "It sounded like hissing static instead."
                $ rexp = 8
                $ rbase = 4
                ren "Hey!"
                n "Clawed fingers snapped in front of my face."
                hide black
                $ renpy.music.set_volume(1, 0, channel="music")
                n "I snapped back to the present as I felt a nail pulled from my leg." with vpunch
                $ rexp = 22
                $ ren_love += 10
                ren "You're bleeding and crying everywhere~"
                n "He pulled another."
                $ rexp = 15
                $ ren_love += 10
                ren "We'll get you all cleaned up hm?"
                n "I felt sick."
                $ ren_love += 10
                ren "Don't worry."
                $ ren_love += 10
                ren "I've got much better self control."
                scene black with dissolve
                stop sound fadeout 1.0
                stop music fadeout 1.0
                n "My head fell forward again."
                n "Eventually I felt him drag me somewhere with running water."
                $ ren_love += 10
                ren "You're not going anywhere~ {image=icon_heart.png}"
                scene black with dissolve
                hide screen health_bar
                hide screen sanity_bar
                hide ren_collar onlayer screens
                $ persistent.ren_ending_nailgun = True
                play music law_reverse fadein 1.0
                scene endslate_clean with Dissolve(1.0)
                screen ren_ending_nailgun:
                    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                    text "\n\n\n\n{=endslate_subtitle}You'll get to enjoy his self control forever.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                show screen ren_ending_nailgun
                with Dissolve(1.0)
                pause
                $ renpy.full_restart()
    "\"No! You're crazy!\"":

        $ rblush = 0
        ren "..."
        $ ren_love -= 10
        ren "...You really think so?"
        jump ren_shortcut_crazy

label ren_day3_dominant:
$ ren_shocking_reverse = False
scene bg_ren_livingroom at right with dissolve
$ rtail = 5
show ren:
    subpixel True
    alpha 0.0
    xalign 0.6
    easeout 0.2 alpha 1.0 xalign 0.5
$ rears,rbase,rexp = 3,7,3
play music ren_warppiano fadein 2.0
ren "Hey [player_name]."
$ rears,rexp = 3,24
ren "You fell asleep..."
n "I looked up blearily at Ren."
ren "And..."
ren "And I've been thinking..."
ren "..."
$ rexp = 27
ren "You've been getting a little out of hand."
p "What!?"
n "I sat up straight."
n "This little bastard thinks he's going to shock me again!?"
ren "L-look, it's for your own good..."
n "I saw him reach for the remote in his pocket."
n "No!"
$ rears,rexp = 1,5
n "Without thinking, I lept at him." with vpunch
n "He barely managed to dodge me, ducking low."
n "We were both thrown off balance."
$ rears,rexp = 2,17
n "He growled quietly and looked at the floor."
ren "You..."
n "He reached for-"
play music ren_obsessed fadein 1.0
$ rears,rexp = 2,18
label ren_sub_attack:
$ time = 1.0
$ timer_range = 1.0
$ timer_jump = 'ren_sub_attack_fail'
show screen countdown
menu:
    "-The chain!-":
        hide screen countdown
        jump ren_sub_attack_pass

label ren_sub_attack_fail:
n "I tried to grab the chain on the floor, but I stumbled."
n "I kicked at him, trying to wrestle him away." with vpunch
n "He was too fast for me to stop him."
n "He grasped the chain and slung it around my neck."
scene cg_ren_chains3 with dissolve
$ health -= 10
$ sanity -= 10
n "I stumbled and fell back to the floor." with vpunch
n "I tried to kick him off but he had better leverage."
$ health -= 10
$ sanity -= 10
n "He kept moving and pressing the chain tighter."
n "I rasped out a last angry grunt as I tried to strike him."
n "He dodged me easily."
$ health -= 10
$ sanity -= 10
n "My arms were getting heavier."
n "I couldn't...couldn't suck in a breath..."
ren "I don't need you..."
$ health -= 10
$ sanity -= 10
n "He heaved all of his weight down on the chain."
ren "I don't need anyone!!"
$ health -= 10
$ sanity -= 10
n "Soon, even my eyelids were too heavy."
$ health -= 100
$ sanity -= 100
scene black with dissolve
stop sound fadeout 1.0
stop music fadeout 1.0
n "I felt my head fall to the side."
n "He never stopped squeezing."
hide screen health_bar
hide screen sanity_bar
hide ren_collar onlayer screens
$ persistent.ren_ending_chain = True
play music law_twinkle fadein 1.0
scene endslate with Dissolve(1.0)
screen ren_ending_chain:
    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
    text "\n\n\n\n{=endslate_subtitle}He didn't need you.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
show screen ren_ending_chain
with Dissolve(1.0)
pause
$ renpy.full_restart()

label ren_sub_attack_pass:
n "I saw him eyeing the chain at our feet and lunged for it myself."
scene cg_ren_chains1 with dissolve
n "I grabbed the chain and slammed it into his neck, pinning him down to the ground." with vpunch
p "Hah!"
n "He squirmed under me, trying to claw at me while I pressed the chain down harder."
n "He couldn't claw hard enough to make me stop."
n "I knew I couldn't let up."
n "I kept pressing as he got weaker."
scene cg_ren_chains2 with dissolve
stop music fadeout 1.0
n "After one last desperate attempt to claw me, he slumped down."
play music ren_warppiano fadein 2.0
n "I watched for a moment as his ear twitched."
n "He's out cold... but he's alive."
menu:
    "-Kill him-":
        n "I'm not taking any chances."
        n "And he brought this on himself."
        n "I pressed the chain back down."
        n "How long can someone live without oxygen?"
        n "Three minutes?"
        n "I kept my weight on the chain."
        n "I stayed there...maybe for ten minutes or more."
        n "He couldn't fight me."
        n "I finally, slowly moved the chain."
        n "I pressed a finger to his neck to be sure."
        n "..."
        n "I killed him."
        n "I stood up shakily."
        n "It's over."
        n "He looked even smaller on the floor like that."
        n "I shook my head."
        n "This was his fault."
        n "It didn't take me long to find his remote and key."
        hide ren_collar onlayer screens with dissolve
        n "I freed myself, tossed the collar on him, and walked out the door."
        scene white with dissolve
        stop sound fadeout 1.0
        stop music fadeout 1.0
        n "I rubbed my neck and stared out into the sunshine darkly."
        n "But I didn't look back."
        hide screen health_bar
        hide screen sanity_bar
        $ persistent.ren_ending_chainkill = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_chainkill:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You choked Ren to death.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_chainkill
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Take his remote-":

        n "All right... first thing's first."
        n "I leaned over his softly breathing body."
        p "I am taking THIS."
        n "I pulled the small remote from his pocket."
        n "I looked it over."
        n "Hm. Not complicated...but not labelled either."
        n "I sure as hell knew what the big red button did."
        n "Slider probably has something to do with strength..."
        n "I fiddled with the two remaining buttons, too fed up to be cautious."
        n "I heard a soft click."
        n "I reached up-"
        hide ren_collar onlayer screens with dissolve
        show ren_remote onlayer screens with dissolve
        n "It's open!!"
        n "I grinned down at the open collar."
        n "Then I focused on Ren."
        p "Hmm."
        menu:
            "-Spare him and leave-":
                n "I looked down at him."
                p "Tsk."
                p "Shitty little weasel..."
                n "I knew I could finish him off easily."
                n "But..."
                n "Whatever."
                n "I tossed the open collar on the floor."
                n "I don't need to kill him."
                n "I took a step and remembered the chain still on my ankle."
                p "Ugh."
                n "I rummaged through Ren's other pockets until I found the small key."
                n "I hastily unlocked the shackle and kicked the damn chain off."
                n "I turned and approached the front door."
                n "I paused for a second."
                n "Then I opened the door and walked through."
                scene white with dissolve
                stop sound fadeout 1.0
                stop music fadeout 1.0
                n "It's over."
                n "I breathed in the sun and never looked back."
                hide screen health_bar
                hide screen sanity_bar
                hide ren_remote onlayer screens
                $ persistent.ren_ending_escapelive = True
                play music law_twinkle fadein 1.0
                scene endslate_clean with Dissolve(1.0)
                screen ren_ending_escapelive:
                    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                    text "\n\n\n\n{=endslate_subtitle}You escaped and spared Ren.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                show screen ren_ending_escapelive
                with Dissolve(1.0)
                pause
                $ renpy.full_restart()
            "-Put it on him-":

                if ren_love <= 0:
                    $ ren_love = 0
                n "I leaned down and clicked the collar closed around his neck."
                n "I couldn't help but smile at the feeling of victory it gave me."
                n "I sat back on the couch and relaxed."
                scene black with dissolve
                n "I played with the remote and put my feet up on the coffee table."
                n "I can't wait to see his face when-"
                ren "Ugghnn..."
                scene bg_ren_livingroom at right
                n "Oh?"
                $ rbase,rexp,rears = 8,24,3
                n "Ren stood slowly, clutching his head."
                show ren:
                    subpixel True
                    xalign 0.5
                    alpha 0.0
                    easeout 0.2 alpha 1.0
                $ rexp = 25
                ren "A-ah..."
                $ rexp = 26
                n "He finally looked my way."
                $ rexp = 27
                n "He seemed to be remembering..."
                n "I flashed him a triumphant grin as he noticed the collar on my neck was absent."
                ren "..."
                $ rexp,rears = 5,4
                n "He touched the collar on himself."
                ren "Oh no..."
                p "Oh yes."
                n "He cowered, seeing the remote in my hand."
                p "Now unchain me."
                $ rexp = 6
                ren "I...o-okay..."
                n "He shuffled awkwardly and retrieved a small key."
                n "He then bent down to unlock the shackle around my ankle."
                n "It fell to the floor with a soft thump."
                menu:
                    "-Thank him-":
                        $ rexp,rears = 2,4
                        p "Thank you, Ren. I appreciate it."
                        n "He seemed surprised."
                        $ rexp,rears = 24,3
                        $ ren_love += 10
                        n "But he appeared to relax a tiny bit."
                        ren "You're...welcome."
                    "-Say nothing-":

                        p "..."
                        n "Ren backed away slightly, looking nervous."
                    "-Test out remote-":

                        n "I played with the remote in my hand."
                        $ rexp = 5
                        n "Ren saw it too, and took a step back."
                        n "Let's see how this works."
                        $ rbase,rears,rexp,rtail,rbangs = 10,0,0,4,0
                        show screen disableclick(2.0)
                        $ ren_shocking_reverse = True
                        play sound ren_shocker
                        show ren at spriteshake
                        ren "AHHHHH!! {w=2.0}{nw}"
                        show ren at default
                        $ ren_shocking_reverse = False
                        stop sound
                        $ rbase,rears,rexp,rtail,rbangs = 8,4,28,5,1
                        n "He wimpered and shrank back from me."
                        p "How does that feel?"
                        ren "..."
                        ren "It hurts..."
                        p "Heh."
                        $ rexp,rblush = 27,4
                        n "He sniffed and wiped his face."
                ren "..."
                $ rexp,rblush = 24,3
                ren "I'm...I'm sorry..."
                n "His voice was sounding desperate."
                $ rexp = 27
                ren "I shouldn't have pushed you like that!"
                $ rexp = 6
                ren "I...I..."
                menu:
                    "-Reassure him-":
                        $ rexp = 27
                        p "Hey, hey..."
                        p "It's okay."
                        $ rears = 3
                        n "He looked at me cautiously."
                        p "I accept your apology."
                        $ rears,rexp = 1,24
                        $ ren_love += 10
                        ren "..."
                        n "He started to look hopeful."
                    "-Threaten him-":
                        $ rears = 4
                        $ rexp = 27
                        p "Oh, you're 'sorry' now?"
                        n "I leaned back."
                        p "Now that the collar's on {i}your{/i} neck."
                        $ rexp = 6
                        p "You're not sorry."
                        $ rexp = 5
                        p "Yet."
                        n "I watched him begin to tremble."
                ren "What are you gonna do to me?"
                $ rexp = 27
                ren "W-what do you want...?"
                menu:
                    "\"Love.\"" if ren_love >= 20:
                        play music ren_piano fadein 1.0
                        $ ren_love += 10
                        $ rexp,rblush = 2,4
                        ren "Wh-what!?"
                        p "I want the same thing you want."
                        n "I lowered the remote."
                        p "I just want someone...to be with."
                        n "I had trouble thinking of the right words."
                        $ ren_love += 10
                        $ rexp = 12
                        ren "You want to be with me...?"
                        p "Yes!"
                        p "You don't need to shock me or chain me, Ren."
                        p "I {i}like{/i} you."
                        p "And I want to get to know you better."
                        $ ren_love += 10
                        ren "..."
                        scene cg_ren_happy with dissolve
                        n "He jumped at me and I yelped in surprise."
                        $ ren_love += 100
                        ren "Thank you!!"
                        ren "I- I won't let you down!!"
                        scene black with dissolve
                        stop sound fadeout 1.0
                        stop music fadeout 1.0
                        n "I stayed with him that night..."
                        n "I didn't see any reason to leave."
                        hide screen health_bar
                        hide screen sanity_bar
                        hide ren_remote onlayer screens
                        $ persistent.ren_ending_sublove = True
                        play music law_twinkle fadein 1.0
                        scene endslate_clean with Dissolve(1.0)
                        screen ren_ending_sublove:
                            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                            text "\n\n\n\n{=endslate_subtitle}You stayed with Ren.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                        show screen ren_ending_sublove
                        with Dissolve(1.0)
                        pause
                        $ renpy.full_restart()
                    "\"Obedience.\"":

                        $ rexp,rears = 26,3
                        $ rblush = 0
                        ren "...O-oh."
                        p "Hey, you're the one that brought me here."
                        p "And you can KEEP me here."
                        $ rexp =  6
                        p "But you're going to have to do what I say."
                        p "Not the other way around."
                        n "I waved the remote lazily to illustrate my point."
                        p "Got it?"
                        $ rexp,rears = 27,3
                        ren "Ah...Y-yes, [player_name]."
                        p "Good."
                        n "I leaned back and relaxed."
                        p "...And I'm getting hungry."
                        $ rexp,rears = 2,1
                        ren "Uh!"
                        ren "I-I'll cook something!"
                        show ren:
                            subpixel True
                            xalign 0.5
                            alpha 1.0
                            easeout 0.2 alpha 0.0 xalign 0.6
                        n "He ran to the kitchen and I sighed in contentment."
                        n "This is MUCH better."
                        scene black with dissolve
                        hide screen health_bar
                        hide screen sanity_bar
                        stop sound fadeout 1.0
                        stop music fadeout 1.0
                        hide ren_remote onlayer screens
                        $ persistent.ren_ending_subobey = True
                        play music law_reverse fadein 1.0
                        scene endslate_clean with Dissolve(1.0)
                        screen ren_ending_subobey:
                            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                            text "\n\n\n\n{=endslate_subtitle}You kept Ren.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                        show screen ren_ending_subobey
                        with Dissolve(1.0)
                        pause
                        $ renpy.full_restart()
                    "\"Sex.\"":

                        $ ren_love += 10
                        $ rexp = 2
                        $ rblush = 4
                        play music ren_vampire fadein 1.0
                        ren "Wh-what!?"
                        n "I held up the remote."
                        p "You heard me."
                        ren "Y-you want...me..."
                        $ ren_love += 10
                        p "On your knees."
                        $ rexp = 29
                        n "I moved my legs apart to give him room."
                        scene cg_ren_oral1 with dissolve
                        n "He nestled between my thighs and looked...eager..."
                        n "I laid the remote to the side and reached for his head."
                        n "He leaned up into my hand as he undid my pants."
                        n "I felt his soft ear and could see he was blushing redder."
                        p "You like that?"
                        $ rexp = 23
                        ren "Ah...y-yes..."
                        $ ren_love += 10
                        ren "{size=10}Those are sensitive...{/size}"
                        n "I rubbed his ear harder and was immediately rewarded with a soft moan."
                        n "I looked down at his panting face."
                        scene cg_ren_oral2 with dissolve
                        n "He bit his lip shyly before leaning in and running his tongue over me."
                        n "I moaned and gripped his hair."
                        n "He moved his tongue confidently..."
                        n "Soon I was panting over him."
                        n "His timidness seemed to melt away."
                        n "My grip got tighter and rougher, but he only responded with muffled hungry moans."
                        p "D-damn...Ren...Ah..."
                        n "I couldn't hold back."
                        n "I gripped his head and came with a cry."
                        n "After a few moments, I realized I was still holding him tight."
                        scene cg_ren_oral3 with dissolve
                        n "I released his hair and looked down, breathing hard."
                        n "He licked his lips."
                        $ ren_love += 10
                        ren "Did...I do well..?"
                        p "Rrr!"
                        n "I gripped him under the arms and pulled him up in my lap."
                        n "I squeezed him and he let out a small nervous laugh."
                        p "You're a little too good...haha..."
                        n "He nuzzled me and smiled."
                        p "And you're all mine."
                        n "I squeezed tighter and thought I felt him shiver."
                        scene black with dissolve
                        hide screen health_bar
                        hide screen sanity_bar
                        stop sound fadeout 1.0
                        stop music fadeout 1.0
                        hide ren_remote onlayer screens
                        $ persistent.ren_ending_subsex = True
                        scene endslate_clean with Dissolve(1.0)
                        play music law_reverse fadein 1.0
                        screen ren_ending_subsex:
                            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                            text "\n\n\n\n{=endslate_subtitle}You took Ren for yourself.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                        show screen ren_ending_subsex
                        with Dissolve(1.0)
                        pause
                        $ renpy.full_restart()

                    "\"Blood.\"" if ren_sawbasement == True:
                        $ rexp,rears = 2,4
                        $ rblush = 0
                        stop music fadeout 1.0
                        ren "B...blood!?"
                        $ rexp = 27
                        ren "What do you mean...?"
                        n "I looked to the side."
                        $ rexp = 5
                        play music ren_ubi fadein 1.0
                        p "I think we should go to the basement."
                        n "I looked back to him to see he'd gone completely still."
                        ren "I...how...how do you..."
                        p "You think I didn't see down there?"
                        if ren_sawcorpse == True:
                            p "I narrowed my eyes at him."
                            p "I saw your dirty little secret down there too."
                        n "He looked terrified."
                        n "I couldn't help but feel a bit of elation, watching him squirm."
                        n "I raised the remote."
                        p "Now."
                        $ rexp = 24
                        ren "I'm..."
                        $ rexp = 16
                        ren "I'm not going back down there!!"
                        p "Tsk."
                        $ rbase,rears,rexp,rtail,rbangs = 10,0,0,4,0
                        show screen disableclick(2.0)
                        $ ren_shocking_reverse = True
                        play sound ren_shocker
                        show ren at spriteshake
                        ren "AAAgggnnn!! {w=2.0}{nw}"
                        show ren at default
                        $ ren_shocking_reverse = False
                        stop sound
                        $ rbase,rears,rexp,rtail,rbangs = 8,4,28,5,1
                        n "He was panting and trembling."
                        p "Don't make me do it twice, Ren."
                        n "He whimpered and turned to walk toward the stairs."
                        show ren:
                            subpixel True
                            xalign 0.5
                            alpha 1.0
                            easeout 0.2 alpha 0.0 xalign 0.6
                        n "I got up to follow and watched him walk silently, slouching in front of me."
                        scene bg_ren_basementstairs with dissolve
                        n "He paused on the stairs and I nudged him forward."
                        scene bg_ren_basement with dissolve
                        show ren:
                            subpixel True
                            xalign 0.6
                            alpha 0.0
                            easeout 0.2 alpha 1.0 xalign 0.5
                        ren "P-please..."
                        p "Sit."
                        n "He kept whimpering softly and obeyed."
                        n "I looked around the basement for something to tie him."
                        n "I easily found some rope and tied his limbs behind the pole in the middle of the basement."
                        n "Judging by the stains, he was not the first person who sat here."
                        scene cg_ren_pole with dissolve
                        hide ren
                        n "I looked down at him."
                        n "He's still crying."
                        menu:
                            "-Soothe him-":
                                n "I reached down to pet his hair and ears."
                                n "He was shaking..."
                                p "Shhhh..."
                                p "It's okay..."
                                $ ren_love += 10
                                n "I stood and stroked his hair patiently."
                                scene cg_ren_pole2
                                n "Eventually his sobbing turned to sniffling."
                                n "I could tell he wasn't really convinced..."
                                n "But he became quieter."
                            "-Encourage crying-":

                                n "I grinned at him."
                                $ ren_love += 10
                                p "You can cry all you want Ren~"
                                scene cg_ren_pole3
                                n "I leaned down to him and stroked his head."
                                n "I like it."
                            "-Discourage crying-":

                                p "Ren."
                                n "He kept sobbing."
                                p "Stop crying."
                                n "I held the remote up for him to see."
                                n "He squirmed and cried harder."
                                p "All right."
                                show screen disableclick(2.0)
                                $ ren_shocking_reverse = True
                                play sound ren_shocker
                                scene cg_ren_pole4
                                ren "AAAA!! {w=2.0}{nw}" with smallshake
                                $ ren_shocking_reverse = False
                                stop sound
                                scene cg_ren_pole5
                                n "He slumped down, no longer making any noise."
                                p "Better."
                        n "I stood up straight."
                        p "Now that you're settled..."
                        p "Hmm."
                        n "I looked around the musty basement."
                        n "So many tools..."
                        n "Everything looked like it would hurt."
                        p "There's too much to pick from down here!"
                        n "I looked over the walls and through cupboards."
                        n "Saws, hammers, axes, knives..."
                        n "I chuckled softly as I spotted a pair of well worn black leather gloves."
                        p "I like these..."
                        n "I rummaged through drawers and eventually narrowed it down to two."
                        menu:
                            "-Something brutal-":
                                n "My eyes settled on a nail gun."
                                p "Oooh~"
                                n "Big, loud, and high power."
                                n "This is the way to go!"
                                scene cg_ren_pole7
                                n "I turned back to Ren and smiled, brandishing the gun."
                                p "How about this?"
                                n "His eyes widened at the tool and he squirmed against the pole."
                                n "I could hear his nails scratching on the floor like an animal."
                                n "Maybe I should take care of that first..."
                                jump ren_day3sub_nailgun
                            "-Something personal-":

                                n "In one of the drawers, a dull shine caught my eye."
                                p "Huh..."
                                n "It was a large hunting knife."
                                n "It looked a little out of place among all these tools."
                                scene cg_ren_pole8
                                n "I turned and showed it to Ren."
                                p "What do you think?"
                                n "He visibly paled and went still."
                                n "I walked closer, interested by his reaction."
                                p "All these saws and hammers and you're scared of this knife...?"
                                n "He tried to shrink away from me, but the pole held him fast."
                                jump ren_day3sub_knife
                            "-Let Ren choose-":

                                p "Tsk."
                                n "I looked over my choices."
                                n "A heavy powered nail gun..."
                                n "Or..."
                                n "I turned over a knife I'd found in a drawer."
                                n "I admired the glint of my reflection in it for a moment before facing Ren."
                                scene cg_ren_pole6
                                show cg_ren_pole_knife
                                show cg_ren_pole_nailgun
                                p "What do you think, Ren?"
                                n "I held up both options for him to see."
                                n "He looked at the nail gun, seeming to need a moment to figure out what it was."
                                n "Then his gaze settled on the knife and he stopped breathing for a moment."
                                n "His eyes were wide, as if he'd seen a ghost."
                                p "Come on Ren."
                                n "He snapped back to reality."
                                p "If you can't choose I'll use both..."
                                scene cg_ren_pole
                                show cg_ren_pole_knife
                                show cg_ren_pole_nailgun
                                ren "{size=10}T...the knife...{/size}"
                                p "Speak up!"
                                ren "The knife!"
                                scene cg_ren_pole5
                                show cg_ren_pole_knife
                                show cg_ren_pole_nailgun
                                n "He looked back down and trembled."
                                p "..."
                                hide cg_ren_pole_nailgun
                                p "Good choice."
                                jump ren_day3sub_knife

label ren_day3sub_nailgun:
n "I wonder if the nail will make it through the floor..."
n "Only one way to find out!"
n "I advanced on Ren, then held one of his legs."
scene cg_ren_pole
show cg_ren_pole_nailgun
n "His begging became wordless whining."
n "His skin felt a little cold..."
n "I pressed the gun to the top of his foot."
p "You wanted to share something special with me Ren."
n "He looked up at me."
scene cg_ren_pole9
n "{size=30}{b}BANG{/b}{/size}" with vpunch
scene cg_ren_pole10
n "I pulled the trigger and listened to him scream."
p "Come on Ren!"
p "We're just getting started!"
n "He tried to pull his foot back and yelped in pain."
n "The nail really did go into the concrete!"
p "This thing is pretty heavy duty, huh?"
n "I licked my lips."
scene cg_ren_pole11
n "I grasped his free foot and positioned the gun."
scene cg_ren_pole12
n "{size=30}{b}BANG{/b}{/size}" with vpunch
scene cg_ren_pole13
ren "S-stop!!!"
ren "Please..."
p "Ren..."
p "We're well past the point of begging."
p "Don't you think?"
scene cg_ren_pole14
show cg_ren_pole_nailgun
n "I held the tool up to his upper arm and fired another nail."
scene cg_ren_pole15
n "{size=30}{b}BANG{/b}{/size}" with vpunch
scene cg_ren_pole16
n "His screames were getting hoarser, but I felt that he hadn't had nearly enough."
n "{size=30}{b}BANG{/b}{/size}" with vpunch
n "{size=30}{b}BANG BANG{/b}{/size}" with vpunch
n "{size=30}{b}BANG BANG BANG{/b}{/size}" with vpunch
scene cg_ren_pole17
n "I gripped his other arm, firing wildly and breathing unsteady."
n "I stopped to catch my breath."
n "...He wasn't screaming any more."
n "I examined his arm."
n "His arms were so thin that the industrial nails went right through to the other side."
n "He was shivering and staring blankly."
show cg_ren_pole_nailgun
n "I tapped his face with the gun."
p "Rennn."
n "He turned his eyes to me, but barely responded."
p "I'm not finished."
n "I looked him over and settled on his fuzzy ear."
scene cg_ren_pole18
n "When I grabbed it, he flinched and made a choked rasp."
ren "N...n-no...pl-"
scene cg_ren_pole19
n "{size=30}{b}BANG{/b}{/size}" with vpunch
n "I fired it through his ear."
n "It was so soft and thin that the nail went through it entirely and ended up on the floor somewhere."
scene cg_ren_pole20
n "He made a last pathetic sob before his head drooped."
p "Hmm."
n "I don't think he can take any more."
menu:
    "-Finish him off-":
        p "Tsk."
        p "You're pathetic."
        n "I held the gun up to his forehead."
        n "He didn't seem to notice."
        n "Or if he did, he didn't care."
        scene black with dissolve
        stop sound fadeout 1.0
        stop music fadeout 1.0
        n "{size=30}{b}BANG{/b}{/size}" with vpunch
        hide screen health_bar
        hide screen sanity_bar
        hide ren_remote onlayer screens
        $ persistent.ren_ending_subnaildie = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_subnaildie:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You nailed Ren in the head.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_subnaildie
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Patch him up-":
        n "I laid the nailgun down."
        n "I think he's learned his lesson."
        n "I checked his neck."
        n "He's alive...just unresponsive."
        n "I didn't have to search hard to find medical supplies."
        n "I pulled the nails out of his skin slowly."
        n "He kept shivering but he didn't make a sound."
        n "I smiled at the blood welling up from the holes left behind."
        p "We {i}did{/i} share something special."
        scene cg_ren_pole21
        p "I held his chin up so he could see me."
        p "I understand what you meant now."
        n "I disinfected his wounds and wrapped bandages around every one."
        p "Do you want to go back upstairs now?"
        n "He looked to me and nodded slowly."
        scene black with dissolve
        n "I put my arm around him and helped him up."
        p "I'm glad you found me, Ren."
        n "I gave him a little squeeze as I pulled him up the stairs."
        stop sound fadeout 1.0
        stop music fadeout 1.0
        n "We're going to have so much fun together..."
        hide screen health_bar
        hide screen sanity_bar
        hide ren_remote onlayer screens
        $ persistent.ren_ending_subnaillive = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_subnaillive:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You gave your pet a few new holes.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_subnaillive
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()

label ren_day3sub_knife:
n "I wanted to be closer to him."
scene cg_ren_pole
show cg_ren_pole_knife
n "I crouched down and held the knife where he could see it."
n "I looked over his arms and legs."
p "You know..."
p "You've got an awful lot of scars."
n "I saw more tears roll down his cheeks."
p "Is that why you're so worried about this?"
n "I wiggled the knife."
scene cg_ren_pole5
show cg_ren_pole_knife
n "He curled up as much as he could."
p "Hey!"
scene cg_ren_pole6
show cg_ren_pole_knife
n "I grabbed his hair and pulled his head back up, eliciting a yelp."
p "I asked you a question."
ren "Y-yes!"
ren "I...that knife..."
p "It's been used on you before?"
n "He nodded once."
p "By who?"
n "His eyes flicked toward the freezer."
if ren_sawcorpse == True:
    p "HIM!?"
    p "Ahaha!"
    p "Well."
    n "I pressed the knife against his cheek."
    p "I'm not gonna end up like that freezer burnt bitch."
else:
    p "Tsk."
    p "Fine, don't tell me."
    n "I pressed the knife to his cheek."
    p "I don't really care anyway."
scene cg_ren_pole22
show cg_ren_pole_knife
n "I dragged the blade lightly over the mark on his face."
n "I grinned approvingly at the two shades of red."
scene cg_ren_pole23
show cg_ren_pole_knife
ren "Please..."
p "Shhh."
n "I grabbed his ankle and pulled his bare leg straight."
ren "N-n..."
scene cg_ren_pole24
n "I plunged the blade into the meat of his upper thigh."
scene cg_ren_pole25
n "He screamed and blood began to drip from the wound."
n "I was suddenly overcome with a strange feeling of... jealousy."
n "These other marks weren't made by me..."
scene cg_ren_pole26
show cg_ren_pole_knife2
n "I held down his leg and pulled the sharp edge through an old scar."
n "He screamed and writhed under my grip."
p "But your blood is mine now..."
n "Ren lifted his teary face to look at me."
ren "W...what..?"
n "I watched it flowing...warm...and pooling around his soft skin."
scene cg_ren_pole27
show cg_ren_pole_knife2
n "I cut him again."
n "Deeper."
n "His cries were becoming weaker as I became more entranced."
n "I wanted to replace every one of his scars..."
scene cg_ren_pole28
show cg_ren_pole_knife2
n "I stopped for a moment and looked down at Ren."
n "He's covered in blood."
n "He began to shiver quietly."
p "Ren."
n "He didn't respond."
n "I pressed the tip of the knife into his flesh again."
p "Ren!"
n "Nothing."
p "Hm."
n "I checked for his pulse."
n "...He's alive...but..."
n "I looked at all of the blood gathering on the floor."
hide cg_ren_pole_knife2
n "I don't think he can take any more."
menu:
    "-Let him bleed-":
        n "I stared at the blood."
        n "There's only one way to make him really mine."
        n "...Forever."
        n "His ears twitched as he slowly raised his head."
        scene cg_ren_pole29
        n "He looked at me."
        n "Almost completely broken..."
        ren "{size=12}Please...{/size}"
        n "It looked like every word was a monumental struggle to him."
        ren "...Help me..."
        n "I looked down at him."
        p "..."
        stop sound fadeout 1.0
        stop music fadeout 1.0
        n "And I didn't do anything."
        scene black with dissolve
        hide screen health_bar
        hide screen sanity_bar
        hide ren_remote onlayer screens
        $ persistent.ren_ending_subknifedie = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_subknifedie:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You let Ren bleed.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_subknifedie
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "-Patch him up-":

        n "I took a deep breath."
        n "I can't just let him die like this."
        n "I put the knife down."
        n "Then I'll never get to replace all his scars..."
        n "I didn't have to search hard to find medical supplies."
        scene cg_ren_pole30
        n "I disinfected and cleaned his cuts."
        n "I retrieved a needle and thread from the supplies."
        p "Some of these are pretty deep...huh?"
        n "I asked him sheepishly and received no response."
        n "I shrugged and got back to work."
        n "I carefully sewed his larger gashes up."
        scene cg_ren_pole31
        n "It was sort of relaxing..."
        n "He kept shivering but he didn't make a sound."
        p "We {i}did{/i} share something special."
        scene cg_ren_pole32
        p "I held his chin up so he could see me."
        p "I understand what you meant now."
        n "I wrapped gauze over his limbs."
        p "Do you want to go back upstairs now?"
        n "He looked to me and nodded slowly."
        scene black with dissolve
        n "I put my arm around him and helped him up."
        p "I'm glad you found me, Ren."
        n "I gave him a little squeeze as I pulled him up the stairs."
        stop sound fadeout 1.0
        stop music fadeout 1.0
        n "We're going to have so much fun together..."
        hide screen health_bar
        hide screen sanity_bar
        hide ren_remote onlayer screens
        $ persistent.ren_ending_subknifelive = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_subknifelive:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}You replaced a few of Ren's scars.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_subknifelive
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()

label ren_day3_neutral:
scene bg_ren_livingroom at right with dissolve
p "Ugh..."
n "I woke up with a deep feeling of dread."
n "Then I realized where I was and it doubled."
play music ren_neutral fadein 2.0
ren "H..Hey [player_name]..."
$ rexp = 25
show ren:
    subpixel True
    xalign 0.6
    alpha 0.0
    easeout 0.2 alpha 1.0 xalign 0.5
n "I couldn't get Lawrence's face out my head."
n "...And by the looks of it, neither could Ren."
n "There was a tense silence before Ren finally spoke."
ren "I...thought it would be easy."
ren "I've never...I mean not really..."
n "I looked at him questioningly."
$ rexp,rears = 26,3
ren "...Killed someone."
ren "...Not before Lawrence..."
menu:
    "\"What about that guy in the basement?\"" if ren_sawcorpse == True:
        $ rexp,rears = 2,1
        ren "What!?"
        $ rexp = 27
        ren "H-how did you..."
        p "...I went in the basement when you were gone."
        $ rears = 3
        p "And I saw..."
        $ rexp = 6
        p "Well...you know."
        n "He looked flustered and...scared."
        ren "I-I didn't kill him!"
        ren "He died... by himself."
        n "I remembered the man in the freezer."
        n "All that blood...and his chest..."
        menu:
            "\"He couldn't have done that to himself.\"":
                $ rexp = 17
                $ rears = 4
                $ ren_love -= 10
                n "Ren huffed with frustration."
                ren "He made a mistake!"
                $ rexp = 6
                ren "It was one of his..."
                ren "..."
                $ rears = 3
                ren "He brought a friend home."
                ren "Um, well not a friend..."
                ren "H-he...hurt people."
                ren "And t-they stabbed him."
                ren "In the neck."
                ren "They both died."
                n "I furrowed my eyebrows."
                n "They both...died?"
                n "...what?"
            "\"How did he die?\"":
                $ rexp,rears = 2,3
                ren "..."
                $ rexp = 27
                n "Ren visibly clammed up."
                ren "He..."
                ren "He brought someone home."
                ren "He sometimes..."
                n "I waited patiently for him to continue."
                $ rexp = 13
                ren "He sometimes hurt people..."
                n "I looked at Ren's face and neck."
                n "Suddenly wondering about those scars."
                $ rexp = 6
                ren "He messed up."
                ren "T-they got a knife..."
                ren "And..."
                ren "Well."
                ren "T-they both ended up dead."
        n "I tried to think it over for a moment."
        n "It wasn't adding up."
        n "I looked back at Ren."
        menu:
            "\"But his chest...\"":
                $ rexp,rears = 21,2
                ren "..."
                $ ren_love -= 20
                $ rexp = 17
                play sound law_brownnote fadein 2.0 loop
                play music ren_warppiano fadein 2.0
                ren "He was already DEAD!"
                ren "And I..."
                n "I realized Ren was breathing harder and I leaned away from him."
                $ rexp = 19
                ren "I wanted a part..."
                ren "After all the things he did..."
                $ rexp = 21
                ren "I deserved it!"
                $ rexp = 12
                ren "I needed a piece of him to take with me..."
                ren "And he looked so good...still warm..."
                $ rexp = 19
                ren "S-so I just cut him open."
                ren "It's not like he'd feel it."
                ren "And I got it..."
                ren "I ate it..."
                n "My eyes widened."
                p "...Ate...Ate what!?"
                $ rexp = 18
                n "I yelped as Ren snapped at me."
                ren "I. am. NOT. HUMAN!"
                ren "I ATE HIS HEART!"
                $ rexp = 16
                ren "..."
                n "I stumbled backward, trying to get away from him."
                ren "I know what you're thinking, [player_name]."
                $ rexp = 7
                ren "'Oh no, how terrible, how disgusting...'"
                $ rexp = 15
                ren "Does that sound right?"
                n "I shook my head quickly."
                stop music fadeout 1.0
                $ rexp = 16
                ren "..."
                $ rbase = 2
                play music ren_obsessed fadein 1.0
                ren "I've decided that I don't really need to hear what you think any more."
                p "No PL-"
                $ rbase = 3
                show screen disableclick(3.0)
                $ ren_shocking = True
                play sound ren_shocked
                $ health = 10
                $ sanity = 10
                p "!!!! {w=3.0}{nw}" with largeshake
                $ ren_shocking = False
                stop sound
                $ rbase,rears,rexp = 1,2,10
                n "The pain shot through my body like fire."
                n "I was only dimly aware that I'd fallen back and that Ren had pounced on top of me."
                scene cg_ren_eatmyheart with dissolve
                play sound law_heartbeat fadein 1.0 loop
                n "I can't...move..."
                n "I tried to scream as he dug claws into my chest through my shirt."
                $ health -= 10
                $ sanity -= 10
                n "I only managed terrified choked wheezes as he tore through the material and flesh."
                n "I had nothing left to fight with."
                stop music fadeout 1.0
                n "I could only stare in dull horror as he pulled the deepest part of me out."
                stop sound fadeout 1.0
                scene black with dissolve
                hide screen health_bar
                hide screen sanity_bar
                hide ren_collar onlayer screens
                $ persistent.ren_ending_neutralheart = True
                play music law_twinkle fadein 1.0
                scene endslate with Dissolve(1.0)
                screen ren_ending_neutralheart:
                    text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                    text "\n\n\n\n{=endslate_subtitle}Ren ate your heart.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                show screen ren_ending_neutralheart
                with Dissolve(1.0)
                pause
                $ renpy.full_restart()
            "\"He...hurt people?\"":

                n "Ren looked uncomfortable."
                ren "Well..."
                ren "He said....that's how you can really know someone..."
                n "I squinted at Ren."
                $ rexp = 13
                ren "Like really REALLY know them."
                ren "...So..."
                $ rexp = 19
                ren "So yeah."
                ren "Sometimes he hurt people."
                $ rexp = 6
                ren "S-sometimes he...killed people."
                n "I remembered the basement."
                n "And the stains on the floor."
                menu:
                    "\"Sounds like he was a psychopath.\"":
                        $ rears,rexp = 2,17
                        n "His fur bristled."
                        ren "No!"
                        $ rears,rexp = 2,21
                        ren "Weak people die!"
                        ren "Strong people live!"
                        ren "That's how it works!"
                        menu:
                            "\"Isn't he dead though?\"":
                                ren "T-that..."
                                $ rears,rexp = 3,16
                                ren "That was a stupid mistake!"
                                $ rears,rexp,rblush = 3,6,1
                                ren "It wasn't fair..."
                                n "He took a few deep breaths, looking like he was trying to hold back tears."
                                $ rears,rexp,rblush = 3,27,2
                                ren "He was the only one..."
                                ren "He took care of me..."
                                menu:
                                    "\"It looks like he only hurt you.\"":
                                        $ rears,rexp,rblush = 4,28,0
                                        n "He couldn't hold back his tears any more."
                                        ren "That's not true!"
                                        ren "He...he..."
                                        ren "No one ever cared about me like that!"
                                        ren "He {i}loved{/i} me..."
                                        n "Ren sniffed and slouched, shrinking down."
                                        ren "And now that he's gone..."
                                        ren "I've never felt more empty."
                                        n "He started sobbing."
                                        ren "Why....why did I..."
                                        menu:
                                            "\"He didn't love you.\"":
                                                jump ren_neutral_stradeconvo_murder
                                            "\"What did you do?\"":
                                                n "I asked him cautiously."
                                                n "Quietly, almost a whisper."
                                                n "I could tell he was unstable..."
                                                n "Dangerous."
                                                $ rears,rexp,rblush = 3,27,2
                                                n "Ren sniffed and lifted his head."
                                                ren "I didn't do anything."
                                                n "I looked at him, confused."
                                                ren "I didn't..."
                                                $ rears,rexp,rblush = 3,13,1
                                                ren "I didn't do anything."
                                                scene cg_ren_flashback1 with Dissolve(1.5)
                                                ren "I didn't do anything."
                                                ren "He told me to help him."
                                                ren "He even begged me."
                                                ren "..."
                                                scene cg_ren_flashback2 with dissolve
                                                ren "But I didn't do anything."
                                                ren "I could only think of the things...he did..."
                                                scene bg_ren_livingroom at right
                                                $ rears,rexp,rblush = 4,5,2
                                                show ren with vpunch
                                                ren "WHY DIDN'T I HELP HIM!?"
                                                menu:
                                                    "\"You don't need him.\"":
                                                        $ rears,rexp,rblush = 3,27,1
                                                        ren "W-what?"
                                                        menu:
                                                            "\"You have me now.\"":
                                                                jump ren_neutral_stradeconvo_keep
                                                            "\"You never needed him.\"":
                                                                $ rears,rexp,rblush = 3,6,1
                                                                ren "Of course I did..."
                                                                $ rears,rexp,rblush = 3,26,0
                                                                ren "I didn't have anything before him."
                                                                $ rears,rexp,rblush = 4,25,0
                                                                ren "My family hates me."
                                                                ren "I didn't have any friends..."
                                                                ren "He was the only-"
                                                                $ rears,rexp,rblush = 3,25,0
                                                                p "Stop."
                                                                $ rears,rexp,rblush = 3,27,0
                                                                ren "...What?"
                                                                p "You're alive now, right?"
                                                                ren "Yeah...I guess..."
                                                                p "You've done that with and without him."
                                                                p "You don't need him."
                                                                p "And you don't need me."
                                                                ren "But..."
                                                                p "You've been through pain."
                                                                p "But you don't know what tomorrow's gonna bring."
                                                                p "So why not wait and find out?"
                                                                $ rears,rexp,rblush = 1,24,0
                                                                ren "I..."
                                                                ren "I don't want any more pain."
                                                                $ rears,rexp,rblush = 3,6,0
                                                                ren "I'm scared."
                                                                p "That's okay."
                                                                p "The future is scary."
                                                                $ rears,rexp,rblush = 1,6,0
                                                                p "But it can be fun too."
                                                                p "You're only gonna get one chance at this, Ren."
                                                                $ rears,rexp,rblush = 1,27,0
                                                                stop music fadeout 2.0
                                                                ren "..."
                                                                $ rears,rexp,rblush = 1,13,0
                                                                $ rbase = 2
                                                                n "I tensed up as he raised the remote."
                                                                $ rbase = 3
                                                                n "But instead of a shock, I heard a quiet click."
                                                                $ rbase = 1
                                                                play music ren_piano fadein 3.0
                                                                hide ren_collar onlayer screens with dissolve
                                                                n "The collar popped open and fell to the floor like a dead weight."
                                                                $ rears,rexp,rblush = 3,25,0
                                                                ren "Please...just go."
                                                                ren "Before I change my mind again."
                                                                n "I paused for a moment."
                                                                n "Then I grabbed a pen and paper off the coffee table."
                                                                p "I'm going to leave."
                                                                $ rears,rexp,rblush = 1,2,0
                                                                p "But...I want you to have my number."
                                                                scene cg_ren_good with dissolve
                                                                p "I want to be your friend... for real."
                                                                p "Call me, and we can do something fun together."
                                                                p "Something we both like."
                                                                p "...Okay?"
                                                                n "He nodded silently."
                                                                scene white with dissolve
                                                                stop sound fadeout 1.0
                                                                stop music fadeout 1.0
                                                                n "I can't know what the future holds either."
                                                                n "But I'm willing to find out."
                                                                hide screen health_bar
                                                                hide screen sanity_bar
                                                                hide ren_collar onlayer screens
                                                                $ persistent.ren_ending_neutralgood = True
                                                                play music ren_piano fadein 1.0
                                                                scene endslate_clean with Dissolve(1.0)
                                                                screen ren_ending_neutralgood:
                                                                    text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                                                                    text "\n\n\n\n{=endslate_subtitle}and you helped Ren.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                                                                show screen ren_ending_neutralgood
                                                                with Dissolve(1.0)
                                                                pause
                                                                $ renpy.full_restart()
                                                    "\"You did the right thing.\"":
                                                        p "He was a murderer."
                                                        $ rexp = 24
                                                        p "...A monster."
                                                        ren "..."
                                                        $ rexp = 25
                                                        $ rblush = 0
                                                        ren "You're right."
                                                        $ rexp = 26
                                                        n "Ren looked up at me wearily."
                                                        ren "And so am I."
                                                        jump ren_neutral_stradeconvo_murder
                                                    "-Say nothing-":
                                                        n "Ren continued to shake silently for a few moments."
                                                        $ rexp,rblush = 24,1
                                                        n "When he finally spoke again, his voice was soft and even."
                                                        ren "Now he's gone."
                                                        ren "And I've been... trying to replace him."
                                                        $ rexp,rblush = 25,0
                                                        ren "But I can't."
                                                        ren "You're nothing like him."
                                                        ren "..."
                                                        ren "What a mistake."
                                                        ren "Everything I do is a mistake."
                                                        $ rexp = 26
                                                        ren "...I deserve to be alone."
                                                        $ rbase = 2
                                                        n "He raised the remote."
                                                        n "I didn't have time to react."
                                                        $ rbase = 3
                                                        show screen disableclick(2.0)
                                                        $ ren_shocking = True
                                                        play sound ren_shocked
                                                        $ health -= 20
                                                        $ sanity -= 20
                                                        p "!!!! {w=2.0}{nw}" with largeshake
                                                        scene black with vpunch
                                                        $ ren_shocking = False
                                                        stop sound
                                                        stop music fadeout 1.0
                                                        pause 1.5
                                                        hide ren_collar onlayer screens
                                                        $ health += 10
                                                        $ sanity += 10
                                                        scene bg_ren_livingroom at right with Dissolve(1.5)
                                                        play sound law_day fadein 1.0 loop
                                                        p "Ugh..."
                                                        n "I woke up and looked around."
                                                        n "The living room was becoming familiar to me."
                                                        n "I wasn't sure how I felt about that."
                                                        n "I looked down and noticed that I was no longer chained to the wall."
                                                        n "I reached up."
                                                        p "!!!"
                                                        n "No collar either!"
                                                        p "R...Ren?"
                                                        n "I searched around the room and yelled louder."
                                                        p "Ren!?"
                                                        n "No reply."
                                                        n "Just silence."
                                                        scene black with dissolve
                                                        n "I searched the entire house and waited."
                                                        n "But he never came back."
                                                        scene black with dissolve
                                                        hide screen health_bar
                                                        hide screen sanity_bar
                                                        hide ren_collar onlayer screens
                                                        $ persistent.ren_ending_neutralabandon = True
                                                        play music law_twinkle fadein 1.0
                                                        scene endslate_clean with Dissolve(1.0)
                                                        screen ren_ending_neutralabandon:
                                                            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                                                            text "\n\n\n\n{=endslate_subtitle}Now the house is yours.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
                                                        show screen ren_ending_neutralabandon
                                                        with Dissolve(1.0)
                                                        pause
                                                        $ renpy.full_restart()
                                            "\"I'm sorry...it's okay now.\"":
                                                jump ren_neutral_stradeconvo_keepren
                                    "\"I can take care of you now.\"":
                                        jump ren_neutral_stradeconvo_keepren
                            "\"I'm sorry, I didn't mean it that way.\"":
                                p "That's all in the past now anyway."
                                p "It doesn't matter."
                                jump ren_neutral_stradeconvo_keepren
                    "-Say Nothing-":

                        jump ren_neutral_stradeconvo_keep
    "\"Neither have I.\"":

        $ rexp = 27
        ren "..."
        $ ren_love += 10
        $ rexp = 15
        ren "Is...is that a joke?"
        n "I shrugged and let out a small awkward laugh."
        $ rears = 1
        n "He joined me and relaxed a bit."
        p "I guess we're both criminals now."
        $ rexp = 6
        ren "Ah...ha....yeah..."
        ren "Well..."
        ren "This house is made for people like us."
        n "I looked around at the seemingly pleasant room."
        p "It's not so bad, huh?"
        ren "No..."
        $ rexp = 12
        ren "And we have each other."
        p "..."
        p "Yeah."
        scene black with dissolve
        p "We got each other."
        stop sound fadeout 1.0
        stop music fadeout 1.0
        scene black with dissolve
        hide screen health_bar
        hide screen sanity_bar
        hide ren_collar onlayer screens
        $ persistent.ren_ending_neutralneutral = True
        play music law_reverse fadein 1.0
        scene endslate_clean with Dissolve(1.0)
        screen ren_ending_neutralneutral:
            text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
            text "\n\n\n\n{=endslate_subtitle}It's not so bad.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
        show screen ren_ending_neutralneutral
        with Dissolve(1.0)
        pause
        $ renpy.full_restart()
    "\"You're a monster.\"":

        if ren_love >= 70:
            $ rexp = 27
            ren "I...I..."
            ren "I'm not..."
            n "He started crying."
            ren "I was just so..."
            ren "I was so lonely!"
            $ rexp,rears = 28,4
            n "He broke down."
            ren "I'm sorry!"
            ren "I'm sorry for everything!!"
            $ rbase = 2
            n "I flinched as he lifted the remote."
            n "But he pressed a different button."
            n "I heard a metallic click and the collar around my neck sprung open."
            $ rbase = 1
            n "It fell to the floor in front of me and I looked at Ren in surprise."
            $ rexp = 25
            ren "You need to go."
            n "I almost wanted to comfort him..."
            n "But my survival instinct told me that this chance wouldn't last."
            ren "You're right..."
            $ rexp = 26
            ren "I am a monster."
            n "I took a step backward."
            $ rexp = 21
            ren "GO!!!"
            n "He screamed at me and I turned on my heel."
            n "I ran to the door and stumbled outside."
            stop music fadeout 1.0
            scene white with dissolve
            n "I ran until I couldn't any more."
            n "And I never turned back."
            hide screen health_bar
            hide screen sanity_bar
            hide ren_collar onlayer screens
            $ persistent.ren_ending_neutralrun = True
            play music law_twinkle fadein 1.0
            scene endslate_clean with Dissolve(1.0)
            screen ren_ending_neutralrun:
                text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                text "\n\n\n\n{=endslate_subtitle}You ran from Ren.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
            show screen ren_ending_neutralrun
            with Dissolve(1.0)
            pause
            $ renpy.full_restart()
        else:
            $ rexp = 27
            ren "I..."
            $ ren_love -= 100
            n "He looked hurt for a moment..."
            $ rexp = 16
            play music ren_obsessed fadein 1.0
            n "But then something changed."
            $ rexp = 17
            ren "STRADE was a monster!"
            ren "LAWRENCE was a monster!"
            $ rexp = 21
            ren "All I wanted was for someone to love me!"
            n "He was breathing hard..."
            n "I took a step back."
            ren "I was lonely...and I chose you."
            ren "But you're an ungrateful, unloving..."
            ren "Y-you..."
            $ rears,rexp = 2,18
            ren "YOU'RE the monster!"
            $ rbase = 2
            n "He raised the remote."
            n "I tried to run, but it was too late."
            $ rbase = 3
            $ ren_shocking = True
            play sound ren_shocked
            show screen disableclick(2.0)
            $ health -= 20
            $ sanity -= 20
            p "{cps=12}!!!!{/cps}{w=2.0}{nw}" with largeshake
            $ ren_shocking = False
            n "I fell to the floor."
            scene cg_ren_neutralmad with dissolve
            stop sound
            pause(1.0)
            n "I gasped for air."
            n "I didn't have time to beg before he pressed it again."
            $ ren_shocking = True
            play sound ren_shocked
            show screen disableclick(2.0)
            $ health -= 100
            $ sanity -= 100
            n "{cps=12}{/cps}{w=2.0}{nw}" with largeshake
            $ ren_shocking = False
            stop sound
            stop music fadeout 1.0
            scene black with dissolve
            n "Eventually, the pain stopped."
            hide screen health_bar
            hide screen sanity_bar
            hide ren_collar onlayer screens
            $ persistent.ren_ending_neutralshock = True
            play music law_twinkle fadein 1.0
            scene endslate with Dissolve(1.0)
            screen ren_ending_neutralshock:
                text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
                text "\n\n\n\n{=endslate_subtitle}Ren shocked you to death.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
            show screen ren_ending_neutralshock
            with Dissolve(1.0)
            pause
            $ renpy.full_restart()

label ren_neutral_stradeconvo_keep:
    $ ren_love += 10
    ren "..."
    $ rexp = 13
    ren "I have you now..."
    n "He shook his head."
    $ rexp = 15
    ren "L-look at me, getting all worked up about the past."
    n "His worried expression was only partially replaced by a strange smile."
    $ rexp = 19
    ren "I don't need to worry about him any more."
    $ rexp = 22
    ren "And you don't need to worry about anything."
    scene cg_ren_neutralyandere with dissolve
    ren "...You'll never leave me..."
    ren "I won't let you die."
    ren "I'll take care of you..."
    scene black with dissolve
    stop sound fadeout 1.0
    stop music fadeout 1.0
    ren "Forever. {image=icon_heart.png}"
    hide screen health_bar
    hide screen sanity_bar
    hide ren_collar onlayer screens
    $ persistent.ren_ending_neutralkeep = True
    play music law_reverse fadein 1.0
    scene endslate_clean with Dissolve(1.0)
    screen ren_ending_neutralkeep:
        text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}Ren won't let you die.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen ren_ending_neutralkeep
    with Dissolve(1.0)
    pause
    $ renpy.full_restart()

label ren_neutral_stradeconvo_keepren:
    $ ren_love += 10
    $ rexp,rears = 2,3
    ren "...H-huh?"
    p "The past is all over."
    $ rexp,rears = 27,1
    n "I reached for him slowly and pet his hair."
    n "He accepted it and seemed to calm down a little."
    p "I'm here now."
    p "And I like it here."
    $ rexp,rears,rblush = 15,1,1
    ren "You...do...?"
    $ ren_love += 10
    p "And I like you."
    n "I'm sure it looked strange, someone in a chain and collar, petting their captor."
    n "But I didn't care."
    $ rexp,rears,rblush = 8,1,2
    p "I'll take care of you."
    n "He relaxed."
    ren "I'll take care of you too..."
    $ rexp,rears,rblush = 1,3,2
    n "He crawled onto the couch with me."
    n "I heard the soft clinking of the chain on the floor."
    scene black with dissolve
    stop sound fadeout 1.0
    stop music fadeout 1.0
    n "But it didn't bother me."
    hide screen health_bar
    hide screen sanity_bar
    hide ren_collar onlayer screens
    play music law_reverse fadein 1.0
    $ persistent.ren_ending_neutralkeepren = True
    scene endslate_clean with Dissolve(1.0)
    screen ren_ending_neutralkeepren:
        text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}You'll take care of each other.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen ren_ending_neutralkeepren
    with Dissolve(1.0)
    pause
    $ renpy.full_restart()

label ren_neutral_stradeconvo_murder:
    play music ren_obsessed fadein 1.0
    $ rexp = 16
    n "Ren looked at me darkly."
    n "I felt a pit of dread in my gut as I knew I'd done something wrong."
    $ rbase = 2
    n "He raised the remote."
    n "I tried to run, but it was too late."
    $ rbase = 3
    $ ren_shocking = True
    play sound ren_shocked
    show screen disableclick(2.0)
    $ health -= 20
    $ sanity -= 20
    p "{cps=12}!!!!{/cps}{w=2.0}{nw}" with largeshake
    $ ren_shocking = False
    stop sound
    scene cg_ren_neutralmad with dissolve
    n "I fell to the floor."
    pause(1.0)
    n "I gasped for air."
    n "I didn't have time to beg before he pressed it again."
    $ ren_shocking = True
    play sound ren_shocked
    $ health -= 100
    $ sanity -= 100
    n "{cps=12}{/cps}{w=2.0}{nw}" with largeshake
    $ ren_shocking = False
    stop sound
    scene black with dissolve
    n "Eventually, the pain stopped."
    hide screen health_bar
    hide screen sanity_bar
    hide ren_collar onlayer screens
    play music law_twinkle fadein 1.0
    $ persistent.ren_ending_neutralshock = True
    scene endslate with Dissolve(1.0)
    screen ren_ending_neutralshock:
        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}Ren shocked you to death.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen ren_ending_neutralshock
    with Dissolve(1.0)
    pause
    $ renpy.full_restart()

label ren_ending_health:
    n "Ah.h...I can't..."
    scene black with dissolve
    scene black with vpunch
    stop sound fadeout 1.0
    stop music fadeout 1.0
    n "I couldn't move."
    n "I couldn't even... feel any more."
    n "I couldn't open my eyes."
    n "And somehow I knew..."
    n "I'd never open them again."
    $ health -= 100
    $ sanity -= 100
    n "At least it didn't hurt any more."
    hide screen health_bar
    hide screen sanity_bar
    hide ren_collar onlayer screens
    hide ren_remote onlayer screens
    $ persistent.ren_ending_health = True
    play music law_twinkle fadein 1.0
    scene endslate with Dissolve(1.0)
    screen ren_ending_health:
        text "{=endslate_title}You Died{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}Your body gave out.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen ren_ending_health
    with Dissolve(1.0)
    pause
    $ renpy.full_restart()

label ren_ending_sanity:
    n "My head fell forward."
    n "I could feel myself...pulling..."
    n "Everything hurt so much, it felt like my mind was on fire."
    n "He...he did this to me."
    stop music fadeout 1.0
    n "I looked up."
    $ rexp,rblush = 2,1
    play music ren_vampire fadein 1.0
    p "Ren..."
    $ rears,rbase = 1,4
    n "I was breathing harder."
    n "Everything on fire."
    n "He made me feel..."
    $ rexp,rblush = 15,2
    $ ren_love += 10
    ren "[player_name], what are you doing?"
    n "What was I..."
    n "I looked down again."
    n "I was rubbing my knees together."
    n "Slowly..."
    $ ren_love += 10
    p "Ren...please..."
    $ rexp, blush = 23,2
    p "M-more..."
    n "My nerves were buzzing."
    n "He crouched closer."
    n "I wanted him to."
    n "I wanted..."
    $ rexp,rblush = 2,2
    n "I slowly spread my legs in front of him."
    p "Touch me... hurt me..."
    n "The blaze was getting brighter."
    scene cg_ren_sanity with dissolve
    n "He came close and touched me."
    n "Everywhere he touched...licked...his claws sank in."
    n "It was like a hundred thousand fireflies."
    n "Everything was bright and blurry, but I could feel so much."
    n "He was moving against me..."
    n "I could feel his skin on mine."
    n "His claws in my neck."
    n "Touching my veins on fire... I couldn't take it."
    n "My whimpering turned into loud and desperate moans."
    n "My breath was caught for a moment as I felt something harder pressed against me."
    n "Only a moment later, it returned with a sharp cry as he pressed himself inside of me."
    n "I pulled and twisted against my bonds."
    n "Not to get away, but because I wanted so badly to touch him more."
    n "I writhed and bled for him."
    n "It was too much... too bright."
    n "I cried out wordlessly in time with his movements."
    n "His grip became tighter, claws sinking deeper."
    n "I couldn't hold anything back."
    n "I was barely aware of his own fevered panting and the warmth that filled me."
    n "I Let out a last hoarse cry and shuddered."
    n "I could barely breathe, but the explosive fire was finally turning to a warm fading glow."
    scene black with dissolve
    n "I sank willingly into the darkness."
    hide screen health_bar
    hide screen sanity_bar
    stop music fadeout 1.0
    stop sound fadeout 1.0
    n "I'd found what I needed."
    n "A weak smile crossed my features as I slipped into unconsciousness."
    n "I knew when I woke up I'd do anything for more."
    hide ren_collar onlayer screens
    hide ren_remote onlayer screens
    $ persistent.ren_ending_sanity = True
    play music law_reverse fadein 1.0
    scene endslate_clean with Dissolve(1.0)
    screen ren_ending_sanity:
        text "{=endslate_title}You Survived{/=endslate_title}\n\n\n" outlines [(2, "000000", 0, 0)] at truecenter
        text "\n\n\n\n{=endslate_subtitle}You begged for more.{/=endslate_subtitle}" outlines [(2, "000000", 0, 0)] at truecenter
    show screen ren_ending_sanity
    with Dissolve(1.0)
    pause
    $ renpy.full_restart()



label law_subroutine:
    if health <= 20:
        jump law_ending_health
    if lsanity <= 0:
        jump law_ending_lsanity
    if sanity <= 0:
        jump law_ending_sanity
    if drugs == 3 and not drugwarning1:
        n "I had trouble focusing for a moment."
        n "I couldn't get my head to feel right..."
        $ drugwarning1 = True
    if drugs >= 4:
        jump law_ending_drugs
    return ()
label ren_subroutine:
    if health <= 0:
        jump ren_ending_health
    if sanity <= 0:
        jump ren_ending_sanity
    return ()

image sano_bg = "bs/sano_BG.jpg"
define sano = DynamicCharacter ("sano_name", window_background="vincent/dialoguebox_sano.png" )
image sano neutral = "vincent/sano_neutral.png"
image sano blush = "vincent/sano_blush.png"
image sano licklips = "vincent/sano_licklips.png"
image sano moanblush = "vincent/sano_moanblush.png"


label sano_extra:
scene bg_pub with fade
$ vbase, vblush, vexp = 6,0,2
$ lbase,lexp,lbangs,lblush = 1,1,1,0
show vincent
hide screen health_bar
hide screen sanity_bar
hide screen vincent_rage_bar
$ sano_name = "???"
play music "vincent/sanomusic.mp3"
n "Vincent leaned on the counter and sighed."
vincent "Ugh, shit."
n "He grumbled softly into his chest."
n "He was just meeting his friend for a drink, but he was always exhausted after a full moon."
n "He pushed the ice around his whiskey around."
vincent "Where is he?"
n "He felt someone tap him on the shoulder and Vincent closed his eye."
vincent "Who are you?"
show vincent:
    subpixel True
    xalign 0.05
    alpha 0.0
    easeout 0.3 alpha 1.0
show sano neutral:
    subpixel True
    xalign 0.9
    alpha 0.0
    easeout 0.3 alpha 1.0
n "Vincent grumbled into the glass as he sipped it."
sano "That's not really important."
sano "You've been talking to one of my patients, I just wanted to come see you."
n "Vincent's eye narrowed and he spun on his chair growling low at the man in front of him."
vincent "Yeah? What of it?"
sano "I just wanted to see who was making the scratch marks all over her body."
n "Vincent didn't like the way this guy was talking to him."
n "Vincent shot out of his seat and advanced on him."
vincent "Yeah?... What. Of. It?"
n "Vincent said slowly, his voice dripping in malice."
n "He knew exactly who the other man was looking for."
n "He backed up into the darkened hallway leading to the bathroom."
n "Vincent slammed the man into the wall."
n "His hand firmly around his neck."
vincent "Leave her alone."
n "Vincent growled as he pushed down on his throat."
show sano blush:
    subpixel True
    xalign 0.9
n "His face reddened with excitement as his hand gripped Vincent's arm."
sano "I wasn't interested in your relationship with the doll."
sano "I was interested in-"
show sano licklips:
    subpixel True
    xalign 0.9
n "A black tongue slid slowly across the other man's lips."
sano "You."
n "Vincent dropped the doctor and leaned back."
$ vbase, vexp = 6, 1
vincent "What?"
show sano blush:
    subpixel True
    xalign 0.9
sano "I'll be seeing you again."
sano "This isn't over."
n "He put his hands on Vincent's chest and tried to push him against the wall."
show sano moanblush:
    subpixel True
    xalign 0.9
show CG_sano_vincent with fade
n "Vincent snorted and shoved him back with greater force, a moan escaping the doctor's lips."
$ vbase,vblush, vexp = 6,1,2
sano "Ah~"
scene bg_pub with fade
show vincent:
    xalign 0.05
show sano blush:
    subpixel True
    xalign 0.9
vincent "Your name."
n "Vincent demanded."
$ vbase,vblush, vexp = 6,0,2
show sano blush:
    subpixel True
    xalign 0.9
n "The doctor pulled out a card and put it into Vincent's hand."
show sano neutral:
    subpixel True
    xalign 0.9
sano "Take care."
n "His hand gripped Vincent's, almost desperately."
n "He quickly turned and walked into the main room."
hide sano with dissolve
n "Vincent didn't follow."
n "He looked at the card and flipped it over."
vincent "Sano Kojima."
$ persistent.character_unlock_sano = True
vincent "Kojima huh?"
$ lbase, lexp, lbangs= 1, 1, 1
$ law_crazy = False
$ lawrence_name = "Lawrence"
show law with dissolve:
    subpixel True
    xalign .98
n "Vincent grumbled to himself as he looked over at Lawrence."
vincent "How long have you been there?"
law "I didn't want to bother you."
vincent "It's fine, better not to get tangled up in messes."
$ vbase,vblush, vexp = 6,0,9
n "Vincent pushed Lawrence playfully and nodded towards the bar."
$ lbase, lexp, lbangs= 1, 3, 1
vincent "Come on, Law. Let's grab a drink."
$ renpy.full_restart()


image bs_law_dick = "BS/cg_lawrence_dick.jpg"
image cg_cainspecial = "BS/CG_Cain_Special.jpg"
image cg_cainspecial2 = "BS/CG_Cain_Special_2.jpg"
image sano_bg = "BS/sano_BG.jpg"
define rire = Character("Rire",window_background="BS/dialoguebox_rire.png")
image rire = "BS/casual_rire_smile.png"
image rire smirk = "BS/casual_rire_smirk.png"
image bs_vincent_farz = "BS/cg_vincent_farz.jpg"
image bs_ren_doodles = "BS/ren_doodles.jpg"
image bs_mcrib = "BS/VincentEatsMcRib.jpg"


label bonus_law_dick:
scene bs_law_dick with fade
pause
$ renpy.transition(fade)
call screen extra

label bonus_vfarz:
scene bs_vincent_farz with fade
pause
$ renpy.transition(fade)
call screen extra

label bonus_ren_doodle:
scene bs_ren_doodles with fade
pause
$ renpy.transition(fade)
call screen extra

label bonus_mcrib:
scene bs_mcrib with fade
pause
$ renpy.transition(fade)
call screen extra

label bonus_ren_closet:
scene bg_ren_livingroom at right with fade
$ ren_name = "Ren"
$ ren_hideheart = True
show ren with dissolve
ren "And then we can..."
ren "-Sniff-"
$ rexp = 15
ren "...Do you smell that?"
n "I sniffed and shook my head."
$ rexp = 3
ren "It smells like..."
n "He walked over to the large closet and sniffed the door."
$ rexp = 2
ren "Ugh! It smells like rotting meat in here!"
n "I walked closer."
$ rexp = 24
ren "Sorry, I guess it's my fault."
ren "I didn't have time to move Law yet."
n "I bit my lip and looked at the door."
n "I could smell it now."
n "But it hasn't even been a day yet. Why would it smell so..."
$ rexp = 15
ren "Would you mind moving that downstairs? I need to get some cleaning stuff."
n "I nodded and opened the door."
scene bg_ren_darkroom with fade
n "..."
n "A chill crawled down my spine."
n "There's nothing here..."
$ renpy.transition(fade)
call screen extra

label sano_rire_special:
scene sano_bg with fade
show sano neutral
$ sano_name = "Sano"
play music "vincent/sanomusic.mp3"
n "Sano jumped at the sound behind him."
sano "Ah.. Can't you use the door?"
n "Sano said as he started to clean the exam table of his tools."
n "Sano sighed turning his back."
show sano neutral:
    subpixel True
    xalign 0.05
    alpha 0.0
    easeout 0.3 alpha 1.0
show rire:
    subpixel True
    xalign 0.9
    alpha 0.0
    easeout 0.3 alpha 1.0
rire "I can't come and visit my little snake once in awhile."
rire "Now where's the fun in that."
n "Rire said moving over to him and putting his hands on either side of Sano's body, pinning him in place against Sano's exam table."
sano "What do you want, Rire?"
rire "How have you been, Sano?"
n "He said in that smooth tone that made Sano tremble and turn quickly to face Rire."
n "He had to look up at the tall demon but Sano's composure remained."
sano "You know how I've been."
sano "I can't find Strade and I don't... know what happened to Akira."
n "Sano said pushing on Rire's arm, trying to release himself from the trap of the demon king."
n "A tentacle slid out of Rire's back tipping Sano's head up to look him in the eye."
n "His sunglasses sliding down slightly."
rire "Still chasing after shadows, little snake?"
sano "It's all I have left."
n "Sano said trying to push Rire's chest now."
n "Rire's hands slipped behind Sano's back and pulled him close, Sano's eyes snapping open."
show sano blush:
    xalign 0.05
n "He tried to contain the blush but he couldn't help but heat up."
rire "Now, now. Don't be rude."
rire "Shadows aren't the only thing you have."
n "Rire leaned down, the yellow eyes behind Rire's glasses glowing slightly."
rire "I'm here for you, Sano."
show rire smirk:
    xalign 0.9
n "He said with a grin showing off all his sharp teeth."
n "Sano swallowed hard and tried to lash out only to have more tentacles wrap around his wrists, pulling them up in the air."
sano "You can't replace Strade."
n "Sano muttered trying to shake the Demon king from his wrists."
n "Rire pushed his knee between Sano's leg grinding up against the younger man."
n "Sano let out a soft moan, immediately feeling ashamed."
n "He could just fight his way out, he was faster than Rire."
n "But, Sano couldn't get himself to care enough to run."
n "Maybe he just wanted this... more than anything."
rire "I don't need to replace him."
n "Rire said gripping Sano's face."
rire "I'm better than him."
rire "I can help you forget him, Sano."
n "He pulled Sano's chin closer to his own and grinned into Sano's lips."
n "Sano could feel himself relaxing a bit more as tears ran down his face."
n "The black inky tentacles running up his body, made him pant and squirm."
n "{i}'Help me forget....'{/i}"
rire "You'll feel better when I'm done with you, little snake."
stop music
$ renpy.transition(fade)
call screen extra





label vincent_special:
image cg_lawrence_Vincent_special = "bs/cg_lawrence_Vincent_special.jpg"
scene vincent_bedroom_day with fade
play music "vincent/vincent_sad_full.mp3"
$ lawrence_name = "Lawrence"
$ vincent_name = "Vincent"
$ lbase,lexp,lbangs,lblush= 1,1,1,0
$ vbase,vblush, vexp = 10,0, 14
$ law_crazy = False
$ vincent_love = 0
$ law_love = 0
show law:
    xalign .98
show vincent:
    subpixel True
    xalign 0.05
n "Vincent sat down on his bed and looked at Lawrence."
vincent "Ya know, I have weird things that comfort me."
n "Vincent said softly, Lawrence looked over at him and Vincent's eye drifted over to Lawrence."
n "Vincent hand gently gripping his black jeans."
$ lexp = 8
law "Don't we all..."
n "Lawrence said looking around Vincent, avoiding eye contact as usual but Vincent was used to it now."
vincent "Mine... is this patch."
n "Vincent said putting his hand over the worn cloth."
$ lexp = 1
law "...I... noticed that it wasn't really new."
vincent "I don't know where it came from, a friend gave it to me."
vincent "She said that she found it, but she didn't know where."
n "Vincent said with a soft growl."
n "He lifted the shirt to his nose and sniffed it."
vincent "I wish she did."
vincent "It makes me feel better."
n "Lawrence looked at it and looked at Vincent, listening intently."
n "Vincent knew there was no solution to what he was feeling."
vincent "I just wanted to vent."
vincent "Personal things aren't really something that people like hearin' ya know?"
n "Vincent said laying his head down on Lawrence's legs."
$ lexp = 8
law "I like listening to you."
n "Vincent growled and put his hand on Lawrence's knee, gripping the soft sweatpant cloth."
n "He rubbed his face into Lawrence's pants and Lawrence made a soft sound of worry."
n "He froze for a moment but he placed his hand on Vincent's head."
law "Some things..."
$ lexp = 23
law "Are better left forgotten."
law "Maybe this is one of them."
n "Lawrence said, running his fingers through Vincent's hair."
$ lexp = 12
n "Lawrence's eyes locked on the soft black hair and the back of Vincent's head."
n "Lawrence gripped Vincent's shoulder as he felt the larger man grow still."
vincent "You might be right."
n "Vincent said his usual confident tone, shaken."
n "Lawrence leaned back against Vincent's window, letting the sun warm his back."
n "Vincent placed his hand over Lawrence's gripping it lightly."
law "Plus, there's nothing wrong with the way you are now."
show cg_lawrence_Vincent_special with dissolve
n "Lawrence said, his eyes closed, speaking as if he was musing to himself."
n "Vincent's eye widened and he closed it feeling tears rolling down his face."
n "He huffed trying to keep his emotions to himself."
vincent "Thank you, Lawrence."
stop music
$ renpy.transition(fade)
call screen extra



label cain_rire_special:
show cg_cainspecial with fade
$ cain_hideheart = False
$ cain_name = "Cain"
$ cain_love = 0
play music "cain/cain_sexy.mp3"
n "Cain stirred his drink."
cain "I'm glad you were able to meet me, Demon King."
cain "I have a special interest in speaking with you."
n "Rire cocked an eyebrow over his glasses but kept his composure."
n "He couldn't show any weakness with this fallen angel."
n "Cain chuckled and leaned back."
cain "You can relax you know."
cain "I'm not here to start anything."
rire "Hm?"
n "Rire mused and touched the handle of his cup."
rire "What is it that you called me for?"
n "Rire asked keeping his sharp smile."
n "Cain looked at his drink for a moment and then back up at Rire."
cain "Do you know a demon named Sano Kojima, by chance?"
n "Cain said, his tone still smooth and relaxed, but there was a sharp annoyed tone to it."
n "Rire thought about what he would say but just kept his poker face on."
rire "Hm? Of course."
rire "He's a very good little snake."
n "Rire taunted running his finger over the lip of his cup."
n "Cain seized up for a fraction of a moment and tilted his head to the side, his gaze steady on Rire."
cain "I'm going to have to ask you to stop seeing him."
n "Cain said with a fake cheerful tone that made Rire cringe internally."
rire "And if I refuse?"
cain "My brother is a priest."
cain ".D is very cute. I could see why you would want his soul, Rire."
n "Rire's smile broke into a frown."
rire "Tch."
show cg_cainspecial2 with dissolve
n "His tentacles slipping from his back."
n "Cain's eyes drifted over to them."
cain "Do you REALLY think you can face off against me?"
n "Cain's eyes shifted to black."
cain "I'd like to see you try."
stop music
$ renpy.transition(fade)
call screen extra
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
