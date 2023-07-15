import bpy

from ..preferences.properties import MMZAddonProperties

print("MMZ Add-on: Panel: loaded.")

class AutomergePanel(bpy.types.Panel):
    bl_label = "自動マージ"
    bl_idname = "MMZ_PT_automerge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"

    def draw(self, context):

        self.selected = False
        layout = self.layout
        scene = context.scene
        layout.row()
        layout.label(text="面・辺・頂点の選択は解除されます。")
        layout.row()
        if bpy.context.selected_objects:
            mesh_count = 0
            for obj in bpy.context.selected_objects:
                if obj.type == "MESH":
                    mesh_count = mesh_count + 1
            if mesh_count == len(bpy.context.selected_objects):
                layout.operator("mmz.automerge_operator", text="マージする")
                layout.label(text="")
            else:
                if mesh_count >= 1:
                    row = layout.row(align=False)
                    row.alert=False
                    row.operator("mmz.automerge_operator", text="マージする")
                    layout.label(text="注意:メッシュオブジェクト以外が選択されています。")
                else:
                    row = layout.row(align=False)
                    row.enabled = False
                    row.operator("mmz.automerge_operator", text="マージする")
                    layout.label(text="注意:メッシュオブジェクトが選択されていません。")

        else:
            row = layout.row(align=False)
            row.enabled = False
            row.operator("mmz.automerge_operator", text="マージする")
            layout.label(text="注意:オブジェクトが選択されていません。")
        
        return None

class ExtrudeCancelPanel(bpy.types.Panel):
    bl_label = "押し出しキャンセル"
    bl_idname = "MMZ_PT_extrudecancel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"
    
    enabled = None

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not self.enabled:
            enabled = False

        layout.operator("mmz.automerge_operator", text="マージする")
        layout.row()

        if scene.mmz_properties.cancelextrude_checkbox:
            self.call_operator()
            if not self.enabled:
                print("MMZ Add-on: ExtrudeCancel is enabled.")
                self.enabled = True
        else:
            if self.enabled:
                print("MMZ Add-on: ExtrudeCancel is disabled.")
                self.enabled = False
            
        return None


    def call_cancelextrude_operator(self):
        bpy.ops.mmz.extrudecancel_operator()

class NoticePanel(bpy.types.Panel):
    bl_idname = "MMZ_PT_Notice"
    bl_label = "使い方"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row()
        layout.label(text="デフォルトではデフォルトのキーで動きます(小泉)")

class TransformAssistPanel(bpy.types.Panel):
    bl_idname = "MMZ_PT_Transformassist"
    bl_label = "移動アシスト"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="移動軸", icon="EVENT_G")
        layout.row()

        col1 = layout.column(align=True)
        col2 = layout.column(align=True)
        box_grab_mode = col1.box()
        box_grab_dir = col2.box()
        row_grab_dir = box_grab_dir.row(align=True)

        box_grab_mode.prop(scene.grab_pro, "enabled", text="モードを有効にする")

        row_grab_dir.prop(scene.grab_pro, "dir", expand=True)  

        layout.label(text="回転軸", icon="EVENT_R")
        layout.row()
        
        col3 = layout.column(align=True)
        col4 = layout.column(align=True)
        box_rotate_mode = col3.box()
        box_rotate_dir = col4.box()
        row_rotate_dir = box_rotate_dir.row(align=True)

        box_rotate_mode.prop(scene.rotate_pro, "enabled", text="モードを有効にする")

        row_rotate_dir.prop(scene.rotate_pro, "dir", expand=True)  
        
        layout.label(text="スケール軸", icon="EVENT_S")
        layout.row()

        col5 = layout.column(align=True)
        col6 = layout.column(align=True)
        box_resize_mode = col5.box()
        box_resize_dir = col6.box()
        row_resize_dir = box_resize_dir.row(align=True)

        box_resize_mode.prop(scene.resize_pro, "enabled", text="モードを有効にする")

        row_resize_dir.prop(scene.resize_pro, "dir", expand=True)  

        if scene.grab_pro.enabled:
            col2.enabled = True
        else:
            col2.enabled = False
        if scene.rotate_pro.enabled:
            col4.enabled = True
        else:
            col4.enabled = False
        if scene.resize_pro.enabled:
            col6.enabled = True
        else:
            col6.enabled = False

