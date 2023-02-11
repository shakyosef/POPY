from pypot.creatures import PoppyTorso
import Settings as s
import time
import threading
import random
from GUI2 import StartPage, TryAgainPage, BlankPage, GoodbyePage, ExercisePage
from CognitiveGame1 import GameOneStart
from CognitiveGame2 import GameTwoStart
from CognitiveGame3 import GameThreeStart
import Excel


class Poppy(threading.Thread):



    def __init__(self):
        threading.Thread.__init__(self)
        self.poppy = PoppyTorso()  # for real robot
        # self.poppy = PoppyTorso(simulator='vrep')  # for simulator
        print("init robot")
        for m in self.poppy.motors:  # motors need to be initialized, False=stiff, True=loose
            m.compliant = False
        self.init_robot()

    def run(self):
        print("hello wave, introduction")
        self.run_exercise(self.hello_waving, "hello")
        time.sleep(1)
        s.str_to_say = 'ready wave'
        s.screen.switch_frame(StartPage)
        while (not s.waved): # wait for participant to wave
            continue
        time.sleep(1)
        s.screen.switch_frame(BlankPage)
        print("Let's start!")
        s.str_to_say='lets start'
        time.sleep(2)
        chosen_exercises, cog_screen_name = self.choose_exercises_and_game()
        cog_screen_name = GameOneStart  # FOR EXPERIMENTS - USING THE SAME COGNITIVE GAME
        self.run_workout(chosen_exercises, cog_screen_name)  # Running function
        # self.test_for_exercise() #Testing function


    def choose_exercises_and_game(self):
        t = 1
        ## 3, 5
        foult = 1

        raise_arms_horizontally_f_1
    # 1 for interaction 2 for program
        exercise_names=[]
        if t == 1:
            if foult == 1:
                exercise_names = [self.raise_arms_horizontally_f_1, self.raise_arms_horizontally, self.bend_elbows, self.raise_arms_forward_static, self.raise_arms_bend_elbows ]
            if foult == 2 :
                exercise_names = [self.raise_arms_horizontally_f_2, self.bend_elbows,
                                  self.raise_arms_horizontally_separate_f, self.raise_arms_forward_static,
                                  self.raise_arms_bend_elbows]
        if t == 3:
            if foult == 1:
                exercise_names = [self.raise_arms_horizontally_f_1,  self.bend_elbows,self.raise_arms_horizontally_separate_f, self.raise_arms_forward_static,self.raise_arms_bend_elbows ]
            if foult == 2 :
                exercise_names = [self.raise_arms_horizontally_f_2,  self.bend_elbows,self.raise_arms_horizontally_separate_f, self.raise_arms_forward_static,self.raise_arms_bend_elbows ]
        if t == 5:
            if foult == 1:
                exercise_names = [self.raise_arms_horizontally_f_1, self.bend_elbows, self.raise_arms_forward_static, self.raise_arms_bend_elbows, self.raise_arms_horizontally_separate_f]
            if foult == 2 :
                exercise_names = [self.raise_arms_horizontally_f_2, self.bend_elbows,
                                  self.raise_arms_horizontally_separate_f, self.raise_arms_forward_static,
                                  self.raise_arms_bend_elbows]





        cog_game_number = random.randint(1, 2)  # choose cognitive game from the 3 existing
        print("Cognitive game ", cog_game_number)
        if cog_game_number == 1:
            cog_screen_name = GameOneStart
        else:
            if cog_game_number == 2:
                cog_screen_name = GameTwoStart
            else:
                cog_screen_name = GameThreeStart
        return exercise_names, cog_screen_name

    def run_workout(self, chosen_exercises, cog_screen_name):
        # RUN WORKOUT
        count = 0
        print("POPPY: Exercises - Starting Workout")
        for e in chosen_exercises:
            count = count + 1
            if e.amount == 2:
                self.run_exercise(e, "")
            else:
                print ("POPPY:", getattr(e, "instructions"))
                self.run_exercise_and_repeat(e, getattr(e, "instructions"))
            if (count == s.exercies_amount/2 and s.with_cog):
                s.str_to_say="come to the screen"
                time.sleep(2)
                s.cogGame = True
                s.cogGameCount = 0
                s.screen.switch_frame(cog_screen_name)
                while (s.cogGame):
                    continue
                s.str_to_say = "continue exercises"  # go back from the robot and screen to continue the session
                time.sleep(7)
            print("POPPY: Write To Excel", s.ex_list)
        self.finish_workout()

    def test_for_exercise(self):
    # For testing exercises separtly, not as part of the workout

        # self.run_exercise(self.raise_arms_horizontally, "raise arms horizontally")
        # self.run_exercise(self.raise_arms_horizontally_separate, "")
        # self.run_exercise(self.raise_arms_horiz_turn, "raise arms horizontally turn hands")
        # self.run_exercise(self.bend_elbows, "bend elbows")
        # self.run_exercise(self.raise_arms_forward_separate, "")
        # self.run_exercise(self.raise_arms_forward, "raise arms forward")
        # self.run_exercise(self.raise_arms_forward_static, "raise arms forward static")
        # self.run_exercise(self.raise_arms_forward_turn, "raise arms forward turn hands")
        # self.run_exercise(self.raise_arms_bend_elbows, "raise arms bend elbows")
        # self.run_exercise(self.open_arms_and_forward, "open arms and move forward")
        # self.run_exercise(self.open_and_close_arms_90, "open and close arms 90")
        # self.run_exercise(self.raise_arms_90_and_up, "raise arms 90 and up")

        # # self.run_exercise(self.open_hands_and_raise_up, "raise arms forward")
        # self.run_exercise(self.raise_arms_and_lean, "")
        # self.run_exercise_and_repeat(self.raise_hands_and_fold_backward, "")

        self.finish_workout()

    def init_robot(self):
        for m in self.poppy.motors:
            if not  m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
                m.goto_position(0, 1, wait=True)
        self.poppy.head_y.goto_position(-20,1,wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    # run exercise
    def run_exercise(self, exercise, exercise_name):
        s.success_exercise = False
        s.req_exercise = exercise.__name__
        print ("POPPY: ", s.req_exercise)
        print("POPPY: instruction for exercise")
        s.str_to_say = exercise_name
        time.sleep(5)
        exercise()
        if exercise_name != "hello":
            s.req_exercise = ""
            time.sleep(3)

    def repeat_exercise(self):
        print("You need to do the exercise 8 times. if you want to try again please raise your right hand")
        # s.tts.say='feedback 8 times'
        s.str_to_say='try again'
        s.waved = False
        self.time1 = time.time()
        self.time2 = 0
        s.req_exercise = "hello_waving"
        time.sleep(1)
        s.screen.switch_frame(TryAgainPage)
        time.sleep(5)
        while not s.waved and (self.time2 - self.time1 < 15) and not s.clickedTryAgain:
            self.time2 = time.time()
            continue
        s.req_exercise = ""
        s.clickedTryAgain = False
        time.sleep(1)
        if s.waved:
            s.screen.switch_frame(ExercisePage)
            return True
        else:
            return False

    def run_exercise_and_repeat(self, exercise, exercise_name):
        time.sleep(1)
        s.screen.switch_frame(ExercisePage)
        self.run_exercise(exercise, exercise_name)
        if not s.success_exercise:
           if self.repeat_exercise():
                self.run_exercise(exercise, exercise_name)
        print (s.waved)

    #TODO def finish_exercise(self)

    def finish_workout(self):
        time.sleep(1)
        s.screen.switch_frame(GoodbyePage)
        s.str_to_say = 'goodbye'
        time.sleep(5)
        Excel.wf_exercise()
        Excel.close_workbook()
        # for m in self.poppy.motors:  # need to be initialized for the real robot. False=stiff, True=loose
        #   m.compliant = True
        s.finish_workout = True
        s.screen.quit()
        print ("finish workout")

    # define attributes for a function
    def func_attributes(**attrs):
        def attributes(f):
            for k, v in attrs.items():
                setattr(f, k, v)
            return f
        return attributes

    #-----------------------Exercises---------------------------#
    def hello_waving(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-80, 1.5, wait=False)
        for i in range(3):
            self.poppy.r_arm[3].goto_position(-35, 0.6, wait=True)
            self.poppy.r_arm[3].goto_position(35, 0.6, wait=True)
        self.finish_waving()

    def finish_waving(self):
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)

    # EX1 - Right Arm Horizontally and Left arm Horizontally
    @func_attributes(number=1 ,amount=2, instructions="raise arms horizontally separate")
    def raise_arms_horizontally_separate(self):
        self.run_exercise_and_repeat(self.raise_right_arm_horiz, "raise right arm horizontally")
        self.run_exercise_and_repeat(self.raise_left_arm_horiz, "raise left arm horizontally")




    @func_attributes(instructions="raise left arm horizontally")
    def raise_left_arm_horiz(self):
        for i in range(s.rep):
            right_hand_up = [self.poppy.r_shoulder_x.goto_position(-90, 1.7, wait=False),
                             self.poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            right_hand_down = [self.poppy.r_shoulder_x.goto_position(0, 1.7, wait=False),
                               self.poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break

    @func_attributes(instructions="raise right arm horizontally")
    def raise_right_arm_horiz(self):
        for i in range(s.rep):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.7, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.7, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break

    # EX2 - Two Arms Horizontally
    @func_attributes(number=2, amount=1, instructions="raise arms horizontally")
    def raise_arms_horizontally(self):
        for i in range(s.rep):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                          self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break


    # EX2 - Two Arms Horizontally with foulttttt!!!!!
    @func_attributes(number=2, amount=1, instructions="raise arms horizontally")
    def raise_arms_horizontally_f_1(self):
        for i in range(s.rep_f):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                          self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break
    @func_attributes(number=2, amount=1, instructions="raise arms horizontally")
    def raise_arms_horizontally_f_2(self):
        for i in range(s.rep):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)

            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                          self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            if i == 5:
                time.sleep(40)
            time.sleep(2)
            if (s.success_exercise):
                break



    # EX3 - Bend Elbows
    @func_attributes(number=3, amount=1, instructions="bend elbows")
    def bend_elbows(self):
        for i in range(s.rep):
            self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
            self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
            self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
            time.sleep(0.5)
            if (s.success_exercise):
                break

    # EX4 - Static hands forward
    @func_attributes(number=4, amount=1, instructions="raise arms forward static")
    def raise_arms_forward_static(self):
        self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
        time.sleep(s.rep)
        time.sleep(10)
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)

    # EX5 - Raise Arms Bend Elbows
    @func_attributes(number=5, amount=1, instructions="raise arms bend elbows")
    def raise_arms_bend_elbows(self):
        for i in range(s.rep):
            l_hand = [self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.l_arm_z.goto_position(-90, 2, wait=False),
                      self.poppy.l_shoulder_x.goto_position(50, 2, wait=False),
                      self.poppy.l_elbow_y.goto_position(-50, 2, wait=False)]
            r_hand = [self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.r_arm_z.goto_position(90, 2, wait=False),
                      self.poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
                      self.poppy.r_elbow_y.goto_position(-50, 2, wait=False)]
            time.sleep(3)
            self.open_hands_aside_move()
            if (s.success_exercise):
                break
        time.sleep(2)
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)


    def open_hands_aside_move(self):
        self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)



    def raise_left_arm_forward(self):
        for i in range(s.rep):
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1.2)
            if (s.success_exercise):
                break

    def raise_right_arm_forward(self):
        for i in range(s.rep):
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1.2)
            if (s.success_exercise):
                break

    # EX9 - Raise arms 90 and up
    @func_attributes(number=9, amount=1, instructions="raise arms 90 and up")
    def raise_arms_90_and_up(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        for i in range(s.rep):
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
            time.sleep(1)
            self.poppy.r_shoulder_x.goto_position(-150, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(150, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(60, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(60, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break

    # EX10 raise arms and lean
    @func_attributes(number=10, amount=2, instructions="raise arms and lean")
    def raise_arms_and_lean(self):
        self.run_exercise_and_repeat(self.raise_right_arm_and_lean,"")
        self.run_exercise_and_repeat(self.raise_left_arm_and_lean, "")

    @func_attributes(instructions="raise right arm and lean")
    def raise_right_arm_and_lean(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(30, 1.5, wait=False)
        self.poppy.bust_x.goto_position(20, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=True)
        self.poppy.r_shoulder_x.goto_position(-30, 1.5, wait=False)
        time.sleep(s.rep)
        self.poppy.bust_x.goto_position(0, 1.5, wait=True)
        self.poppy.bust_y.goto_position(0, 1, wait=True)

    @func_attributes(instructions="raise left arm and lean")
    def raise_left_arm_and_lean(self):
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(30, 1.5, wait=False)
        self.poppy.bust_x.goto_position(-20, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(30, 1.5, wait=False)
        time.sleep(s.rep)
        self.poppy.bust_x.goto_position(0, 1.5, wait=True)
        self.poppy.bust_y.goto_position(0, 1, wait=True)


    # EX12 Raise hands and fold backward
    @func_attributes(number=12, amount=1, instructions="raise hands and fold backward")
    def raise_hands_and_fold_backward(self):
        self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
        for i in range(s.rep):
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
            time.sleep(1.5)
            self.poppy.l_elbow_y.goto_position(-20, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
            time.sleep(1.5)
            if (s.success_exercise):
                break

    # EX13 open hands and raise up
    @func_attributes(number=13, amount=1, instructions="open hands and raise up")
    def open_hands_and_raise_up(self):
        for i in range(s.rep):
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
            time.sleep(1.5)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(10, 1, wait=False)
            self.poppy.r_shoulder_x.goto_position(-10, 1, wait=False)
            self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=True)
            time.sleep(1.5)
            if (s.success_exercise):
                break

    # def strech(self):
    #     self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
    #     self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)
    #     time.sleep(2)
    #     self.poppy.r_shoulder_x.goto_position(80, 1.5, wait=True)
    #     self.poppy.r_elbow_y.goto_position(-15, 1.5, wait=True)
    #     self.poppy.r_shoulder_y.goto_position(-110, 1.5, wait=True)
    #
    # def trying(self): #hands in x?
    #         self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
    #         self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
    #         self.poppy.l_shoulder_x.goto_position(45, 1.5, wait=False)
    #         self.poppy.r_shoulder_x.goto_position(-45, 1.5, wait=True)
    #         time.sleep(2)
    #         self.poppy.l_shoulder_y.goto_position(-20, 1.5, wait=False)
    #         self.poppy.l_shoulder_x.goto_position(-25, 1.5, wait=False)
    #         self.poppy.l_elbow_y.goto_position(-40, 1.5, wait=False)
    #         self.poppy.l_arm_z.goto_position(-90, 1.5, wait=True)
    #         time.sleep(1)
    #         self.poppy.r_shoulder_y.goto_position(-60, 1.5, wait=True)
    #         self.poppy.r_shoulder_x.goto_position(15, 1.5, wait=True)
    #         self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=True)
    #         self.poppy.r_arm_z.goto_position(75, 1.5, wait=True)


    # if __name__ == '__main__':
