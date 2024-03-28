from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .frouge import FlammeRougeEnv

from nicegui import ui
import threading

from .classes import *

STOP_STEP_MODE = True

model_data = {
    "game_env": None
}



def _get_player_color(n: int):
    if n == 1:
        return "red"
    if n == 2:
        return "blue"
    if n == 3:
        return "green"
    if n == 4:
        return "orange"
    if n == 5:
        return "purple"
    
def _get_rider_color(board, c, r):
    r = _get_rider(board, c, r)
    if r != "-":
        return _get_player_color(int(r[0]))
    return ""

def _get_rider(board, c, r):
    rider = board.get_cell_display(c,r)
    if rider == "":
        rider = "-"
    return rider

def _on_select_sprinteur_deck():
    action = model_data["game_env"].ACTION_SELECT_SPRINTEUR_DECK
    model_data["game_env"]._interactive_action_result = action

def _on_select_rouleur_deck():
    action = model_data["game_env"].ACTION_SELECT_ROULEUR_DECK
    model_data["game_env"]._interactive_action_result = action

def _on_card_selected(card):
    action = ALL_CARDS.index(card)
    model_data["game_env"]._interactive_action_result = action

def _on_click_cell_listener(c, r):
    if model_data["game_env"].phase == 0:
        if model_data["game_env"].board.get_cell(c,r) == CS:
            if model_data["game_env"].board.get_cell_display(c,r) == "":
                action = c*3 + r + len(ALL_CARDS) + 2
                model_data["game_env"]._interactive_action_result = action

@ui.refreshable
def _gui_board(board: Board):
    if board != None:
        cell_per_line = 40
        for i in range(3):
            with ui.grid(rows=3, columns=cell_per_line).classes("gap-0").style("width: 100%"):
                for r in range(3):
                    for c in range(cell_per_line):
                        cell = board.get_cell(c+cell_per_line*i,r)
                        if cell == CV:
                            bg_c = "transparent"
                        if cell == CC: # climb
                            bg_c = "red" # light red
                        if cell == CD: # descent
                            bg_c = "blue" # blue
                        if cell == CP: # paved
                            bg_c = "yellow" # yellow
                        if cell == CSU: # supply cell
                            bg_c = "cyan" # cyan
                        if cell == CS: # start
                            bg_c = "grey-6" # gray
                        if cell == CF: # finish
                            bg_c = "grey-6" # gray
                        if cell == CN: #normal
                            bg_c = "grey-4" # light grey
                        rider = _get_rider(board,c+cell_per_line*i,r)
                        style_border = "border-top: 3px solid white; padding-top: 3px;" if r == 0 else "border-top: 2px dashed white; padding-top: 2px;"
                        if cell != CV and (r == 2 or board.get_cell(c+cell_per_line*i,r+1) == CV):
                            style_border += " border-bottom: 3px solid white; padding-bottom: 3px;"
                        if model_data["game_env"].phase == 0 and cell == CS and rider == "-":
                            ui.button("-", on_click=lambda x=(c+cell_per_line*i,r): _on_click_cell_listener(x[0],x[1])).style("width: 100%;")
                        else:
                            if rider.endswith("r"):
                                _element_rouleur(_get_rider_color(board,c+cell_per_line*i,r)).style(f'width: 100%; {style_border}').tailwind.display("flex").background_color(bg_c)
                            elif rider.endswith("s"):
                                _element_sprinteur(_get_rider_color(board,c+cell_per_line*i,r)).style(f'width: 100%; {style_border}').tailwind.display("flex").background_color(bg_c)
                            else:
                                ui.html("<div>&nbsp;</div>").style(f'width: 100%; {style_border}').tailwind.background_color(bg_c).border_color("black")
