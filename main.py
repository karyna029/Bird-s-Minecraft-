from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from random import *
from math import *
import math
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.craft = self.loader.loadModel("models/Mineways2Skfb_obj/Mineways2Skfb.obj")
        self.craft.reparentTo(self.render)

        textur_1 = self.loader.loadTexture(
            "models/Mineways2Skfb_obj/Mineways2Skfb-RGBA.png")
        self.craft.setTexture(textur_1)

        

        self.craft.setPos(0, 0, 0)
        self.craft.setScale(100, 100, 100)
        self.craft.setHpr(0, 90, 0)


        self.Actor = Actor("models/red-angry-birds-dancing/Salsa Dancing (30).fbx")
        self.Actor.reparentTo(self.render)




        self.Actor.setScale(0.03, 0.03, 0.03)
        self.Actor.setHpr(0, 0, 180) # Rotate to face the correct direction
        textur1 = self.loader.loadTexture("models/red-angry-birds-dancing/RedDiffuse.png")
        self.Actor.setTexture(textur1)
        self.Actor.reparentTo(self.render)
        self.Actor.loop("dancing")
        self.Actor.setPos(0, 0, 85)

        self.move_speed = 40  #
        self.turn_speed = 90

        self.key_map = {"forward": False, "left": False, "right": False, "backward": False, 'up':False, 'down': False, 'rotate+': False, 'rotate-': False}

        self.accept("arrow_up", self.update_key_map, ["rotate+",True])
        self.accept("arrow_up-up", self.update_key_map, ["rotate+", False])

        self.accept("arrow_down", self.update_key_map, ["rotate-", True])
        self.accept("arrow_down-up", self.update_key_map, ["rotate-", False])
        self.accept("arrow_left", self.update_key_map, ["left", True])
        self.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.accept("arrow_right", self.update_key_map, ["right", True])
        self.accept("arrow_right-up", self.update_key_map, ["right", False])
        self.accept("q", self.update_key_map, ["up", True])
        self.accept("q-up", self.update_key_map, ["up", False])
        self.accept("e", self.update_key_map, ["down", True])
        self.accept("e-up", self.update_key_map, ["down", False])

        self.accept("w", self.update_key_map, ["forward", True])
        self.accept("w-up", self.update_key_map, ["forward", False])
        self.accept("s", self.update_key_map, ["backward", True])
        self.accept("s-up", self.update_key_map, ["backward", False])
        self.taskMgr.add(self.update,"update")

        # Mouse Camera

        self.mouse_sensitive = 0.7
        self.angle_p = 0
        self.angle_h = 0
        self.prev_mouse_pos = None
        #self.disableMouse()
        self.accept("mouse1", self.on_mouse_click)
        self.taskMgr.add(self.update_mouse, "update_mouse")

        self.is_jump = False
        self.jump_height = 10
        self.velocity_speed = 0
        self.gravity = 9.8

        self.accept("space", self.jump)

        # NPC
        self.npc_data = []
        self.num_npc = 20
        for i in range(self.num_npc):
            npc = self.loader.loadModel("models/angry-birds-bomb/source/Bomb.obj")
            npc.setHpr(90, 90, 0)
            npc.reparentTo(self.render)
            npc.setScale(1)

            direction = Point3(uniform(0, 100), uniform(0, 100), uniform(50, 100))
            direction.normalize()
            npc.setHpr(0, 90, 0)

            start_pos = Point3(uniform(-100, 100), uniform(-50, 100), uniform(50, 100))
            npc.setPos(start_pos)

            self.npc_data.append({"npc": npc,
                                  "direction": direction
                                  })
        self.taskMgr.add(self.npc_move, "npc_move")

        for i in range(self.num_npc):
            npc = self.loader.loadModel("models/chuck-angry-birds-dancing/Samba Dancing (57).fbx")
            npc.setHpr(90, 90, 0)
            npc.reparentTo(self.render)
            npc.setScale(0.01)

            texture_npc = self.loader.loadTexture("models/chuck-angry-birds-dancing/Chuck_Diffuse.png")
            npc.setTexture(texture_npc)

            direction = Point3(uniform(0, 100), uniform(0, 100), uniform(50, 100))
            direction.normalize()
            npc.setHpr(0, 90, 0)

            start_pos = Point3(uniform(-100, 100), uniform(-50, 100), uniform(50, 100))
            npc.setPos(start_pos)

            self.npc_data.append({"npc": npc,
                                  "direction": direction
                                  })
        self.taskMgr.add(self.npc_move, "npc_move")

    def update_key_map(self, key, value):
        self.key_map[key] = value

    def update(self, task):
        dt = globalClock.getDt()

        # Move the panda based on key inputs
        if self.key_map["forward"]:
            self.Actor.setY(self.Actor, self.move_speed)
        if self.key_map["backward"]:
            self.Actor.setY(self.Actor, -self.move_speed)
        if self.key_map["left"]:
            self.Actor.setH(self.Actor.getH() + self.turn_speed * dt)
        if self.key_map["right"]:
            self.Actor.setH(self.Actor.getH() - self.turn_speed * dt)
        if self.key_map["up"]:
            self.Actor.setZ(self.Actor.getZ() + self.move_speed * dt)
        if self.key_map["down"]:
            self.Actor.setZ(self.Actor.getZ() - self.move_speed * dt)
        if self.key_map["rotate+"]:
            self.Actor.setP(self.Actor.getP() + self.move_speed * dt)
        if self.key_map["rotate-"]:
            self.Actor.setP(self.Actor.getP() - self.turn_speed * dt)
        if self.is_jump:
            self.Actor.setP(self.Actor.getP()+self.velocity_speed*dt)
            self.velocity_speed -= self.gravity *dt
            if self.Actor.getZ()<=-3:
                self.is_jump = False
                self.Actor.setZ(-3)
        return task.cont

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.velocity_speed = self.jump_height
    def on_mouse_click(self):
        self.prev_mouse_pos =self.win.getPointer(0)

    def check_collision(self, craft, Actor, threshold=1.0):
        distance = (craft.getPos() - Actor.getPos()).length()
        return distance < threshold
    def update_mouse(self, task):
        if self.prev_mouse_pos is not None:
            current_mouse_pos = self.win.getPointer(0)
            delta_x = current_mouse_pos.get_x()-self.prev_mouse_pos.get_x()
            delta_y = current_mouse_pos.get_y()-self.prev_mouse_pos.get_y()

            self.angle_h += delta_x*self.mouse_sensitive
            self.angle_p += delta_y*self.mouse_sensitive
            self.angle_p = max(0, min(90, self.angle_p))

            self.prev_mouse_pos = current_mouse_pos



        radius = 50
        cam_x = self.Actor.get_x() + radius*sin(self.angle_h*(3.14/180))
        cam_y = self.Actor.get_y() + radius*cos(self.angle_h*(3.14/180))
        cam_z = self.Actor.get_z() + self.angle_p

        # Update camera to follow the panda
        self.camera.setPos(cam_x, cam_y, cam_z)
        self.camera.lookAt(self.Actor.getPos())
        return task.cont

    def npc_move(self, task):
        dt = globalClock.getDt()  # Отримуємо час між кадрами
        target_altitude = 85  # Бажана висота польоту

        for data in self.npc_data:
            npc = data["npc"]

            # Ініціалізація даних для плавного руху
            if "target_direction" not in data:
                data["target_direction"] = data["direction"]
                data["rotation_speed"] = uniform(30, 90)
                data["change_timer"] = 0
                data["target_z"] = target_altitude  # Початкова висота

            # Таймер для змін напрямку
            data["change_timer"] += dt
            if data["change_timer"] > uniform(2, 5) or random() < 0.01:
                data["change_timer"] = 0
                # Новий напрямок з випадковим відхиленням
                current_h = npc.getH()
                new_h = current_h + uniform(-45, 45)
                data["target_direction"] = Point3(
                    -math.sin(math.radians(new_h)),
                    math.cos(math.radians(new_h)),
                    uniform(-0.1, 0.1)  # Невелике відхилення по Z
                )
                data["target_direction"].normalize()
                data["rotation_speed"] = uniform(30, 90)
                # Випадкові коливання висоти біля цільової
                data["target_z"] = target_altitude + uniform(-3, 3)

            # Плавна зміна напрямку
            current_dir = data["direction"]
            target_dir = data["target_direction"]
            blend_factor = min(1.0, dt * 2)
            new_dir = current_dir * (1 - blend_factor) + target_dir * blend_factor
            new_dir.normalize()
            data["direction"] = new_dir

            # Плавна корекція висоти
            current_z = npc.getZ()
            target_z = data["target_z"]
            altitude_blend = min(100.0, dt * 5.5)  # Повільніше змінюємо висоту
            new_z = current_z + (target_z - current_z) * altitude_blend

            # Рух NPC
            speed = uniform(0.05, 0.15)
            new_pos = npc.getPos() + new_dir * speed * 60 * dt
            new_pos.setZ(new_z)
            npc.setPos(new_pos)

            # Обертання моделі
            h = math.degrees(math.atan2(-new_dir.getX(), new_dir.getY()))
            npc.setH(h+180)
            npc.setP(180)
            # Анімація крил (якщо є)
            if hasattr(npc, "getAnimControl") and npc.getAnimControl("dancing"):
                npc.setPlayRate(uniform(0.8, 1.2), "dancing")

        return task.cont


app = MyApp()
app.run()