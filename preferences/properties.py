import bpy
from .shortcuts import OverrideOperator

print("MMZ Add-on: Properties: loaded.")

class MMZAddonProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_properties"
    bl_label = "MMZ Add-on Properties"

    cancelextrude_checkbox: bpy.props.BoolProperty(
        name="押し出しキャンセル機能を有効にする",
        description="押し出しキャンセル機能を有効にするかどうかを設定します",
        default=False
    )

class GrabAssistProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_GrabAssist"
    bl_label = "MMZ Add-on GrabAssist Properties"

    print("MMZ Add-on: Properties: GrabAssist: Registered.")

    condition = {"latest": "x", "oldest": "x", "busy": False}

    def update_enabled(self, context):
        OverrideOperator.grab_register(self, context)
    
    def update_multi(self, context):
        x = bpy.context.scene.grab_pro.dir_x
        y = bpy.context.scene.grab_pro.dir_y
        z = bpy.context.scene.grab_pro.dir_z
        if not bpy.context.scene.grab_pro.multi:
            if [x, y, z].count(True) == 2:
                condition = self.condition
                latest = condition["latest"]
                def enable_x(self, context):
                    print("enableX")
                    bpy.context.scene.grab_pro.dir_x = True
                    bpy.context.scene.grab_pro.dir_y = False
                    bpy.context.scene.grab_pro.dir_z = False
                    condition["oldest"] = "x"
                    condition["latest"] = "x"
                def enable_y(self, context):
                    print("enableY")
                    bpy.context.scene.grab_pro.dir_x = False
                    bpy.context.scene.grab_pro.dir_y = True
                    bpy.context.scene.grab_pro.dir_z = False
                    condition["oldest"] = "y"
                    condition["latest"] = "y"
                def enable_z(self, context):
                    print("enableZ")
                    bpy.context.scene.grab_pro.dir_x = False
                    bpy.context.scene.grab_pro.dir_y = False
                    bpy.context.scene.grab_pro.dir_z = True
                    condition["oldest"] = "z"
                    condition["latest"] = "z"
                if latest == "x": enable_x(self, context)
                if latest == "y": enable_y(self, context)
                if latest == "z": enable_z(self, context)
    
    def update_dir(self, context):
         
        condition = self.condition
        latest = condition["latest"]
        oldest = condition["oldest"]
        busy = condition["busy"]
        
        if not busy:
            condition["busy"] = True

            x = bpy.context.scene.grab_pro.dir_x
            y = bpy.context.scene.grab_pro.dir_y
            z = bpy.context.scene.grab_pro.dir_z

            count = [x, y, z].count(True) #それぞれの軸のチェックが入っているか
            if count == 1:  # 軸が一つだけ選択されているとき
                if x == True:  # 選択されているのがX軸なら
                    condition["oldest"] = "x"  # latestとoldestをxに設定(以下同じ)
                    condition["latest"] = "x"
                if y == True:
                    condition["oldest"] = "y"
                    condition["latest"] = "y"
                if z == True:
                    condition["oldest"] = "z"
                    condition["latest"] = "z"
            if count >= 2:
                if bpy.context.scene.grab_pro.multi:
                    if count == 2:  # 軸が二つ選択されているとき
                        if x and not oldest == "x":  # X軸が選択されていてoldestでないなら(=新しく選択された)
                            condition["latest"] = "x"  # latestをxに設定(以下同じ)
                        if y and not oldest == "y":
                            condition["latest"] = "y"
                        if z and not oldest == "z":
                            condition["latest"] = "z"
                    elif count == 3:  # 軸が3つとも選択されているとき
                        if oldest == "x":  # oldestがxなら(=最初に選択されたのがX軸なら)
                            bpy.context.scene.grab_pro.dir_x = False  # X軸のチェックを解除する(以下同じ)
                            if latest == "y":  # latestがyなら(2つ目に選択されたのがyなら)
                                condition["latest"] = "z"  # zをlatestに設定
                                condition["oldest"] = "y"  # yをoldestに設定(以下同じ)
                            elif latest == "z":
                                condition["latest"] = "y"
                                condition["oldest"] = "z"
                        elif oldest == "y":
                            bpy.context.scene.grab_pro.dir_y = False
                            if latest == "x":
                                condition["latest"] = "z"
                                condition["oldest"] = "x"
                            elif latest == "z":
                                condition["latest"] = "x"
                                condition["oldest"] = "z"
                        elif oldest == "z":
                            bpy.context.scene.grab_pro.dir_z = False
                            if latest == "x":
                                condition["latest"] = "y"
                                condition["oldest"] = "x"
                            elif latest == "y":
                                condition["latest"] = "x"
                                condition["oldest"] = "y"
                else:
                    def enable_x(self, context):
                        print("enableX")
                        bpy.context.scene.grab_pro.dir_x = True
                        bpy.context.scene.grab_pro.dir_y = False
                        bpy.context.scene.grab_pro.dir_z = False
                        condition["oldest"] = "x"
                        condition["latest"] = "x"
                    def enable_y(self, context):
                        print("enableY")
                        bpy.context.scene.grab_pro.dir_x = False
                        bpy.context.scene.grab_pro.dir_y = True
                        bpy.context.scene.grab_pro.dir_z = False
                        condition["oldest"] = "y"
                        condition["latest"] = "y"
                    def enable_z(self, context):
                        print("enableZ")
                        bpy.context.scene.grab_pro.dir_x = False
                        bpy.context.scene.grab_pro.dir_y = False
                        bpy.context.scene.grab_pro.dir_z = True
                        condition["oldest"] = "z"
                        condition["latest"] = "z"
                    if not latest == "x" and x: enable_x(self, context)
                    elif not latest == "y" and y: enable_y(self, context)
                    elif not latest == "z" and z: enable_z(self, context)
                            
            condition["busy"] = False

    dir_x: bpy.props.BoolProperty(
        name="X軸",
        description="X軸方向への移動",
        default=False,
        update=update_dir
    )
    dir_y: bpy.props.BoolProperty(
        name="Y軸",
        description="Y軸方向への移動",
        default=False,
        update=update_dir
    )
    dir_z: bpy.props.BoolProperty(
        name="Z軸",
        description="Z軸方向への移動",
        default=False,
        update=update_dir
    )

    enabled: bpy.props.BoolProperty(
        name="モードが有効かを表す",
        description="モードが有効であるかを示します。",
        default=False,
        update=update_enabled
    )

    slide: bpy.props.BoolProperty(
        name="エッジスライドが有効かを表す",
        description="エッジスライド機能を有効にするかを表します。",
        default=False
    )

    extend: bpy.props.BoolProperty(
        name="エッジスライドの延長線モードが有効かを表す",
        description="エッジスライドの延長線モードを有効にするかを表します。",
        default=False
    )
    multi: bpy.props.BoolProperty(
        name="複数軸",
        description="複数の軸を選択できるかを示します。",
        default=True,
        update=update_multi
    )

class RotateAssistProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_RotateAssist"
    bl_label = "MMZ Add-on RotateAssist Properties"

    print("MMZ Add-on: Properties: RotateAssist: Registered.")

    condition = {"latest": "x", "oldest": "x", "busy": False}

    def update_enabled(self, context):
        OverrideOperator.rotate_register(self, context)
    
    def update_multi(self, context):
        x = bpy.context.scene.rotate_pro.dir_x
        y = bpy.context.scene.rotate_pro.dir_y
        z = bpy.context.scene.rotate_pro.dir_z
        if not bpy.context.scene.rotate_pro.multi:
            if [x, y, z].count(True) == 2:
                if x and y:
                    bpy.context.scene.rotate_pro.dir_x = False
                    bpy.context.scene.rotate_pro.dir_y = False
                    bpy.context.scene.rotate_pro.dir_z = True
                if x and z:
                    bpy.context.scene.rotate_pro.dir_x = False
                    bpy.context.scene.rotate_pro.dir_y = True
                    bpy.context.scene.rotate_pro.dir_z = False
                if y and z:
                    bpy.context.scene.rotate_pro.dir_x = True
                    bpy.context.scene.rotate_pro.dir_y = False
                    bpy.context.scene.rotate_pro.dir_z = False

    def update_dir(self, context):         
        condition = self.condition
        latest = condition["latest"]
        oldest = condition["oldest"]
        busy = condition["busy"]
        
        if not busy:
            condition["busy"] = True

            x = bpy.context.scene.rotate_pro.dir_x
            y = bpy.context.scene.rotate_pro.dir_y
            z = bpy.context.scene.rotate_pro.dir_z

            count = [x, y, z].count(True) #それぞれの軸のチェックが入っているか
            if count == 1:  # 軸が一つだけ選択されているとき
                if x == True:  # 選択されているのがX軸なら
                    condition["oldest"] = "x"  # latestとoldestをxに設定(以下同じ)
                    condition["latest"] = "x"
                if y == True:
                    condition["oldest"] = "y"
                    condition["latest"] = "y"
                if z == True:
                    condition["oldest"] = "z"
                    condition["latest"] = "z"
                latest = condition["latest"]
                oldest = condition["oldest"]
            
            if count >= 2:
                if bpy.context.scene.rotate_pro.multi:
                    if count == 2:  # 軸が二つ選択されているとき
                        if x and not oldest == "x":  # X軸が選択されていてoldestでないなら(=新しく選択された)
                            condition["latest"] = "x"  # latestをxに設定(以下同じ)
                        if y and not oldest == "y":
                            condition["latest"] = "y"
                        if z and not oldest == "z":
                            condition["latest"] = "z"
                    elif count == 3:  # 軸が3つとも選択されているとき
                        if oldest == "x":  # oldestがxなら(=最初に選択されたのがX軸なら)
                            bpy.context.scene.rotate_pro.dir_x = False  # X軸のチェックを解除する(以下同じ)
                            if latest == "y":  # latestがyなら(2つ目に選択されたのがyなら)
                                condition["latest"] = "z"  # zをlatestに設定
                                condition["oldest"] = "y"  # yをoldestに設定(以下同じ)
                            elif latest == "z":
                                condition["latest"] = "y"
                                condition["oldest"] = "z"
                        elif oldest == "y":
                            bpy.context.scene.rotate_pro.dir_y = False
                            if latest == "x":
                                condition["latest"] = "z"
                                condition["oldest"] = "x"
                            elif latest == "z":
                                condition["latest"] = "x"
                                condition["oldest"] = "z"
                        elif oldest == "z":
                            bpy.context.scene.rotate_pro.dir_z = False
                            if latest == "x":
                                condition["latest"] = "y"
                                condition["oldest"] = "x"
                            elif latest == "y":
                                condition["latest"] = "x"
                                condition["oldest"] = "y"
                else:
                    def enable_x(self, context):
                        print("enableX")
                        bpy.context.scene.rotate_pro.dir_x = True
                        bpy.context.scene.rotate_pro.dir_y = False
                        bpy.context.scene.rotate_pro.dir_z = False
                        condition["oldest"] = "x"
                        condition["latest"] = "x"
                    def enable_y(self, context):
                        print("enableY")
                        bpy.context.scene.rotate_pro.dir_x = False
                        bpy.context.scene.rotate_pro.dir_y = True
                        bpy.context.scene.rotate_pro.dir_z = False
                        condition["oldest"] = "y"
                        condition["latest"] = "y"
                    def enable_z(self, context):
                        print("enableZ")
                        bpy.context.scene.rotate_pro.dir_x = False
                        bpy.context.scene.rotate_pro.dir_y = False
                        bpy.context.scene.rotate_pro.dir_z = True
                        condition["oldest"] = "z"
                        condition["latest"] = "z"
                    if not latest == "x" and x: enable_x(self, context)
                    elif not latest == "y" and y: enable_y(self, context)
                    elif not latest == "z" and z: enable_z(self, context)
                        
            condition["busy"] = False

    dir_x: bpy.props.BoolProperty(
        name="X軸",
        description="X軸方向への移動",
        default=False,
        update=update_dir
    )
    dir_y: bpy.props.BoolProperty(
        name="Y軸",
        description="Y軸方向への移動",
        default=False,
        update=update_dir
    )
    dir_z: bpy.props.BoolProperty(
        name="Z軸",
        description="Z軸方向への移動",
        default=False,
        update=update_dir
    )

    enabled: bpy.props.BoolProperty(
        name="モードが有効かを表す",
        description="モードが有効であるかを示します。",
        default=False,
        update=update_enabled
    )

    slide: bpy.props.BoolProperty(
        name="エッジスライドが有効かを表す",
        description="エッジスライド機能を有効にするかを表します。",
        default=False
    )

    extend: bpy.props.BoolProperty(
        name="エッジスライドの延長線モードが有効かを表す",
        description="エッジスライドの延長線モードを有効にするかを表します。",
        default=False
    )
    multi: bpy.props.BoolProperty(
        name="複数軸",
        description="複数の軸を選択できるかを示します。",
        default=False,
        update=update_multi
    )

class TextSenderProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_RotateAssist"
    bl_label = "MMZ Add-on RotateAssist Properties"

    print("MMZ Add-on: Properties: TextSender: Registered.")

    text: bpy.props.StringProperty(
        name="テキスト",
        description="追加するテキスト",
        default=""
    )
    previous: bpy.props.StringProperty(
        name="入力されているテキスト",
        description="すでに入力されているテキスト",
        default=""
    )
    line_mode: bpy.props.EnumProperty(
        name="モード",
        items=[
            ("add", "追加/上書きモード", "上書きします。"),
            ("new_line", "改行モード", "改行します。"),
        ],
        default="add"
    )

class ChangeResolutionProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_ChangeResolution"
    bl_label = "MMZ Add-on ChangeResolution Properties"

    def change(self,context):
        engine = bpy.context.scene.change_resolution.render_engine #レンダリングエンジンの設定
        frame_rate = bpy.context.scene.change_resolution.frame_rate #フレームレートの設定
        resolution = bpy.context.scene.change_resolution.resolution #解像度の設定
        scene = bpy.context.scene
        
        if bpy.context.scene.change_resolution.enable: #大元の有効/無効設定
            if bpy.context.scene.change_resolution.render_engine_enabled:
                if engine == "Cycles": #Cyclesが選択されていたら
                    bpy.context.scene.render.engine = "CYCLES" #エンジンをCyclesに設定
                else: #違うなら(Eeveeなら)
                    bpy.context.scene.render.engine = "BLENDER_EEVEE" #Eeveeに設定
            if bpy.context.scene.change_resolution.frame_rate_enabled:
                scene.render.fps = int(frame_rate) #プロパティのname(フレームレート)をintにキャストして設定
            if bpy.context.scene.change_resolution.resolution_enabled:
                width, height = resolution.split("x") #プロパティのname(解像度)をxで分割
                #幅と高さをintにキャストして設定
                scene.render.resolution_x = int(width)
                scene.render.resolution_y = int(height)

    render_engine: bpy.props.EnumProperty(
        name="レンダリングエンジン",
        items=[
            ("Cycles", "Cycles", "Cyclesエンジン"),
            ("Eevee", "Eevee", "Eeveeエンジン")
        ],
        default="Cycles",
        update=change
    )
    
    #フレームレートのプロパティ
    frame_rate: bpy.props.EnumProperty(
        name="フレームレート",
        
        #============================================
        #items=[]の中で改行して
        #("[フレームレート]", "◯◯FPS(表示名)", "[評価]"),
        #の順で記入する(最初のフレームレート以外は任意)
        #============================================
        items=[
            ("24", "24FPS", "映画"),
            ("30", "30FPS", "普通"),
            ("60", "60FPS", "ヌルヌル"),
        ],
        default="30",
        update=change
    )
    resolution: bpy.props.EnumProperty(
        name="解像度",
        
        #============================================
        #items=[]の中で改行して
        #("[解像度]", "[表示名]", "([解像度])")
        #の順で記入する(同じく最初の解像度以外は任意)
        #[横x(小文字のエックス)縦]の形で書いてください。
        #============================================
        items=[
            ("1920x1080", "フルHD", "1920x1080"),
            ("2560x1440", "WQHD", "2560x1440"),
            ("3840x2160", "4K", "3840x2160"),
        ],
        default="1920x1080",
        update=change
    )
    enable: bpy.props.BoolProperty(
        name="有効",
        description="設定を有効にするか選択します。",
        default=False
    )
    render_engine_enabled: bpy.props.BoolProperty(
        name="エンジン設定",
        description="レンダリングエンジンの変更を有効にするか選択します。",
        default=True
    )
    frame_rate_enabled: bpy.props.BoolProperty(
        name="フレームレート設定",
        description="フレームレートの変更を有効にするか選択します。",
        default=True
    )
    resolution_enabled: bpy.props.BoolProperty(
        name="解像度設定",
        description="解像度の変更を有効にするか選択します。",
        default=True
    )

class AddBooleanProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_AddBoolean"
    bl_label = "MMZ Add-on Add Boolean Properties"

    print("MMZ Add-on: Properties: AddBoolean: Registered.")

    mode: bpy.props.EnumProperty(
        name="モード",
        items=[
            ("DIFFERENCE", "差分", "差分"),
            ("UNION", "合成", "合成"),
            ("INTERSECT", "交差", "交差"),
        ],
        default="DIFFERENCE",
    )

#パネルの登録
#登録するパネルクラスをまとめる関数
def register_classes():
    classes = [
        MMZAddonProperties,
        GrabAssistProperties,
        RotateAssistProperties,
        TextSenderProperties,
        ChangeResolutionProperties,
        AddBooleanProperties
    ]
    return classes

def register():
    classes = register_classes()
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.mmz_properties = bpy.props.PointerProperty(type=MMZAddonProperties)
    bpy.types.Scene.grab_pro = bpy.props.PointerProperty(type=GrabAssistProperties)
    bpy.types.Scene.rotate_pro = bpy.props.PointerProperty(type=RotateAssistProperties)
    bpy.types.Scene.textsender = bpy.props.PointerProperty(type=TextSenderProperties)
    bpy.types.Scene.change_resolution = bpy.props.PointerProperty(type=ChangeResolutionProperties)
    bpy.types.Scene.addbool = bpy.props.PointerProperty(type=AddBooleanProperties)

def unregister():
    classes = register_classes()
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.mmz_properties
    del bpy.types.Scene.grab_pro
    del bpy.types.Scene.rotate_pro
    del bpy.types.Scene.textsender
    del bpy.types.Scene.change_resolution
    del bpy.types.Scene.addbool

if __name__ == "__main__":
    register()