#fix : Traceback (most recent call last):
#  File "/app/environments/frouge/frouge/envs/render_web.py", line 99, in _gui_board
#    ui.html("<div>&nbsp;</div>").style(f'width: 100%; {style_border}').tailwind.background_color(bg_c).border_color("black")
#  File "/home/selfplay/.local/lib/python3.10/site-packages/nicegui/elements/html.py", line 17, in __init__
#    super().__init__(tag=tag, content=content)
#  File "/home/selfplay/.local/lib/python3.10/site-packages/nicegui/elements/mixins/content_element.py", line 15, in __init__
#    super().__init__(**kwargs)
# File "/home/selfplay/.local/lib/python3.10/site-packages/nicegui/element.py", line 75, in __init__
#    self.client = _client or context.get_client()
#  File "/home/selfplay/.local/lib/python3.10/site-packages/nicegui/context.py", line 28, in get_client
#    return get_slot().parent.client
#  File "/home/selfplay/.local/lib/python3.10/site-packages/nicegui/context.py", line 20, in get_slot
#    raise RuntimeError('The current slot cannot be determined because the slot stack for this task is empty.\n'
#RuntimeError: The current slot cannot be determined because the slot stack for this task is empty.
#This may happen if you try to create UI from a background task.
#To fix this, enter the target slot explicitly using `with container_element:`.
            #blank line
            ui.separator()

@ui.refreshable
def _gui_players(env: FlammeRougeEnv):
    with ui.row():
        ui.label("Last played cards")
        with ui.grid(columns=6):
            ui.label("-")
            for p in env.board.players:
                ui.label(f"Player {p.name}").tailwind.text_color(_get_player_color(p.n))
            ui.label("Rouleur")
            for p in env.board.players:
                card = env.last_played_cards[(p,"r")]
                penalty = str(p.n)+"r" in env.penalty
                if card != None:
                    with ui.row().classes("border"):
                        ui.label(card.name).tailwind.text_color(_get_player_color(p.n))
                        if penalty:
                            ui.label("X").tailwind.background_color("red-10")
                else:
                    ui.label("-")
            ui.label("Sprinter")
            for p in env.board.players:
                card = env.last_played_cards[(p,"s")]
                penalty = str(p.n)+"s" in env.penalty
                if card != None:
                    with ui.row().classes("border"):
                        ui.label(card.name).tailwind.text_color(_get_player_color(p.n))
                        if penalty:
                            ui.label("X").tailwind.background_color("red-10")
                else:
                    ui.label("-")
    ui.label(f"Player {env.score_game().index(max(env.score_game()))+1} WIN !!!!").bind_visibility_from(env, "done").classes("text-h6").tailwind.text_color("red")

@ui.refreshable
def _gui_human_actions(env: FlammeRougeEnv):
    with ui.row().bind_visibility_from(env, '_interactive_action_on'):
        with ui.column():
            ui.label("").bind_text_from(env,"current_player_num",backward=lambda x: f"Human player {x+1} turn")
            ui.label("").bind_visibility_from(env,"phase",backward=lambda x: x == 0).bind_text_from(env.current_player.s_position,"col",backward=lambda x:  "Place your Sprinteur (click on a starting cell)" if x == -1 else "Place your Rouleur (click on a starting cell)")
            with ui.row().bind_visibility_from(env,"phase",backward=lambda p: p==1):
                with ui.button("Choose Sprinter deck", on_click=_on_select_sprinteur_deck):
                    _element_sprinteur(_get_player_color(env.current_player_num+1)).style("width: 100%;")
                with ui.button("Choose Rouleur deck", on_click=_on_select_rouleur_deck):
                    _element_rouleur(_get_player_color(env.current_player_num+1)).style("width: 100%;")
            with ui.row().bind_visibility_from(env,"phase",backward=lambda p: p==2):
                if env.current_player.hand_order[env.hand_number] == 'r':
                    ui.label("Choose Rouleur card")
                    hand_cards = env.current_player.r_hand
                else:
                    ui.label("Choose Sprinter card")
                    hand_cards = env.current_player.s_hand
                for c in hand_cards.cards:
                    #TODO : change color button to red for penalty card
                    with ui.button(on_click=lambda c=c: _on_card_selected(c)).classes("text-h4 q-px-md"):
                        with ui.column():
                            ui.label(f"{c.value}").classes("text-h4 q-px-lg")
                            if env.current_player.hand_order[env.hand_number] == 'r':
                                _element_rouleur(_get_player_color(env.current_player_num+1)).style("width: 100%;")
                            else:
                                _element_sprinteur(_get_player_color(env.current_player_num+1)).style("width: 100%;")
    

