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


    def update_enabled(self, context):
        OverrideOperator.grab_register(self, context)
    
    dir: bpy.props.EnumProperty(
        name="軸",
        items=[
            ("x", "X軸", "X軸を有効にする"),
            ("y", "Y軸", "Y軸を有効にする"),
            ("z", "Z軸", "Z軸を有効にする"),
        ],
        options={"ENUM_FLAG"}
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
    )

class RotateAssistProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_RotateAssist"
    bl_label = "MMZ Add-on RotateAssist Properties"

    print("MMZ Add-on: Properties: RotateAssist: Registered.")

    def update_enabled(self, context):
        OverrideOperator.rotate_register(self, context)
    
    dir: bpy.props.EnumProperty(
        name="軸",
        items=[
            ("x", "X軸", "X軸を有効にする"),
            ("y", "Y軸", "Y軸を有効にする"),
            ("z", "Z軸", "Z軸を有効にする"),
        ],
        options={"ENUM_FLAG"}
    )

    enabled: bpy.props.BoolProperty(
        name="モードが有効かを表す",
        description="モードが有効であるかを示します。",
        default=False,
        update=update_enabled
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
    )

class ResizeAssistProperties(bpy.types.PropertyGroup):
    bl_idname = "MMZ_PT_ResizeAssist"
    bl_label = "MMZ Add-on ResizeAssist Properties"

    print("MMZ Add-on: Properties: ResizeAssist: Registered.")

    def update_enabled(self, context):
        OverrideOperator.resize_register(self, context)

    dir: bpy.props.EnumProperty(
        name="軸",
        items=[
            ("x", "X軸", "X軸を有効にする"),
            ("y", "Y軸", "Y軸を有効にする"),
            ("z", "Z軸", "Z軸を有効にする"),
        ],
        options={"ENUM_FLAG"}
    )

    enabled: bpy.props.BoolProperty(
        name="モードが有効かを表す",
        description="モードが有効であるかを示します。",
        default=False,
        update=update_enabled
    )

    multi: bpy.props.BoolProperty(
        name="複数軸",
        description="複数の軸を選択できるかを示します。",
        default=True,
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
        ResizeAssistProperties,
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
    bpy.types.Scene.resize_pro = bpy.props.PointerProperty(type=ResizeAssistProperties)
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
