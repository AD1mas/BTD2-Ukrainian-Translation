








init -1 python hide:



    config.screen_width = 800
    config.screen_height = 600




    config.window_title = u"Тебе тут трахнуть та згвалтують 2: Свіжа кров"



    config.name = "Тебе тут трахнуть та згвалтують 2: Свіжа кров"
    config.version = "1.0"










    theme.tv(
        
        

        
        widget = "#444",

        
        widget_hover = "#760000",

        
        widget_text = "#fff",

        
        
        widget_selected = "#eee",

        
        disabled = "#222",

        
        disabled_text = "#555",

        
        label = "#ffffff",

        
        frame = "#222",

        
        
        
        mm_root = "titlecard.jpg",

        
        
        
        gm_root = "menubg.jpg",

        
        
        rounded_window = False,

        
        
        
        )










    style.window.background = "dialoguebox.png"



    config.windows_icon = "icon.png"





    style.window.left_padding = 20
    style.window.right_padding = 35
    style.window.top_padding = 86
    style.window.bottom_padding = 0




    style.window.yminimum = 223


init python:
    style.say_dialogue.drop_shadow = (1, 1)
    style.say_dialogue.ypos = 10
    style.say_dialogue.xpos = 10
    style.say_thought.drop_shadow = (1, 1)
    style.say_thought.ypos = 10
    style.say_thought.xpos = 10
    style.input.ypos = 15
    style.input.xpos = 10

















    style.mm_menu_frame.xpos = 0
    style.mm_menu_frame.xanchor = 0
    style.mm_menu_frame.ypos = 0
    style.mm_menu_frame.yanchor = 0
    style.menu_choice.size = 18
    style.menu_choice_button.yminimum = 50
    style.menu_choice_button.background = Frame("texture_grunge.png",0,9)
    style.menu_choice_button.hover_background = Frame("texture_grunge_lighter.png",28,9)








    style.default.font = "verdana.ttf"



    style.default.size = 18











    config.has_sound = True



    config.has_music = True



    config.has_voice = False



    style.button.activate_sound = "click.mp3"
    style.imagemap.activate_sound = "click.mp3"












    config.main_menu_music = "menu.mp3"












    config.help = "README.html"






    config.enter_transition = None


    config.exit_transition = None


    config.intra_transition = None


    config.main_game_transition = None


    config.game_main_transition = None


    config.end_splash_transition = fade


    config.end_game_transition = fade


    config.after_load_transition = None


    config.window_show_transition = None


    config.window_hide_transition = None


    config.adv_nvl_transition = dissolve


    config.nvl_adv_transition = dissolve


    config.enter_yesno_transition = None


    config.exit_yesno_transition = None


    config.enter_replay_transition = None


    config.exit_replay_transition = None


    config.say_attribute_transition = None





python early:
    config.save_directory = "Boyfriend to Death 2"

init -1 python hide:









    config.default_fullscreen = False



    config.default_text_cps = 0



    config.default_afm_time = 10
    config.developer = False







init python:




    build.directory_name = "Boyfriend_To_Death_2_Fresh_Blood"




    build.executable_name = "Boyfriend To Death 2: Fresh Blood"



    build.include_update = False





























    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('game/**.png', 'archive')
    build.classify('game/**.jpg', 'archive')
    build.classify('game/**.mp3', 'archive')
    build.classify('game/**.ogg', 'archive')
    build.classify('game/**.wav', 'archive')
    build.classify('game/**.rpy', 'archive')
    build.classify('game/**.rpt', 'archive')
    build.classify('game/**.ttf', 'archive')
    build.classify('game/**.rpa', 'archive')










    build.documentation('*.html')
    build.documentation('*.txt')
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
