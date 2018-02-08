#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Elvis Yu-Jing Lin <elvisyjlin@gmail.com>
# Licensed under the MIT License - https://opensource.org/licenses/MIT

"""lf2gym.py: LF2-Gym, a maker of the OpenAI-Gym-like environment for Little Fighter 2."""

# # Make it easy to import packages under lib/gym/.
# import sys
# sys.path.append('lib/gym')

# Make these enums available from lf2gym.
# E.g. lf2gym.Character.Firen
# E.g. lf2gym.C.Firen
from lib.gym.config import WebDriver, Character, Difficulty, Background
W, C, D, B = WebDriver, Character, Difficulty, Background

# Make function for LF2 environment.
def make(lf2gymPath='.', ip='127.0.0.1', port=8000, startServer=False, driverType=WebDriver.PhantomJS, 
    wrap='skip4', characters=[Character.Davis, Character.Dennis], difficulty=Difficulty.Dumbass, 
    background=Background.HK_Coliseum, action_options=['Basic', 'AJD', 'Full Combos'], 
    versusPlayer=False, duel=False, rewardList=['hp'], localDriver=True, canvasSize=(550, 794), debug=False):

    from lib.gym.lf2environment import LF2Environment
    from lib.gym.lf2wrapper import LF2Wrapper, LF2SkipNWrapper
    from lib.gym.lf2exception import lf2raise
    from time import sleep

    if startServer:
        start_server(ip=ip, port=port, path=lf2gymPath, block=False)
        sleep(2)
    
    env = LF2Environment(lf2gymPath=lf2gymPath, ip=ip, port=port, driverType=driverType, 
        characters=characters, difficulty=difficulty, background=background, 
        versusPlayer=versusPlayer, duel=duel, rewardList=rewardList, localDriver=localDriver, 
        canvasSize=canvasSize, debug=debug)

    if wrap is not None:
        if wrap == '4':
            print('Wrapping env with LF2Wrapper...')
            env = LF2Wrapper(env)
        elif wrap[:-1] == 'skip':
            num_frame = int(wrap[-1])
            print('Wrapping env with LF2SkipNWrapper, N = %d...' % num_frame)
            env = LF2SkipNWrapper(env, num_frame, 4, characters[0], action_options, debug)
        else:
            lf2raise('Not supported wrap method [%s].' % (wrap))

    return env

# Server starting function.
def start_server(ip='', port=8000, path='.', block=True):

    import lib.gym.lf2server as lf2server

    server = lf2server.LF2Server(path=path, ip=ip, port=port)
    server.start()

    if block:
        from time import sleep
        while True:
            sleep(60)