def render_web(env: FlammeRougeEnv):

    if env._web_thread == None:
        #TODO : to remove
        global model_data
        model_data["game_env"] = env

        with ui.row().classes("bg-green-1 q-py-md").style("width: 100%;"):
            _gui_board(env.board)
        with ui.row():
            ui.label("").bind_text_from(env, "turns_taken", backward=lambda x: f"Turn : {x}")
            ui.label("").bind_text_from(env, "phase", backward=lambda x: "Rider placement" if x == 0 else "Deck choice" if x == 1 else "Card choice")
        _gui_players(env)
        _gui_human_actions(env)

        env._web_thread = threading.Thread(target=lambda: ui.run(reload=False))
        env._web_thread.daemon = True
        env._web_thread.start()
    else:
        _gui_board.refresh(env.board)
        _gui_human_actions.refresh(env)
        _gui_players.refresh(env)
    
@ui.refreshable
def _element_rouleur(color: str):
    content = f'''
        <svg viewBox="0 0 340 285" xmlns="http://www.w3.org/2000/svg">
 <g label="Camada 1" id="imagebot_3">
  <title>Camada 1</title>
  <g transform="translate(1.25 0) matrix(1 0 0 1 1.25 1.25)" id="imagebot_10">
   <path label="Camada 1" fill="{color}" transform="translate(0 1.25) matrix(1.6571 -0.11142 0.11142 1.6571 -507.444 -29.551)" d="M409.38,76.812C409.20686,76.8195 408.73951,76.85331 408.5675,76.8745S407.92478,76.96473 407.755,76.9995S407.10899,77.13887 406.9425,77.187S406.3234,77.40706 406.16125,77.46825S405.53678,77.70689 405.38,77.78075S404.81168,78.06969 404.66125,78.15575S404.08562,78.49552 403.9425,78.59325S403.42117,78.98448 403.28625,79.09325L363.59825,111.21825C363.40648,111.3726 362.89643,111.85579 362.72325,112.03075S362.09438,112.71241 361.942,112.90575S361.38415,113.66524 361.2545,113.8745S360.79727,114.68322 360.692,114.9057C360.58673,115.12823 360.33405,115.76649 360.2545,115.9995C360.175,116.23246 359.99482,116.88406 359.942,117.1245C359.8892,117.36494 359.77992,118.0359 359.7545,118.2807C359.7291,118.52555 359.6897,119.22204 359.692,119.4682C359.694,119.71436 359.7245,120.41137 359.7545,120.6557S359.91594,121.57255 359.97325,121.8119C360.03055,122.0513 360.2331,122.70547 360.317,122.9369S360.67633,123.81013 360.78575,124.0307C360.89517,124.25122 361.24595,124.8239 361.3795,125.0307S361.91102,125.809 362.067,125.99945S362.67183,126.70277 362.84825,126.87445S363.55987,127.47372 363.7545,127.62445L389.5665,147.71845L384.5665,183.40645L384.5665,183.46895C384.5266,183.71311 384.45689,184.26257 384.4415,184.46895C384.4252,184.68805 384.4045,185.28057 384.4102,185.50015C384.4162,185.71978 384.4762,186.34471 384.5039,186.56265C384.5317,186.78059 384.64189,187.37985 384.6914,187.59385C384.7409,187.8079 384.90189,188.38585 384.97265,188.59385C385.04345,188.80185 385.28761,189.39401 385.3789,189.59385C385.4702,189.79369 385.73676,190.31044 385.84765,190.5001S386.28077,191.22878 386.41015,191.40635S386.95109,192.05517 387.09765,192.21885S387.65415,192.82071 387.8164,192.96885S388.45259,193.494 388.6289,193.6251S389.31532,194.10612 389.5039,194.21885S390.24245,194.62563 390.4414,194.71885C390.64035,194.81205 391.20285,195.02108 391.41015,195.09385C391.61745,195.16665 392.19659,195.35476 392.41015,195.40635C392.62371,195.45795 393.25499,195.56397 393.47265,195.59385C393.69031,195.62375 394.28434,195.67975 394.50385,195.68755C394.72341,195.69555 395.34711,195.67055 395.56635,195.65625C395.78559,195.64205 396.38089,195.59865 396.59755,195.56255C396.81426,195.52635 397.41682,195.37029 397.62875,195.31255C397.84073,195.25485 398.42364,195.07878 398.62875,195.00005C398.83386,194.92135 399.40133,194.66148 399.5975,194.56255C399.79367,194.46365 400.31851,194.18068 400.50375,194.06255S401.2063,193.57368 401.37875,193.43755S402.0021,192.90281 402.16,192.75005S402.73698,192.13665 402.87875,191.9688S403.37955,191.33753 403.50375,191.1563S403.96088,190.44284 404.06625,190.25005S404.41827,189.51494 404.50375,189.31255C404.58925,189.11016 404.81403,188.5225 404.87875,188.31255C404.94345,188.1026 405.08544,187.49669 405.12875,187.28135C405.16825,187.0851 405.2551,186.60025 405.285,186.34385C405.288,186.31885 405.283,186.26955 405.285,186.25015L411.0975,144.62515C411.1369,144.34244 411.189,143.53555 411.1912,143.25015C411.1932,142.96471 411.1637,142.15845 411.1287,141.87515C411.0937,141.59186 410.91912,140.80775 410.84745,140.53135C410.77575,140.25505 410.5483,139.51465 410.4412,139.25015C410.3341,138.98556 409.98814,138.24855 409.84745,138.00015C409.70676,137.75179 409.26934,137.10304 409.09745,136.87515S408.39134,136.04742 408.1912,135.84395C407.99106,135.64043 407.38493,135.11338 407.16,134.9377L386.972,119.2497L409.378,101.0937L431.034,121.3437C431.16647,121.46714 431.54801,121.79417 431.69025,121.9062S432.25796,122.30634 432.409,122.4062C432.56004,122.5061 433.0002,122.7567 433.159,122.8437S433.77479,123.17641 433.94025,123.24995C434.10571,123.32345 434.55051,123.50288 434.7215,123.56245C434.89249,123.62205 435.38991,123.76725 435.56525,123.81245S436.23052,123.96944 436.409,123.99995C436.58748,124.03045 437.10361,124.07805 437.284,124.09365L458.346,125.93745L458.4397,125.93745C458.69659,125.96575 459.2075,126.02585 459.40845,126.03115C459.62868,126.03715 460.22,126.01615 460.43965,125.99985C460.65935,125.98355 461.2852,125.91315 461.50215,125.87485S462.32142,125.68483 462.53335,125.62485C462.74533,125.56485 463.32848,125.36212 463.53335,125.2811C463.73822,125.2001 464.30643,124.94484 464.5021,124.8436S465.22387,124.43278 465.40835,124.31235S466.08069,123.82574 466.2521,123.68735S466.87674,123.1548 467.03335,122.99985S467.61189,122.38853 467.7521,122.2186S468.25471,121.55804 468.3771,121.37485S468.80503,120.66318 468.90835,120.4686S469.2939,119.70384 469.3771,119.49985S469.65861,118.74243 469.72085,118.5311C469.78305,118.31977 469.93021,117.71638 469.97085,117.4999C470.01145,117.28337 470.07722,116.65692 470.09585,116.4374C470.11445,116.21788 470.13065,115.62643 470.12715,115.4062C470.12315,115.18592 470.09035,114.5625 470.06465,114.3437S469.95603,113.52755 469.9084,113.3125C469.8608,113.0974 469.6962,112.49046 469.62715,112.2813C469.55805,112.07209 469.31066,111.51374 469.2209,111.31255C469.1311,111.11136 468.86172,110.53493 468.75215,110.3438S468.3179,109.64793 468.18965,109.4688S467.67904,108.8216 467.5334,108.6563S466.94494,108.0561 466.7834,107.9063S466.14671,107.35157 465.9709,107.2188S465.28418,106.73944 465.0959,106.62505S464.38849,106.2199 464.18965,106.12505C463.99081,106.03025 463.42828,105.79315 463.2209,105.7188C463.01352,105.6445 462.40346,105.45939 462.1897,105.4063C461.97589,105.3532 461.37652,105.25009 461.1585,105.2188C460.95353,105.1894 460.43826,105.1388 460.18975,105.1251L460.12725,105.1251L442.72125,103.5939L417.00225,79.5939C416.84348,79.44553 416.36248,79.0695 416.18975,78.93765S415.53098,78.45792 415.346,78.3439S414.63515,77.93897 414.43975,77.8439S413.67489,77.51282 413.471,77.43765S412.68135,77.17968 412.471,77.12515S411.68573,76.93975 411.471,76.9064S410.62548,76.82448 410.4085,76.81265S409.59433,76.80285 409.3773,76.81265L409.38,76.812z" id="imagebot_7"/>
   <path transform="translate(0 1.25) matrix(1 0 0 1 -235.634 -41.648)" label="Camada 1" fill="{color}" d="M486,70.984C486,87.186 472.866,100.32 456.664,100.32S427.328,87.186 427.328,70.984S440.462,41.648 456.664,41.648S486,54.782 486,70.984zM500.729,183.004C462.656,183.004 431.664,213.996 431.664,252.069S462.656,321.134 500.729,321.134S569.794,290.142 569.794,252.069S538.802,183.004 500.729,183.004zM500.729,196.721C531.394,196.721 556.158,221.404 556.158,252.069S531.395,307.417 500.729,307.417C470.064,307.417 445.381,282.734 445.381,252.069S470.064,196.721 500.729,196.721zM305.949,183.001C267.876,183.001 236.884,213.993 236.884,252.066S267.876,321.131 305.949,321.131S375.014,290.139 375.014,252.066S344.022,183.001 305.949,183.001zM305.949,196.718C336.614,196.718 361.378,221.401 361.378,252.066S336.615,307.414 305.949,307.414C275.284,307.414 250.601,282.731 250.601,252.066S275.284,196.718 305.949,196.718z" id="imagebot_6"/>
  </g>
 </g>
</svg>'''
    return ui.html(content)