class TextSenderPanel(bpy.types.Panel):
    bl_idname = "MMZ_PT_Textsender"
    bl_label = "テキスト送信"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row()
        col = layout.column(align=True)
        col.label(text="全角文字を使うときはフォントに注意！")
        col.prop(scene.textsender, "text", text="") #テキストボックス(String型のtextプロパティ)
        active_obj = bpy.context.active_object #アクティブオブジェクトを取得
        
        row = layout.row(align=False)
        if bpy.context.selected_objects: #オブジェクトが選択されていたら
            if active_obj and active_obj.type == "FONT": #アクティブオブジェクトが存在する＆テキストなら
                row.enabled = True #ボタンを有効にする
            else:
                row.enabled = False #ボタンを無効にする
        else:
            row.enabled = False #ボタンを無効にする
        row.operator("mmz.getprevioustext_operator", text="文字を取得する")
        layout.prop(scene.textsender, "line_mode", expand=True)
        layout.operator("mmz.textsender_operator", text="追加する", icon="FILE_TEXT")

class ToolsPanel(bpy.types.Panel):
    bl_idname = "MMZ_PT_Tools"
    bl_label = "ツール"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row1 = layout.row()
        row2 = layout.row()
        row1.operator("mmz.textremesh_operator", text="テキストリメッシュ", icon="FILE_TEXT")
        row1.operator("mmz.getmiddletoorigin_operator", text="原点移動", icon="TRANSFORM_ORIGINS")
        row2.operator("mmz.wireframeswitch_operator", text="表示切替", icon="MOD_WIREFRAME")
        row2.operator("mmz.applymodifier_operator", text="モディファイアを適用", icon="MODIFIER")


class AddBooleanPanel(bpy.types.Panel):
    bl_idname = "MMZ_PT_AddBoolean"
    bl_label = "クイックブーリアン"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        col = layout.column()
        
        col.label(text="ちょっとバグが残ってるかもなので重ねがけするときは注意！")
        row.prop(scene.addbool, "mode", expand=True)
        col.operator("mmz.addboolean_operator", text="ブーリアンを追加", icon="MOD_BOOLEAN")

        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        bool_length = 2
        if len(selected_obj) == bool_length:
            if active_obj:
                mesh_count = 0
                for obj in selected_obj:
                    if obj.type == "MESH":
                        mesh_count = mesh_count + 1
                if mesh_count == bool_length:
                    col.enabled = True
                else:
                    col.enabled = False
                    col.label(text="メッシュオブジェクトを2つ選択してください。")
            else:
                col.enabled = False
                col.label(text="アクティブオブジェクトがありません。")
        else:
            col.enabled = False
            col.label(text="メッシュオブジェクトを2つ選択してください。")
        

class ChangeResolutionPanel(bpy.types.Panel):
    bl_idname = "MMZ_PT_ChangeResolution"
    bl_label = "解像度変更"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMZ"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        
        #レンダリングエンジンの要素
        box1 = layout.box()
        col1 = box1.column()
        row1 = box1.row()

        #フレームレートの要素
        box2 = layout.box()
        col2 = box2.column()
        row2 = box2.row()

        #解像度の要素
        box3 = layout.box()
        col3 = box3.column()
        row3 = box3.row()
        
        row.prop(scene.change_resolution, "enable", text="設定を有効にする")

        col1.label(text="レンダリングエンジン", icon="RENDER_STILL")
        col1.prop(scene.change_resolution, "render_engine_enabled")
        row1.prop(scene.change_resolution, "render_engine", expand=True)

        col2.label(text="フレームレート", icon="RENDERLAYERS")
        col2.prop(scene.change_resolution, "frame_rate_enabled")
        row2.prop(scene.change_resolution, "frame_rate", expand=True)
        
        col3.label(text="解像度", icon="FULLSCREEN_ENTER")
        col3.prop(scene.change_resolution, "resolution_enabled")
        row3.prop(scene.change_resolution, "resolution", expand=True)

        if scene.change_resolution.enable:
            box1.enabled = True
            box2.enabled = True
            box3.enabled = True
            if scene.change_resolution.render_engine_enabled:
                row1.enabled = True
            else:
                row1.enabled = False
            if scene.change_resolution.frame_rate_enabled:
                row2.enabled = True
            else:
                row2.enabled = False
            if scene.change_resolution.resolution_enabled:
                row3.enabled = True
            else:
                row3.enabled = False
        else:
            box1.enabled = False
            box2.enabled = False
            box3.enabled = False

#パネルの登録
#登録するパネルクラスをまとめる関数
def register_classes():
    classes = [
        TransformAssistPanel,
        TextSenderPanel,
        ToolsPanel,
        AddBooleanPanel,
        ChangeResolutionPanel
    ]
    return classes

def register():
    classes = register_classes()
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    classes = register_classes()
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