@ui.refreshable
def _element_sprinteur(color: str):
    content = f'''
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg viewBox="0 0 340 285" xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs1" />
  <sodipodi:namedview
     id="namedview1"
     pagecolor="#ffffff"
     bordercolor="#000000"
     borderopacity="0.25"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:zoom="2.8631579"
     inkscape:cx="170.61581"
     inkscape:cy="148.78676"
     inkscape:window-width="1920"
     inkscape:window-height="1016"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="svg1" />
  <g
     label="Camada 1"
     id="imagebot_3">
    <title
       id="title1">Camada 1</title>
    <g
       transform="translate(1.25 0) matrix(1 0 0 1 1.25 1.25)"
       id="imagebot_10">
      <path
         label="Camada 1"
         fill="{color}"
         d="m 436.6909,93.831018 c -0.13206,-0.11223 -0.49773,-0.40522 -0.63827,-0.50664 -0.14053,-0.10142 -0.53262,-0.37086 -0.68076,-0.46081 -0.14813,-0.09 -0.56845,-0.33707 -0.72326,-0.41498 -0.1548,-0.0779 -0.60358,-0.25961 -0.76409,-0.32499 -0.1605,-0.0654 -0.62016,-0.24963 -0.78534,-0.30208 -0.16518,-0.0524 -0.61319,-0.17457 -0.78201,-0.21375 -0.16882,-0.0392 -0.65311,-0.14227 -0.8245,-0.16792 -0.1714,-0.0257 -0.64829,-0.0676 -0.82118,-0.0796 l -51.34885,2.577002 c -0.24556,-0.01722 -0.94811,-0.0097 -1.19406,8.03e-4 -0.24595,0.01054 -0.92462,0.07222 -1.16781,0.110378 -0.2432,0.03816 -0.92547,0.177582 -1.16282,0.242866 -0.23736,0.06528 -0.88516,0.282097 -1.11363,0.373652 -0.2285,0.09159 -0.84777,0.387784 -1.06453,0.504549 -0.2167,0.116759 -0.79188,0.472029 -0.9941,0.612419 -0.2022,0.1404 -0.73856,0.55808 -0.92365,0.72029 -0.18511,0.16227 -0.68758,0.64618 -0.85328,0.82824 -0.16591,0.18186 -0.61748,0.71368 -0.76162,0.91324 -0.14413,0.19955 -0.50504,0.78205 -0.62577,0.99652 -0.12076,0.2145 -0.41705,0.831903 -0.51289,1.058643 -0.0958,0.22675 -0.33028,0.88463 -0.40003,1.12076 -0.0697,0.2361 -0.2019,0.89454 -0.24459,1.13698 -0.0427,0.24245 -0.13947,0.9321 -0.1546,1.17781 -0.0151,0.24571 -0.0347,0.92697 -0.0221,1.17281 0.0126,0.24584 0.11432,0.92329 0.15454,1.16615 l 5.82912,23.87455 6.31452,46.36433 0.0151,0.0606 c 0.0203,0.24656 0.0854,0.79657 0.12037,1.00056 0.0371,0.21654 0.16024,0.79651 0.21883,1.0082 0.0589,0.21166 0.26815,0.80357 0.34769,1.00836 0.0796,0.20477 0.33139,0.75963 0.43115,0.95532 0.0998,0.19575 0.39565,0.71766 0.51457,0.9024 0.11898,0.18471 0.499,0.70033 0.63588,0.87219 0.1369,0.17182 0.52042,0.60887 0.67386,0.76611 0.15341,0.15727 0.59638,0.6024 0.76484,0.74344 0.16844,0.14107 0.68172,0.49885 0.86345,0.62231 0.18168,0.12355 0.68555,0.44938 0.87872,0.55404 0.19321,0.10457 0.74424,0.35585 0.947,0.44045 0.20275,0.0846 0.78232,0.30088 0.99256,0.3647 0.21022,0.0638 0.81496,0.21624 1.03054,0.25862 0.21557,0.0424 0.81192,0.10926 1.03066,0.12977 0.21875,0.0206 0.82618,0.0631 1.04588,0.0616 0.2197,-0.002 0.85789,-0.0512 1.07632,-0.0748 0.21844,-0.0236 0.80839,-0.1128 1.02328,-0.15827 0.21499,-0.0453 0.81416,-0.22029 1.02345,-0.28715 0.2093,-0.0668 0.77646,-0.25273 0.97798,-0.34013 0.20154,-0.0875 0.74853,-0.38454 0.94022,-0.49179 0.19175,-0.10721 0.71484,-0.41893 0.89484,-0.54489 0.18005,-0.12592 0.66786,-0.51525 0.83431,-0.65865 0.16648,-0.14336 0.60736,-0.5448 0.75856,-0.70419 0.15117,-0.15941 0.56359,-0.64416 0.69803,-0.81793 0.1344,-0.17379 0.4756,-0.66956 0.59194,-0.85592 0.11601,-0.18659 0.41161,-0.73468 0.50867,-0.93177 0.097,-0.19716 0.33341,-0.73358 0.41013,-0.93946 0.0768,-0.20585 0.27117,-0.80279 0.32683,-1.01533 0.0557,-0.21253 0.16393,-0.79839 0.19797,-1.01543 0.034,-0.21707 0.11016,-0.84162 0.12222,-1.06099 0.012,-0.21936 0.003,-0.84163 -0.007,-1.06105 -0.009,-0.19998 -0.042,-0.69145 -0.0749,-0.94748 -0.003,-0.025 -0.0198,-0.0716 -0.0226,-0.0909 l -0.007,-25.09106 c 0.22112,-0.18051 0.80797,-0.73673 1.00365,-0.94451 0.19555,-0.20794 0.72214,-0.81919 0.88911,-1.05072 0.16696,-0.23152 0.57211,-0.92517 0.7075,-1.17658 0.1353,-0.25135 0.47196,-0.9489 0.57328,-1.21567 0.10138,-0.26684 0.34884,-1.04249 0.41458,-1.32029 0.0657,-0.27777 0.1861,-1.0509 0.21501,-1.33488 0.0289,-0.28398 0.0451,-1.08706 0.0367,-1.37234 -0.008,-0.28532 -0.0944,-1.08392 -0.13992,-1.36568 l -13.90924,-23.47353 29.17847,-4.08525 2.27172,27.17051 c 0.0132,0.18059 0.0706,0.67981 0.0987,0.85868 0.0281,0.17886 0.14419,0.67942 0.18704,0.85534 0.0428,0.17595 0.19518,0.659 0.25246,0.83077 0.0573,0.17177 0.2253,0.66267 0.29662,0.8291 0.0713,0.1664 0.27549,0.60041 0.36036,0.76036 0.0849,0.15996 0.35086,0.60466 0.4487,0.75702 0.0978,0.15237 0.38106,0.56747 0.49118,0.7112 0.11014,0.14372 0.45622,0.52957 0.57789,0.66367 l 14.19003,15.67324 0.0687,0.0637 c 0.16912,0.19543 0.50288,0.5869 0.64663,0.72742 0.1574,0.15415 0.60527,0.54082 0.77741,0.67822 0.17218,0.13744 0.67895,0.51137 0.86407,0.6308 0.18512,0.11943 0.72994,0.41774 0.92612,0.51786 0.19623,0.10014 0.76168,0.34801 0.96699,0.4279 0.20529,0.0799 0.7955,0.2791 1.00782,0.33791 0.21231,0.0588 0.80857,0.18954 1.02573,0.22668 0.21716,0.0371 0.82387,0.10035 1.04366,0.11543 0.21978,0.0151 0.82013,0.0342 1.04032,0.0271 0.22019,-0.007 0.83989,-0.0549 1.05824,-0.0841 0.21836,-0.0293 0.81769,-0.1426 1.032,-0.1937 0.2143,-0.0511 0.79768,-0.23086 1.00575,-0.30329 0.20807,-0.0724 0.80271,-0.2986 1.00242,-0.3916 0.19971,-0.093 0.72143,-0.36397 0.91076,-0.4766 0.18931,-0.11267 0.70749,-0.45504 0.88449,-0.58614 0.177,-0.13117 0.65119,-0.54579 0.81411,-0.69409 0.1629,-0.14831 0.57694,-0.57098 0.72412,-0.73484 0.14685,-0.16424 0.5467,-0.64367 0.67663,-0.82158 0.12993,-0.17791 0.4753,-0.6723 0.5866,-0.86237 0.11136,-0.19009 0.40336,-0.74705 0.49495,-0.94737 0.0916,-0.20039 0.28984,-0.77801 0.36083,-0.98657 0.0709,-0.20858 0.26538,-0.81442 0.31499,-1.02907 0.0496,-0.21465 0.15475,-0.80552 0.18251,-1.02407 0.0278,-0.21855 0.0657,-0.82175 0.0713,-1.04199 0.006,-0.22023 -0.0234,-0.84022 -0.04,-1.0599 -0.0166,-0.21968 -0.0897,-0.83968 -0.12829,-1.05658 -0.0386,-0.2169 -0.1776,-0.81843 -0.23787,-1.03033 -0.0603,-0.2119 -0.24323,-0.77809 -0.32453,-0.98284 -0.0813,-0.20471 -0.3326,-0.76106 -0.43411,-0.95659 -0.10154,-0.19549 -0.423,-0.74604 -0.54364,-0.93031 -0.12067,-0.18432 -0.49005,-0.66747 -0.62864,-0.83866 -0.1303,-0.16093 -0.47372,-0.54839 -0.64662,-0.72742 l -0.0458,-0.0425 -11.72182,-12.9581 -2.70107,-32.68288 c -0.0155,-0.21675 -0.11255,-0.81953 -0.14955,-1.03366 -0.037,-0.214129 -0.15685,-0.799699 -0.21495,-1.009079 -0.0581,-0.20939 -0.2459,-0.78027 -0.32453,-0.98284 -0.0786,-0.20257 -0.33572,-0.76284 -0.43411,-0.95659 -0.0984,-0.19376 -0.4036,-0.72609 -0.52076,-0.9091 -0.11716,-0.18301 -0.44974,-0.6699 -0.58451,-0.84036 -0.13478,-0.17046 -0.56428,-0.63498 -0.71534,-0.7912 -0.15105,-0.15621 -0.59032,-0.560783 -0.75612,-0.701173 z"
         id="imagebot_7"
         transform="matrix(1.6571,-0.11142,0.11142,1.6571,-507.444,-28.301)"
         style="stroke-width:1.0001;stroke-dasharray:none"
         sodipodi:nodetypes="csssssssccsssccsccscscssscccccccscsssssssssssccccsssssssssssccccsccsscccccscscsssccccssssssssssssccscscssssssssccssccccssssssscc" />
      <path
         transform="translate(-235.634,-40.398)"
         label="Camada 1"
         fill="{color}"
         d="m 534,120.984 c 0,16.202 -13.134,29.336 -29.336,29.336 -16.202,0 -29.336,-13.134 -29.336,-29.336 0,-16.202 13.134,-29.336 29.336,-29.336 16.202,0 29.336,13.134 29.336,29.336 z m -33.271,62.02 c -38.073,0 -69.065,30.992 -69.065,69.065 0,38.073 30.992,69.065 69.065,69.065 38.073,0 69.065,-30.992 69.065,-69.065 0,-38.073 -30.992,-69.065 -69.065,-69.065 z m 0,13.717 c 30.665,0 55.429,24.683 55.429,55.348 0,30.665 -24.763,55.348 -55.429,55.348 -30.665,0 -55.348,-24.683 -55.348,-55.348 0,-30.665 24.683,-55.348 55.348,-55.348 z m -194.78,-13.72 c -38.073,0 -69.065,30.992 -69.065,69.065 0,38.073 30.992,69.065 69.065,69.065 38.073,0 69.065,-30.992 69.065,-69.065 0,-38.073 -30.992,-69.065 -69.065,-69.065 z m 0,13.717 c 30.665,0 55.429,24.683 55.429,55.348 0,30.665 -24.763,55.348 -55.429,55.348 -30.665,0 -55.348,-24.683 -55.348,-55.348 0,-30.665 24.683,-55.348 55.348,-55.348 z"
         id="imagebot_6"
         sodipodi:nodetypes="sssssssssssssssssssssssss" />
    </g>
  </g>
</svg>'''
    return ui.html(content)

    
